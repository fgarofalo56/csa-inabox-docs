"""Release management for documentation versions."""

import logging
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class ReleaseCheck:
    """Result of a single release-readiness check."""
    name: str
    passed: bool
    message: str


class ReleaseManager:
    """Manage documentation release lifecycle."""

    def __init__(self, repo_path: Path):
        """Initialize release manager.

        Args:
            repo_path: Path to the repository root.
        """
        self.repo_path = Path(repo_path)
        self.mkdocs_config = self.repo_path / "mkdocs.yml"
        self.docs_dir = self.repo_path / "docs"

    # ------------------------------------------------------------------
    # Release readiness
    # ------------------------------------------------------------------

    def validate_release_readiness(
        self, version: str
    ) -> Tuple[bool, List[str]]:
        """Check whether the repository is ready for a release.

        Args:
            version: Version string being released (without 'v' prefix).

        Returns:
            Tuple of (is_ready, list_of_issue_messages).
        """
        issues: List[str] = []

        checks = [
            self._check_mkdocs_config(),
            self._check_docs_directory(),
            self._check_uncommitted_changes(),
            self._check_version_format(version),
        ]

        for check in checks:
            if not check.passed:
                issues.append(f"{check.name}: {check.message}")

        return len(issues) == 0, issues

    def _check_mkdocs_config(self) -> ReleaseCheck:
        """Verify mkdocs.yml exists and is parsable."""
        if not self.mkdocs_config.exists():
            return ReleaseCheck("mkdocs.yml", False, "mkdocs.yml not found")
        try:
            import yaml
            with open(self.mkdocs_config, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            if not config or 'site_name' not in config:
                return ReleaseCheck("mkdocs.yml", False, "Missing site_name in mkdocs.yml")
        except Exception as e:
            return ReleaseCheck("mkdocs.yml", False, f"Invalid mkdocs.yml: {e}")
        return ReleaseCheck("mkdocs.yml", True, "Valid configuration")

    def _check_docs_directory(self) -> ReleaseCheck:
        """Verify docs directory exists and contains markdown."""
        if not self.docs_dir.exists():
            return ReleaseCheck("docs_dir", False, "docs/ directory not found")
        md_files = list(self.docs_dir.rglob("*.md"))
        if not md_files:
            return ReleaseCheck("docs_dir", False, "No markdown files in docs/")
        return ReleaseCheck("docs_dir", True, f"Found {len(md_files)} markdown files")

    def _check_uncommitted_changes(self) -> ReleaseCheck:
        """Check for uncommitted changes in the working tree."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
                timeout=30,
            )
            if result.stdout.strip():
                return ReleaseCheck(
                    "git_clean", False,
                    "Uncommitted changes detected"
                )
        except Exception as e:
            return ReleaseCheck("git_clean", False, f"Could not check git status: {e}")
        return ReleaseCheck("git_clean", True, "Working tree is clean")

    def _check_version_format(self, version: str) -> ReleaseCheck:
        """Validate version string format."""
        from .version_manager import SemanticVersionManager
        manager = SemanticVersionManager()
        try:
            manager.parse_version(version)
        except ValueError as e:
            return ReleaseCheck("version_format", False, str(e))
        return ReleaseCheck("version_format", True, f"Valid version: {version}")

    # ------------------------------------------------------------------
    # Changelog generation
    # ------------------------------------------------------------------

    def generate_changelog(
        self,
        from_version: str,
        to_version: str,
    ) -> str:
        """Generate a changelog between two versions using git log.

        Args:
            from_version: Starting version tag (exclusive).
            to_version: Ending version tag (inclusive / HEAD).

        Returns:
            Markdown-formatted changelog string.
        """
        sections: Dict[str, List[str]] = {
            'Features': [],
            'Bug Fixes': [],
            'Documentation': [],
            'Other': [],
        }

        commit_range = f"{from_version}..HEAD"
        try:
            result = subprocess.run(
                ["git", "log", "--pretty=format:%s", commit_range],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
                timeout=30,
            )
            lines = result.stdout.strip().splitlines() if result.stdout else []
        except Exception as e:
            logger.warning(f"Could not read git log: {e}")
            lines = []

        for line in lines:
            lower = line.lower()
            if lower.startswith("feat"):
                sections['Features'].append(f"- {line}")
            elif lower.startswith("fix"):
                sections['Bug Fixes'].append(f"- {line}")
            elif lower.startswith("docs"):
                sections['Documentation'].append(f"- {line}")
            else:
                sections['Other'].append(f"- {line}")

        parts = [f"# Changelog: {from_version} -> {to_version}\n"]
        parts.append(f"Generated on {datetime.now().strftime('%Y-%m-%d')}\n")

        for heading, items in sections.items():
            if items:
                parts.append(f"\n## {heading}\n")
                parts.extend(items)

        if not any(sections.values()):
            parts.append("\nNo notable changes.\n")

        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Release metadata
    # ------------------------------------------------------------------

    def get_release_metadata(self, version: str) -> Dict[str, object]:
        """Build release metadata dictionary.

        Args:
            version: Version being released.

        Returns:
            Dictionary suitable for JSON serialisation.
        """
        return {
            'version': version,
            'release_date': datetime.now().isoformat(),
            'repo_path': str(self.repo_path),
            'docs_exist': self.docs_dir.exists(),
            'config_exists': self.mkdocs_config.exists(),
        }
