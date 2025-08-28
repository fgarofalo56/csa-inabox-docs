"""Command-line interface for CSA Docs Tools."""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import logging

from . import (
    DocumentationBuildTester,
    LinkValidator,
    MarkdownQualityChecker, 
    ImageReferenceValidator,
    NavigationStructureValidator
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_parser() -> argparse.ArgumentParser:
    """Set up command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="CSA Documentation Testing and Validation Tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all validations
  csa-docs-validate all
  
  # Test documentation build
  csa-docs-validate build --strict
  
  # Check markdown quality
  csa-docs-validate quality --min-score 80
  
  # Validate links (internal only)
  csa-docs-validate links --no-external
  
  # Check images
  csa-docs-validate images --report-unused
  
  # Validate navigation
  csa-docs-validate nav --max-depth 4
        """
    )
    
    parser.add_argument(
        "--docs-root",
        type=Path,
        default=Path.cwd(),
        help="Path to documentation root directory (default: current directory)"
    )
    
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--output",
        choices=["json", "text", "summary"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress non-error output"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true", 
        help="Enable verbose output"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # All validations command
    all_parser = subparsers.add_parser("all", help="Run all validations")
    all_parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop on first failure"
    )
    
    # Build testing command
    build_parser = subparsers.add_parser("build", help="Test documentation build")
    build_parser.add_argument(
        "--strict",
        action="store_true",
        help="Use strict mode (warnings as errors)"
    )
    
    # Quality checking command
    quality_parser = subparsers.add_parser("quality", help="Check markdown quality")
    quality_parser.add_argument(
        "--min-score",
        type=float,
        default=70.0,
        help="Minimum quality score required (default: 70.0)"
    )
    quality_parser.add_argument(
        "--markdownlint",
        action="store_true",
        help="Use markdownlint CLI if available"
    )
    
    # Link validation command  
    links_parser = subparsers.add_parser("links", help="Validate links")
    links_parser.add_argument(
        "--no-external",
        action="store_true",
        help="Skip external link validation"
    )
    links_parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout for external links in seconds (default: 30)"
    )
    
    # Image validation command
    images_parser = subparsers.add_parser("images", help="Validate image references")
    images_parser.add_argument(
        "--report-unused",
        action="store_true",
        help="Report unused image files"
    )
    images_parser.add_argument(
        "--check-alt-text",
        action="store_true",
        help="Validate alt text quality"
    )
    
    # Navigation validation command
    nav_parser = subparsers.add_parser("nav", help="Validate navigation structure")
    nav_parser.add_argument(
        "--max-depth",
        type=int,
        default=4,
        help="Maximum navigation depth (default: 4)"
    )
    
    return parser


async def run_all_validations(args) -> Dict[str, Any]:
    """Run all validation checks."""
    results = {}
    docs_root = args.docs_root
    
    try:
        # Build validation
        if not args.quiet:
            print("🔧 Testing documentation build...")
        
        build_tester = DocumentationBuildTester(docs_root)
        build_stats = build_tester.get_build_statistics()
        results['build'] = {
            'status': 'success' if build_stats['build_successful'] else 'failed',
            'stats': build_stats
        }
        
        if args.fail_fast and not build_stats['build_successful']:
            return results
            
    except Exception as e:
        results['build'] = {'status': 'error', 'message': str(e)}
        if args.fail_fast:
            return results
    
    try:
        # Quality validation
        if not args.quiet:
            print("📝 Checking markdown quality...")
            
        quality_checker = MarkdownQualityChecker(docs_root)
        quality_results = quality_checker.check_all_files()
        quality_report = quality_checker.generate_quality_report(quality_results)
        results['quality'] = {
            'status': 'success',
            'report': quality_report
        }
        
    except Exception as e:
        results['quality'] = {'status': 'error', 'message': str(e)}
        if args.fail_fast:
            return results
    
    try:
        # Image validation
        if not args.quiet:
            print("🖼️  Validating images...")
            
        image_validator = ImageReferenceValidator(docs_root)
        image_results = image_validator.validate_all_images()
        image_report = image_validator.generate_image_report(image_results)
        results['images'] = {
            'status': 'success',
            'report': image_report
        }
        
    except Exception as e:
        results['images'] = {'status': 'error', 'message': str(e)}
        if args.fail_fast:
            return results
    
    try:
        # Navigation validation
        if not args.quiet:
            print("🧭 Validating navigation structure...")
            
        nav_validator = NavigationStructureValidator(docs_root)
        nav_results = nav_validator.validate_all_navigation()
        nav_report = nav_validator.generate_navigation_report(nav_results)
        results['navigation'] = {
            'status': 'success',
            'report': nav_report
        }
        
    except Exception as e:
        results['navigation'] = {'status': 'error', 'message': str(e)}
        if args.fail_fast:
            return results
    
    try:
        # Link validation (internal only by default for speed)
        if not args.quiet:
            print("🔗 Validating links...")
            
        async with LinkValidator(docs_root) as link_validator:
            link_results = await link_validator.validate_all_links(check_external=False)
            link_report = link_validator.generate_report(link_results)
            results['links'] = {
                'status': 'success',
                'report': link_report
            }
            
    except Exception as e:
        results['links'] = {'status': 'error', 'message': str(e)}
    
    return results


def run_build_test(args) -> Dict[str, Any]:
    """Run build testing."""
    build_tester = DocumentationBuildTester(args.docs_root)
    
    # Validate configuration
    config_valid, config_errors = build_tester.validate_mkdocs_config()
    if not config_valid:
        return {
            'status': 'failed',
            'errors': config_errors
        }
    
    # Test build
    success, stdout, stderr = build_tester.test_build(strict=args.strict)
    
    return {
        'status': 'success' if success else 'failed',
        'build_successful': success,
        'stdout': stdout,
        'stderr': stderr,
        'stats': build_tester.get_build_statistics()
    }


def run_quality_check(args) -> Dict[str, Any]:
    """Run markdown quality checking."""
    quality_checker = MarkdownQualityChecker(args.docs_root)
    
    # Check all files
    results = quality_checker.check_all_files()
    report = quality_checker.generate_quality_report(results)
    
    # Check minimum score
    passed = report['quality_score'] >= args.min_score
    
    return {
        'status': 'success' if passed else 'failed',
        'passed_min_score': passed,
        'min_score_required': args.min_score,
        'report': report
    }


async def run_link_validation(args) -> Dict[str, Any]:
    """Run link validation."""
    async with LinkValidator(args.docs_root) as validator:
        check_external = not args.no_external
        results = await validator.validate_all_links(check_external=check_external)
        report = validator.generate_report(results)
        
        # Consider it a failure if there are broken links
        has_broken_links = report['broken_links'] > 0
        
        return {
            'status': 'failed' if has_broken_links else 'success',
            'has_broken_links': has_broken_links,
            'checked_external': check_external,
            'report': report
        }


def run_image_validation(args) -> Dict[str, Any]:
    """Run image validation."""
    image_validator = ImageReferenceValidator(args.docs_root)
    
    results = image_validator.validate_all_images()
    report = image_validator.generate_image_report(results)
    
    # Check for errors
    error_count = sum(
        1 for issues in results.values() 
        for issue in issues 
        if issue.severity == 'error'
    )
    
    return {
        'status': 'failed' if error_count > 0 else 'success',
        'has_errors': error_count > 0,
        'error_count': error_count,
        'report': report
    }


def run_nav_validation(args) -> Dict[str, Any]:
    """Run navigation validation."""
    nav_validator = NavigationStructureValidator(args.docs_root)
    
    results = nav_validator.validate_all_navigation()
    
    # Check depth if specified
    depth_results = nav_validator.validate_nav_depth(args.max_depth)
    if depth_results:
        results['nav_depth'] = depth_results
    
    report = nav_validator.generate_navigation_report(results)
    
    # Check for errors
    error_count = sum(
        1 for issues in results.values()
        for issue in issues
        if issue.severity == 'error'
    )
    
    return {
        'status': 'failed' if error_count > 0 else 'success',
        'has_errors': error_count > 0,
        'error_count': error_count,
        'max_depth_checked': args.max_depth,
        'report': report
    }


def format_output(results: Dict[str, Any], output_format: str, quiet: bool = False) -> str:
    """Format output based on specified format."""
    if output_format == "json":
        return json.dumps(results, indent=2, default=str)
    
    elif output_format == "summary":
        # Generate summary format
        if 'build' in results:
            build_status = results['build']['status']
        else:
            build_status = results.get('status', 'unknown')
            
        summary = f"Status: {build_status}\n"
        
        if 'report' in results:
            report = results['report']
            if 'quality_score' in report:
                summary += f"Quality Score: {report['quality_score']:.1f}/100\n"
            if 'image_health_score' in report:
                summary += f"Image Health: {report['image_health_score']:.1f}/100\n"
            if 'navigation_health_score' in report:
                summary += f"Navigation Health: {report['navigation_health_score']:.1f}/100\n"
                
        return summary.strip()
    
    else:  # text format
        output_lines = []
        
        if isinstance(results, dict) and 'build' in results:
            # All validations result
            output_lines.append("=== CSA Documentation Validation Report ===\n")
            
            for category, result in results.items():
                if result['status'] == 'success':
                    output_lines.append(f"✅ {category.title()}: PASSED")
                    
                    # Add key metrics
                    if 'report' in result:
                        report = result['report']
                        if 'quality_score' in report:
                            output_lines.append(f"   Quality Score: {report['quality_score']:.1f}/100")
                        if 'image_health_score' in report:
                            output_lines.append(f"   Image Health: {report['image_health_score']:.1f}/100")
                        if 'navigation_health_score' in report:
                            output_lines.append(f"   Navigation Health: {report['navigation_health_score']:.1f}/100")
                        if 'success_rate' in report:
                            output_lines.append(f"   Link Success Rate: {report['success_rate']:.1f}%")
                            
                elif result['status'] == 'failed':
                    output_lines.append(f"❌ {category.title()}: FAILED")
                    if 'message' in result:
                        output_lines.append(f"   Error: {result['message']}")
                        
                else:  # error
                    output_lines.append(f"⚠️  {category.title()}: ERROR")
                    if 'message' in result:
                        output_lines.append(f"   {result['message']}")
                
                output_lines.append("")
                
        else:
            # Single validation result
            status = results.get('status', 'unknown')
            if status == 'success':
                output_lines.append("✅ Validation PASSED")
            elif status == 'failed':
                output_lines.append("❌ Validation FAILED")
            else:
                output_lines.append("⚠️  Validation ERROR")
                
            # Add specific details based on validation type
            if 'report' in results:
                report = results['report']
                if not quiet:
                    output_lines.append("\n--- Details ---")
                    for key, value in report.items():
                        if isinstance(value, (int, float)):
                            output_lines.append(f"{key}: {value}")
                        elif isinstance(value, str):
                            output_lines.append(f"{key}: {value}")
        
        return "\n".join(output_lines)


async def main() -> int:
    """Main CLI entry point."""
    parser = setup_parser()
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Validate docs root
    if not args.docs_root.exists():
        print(f"Error: Documentation root not found: {args.docs_root}")
        return 1
    
    try:
        # Execute command
        if args.command == "all":
            results = await run_all_validations(args)
        elif args.command == "build":
            results = run_build_test(args)
        elif args.command == "quality":
            results = run_quality_check(args)
        elif args.command == "links":
            results = await run_link_validation(args)
        elif args.command == "images":
            results = run_image_validation(args)
        elif args.command == "nav":
            results = run_nav_validation(args)
        else:
            print(f"Unknown command: {args.command}")
            return 1
        
        # Format and print output
        output = format_output(results, args.output, args.quiet)
        print(output)
        
        # Determine exit code
        if args.command == "all":
            # Check if any validation failed
            failed = any(
                result.get('status') in ['failed', 'error'] 
                for result in results.values()
            )
            return 1 if failed else 0
        else:
            # Single validation
            return 1 if results.get('status') in ['failed', 'error'] else 0
            
    except KeyboardInterrupt:
        print("\nValidation interrupted by user")
        return 130
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def sync_main() -> int:
    """Synchronous wrapper for main."""
    return asyncio.run(main())


if __name__ == "__main__":
    sys.exit(sync_main())