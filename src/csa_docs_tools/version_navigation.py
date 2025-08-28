"""Multi-version navigation and comparison tools for CSA documentation.

This module provides:
- Version switcher component generation
- Cross-version content comparison
- Migration path recommendations
- Version compatibility matrices
"""

import difflib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import yaml
from jinja2 import Environment, FileSystemLoader, Template
from markupsafe import Markup

from .mike_manager import MikeVersionManager, DeployedVersion
from .version_manager import SemanticVersionManager, VersionType


@dataclass
class NavigationConfig:
    """Configuration for version navigation components."""
    
    show_prerelease: bool = True
    show_development: bool = False
    show_legacy: bool = True
    group_by_major: bool = True
    max_versions_shown: int = 10
    default_comparison_depth: int = 3
    enable_search_across_versions: bool = True
    

@dataclass
class VersionDifference:
    """Represents a difference between versions."""
    
    section: str
    change_type: str  # 'added', 'removed', 'modified'
    content_before: Optional[str] = None
    content_after: Optional[str] = None
    line_number: Optional[int] = None
    severity: str = 'minor'  # 'minor', 'major', 'breaking'
    

@dataclass 
class MigrationPath:
    """Migration path between two versions."""
    
    from_version: str
    to_version: str
    steps: List[str] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)
    deprecations: List[str] = field(default_factory=list)
    new_features: List[str] = field(default_factory=list)
    effort_level: str = 'low'  # 'low', 'medium', 'high'
    estimated_time: str = '< 1 hour'
    

class VersionNavigationManager:
    """Manages multi-version navigation and comparison features."""
    
    def __init__(self, repo_path: Optional[Path] = None, 
                 config: Optional[NavigationConfig] = None):
        """Initialize version navigation manager.
        
        Args:
            repo_path: Path to repository root
            config: Navigation configuration
        """
        self.repo_path = repo_path or Path.cwd()
        self.config = config or NavigationConfig()
        self.mike_manager = MikeVersionManager(repo_path)
        self.version_manager = SemanticVersionManager()
        
        # Setup Jinja2 environment for templates
        template_dir = self.repo_path / "docs" / "templates" / "versioning"
        if template_dir.exists():
            self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        else:
            self.jinja_env = Environment(loader=FileSystemLoader("/"))
    
    def generate_version_switcher(self, current_version: str, 
                                 template_name: str = "version_switcher.html") -> str:
        """Generate HTML for version switcher component.
        
        Args:
            current_version: Currently displayed version
            template_name: Template file name
            
        Returns:
            Rendered HTML for version switcher
        """
        navigation_data = self.mike_manager.generate_version_navigation(current_version)
        
        # Filter versions based on configuration
        filtered_versions = self._filter_versions_for_navigation(navigation_data)
        
        # Group versions if configured
        if self.config.group_by_major:
            filtered_versions = self._group_versions_by_major(filtered_versions)
        
        # Prepare template context
        context = {
            'current_version': current_version,
            'versions': filtered_versions,
            'config': self.config,
            'total_versions': len(navigation_data['grouped_versions']['stable']) + 
                             len(navigation_data['grouped_versions']['prerelease']) + 
                             len(navigation_data['grouped_versions']['development'])
        }
        
        # Render template
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**context)
        except Exception:
            # Fallback to built-in template
            return self._render_default_version_switcher(context)
    
    def generate_version_comparison(self, version1: str, version2: str,
                                  include_content: bool = True) -> Dict[str, Any]:
        """Generate detailed comparison between two versions.
        
        Args:
            version1: First version to compare
            version2: Second version to compare
            include_content: Whether to include content differences
            
        Returns:
            Dictionary with comparison results
        """
        # Get basic version comparison
        basic_comparison = self.mike_manager.compare_versions(version1, version2)
        
        # Analyze semantic version differences
        semantic_analysis = self._analyze_semantic_differences(version1, version2)
        
        comparison = {
            **basic_comparison,
            'semantic_analysis': semantic_analysis,
            'migration_path': self.get_migration_path(version1, version2),
            'compatibility_level': self._assess_compatibility(version1, version2)
        }
        
        if include_content:
            content_differences = self._compare_version_content(version1, version2)
            comparison['content_differences'] = content_differences
        
        return comparison
    
    def get_migration_path(self, from_version: str, to_version: str) -> MigrationPath:
        """Get migration path between two versions.
        
        Args:
            from_version: Source version
            to_version: Target version
            
        Returns:
            MigrationPath with detailed migration information
        """
        try:
            from_parsed = self.version_manager.parse_version(from_version)
            to_parsed = self.version_manager.parse_version(to_version)
        except ValueError as e:
            raise ValueError(f"Invalid version format: {e}") from e
        
        migration = MigrationPath(
            from_version=from_version,
            to_version=to_version
        )
        
        # Determine migration complexity
        if from_parsed['major'] != to_parsed['major']:
            migration.effort_level = 'high'
            migration.estimated_time = '4-8 hours'
            migration.steps.extend([
                "Review breaking changes documentation",
                "Update configuration files",
                "Test critical functionality",
                "Update deployment scripts"
            ])
            migration.breaking_changes.extend(
                self._get_breaking_changes_between_versions(from_version, to_version)
            )
        elif from_parsed['minor'] != to_parsed['minor']:
            migration.effort_level = 'medium'
            migration.estimated_time = '1-2 hours'
            migration.steps.extend([
                "Review new features documentation",
                "Update configuration if needed",
                "Test new functionality"
            ])
            migration.new_features.extend(
                self._get_new_features_between_versions(from_version, to_version)
            )
        else:
            migration.effort_level = 'low'
            migration.estimated_time = '< 30 minutes'
            migration.steps.extend([
                "Review patch notes",
                "Apply version update",
                "Verify functionality"
            ])
        
        # Add deprecation warnings
        migration.deprecations.extend(
            self._get_deprecations_between_versions(from_version, to_version)
        )
        
        return migration
    
    def generate_compatibility_matrix(self, target_version: str) -> Dict[str, Any]:
        """Generate compatibility matrix for a target version.
        
        Args:
            target_version: Version to generate matrix for
            
        Returns:
            Compatibility matrix with version relationships
        """
        deployed_versions = self.mike_manager.list_versions()
        compatible_versions = self.version_manager.get_compatible_versions(target_version)
        
        matrix = {
            'target_version': target_version,
            'compatible_versions': [],
            'incompatible_versions': [],
            'upgrade_paths': [],
            'downgrade_paths': []
        }
        
        for version in deployed_versions:
            version_str = version.version
            
            if version_str in compatible_versions:
                compatibility_info = {
                    'version': version_str,
                    'title': version.title,
                    'compatibility_level': self._assess_compatibility(version_str, target_version),
                    'migration_effort': self.get_migration_path(version_str, target_version).effort_level
                }
                matrix['compatible_versions'].append(compatibility_info)
                
                # Determine upgrade/downgrade paths
                comparison = self.version_manager.compare_versions(version_str, target_version)
                if comparison < 0:
                    matrix['upgrade_paths'].append(compatibility_info)
                elif comparison > 0:
                    matrix['downgrade_paths'].append(compatibility_info)
            else:
                matrix['incompatible_versions'].append({
                    'version': version_str,
                    'title': version.title,
                    'reason': 'Major version difference'
                })
        
        # Sort paths by version
        matrix['upgrade_paths'].sort(key=lambda x: self.version_manager.parse_version(x['version'])['clean'])
        matrix['downgrade_paths'].sort(key=lambda x: self.version_manager.parse_version(x['version'])['clean'], reverse=True)
        
        return matrix
    
    def generate_version_selector_data(self) -> Dict[str, Any]:
        """Generate data for version selector components.
        
        Returns:
            Data structure for version selection UI
        """
        deployed_versions = self.mike_manager.list_versions()
        
        # Group versions by type and major version
        grouped_data = {
            'stable_releases': {},
            'prerelease_versions': [],
            'development_versions': [],
            'legacy_versions': []
        }
        
        for version in deployed_versions:
            try:
                parsed = self.version_manager.parse_version(version.version)
                version_info = {
                    'version': version.version,
                    'title': version.title,
                    'aliases': version.aliases,
                    'is_default': version.is_default,
                    'parsed': parsed
                }
                
                if parsed['prerelease']:
                    if 'alpha' in parsed['prerelease'] or 'beta' in parsed['prerelease']:
                        grouped_data['prerelease_versions'].append(version_info)
                    else:
                        grouped_data['development_versions'].append(version_info)
                else:
                    major_version = f"v{parsed['major']}.x"
                    if major_version not in grouped_data['stable_releases']:
                        grouped_data['stable_releases'][major_version] = []
                    grouped_data['stable_releases'][major_version].append(version_info)
                    
            except ValueError:
                # Handle non-semantic versions
                grouped_data['legacy_versions'].append({
                    'version': version.version,
                    'title': version.title,
                    'aliases': version.aliases,
                    'is_default': version.is_default
                })
        
        # Sort versions within each group
        for major_group in grouped_data['stable_releases'].values():
            major_group.sort(key=lambda x: x['parsed']['clean'], reverse=True)
        
        grouped_data['prerelease_versions'].sort(key=lambda x: x['parsed']['clean'], reverse=True)
        grouped_data['development_versions'].sort(key=lambda x: x['parsed']['clean'], reverse=True)
        
        return grouped_data
    
    def create_version_aware_search_index(self) -> Dict[str, Any]:
        """Create search index that works across multiple versions.
        
        Returns:
            Search index data structure
        """
        deployed_versions = self.mike_manager.list_versions()
        
        search_index = {
            'versions': {},
            'global_index': {},
            'version_mapping': {}
        }
        
        for version in deployed_versions:
            version_str = version.version
            
            # This would need to be implemented with actual content parsing
            # For now, create placeholder structure
            search_index['versions'][version_str] = {
                'title': version.title,
                'aliases': version.aliases,
                'pages': [],  # Would contain page-specific search data
                'keywords': [],  # Version-specific keywords
                'last_updated': None
            }
            
            # Map aliases to main version
            for alias in version.aliases:
                search_index['version_mapping'][alias] = version_str
        
        return search_index
    
    def _filter_versions_for_navigation(self, navigation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Filter versions based on configuration settings."""
        filtered = {'grouped_versions': {}}
        
        if self.config.show_prerelease:
            filtered['grouped_versions']['prerelease'] = navigation_data['grouped_versions']['prerelease']
        
        if self.config.show_development:
            filtered['grouped_versions']['development'] = navigation_data['grouped_versions']['development']
        
        if self.config.show_legacy:
            filtered['grouped_versions']['legacy'] = navigation_data['grouped_versions']['legacy']
        
        # Always show stable versions
        stable_versions = navigation_data['grouped_versions']['stable']
        if len(stable_versions) > self.config.max_versions_shown:
            stable_versions = stable_versions[:self.config.max_versions_shown]
        
        filtered['grouped_versions']['stable'] = stable_versions
        
        return filtered
    
    def _group_versions_by_major(self, filtered_versions: Dict[str, Any]) -> Dict[str, Any]:
        """Group versions by major version number."""
        grouped = {'grouped_versions': {'major_groups': {}}}
        
        for version_type, versions in filtered_versions['grouped_versions'].items():
            if version_type == 'stable':
                for version in versions:
                    try:
                        parsed = self.version_manager.parse_version(version['version'])
                        major_key = f"v{parsed['major']}.x"
                        
                        if major_key not in grouped['grouped_versions']['major_groups']:
                            grouped['grouped_versions']['major_groups'][major_key] = []
                        
                        grouped['grouped_versions']['major_groups'][major_key].append(version)
                    except ValueError:
                        # Handle non-semantic versions separately
                        if 'other' not in grouped['grouped_versions']:
                            grouped['grouped_versions']['other'] = []
                        grouped['grouped_versions']['other'].append(version)
            else:
                grouped['grouped_versions'][version_type] = versions
        
        return grouped
    
    def _analyze_semantic_differences(self, version1: str, version2: str) -> Dict[str, Any]:
        """Analyze semantic differences between versions."""
        try:
            parsed1 = self.version_manager.parse_version(version1)
            parsed2 = self.version_manager.parse_version(version2)
            
            release_type = self.version_manager.determine_release_type(version1, version2)
            
            return {
                'release_type': release_type.value,
                'major_change': parsed1['major'] != parsed2['major'],
                'minor_change': parsed1['minor'] != parsed2['minor'],
                'patch_change': parsed1['patch'] != parsed2['patch'],
                'prerelease_change': parsed1['prerelease'] != parsed2['prerelease'],
                'is_upgrade': self.version_manager.compare_versions(version1, version2) < 0,
                'version_distance': abs(parsed2['major'] - parsed1['major']) * 100 + 
                                  abs(parsed2['minor'] - parsed1['minor']) * 10 + 
                                  abs(parsed2['patch'] - parsed1['patch'])
            }
        except ValueError as e:
            return {
                'error': f"Cannot analyze semantic differences: {e}",
                'release_type': 'unknown',
                'major_change': False,
                'minor_change': False,
                'patch_change': False
            }
    
    def _compare_version_content(self, version1: str, version2: str) -> List[VersionDifference]:
        """Compare content between two versions."""
        # This would need implementation with actual content comparison
        # For now, return placeholder structure
        differences = []
        
        # Placeholder implementation
        # In a real implementation, this would:
        # 1. Load content from both versions
        # 2. Parse and compare documentation structure
        # 3. Identify added, removed, or modified sections
        # 4. Calculate change severity
        
        return differences
    
    def _assess_compatibility(self, version1: str, version2: str) -> str:
        """Assess compatibility level between versions."""
        try:
            parsed1 = self.version_manager.parse_version(version1)
            parsed2 = self.version_manager.parse_version(version2)
            
            if parsed1['major'] != parsed2['major']:
                return 'incompatible'
            elif parsed1['minor'] != parsed2['minor']:
                return 'partially_compatible'
            else:
                return 'fully_compatible'
        except ValueError:
            return 'unknown'
    
    def _get_breaking_changes_between_versions(self, from_version: str, to_version: str) -> List[str]:
        """Get breaking changes between versions."""
        # Placeholder implementation
        # In a real system, this would parse changelog or release notes
        return []
    
    def _get_new_features_between_versions(self, from_version: str, to_version: str) -> List[str]:
        """Get new features between versions."""
        # Placeholder implementation
        return []
    
    def _get_deprecations_between_versions(self, from_version: str, to_version: str) -> List[str]:
        """Get deprecations between versions."""
        # Placeholder implementation
        return []
    
    def _render_default_version_switcher(self, context: Dict[str, Any]) -> str:
        """Render default version switcher HTML."""
        html_parts = [
            '<div class="version-switcher">',
            f'<div class="current-version">Current: {context["current_version"]}</div>',
            '<div class="version-list">'
        ]
        
        # Add version options
        for version_type, versions in context['versions']['grouped_versions'].items():
            if versions:
                html_parts.append(f'<div class="version-group {version_type}">')
                html_parts.append(f'<h4>{version_type.replace("_", " ").title()}</h4>')
                
                for version in versions:
                    current_class = ' current' if version['version'] == context['current_version'] else ''
                    html_parts.append(
                        f'<a href="../{version["version"]}/" class="version-link{current_class}">{version["title"]}</a>'
                    )
                
                html_parts.append('</div>')
        
        html_parts.extend(['</div>', '</div>'])
        
        return '\n'.join(html_parts)
