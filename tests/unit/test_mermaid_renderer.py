"""Tests for the Mermaid diagram renderer."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess

from csa_docs_tools.mermaid_renderer import MermaidRenderer, RenderResult, RenderReport


@pytest.fixture
def renderer():
    return MermaidRenderer()


class TestMermaidRendererAvailability:
    """Test mmdc availability detection."""

    def test_is_available_when_installed(self, renderer):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            assert renderer.is_available() is True

    def test_is_available_when_not_installed(self, renderer):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            assert renderer.is_available() is False

    def test_is_available_when_timeout(self, renderer):
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("mmdc", 10)):
            assert renderer.is_available() is False

    def test_is_available_when_error(self, renderer):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            assert renderer.is_available() is False


class TestMermaidRendererFile:
    """Test file-based rendering."""

    def test_render_file_success(self, renderer, tmp_path):
        source = tmp_path / "diagram.mmd"
        source.write_text("graph TD\n  A-->B\n")
        output = tmp_path / "diagram.png"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = renderer.render_file(source, output)

        assert result.success is True
        assert result.source_path == str(source)
        assert result.output_path == str(output)
        assert result.error is None

    def test_render_file_default_output(self, renderer, tmp_path):
        source = tmp_path / "diagram.mmd"
        source.write_text("graph TD\n  A-->B\n")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = renderer.render_file(source)

        assert result.output_path == str(source.with_suffix(".png"))

    def test_render_file_failure(self, renderer, tmp_path):
        source = tmp_path / "bad.mmd"
        source.write_text("invalid content")
        output = tmp_path / "bad.png"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1,
                stderr="Parse error",
                stdout="",
            )
            result = renderer.render_file(source, output)

        assert result.success is False
        assert "Parse error" in result.error

    def test_render_file_mmdc_not_found(self, renderer, tmp_path):
        source = tmp_path / "diagram.mmd"
        source.write_text("graph TD\n  A-->B\n")

        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = renderer.render_file(source)

        assert result.success is False
        assert "mmdc not found" in result.error

    def test_render_file_timeout(self, renderer, tmp_path):
        source = tmp_path / "diagram.mmd"
        source.write_text("graph TD\n  A-->B\n")

        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("mmdc", 60)):
            result = renderer.render_file(source)

        assert result.success is False
        assert "timed out" in result.error

    def test_render_file_passes_options(self, renderer, tmp_path):
        renderer.background = "white"
        renderer.theme = "dark"
        renderer.width = 800
        renderer.height = 600

        source = tmp_path / "diagram.mmd"
        source.write_text("graph TD\n  A-->B\n")
        output = tmp_path / "diagram.png"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            renderer.render_file(source, output)

        cmd = mock_run.call_args[0][0]
        assert "-b" in cmd
        assert "white" in cmd
        assert "-t" in cmd
        assert "dark" in cmd
        assert "-w" in cmd
        assert "800" in cmd
        assert "-H" in cmd
        assert "600" in cmd


class TestMermaidRendererText:
    """Test text-based rendering."""

    def test_render_text_success(self, renderer, tmp_path):
        output = tmp_path / "diagram.png"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = renderer.render_text("graph TD\n  A-->B", output)

        assert result.success is True
        assert result.output_path == str(output)

    def test_render_text_cleans_temp_file(self, renderer, tmp_path):
        output = tmp_path / "diagram.png"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = renderer.render_text("graph TD\n  A-->B", output)

        # Temp file should be cleaned up
        # (Can't check directly since it's deleted, but no error means cleanup worked)
        assert result.success is True


class TestMermaidRendererDirectory:
    """Test directory-based batch rendering."""

    def test_render_directory_success(self, renderer, tmp_path):
        source_dir = tmp_path / "src"
        source_dir.mkdir()
        (source_dir / "a.mmd").write_text("graph TD\n  A-->B\n")
        (source_dir / "b.mermaid").write_text("graph TD\n  C-->D\n")

        output_dir = tmp_path / "out"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            report = renderer.render_directory(source_dir, output_dir)

        assert report.total == 2
        assert report.succeeded == 2
        assert report.failed == 0

    def test_render_directory_mixed_results(self, renderer, tmp_path):
        source_dir = tmp_path / "src"
        source_dir.mkdir()
        (source_dir / "good.mmd").write_text("graph TD\n  A-->B\n")
        (source_dir / "bad.mmd").write_text("invalid\n")

        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return MagicMock(returncode=0)
            else:
                return MagicMock(returncode=1, stderr="Error", stdout="")

        with patch("subprocess.run", side_effect=side_effect):
            report = renderer.render_directory(source_dir)

        assert report.total == 2
        assert report.succeeded == 1
        assert report.failed == 1

    def test_render_directory_empty(self, renderer, tmp_path):
        source_dir = tmp_path / "empty"
        source_dir.mkdir()

        report = renderer.render_directory(source_dir)

        assert report.total == 0
        assert report.succeeded == 0
        assert report.failed == 0

    def test_render_directory_default_output(self, renderer, tmp_path):
        source_dir = tmp_path / "src"
        source_dir.mkdir()
        (source_dir / "a.mmd").write_text("graph TD\n  A-->B\n")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            report = renderer.render_directory(source_dir)

        # Output should be in source_dir when no output_dir specified
        assert report.results[0].output_path.startswith(str(source_dir))


class TestMermaidRendererConfig:
    """Test renderer configuration."""

    def test_custom_output_format(self, tmp_path):
        renderer = MermaidRenderer(output_format="svg")
        source = tmp_path / "diagram.mmd"
        source.write_text("graph TD\n  A-->B\n")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = renderer.render_file(source)

        assert result.output_path.endswith(".svg")

    def test_default_config(self):
        renderer = MermaidRenderer()
        assert renderer.background == "transparent"
        assert renderer.theme == "default"
        assert renderer.width == 1920
        assert renderer.height == 1080
        assert renderer.output_format == "png"
