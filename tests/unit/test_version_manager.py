"""Unit tests for SemanticVersionManager."""

import pytest
from pathlib import Path
from unittest.mock import patch
import yaml

from csa_docs_tools.version_manager import (
    SemanticVersionManager,
    VersionInfo,
    VersionType,
)


class TestSemanticVersionManager:
    """Test cases for SemanticVersionManager."""

    @pytest.mark.unit
    def test_init_no_config(self):
        """Test initialization without config file."""
        manager = SemanticVersionManager()
        assert manager.config_path is None
        assert manager.versions == []

    @pytest.mark.unit
    def test_init_with_config(self, tmp_path):
        """Test initialization with config file."""
        config_file = tmp_path / "versions.yml"
        config_file.write_text(yaml.dump({
            'versions': [
                {
                    'version': '1.0.0',
                    'type': 'stable',
                    'title': 'v1.0.0',
                    'aliases': ['latest'],
                    'is_default': True,
                    'release_date': '2024-01-01',
                    'changelog_path': 'CHANGELOG.md',
                }
            ]
        }))
        manager = SemanticVersionManager(config_file)
        assert len(manager.versions) == 1
        assert manager.versions[0].version == '1.0.0'
        assert manager.versions[0].is_default is True

    @pytest.mark.unit
    def test_init_missing_config(self, tmp_path):
        """Test initialization when config file doesn't exist."""
        config_file = tmp_path / "nonexistent.yml"
        manager = SemanticVersionManager(config_file)
        assert manager.versions == []

    @pytest.mark.unit
    def test_parse_version_simple(self):
        """Test parsing a simple version string."""
        manager = SemanticVersionManager()
        result = manager.parse_version("1.2.3")
        assert result['major'] == 1
        assert result['minor'] == 2
        assert result['patch'] == 3
        assert result['prerelease'] is None
        assert result['build_metadata'] is None

    @pytest.mark.unit
    def test_parse_version_with_v_prefix(self):
        """Test parsing version with 'v' prefix."""
        manager = SemanticVersionManager()
        result = manager.parse_version("v2.0.1")
        assert result['major'] == 2
        assert result['minor'] == 0
        assert result['patch'] == 1

    @pytest.mark.unit
    def test_parse_version_with_prerelease(self):
        """Test parsing version with prerelease tag."""
        manager = SemanticVersionManager()
        result = manager.parse_version("1.0.0-alpha.1")
        assert result['major'] == 1
        assert result['prerelease'] == 'alpha.1'

    @pytest.mark.unit
    def test_parse_version_with_build_metadata(self):
        """Test parsing version with build metadata."""
        manager = SemanticVersionManager()
        result = manager.parse_version("1.0.0+build.123")
        assert result['build_metadata'] == 'build.123'

    @pytest.mark.unit
    def test_parse_version_invalid(self):
        """Test parsing an invalid version string."""
        manager = SemanticVersionManager()
        with pytest.raises(ValueError, match="Invalid semantic version"):
            manager.parse_version("not-a-version")

    @pytest.mark.unit
    def test_parse_version_invalid_empty(self):
        """Test parsing an empty version string."""
        manager = SemanticVersionManager()
        with pytest.raises(ValueError):
            manager.parse_version("")

    @pytest.mark.unit
    def test_compare_versions_equal(self):
        """Test comparing equal versions."""
        manager = SemanticVersionManager()
        assert manager.compare_versions("1.0.0", "1.0.0") == 0

    @pytest.mark.unit
    def test_compare_versions_major(self):
        """Test comparing versions with different majors."""
        manager = SemanticVersionManager()
        assert manager.compare_versions("1.0.0", "2.0.0") == -1
        assert manager.compare_versions("2.0.0", "1.0.0") == 1

    @pytest.mark.unit
    def test_compare_versions_minor(self):
        """Test comparing versions with different minors."""
        manager = SemanticVersionManager()
        assert manager.compare_versions("1.1.0", "1.2.0") == -1
        assert manager.compare_versions("1.2.0", "1.1.0") == 1

    @pytest.mark.unit
    def test_compare_versions_patch(self):
        """Test comparing versions with different patches."""
        manager = SemanticVersionManager()
        assert manager.compare_versions("1.0.1", "1.0.2") == -1

    @pytest.mark.unit
    def test_compare_versions_prerelease_lower(self):
        """Test that prerelease has lower precedence than release."""
        manager = SemanticVersionManager()
        assert manager.compare_versions("1.0.0-alpha", "1.0.0") == -1
        assert manager.compare_versions("1.0.0", "1.0.0-beta") == 1

    @pytest.mark.unit
    def test_compare_versions_prerelease_ordering(self):
        """Test ordering between different prereleases."""
        manager = SemanticVersionManager()
        assert manager.compare_versions("1.0.0-alpha", "1.0.0-beta") == -1

    @pytest.mark.unit
    def test_bump_version_patch(self):
        """Test patch version bump."""
        manager = SemanticVersionManager()
        assert manager.bump_version("1.0.0", "patch") == "1.0.1"

    @pytest.mark.unit
    def test_bump_version_minor(self):
        """Test minor version bump."""
        manager = SemanticVersionManager()
        assert manager.bump_version("1.2.3", "minor") == "1.3.0"

    @pytest.mark.unit
    def test_bump_version_major(self):
        """Test major version bump."""
        manager = SemanticVersionManager()
        assert manager.bump_version("1.2.3", "major") == "2.0.0"

    @pytest.mark.unit
    def test_add_version(self, tmp_path):
        """Test adding a version."""
        config_file = tmp_path / "versions.yml"
        manager = SemanticVersionManager(config_file)

        info = VersionInfo(version="1.0.0", title="v1.0.0", is_default=True)
        manager.add_version(info)

        assert len(manager.versions) == 1
        assert manager.versions[0].version == "1.0.0"
        assert config_file.exists()

    @pytest.mark.unit
    def test_add_version_clears_default(self, tmp_path):
        """Test that adding a default version clears other defaults."""
        config_file = tmp_path / "versions.yml"
        manager = SemanticVersionManager(config_file)

        v1 = VersionInfo(version="1.0.0", is_default=True)
        v2 = VersionInfo(version="2.0.0", is_default=True)

        manager.add_version(v1)
        manager.add_version(v2)

        assert manager.versions[0].version == "2.0.0"
        assert manager.versions[0].is_default is True
        assert manager.versions[1].is_default is False

    @pytest.mark.unit
    def test_add_version_replaces_existing(self, tmp_path):
        """Test that adding existing version replaces it."""
        config_file = tmp_path / "versions.yml"
        manager = SemanticVersionManager(config_file)

        v1 = VersionInfo(version="1.0.0", title="old")
        v2 = VersionInfo(version="1.0.0", title="new")

        manager.add_version(v1)
        manager.add_version(v2)

        assert len(manager.versions) == 1
        assert manager.versions[0].title == "new"

    @pytest.mark.unit
    def test_get_version_found(self):
        """Test retrieving an existing version."""
        manager = SemanticVersionManager()
        manager.versions = [VersionInfo(version="1.0.0", title="Test")]

        result = manager.get_version("1.0.0")
        assert result is not None
        assert result.title == "Test"

    @pytest.mark.unit
    def test_get_version_not_found(self):
        """Test retrieving a non-existent version."""
        manager = SemanticVersionManager()
        assert manager.get_version("9.9.9") is None

    @pytest.mark.unit
    def test_get_latest_stable(self):
        """Test getting the latest stable version."""
        manager = SemanticVersionManager()
        manager.versions = [
            VersionInfo(version="2.0.0", version_type=VersionType.STABLE),
            VersionInfo(version="1.0.0", version_type=VersionType.STABLE),
            VersionInfo(version="3.0.0-alpha", version_type=VersionType.PRERELEASE),
        ]
        latest = manager.get_latest_stable()
        assert latest is not None
        assert latest.version == "2.0.0"

    @pytest.mark.unit
    def test_get_latest_stable_none(self):
        """Test getting latest stable when none exist."""
        manager = SemanticVersionManager()
        assert manager.get_latest_stable() is None

    @pytest.mark.unit
    def test_list_versions_all(self):
        """Test listing all versions."""
        manager = SemanticVersionManager()
        manager.versions = [
            VersionInfo(version="1.0.0"),
            VersionInfo(version="1.0.0-alpha", version_type=VersionType.PRERELEASE),
        ]
        assert len(manager.list_versions()) == 2

    @pytest.mark.unit
    def test_list_versions_stable_only(self):
        """Test listing stable versions only."""
        manager = SemanticVersionManager()
        manager.versions = [
            VersionInfo(version="1.0.0"),
            VersionInfo(version="1.0.0-alpha", version_type=VersionType.PRERELEASE),
        ]
        stable = manager.list_versions(include_prerelease=False)
        assert len(stable) == 1
        assert stable[0].version == "1.0.0"

    @pytest.mark.unit
    def test_save_and_reload(self, tmp_path):
        """Test round-trip save and reload."""
        config_file = tmp_path / "versions.yml"
        manager = SemanticVersionManager(config_file)

        info = VersionInfo(
            version="1.0.0",
            version_type=VersionType.STABLE,
            title="Release 1.0",
            aliases=["latest"],
            is_default=True,
            release_date="2024-01-01",
            changelog_path="CHANGELOG.md",
        )
        manager.add_version(info)

        # Reload from file
        manager2 = SemanticVersionManager(config_file)
        assert len(manager2.versions) == 1
        v = manager2.versions[0]
        assert v.version == "1.0.0"
        assert v.title == "Release 1.0"
        assert v.aliases == ["latest"]
        assert v.is_default is True
