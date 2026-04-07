"""Semantic version management for documentation releases."""

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
import logging

logger = logging.getLogger(__name__)


class VersionType(Enum):
    """Types of version releases."""
    STABLE = "stable"
    PRERELEASE = "prerelease"
    DEVELOPMENT = "development"


@dataclass
class VersionInfo:
    """Information about a documentation version."""
    version: str
    version_type: VersionType = VersionType.STABLE
    title: str = ""
    aliases: List[str] = field(default_factory=list)
    is_default: bool = False
    release_date: str = ""
    changelog_path: str = ""


# Precompiled regex for version parsing
_VERSION_PATTERN = re.compile(
    r'^v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)'
    r'(?:-(?P<pre>[a-zA-Z0-9]+(?:\.\d+)?))?'
    r'(?:\+(?P<build>[a-zA-Z0-9.]+))?$'
)


class SemanticVersionManager:
    """Manage semantic versioning for documentation."""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize version manager.

        Args:
            config_path: Path to versions.yml configuration file.
                         If None, operates without persistence.
        """
        self.config_path = config_path
        self.versions: List[VersionInfo] = []
        if self.config_path and self.config_path.exists():
            self._load_versions()

    def _load_versions(self) -> None:
        """Load version information from config file."""
        if not self.config_path or not self.config_path.exists():
            return
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            for entry in data.get('versions', []):
                self.versions.append(VersionInfo(
                    version=entry.get('version', ''),
                    version_type=VersionType(entry.get('type', 'stable')),
                    title=entry.get('title', ''),
                    aliases=entry.get('aliases', []),
                    is_default=entry.get('is_default', False),
                    release_date=entry.get('release_date', ''),
                    changelog_path=entry.get('changelog_path', ''),
                ))
        except Exception as e:
            logger.error(f"Error loading versions from {self.config_path}: {e}")

    def _save_versions(self) -> None:
        """Persist version information to config file."""
        if not self.config_path:
            return
        data = {
            'versions': [
                {
                    'version': v.version,
                    'type': v.version_type.value,
                    'title': v.title,
                    'aliases': v.aliases,
                    'is_default': v.is_default,
                    'release_date': v.release_date,
                    'changelog_path': v.changelog_path,
                }
                for v in self.versions
            ]
        }
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            logger.error(f"Error saving versions to {self.config_path}: {e}")

    def parse_version(self, version_string: str) -> Dict[str, object]:
        """Parse a semantic version string.

        Args:
            version_string: Version string (e.g. 'v1.2.3', '1.2.3-alpha.1')

        Returns:
            Dictionary with major, minor, patch, prerelease, build_metadata keys.

        Raises:
            ValueError: If version string is not valid semver.
        """
        match = _VERSION_PATTERN.match(version_string.strip())
        if not match:
            raise ValueError(
                f"Invalid semantic version: '{version_string}'. "
                "Expected format: [v]MAJOR.MINOR.PATCH[-prerelease][+build]"
            )
        return {
            'major': int(match.group('major')),
            'minor': int(match.group('minor')),
            'patch': int(match.group('patch')),
            'prerelease': match.group('pre'),
            'build_metadata': match.group('build'),
        }

    def compare_versions(self, a: str, b: str) -> int:
        """Compare two semantic version strings.

        Returns:
            -1 if a < b, 0 if a == b, 1 if a > b
        """
        pa = self.parse_version(a)
        pb = self.parse_version(b)

        for key in ('major', 'minor', 'patch'):
            if pa[key] < pb[key]:
                return -1
            if pa[key] > pb[key]:
                return 1

        # Prerelease versions have lower precedence than release
        pre_a = pa['prerelease']
        pre_b = pb['prerelease']
        if pre_a and not pre_b:
            return -1
        if not pre_a and pre_b:
            return 1
        if pre_a and pre_b:
            if pre_a < pre_b:
                return -1
            if pre_a > pre_b:
                return 1

        return 0

    def add_version(self, version_info: VersionInfo) -> None:
        """Add a version to the managed list.

        If is_default is True, clears default flag on all other versions.
        Persists to disk if config_path is set.
        """
        if version_info.is_default:
            for v in self.versions:
                v.is_default = False

        # Replace if version already exists
        self.versions = [v for v in self.versions if v.version != version_info.version]
        self.versions.insert(0, version_info)
        self._save_versions()

    def get_version(self, version_string: str) -> Optional[VersionInfo]:
        """Retrieve a specific version by its version string."""
        for v in self.versions:
            if v.version == version_string:
                return v
        return None

    def get_latest_stable(self) -> Optional[VersionInfo]:
        """Return the latest stable version."""
        stable = [v for v in self.versions if v.version_type == VersionType.STABLE]
        if not stable:
            return None
        stable.sort(key=lambda v: v.version, reverse=True)
        return stable[0]

    def list_versions(self, include_prerelease: bool = True) -> List[VersionInfo]:
        """List all managed versions.

        Args:
            include_prerelease: Whether to include prerelease/dev versions.
        """
        if include_prerelease:
            return list(self.versions)
        return [v for v in self.versions if v.version_type == VersionType.STABLE]

    def bump_version(self, current: str, bump_type: str = "patch") -> str:
        """Calculate the next version.

        Args:
            current: Current version string.
            bump_type: One of 'major', 'minor', 'patch'.

        Returns:
            New version string (without 'v' prefix).
        """
        parsed = self.parse_version(current)
        major, minor, patch = parsed['major'], parsed['minor'], parsed['patch']

        if bump_type == 'major':
            return f"{major + 1}.0.0"
        elif bump_type == 'minor':
            return f"{major}.{minor + 1}.0"
        else:
            return f"{major}.{minor}.{patch + 1}"
