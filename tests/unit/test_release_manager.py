"""Unit tests for ReleaseManager."""

import pytest
from pathlib import Path
from unittest.mock import patch, Mock
import yaml

from csa_docs_tools.release_manager import ReleaseManager, ReleaseCheck


class TestReleaseManager:
    """Test cases for ReleaseManager."""

    @pytest.fixture
    def release_root(self, tmp_path):
        """Create a temporary release-ready directory."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "index.md").write_text("# Test Documentation")

        config = {'site_name': 'Test Site', 'docs_dir': 'docs'}
        with open(tmp_path / "mkdocs.yml", 'w') as f:
            yaml.dump(config, f)

        return tmp_path

    @pytest.mark.unit
    def test_init(self, release_root):
        """Test ReleaseManager initialization."""
        manager = ReleaseManager(release_root)
        assert manager.repo_path == release_root
        assert manager.mkdocs_config == release_root / "mkdocs.yml"
        assert manager.docs_dir == release_root / "docs"

    @pytest.mark.unit
    def test_validate_release_readiness_pass(self, release_root):
        """Test release readiness with valid setup."""
        manager = ReleaseManager(release_root)

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(stdout="", returncode=0)
            is_ready, issues = manager.validate_release_readiness("1.0.0")

        assert is_ready
        assert len(issues) == 0

    @pytest.mark.unit
    def test_validate_release_readiness_no_config(self, tmp_path):
        """Test readiness when mkdocs.yml is missing."""
        (tmp_path / "docs").mkdir()
        manager = ReleaseManager(tmp_path)

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(stdout="", returncode=0)
            is_ready, issues = manager.validate_release_readiness("1.0.0")

        assert not is_ready
        assert any("mkdocs.yml" in i for i in issues)

    @pytest.mark.unit
    def test_validate_release_readiness_no_docs(self, tmp_path):
        """Test readiness when docs/ is missing."""
        config = {'site_name': 'Test'}
        with open(tmp_path / "mkdocs.yml", 'w') as f:
            yaml.dump(config, f)

        manager = ReleaseManager(tmp_path)

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(stdout="", returncode=0)
            is_ready, issues = manager.validate_release_readiness("1.0.0")

        assert not is_ready
        assert any("docs" in i.lower() for i in issues)

    @pytest.mark.unit
    def test_validate_release_readiness_dirty_worktree(self, release_root):
        """Test readiness with uncommitted changes."""
        manager = ReleaseManager(release_root)

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(stdout="M file.py\n", returncode=0)
            is_ready, issues = manager.validate_release_readiness("1.0.0")

        assert not is_ready
        assert any("uncommitted" in i.lower() for i in issues)

    @pytest.mark.unit
    def test_validate_release_readiness_bad_version(self, release_root):
        """Test readiness with invalid version format."""
        manager = ReleaseManager(release_root)

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(stdout="", returncode=0)
            is_ready, issues = manager.validate_release_readiness("not-a-version")

        assert not is_ready
        assert any("version" in i.lower() for i in issues)

    @pytest.mark.unit
    def test_generate_changelog_empty(self, release_root):
        """Test changelog generation with no commits."""
        manager = ReleaseManager(release_root)

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(stdout="", returncode=0)
            changelog = manager.generate_changelog("v0.9.0", "v1.0.0")

        assert "Changelog" in changelog
        assert "v0.9.0" in changelog
        assert "v1.0.0" in changelog
        assert "No notable changes" in changelog

    @pytest.mark.unit
    def test_generate_changelog_with_commits(self, release_root):
        """Test changelog generation with categorized commits."""
        manager = ReleaseManager(release_root)

        commit_log = "feat: add new feature\nfix: bug fix\ndocs: update readme\nchore: cleanup"
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(stdout=commit_log, returncode=0)
            changelog = manager.generate_changelog("v0.9.0", "v1.0.0")

        assert "Features" in changelog
        assert "Bug Fixes" in changelog
        assert "Documentation" in changelog
        assert "Other" in changelog

    @pytest.mark.unit
    def test_generate_changelog_git_error(self, release_root):
        """Test changelog generation when git fails."""
        manager = ReleaseManager(release_root)

        with patch('subprocess.run', side_effect=Exception("git not found")):
            changelog = manager.generate_changelog("v0.9.0", "v1.0.0")

        assert "No notable changes" in changelog

    @pytest.mark.unit
    def test_get_release_metadata(self, release_root):
        """Test release metadata generation."""
        manager = ReleaseManager(release_root)
        metadata = manager.get_release_metadata("1.0.0")

        assert metadata['version'] == '1.0.0'
        assert 'release_date' in metadata
        assert metadata['docs_exist'] is True
        assert metadata['config_exists'] is True

    @pytest.mark.unit
    def test_get_release_metadata_missing_docs(self, tmp_path):
        """Test metadata when docs don't exist."""
        manager = ReleaseManager(tmp_path)
        metadata = manager.get_release_metadata("1.0.0")

        assert metadata['docs_exist'] is False

    @pytest.mark.unit
    def test_check_mkdocs_config_empty(self, tmp_path):
        """Test config check with empty mkdocs.yml."""
        (tmp_path / "mkdocs.yml").write_text("")
        manager = ReleaseManager(tmp_path)
        check = manager._check_mkdocs_config()
        assert not check.passed

    @pytest.mark.unit
    def test_check_mkdocs_config_no_site_name(self, tmp_path):
        """Test config check without site_name."""
        with open(tmp_path / "mkdocs.yml", 'w') as f:
            yaml.dump({'plugins': ['search']}, f)
        manager = ReleaseManager(tmp_path)
        check = manager._check_mkdocs_config()
        assert not check.passed
        assert "site_name" in check.message

    @pytest.mark.unit
    def test_check_uncommitted_git_error(self, tmp_path):
        """Test uncommitted check when git fails."""
        manager = ReleaseManager(tmp_path)
        with patch('subprocess.run', side_effect=Exception("git error")):
            check = manager._check_uncommitted_changes()
        assert not check.passed
