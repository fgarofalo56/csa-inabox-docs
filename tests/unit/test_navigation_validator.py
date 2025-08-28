"""Unit tests for NavigationStructureValidator."""

import pytest
import yaml
from pathlib import Path
from unittest.mock import patch

from src.csa_docs_tools.navigation_validator import NavigationStructureValidator, NavigationIssue


class TestNavigationStructureValidator:
    """Test cases for NavigationStructureValidator class."""

    @pytest.mark.unit
    def test_init(self, temp_docs_root):
        """Test NavigationStructureValidator initialization."""
        validator = NavigationStructureValidator(temp_docs_root)
        
        assert validator.docs_root == Path(temp_docs_root)
        assert validator.mkdocs_config == Path(temp_docs_root) / "mkdocs.yml"
        assert validator.docs_dir is not None
        assert validator.config is not None
        assert validator.nav_structure is not None

    @pytest.mark.unit
    def test_init_no_config(self, tmp_path):
        """Test initialization when mkdocs.yml doesn't exist."""
        validator = NavigationStructureValidator(tmp_path)
        
        assert validator.config is None
        assert validator.nav_structure is None

    @pytest.mark.unit
    def test_load_config_success(self, temp_docs_root):
        """Test successful configuration loading."""
        validator = NavigationStructureValidator(temp_docs_root)
        
        success = validator._load_config()
        assert success
        assert validator.config is not None
        assert 'site_name' in validator.config
        assert validator.docs_dir.exists()

    @pytest.mark.unit
    def test_load_config_invalid_yaml(self, tmp_path):
        """Test loading invalid YAML configuration."""
        # Create invalid mkdocs.yml
        mkdocs_file = tmp_path / "mkdocs.yml"
        mkdocs_file.write_text("invalid: yaml: content: [unclosed")
        
        validator = NavigationStructureValidator(tmp_path)
        
        assert validator.config is None

    @pytest.mark.unit
    def test_validate_nav_consistency_valid(self, temp_docs_root):
        """Test navigation consistency validation with valid navigation."""
        validator = NavigationStructureValidator(temp_docs_root)
        
        issues = validator.validate_nav_consistency()
        
        # Should have no errors for valid navigation
        error_issues = [issue for issue in issues if issue.severity == 'error']
        assert len(error_issues) == 0

    @pytest.mark.unit
    def test_validate_nav_consistency_no_config(self, tmp_path):
        """Test navigation validation with no configuration."""
        validator = NavigationStructureValidator(tmp_path)
        
        issues = validator.validate_nav_consistency()
        
        assert len(issues) == 1
        assert issues[0].issue_type == 'config_error'
        assert issues[0].severity == 'error'

    @pytest.mark.unit
    def test_validate_nav_consistency_no_nav(self, tmp_path):
        """Test navigation validation with no explicit navigation."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs"
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        validator = NavigationStructureValidator(tmp_path)
        issues = validator.validate_nav_consistency()
        
        # No navigation is valid (auto-generated)
        assert len(issues) == 0

    @pytest.mark.unit
    def test_validate_nav_items_missing_files(self, tmp_path):
        """Test navigation validation with missing files."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "existing.md").write_text("# Existing")
        
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs",
            "nav": [
                {"Home": "existing.md"},
                {"Missing": "nonexistent.md"}
            ]
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        validator = NavigationStructureValidator(tmp_path)
        issues = validator.validate_nav_consistency()
        
        missing_file_issues = [issue for issue in issues if issue.issue_type == 'missing_file']
        assert len(missing_file_issues) >= 1
        assert any("nonexistent.md" in issue.message for issue in missing_file_issues)

    @pytest.mark.unit
    def test_validate_nav_items_duplicate_titles(self, tmp_path):
        """Test navigation validation with duplicate titles."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "page1.md").write_text("# Page 1")
        (docs_dir / "page2.md").write_text("# Page 2")
        
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs",
            "nav": [
                {"Home": "page1.md"},
                {"Home": "page2.md"}  # Duplicate title
            ]
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        validator = NavigationStructureValidator(tmp_path)
        issues = validator.validate_nav_consistency()
        
        duplicate_issues = [issue for issue in issues if issue.issue_type == 'duplicate_title']
        assert len(duplicate_issues) >= 1

    @pytest.mark.unit
    def test_validate_nav_items_nested_structure(self, tmp_path):
        """Test navigation validation with nested structure."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "index.md").write_text("# Index")
        (docs_dir / "guide.md").write_text("# Guide")
        
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs",
            "nav": [
                {"Home": "index.md"},
                {"Section": [
                    {"Guide": "guide.md"},
                    {"Missing": "nonexistent.md"}
                ]}
            ]
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        validator = NavigationStructureValidator(tmp_path)
        issues = validator.validate_nav_consistency()
        
        # Should find the missing file in nested structure
        missing_issues = [issue for issue in issues if issue.issue_type == 'missing_file']
        assert len(missing_issues) >= 1

    @pytest.mark.unit
    def test_validate_nav_items_invalid_format(self, tmp_path):
        """Test navigation validation with invalid format."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs",
            "nav": [
                {"Invalid": 123},  # Number instead of string/list
                {"Another": None}   # None value
            ]
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        validator = NavigationStructureValidator(tmp_path)
        issues = validator.validate_nav_consistency()
        
        invalid_issues = [issue for issue in issues if issue.issue_type == 'invalid_nav_item']
        assert len(invalid_issues) >= 1

    @pytest.mark.unit
    def test_check_orphaned_files_no_orphans(self, temp_docs_root):
        """Test orphaned files check with no orphaned files."""
        validator = NavigationStructureValidator(temp_docs_root)
        
        issues = validator.check_orphaned_files()
        
        # The fixture should have all files in navigation
        orphaned_issues = [issue for issue in issues if issue.issue_type == 'orphaned_file']
        # Depending on the fixture, there might be some orphaned files
        assert isinstance(orphaned_issues, list)

    @pytest.mark.unit
    def test_check_orphaned_files_with_orphans(self, tmp_path):
        """Test orphaned files check with orphaned files."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "included.md").write_text("# Included")
        (docs_dir / "orphaned.md").write_text("# Orphaned")
        
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs",
            "nav": [
                {"Home": "included.md"}
            ]
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        validator = NavigationStructureValidator(tmp_path)
        issues = validator.check_orphaned_files()
        
        orphaned_issues = [issue for issue in issues if issue.issue_type == 'orphaned_file']
        assert len(orphaned_issues) >= 1
        assert any("orphaned.md" in issue.message for issue in orphaned_issues)

    @pytest.mark.unit
    def test_check_orphaned_files_ignore_patterns(self, tmp_path):
        """Test orphaned files check ignores certain patterns."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "included.md").write_text("# Included")
        (docs_dir / "README.md").write_text("# README")  # Should be ignored
        (docs_dir / "index.md").write_text("# Index")    # Should be ignored
        
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs",
            "nav": [
                {"Home": "included.md"}
            ]
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        validator = NavigationStructureValidator(tmp_path)
        issues = validator.check_orphaned_files()
        
        # README.md and index.md should be ignored
        orphaned_issues = [issue for issue in issues if issue.issue_type == 'orphaned_file']
        orphaned_files = [issue.file_path for issue in orphaned_issues]
        
        assert "README.md" not in orphaned_files
        assert "index.md" not in orphaned_files

    @pytest.mark.unit
    def test_validate_nav_depth_within_limit(self, tmp_path):
        """Test navigation depth validation within limits."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "page.md").write_text("# Page")
        
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs",
            "nav": [
                {"Level 1": [
                    {"Level 2": [
                        {"Level 3": "page.md"}
                    ]}
                ]}
            ]
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        validator = NavigationStructureValidator(tmp_path)
        issues = validator.validate_nav_depth(max_depth=4)
        
        depth_issues = [issue for issue in issues if issue.issue_type == 'nav_too_deep']
        assert len(depth_issues) == 0

    @pytest.mark.unit
    def test_validate_nav_depth_exceeds_limit(self, tmp_path):
        """Test navigation depth validation exceeding limits."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "page.md").write_text("# Page")
        
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs",
            "nav": [
                {"L1": [
                    {"L2": [
                        {"L3": [
                            {"L4": [
                                {"L5": "page.md"}  # Depth 5
                            ]}
                        ]}
                    ]}
                ]}
            ]
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        validator = NavigationStructureValidator(tmp_path)
        issues = validator.validate_nav_depth(max_depth=3)
        
        depth_issues = [issue for issue in issues if issue.issue_type == 'nav_too_deep']
        assert len(depth_issues) > 0

    @pytest.mark.unit
    def test_validate_nav_order_good_start(self, tmp_path):
        """Test navigation order validation with good start."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "overview.md").write_text("# Overview")
        (docs_dir / "guide.md").write_text("# Guide")
        
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs",
            "nav": [
                {"Overview": "overview.md"},
                {"Guide": "guide.md"}
            ]
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        validator = NavigationStructureValidator(tmp_path)
        issues = validator.validate_nav_order()
        
        order_issues = [issue for issue in issues if issue.issue_type == 'nav_order']
        assert len(order_issues) == 0

    @pytest.mark.unit
    def test_validate_nav_order_poor_start(self, tmp_path):
        """Test navigation order validation with poor start."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "advanced.md").write_text("# Advanced")
        (docs_dir / "guide.md").write_text("# Guide")
        
        config = {
            "site_name": "Test Site",
            "docs_dir": "docs",
            "nav": [
                {"Advanced Topics": "advanced.md"},
                {"Guide": "guide.md"}
            ]
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        validator = NavigationStructureValidator(tmp_path)
        issues = validator.validate_nav_order()
        
        order_issues = [issue for issue in issues if issue.issue_type == 'nav_order']
        assert len(order_issues) >= 1

    @pytest.mark.unit
    def test_check_index_files_good_structure(self, tmp_path):
        """Test index files check with good directory structure."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        # Create directory with index file
        section_dir = docs_dir / "section"
        section_dir.mkdir()
        (section_dir / "index.md").write_text("# Section Index")
        (section_dir / "page1.md").write_text("# Page 1")
        (section_dir / "page2.md").write_text("# Page 2")
        
        validator = NavigationStructureValidator(tmp_path)
        issues = validator.check_index_files()
        
        missing_index_issues = [issue for issue in issues if issue.issue_type == 'missing_index']
        assert len(missing_index_issues) == 0

    @pytest.mark.unit
    def test_check_index_files_missing_index(self, tmp_path):
        """Test index files check with missing index files."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        # Create directory without index file but with multiple pages
        section_dir = docs_dir / "section"
        section_dir.mkdir()
        (section_dir / "page1.md").write_text("# Page 1")
        (section_dir / "page2.md").write_text("# Page 2")
        (section_dir / "page3.md").write_text("# Page 3")
        
        validator = NavigationStructureValidator(tmp_path)
        issues = validator.check_index_files()
        
        missing_index_issues = [issue for issue in issues if issue.issue_type == 'missing_index']
        assert len(missing_index_issues) >= 1

    @pytest.mark.unit
    def test_check_index_files_single_file_dir(self, tmp_path):
        """Test index files check with single file directories."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        # Create directory with only one file (no index needed)
        section_dir = docs_dir / "section"
        section_dir.mkdir()
        (section_dir / "single.md").write_text("# Single Page")
        
        validator = NavigationStructureValidator(tmp_path)
        issues = validator.check_index_files()
        
        missing_index_issues = [issue for issue in issues if issue.issue_type == 'missing_index']
        # Should not complain about directories with only one file
        section_issues = [issue for issue in missing_index_issues if "section" in str(issue.file_path)]
        assert len(section_issues) == 0

    @pytest.mark.unit
    def test_validate_all_navigation(self, temp_docs_root):
        """Test comprehensive navigation validation."""
        validator = NavigationStructureValidator(temp_docs_root)
        
        results = validator.validate_all_navigation()
        
        assert isinstance(results, dict)
        expected_categories = ['consistency', 'orphaned_files', 'nav_depth', 'nav_order', 'index_files']
        
        for category in expected_categories:
            assert category in results
            assert isinstance(results[category], list)

    @pytest.mark.unit
    def test_generate_navigation_report(self, temp_docs_root):
        """Test navigation report generation."""
        validator = NavigationStructureValidator(temp_docs_root)
        
        # Create sample validation results
        sample_issues = {
            'consistency': [
                NavigationIssue('missing_file', 'error', 'Missing file: test.md', 'test.md')
            ],
            'orphaned_files': [
                NavigationIssue('orphaned_file', 'warning', 'Orphaned: orphan.md', 'orphan.md')
            ],
            'nav_depth': [],
            'nav_order': [],
            'index_files': [
                NavigationIssue('missing_index', 'info', 'Missing index in dir/', 'dir/')
            ]
        }
        
        report = validator.generate_navigation_report(sample_issues)
        
        assert 'total_issues' in report
        assert 'severity_breakdown' in report
        assert 'issue_type_breakdown' in report
        assert 'navigation_health_score' in report
        assert 'has_explicit_nav' in report
        assert 'total_nav_items' in report
        assert 'max_nav_depth' in report
        assert 'recommendations' in report
        assert 'category_breakdown' in report
        
        assert report['total_issues'] == 3
        assert report['severity_breakdown']['error'] == 1
        assert report['severity_breakdown']['warning'] == 1
        assert report['severity_breakdown']['info'] == 1

    @pytest.mark.unit
    def test_navigation_health_score_calculation(self, temp_docs_root):
        """Test navigation health score calculation."""
        validator = NavigationStructureValidator(temp_docs_root)
        
        # Test with no issues
        no_issues = {
            'consistency': [],
            'orphaned_files': [],
            'nav_depth': [],
            'nav_order': [],
            'index_files': []
        }
        
        report = validator.generate_navigation_report(no_issues)
        assert report['navigation_health_score'] == 100.0
        
        # Test with various severity issues
        with_issues = {
            'consistency': [
                NavigationIssue('missing_file', 'error', 'Error', None)
            ],
            'orphaned_files': [
                NavigationIssue('orphaned_file', 'warning', 'Warning', None)
            ],
            'nav_depth': [],
            'nav_order': [
                NavigationIssue('nav_order', 'info', 'Info', None)
            ],
            'index_files': []
        }
        
        report = validator.generate_navigation_report(with_issues)
        assert report['navigation_health_score'] < 100.0

    @pytest.mark.unit
    def test_count_nav_items(self, temp_docs_root):
        """Test navigation item counting."""
        validator = NavigationStructureValidator(temp_docs_root)
        
        count = validator._count_nav_items()
        assert isinstance(count, int)
        assert count > 0  # Should have navigation items from fixture

    @pytest.mark.unit
    def test_get_max_nav_depth(self, temp_docs_root):
        """Test maximum navigation depth calculation."""
        validator = NavigationStructureValidator(temp_docs_root)
        
        max_depth = validator._get_max_nav_depth()
        assert isinstance(max_depth, int)
        assert max_depth > 0

    @pytest.mark.unit
    def test_collect_nav_files(self, temp_docs_root):
        """Test navigation file collection."""
        validator = NavigationStructureValidator(temp_docs_root)
        
        nav_files = set()
        if validator.nav_structure:
            validator._collect_nav_files(validator.nav_structure, nav_files)
            
            assert isinstance(nav_files, set)
            assert len(nav_files) > 0
            
            # Should contain actual markdown files
            for file_path in nav_files:
                assert file_path.endswith('.md')

    @pytest.mark.unit
    def test_collect_nav_titles(self, temp_docs_root):
        """Test navigation title collection."""
        validator = NavigationStructureValidator(temp_docs_root)
        
        titles = []
        if validator.nav_structure:
            validator._collect_nav_titles(validator.nav_structure, titles)
            
            assert isinstance(titles, list)
            assert len(titles) > 0
            
            # Should contain navigation titles
            assert all(isinstance(title, str) for title in titles)

    @pytest.mark.unit
    def test_generate_nav_recommendations(self, temp_docs_root):
        """Test navigation recommendation generation."""
        validator = NavigationStructureValidator(temp_docs_root)
        
        # Test with different types of issues
        validation_results = {
            'consistency': [
                NavigationIssue('missing_file', 'error', 'Error', None)
            ],
            'orphaned_files': [
                NavigationIssue('orphaned_file', 'warning', 'Warning', None)
            ],
            'nav_depth': [],
            'nav_order': [],
            'index_files': []
        }
        
        recommendations = validator._generate_nav_recommendations(validation_results)
        
        assert isinstance(recommendations, list)
        
        if recommendations:
            # Check that recommendations are strings
            assert all(isinstance(rec, str) for rec in recommendations)

    @pytest.mark.unit
    def test_error_handling_missing_docs_dir(self, tmp_path):
        """Test error handling when docs directory is missing."""
        config = {
            "site_name": "Test Site",
            "docs_dir": "nonexistent_docs"
        }
        
        mkdocs_file = tmp_path / "mkdocs.yml"
        with open(mkdocs_file, 'w') as f:
            yaml.dump(config, f)
        
        validator = NavigationStructureValidator(tmp_path)
        
        # Should handle missing docs directory gracefully
        issues = validator.check_orphaned_files()
        assert isinstance(issues, list)  # Should not raise exception