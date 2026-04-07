"""Unit tests for MikeVersionManager."""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, Mock
import subprocess

from csa_docs_tools.mike_manager import MikeVersionManager, DeployedVersion


class TestMikeVersionManager:
    """Test cases for MikeVersionManager."""

    @pytest.mark.unit
    def test_init(self, tmp_path):
        """Test MikeVersionManager initialization."""
        manager = MikeVersionManager(tmp_path)
        assert manager.repo_path == tmp_path

    @pytest.mark.unit
    def test_is_available_true(self, tmp_path):
        """Test is_available when mike is installed."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            assert manager.is_available() is True

    @pytest.mark.unit
    def test_is_available_false(self, tmp_path):
        """Test is_available when mike is not installed."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike', side_effect=FileNotFoundError):
            assert manager.is_available() is False

    @pytest.mark.unit
    def test_is_available_error(self, tmp_path):
        """Test is_available on unexpected error."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike', side_effect=Exception("boom")):
            assert manager.is_available() is False

    @pytest.mark.unit
    def test_list_versions_success(self, tmp_path):
        """Test listing versions successfully."""
        manager = MikeVersionManager(tmp_path)

        mike_output = json.dumps([
            {"version": "1.0.0", "title": "v1.0.0", "aliases": ["latest"]},
            {"version": "0.9.0", "title": "v0.9.0", "aliases": []},
        ])

        with patch.object(manager, '_run_mike') as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout=mike_output)
            versions = manager.list_versions()

        assert len(versions) == 2
        assert versions[0].version == "1.0.0"
        assert versions[0].aliases == ["latest"]
        assert versions[1].version == "0.9.0"

    @pytest.mark.unit
    def test_list_versions_empty(self, tmp_path):
        """Test listing versions when none exist."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike') as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="")
            versions = manager.list_versions()

        assert versions == []

    @pytest.mark.unit
    def test_list_versions_error(self, tmp_path):
        """Test listing versions when mike fails."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike') as mock_run:
            mock_run.return_value = Mock(returncode=1, stdout="")
            versions = manager.list_versions()

        assert versions == []

    @pytest.mark.unit
    def test_list_versions_invalid_json(self, tmp_path):
        """Test listing versions with invalid JSON output."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike') as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="not json")
            versions = manager.list_versions()

        assert versions == []

    @pytest.mark.unit
    def test_list_versions_file_not_found(self, tmp_path):
        """Test listing versions when mike is not installed."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike', side_effect=FileNotFoundError):
            versions = manager.list_versions()

        assert versions == []

    @pytest.mark.unit
    def test_deploy_version_success(self, tmp_path):
        """Test successful version deployment."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike') as mock_run:
            mock_run.return_value = Mock(returncode=0, stderr="")
            result = manager.deploy_version("1.0.0", title="v1.0.0")

        assert result is True
        args = mock_run.call_args[0][0]
        assert "deploy" in args
        assert "1.0.0" in args
        assert "v1.0.0" in args

    @pytest.mark.unit
    def test_deploy_version_with_push(self, tmp_path):
        """Test deployment with push flag."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike') as mock_run:
            mock_run.return_value = Mock(returncode=0, stderr="")
            manager.deploy_version("1.0.0", push=True)

        args = mock_run.call_args[0][0]
        assert "--push" in args

    @pytest.mark.unit
    def test_deploy_version_with_aliases(self, tmp_path):
        """Test deployment with aliases."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike') as mock_run:
            mock_run.return_value = Mock(returncode=0, stderr="")
            manager.deploy_version("1.0.0", aliases=["latest", "stable"])

        args = mock_run.call_args[0][0]
        assert "latest" in args
        assert "stable" in args

    @pytest.mark.unit
    def test_deploy_version_failure(self, tmp_path):
        """Test failed version deployment."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike') as mock_run:
            mock_run.return_value = Mock(returncode=1, stderr="deploy error")
            result = manager.deploy_version("1.0.0")

        assert result is False

    @pytest.mark.unit
    def test_deploy_version_mike_not_found(self, tmp_path):
        """Test deployment when mike is not installed."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike', side_effect=FileNotFoundError):
            result = manager.deploy_version("1.0.0")

        assert result is False

    @pytest.mark.unit
    def test_set_default_success(self, tmp_path):
        """Test setting default version."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            result = manager.set_default("1.0.0")

        assert result is True
        args = mock_run.call_args[0][0]
        assert "set-default" in args
        assert "1.0.0" in args

    @pytest.mark.unit
    def test_set_default_failure(self, tmp_path):
        """Test setting default version failure."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike') as mock_run:
            mock_run.return_value = Mock(returncode=1)
            result = manager.set_default("1.0.0")

        assert result is False

    @pytest.mark.unit
    def test_delete_version_success(self, tmp_path):
        """Test deleting a version."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            result = manager.delete_version("0.9.0")

        assert result is True
        args = mock_run.call_args[0][0]
        assert "delete" in args
        assert "0.9.0" in args

    @pytest.mark.unit
    def test_delete_version_with_push(self, tmp_path):
        """Test deleting a version with push."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, '_run_mike') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            manager.delete_version("0.9.0", push=True)

        args = mock_run.call_args[0][0]
        assert "--push" in args

    @pytest.mark.unit
    def test_compare_versions(self, tmp_path):
        """Test version comparison delegation."""
        manager = MikeVersionManager(tmp_path)
        assert manager.compare_versions("1.0.0", "2.0.0") == -1
        assert manager.compare_versions("2.0.0", "1.0.0") == 1
        assert manager.compare_versions("1.0.0", "1.0.0") == 0

    @pytest.mark.unit
    def test_archive_old_versions_empty(self, tmp_path):
        """Test archiving when no versions exist."""
        manager = MikeVersionManager(tmp_path)

        with patch.object(manager, 'list_versions', return_value=[]):
            archived = manager.archive_old_versions()

        assert archived == []

    @pytest.mark.unit
    def test_archive_old_versions_keeps_recent(self, tmp_path):
        """Test that recent stable versions are kept."""
        manager = MikeVersionManager(tmp_path)

        versions = [
            DeployedVersion(version="3.0.0"),
            DeployedVersion(version="2.0.0"),
            DeployedVersion(version="1.0.0"),
        ]

        with patch.object(manager, 'list_versions', return_value=versions):
            with patch.object(manager, 'delete_version', return_value=True):
                archived = manager.archive_old_versions(keep_count=2)

        assert len(archived) == 1
        assert "1.0.0" in archived

    @pytest.mark.unit
    def test_archive_old_versions_archives_prereleases(self, tmp_path):
        """Test archiving prerelease versions."""
        manager = MikeVersionManager(tmp_path)

        versions = [
            DeployedVersion(version="2.0.0"),
            DeployedVersion(version="2.0.0-alpha"),
            DeployedVersion(version="1.0.0-beta"),
        ]

        with patch.object(manager, 'list_versions', return_value=versions):
            with patch.object(manager, 'delete_version', return_value=True):
                archived = manager.archive_old_versions(keep_count=5, archive_prereleases=True)

        assert "2.0.0-alpha" in archived
        assert "1.0.0-beta" in archived
        assert "2.0.0" not in archived

    @pytest.mark.unit
    def test_archive_old_versions_no_archive_prereleases(self, tmp_path):
        """Test not archiving prereleases when flag is False."""
        manager = MikeVersionManager(tmp_path)

        versions = [
            DeployedVersion(version="1.0.0"),
            DeployedVersion(version="1.0.0-alpha"),
        ]

        with patch.object(manager, 'list_versions', return_value=versions):
            with patch.object(manager, 'delete_version', return_value=True):
                archived = manager.archive_old_versions(keep_count=5, archive_prereleases=False)

        assert archived == []
