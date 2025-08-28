"""Tests for release management functionality."""

import pytest
import subprocess
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call

from src.csa_docs_tools.release_manager import (
    ReleaseManager,
    ReleaseConfig,
    ChangelogEntry,
    ReleaseType
)


class TestReleaseConfig:
    """Test cases for ReleaseConfig."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ReleaseConfig()
        
        assert config.main_branch == "master"
        assert config.release_branch_prefix == "release/"
        assert config.hotfix_branch_prefix == "hotfix/"
        assert config.changelog_path == "CHANGELOG.md"
        assert config.tag_prefix == "v"
        assert not config.auto_merge_releases
        assert config.require_pr_for_releases
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = ReleaseConfig(
            main_branch="main",
            release_branch_prefix="releases/",
            auto_merge_releases=True,
            tag_prefix="version-"
        )
        
        assert config.main_branch == "main"
        assert config.release_branch_prefix == "releases/"
        assert config.auto_merge_releases
        assert config.tag_prefix == "version-"


class TestReleaseManager:
    """Test cases for ReleaseManager."""
    
    @pytest.fixture
    def release_manager(self, tmp_path):
        """Create ReleaseManager instance for testing."""
        config = ReleaseConfig()
        return ReleaseManager(config, tmp_path)
    
    @pytest.fixture
    def mock_git_command(self):
        """Mock git command execution."""
        with patch.object(ReleaseManager, '_run_git_command') as mock:
            yield mock
    
    def test_create_release_branch_success(self, release_manager, mock_git_command):
        """Test successful release branch creation."""
        mock_git_command.side_effect = [
            "",  # branch --list (empty = branch doesn't exist)
            ""   # checkout -b
        ]
        
        branch_name = release_manager.create_release_branch("1.0.0")
        
        assert branch_name == "release/1.0.0"
        assert mock_git_command.call_count == 2
        mock_git_command.assert_any_call(['branch', '--list', 'release/1.0.0'])
        mock_git_command.assert_any_call(['checkout', '-b', 'release/1.0.0', 'master'])
    
    def test_create_release_branch_already_exists(self, release_manager, mock_git_command):
        """Test release branch creation when branch already exists."""
        mock_git_command.return_value = "release/1.0.0"  # Branch exists
        
        with pytest.raises(ValueError, match="Release branch release/1.0.0 already exists"):
            release_manager.create_release_branch("1.0.0")
    
    def test_create_hotfix_branch_success(self, release_manager, mock_git_command):
        """Test successful hotfix branch creation."""
        mock_git_command.side_effect = [
            "",  # branch --list (empty = branch doesn't exist)
            ""   # checkout -b
        ]
        
        branch_name = release_manager.create_hotfix_branch("1.0.1", "v1.0.0")
        
        assert branch_name == "hotfix/1.0.1"
        mock_git_command.assert_any_call(['checkout', '-b', 'hotfix/1.0.1', 'v1.0.0'])
    
    def test_generate_changelog_with_version_range(self, release_manager, mock_git_command):
        """Test changelog generation with specific version range."""
        # Mock git log output
        mock_commits = [
            "abc123|John Doe|john@example.com|2023-01-01 10:00:00|feat: add new feature",
            "def456|Jane Smith|jane@example.com|2023-01-02 11:00:00|fix: resolve issue",
            "ghi789|Bob Johnson|bob@example.com|2023-01-03 12:00:00|docs: update documentation"
        ]
        
        mock_git_command.return_value = "\n".join(mock_commits)
        
        changelog = release_manager.generate_changelog("v1.0.0", "v1.1.0")
        
        assert "## [v1.1.0]" in changelog
        assert "### 🚀 Features" in changelog
        assert "add new feature" in changelog
        assert "### 🐛 Bug Fixes" in changelog
        assert "resolve issue" in changelog
        assert "### 📚 Documentation" in changelog
        assert "update documentation" in changelog
    
    def test_generate_changelog_no_commits(self, release_manager, mock_git_command):
        """Test changelog generation with no commits."""
        mock_git_command.return_value = ""
        
        changelog = release_manager.generate_changelog("v1.0.0", "v1.1.0")
        
        assert "## [v1.1.0]" in changelog
        assert "No changes." in changelog
    
    def test_validate_release_readiness_success(self, release_manager, mock_git_command):
        """Test successful release readiness validation."""
        mock_git_command.side_effect = [
            "",  # git status --porcelain (no uncommitted changes)
            ""   # git tag --list (tag doesn't exist)
        ]
        
        # Mock changelog file existence
        changelog_path = release_manager.repo_path / release_manager.config.changelog_path
        with patch.object(changelog_path, 'exists', return_value=True):
            is_ready, issues = release_manager.validate_release_readiness("1.0.0")
        
        assert is_ready
        assert len(issues) == 0
    
    def test_validate_release_readiness_uncommitted_changes(self, release_manager, mock_git_command):
        """Test release readiness validation with uncommitted changes."""
        mock_git_command.side_effect = [
            "M modified_file.py",  # git status --porcelain (uncommitted changes)
            ""   # git tag --list
        ]
        
        changelog_path = release_manager.repo_path / release_manager.config.changelog_path
        with patch.object(changelog_path, 'exists', return_value=True):
            is_ready, issues = release_manager.validate_release_readiness("1.0.0")
        
        assert not is_ready
        assert "uncommitted changes" in issues[0]
    
    def test_validate_release_readiness_tag_exists(self, release_manager, mock_git_command):
        """Test release readiness validation when tag already exists."""
        mock_git_command.side_effect = [
            "",  # git status --porcelain
            "v1.0.0"   # git tag --list (tag exists)
        ]
        
        changelog_path = release_manager.repo_path / release_manager.config.changelog_path
        with patch.object(changelog_path, 'exists', return_value=True):
            is_ready, issues = release_manager.validate_release_readiness("1.0.0")
        
        assert not is_ready
        assert "already exists as a tag" in issues[0]
    
    def test_validate_release_readiness_missing_changelog(self, release_manager, mock_git_command):
        """Test release readiness validation with missing changelog."""
        mock_git_command.side_effect = [
            "",  # git status --porcelain
            ""   # git tag --list
        ]
        
        changelog_path = release_manager.repo_path / release_manager.config.changelog_path
        with patch.object(changelog_path, 'exists', return_value=False):
            is_ready, issues = release_manager.validate_release_readiness("1.0.0")
        
        assert not is_ready
        assert "does not exist" in issues[0]
    
    def test_finalize_release_success(self, release_manager, mock_git_command):
        """Test successful release finalization."""
        # Mock git commands
        mock_git_command.side_effect = [
            "release/1.0.0",  # branch --list (branch exists)
            "",               # checkout release/1.0.0
            "",               # add .
            "",               # commit
            "",               # tag -a
            "abc123"          # rev-parse HEAD (current commit hash)
        ]
        
        # Mock file operations
        with patch.object(release_manager, '_update_version_files'), \
             patch.object(release_manager, '_update_changelog_file'), \
             patch.object(release_manager, 'generate_changelog', return_value="## [1.0.0] - 2023-01-01\n\nTest changelog"):
            
            result = release_manager.finalize_release("1.0.0")
        
        assert result['version'] == "1.0.0"
        assert result['tag'] == "v1.0.0"
        assert result['branch'] == "release/1.0.0"
        assert result['commit'] == "abc123"
        assert "Test changelog" in result['changelog']
    
    def test_finalize_release_branch_not_exists(self, release_manager, mock_git_command):
        """Test release finalization when release branch doesn't exist."""
        mock_git_command.return_value = ""  # branch --list (branch doesn't exist)
        
        with pytest.raises(ValueError, match="Release branch release/1.0.0 does not exist"):
            release_manager.finalize_release("1.0.0")
    
    def test_get_latest_tag(self, release_manager, mock_git_command):
        """Test getting latest git tag."""
        mock_git_command.return_value = "v1.2.3"
        
        tag = release_manager._get_latest_tag()
        
        assert tag == "v1.2.3"
        mock_git_command.assert_called_with(['describe', '--tags', '--abbrev=0'])
    
    def test_get_commits_between(self, release_manager, mock_git_command):
        """Test getting commits between two references."""
        mock_commits = [
            "abc123|John Doe|john@example.com|2023-01-01 10:00:00|feat: add feature",
            "def456|Jane Smith|jane@example.com|2023-01-02 11:00:00|fix: bug fix"
        ]
        
        mock_git_command.return_value = "\n".join(mock_commits)
        
        commits = release_manager._get_commits_between("v1.0.0", "v1.1.0")
        
        assert len(commits) == 2
        assert commits[0]['hash'] == "abc123"
        assert commits[0]['author'] == "John Doe"
        assert commits[0]['message'] == "feat: add feature"
        assert commits[1]['hash'] == "def456"
        assert commits[1]['author'] == "Jane Smith"
    
    def test_parse_commits_conventional(self, release_manager):
        """Test parsing conventional commits."""
        commits = [
            {
                'hash': 'abc123',
                'author': 'John Doe',
                'email': 'john@example.com',
                'date': '2023-01-01 10:00:00',
                'message': 'feat(ui): add new button component'
            },
            {
                'hash': 'def456',
                'author': 'Jane Smith',
                'email': 'jane@example.com',
                'date': '2023-01-02 11:00:00',
                'message': 'fix!: resolve critical security issue'
            }
        ]
        
        entries = release_manager._parse_commits(commits)
        
        assert len(entries) == 2
        
        # Test feature commit
        feat_entry = entries[0]
        assert feat_entry.type == 'feat'
        assert feat_entry.scope == 'ui'
        assert feat_entry.description == 'add new button component'
        assert not feat_entry.breaking_change
        
        # Test breaking change commit
        fix_entry = entries[1]
        assert fix_entry.type == 'fix'
        assert fix_entry.description == 'resolve critical security issue'
        assert fix_entry.breaking_change
    
    def test_parse_commits_non_conventional(self, release_manager):
        """Test parsing non-conventional commits."""
        commits = [
            {
                'hash': 'abc123',
                'author': 'John Doe',
                'email': 'john@example.com',
                'date': '2023-01-01 10:00:00',
                'message': 'Update README with installation instructions'
            }
        ]
        
        entries = release_manager._parse_commits(commits)
        
        assert len(entries) == 1
        entry = entries[0]
        assert entry.type == 'other'
        assert entry.scope is None
        assert entry.description == 'Update README with installation instructions'
        assert not entry.breaking_change
    
    def test_format_changelog(self, release_manager):
        """Test changelog formatting."""
        entries = [
            ChangelogEntry(
                type='feat',
                scope='api',
                description='add new endpoint',
                commit_hash='abc123',
                author='John Doe',
                date=datetime(2023, 1, 1, 10, 0, 0),
                breaking_change=False
            ),
            ChangelogEntry(
                type='fix',
                scope=None,
                description='resolve memory leak',
                commit_hash='def456',
                author='Jane Smith',
                date=datetime(2023, 1, 2, 11, 0, 0),
                breaking_change=True
            )
        ]
        
        changelog = release_manager._format_changelog(entries, "1.1.0")
        
        assert "## [1.1.0]" in changelog
        assert "### ⚠️ BREAKING CHANGES" in changelog
        assert "resolve memory leak" in changelog
        assert "### 🚀 Features" in changelog
        assert "**api**: add new endpoint (abc123)" in changelog
        assert "### 🐛 Bug Fixes" in changelog
    
    def test_run_git_command_success(self, release_manager):
        """Test successful git command execution."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                stdout="command output",
                stderr="",
                returncode=0
            )
            
            result = release_manager._run_git_command(['status'])
            
            assert result == "command output"
            mock_run.assert_called_once_with(
                ['git', 'status'],
                cwd=release_manager.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
    
    def test_run_git_command_failure(self, release_manager):
        """Test git command execution failure."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, ['git', 'status'], 'command failed', 'error message'
            )
            
            with pytest.raises(subprocess.CalledProcessError):
                release_manager._run_git_command(['status'])
    
    def test_update_version_files_pyproject(self, release_manager, tmp_path):
        """Test updating version in pyproject.toml."""
        pyproject_content = '''[project]
name = "test-project"
version = "1.0.0"
description = "Test project"
'''
        
        pyproject_path = tmp_path / "pyproject.toml"
        pyproject_path.write_text(pyproject_content)
        
        release_manager._update_version_files("1.1.0")
        
        updated_content = pyproject_path.read_text()
        assert 'version = "1.1.0"' in updated_content
        assert 'version = "1.0.0"' not in updated_content
    
    def test_update_version_files_package_json(self, release_manager, tmp_path):
        """Test updating version in package.json."""
        package_content = {
            "name": "test-project",
            "version": "1.0.0",
            "description": "Test project"
        }
        
        package_path = tmp_path / "package.json"
        with open(package_path, 'w') as f:
            import json
            json.dump(package_content, f)
        
        release_manager._update_version_files("1.1.0")
        
        with open(package_path, 'r') as f:
            import json
            updated_content = json.load(f)
        
        assert updated_content["version"] == "1.1.0"
    
    def test_update_changelog_file_new_file(self, release_manager, tmp_path):
        """Test updating changelog file when it doesn't exist."""
        changelog_content = "## [1.1.0] - 2023-01-01\n\nNew features and fixes"
        
        release_manager._update_changelog_file(changelog_content, "1.1.0")
        
        changelog_path = tmp_path / "CHANGELOG.md"
        assert changelog_path.exists()
        
        content = changelog_path.read_text()
        assert "# Changelog" in content
        assert "## [1.1.0] - 2023-01-01" in content
        assert "New features and fixes" in content
    
    def test_update_changelog_file_existing_file(self, release_manager, tmp_path):
        """Test updating existing changelog file."""
        existing_content = """# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2023-01-01

Initial release"""
        
        changelog_path = tmp_path / "CHANGELOG.md"
        changelog_path.write_text(existing_content)
        
        new_changelog = "## [1.1.0] - 2023-02-01\n\nNew features and fixes"
        release_manager._update_changelog_file(new_changelog, "1.1.0")
        
        updated_content = changelog_path.read_text()
        lines = updated_content.split('\n')
        
        # Check that new content is inserted before old content
        assert "## [1.1.0] - 2023-02-01" in updated_content
        assert "## [1.0.0] - 2023-01-01" in updated_content
        
        # Find positions to ensure correct order
        v11_index = next(i for i, line in enumerate(lines) if "[1.1.0]" in line)
        v10_index = next(i for i, line in enumerate(lines) if "[1.0.0]" in line)
        assert v11_index < v10_index


class TestChangelogEntry:
    """Test cases for ChangelogEntry dataclass."""
    
    def test_changelog_entry_creation(self):
        """Test creating a changelog entry."""
        entry = ChangelogEntry(
            type='feat',
            scope='api',
            description='add new endpoint',
            commit_hash='abc123',
            author='John Doe',
            date=datetime(2023, 1, 1, 10, 0, 0)
        )
        
        assert entry.type == 'feat'
        assert entry.scope == 'api'
        assert entry.description == 'add new endpoint'
        assert entry.commit_hash == 'abc123'
        assert entry.author == 'John Doe'
        assert not entry.breaking_change
    
    def test_changelog_entry_breaking_change(self):
        """Test creating a breaking change entry."""
        entry = ChangelogEntry(
            type='feat',
            scope=None,
            description='redesign API',
            commit_hash='def456',
            author='Jane Smith',
            date=datetime(2023, 1, 2, 11, 0, 0),
            breaking_change=True
        )
        
        assert entry.breaking_change
        assert entry.scope is None


@pytest.fixture
def mock_git_repo(tmp_path):
    """Create a mock git repository for testing."""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    
    # Create basic files
    (repo_path / "README.md").write_text("# Test Repository")
    (repo_path / "CHANGELOG.md").write_text("# Changelog\n")
    
    return repo_path


class TestReleaseManagerIntegration:
    """Integration tests for ReleaseManager."""
    
    def test_complete_release_workflow(self, mock_git_repo):
        """Test complete release workflow."""
        config = ReleaseConfig(auto_merge_releases=False)
        manager = ReleaseManager(config, mock_git_repo)
        
        with patch.object(manager, '_run_git_command') as mock_git:
            # Mock git commands for the workflow
            mock_git.side_effect = [
                "",              # branch --list (release branch doesn't exist)
                "",              # checkout -b (create release branch)
                "",              # status --porcelain (no uncommitted changes)
                "",              # tag --list (tag doesn't exist)
                "release/1.0.0", # branch --list (release branch exists)
                "",              # checkout release/1.0.0
                "",              # add .
                "",              # commit
                "",              # tag -a
                "abc123456789"   # rev-parse HEAD
            ]
            
            # Mock changelog generation
            with patch.object(manager, 'generate_changelog', return_value="## [1.0.0] - 2023-01-01\n\nTest release"):
                # Create release branch
                branch = manager.create_release_branch("1.0.0")
                assert branch == "release/1.0.0"
                
                # Validate release readiness
                is_ready, issues = manager.validate_release_readiness("1.0.0")
                assert is_ready
                assert len(issues) == 0
                
                # Finalize release
                result = manager.finalize_release("1.0.0")
                assert result['version'] == "1.0.0"
                assert result['tag'] == "v1.0.0"
                assert result['branch'] == "release/1.0.0"
                assert result['commit'] == "abc123456789"
    
    def test_hotfix_workflow(self, mock_git_repo):
        """Test hotfix release workflow."""
        config = ReleaseConfig()
        manager = ReleaseManager(config, mock_git_repo)
        
        with patch.object(manager, '_run_git_command') as mock_git:
            mock_git.side_effect = [
                "",              # branch --list (hotfix branch doesn't exist)
                ""               # checkout -b (create hotfix branch)
            ]
            
            branch = manager.create_hotfix_branch("1.0.1", "v1.0.0")
            
            assert branch == "hotfix/1.0.1"
            mock_git.assert_any_call(['checkout', '-b', 'hotfix/1.0.1', 'v1.0.0'])
