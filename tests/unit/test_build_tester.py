"""Unit tests for DocumentationBuildTester."""

import pytest
import subprocess
from pathlib import Path
from unittest.mock import patch, Mock
import yaml
import tempfile

from src.csa_docs_tools.build_tester import DocumentationBuildTester


class TestDocumentationBuildTester:
    """Test cases for DocumentationBuildTester class."""

    @pytest.mark.unit
    def test_init(self, temp_docs_root):
        """Test DocumentationBuildTester initialization."""
        tester = DocumentationBuildTester(temp_docs_root)
        
        assert tester.docs_root == Path(temp_docs_root)
        assert tester.mkdocs_config == Path(temp_docs_root) / "mkdocs.yml"

    @pytest.mark.unit
    def test_validate_mkdocs_config_valid(self, build_tester):
        """Test validation of valid mkdocs.yml."""
        is_valid, errors = build_tester.validate_mkdocs_config()
        
        assert is_valid
        assert len(errors) == 0

    @pytest.mark.unit
    def test_validate_mkdocs_config_missing_file(self, tmp_path):
        """Test validation when mkdocs.yml is missing."""
        tester = DocumentationBuildTester(tmp_path)
        
        is_valid, errors = tester.validate_mkdocs_config()
        
        assert not is_valid
        assert len(errors) == 1
        assert "not found" in errors[0]

    @pytest.mark.unit
    def test_validate_mkdocs_config_invalid_yaml(self, tmp_path):
        """Test validation with invalid YAML."""
        # Create invalid YAML file
        mkdocs_file = tmp_path / "mkdocs.yml"
        mkdocs_file.write_text("invalid: yaml: content: [unclosed")
        
        tester = DocumentationBuildTester(tmp_path)
        is_valid, errors = tester.validate_mkdocs_config()
        
        assert not is_valid
        assert len(errors) == 1
        assert "Invalid YAML" in errors[0]

    @pytest.mark.unit
    def test_validate_mkdocs_config_missing_required_fields(self, tmp_path):
        """Test validation with missing required fields."""
        # Create mkdocs.yml without required fields
        config = {"plugins": ["search"]}
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        tester = DocumentationBuildTester(tmp_path)
        is_valid, errors = tester.validate_mkdocs_config()
        
        assert not is_valid
        assert any("site_name" in error for error in errors)
        assert any("docs_dir" in error for error in errors)

    @pytest.mark.unit
    def test_validate_mkdocs_config_missing_docs_dir(self, tmp_path):
        """Test validation when docs_dir doesn't exist."""
        config = {
            "site_name": "Test Site",
            "docs_dir": "nonexistent_docs"
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        tester = DocumentationBuildTester(tmp_path)
        is_valid, errors = tester.validate_mkdocs_config()
        
        assert not is_valid
        assert any("Documentation directory not found" in error for error in errors)

    @pytest.mark.unit
    def test_validate_mkdocs_config_theme_validation(self, tmp_path):
        """Test theme configuration validation."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        # Test with invalid theme config
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs",
            "theme": {"invalid": "config"}  # Missing 'name'
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        tester = DocumentationBuildTester(tmp_path)
        is_valid, errors = tester.validate_mkdocs_config()
        
        assert not is_valid
        assert any("Theme name not specified" in error for error in errors)

    @pytest.mark.unit
    def test_test_build_success(self, build_tester, mock_subprocess_success):
        """Test successful documentation build."""
        success, stdout, stderr = build_tester.test_build()
        
        assert success
        assert "completed successfully" in stdout
        assert stderr == ""
        
        # Verify mkdocs build was called
        mock_subprocess_success.assert_called_once()
        args = mock_subprocess_success.call_args[0][0]
        assert "mkdocs" in args
        assert "build" in args

    @pytest.mark.unit
    def test_test_build_failure(self, build_tester, mock_subprocess_failure):
        """Test failed documentation build."""
        success, stdout, stderr = build_tester.test_build()
        
        assert not success
        assert stdout == ""
        assert "Build failed" in stderr

    @pytest.mark.unit
    def test_test_build_strict_mode(self, build_tester, mock_subprocess_success):
        """Test build with strict mode enabled."""
        build_tester.test_build(strict=True)
        
        # Verify --strict was passed
        args = mock_subprocess_success.call_args[0][0]
        assert "--strict" in args

    @pytest.mark.unit
    def test_test_build_timeout(self, build_tester):
        """Test build timeout handling."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(
                cmd=["mkdocs", "build"], 
                timeout=300
            )
            
            success, stdout, stderr = build_tester.test_build()
            
            assert not success
            assert "timed out" in stderr

    @pytest.mark.unit
    def test_validate_nav_structure_valid(self, build_tester):
        """Test navigation structure validation with valid nav."""
        is_valid, errors = build_tester.validate_nav_structure()
        
        assert is_valid
        assert len(errors) == 0

    @pytest.mark.unit
    def test_validate_nav_structure_no_nav(self, tmp_path):
        """Test navigation validation when no nav is defined."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs"
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        tester = DocumentationBuildTester(tmp_path)
        is_valid, errors = tester.validate_nav_structure()
        
        assert is_valid  # No nav is valid
        assert len(errors) == 0

    @pytest.mark.unit
    def test_validate_nav_structure_missing_files(self, tmp_path):
        """Test navigation validation with missing files."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs",
            "nav": [
                {"Home": "index.md"},
                {"Missing": "nonexistent.md"}
            ]
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        tester = DocumentationBuildTester(tmp_path)
        is_valid, errors = tester.validate_nav_structure()
        
        assert not is_valid
        assert len(errors) >= 1
        assert any("nonexistent.md" in error for error in errors)

    @pytest.mark.unit
    def test_get_build_statistics(self, build_tester):
        """Test build statistics generation."""
        with patch.object(build_tester, 'test_build', return_value=(True, "", "")):
            stats = build_tester.get_build_statistics()
            
            assert isinstance(stats, dict)
            assert 'total_markdown_files' in stats
            assert 'total_assets' in stats
            assert 'config_valid' in stats
            assert 'nav_valid' in stats
            assert 'build_successful' in stats
            
            assert stats['total_markdown_files'] > 0
            assert stats['config_valid']
            assert stats['nav_valid']
            assert stats['build_successful']

    @pytest.mark.unit
    def test_check_plugin_dependencies_no_plugins(self, tmp_path):
        """Test plugin dependency check with no plugins."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs"
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        tester = DocumentationBuildTester(tmp_path)
        all_available, missing = tester.check_plugin_dependencies()
        
        assert all_available
        assert len(missing) == 0

    @pytest.mark.unit
    def test_check_plugin_dependencies_with_plugins(self, build_tester):
        """Test plugin dependency check with plugins."""
        all_available, missing = build_tester.check_plugin_dependencies()
        
        # Since we have 'search' plugin in the config
        assert isinstance(all_available, bool)
        assert isinstance(missing, list)

    @pytest.mark.unit
    def test_validate_nav_items_recursive(self, build_tester):
        """Test recursive navigation item validation."""
        # This tests the private method indirectly through validate_nav_structure
        is_valid, errors = build_tester.validate_nav_structure()
        
        # Should handle nested navigation properly
        assert isinstance(is_valid, bool)
        assert isinstance(errors, list)

    @pytest.mark.unit
    def test_error_handling_in_validation(self, tmp_path):
        """Test error handling in various validation methods."""
        # Test with permission denied scenario (simulated)
        tester = DocumentationBuildTester(tmp_path)
        
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            is_valid, errors = tester.validate_mkdocs_config()
            
            assert not is_valid
            assert len(errors) > 0
            assert any("Permission denied" in error for error in errors)

    @pytest.mark.unit
    def test_build_with_custom_site_dir(self, build_tester):
        """Test build with custom site directory."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="", stderr="")
            
            build_tester.test_build()
            
            # Verify temporary directory was used
            args = mock_run.call_args[0][0]
            assert "--site-dir" in args
            site_dir_index = args.index("--site-dir") + 1
            assert args[site_dir_index].startswith("/tmp") or "tmp" in args[site_dir_index]

    @pytest.mark.unit
    def test_config_edge_cases(self, tmp_path):
        """Test edge cases in configuration validation."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        # Test with string theme instead of dict
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs",
            "theme": "material"  # String instead of dict
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        tester = DocumentationBuildTester(tmp_path)
        is_valid, errors = tester.validate_mkdocs_config()
        
        assert is_valid  # String theme is valid
        assert len(errors) == 0

    @pytest.mark.unit
    def test_navigation_validation_edge_cases(self, tmp_path):
        """Test edge cases in navigation validation."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "index.md").write_text("# Test")
        
        # Test with complex nested navigation
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs",
            "nav": [
                "index.md",  # Simple string
                {"Section": [
                    {"Subsection": [
                        {"Deep": "index.md"}
                    ]}
                ]}
            ]
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        tester = DocumentationBuildTester(tmp_path)
        is_valid, errors = tester.validate_nav_structure()
        
        assert is_valid
        assert len(errors) == 0