"""Navigation structure validation utilities."""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class NavigationIssue:
    """Represents a navigation structure issue."""
    issue_type: str
    severity: str
    message: str
    file_path: Optional[str] = None
    nav_item: Optional[str] = None


class NavigationStructureValidator:
    """Validate MkDocs navigation structure and consistency."""
    
    def __init__(self, docs_root: Path):
        """Initialize navigation structure validator.
        
        Args:
            docs_root: Path to documentation root directory
        """
        self.docs_root = Path(docs_root)
        self.mkdocs_config = self.docs_root / "mkdocs.yml"
        self.docs_dir = None
        self.nav_structure = None
        self.config = None
        
        self._load_config()
    
    def _load_config(self) -> bool:
        """Load MkDocs configuration.
        
        Returns:
            True if config loaded successfully
        """
        if not self.mkdocs_config.exists():
            logger.error(f"MkDocs config not found: {self.mkdocs_config}")
            return False
            
        try:
            with open(self.mkdocs_config, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
                
            self.docs_dir = self.docs_root / self.config.get('docs_dir', 'docs')
            self.nav_structure = self.config.get('nav', [])
            return True
            
        except Exception as e:
            logger.error(f"Error loading MkDocs config: {e}")
            return False
    
    def validate_nav_consistency(self) -> List[NavigationIssue]:
        """Validate navigation structure consistency.
        
        Returns:
            List of NavigationIssue objects
        """
        issues = []
        
        if not self.config:
            issues.append(NavigationIssue(
                issue_type='config_error',
                severity='error',
                message='Could not load MkDocs configuration'
            ))
            return issues
        
        if not self.nav_structure:
            # No navigation defined - auto-generated nav will be used
            return issues
        
        # Validate navigation structure
        issues.extend(self._validate_nav_items(self.nav_structure))
        
        return issues
    
    def _validate_nav_items(self, nav_items: List, path_prefix: str = "") -> List[NavigationIssue]:
        """Recursively validate navigation items.
        
        Args:
            nav_items: List of navigation items
            path_prefix: Current navigation path prefix
            
        Returns:
            List of NavigationIssue objects
        """
        issues = []
        seen_titles = set()
        
        for item in nav_items:
            if isinstance(item, str):
                # Simple file reference
                file_path = self.docs_dir / item
                if not file_path.exists():
                    issues.append(NavigationIssue(
                        issue_type='missing_file',
                        severity='error',
                        message=f'Navigation references missing file: {item}',
                        file_path=item
                    ))
                    
            elif isinstance(item, dict):
                for title, content in item.items():
                    current_path = f"{path_prefix}/{title}" if path_prefix else title
                    
                    # Check for duplicate titles at same level
                    if title in seen_titles:
                        issues.append(NavigationIssue(
                            issue_type='duplicate_title',
                            severity='warning',
                            message=f'Duplicate navigation title: "{title}"',
                            nav_item=current_path
                        ))
                    seen_titles.add(title)
                    
                    if isinstance(content, str):
                        # Single file
                        file_path = self.docs_dir / content
                        if not file_path.exists():
                            issues.append(NavigationIssue(
                                issue_type='missing_file',
                                severity='error',
                                message=f'Navigation references missing file: {content}',
                                file_path=content,
                                nav_item=current_path
                            ))
                    elif isinstance(content, list):
                        # Nested navigation
                        issues.extend(self._validate_nav_items(content, current_path))
                    else:
                        issues.append(NavigationIssue(
                            issue_type='invalid_nav_item',
                            severity='error',
                            message=f'Invalid navigation item type for "{title}": {type(content)}',
                            nav_item=current_path
                        ))
            else:
                issues.append(NavigationIssue(
                    issue_type='invalid_nav_format',
                    severity='error',
                    message=f'Invalid navigation format: {type(item)}'
                ))
        
        return issues
    
    def check_orphaned_files(self) -> List[NavigationIssue]:
        """Find markdown files not included in navigation.
        
        Returns:
            List of NavigationIssue objects for orphaned files
        """
        issues = []
        
        if not self.docs_dir or not self.docs_dir.exists():
            return issues
        
        # Get all markdown files
        all_md_files = set()
        for file_path in self.docs_dir.glob("**/*.md"):
            relative_path = file_path.relative_to(self.docs_dir)
            all_md_files.add(str(relative_path).replace('\\', '/'))
        
        # Get files referenced in navigation
        nav_files = set()
        if self.nav_structure:
            self._collect_nav_files(self.nav_structure, nav_files)
        else:
            # No explicit nav - all files are considered included
            nav_files = all_md_files
        
        # Find orphaned files
        orphaned_files = all_md_files - nav_files
        
        # Filter out index files and README files that are typically auto-included
        ignored_patterns = {'index.md', 'README.md'}
        orphaned_files = {f for f in orphaned_files if Path(f).name not in ignored_patterns}
        
        for orphaned_file in sorted(orphaned_files):
            issues.append(NavigationIssue(
                issue_type='orphaned_file',
                severity='warning',
                message=f'File not included in navigation: {orphaned_file}',
                file_path=orphaned_file
            ))
        
        return issues
    
    def _collect_nav_files(self, nav_items: List, nav_files: Set[str]):
        """Recursively collect all files referenced in navigation.
        
        Args:
            nav_items: List of navigation items
            nav_files: Set to collect referenced files
        """
        for item in nav_items:
            if isinstance(item, str):
                nav_files.add(item)
            elif isinstance(item, dict):
                for title, content in item.items():
                    if isinstance(content, str):
                        nav_files.add(content)
                    elif isinstance(content, list):
                        self._collect_nav_files(content, nav_files)
    
    def validate_nav_depth(self, max_depth: int = 4) -> List[NavigationIssue]:
        """Validate navigation depth doesn't exceed recommended maximum.
        
        Args:
            max_depth: Maximum recommended navigation depth
            
        Returns:
            List of NavigationIssue objects
        """
        issues = []
        
        if not self.nav_structure:
            return issues
        
        def check_depth(nav_items: List, current_depth: int = 1, path: str = ""):
            for item in nav_items:
                if isinstance(item, dict):
                    for title, content in item.items():
                        current_path = f"{path}/{title}" if path else title
                        
                        if current_depth > max_depth:
                            issues.append(NavigationIssue(
                                issue_type='nav_too_deep',
                                severity='warning',
                                message=f'Navigation depth {current_depth} exceeds recommended maximum of {max_depth}',
                                nav_item=current_path
                            ))
                        
                        if isinstance(content, list):
                            check_depth(content, current_depth + 1, current_path)
        
        check_depth(self.nav_structure)
        return issues
    
    def validate_nav_order(self) -> List[NavigationIssue]:
        """Validate logical navigation order and structure.
        
        Returns:
            List of NavigationIssue objects
        """
        issues = []
        
        if not self.nav_structure:
            return issues
        
        # Check for common ordering patterns
        nav_titles = []
        self._collect_nav_titles(self.nav_structure, nav_titles)
        
        # Check for introduction/overview at the beginning
        if nav_titles:
            first_title = nav_titles[0].lower()
            if not any(keyword in first_title for keyword in ['intro', 'overview', 'getting', 'start', 'index']):
                issues.append(NavigationIssue(
                    issue_type='nav_order',
                    severity='info',
                    message='Consider starting navigation with an introduction or overview section',
                    nav_item=nav_titles[0]
                ))
        
        return issues
    
    def _collect_nav_titles(self, nav_items: List, titles: List[str]):
        """Recursively collect navigation titles.
        
        Args:
            nav_items: List of navigation items
            titles: List to collect titles
        """
        for item in nav_items:
            if isinstance(item, dict):
                for title, content in item.items():
                    titles.append(title)
                    if isinstance(content, list):
                        self._collect_nav_titles(content, titles)
    
    def check_index_files(self) -> List[NavigationIssue]:
        """Check for proper index files in directories.
        
        Returns:
            List of NavigationIssue objects
        """
        issues = []
        
        if not self.docs_dir or not self.docs_dir.exists():
            return issues
        
        # Find directories with markdown files but no index
        for dir_path in self.docs_dir.rglob("*"):
            if not dir_path.is_dir():
                continue
                
            # Skip root docs directory
            if dir_path == self.docs_dir:
                continue
            
            # Check if directory has markdown files
            md_files = list(dir_path.glob("*.md"))
            if not md_files:
                continue
            
            # Check for index file
            index_files = [f for f in md_files if f.name.lower() in ['index.md', 'readme.md']]
            
            if not index_files and len(md_files) > 1:
                relative_dir = dir_path.relative_to(self.docs_dir)
                issues.append(NavigationIssue(
                    issue_type='missing_index',
                    severity='info',
                    message=f'Directory with multiple files lacks index file: {relative_dir}',
                    file_path=str(relative_dir)
                ))
        
        return issues
    
    def validate_all_navigation(self) -> Dict[str, List[NavigationIssue]]:
        """Run all navigation validation checks.
        
        Returns:
            Dictionary with categorized navigation issues
        """
        validation_results = {
            'consistency': self.validate_nav_consistency(),
            'orphaned_files': self.check_orphaned_files(),
            'nav_depth': self.validate_nav_depth(),
            'nav_order': self.validate_nav_order(),
            'index_files': self.check_index_files()
        }
        
        return validation_results
    
    def generate_navigation_report(self, validation_results: Dict[str, List[NavigationIssue]]) -> Dict:
        """Generate comprehensive navigation validation report.
        
        Args:
            validation_results: Dictionary of validation results by category
            
        Returns:
            Navigation report dictionary
        """
        total_issues = sum(len(issues) for issues in validation_results.values())
        
        # Count by severity
        severity_counts = {'error': 0, 'warning': 0, 'info': 0}
        issue_type_counts = {}
        
        for category, issues in validation_results.items():
            for issue in issues:
                severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
                issue_type_counts[issue.issue_type] = issue_type_counts.get(issue.issue_type, 0) + 1
        
        # Calculate navigation health score
        error_weight = 3
        warning_weight = 2
        info_weight = 1
        
        weighted_issues = (
            severity_counts['error'] * error_weight +
            severity_counts['warning'] * warning_weight +
            severity_counts['info'] * info_weight
        )
        
        nav_health_score = max(0, 100 - weighted_issues * 5)
        
        return {
            'total_issues': total_issues,
            'severity_breakdown': severity_counts,
            'issue_type_breakdown': issue_type_counts,
            'navigation_health_score': round(nav_health_score, 2),
            'has_explicit_nav': bool(self.nav_structure),
            'total_nav_items': self._count_nav_items(),
            'max_nav_depth': self._get_max_nav_depth(),
            'recommendations': self._generate_nav_recommendations(validation_results),
            'category_breakdown': {
                category: len(issues) for category, issues in validation_results.items()
            }
        }
    
    def _count_nav_items(self) -> int:
        """Count total navigation items."""
        if not self.nav_structure:
            return 0
            
        def count_items(nav_items: List) -> int:
            count = 0
            for item in nav_items:
                count += 1
                if isinstance(item, dict):
                    for title, content in item.items():
                        if isinstance(content, list):
                            count += count_items(content)
            return count
        
        return count_items(self.nav_structure)
    
    def _get_max_nav_depth(self) -> int:
        """Get maximum navigation depth."""
        if not self.nav_structure:
            return 0
            
        def get_depth(nav_items: List, current_depth: int = 1) -> int:
            max_depth = current_depth
            for item in nav_items:
                if isinstance(item, dict):
                    for title, content in item.items():
                        if isinstance(content, list):
                            depth = get_depth(content, current_depth + 1)
                            max_depth = max(max_depth, depth)
            return max_depth
        
        return get_depth(self.nav_structure)
    
    def _generate_nav_recommendations(self, validation_results: Dict) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        error_count = sum(len(issues) for issues in validation_results.values() if any(i.severity == 'error' for i in issues))
        warning_count = sum(len(issues) for issues in validation_results.values() if any(i.severity == 'warning' for i in issues))
        
        if error_count > 0:
            recommendations.append("Fix navigation errors to ensure proper site functionality")
        
        if len(validation_results['orphaned_files']) > 0:
            recommendations.append("Review orphaned files and consider adding them to navigation or removing if unnecessary")
        
        if self._get_max_nav_depth() > 4:
            recommendations.append("Consider flattening deep navigation hierarchies for better user experience")
        
        if not self.nav_structure:
            recommendations.append("Consider defining explicit navigation for better content organization")
        
        return recommendations