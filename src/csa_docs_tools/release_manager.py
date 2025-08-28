"""Release management for CSA documentation.

This module handles:
- Release branch creation and management
- Automated changelog generation
- Release notes creation
- Version tagging
- Release validation
"""

import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

from .version_manager import ReleaseType, SemanticVersionManager, VersionInfo, VersionType


@dataclass
class ReleaseConfig:
    """Configuration for release management."""
    
    main_branch: str = "master"
    release_branch_prefix: str = "release/"
    hotfix_branch_prefix: str = "hotfix/"
    changelog_path: str = "CHANGELOG.md"
    release_notes_template: str = "RELEASE_NOTES_TEMPLATE.md"
    auto_merge_releases: bool = False
    require_pr_for_releases: bool = True
    tag_prefix: str = "v"
    

@dataclass
class ChangelogEntry:
    """Entry in the changelog."""
    
    type: str  # feat, fix, docs, etc.
    scope: Optional[str]
    description: str
    commit_hash: str
    author: str
    date: datetime
    breaking_change: bool = False
    

class ReleaseManager:
    """Manages documentation releases and branching strategy."""
    
    COMMIT_TYPES = {
        'feat': '🚀 Features',
        'fix': '🐛 Bug Fixes', 
        'docs': '📚 Documentation',
        'style': '💄 Styling',
        'refactor': '♻️ Refactoring',
        'perf': '⚡ Performance',
        'test': '🧪 Testing',
        'build': '📦 Build System',
        'ci': '👷 Continuous Integration',
        'chore': '🔧 Maintenance',
        'revert': '⏪ Reverts'
    }
    
    def __init__(self, config: Optional[ReleaseConfig] = None, repo_path: Optional[Path] = None):
        """Initialize release manager.
        
        Args:
            config: Release configuration
            repo_path: Path to repository root
        """
        self.config = config or ReleaseConfig()
        self.repo_path = repo_path or Path.cwd()
        self.version_manager = SemanticVersionManager()
        
    def create_release_branch(self, version: str, base_branch: Optional[str] = None) -> str:
        """Create a new release branch.
        
        Args:
            version: Target version for the release
            base_branch: Base branch to create from (defaults to main branch)
            
        Returns:
            Name of the created release branch
        """
        base = base_branch or self.config.main_branch
        branch_name = f"{self.config.release_branch_prefix}{version}"
        
        # Check if branch already exists
        result = self._run_git_command(['branch', '--list', branch_name])
        if result.strip():
            raise ValueError(f"Release branch {branch_name} already exists")
        
        # Create and checkout new branch
        self._run_git_command(['checkout', '-b', branch_name, base])
        
        return branch_name
    
    def create_hotfix_branch(self, version: str, base_tag: str) -> str:
        """Create a new hotfix branch.
        
        Args:
            version: Target version for the hotfix
            base_tag: Base tag to create from
            
        Returns:
            Name of the created hotfix branch
        """
        branch_name = f"{self.config.hotfix_branch_prefix}{version}"
        
        # Check if branch already exists
        result = self._run_git_command(['branch', '--list', branch_name])
        if result.strip():
            raise ValueError(f"Hotfix branch {branch_name} already exists")
        
        # Create and checkout new branch from tag
        self._run_git_command(['checkout', '-b', branch_name, base_tag])
        
        return branch_name
    
    def generate_changelog(self, from_version: Optional[str] = None, 
                          to_version: Optional[str] = None) -> str:
        """Generate changelog for a version range.
        
        Args:
            from_version: Starting version (defaults to last tag)
            to_version: Ending version (defaults to HEAD)
            
        Returns:
            Generated changelog content
        """
        # Determine version range
        if not from_version:
            try:
                from_version = self._get_latest_tag()
            except subprocess.CalledProcessError:
                from_version = None
        
        to_ref = to_version if to_version else "HEAD"
        from_ref = from_version if from_version else "--all"
        
        # Get commit history
        if from_version:
            commits = self._get_commits_between(from_version, to_ref)
        else:
            commits = self._get_all_commits(to_ref)
        
        # Parse commits and generate changelog
        changelog_entries = self._parse_commits(commits)
        return self._format_changelog(changelog_entries, to_version or "Unreleased")
    
    def create_release_notes(self, version: str, template_path: Optional[Path] = None) -> str:
        """Create release notes for a version.
        
        Args:
            version: Version to create release notes for
            template_path: Path to release notes template
            
        Returns:
            Generated release notes content
        """
        template_file = template_path or (self.repo_path / self.config.release_notes_template)
        
        # Generate changelog content
        changelog_content = self.generate_changelog(to_version=version)
        
        # Load template if exists
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                template = f.read()
        else:
            template = self._get_default_release_notes_template()
        
        # Replace template variables
        release_notes = template.format(
            version=version,
            date=datetime.now().strftime('%Y-%m-%d'),
            changelog=changelog_content,
            contributors=self._get_contributors_since_last_release()
        )
        
        return release_notes
    
    def finalize_release(self, version: str, release_branch: Optional[str] = None) -> Dict[str, str]:
        """Finalize a release by creating tags and merging branches.
        
        Args:
            version: Version being released
            release_branch: Release branch name
            
        Returns:
            Dictionary with release information
        """
        branch_name = release_branch or f"{self.config.release_branch_prefix}{version}"
        tag_name = f"{self.config.tag_prefix}{version}"
        
        # Validate release branch exists
        result = self._run_git_command(['branch', '--list', branch_name])
        if not result.strip():
            raise ValueError(f"Release branch {branch_name} does not exist")
        
        # Checkout release branch
        self._run_git_command(['checkout', branch_name])
        
        # Update version in project files
        self._update_version_files(version)
        
        # Generate and update changelog
        changelog_content = self.generate_changelog(to_version=version)
        self._update_changelog_file(changelog_content, version)
        
        # Commit version updates
        commit_message = f"chore: prepare release {version}"
        self._run_git_command(['add', '.'])
        self._run_git_command(['commit', '-m', commit_message])
        
        # Create annotated tag
        tag_message = f"Release {version}"
        self._run_git_command(['tag', '-a', tag_name, '-m', tag_message])
        
        # Merge to main branch if configured
        if self.config.auto_merge_releases:
            self._run_git_command(['checkout', self.config.main_branch])
            self._run_git_command(['merge', '--no-ff', branch_name, '-m', f"Merge release {version}"])
        
        return {
            'version': version,
            'tag': tag_name,
            'branch': branch_name,
            'commit': self._get_current_commit_hash(),
            'changelog': changelog_content
        }
    
    def validate_release_readiness(self, version: str) -> Tuple[bool, List[str]]:
        """Validate that a release is ready.
        
        Args:
            version: Version to validate
            
        Returns:
            Tuple of (is_ready, list_of_issues)
        """
        issues = []
        
        # Check version format
        try:
            self.version_manager.parse_version(version)
        except ValueError as e:
            issues.append(f"Invalid version format: {e}")
        
        # Check for uncommitted changes
        status = self._run_git_command(['status', '--porcelain'])
        if status.strip():
            issues.append("Repository has uncommitted changes")
        
        # Check if version already exists
        try:
            existing_tags = self._run_git_command(['tag', '--list', f"{self.config.tag_prefix}{version}"])
            if existing_tags.strip():
                issues.append(f"Version {version} already exists as a tag")
        except subprocess.CalledProcessError:
            pass
        
        # Validate changelog exists and is properly formatted
        changelog_path = self.repo_path / self.config.changelog_path
        if not changelog_path.exists():
            issues.append(f"Changelog file {self.config.changelog_path} does not exist")
        
        return len(issues) == 0, issues
    
    def _run_git_command(self, args: List[str]) -> str:
        """Run a git command and return output.
        
        Args:
            args: Git command arguments
            
        Returns:
            Command output
            
        Raises:
            subprocess.CalledProcessError: If command fails
        """
        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise subprocess.CalledProcessError(
                e.returncode, e.cmd, e.stdout, f"Git command failed: {e.stderr}"
            ) from e
    
    def _get_latest_tag(self) -> str:
        """Get the latest git tag."""
        return self._run_git_command(['describe', '--tags', '--abbrev=0']).strip()
    
    def _get_current_commit_hash(self) -> str:
        """Get current commit hash."""
        return self._run_git_command(['rev-parse', 'HEAD']).strip()
    
    def _get_commits_between(self, from_ref: str, to_ref: str) -> List[Dict[str, str]]:
        """Get commits between two references."""
        output = self._run_git_command([
            'log', f"{from_ref}..{to_ref}", 
            '--pretty=format:%H|%an|%ae|%ad|%s', 
            '--date=iso'
        ])
        
        commits = []
        for line in output.strip().split('\n'):
            if line:
                parts = line.split('|', 4)
                if len(parts) == 5:
                    commits.append({
                        'hash': parts[0],
                        'author': parts[1],
                        'email': parts[2],
                        'date': parts[3],
                        'message': parts[4]
                    })
        
        return commits
    
    def _get_all_commits(self, to_ref: str) -> List[Dict[str, str]]:
        """Get all commits up to a reference."""
        output = self._run_git_command([
            'log', to_ref,
            '--pretty=format:%H|%an|%ae|%ad|%s',
            '--date=iso'
        ])
        
        commits = []
        for line in output.strip().split('\n'):
            if line:
                parts = line.split('|', 4)
                if len(parts) == 5:
                    commits.append({
                        'hash': parts[0],
                        'author': parts[1],
                        'email': parts[2],
                        'date': parts[3],
                        'message': parts[4]
                    })
        
        return commits
    
    def _parse_commits(self, commits: List[Dict[str, str]]) -> List[ChangelogEntry]:
        """Parse commits into changelog entries."""
        entries = []
        
        # Regex for conventional commits
        pattern = re.compile(
            r'^(?P<type>\w+)'  # type
            r'(?:\((?P<scope>[^)]+)\))?'  # scope (optional)
            r'(?P<breaking>!)?'  # breaking change indicator
            r': (?P<description>.+)'  # description
        )
        
        for commit in commits:
            match = pattern.match(commit['message'])
            if match:
                entry = ChangelogEntry(
                    type=match.group('type'),
                    scope=match.group('scope'),
                    description=match.group('description'),
                    commit_hash=commit['hash'][:8],
                    author=commit['author'],
                    date=datetime.fromisoformat(commit['date'].replace(' ', 'T')),
                    breaking_change=bool(match.group('breaking'))
                )
                entries.append(entry)
            else:
                # Handle non-conventional commits
                entry = ChangelogEntry(
                    type='other',
                    scope=None,
                    description=commit['message'],
                    commit_hash=commit['hash'][:8],
                    author=commit['author'],
                    date=datetime.fromisoformat(commit['date'].replace(' ', 'T')),
                    breaking_change=False
                )
                entries.append(entry)
        
        return entries
    
    def _format_changelog(self, entries: List[ChangelogEntry], version: str) -> str:
        """Format changelog entries into markdown."""
        if not entries:
            return f"## [{version}] - {datetime.now().strftime('%Y-%m-%d')}\n\nNo changes."
        
        changelog = [f"## [{version}] - {datetime.now().strftime('%Y-%m-%d')}"]
        
        # Group entries by type
        grouped = {}
        for entry in entries:
            entry_type = entry.type if entry.type in self.COMMIT_TYPES else 'other'
            if entry_type not in grouped:
                grouped[entry_type] = []
            grouped[entry_type].append(entry)
        
        # Add breaking changes section first
        breaking_changes = [e for e in entries if e.breaking_change]
        if breaking_changes:
            changelog.append("\n### ⚠️ BREAKING CHANGES")
            for entry in breaking_changes:
                scope_text = f"**{entry.scope}**: " if entry.scope else ""
                changelog.append(f"- {scope_text}{entry.description} ({entry.commit_hash})")
        
        # Add sections for each type
        for commit_type in ['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'build', 'ci', 'chore']:
            if commit_type in grouped:
                changelog.append(f"\n### {self.COMMIT_TYPES[commit_type]}")
                for entry in grouped[commit_type]:
                    if not entry.breaking_change:  # Breaking changes already shown
                        scope_text = f"**{entry.scope}**: " if entry.scope else ""
                        changelog.append(f"- {scope_text}{entry.description} ({entry.commit_hash})")
        
        # Add other changes
        if 'other' in grouped:
            changelog.append("\n### 🔄 Other Changes")
            for entry in grouped['other']:
                changelog.append(f"- {entry.description} ({entry.commit_hash})")
        
        return "\n".join(changelog)
    
    def _update_version_files(self, version: str) -> None:
        """Update version in project files."""
        # Update pyproject.toml
        pyproject_path = self.repo_path / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace version in pyproject.toml
            content = re.sub(
                r'version = "[^"]+"',
                f'version = "{version}"',
                content
            )
            
            with open(pyproject_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Update package.json if it exists
        package_json_path = self.repo_path / "package.json"
        if package_json_path.exists():
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            package_data['version'] = version
            
            with open(package_json_path, 'w', encoding='utf-8') as f:
                json.dump(package_data, f, indent=2)
    
    def _update_changelog_file(self, changelog_content: str, version: str) -> None:
        """Update the changelog file with new content."""
        changelog_path = self.repo_path / self.config.changelog_path
        
        if changelog_path.exists():
            with open(changelog_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        else:
            existing_content = "# Changelog\n\nAll notable changes to this project will be documented in this file."
        
        # Insert new changelog at the top
        lines = existing_content.split('\n')
        header_end = 0
        for i, line in enumerate(lines):
            if line.startswith('## [') or line.startswith('## Unreleased'):
                header_end = i
                break
        
        new_lines = lines[:header_end] + ['', changelog_content] + lines[header_end:]
        
        with open(changelog_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
    
    def _get_contributors_since_last_release(self) -> str:
        """Get list of contributors since last release."""
        try:
            last_tag = self._get_latest_tag()
            authors = self._run_git_command([
                'log', f"{last_tag}..HEAD",
                '--format=%an', '--no-merges'
            ])
            
            unique_authors = sorted(set(authors.strip().split('\n')))
            return '\n'.join(f"- @{author}" for author in unique_authors if author)
        except subprocess.CalledProcessError:
            return "- No contributors found"
    
    def _get_default_release_notes_template(self) -> str:
        """Get default release notes template."""
        return """# Release {version}

**Release Date**: {date}

## What's Changed

{changelog}

## Contributors

{contributors}

**Full Changelog**: https://github.com/your-org/csa-inabox-docs/compare/v{previous_version}...v{version}
"""
