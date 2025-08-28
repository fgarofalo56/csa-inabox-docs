"""Tests for version management functionality."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from packaging.version import Version as PackagingVersion

from src.csa_docs_tools.version_manager import (
    SemanticVersionManager,
    VersionInfo,
    VersionType,
    ReleaseType,
    validate_version_constraints
)


class TestSemanticVersionManager:
    """Test cases for SemanticVersionManager."""
    
    def test_parse_version_valid_formats(self):
        """Test parsing of valid semantic version formats."""
        manager = SemanticVersionManager()
        
        # Test basic versions
        result = manager.parse_version("1.2.3")
        assert result['major'] == 1
        assert result['minor'] == 2
        assert result['patch'] == 3
        assert result['prerelease'] is None
        assert result['build'] is None
        
        # Test version with v prefix
        result = manager.parse_version("v2.0.0")
        assert result['major'] == 2
        assert result['minor'] == 0
        assert result['patch'] == 0
        
        # Test prerelease version
        result = manager.parse_version("1.0.0-alpha.1")
        assert result['major'] == 1
        assert result['minor'] == 0
        assert result['patch'] == 0
        assert result['prerelease'] == 'alpha.1'
        
        # Test version with build metadata
        result = manager.parse_version("1.0.0+build.123")
        assert result['build'] == 'build.123'
        
        # Test full version
        result = manager.parse_version("v2.1.0-beta.2+build.456")
        assert result['major'] == 2
        assert result['minor'] == 1
        assert result['patch'] == 0
        assert result['prerelease'] == 'beta.2'
        assert result['build'] == 'build.456'
    
    def test_parse_version_invalid_formats(self):
        """Test parsing of invalid version formats."""
        manager = SemanticVersionManager()
        
        with pytest.raises(ValueError):
            manager.parse_version("1.2")
        
        with pytest.raises(ValueError):
            manager.parse_version("invalid")
        
        with pytest.raises(ValueError):
            manager.parse_version("1.2.3.4")
        
        with pytest.raises(ValueError):
            manager.parse_version("")
    
    def test_compare_versions(self):
        """Test version comparison functionality."""
        manager = SemanticVersionManager()
        
        # Test equal versions
        assert manager.compare_versions("1.2.3", "1.2.3") == 0
        assert manager.compare_versions("v1.2.3", "1.2.3") == 0
        
        # Test version ordering
        assert manager.compare_versions("1.2.3", "1.2.4") == -1
        assert manager.compare_versions("1.2.4", "1.2.3") == 1
        
        assert manager.compare_versions("1.2.3", "1.3.0") == -1
        assert manager.compare_versions("1.3.0", "1.2.3") == 1
        
        assert manager.compare_versions("1.2.3", "2.0.0") == -1
        assert manager.compare_versions("2.0.0", "1.2.3") == 1
        
        # Test prerelease versions
        assert manager.compare_versions("1.0.0-alpha", "1.0.0") == -1
        assert manager.compare_versions("1.0.0", "1.0.0-alpha") == 1
        
        assert manager.compare_versions("1.0.0-alpha", "1.0.0-beta") == -1
        assert manager.compare_versions("1.0.0-beta", "1.0.0-alpha") == 1
    
    def test_determine_release_type(self):
        """Test release type determination."""
        manager = SemanticVersionManager()
        
        # Test major release
        assert manager.determine_release_type("1.2.3", "2.0.0") == ReleaseType.MAJOR
        
        # Test minor release
        assert manager.determine_release_type("1.2.3", "1.3.0") == ReleaseType.MINOR
        
        # Test patch release
        assert manager.determine_release_type("1.2.3", "1.2.4") == ReleaseType.PATCH
        
        # Test prerelease
        assert manager.determine_release_type("1.2.3", "1.2.4-alpha.1") == ReleaseType.PRERELEASE
    
    def test_bump_version(self):
        """Test version bumping functionality."""
        manager = SemanticVersionManager()
        
        # Test major bump
        assert manager.bump_version("1.2.3", ReleaseType.MAJOR) == "2.0.0"
        
        # Test minor bump
        assert manager.bump_version("1.2.3", ReleaseType.MINOR) == "1.3.0"
        
        # Test patch bump
        assert manager.bump_version("1.2.3", ReleaseType.PATCH) == "1.2.4"
        
        # Test prerelease bump
        result = manager.bump_version("1.2.3", ReleaseType.PRERELEASE, "alpha")
        assert result == "1.2.3-alpha.1"
    
    @patch('pathlib.Path.exists')
    @patch('builtins.open')
    def test_load_versions_empty_file(self, mock_open, mock_exists):
        """Test loading versions from empty configuration."""
        mock_exists.return_value = False
        
        manager = SemanticVersionManager(Path("test.yml"))
        assert len(manager.versions) == 0
    
    @patch('pathlib.Path.exists')
    @patch('builtins.open')
    @patch('yaml.safe_load')
    def test_load_versions_with_data(self, mock_yaml_load, mock_open, mock_exists):
        """Test loading versions with existing data."""
        mock_exists.return_value = True
        mock_yaml_load.return_value = {
            'versions': [
                {
                    'version': '1.0.0',
                    'version_type': 'stable',
                    'title': 'Version 1.0.0',
                    'aliases': ['latest'],
                    'is_default': True
                }
            ]
        }
        
        manager = SemanticVersionManager(Path("test.yml"))
        assert len(manager.versions) == 1
        assert manager.versions[0].version == '1.0.0'
        assert manager.versions[0].version_type == VersionType.STABLE
    
    def test_add_version(self):
        """Test adding new version."""
        with patch('pathlib.Path.exists', return_value=False):
            manager = SemanticVersionManager(Path("test.yml"))
        
        version_info = VersionInfo(
            version="1.0.0",
            version_type=VersionType.STABLE,
            title="Test Version",
            aliases=["latest"]
        )
        
        with patch.object(manager, '_save_versions') as mock_save:
            manager.add_version(version_info)
            mock_save.assert_called_once()
        
        assert len(manager.versions) == 1
        assert manager.versions[0].version == "1.0.0"
    
    def test_add_duplicate_version(self):
        """Test adding duplicate version raises error."""
        with patch('pathlib.Path.exists', return_value=False):
            manager = SemanticVersionManager(Path("test.yml"))
        
        version_info = VersionInfo(
            version="1.0.0",
            version_type=VersionType.STABLE,
            title="Test Version",
            aliases=[]
        )
        
        with patch.object(manager, '_save_versions'):
            manager.add_version(version_info)
        
        # Try to add the same version again
        with pytest.raises(ValueError, match="Version 1.0.0 already exists"):
            manager.add_version(version_info)
    
    def test_get_latest_version(self):
        """Test getting latest stable version."""
        with patch('pathlib.Path.exists', return_value=False):
            manager = SemanticVersionManager(Path("test.yml"))
        
        # No versions
        assert manager.get_latest_version() is None
        
        # Add versions
        versions = [
            VersionInfo("1.0.0", VersionType.STABLE, "v1.0.0", []),
            VersionInfo("2.0.0", VersionType.STABLE, "v2.0.0", []),
            VersionInfo("1.5.0", VersionType.STABLE, "v1.5.0", []),
            VersionInfo("2.1.0-alpha", VersionType.PRERELEASE, "v2.1.0-alpha", [])
        ]
        
        with patch.object(manager, '_save_versions'):
            for version in versions:
                manager.add_version(version)
        
        latest = manager.get_latest_version()
        assert latest == "2.0.0"  # Should be latest stable, not prerelease
    
    def test_get_compatible_versions(self):
        """Test getting compatible versions."""
        with patch('pathlib.Path.exists', return_value=False):
            manager = SemanticVersionManager(Path("test.yml"))
        
        versions = [
            VersionInfo("1.0.0", VersionType.STABLE, "v1.0.0", []),
            VersionInfo("1.1.0", VersionType.STABLE, "v1.1.0", []),
            VersionInfo("2.0.0", VersionType.STABLE, "v2.0.0", []),
            VersionInfo("2.1.0", VersionType.STABLE, "v2.1.0", [])
        ]
        
        with patch.object(manager, '_save_versions'):
            for version in versions:
                manager.add_version(version)
        
        compatible = manager.get_compatible_versions("1.2.0")
        assert "1.0.0" in compatible
        assert "1.1.0" in compatible
        assert "2.0.0" not in compatible  # Different major version
        assert "2.1.0" not in compatible


class TestVersionInfo:
    """Test cases for VersionInfo dataclass."""
    
    def test_valid_version_info(self):
        """Test creating valid version info."""
        version_info = VersionInfo(
            version="1.0.0",
            version_type=VersionType.STABLE,
            title="Test Version",
            aliases=["latest"]
        )
        
        assert version_info.version == "1.0.0"
        assert version_info.version_type == VersionType.STABLE
        assert version_info.title == "Test Version"
        assert version_info.aliases == ["latest"]
        assert not version_info.is_default
    
    def test_invalid_version_format(self):
        """Test that invalid version format raises error."""
        with pytest.raises(ValueError, match="Invalid version format"):
            VersionInfo(
                version="invalid",
                version_type=VersionType.STABLE,
                title="Test",
                aliases=[]
            )
    
    def test_empty_version(self):
        """Test that empty version raises error."""
        with pytest.raises(ValueError, match="Version cannot be empty"):
            VersionInfo(
                version="",
                version_type=VersionType.STABLE,
                title="Test",
                aliases=[]
            )
    
    def test_empty_title(self):
        """Test that empty title raises error."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            VersionInfo(
                version="1.0.0",
                version_type=VersionType.STABLE,
                title="",
                aliases=[]
            )


class TestValidateVersionConstraints:
    """Test cases for version constraint validation."""
    
    def test_valid_version_list(self):
        """Test validation of valid version list."""
        versions = ["1.0.0", "1.1.0", "1.2.0", "2.0.0"]
        is_valid, errors = validate_version_constraints(versions)
        
        assert is_valid
        assert len(errors) == 0
    
    def test_duplicate_versions(self):
        """Test validation fails with duplicate versions."""
        versions = ["1.0.0", "1.1.0", "1.0.0", "2.0.0"]
        is_valid, errors = validate_version_constraints(versions)
        
        assert not is_valid
        assert any("Duplicate versions" in error for error in errors)
    
    def test_invalid_version_format(self):
        """Test validation fails with invalid version format."""
        versions = ["1.0.0", "invalid", "2.0.0"]
        is_valid, errors = validate_version_constraints(versions)
        
        assert not is_valid
        assert any("Invalid version format" in error for error in errors)
    
    def test_unsorted_versions(self):
        """Test validation fails with unsorted versions."""
        versions = ["2.0.0", "1.0.0", "1.1.0"]
        is_valid, errors = validate_version_constraints(versions)
        
        assert not is_valid
        assert any("not in ascending order" in error for error in errors)
    
    def test_empty_version_list(self):
        """Test validation of empty version list."""
        versions = []
        is_valid, errors = validate_version_constraints(versions)
        
        assert is_valid
        assert len(errors) == 0


@pytest.fixture
def temp_config_file(tmp_path):
    """Create temporary configuration file for testing."""
    config_file = tmp_path / "versions.yml"
    return config_file


@pytest.fixture
def sample_version_data():
    """Sample version data for testing."""
    return {
        'versions': [
            {
                'version': '1.0.0',
                'version_type': 'stable',
                'title': 'Version 1.0.0',
                'aliases': ['v1'],
                'is_default': False,
                'release_date': '2023-01-01'
            },
            {
                'version': '2.0.0',
                'version_type': 'stable',
                'title': 'Version 2.0.0',
                'aliases': ['latest', 'v2'],
                'is_default': True,
                'release_date': '2023-06-01'
            }
        ]
    }


class TestSemanticVersionManagerIntegration:
    """Integration tests for SemanticVersionManager."""
    
    def test_save_and_load_versions(self, temp_config_file, sample_version_data):
        """Test saving and loading versions to/from file."""
        # Create manager and add versions
        manager = SemanticVersionManager(temp_config_file)
        
        version1 = VersionInfo(
            version="1.0.0",
            version_type=VersionType.STABLE,
            title="Version 1.0.0",
            aliases=["v1"],
            release_date="2023-01-01"
        )
        
        version2 = VersionInfo(
            version="2.0.0",
            version_type=VersionType.STABLE,
            title="Version 2.0.0",
            aliases=["latest", "v2"],
            is_default=True,
            release_date="2023-06-01"
        )
        
        manager.add_version(version1)
        manager.add_version(version2)
        
        # Create new manager instance to test loading
        new_manager = SemanticVersionManager(temp_config_file)
        
        assert len(new_manager.versions) == 2
        
        loaded_version1 = new_manager.get_version_info("1.0.0")
        assert loaded_version1 is not None
        assert loaded_version1.title == "Version 1.0.0"
        assert loaded_version1.aliases == ["v1"]
        
        loaded_version2 = new_manager.get_version_info("2.0.0")
        assert loaded_version2 is not None
        assert loaded_version2.title == "Version 2.0.0"
        assert loaded_version2.is_default
    
    def test_version_operations(self, temp_config_file):
        """Test various version operations."""
        manager = SemanticVersionManager(temp_config_file)
        
        # Add test versions
        versions = [
            VersionInfo("1.0.0", VersionType.STABLE, "v1.0.0", []),
            VersionInfo("1.1.0", VersionType.STABLE, "v1.1.0", []),
            VersionInfo("2.0.0-alpha", VersionType.PRERELEASE, "v2.0.0-alpha", []),
            VersionInfo("2.0.0", VersionType.STABLE, "v2.0.0", ["latest"], True)
        ]
        
        for version in versions:
            manager.add_version(version)
        
        # Test latest version
        latest = manager.get_latest_version()
        assert latest == "2.0.0"
        
        # Test version lookup by alias
        latest_info = manager.get_version_info("latest")
        assert latest_info is not None
        assert latest_info.version == "2.0.0"
        
        # Test compatible versions
        compatible = manager.get_compatible_versions("1.5.0")
        assert "1.0.0" in compatible
        assert "1.1.0" in compatible
        assert "2.0.0" not in compatible
        
        # Test remove version
        removed = manager.remove_version("2.0.0-alpha")
        assert removed
        assert manager.get_version_info("2.0.0-alpha") is None
        
        # Test remove non-existent version
        removed = manager.remove_version("non-existent")
        assert not removed
