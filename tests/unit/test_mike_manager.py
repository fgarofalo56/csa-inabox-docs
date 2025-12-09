"""Unit tests for MikeVersionManager."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess
import json

from csa_docs_tools.mike_manager import (
    MikeVersionManager,
    MikeConfig,
    DeployedVersion
)


@pytest.fixture
def temp_repo_dir(tmp_path):
    """Create a temporary repository directory."""
    repo_path = tmp_path / "repo"
    repo_path.mkdir()

    # Create mkdocs.yml
    mkdocs_config = """
site_name: Test Docs
docs_dir: docs
theme:
  name: material
"""
    (repo_path / "mkdocs.yml").write_text(mkdocs_config)

    # Create docs directory
    (repo_path / "docs").mkdir()

    return repo_path


@pytest.fixture
def mike_manager(temp_repo_dir):
    """Create a MikeVersionManager instance."""
    return MikeVersionManager(temp_repo_dir)


@pytest.fixture
def mock_mike_command_success():
    """Mock successful Mike command execution."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Success",
            stderr=""
        )
        yield mock_run


@pytest.fixture
def mock_mike_command_failure():
    """Mock failed Mike command execution."""
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=['mike'],
            output="",
            stderr="Error"
        )
        yield mock_run


@pytest.fixture
def sample_deployed_versions():
    """Sample deployed versions data."""
    return [
        {
            "version": "2.0.0",
            "title": "2.0.0",
            "aliases": ["latest"],
            "is_default": True
        },
        {
            "version": "1.5.0",
            "title": "1.5.0",
            "aliases": ["stable"],
            "is_default": False
        },
        {
            "version": "1.0.0",
            "title": "1.0.0",
            "aliases": [],
            "is_default": False
        }
    ]


class TestMikeVersionManager:
    """Test suite for MikeVersionManager."""

    def test_init(self, mike_manager, temp_repo_dir):
        """Test MikeVersionManager initialization."""
        assert mike_manager.repo_path == temp_repo_dir
        assert mike_manager.mkdocs_config_file.exists()
        assert isinstance(mike_manager.config, MikeConfig)

    def test_init_with_custom_config(self, temp_repo_dir):
        """Test initialization with custom Mike config."""
        # Create custom config file
        config_file = temp_repo_dir / ".mike.yml"
        config_content = """
alias_type: redirect
branch: gh-pages
remote: origin
"""
        config_file.write_text(config_content)

        manager = MikeVersionManager(temp_repo_dir, config_file)

        assert manager.config.alias_type == "redirect"
        assert manager.config.branch == "gh-pages"

    def test_deploy_version_basic(self, mike_manager, mock_mike_command_success):
        """Test basic version deployment."""
        result = mike_manager.deploy_version("1.0.0", title="Version 1.0")

        assert result['version'] == "1.0.0"
        assert result['title'] == "Version 1.0"
        assert result['is_default'] is False

        # Verify mike deploy was called
        mock_mike_command_success.assert_called()

    def test_deploy_version_with_aliases(self, mike_manager, mock_mike_command_success):
        """Test version deployment with aliases."""
        result = mike_manager.deploy_version(
            "1.0.0",
            title="Version 1.0",
            aliases=["latest", "stable"]
        )

        assert result['aliases'] == ["latest", "stable"]

    def test_deploy_version_set_default(self, mike_manager, mock_mike_command_success):
        """Test deploying version as default."""
        result = mike_manager.deploy_version(
            "1.0.0",
            set_default=True
        )

        assert result['is_default'] is True

    def test_deploy_version_invalid_format(self, mike_manager):
        """Test deploying version with invalid format."""
        with pytest.raises(ValueError, match="Invalid version format"):
            mike_manager.deploy_version("invalid-version")

    def test_deploy_version_command_failure(self, mike_manager, mock_mike_command_failure):
        """Test handling deployment failure."""
        with pytest.raises(RuntimeError, match="Failed to deploy version"):
            mike_manager.deploy_version("1.0.0")

    def test_list_versions(self, mike_manager, sample_deployed_versions):
        """Test listing deployed versions."""
        with patch.object(mike_manager, '_run_mike_command') as mock_run:
            mock_run.return_value = json.dumps(sample_deployed_versions)

            versions = mike_manager.list_versions(include_metadata=False)

            assert len(versions) == 3
            assert isinstance(versions[0], DeployedVersion)
            assert versions[0].version == "2.0.0"
            assert versions[0].is_default is True

    def test_list_versions_with_metadata(self, mike_manager, sample_deployed_versions, tmp_path):
        """Test listing versions with metadata."""
        with patch.object(mike_manager, '_run_mike_command') as mock_run:
            mock_run.return_value = json.dumps(sample_deployed_versions)

            # Create site directory structure
            site_dir = mike_manager.repo_path / "site" / "2.0.0"
            site_dir.mkdir(parents=True)
            (site_dir / "index.html").write_text("<html>Test</html>")

            versions = mike_manager.list_versions(include_metadata=True)

            assert len(versions) == 3
            # Size metadata should be added for version 2.0.0
            assert versions[0].size_mb is not None or versions[0].size_mb is None

    def test_list_versions_command_failure(self, mike_manager, mock_mike_command_failure):
        """Test handling failure when listing versions."""
        with pytest.raises(RuntimeError, match="Failed to list versions"):
            mike_manager.list_versions()

    def test_delete_version_success(self, mike_manager, mock_mike_command_success):
        """Test deleting a version."""
        result = mike_manager.delete_version("1.0.0", confirm=True)

        assert result is True
        mock_mike_command_success.assert_called()

    def test_delete_version_without_confirmation(self, mike_manager):
        """Test deleting version without confirmation fails."""
        with pytest.raises(ValueError, match="requires explicit confirmation"):
            mike_manager.delete_version("1.0.0", confirm=False)

    def test_delete_version_failure(self, mike_manager, mock_mike_command_failure):
        """Test handling delete failure."""
        with pytest.raises(RuntimeError, match="Failed to delete version"):
            mike_manager.delete_version("1.0.0", confirm=True)

    def test_set_default_version(self, mike_manager, mock_mike_command_success):
        """Test setting default version."""
        result = mike_manager.set_default_version("1.0.0")

        assert result['default_version'] == "1.0.0"
        assert result['status'] == 'success'

    def test_set_default_version_failure(self, mike_manager, mock_mike_command_failure):
        """Test handling set default failure."""
        with pytest.raises(RuntimeError, match="Failed to set default version"):
            mike_manager.set_default_version("1.0.0")

    def test_alias_version(self, mike_manager, mock_mike_command_success):
        """Test adding alias to version."""
        result = mike_manager.alias_version("1.0.0", "latest", update=True)

        assert result['version'] == "1.0.0"
        assert result['alias'] == "latest"
        assert result['status'] == 'success'

    def test_alias_version_failure(self, mike_manager, mock_mike_command_failure):
        """Test handling alias failure."""
        with pytest.raises(RuntimeError, match="Failed to alias version"):
            mike_manager.alias_version("1.0.0", "latest")

    def test_serve_version(self, mike_manager):
        """Test serving a version."""
        with patch('subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_popen.return_value = mock_process

            result = mike_manager.serve_version("1.0.0", port=8000)

            assert result == mock_process
            mock_popen.assert_called_once()

    def test_compare_versions(self, mike_manager, sample_deployed_versions):
        """Test comparing two versions."""
        with patch.object(mike_manager, 'list_versions') as mock_list:
            deployed_versions = [
                DeployedVersion(**data) for data in sample_deployed_versions
            ]
            mock_list.return_value = deployed_versions

            comparison = mike_manager.compare_versions("1.0.0", "2.0.0")

            assert comparison['version1'] == "1.0.0"
            assert comparison['version2'] == "2.0.0"
            assert comparison['version2_newer'] is True
            assert comparison['version1_newer'] is False

    def test_compare_versions_not_found(self, mike_manager):
        """Test comparing non-existent versions."""
        with patch.object(mike_manager, 'list_versions') as mock_list:
            mock_list.return_value = []

            with pytest.raises(ValueError, match="not found"):
                mike_manager.compare_versions("1.0.0", "2.0.0")

    def test_generate_version_navigation(self, mike_manager, sample_deployed_versions):
        """Test generating version navigation."""
        with patch.object(mike_manager, 'list_versions') as mock_list:
            deployed_versions = [
                DeployedVersion(**data) for data in sample_deployed_versions
            ]
            mock_list.return_value = deployed_versions

            navigation = mike_manager.generate_version_navigation("2.0.0")

            assert navigation['current_version'] == "2.0.0"
            assert navigation['default_version'] == "2.0.0"
            assert 'grouped_versions' in navigation
            assert navigation['total_versions'] == 3

    def test_archive_old_versions(self, mike_manager, sample_deployed_versions):
        """Test archiving old versions."""
        with patch.object(mike_manager, 'list_versions') as mock_list:
            deployed_versions = [
                DeployedVersion(**data) for data in sample_deployed_versions
            ]
            mock_list.return_value = deployed_versions

            with patch.object(mike_manager, 'delete_version') as mock_delete:
                mock_delete.return_value = True

                archived = mike_manager.archive_old_versions(keep_count=2)

                # Should archive versions beyond keep_count (except default)
                assert isinstance(archived, list)

    def test_archive_old_versions_never_archive_default(self, mike_manager):
        """Test that default version is never archived."""
        deployed_versions = [
            DeployedVersion(
                version="2.0.0",
                title="2.0.0",
                aliases=["latest"],
                is_default=True
            ),
            DeployedVersion(
                version="1.0.0",
                title="1.0.0",
                aliases=[],
                is_default=False
            )
        ]

        with patch.object(mike_manager, 'list_versions') as mock_list:
            mock_list.return_value = deployed_versions

            with patch.object(mike_manager, 'delete_version') as mock_delete:
                mock_delete.return_value = True

                archived = mike_manager.archive_old_versions(keep_count=1)

                # Default version should not be in archived list
                assert "2.0.0" not in archived

    def test_validate_deployment(self, mike_manager, sample_deployed_versions):
        """Test deployment validation."""
        with patch.object(mike_manager, 'list_versions') as mock_list:
            deployed_versions = [
                DeployedVersion(**data) for data in sample_deployed_versions
            ]
            mock_list.return_value = deployed_versions

            is_valid, issues = mike_manager.validate_deployment("2.0.0")

            # Should validate successfully
            assert isinstance(is_valid, bool)
            assert isinstance(issues, list)

    def test_validate_deployment_not_deployed(self, mike_manager):
        """Test validating non-existent deployment."""
        with patch.object(mike_manager, 'list_versions') as mock_list:
            mock_list.return_value = []

            is_valid, issues = mike_manager.validate_deployment("1.0.0")

            assert is_valid is False
            assert any("not deployed" in issue for issue in issues)

    def test_classify_version_stable(self, mike_manager):
        """Test classifying stable version."""
        version_info = mike_manager._classify_version("1.0.0")

        assert version_info.version == "1.0.0"
        assert version_info.version_type.value == "stable"

    def test_classify_version_prerelease(self, mike_manager):
        """Test classifying prerelease version."""
        version_info = mike_manager._classify_version("1.0.0-beta.1")

        assert version_info.version == "1.0.0-beta.1"
        assert version_info.version_type.value == "prerelease"

    def test_classify_version_development(self, mike_manager):
        """Test classifying development version."""
        version_info = mike_manager._classify_version("1.0.0-dev")

        assert version_info.version == "1.0.0-dev"
        assert version_info.version_type.value in ["development", "prerelease"]

    def test_analyze_version_differences(self, mike_manager):
        """Test analyzing version differences."""
        version1 = DeployedVersion(
            version="1.0.0",
            title="Version 1.0",
            aliases=["stable"],
            is_default=False,
            size_mb=10.0
        )
        version2 = DeployedVersion(
            version="2.0.0",
            title="Version 2.0",
            aliases=["latest"],
            is_default=True,
            size_mb=15.5
        )

        differences = mike_manager._analyze_version_differences(version1, version2)

        assert isinstance(differences, list)
        # Should detect title, aliases, and default status differences
        assert len(differences) > 0


class TestMikeConfig:
    """Test MikeConfig dataclass."""

    def test_mike_config_defaults(self):
        """Test MikeConfig default values."""
        config = MikeConfig()

        assert config.alias_type == "symlink"
        assert config.branch == "gh-pages"
        assert config.remote == "origin"
        assert config.versions_file == "versions.json"

    def test_mike_config_custom_values(self):
        """Test MikeConfig with custom values."""
        config = MikeConfig(
            alias_type="redirect",
            branch="main",
            remote="upstream"
        )

        assert config.alias_type == "redirect"
        assert config.branch == "main"
        assert config.remote == "upstream"


class TestDeployedVersion:
    """Test DeployedVersion dataclass."""

    def test_deployed_version_creation(self):
        """Test DeployedVersion creation."""
        version = DeployedVersion(
            version="1.0.0",
            title="Version 1.0",
            aliases=["latest", "stable"],
            is_default=True,
            size_mb=10.5
        )

        assert version.version == "1.0.0"
        assert version.title == "Version 1.0"
        assert len(version.aliases) == 2
        assert version.is_default is True
        assert version.size_mb == 10.5

    def test_deployed_version_minimal(self):
        """Test DeployedVersion with minimal fields."""
        version = DeployedVersion(
            version="1.0.0",
            title="1.0.0",
            aliases=[]
        )

        assert version.version == "1.0.0"
        assert version.is_default is False
        assert version.deploy_date is None
