"""Version migration tools and utilities for CSA documentation.

This module provides:
- Content migration between versions
- Breaking change documentation
- Deprecation notices
- Migration guides generation
- Backward compatibility validation
"""

import json
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import yaml
from jinja2 import Environment, FileSystemLoader

from .version_manager import SemanticVersionManager, VersionInfo, VersionType
from .mike_manager import MikeVersionManager


@dataclass
class MigrationRule:
    """Rule for migrating content between versions."""
    
    rule_id: str
    name: str
    description: str
    from_version: str
    to_version: str
    rule_type: str  # 'content', 'structure', 'navigation', 'config'
    action: str  # 'move', 'copy', 'rename', 'delete', 'transform'
    source_path: str
    target_path: Optional[str] = None
    transformation_script: Optional[str] = None
    conditions: List[str] = field(default_factory=list)
    is_breaking: bool = False
    deprecation_date: Optional[str] = None
    removal_date: Optional[str] = None
    

@dataclass
class BreakingChange:
    """Information about a breaking change."""
    
    change_id: str
    title: str
    description: str
    introduced_in: str
    affects: List[str]  # Areas affected: 'api', 'config', 'ui', 'content'
    migration_steps: List[str]
    workaround: Optional[str] = None
    severity: str = 'high'  # 'low', 'medium', 'high', 'critical'
    

@dataclass
class DeprecationNotice:
    """Notice about deprecated features or content."""
    
    notice_id: str
    title: str
    description: str
    deprecated_in: str
    removal_planned: Optional[str] = None
    replacement: Optional[str] = None
    migration_guide: Optional[str] = None
    affected_pages: List[str] = field(default_factory=list)
    

@dataclass
class MigrationGuide:
    """Complete migration guide between versions."""
    
    from_version: str
    to_version: str
    title: str
    overview: str
    breaking_changes: List[BreakingChange] = field(default_factory=list)
    deprecations: List[DeprecationNotice] = field(default_factory=list)
    migration_steps: List[str] = field(default_factory=list)
    testing_checklist: List[str] = field(default_factory=list)
    rollback_instructions: Optional[str] = None
    estimated_effort: str = "Medium"
    

class MigrationManager:
    """Manages version migrations and content transformations."""
    
    def __init__(self, repo_path: Optional[Path] = None):
        """Initialize migration manager.
        
        Args:
            repo_path: Path to repository root
        """
        self.repo_path = repo_path or Path.cwd()
        self.config_dir = self.repo_path / "docs" / "migration"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.version_manager = SemanticVersionManager()
        self.mike_manager = MikeVersionManager(repo_path)
        
        # Load migration configuration
        self.migration_rules: List[MigrationRule] = []
        self.breaking_changes: List[BreakingChange] = []
        self.deprecations: List[DeprecationNotice] = []
        
        self._load_migration_config()
        
        # Setup Jinja2 for templates
        template_dir = self.repo_path / "docs" / "templates" / "migration"
        if template_dir.exists():
            self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        else:
            self.jinja_env = Environment(loader=FileSystemLoader("/"))
    
    def create_migration_guide(self, from_version: str, to_version: str, 
                              output_path: Optional[Path] = None) -> MigrationGuide:
        """Create comprehensive migration guide between versions.
        
        Args:
            from_version: Source version
            to_version: Target version
            output_path: Path to save the guide
            
        Returns:
            Generated migration guide
        """
        # Analyze version differences
        try:
            parsed_from = self.version_manager.parse_version(from_version)
            parsed_to = self.version_manager.parse_version(to_version)
        except ValueError as e:
            raise ValueError(f"Invalid version format: {e}") from e
        
        # Determine migration complexity
        if parsed_from['major'] != parsed_to['major']:
            effort = "High"
            complexity = "Major version upgrade with potential breaking changes"
        elif parsed_from['minor'] != parsed_to['minor']:
            effort = "Medium"
            complexity = "Minor version upgrade with new features"
        else:
            effort = "Low"
            complexity = "Patch upgrade with bug fixes and improvements"
        
        # Get applicable breaking changes and deprecations
        applicable_breaking = self._get_breaking_changes_for_range(from_version, to_version)
        applicable_deprecations = self._get_deprecations_for_range(from_version, to_version)
        
        # Generate migration steps
        migration_steps = self._generate_migration_steps(from_version, to_version)
        
        # Create testing checklist
        testing_checklist = self._generate_testing_checklist(from_version, to_version)
        
        # Create the migration guide
        guide = MigrationGuide(
            from_version=from_version,
            to_version=to_version,
            title=f"Migration Guide: {from_version} to {to_version}",
            overview=f"This guide helps you migrate from version {from_version} to {to_version}. {complexity}",
            breaking_changes=applicable_breaking,
            deprecations=applicable_deprecations,
            migration_steps=migration_steps,
            testing_checklist=testing_checklist,
            estimated_effort=effort
        )
        
        # Save guide if output path provided
        if output_path:
            self._save_migration_guide(guide, output_path)
        
        return guide
    
    def apply_migration_rules(self, from_version: str, to_version: str, 
                             dry_run: bool = True) -> Dict[str, Any]:
        """Apply migration rules to transform content.
        
        Args:
            from_version: Source version
            to_version: Target version
            dry_run: Whether to perform a dry run
            
        Returns:
            Results of migration rule application
        """
        applicable_rules = [
            rule for rule in self.migration_rules
            if self._is_rule_applicable(rule, from_version, to_version)
        ]
        
        results = {
            'applied_rules': [],
            'failed_rules': [],
            'modified_files': [],
            'warnings': [],
            'dry_run': dry_run
        }
        
        for rule in applicable_rules:
            try:
                result = self._apply_migration_rule(rule, dry_run)
                results['applied_rules'].append({
                    'rule_id': rule.rule_id,
                    'name': rule.name,
                    'result': result
                })
                
                if 'modified_files' in result:
                    results['modified_files'].extend(result['modified_files'])
                    
            except Exception as e:
                results['failed_rules'].append({
                    'rule_id': rule.rule_id,
                    'name': rule.name,
                    'error': str(e)
                })
        
        return results
    
    def validate_backward_compatibility(self, version: str) -> Tuple[bool, List[str]]:
        """Validate backward compatibility for a version.
        
        Args:
            version: Version to validate
            
        Returns:
            Tuple of (is_compatible, list_of_issues)
        """
        issues = []
        
        # Get all breaking changes that affect this version
        breaking_changes = [
            change for change in self.breaking_changes
            if self.version_manager.compare_versions(change.introduced_in, version) <= 0
        ]
        
        # Check for critical breaking changes
        critical_changes = [change for change in breaking_changes if change.severity == 'critical']
        if critical_changes:
            issues.extend([
                f"Critical breaking change: {change.title}" for change in critical_changes
            ])
        
        # Check for deprecated features that should be removed
        for deprecation in self.deprecations:
            if (deprecation.removal_planned and 
                self.version_manager.compare_versions(deprecation.removal_planned, version) <= 0):
                issues.append(f"Deprecated feature should be removed: {deprecation.title}")
        
        # Check migration rules for breaking changes
        breaking_rules = [rule for rule in self.migration_rules if rule.is_breaking]
        for rule in breaking_rules:
            if self._is_rule_applicable(rule, rule.from_version, version):
                issues.append(f"Breaking migration rule applies: {rule.name}")
        
        return len(issues) == 0, issues
    
    def generate_deprecation_warnings(self, version: str) -> List[Dict[str, Any]]:
        """Generate deprecation warnings for a version.
        
        Args:
            version: Version to generate warnings for
            
        Returns:
            List of deprecation warning data
        """
        warnings = []
        
        for deprecation in self.deprecations:
            # Check if deprecation applies to this version
            if self.version_manager.compare_versions(deprecation.deprecated_in, version) <= 0:
                # Calculate urgency based on removal date
                urgency = "low"
                if deprecation.removal_planned:
                    try:
                        removal_version = self.version_manager.parse_version(deprecation.removal_planned)
                        current_version = self.version_manager.parse_version(version)
                        
                        if removal_version['major'] == current_version['major']:
                            urgency = "high"  # Removal in same major version
                        elif removal_version['major'] == current_version['major'] + 1:
                            urgency = "medium"  # Removal in next major version
                    except ValueError:
                        pass
                
                warnings.append({
                    'id': deprecation.notice_id,
                    'title': deprecation.title,
                    'description': deprecation.description,
                    'deprecated_in': deprecation.deprecated_in,
                    'removal_planned': deprecation.removal_planned,
                    'replacement': deprecation.replacement,
                    'migration_guide': deprecation.migration_guide,
                    'affected_pages': deprecation.affected_pages,
                    'urgency': urgency
                })
        
        return warnings
    
    def create_migration_checklist(self, from_version: str, to_version: str) -> List[Dict[str, Any]]:
        """Create detailed migration checklist.
        
        Args:
            from_version: Source version
            to_version: Target version
            
        Returns:
            Structured migration checklist
        """
        checklist = []
        
        # Pre-migration checks
        checklist.append({
            'category': 'Pre-Migration',
            'items': [
                {'task': f'Backup current documentation from {from_version}', 'completed': False},
                {'task': 'Review release notes and changelog', 'completed': False},
                {'task': 'Identify customizations that may be affected', 'completed': False},
                {'task': 'Plan downtime window if required', 'completed': False}
            ]
        })
        
        # Breaking changes
        breaking_changes = self._get_breaking_changes_for_range(from_version, to_version)
        if breaking_changes:
            checklist.append({
                'category': 'Breaking Changes',
                'items': [
                    {'task': f'Address: {change.title}', 'completed': False}
                    for change in breaking_changes
                ]
            })
        
        # Content migration
        applicable_rules = [
            rule for rule in self.migration_rules
            if self._is_rule_applicable(rule, from_version, to_version)
        ]
        
        if applicable_rules:
            checklist.append({
                'category': 'Content Migration', 
                'items': [
                    {'task': f'Apply migration rule: {rule.name}', 'completed': False}
                    for rule in applicable_rules
                ]
            })
        
        # Testing
        checklist.append({
            'category': 'Testing',
            'items': [
                {'task': 'Test documentation build', 'completed': False},
                {'task': 'Verify all links work correctly', 'completed': False},
                {'task': 'Check navigation structure', 'completed': False},
                {'task': 'Test search functionality', 'completed': False},
                {'task': 'Validate responsive design', 'completed': False}
            ]
        })
        
        # Post-migration
        checklist.append({
            'category': 'Post-Migration',
            'items': [
                {'task': f'Deploy version {to_version}', 'completed': False},
                {'task': 'Update version aliases if needed', 'completed': False},
                {'task': 'Notify users of the update', 'completed': False},
                {'task': 'Monitor for issues', 'completed': False}
            ]
        })
        
        return checklist
    
    def add_breaking_change(self, breaking_change: BreakingChange) -> None:
        """Add a breaking change to the registry.
        
        Args:
            breaking_change: Breaking change information
        """
        # Check if change already exists
        existing = next(
            (change for change in self.breaking_changes if change.change_id == breaking_change.change_id),
            None
        )
        
        if existing:
            # Update existing change
            idx = self.breaking_changes.index(existing)
            self.breaking_changes[idx] = breaking_change
        else:
            # Add new change
            self.breaking_changes.append(breaking_change)
        
        self._save_breaking_changes()
    
    def add_deprecation_notice(self, deprecation: DeprecationNotice) -> None:
        """Add a deprecation notice.
        
        Args:
            deprecation: Deprecation notice information
        """
        # Check if notice already exists
        existing = next(
            (notice for notice in self.deprecations if notice.notice_id == deprecation.notice_id),
            None
        )
        
        if existing:
            # Update existing notice
            idx = self.deprecations.index(existing)
            self.deprecations[idx] = deprecation
        else:
            # Add new notice
            self.deprecations.append(deprecation)
        
        self._save_deprecations()
    
    def add_migration_rule(self, migration_rule: MigrationRule) -> None:
        """Add a migration rule.
        
        Args:
            migration_rule: Migration rule information
        """
        # Check if rule already exists
        existing = next(
            (rule for rule in self.migration_rules if rule.rule_id == migration_rule.rule_id),
            None
        )
        
        if existing:
            # Update existing rule
            idx = self.migration_rules.index(existing)
            self.migration_rules[idx] = migration_rule
        else:
            # Add new rule
            self.migration_rules.append(migration_rule)
        
        self._save_migration_rules()
    
    def _load_migration_config(self) -> None:
        """Load migration configuration from files."""
        # Load breaking changes
        breaking_changes_file = self.config_dir / "breaking_changes.yml"
        if breaking_changes_file.exists():
            with open(breaking_changes_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
                self.breaking_changes = [
                    BreakingChange(**change_data) 
                    for change_data in data.get('breaking_changes', [])
                ]
        
        # Load deprecations
        deprecations_file = self.config_dir / "deprecations.yml"
        if deprecations_file.exists():
            with open(deprecations_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
                self.deprecations = [
                    DeprecationNotice(**deprecation_data)
                    for deprecation_data in data.get('deprecations', [])
                ]
        
        # Load migration rules
        migration_rules_file = self.config_dir / "migration_rules.yml"
        if migration_rules_file.exists():
            with open(migration_rules_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
                self.migration_rules = [
                    MigrationRule(**rule_data)
                    for rule_data in data.get('migration_rules', [])
                ]
    
    def _save_breaking_changes(self) -> None:
        """Save breaking changes to file."""
        breaking_changes_file = self.config_dir / "breaking_changes.yml"
        data = {
            'breaking_changes': [
                {
                    'change_id': change.change_id,
                    'title': change.title,
                    'description': change.description,
                    'introduced_in': change.introduced_in,
                    'affects': change.affects,
                    'migration_steps': change.migration_steps,
                    'workaround': change.workaround,
                    'severity': change.severity
                }
                for change in self.breaking_changes
            ]
        }
        
        with open(breaking_changes_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=True)
    
    def _save_deprecations(self) -> None:
        """Save deprecation notices to file."""
        deprecations_file = self.config_dir / "deprecations.yml"
        data = {
            'deprecations': [
                {
                    'notice_id': dep.notice_id,
                    'title': dep.title,
                    'description': dep.description,
                    'deprecated_in': dep.deprecated_in,
                    'removal_planned': dep.removal_planned,
                    'replacement': dep.replacement,
                    'migration_guide': dep.migration_guide,
                    'affected_pages': dep.affected_pages
                }
                for dep in self.deprecations
            ]
        }
        
        with open(deprecations_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=True)
    
    def _save_migration_rules(self) -> None:
        """Save migration rules to file."""
        migration_rules_file = self.config_dir / "migration_rules.yml"
        data = {
            'migration_rules': [
                {
                    'rule_id': rule.rule_id,
                    'name': rule.name,
                    'description': rule.description,
                    'from_version': rule.from_version,
                    'to_version': rule.to_version,
                    'rule_type': rule.rule_type,
                    'action': rule.action,
                    'source_path': rule.source_path,
                    'target_path': rule.target_path,
                    'transformation_script': rule.transformation_script,
                    'conditions': rule.conditions,
                    'is_breaking': rule.is_breaking,
                    'deprecation_date': rule.deprecation_date,
                    'removal_date': rule.removal_date
                }
                for rule in self.migration_rules
            ]
        }
        
        with open(migration_rules_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=True)
    
    def _save_migration_guide(self, guide: MigrationGuide, output_path: Path) -> None:
        """Save migration guide to markdown file."""
        content = f"""# {guide.title}

## Overview

{guide.overview}

**Estimated Effort**: {guide.estimated_effort}

## Breaking Changes

"""
        
        if guide.breaking_changes:
            for change in guide.breaking_changes:
                content += f"""### {change.title}

**Severity**: {change.severity.title()}
**Affects**: {', '.join(change.affects)}

{change.description}

**Migration Steps**:
"""
                for step in change.migration_steps:
                    content += f"- {step}\n"
                
                if change.workaround:
                    content += f"\n**Workaround**: {change.workaround}\n"
                
                content += "\n"
        else:
            content += "No breaking changes in this migration.\n\n"
        
        content += "## Deprecation Notices\n\n"
        
        if guide.deprecations:
            for deprecation in guide.deprecations:
                content += f"""### {deprecation.title}

{deprecation.description}

**Deprecated in**: {deprecation.deprecated_in}
"""
                if deprecation.removal_planned:
                    content += f"**Removal planned**: {deprecation.removal_planned}\n"
                if deprecation.replacement:
                    content += f"**Replacement**: {deprecation.replacement}\n"
                if deprecation.migration_guide:
                    content += f"**Migration Guide**: {deprecation.migration_guide}\n"
                
                content += "\n"
        else:
            content += "No deprecation notices for this migration.\n\n"
        
        content += "## Migration Steps\n\n"
        for i, step in enumerate(guide.migration_steps, 1):
            content += f"{i}. {step}\n"
        
        content += "\n## Testing Checklist\n\n"
        for item in guide.testing_checklist:
            content += f"- [ ] {item}\n"
        
        if guide.rollback_instructions:
            content += f"\n## Rollback Instructions\n\n{guide.rollback_instructions}\n"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _get_breaking_changes_for_range(self, from_version: str, to_version: str) -> List[BreakingChange]:
        """Get breaking changes applicable to version range."""
        applicable = []
        
        for change in self.breaking_changes:
            # Check if change was introduced in the target range
            if (self.version_manager.compare_versions(change.introduced_in, from_version) > 0 and
                self.version_manager.compare_versions(change.introduced_in, to_version) <= 0):
                applicable.append(change)
        
        return applicable
    
    def _get_deprecations_for_range(self, from_version: str, to_version: str) -> List[DeprecationNotice]:
        """Get deprecation notices applicable to version range."""
        applicable = []
        
        for deprecation in self.deprecations:
            # Check if deprecation was introduced before or in the range
            if self.version_manager.compare_versions(deprecation.deprecated_in, to_version) <= 0:
                # Check if it's still relevant (not removed)
                if (not deprecation.removal_planned or
                    self.version_manager.compare_versions(deprecation.removal_planned, to_version) > 0):
                    applicable.append(deprecation)
        
        return applicable
    
    def _generate_migration_steps(self, from_version: str, to_version: str) -> List[str]:
        """Generate migration steps for version range."""
        steps = [
            f"Review the changelog between {from_version} and {to_version}",
            "Backup your current documentation setup",
            "Test the migration in a staging environment first"
        ]
        
        # Add version-specific steps based on semantic versioning
        try:
            parsed_from = self.version_manager.parse_version(from_version)
            parsed_to = self.version_manager.parse_version(to_version)
            
            if parsed_from['major'] != parsed_to['major']:
                steps.extend([
                    "Review all breaking changes carefully",
                    "Update any custom configurations",
                    "Test all integrations and customizations"
                ])
            
            if parsed_from['minor'] != parsed_to['minor']:
                steps.append("Review new features and configuration options")
                
        except ValueError:
            # Handle non-semantic versions
            steps.append("Manually review version differences")
        
        steps.extend([
            "Deploy the new version",
            "Verify all functionality works as expected",
            "Update any documentation references to the new version"
        ])
        
        return steps
    
    def _generate_testing_checklist(self, from_version: str, to_version: str) -> List[str]:
        """Generate testing checklist for migration."""
        return [
            "Documentation builds successfully",
            "All internal links are working",
            "External links are accessible",
            "Navigation structure is correct",
            "Search functionality works",
            "Version switcher works (if applicable)",
            "Mobile/responsive layout is correct",
            "Performance is acceptable",
            "All images and assets load correctly",
            "PDF exports work (if applicable)"
        ]
    
    def _is_rule_applicable(self, rule: MigrationRule, from_version: str, to_version: str) -> bool:
        """Check if a migration rule is applicable to the version range."""
        try:
            # Check version range
            rule_applies = (
                self.version_manager.compare_versions(rule.from_version, from_version) <= 0 and
                self.version_manager.compare_versions(rule.to_version, to_version) >= 0
            )
            
            if not rule_applies:
                return False
            
            # Check conditions
            for condition in rule.conditions:
                if not self._evaluate_condition(condition, from_version, to_version):
                    return False
            
            return True
            
        except ValueError:
            # Handle version comparison errors
            return False
    
    def _evaluate_condition(self, condition: str, from_version: str, to_version: str) -> bool:
        """Evaluate a migration rule condition."""
        # Simple condition evaluation - could be extended
        if condition.startswith("file_exists:"):
            file_path = condition.split(":", 1)[1].strip()
            return (self.repo_path / file_path).exists()
        
        if condition.startswith("version_range:"):
            # Parse version range condition
            range_spec = condition.split(":", 1)[1].strip()
            # Implementation would parse and evaluate version range
            return True
        
        # Default to True for unknown conditions
        return True
    
    def _apply_migration_rule(self, rule: MigrationRule, dry_run: bool) -> Dict[str, Any]:
        """Apply a single migration rule."""
        result = {
            'rule_id': rule.rule_id,
            'action': rule.action,
            'modified_files': [],
            'dry_run': dry_run
        }
        
        source_path = self.repo_path / rule.source_path
        
        if rule.action == 'move':
            if rule.target_path:
                target_path = self.repo_path / rule.target_path
                if not dry_run and source_path.exists():
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source_path), str(target_path))
                result['modified_files'] = [rule.source_path, rule.target_path]
                
        elif rule.action == 'copy':
            if rule.target_path:
                target_path = self.repo_path / rule.target_path
                if not dry_run and source_path.exists():
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    if source_path.is_dir():
                        shutil.copytree(str(source_path), str(target_path), dirs_exist_ok=True)
                    else:
                        shutil.copy2(str(source_path), str(target_path))
                result['modified_files'] = [rule.target_path]
                
        elif rule.action == 'delete':
            if not dry_run and source_path.exists():
                if source_path.is_dir():
                    shutil.rmtree(str(source_path))
                else:
                    source_path.unlink()
            result['modified_files'] = [rule.source_path]
            
        elif rule.action == 'transform':
            if rule.transformation_script:
                # Execute transformation script
                # This would need proper script execution implementation
                result['modified_files'] = [rule.source_path]
        
        return result
