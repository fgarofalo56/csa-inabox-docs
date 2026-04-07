"""Mike version management wrapper for MkDocs documentation."""

import json
import logging
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class DeployedVersion:
    """Represents a version deployed via Mike."""
    version: str
    title: str = ""
    aliases: List[str] = field(default_factory=list)


class MikeVersionManager:
    """Manage MkDocs documentation versions using Mike."""

    def __init__(self, repo_path: Path):
        """Initialize Mike version manager.

        Args:
            repo_path: Path to the repository root.
        """
        self.repo_path = Path(repo_path)

    # ------------------------------------------------------------------
    # Mike CLI helpers
    # ------------------------------------------------------------------

    def _run_mike(self, args: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run a mike CLI command.

        Args:
            args: Arguments to pass to mike.
            check: Whether to raise on non-zero exit.

        Returns:
            CompletedProcess instance.
        """
        cmd = ["mike"] + args
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=self.repo_path,
            timeout=120,
            check=check,
        )

    def is_available(self) -> bool:
        """Check if mike CLI is installed and available."""
        try:
            result = self._run_mike(["--version"], check=False)
            return result.returncode == 0
        except FileNotFoundError:
            return False
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Version operations
    # ------------------------------------------------------------------

    def list_versions(self) -> List[DeployedVersion]:
        """List all versions currently deployed via Mike.

        Returns:
            List of DeployedVersion objects.
        """
        try:
            result = self._run_mike(["list", "--json"], check=False)
            if result.returncode != 0 or not result.stdout.strip():
                return []
            entries = json.loads(result.stdout)
            versions = []
            for entry in entries:
                versions.append(DeployedVersion(
                    version=entry.get('version', ''),
                    title=entry.get('title', ''),
                    aliases=entry.get('aliases', []),
                ))
            return versions
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.warning(f"Could not list mike versions: {e}")
            return []
        except Exception as e:
            logger.error(f"Error listing mike versions: {e}")
            return []

    def deploy_version(
        self,
        version: str,
        title: Optional[str] = None,
        aliases: Optional[List[str]] = None,
        push: bool = False,
        update_aliases: bool = True,
    ) -> bool:
        """Deploy a documentation version with Mike.

        Args:
            version: Version identifier (e.g. '1.2.0').
            title: Display title for the version.
            aliases: Additional aliases (e.g. ['latest']).
            push: Whether to push to the remote after deploying.
            update_aliases: Whether to update existing aliases.

        Returns:
            True if deployment succeeded.
        """
        args = ["deploy"]
        if push:
            args.append("--push")
        if update_aliases:
            args.append("--update-aliases")
        args.append(version)
        if title:
            args.append(title)
        if aliases:
            args.extend(aliases)

        try:
            result = self._run_mike(args, check=False)
            if result.returncode != 0:
                logger.error(f"Mike deploy failed: {result.stderr}")
                return False
            return True
        except FileNotFoundError:
            logger.error("mike CLI not found. Install with: pip install mike")
            return False
        except Exception as e:
            logger.error(f"Error deploying version: {e}")
            return False

    def set_default(self, version: str, push: bool = False) -> bool:
        """Set the default documentation version.

        Args:
            version: Version to set as default.
            push: Whether to push to the remote.

        Returns:
            True if successful.
        """
        args = ["set-default"]
        if push:
            args.append("--push")
        args.append(version)

        try:
            result = self._run_mike(args, check=False)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Error setting default version: {e}")
            return False

    def delete_version(self, version: str, push: bool = False) -> bool:
        """Delete a deployed documentation version.

        Args:
            version: Version to delete.
            push: Whether to push to the remote.

        Returns:
            True if successful.
        """
        args = ["delete"]
        if push:
            args.append("--push")
        args.append(version)

        try:
            result = self._run_mike(args, check=False)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Error deleting version: {e}")
            return False

    def compare_versions(self, a: str, b: str) -> int:
        """Compare two version strings using SemanticVersionManager.

        Returns:
            -1 if a < b, 0 if a == b, 1 if a > b.
        """
        from .version_manager import SemanticVersionManager
        manager = SemanticVersionManager()
        return manager.compare_versions(a, b)

    # ------------------------------------------------------------------
    # Archival
    # ------------------------------------------------------------------

    def archive_old_versions(
        self,
        keep_count: int = 5,
        archive_prereleases: bool = True,
    ) -> List[str]:
        """Archive old versions, keeping the most recent ones.

        Args:
            keep_count: Number of recent stable versions to keep.
            archive_prereleases: Whether to archive prerelease versions too.

        Returns:
            List of version strings that were archived (deleted).
        """
        versions = self.list_versions()
        if not versions:
            return []

        # Separate stable and prerelease
        stable = []
        prerelease = []
        for v in versions:
            if any(tag in v.version for tag in ('alpha', 'beta', 'rc', 'dev')):
                prerelease.append(v)
            else:
                stable.append(v)

        archived: List[str] = []

        # Archive excess stable versions
        if len(stable) > keep_count:
            to_archive = stable[keep_count:]
            for v in to_archive:
                if self.delete_version(v.version):
                    archived.append(v.version)

        # Archive all prereleases if requested
        if archive_prereleases:
            for v in prerelease:
                if self.delete_version(v.version):
                    archived.append(v.version)

        return archived
