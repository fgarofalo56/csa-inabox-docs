"""Version management utilities for CSA documentation.

This module provides comprehensive version management functionality including:
- Semantic version parsing and validation
- Version comparison and ordering
- Release type determination
- Version bumping automation
- Compatibility checking
"""

import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import yaml
from packaging.version import Version as PackagingVersion


class ReleaseType(Enum):
    """Types of version releases following semantic versioning."""
    
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    PRERELEASE = "prerelease"
    BUILD = "build"


class VersionType(Enum):
    """Types of versions in the documentation system."""
    
    STABLE = "stable"
    PRERELEASE = "prerelease"
    DEVELOPMENT = "development"
    LEGACY = "legacy"


@dataclass
class VersionInfo:
    """Information about a documentation version."""
    
    version: str
    version_type: VersionType
    title: str
    aliases: List[str]
    is_default: bool = False
    release_date: Optional[str] = None
    changelog_path: Optional[str] = None
    migration_notes: Optional[str] = None
    compatibility_notes: Optional[str] = None
    deprecation_date: Optional[str] = None
    
    def __post_init__(self):
        """Validate version info after initialization."""
        if not self.version:
            raise ValueError("Version cannot be empty")
        if not self.title:
            raise ValueError("Title cannot be empty")
        
        # Validate version format
        try:
            PackagingVersion(self.version)
        except Exception as e:
            raise ValueError(f"Invalid version format '{self.version}': {e}") from e


class SemanticVersionManager:
    """Manages semantic versioning for documentation releases."""
    
    VERSION_PATTERN = re.compile(
        r"^v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
        r"(?:-(?P<prerelease>[a-zA-Z0-9.-]+))?"
        r"(?:\+(?P<build>[a-zA-Z0-9.-]+))?$"
    )
    
    def __init__(self, config_file: Optional[Path] = None):
        """Initialize version manager.
        
        Args:
            config_file: Path to version configuration file
        """
        self.config_file = config_file or Path("versions.yml")
        self.versions: List[VersionInfo] = []
        self._load_versions()
    
    def parse_version(self, version_str: str) -> Dict[str, Union[str, int, None]]:
        """Parse a semantic version string.
        
        Args:
            version_str: Version string to parse (e.g., 'v1.2.3-alpha.1+build.123')
            
        Returns:
            Dict containing parsed version components
            
        Raises:
            ValueError: If version string is invalid
        """
        # Remove 'v' prefix if present
        clean_version = version_str.lstrip('v')
        
        match = self.VERSION_PATTERN.match(f"v{clean_version}")
        if not match:
            raise ValueError(f"Invalid semantic version format: {version_str}")
        
        return {
            'major': int(match.group('major')),
            'minor': int(match.group('minor')),
            'patch': int(match.group('patch')),
            'prerelease': match.group('prerelease'),
            'build': match.group('build'),
            'original': version_str,
            'clean': clean_version
        }
    
    def compare_versions(self, version1: str, version2: str) -> int:
        """Compare two semantic versions.
        
        Args:
            version1: First version to compare
            version2: Second version to compare
            
        Returns:
            -1 if version1 < version2, 0 if equal, 1 if version1 > version2
        """
        try:
            v1 = PackagingVersion(version1.lstrip('v'))
            v2 = PackagingVersion(version2.lstrip('v'))
            
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1
            else:
                return 0
        except Exception as e:
            raise ValueError(f"Error comparing versions '{version1}' and '{version2}': {e}") from e
    
    def determine_release_type(self, current_version: str, target_version: str) -> ReleaseType:
        """Determine the type of release based on version change.
        
        Args:
            current_version: Current version
            target_version: Target version
            
        Returns:
            Type of release (MAJOR, MINOR, PATCH, etc.)
        """
        current = self.parse_version(current_version)
        target = self.parse_version(target_version)
        
        if target['major'] > current['major']:
            return ReleaseType.MAJOR
        elif target['minor'] > current['minor']:
            return ReleaseType.MINOR
        elif target['patch'] > current['patch']:
            return ReleaseType.PATCH
        elif target['prerelease'] and not current['prerelease']:
            return ReleaseType.PRERELEASE
        elif target['build'] and not current['build']:
            return ReleaseType.BUILD
        else:
            return ReleaseType.PATCH  # Default to patch for same version
    
    def bump_version(self, current_version: str, release_type: ReleaseType, 
                    prerelease_tag: Optional[str] = None) -> str:
        """Bump version according to semantic versioning rules.
        
        Args:
            current_version: Current version string
            release_type: Type of version bump
            prerelease_tag: Tag for prerelease versions (e.g., 'alpha', 'beta')
            
        Returns:
            New version string
        """
        parsed = self.parse_version(current_version)
        major, minor, patch = parsed['major'], parsed['minor'], parsed['patch']
        
        if release_type == ReleaseType.MAJOR:
            major += 1
            minor = 0
            patch = 0
        elif release_type == ReleaseType.MINOR:
            minor += 1
            patch = 0
        elif release_type == ReleaseType.PATCH:
            patch += 1
        
        new_version = f"{major}.{minor}.{patch}"
        
        if release_type == ReleaseType.PRERELEASE and prerelease_tag:
            new_version += f"-{prerelease_tag}.1"
        
        return new_version
    
    def get_latest_version(self) -> Optional[str]:
        """Get the latest stable version.
        
        Returns:
            Latest version string or None if no versions exist
        """
        stable_versions = [
            v.version for v in self.versions 
            if v.version_type == VersionType.STABLE
        ]
        
        if not stable_versions:
            return None
        
        return max(stable_versions, key=lambda v: PackagingVersion(v.lstrip('v')))
    
    def get_version_info(self, version: str) -> Optional[VersionInfo]:
        """Get information about a specific version.
        
        Args:
            version: Version string to look up
            
        Returns:
            VersionInfo object or None if not found
        """
        for v in self.versions:
            if v.version == version or version in v.aliases:
                return v
        return None
    
    def add_version(self, version_info: VersionInfo) -> None:
        """Add a new version to the manager.
        
        Args:
            version_info: Version information to add
        """
        # Validate version doesn't already exist
        if self.get_version_info(version_info.version):
            raise ValueError(f"Version {version_info.version} already exists")
        
        self.versions.append(version_info)
        self._save_versions()
    
    def remove_version(self, version: str) -> bool:
        """Remove a version from the manager.
        
        Args:
            version: Version string to remove
            
        Returns:
            True if version was removed, False if not found
        """
        for i, v in enumerate(self.versions):
            if v.version == version:
                del self.versions[i]
                self._save_versions()
                return True
        return False
    
    def get_compatible_versions(self, target_version: str) -> List[str]:
        """Get versions compatible with the target version.
        
        Args:
            target_version: Version to check compatibility against
            
        Returns:
            List of compatible version strings
        """
        target_parsed = self.parse_version(target_version)
        compatible = []
        
        for version_info in self.versions:
            try:
                version_parsed = self.parse_version(version_info.version)
                
                # Same major version is considered compatible
                if version_parsed['major'] == target_parsed['major']:
                    compatible.append(version_info.version)
            except ValueError:
                # Skip invalid versions
                continue
        
        return compatible
    
    def _load_versions(self) -> None:
        """Load versions from configuration file."""
        if not self.config_file.exists():
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            
            versions_data = data.get('versions', [])
            self.versions = [
                VersionInfo(**version_data) for version_data in versions_data
            ]
        except Exception as e:
            raise ValueError(f"Error loading versions from {self.config_file}: {e}") from e
    
    def _save_versions(self) -> None:
        """Save versions to configuration file."""
        try:
            # Create directory if it doesn't exist
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                'versions': [
                    {
                        'version': v.version,
                        'version_type': v.version_type.value,
                        'title': v.title,
                        'aliases': v.aliases,
                        'is_default': v.is_default,
                        'release_date': v.release_date,
                        'changelog_path': v.changelog_path,
                        'migration_notes': v.migration_notes,
                        'compatibility_notes': v.compatibility_notes,
                        'deprecation_date': v.deprecation_date
                    }
                    for v in self.versions
                ]
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=True)
        except Exception as e:
            raise ValueError(f"Error saving versions to {self.config_file}: {e}") from e


def validate_version_constraints(versions: List[str]) -> Tuple[bool, List[str]]:
    """Validate version constraints and compatibility.
    
    Args:
        versions: List of version strings to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    manager = SemanticVersionManager()
    
    # Check for duplicate versions
    if len(versions) != len(set(versions)):
        errors.append("Duplicate versions found")
    
    # Validate each version format
    for version in versions:
        try:
            manager.parse_version(version)
        except ValueError as e:
            errors.append(f"Invalid version format '{version}': {e}")
    
    # Check version ordering
    try:
        sorted_versions = sorted(versions, key=lambda v: PackagingVersion(v.lstrip('v')))
        if versions != sorted_versions:
            errors.append("Versions are not in ascending order")
    except Exception as e:
        errors.append(f"Error validating version ordering: {e}")
    
    return len(errors) == 0, errors
