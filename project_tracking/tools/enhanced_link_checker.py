#!/usr/bin/env python3
"""
Enhanced link checker that integrates with the new CSA Documentation Tools
Extends the existing link checker with the unified tooling capabilities
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add project root to path to import existing modules
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from project_planning.tools.link_checker import LinkChecker
    from project_planning.tools.csa_docs_integration import CSADocsIntegration
except ImportError:
    print("Warning: Could not import existing modules. Running in standalone mode.")
    LinkChecker = None


class EnhancedLinkChecker:
    """Enhanced link checker with CSA Documentation Tools integration."""
    
    def __init__(self, docs_dir: str = "docs"):
        """Initialize the enhanced link checker.
        
        Args:
            docs_dir: Documentation directory to check
        """
        self.docs_dir = Path(docs_dir)
        self.csa_integration = None
        
        # Try to initialize CSA integration
        try:
            self.csa_integration = CSADocsIntegration()
        except Exception as e:
            print(f"Warning: CSA Documentation Tools not available: {e}")
        
        # Try to initialize legacy link checker
        self.legacy_checker = None
        if LinkChecker:
            try:
                self.legacy_checker = LinkChecker(str(self.docs_dir))
            except Exception as e:
                print(f"Warning: Legacy link checker not available: {e}")
    
    def check_with_csa_tools(self) -> Tuple[Dict, bool]:
        """Check links using CSA Documentation Tools.
        
        Returns:
            Tuple of (results dict, success boolean)
        """
        if not self.csa_integration:
            return {"error": "CSA Documentation Tools not available"}, False
        
        try:
            print("🔍 Running comprehensive documentation audit...")
            audit_result = self.csa_integration.audit(output_format="json")
            
            print("🔗 Validating internal links...")
            validation_result = self.csa_integration.validate_links()
            
            # Extract link-related issues
            broken_links = audit_result.get("issues", {}).get("brokenLinks", [])
            
            results = {
                "method": "csa-documentation-tools",
                "total_broken_links": len(broken_links),
                "broken_links": broken_links,
                "health_score": audit_result.get("executiveSummary", {}).get("healthScore", 0),
                "validation_output": validation_result.get("output", ""),
                "audit_summary": audit_result.get("summary", {}),
                "timestamp": audit_result.get("timestamp")
            }
            
            return results, len(broken_links) == 0
            
        except Exception as e:
            return {"error": f"CSA tools check failed: {str(e)}"}, False
    
    def check_with_legacy_tools(self) -> Tuple[Dict, bool]:
        """Check links using legacy link checker.
        
        Returns:
            Tuple of (results dict, success boolean)
        """
        if not self.legacy_checker:
            return {"error": "Legacy link checker not available"}, False
        
        try:
            print("🔗 Running legacy link checker...")
            results = self.legacy_checker.check_all_links()
            
            broken_count = len(results.get("broken_links", []))
            
            return {
                "method": "legacy-link-checker",
                "total_broken_links": broken_count,
                "broken_links": results.get("broken_links", []),
                "valid_links": results.get("valid_links", []),
                "summary": results.get("summary", {})
            }, broken_count == 0
            
        except Exception as e:
            return {"error": f"Legacy check failed: {str(e)}"}, False
    
    def comprehensive_check(self, use_legacy: bool = False, 
                          external_links: bool = False) -> Dict:
        """Run comprehensive link checking with both tools.
        
        Args:
            use_legacy: Whether to also run legacy checker
            external_links: Whether to check external links
            
        Returns:
            Combined results from both checkers
        """
        results = {
            "timestamp": None,
            "documentation_directory": str(self.docs_dir),
            "methods_used": [],
            "overall_success": True,
            "summary": {},
            "detailed_results": {}
        }
        
        # Check with CSA Documentation Tools
        if self.csa_integration:
            print("\n" + "="*60)
            print("🚀 CSA Documentation Tools Check")
            print("="*60)
            
            csa_results, csa_success = self.check_with_csa_tools()
            results["methods_used"].append("csa-documentation-tools")
            results["detailed_results"]["csa_tools"] = csa_results
            results["overall_success"] = results["overall_success"] and csa_success
            
            if not csa_success:
                print(f"❌ CSA tools found issues: {csa_results.get('total_broken_links', 'unknown')}")
            else:
                print("✅ CSA tools validation passed")
        
        # Check with legacy tools if requested
        if use_legacy and self.legacy_checker:
            print("\n" + "="*60)
            print("🔗 Legacy Link Checker")
            print("="*60)
            
            legacy_results, legacy_success = self.check_with_legacy_tools()
            results["methods_used"].append("legacy-link-checker")
            results["detailed_results"]["legacy_checker"] = legacy_results
            results["overall_success"] = results["overall_success"] and legacy_success
            
            if not legacy_success:
                print(f"❌ Legacy checker found issues: {legacy_results.get('total_broken_links', 'unknown')}")
            else:
                print("✅ Legacy checker validation passed")
        
        # External link validation with CSA tools
        if external_links and self.csa_integration:
            print("\n" + "="*60)
            print("🌐 External Link Validation")
            print("="*60)
            
            try:
                external_result = self.csa_integration.validate_links(external=True)
                results["detailed_results"]["external_links"] = external_result
                print("✅ External link validation completed")
            except Exception as e:
                print(f"⚠️ External link validation failed: {e}")
                results["detailed_results"]["external_links"] = {"error": str(e)}
        
        # Generate summary
        total_broken = 0
        for method_results in results["detailed_results"].values():
            if isinstance(method_results, dict) and "total_broken_links" in method_results:
                total_broken += method_results["total_broken_links"]
        
        results["summary"] = {
            "total_broken_links": total_broken,
            "methods_used_count": len(results["methods_used"]),
            "overall_success": results["overall_success"],
            "has_external_check": external_links,
            "has_legacy_check": use_legacy
        }
        
        return results
    
    def generate_report(self, results: Dict, output_format: str = "text",
                       output_file: Optional[str] = None) -> str:
        """Generate a formatted report from check results.
        
        Args:
            results: Results from comprehensive_check
            output_format: Format ('text', 'json', 'markdown')
            output_file: Optional file to save report
            
        Returns:
            Formatted report string
        """
        if output_format == "json":
            report = json.dumps(results, indent=2)
        
        elif output_format == "markdown":
            report = self._generate_markdown_report(results)
        
        else:  # text format
            report = self._generate_text_report(results)
        
        # Save to file if requested
        if output_file:
            Path(output_file).write_text(report)
            print(f"📄 Report saved to: {output_file}")
        
        return report
    
    def _generate_text_report(self, results: Dict) -> str:
        """Generate text format report."""
        lines = []
        lines.append("=" * 60)
        lines.append("📊 ENHANCED LINK CHECK REPORT")
        lines.append("=" * 60)
        lines.append("")
        
        # Summary
        summary = results.get("summary", {})
        lines.append("📈 SUMMARY:")
        lines.append(f"Documentation Directory: {results.get('documentation_directory')}")
        lines.append(f"Methods Used: {', '.join(results.get('methods_used', []))}")
        lines.append(f"Total Broken Links: {summary.get('total_broken_links', 0)}")
        lines.append(f"Overall Success: {'✅ PASS' if results.get('overall_success') else '❌ FAIL'}")
        lines.append("")
        
        # Detailed results
        for method, method_results in results.get("detailed_results", {}).items():
            lines.append(f"🔍 {method.upper().replace('_', ' ')} RESULTS:")
            lines.append("-" * 40)
            
            if "error" in method_results:
                lines.append(f"❌ Error: {method_results['error']}")
            else:
                if "total_broken_links" in method_results:
                    lines.append(f"Broken Links: {method_results['total_broken_links']}")
                
                if "health_score" in method_results:
                    score = method_results["health_score"]
                    lines.append(f"Health Score: {score}/100")
                
                if "broken_links" in method_results and method_results["broken_links"]:
                    lines.append("\nBroken Links Details:")
                    for link in method_results["broken_links"][:10]:  # Limit to first 10
                        if isinstance(link, dict):
                            source = link.get("sourceFile", link.get("file", "unknown"))
                            url = link.get("linkUrl", link.get("url", "unknown"))
                            line_num = link.get("line", "unknown")
                            lines.append(f"  - {source}:{line_num} → {url}")
                        else:
                            lines.append(f"  - {link}")
                    
                    if len(method_results["broken_links"]) > 10:
                        remaining = len(method_results["broken_links"]) - 10
                        lines.append(f"  ... and {remaining} more")
            
            lines.append("")
        
        # Recommendations
        lines.append("💡 RECOMMENDATIONS:")
        if summary.get("total_broken_links", 0) == 0:
            lines.append("✅ All links are working correctly!")
        else:
            lines.append("1. Fix broken internal links to improve navigation")
            lines.append("2. Consider using CSA Documentation Tools for automated fixes:")
            lines.append("   cd tools && npm run docs:fix")
            lines.append("3. Run regular link validation in CI/CD pipeline")
        
        lines.append("")
        lines.append("Generated with Enhanced Link Checker")
        
        return "\n".join(lines)
    
    def _generate_markdown_report(self, results: Dict) -> str:
        """Generate markdown format report."""
        lines = []
        lines.append("# Enhanced Link Check Report")
        lines.append("")
        
        # Summary table
        summary = results.get("summary", {})
        lines.append("## Summary")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Documentation Directory | `{results.get('documentation_directory')}` |")
        lines.append(f"| Methods Used | {', '.join(results.get('methods_used', []))} |")
        lines.append(f"| Total Broken Links | {summary.get('total_broken_links', 0)} |")
        lines.append(f"| Overall Status | {'✅ PASS' if results.get('overall_success') else '❌ FAIL'} |")
        lines.append("")
        
        # Detailed results
        lines.append("## Detailed Results")
        lines.append("")
        
        for method, method_results in results.get("detailed_results", {}).items():
            method_title = method.replace('_', ' ').title()
            lines.append(f"### {method_title}")
            lines.append("")
            
            if "error" in method_results:
                lines.append(f"❌ **Error:** {method_results['error']}")
            else:
                if "total_broken_links" in method_results:
                    lines.append(f"- **Broken Links:** {method_results['total_broken_links']}")
                
                if "health_score" in method_results:
                    score = method_results["health_score"]
                    lines.append(f"- **Health Score:** {score}/100")
                
                if "broken_links" in method_results and method_results["broken_links"]:
                    lines.append("")
                    lines.append("**Broken Links:**")
                    lines.append("")
                    for link in method_results["broken_links"][:5]:  # Limit for markdown
                        if isinstance(link, dict):
                            source = link.get("sourceFile", link.get("file", "unknown"))
                            url = link.get("linkUrl", link.get("url", "unknown"))
                            line_num = link.get("line", "unknown")
                            lines.append(f"- `{source}:{line_num}` → `{url}`")
                        else:
                            lines.append(f"- `{link}`")
            
            lines.append("")
        
        # Recommendations
        lines.append("## Recommendations")
        lines.append("")
        
        if summary.get("total_broken_links", 0) == 0:
            lines.append("✅ **All links are working correctly!**")
        else:
            lines.append("1. **Fix broken internal links** to improve navigation")
            lines.append("2. **Use CSA Documentation Tools** for automated fixes:")
            lines.append("   ```bash")
            lines.append("   cd tools && npm run docs:fix")
            lines.append("   ```")
            lines.append("3. **Set up regular validation** in CI/CD pipeline")
        
        lines.append("")
        lines.append("---")
        lines.append("*Generated with Enhanced Link Checker*")
        
        return "\n".join(lines)
    
    def quick_health_check(self) -> bool:
        """Quick health check for CI/CD pipelines.
        
        Returns:
            True if documentation is healthy
        """
        if not self.csa_integration:
            print("⚠️ CSA Documentation Tools not available for health check")
            return False
        
        try:
            is_healthy = self.csa_integration.is_healthy(threshold=80.0)
            health_score = self.csa_integration.get_health_score()
            
            print(f"📊 Documentation Health Score: {health_score:.1f}/100")
            
            if is_healthy:
                print("✅ Documentation is healthy")
            else:
                print("❌ Documentation needs attention")
            
            return is_healthy
            
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Enhanced Link Checker with CSA Documentation Tools integration"
    )
    
    parser.add_argument("--docs-dir", default="docs", 
                       help="Documentation directory to check")
    parser.add_argument("--use-legacy", action="store_true",
                       help="Also run legacy link checker")
    parser.add_argument("--external", action="store_true",
                       help="Check external links (slower)")
    parser.add_argument("--output-format", choices=["text", "json", "markdown"],
                       default="text", help="Report output format")
    parser.add_argument("--output-file", help="Save report to file")
    parser.add_argument("--quick-health", action="store_true",
                       help="Run quick health check only")
    
    args = parser.parse_args()
    
    try:
        checker = EnhancedLinkChecker(args.docs_dir)
        
        if args.quick_health:
            # Quick health check for CI/CD
            success = checker.quick_health_check()
            sys.exit(0 if success else 1)
        
        # Full comprehensive check
        print("🚀 Starting Enhanced Link Check...")
        print(f"📁 Documentation Directory: {args.docs_dir}")
        
        results = checker.comprehensive_check(
            use_legacy=args.use_legacy,
            external_links=args.external
        )
        
        # Generate and display report
        report = checker.generate_report(
            results,
            output_format=args.output_format,
            output_file=args.output_file
        )
        
        if not args.output_file or args.output_format == "text":
            print("\n" + report)
        
        # Exit with appropriate code
        sys.exit(0 if results["overall_success"] else 1)
        
    except Exception as e:
        print(f"❌ Enhanced link check failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()