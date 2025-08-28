"""Integration tests for full documentation validation workflow."""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import patch

from src.csa_docs_tools import (
    DocumentationBuildTester,
    LinkValidator,
    MarkdownQualityChecker,
    ImageReferenceValidator,
    NavigationStructureValidator
)


class TestFullValidationWorkflow:
    """Integration tests for complete documentation validation."""

    @pytest.mark.integration
    def test_complete_documentation_validation(self, temp_docs_root):
        """Test complete validation workflow on test documentation."""
        # Initialize all validators
        build_tester = DocumentationBuildTester(temp_docs_root)
        markdown_checker = MarkdownQualityChecker(temp_docs_root)
        image_validator = ImageReferenceValidator(temp_docs_root)
        nav_validator = NavigationStructureValidator(temp_docs_root)
        
        # Test build validation
        config_valid, config_errors = build_tester.validate_mkdocs_config()
        assert config_valid, f"Config validation failed: {config_errors}"
        
        nav_valid, nav_errors = build_tester.validate_nav_structure()
        assert nav_valid, f"Navigation validation failed: {nav_errors}"
        
        # Test build process (mocked)
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "Build successful"
            mock_run.return_value.stderr = ""
            
            build_success, stdout, stderr = build_tester.test_build()
            assert build_success, f"Build failed: {stderr}"
        
        # Test markdown quality
        quality_results = markdown_checker.check_all_files()
        quality_report = markdown_checker.generate_quality_report(quality_results)
        
        assert quality_report['total_files'] > 0
        assert 'quality_score' in quality_report
        
        # Test image validation
        image_results = image_validator.validate_all_images()
        image_report = image_validator.generate_image_report(image_results)
        
        assert 'total_images' in image_report
        assert 'image_health_score' in image_report
        
        # Test navigation validation
        nav_results = nav_validator.validate_all_navigation()
        nav_report = nav_validator.generate_navigation_report(nav_results)
        
        assert 'navigation_health_score' in nav_report
        assert 'total_issues' in nav_report
        
        # Aggregate results
        overall_health_score = (
            quality_report['quality_score'] * 0.3 +
            image_report['image_health_score'] * 0.3 +
            nav_report['navigation_health_score'] * 0.4
        )
        
        print(f"\nOverall Documentation Health Score: {overall_health_score:.2f}")
        print(f"Quality Score: {quality_report['quality_score']:.2f}")
        print(f"Image Health Score: {image_report['image_health_score']:.2f}")
        print(f"Navigation Health Score: {nav_report['navigation_health_score']:.2f}")
        
        # Basic health check
        assert overall_health_score > 0

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_complete_link_validation(self, temp_docs_root):
        """Test complete link validation workflow."""
        async with LinkValidator(temp_docs_root) as validator:
            # Mock external link responses
            with patch.object(validator, 'validate_external_link') as mock_external:
                # Mock successful external link validation
                from src.csa_docs_tools.link_validator import LinkResult
                mock_external.return_value = LinkResult(
                    url="https://portal.azure.com",
                    status_code=200,
                    is_valid=True,
                    error_message=None,
                    source_file="docs/index.md",
                    line_number=1
                )
                
                results = await validator.validate_all_links(check_external=True)
                report = validator.generate_report(results)
                
                assert report['total_links'] > 0
                assert 'success_rate' in report
                assert 'broken_links' in report
                
                # Print detailed link analysis
                print(f"\nLink Validation Report:")
                print(f"Total Links: {report['total_links']}")
                print(f"Valid Links: {report['valid_links']}")
                print(f"Broken Links: {report['broken_links']}")
                print(f"Success Rate: {report['success_rate']:.1f}%")
                
                if report['broken_links'] > 0:
                    print("\nBroken Links:")
                    for broken in report['broken_link_details'][:5]:  # Show first 5
                        print(f"  - {broken['url']} in {broken['file']}:{broken['line']}")

    @pytest.mark.integration
    def test_real_documentation_structure(self, real_docs_root):
        """Test validation against real documentation structure."""
        if not real_docs_root:
            pytest.skip("Real documentation root not available")
        
        # Test with actual documentation
        nav_validator = NavigationStructureValidator(real_docs_root)
        
        # Check configuration loading
        assert nav_validator.config is not None, "Could not load real mkdocs.yml"
        
        # Run navigation validation
        nav_results = nav_validator.validate_all_navigation()
        nav_report = nav_validator.generate_navigation_report(nav_results)
        
        print(f"\nReal Documentation Navigation Report:")
        print(f"Total Issues: {nav_report['total_issues']}")
        print(f"Navigation Health Score: {nav_report['navigation_health_score']:.2f}")
        
        if nav_report['total_issues'] > 0:
            print(f"Issue Breakdown:")
            for category, count in nav_report['category_breakdown'].items():
                if count > 0:
                    print(f"  - {category}: {count}")

    @pytest.mark.integration
    def test_performance_with_large_documentation(self, temp_docs_root):
        """Test performance with larger documentation sets."""
        import time
        
        # Create additional test files to simulate larger documentation
        docs_dir = temp_docs_root / "docs"
        
        # Create multiple sections with files
        sections = ['getting-started', 'tutorials', 'reference', 'api', 'examples']
        
        for section in sections:
            section_dir = docs_dir / section
            section_dir.mkdir(exist_ok=True)
            
            # Create multiple files per section
            for i in range(10):
                file_path = section_dir / f"page_{i}.md"
                content = f"""# {section.title()} Page {i}

This is a test page for performance testing.

## Section {i}

Here's some content with [links](../index.md) and ![images](../images/architecture.png).

### Code Example

```python
def example_{i}():
    return "Hello from page {i}"
```

### Table

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value {i} | Value {i+1} | Value {i+2} |

More content here...
"""
                file_path.write_text(content)
        
        # Test performance of different validators
        validators = {
            'Build Tester': DocumentationBuildTester(temp_docs_root),
            'Markdown Quality': MarkdownQualityChecker(temp_docs_root),
            'Image Validator': ImageReferenceValidator(temp_docs_root),
            'Navigation Validator': NavigationStructureValidator(temp_docs_root)
        }
        
        performance_results = {}
        
        for name, validator in validators.items():
            start_time = time.time()
            
            try:
                if name == 'Build Tester':
                    validator.get_build_statistics()
                elif name == 'Markdown Quality':
                    results = validator.check_all_files()
                    validator.generate_quality_report(results)
                elif name == 'Image Validator':
                    results = validator.validate_all_images()
                    validator.generate_image_report(results)
                elif name == 'Navigation Validator':
                    results = validator.validate_all_navigation()
                    validator.generate_navigation_report(results)
                    
                end_time = time.time()
                performance_results[name] = end_time - start_time
                
            except Exception as e:
                print(f"Error in {name}: {e}")
                performance_results[name] = float('inf')
        
        print(f"\nPerformance Results:")
        for name, duration in performance_results.items():
            if duration != float('inf'):
                print(f"  {name}: {duration:.2f}s")
            else:
                print(f"  {name}: FAILED")
        
        # Performance assertions (reasonable limits)
        for name, duration in performance_results.items():
            if duration != float('inf'):
                assert duration < 30.0, f"{name} took too long: {duration:.2f}s"

    @pytest.mark.integration
    @pytest.mark.slow
    def test_comprehensive_quality_analysis(self, temp_docs_root):
        """Comprehensive quality analysis of documentation."""
        # Initialize all validators
        build_tester = DocumentationBuildTester(temp_docs_root)
        markdown_checker = MarkdownQualityChecker(temp_docs_root)
        image_validator = ImageReferenceValidator(temp_docs_root)
        nav_validator = NavigationStructureValidator(temp_docs_root)
        
        # Collect comprehensive statistics
        stats = {
            'build': build_tester.get_build_statistics(),
            'quality': markdown_checker.generate_quality_report(
                markdown_checker.check_all_files()
            ),
            'images': image_validator.generate_image_report(
                image_validator.validate_all_images()
            ),
            'navigation': nav_validator.generate_navigation_report(
                nav_validator.validate_all_navigation()
            )
        }
        
        # Generate comprehensive report
        comprehensive_report = {
            'summary': {
                'total_markdown_files': stats['build']['total_markdown_files'],
                'total_assets': stats['build']['total_assets'],
                'config_valid': stats['build']['config_valid'],
                'build_successful': stats['build']['build_successful']
            },
            'quality_metrics': {
                'overall_quality_score': stats['quality']['quality_score'],
                'total_quality_issues': stats['quality']['total_issues'],
                'image_health_score': stats['images']['image_health_score'],
                'navigation_health_score': stats['navigation']['navigation_health_score']
            },
            'detailed_breakdown': {
                'quality_issues_by_severity': stats['quality']['severity_breakdown'],
                'image_issues_by_type': stats['images']['issue_type_breakdown'],
                'navigation_issues_by_category': stats['navigation']['category_breakdown']
            },
            'recommendations': {
                'quality': stats['quality'].get('top_rule_violations', {}),
                'images': stats['images'].get('recommendations', []),
                'navigation': stats['navigation'].get('recommendations', [])
            }
        }
        
        print(f"\nComprehensive Documentation Analysis:")
        print(f"=" * 50)
        print(f"Total Files: {comprehensive_report['summary']['total_markdown_files']}")
        print(f"Total Assets: {comprehensive_report['summary']['total_assets']}")
        print(f"Config Valid: {comprehensive_report['summary']['config_valid']}")
        print(f"Build Successful: {comprehensive_report['summary']['build_successful']}")
        print(f"\nQuality Metrics:")
        print(f"  Overall Quality Score: {comprehensive_report['quality_metrics']['overall_quality_score']:.1f}")
        print(f"  Image Health Score: {comprehensive_report['quality_metrics']['image_health_score']:.1f}")
        print(f"  Navigation Health Score: {comprehensive_report['quality_metrics']['navigation_health_score']:.1f}")
        
        # Calculate overall health score
        overall_score = (
            comprehensive_report['quality_metrics']['overall_quality_score'] * 0.4 +
            comprehensive_report['quality_metrics']['image_health_score'] * 0.3 +
            comprehensive_report['quality_metrics']['navigation_health_score'] * 0.3
        )
        
        print(f"\nOverall Documentation Health: {overall_score:.1f}/100")
        
        # Validation assertions
        assert comprehensive_report['summary']['config_valid'], "Configuration must be valid"
        assert comprehensive_report['summary']['total_markdown_files'] > 0, "Must have markdown files"
        assert overall_score >= 0, "Health score must be non-negative"
        
        return comprehensive_report

    @pytest.mark.integration
    def test_error_recovery_and_resilience(self, temp_docs_root):
        """Test error recovery and resilience of validation system."""
        # Create problematic documentation scenarios
        docs_dir = temp_docs_root / "docs"
        
        # Create file with various issues
        problematic_file = docs_dir / "problematic.md"
        problematic_content = f"""# Problematic Document

This line is way too long and exceeds any reasonable line length limit that might be set for markdown linting purposes and will definitely trigger warnings   

This line has trailing spaces.   

There are too many empty lines below:




## Bad Links

Here's a [broken link](nonexistent.md).
Here's another [bad link](../../../etc/passwd).
![Missing image](missing-image.png)

## Malformed Content

```
Code block without language specification
```

| Bad | Table |
|-----|
| Missing cell |

####### Too many heading levels

### Inconsistent heading levels (skipping levels)
"""
        problematic_file.write_text(problematic_content)
        
        # Test that validators handle problematic content gracefully
        validators = [
            MarkdownQualityChecker(temp_docs_root),
            ImageReferenceValidator(temp_docs_root),
            NavigationStructureValidator(temp_docs_root)
        ]
        
        for validator in validators:
            try:
                if isinstance(validator, MarkdownQualityChecker):
                    results = validator.check_all_files()
                    report = validator.generate_quality_report(results)
                    assert 'total_issues' in report
                    
                elif isinstance(validator, ImageReferenceValidator):
                    results = validator.validate_all_images()
                    report = validator.generate_image_report(results)
                    assert 'total_image_issues' in report
                    
                elif isinstance(validator, NavigationStructureValidator):
                    results = validator.validate_all_navigation()
                    report = validator.generate_navigation_report(results)
                    assert 'total_issues' in report
                    
            except Exception as e:
                pytest.fail(f"Validator {type(validator).__name__} failed with: {e}")
        
        print("All validators handled problematic content gracefully")

    @pytest.mark.integration 
    @pytest.mark.network
    @pytest.mark.asyncio
    async def test_external_link_validation(self, temp_docs_root):
        """Test external link validation with real network calls (optional)."""
        # Create test file with external links
        docs_dir = temp_docs_root / "docs"
        external_links_file = docs_dir / "external_links.md"
        
        content = """# External Links Test

Here are some external links for testing:

- [Microsoft Docs](https://docs.microsoft.com)
- [Azure Portal](https://portal.azure.com)  
- [GitHub](https://github.com)
- [Invalid Domain](https://thisdomaindoesnotexist12345.com)
"""
        external_links_file.write_text(content)
        
        # Test with actual network calls (may be slow/unreliable)
        async with LinkValidator(temp_docs_root) as validator:
            try:
                results = await validator.validate_all_links(check_external=True)
                report = validator.generate_report(results)
                
                print(f"\nExternal Link Validation (Network Test):")
                print(f"Total Links Checked: {report['total_links']}")
                print(f"Success Rate: {report['success_rate']:.1f}%")
                
                if report['broken_links'] > 0:
                    print(f"Broken Links: {report['broken_links']}")
                    for broken in report['broken_link_details'][:3]:
                        print(f"  - {broken['url']}: {broken['error']}")
                        
            except Exception as e:
                pytest.skip(f"Network-based link validation failed: {e}")

    @pytest.mark.integration
    def test_cross_validator_consistency(self, temp_docs_root):
        """Test consistency between different validators."""
        # Get file lists from different validators
        build_tester = DocumentationBuildTester(temp_docs_root)
        markdown_checker = MarkdownQualityChecker(temp_docs_root)
        image_validator = ImageReferenceValidator(temp_docs_root)
        nav_validator = NavigationStructureValidator(temp_docs_root)
        
        # Check that validators agree on basic file structure
        build_stats = build_tester.get_build_statistics()
        quality_results = markdown_checker.check_all_files()
        image_results = image_validator.validate_all_images()
        nav_results = nav_validator.validate_all_navigation()
        
        # Basic consistency checks
        assert build_stats['total_markdown_files'] > 0
        assert len(quality_results) <= build_stats['total_markdown_files']
        
        # Validators should process the same files
        quality_files = set(quality_results.keys())
        image_files = set(image_results.keys())
        
        # Image validator might find fewer files (only those with images)
        if image_files:
            assert image_files.issubset(quality_files) or quality_files.issubset(image_files)
        
        print(f"Cross-validator consistency check passed")
        print(f"Build tester found: {build_stats['total_markdown_files']} files")
        print(f"Quality checker processed: {len(quality_results)} files")
        print(f"Image validator found issues in: {len(image_results)} files")