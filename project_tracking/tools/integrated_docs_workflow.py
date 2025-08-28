#!/usr/bin/env python3
"""
Integrated documentation workflow that combines existing Python tools 
with the new CSA Documentation Tools for a complete build pipeline
"""

import sys
import os
import subprocess
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import time

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from project_planning.tools.csa_docs_integration import CSADocsIntegration
    from project_planning.tools.enhanced_link_checker import EnhancedLinkChecker
except ImportError as e:
    print(f"Warning: Could not import integration modules: {e}")
    CSADocsIntegration = None
    EnhancedLinkChecker = None


class IntegratedDocsWorkflow:
    """Integrated documentation workflow combining Python and Node.js tools."""
    
    def __init__(self, docs_dir: str = "docs", project_root: Optional[str] = None):
        """Initialize the integrated workflow.
        
        Args:
            docs_dir: Documentation directory
            project_root: Project root directory
        """
        self.docs_dir = Path(docs_dir)
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.tools_dir = self.project_root / "tools"
        self.planning_tools_dir = self.project_root / "project_tracking" / "tools"
        
        # Initialize integrations
        self.csa_integration = None
        self.link_checker = None
        
        if CSADocsIntegration:
            try:
                self.csa_integration = CSADocsIntegration(str(self.tools_dir))
            except Exception as e:
                print(f"Warning: CSA integration not available: {e}")
        
        if EnhancedLinkChecker:
            try:
                self.link_checker = EnhancedLinkChecker(str(self.docs_dir))
            except Exception as e:
                print(f"Warning: Enhanced link checker not available: {e}")
        
        # Workflow state
        self.workflow_start_time = None
        self.step_results = {}
        self.overall_success = True
    
    def log_step(self, step: str, status: str, message: str = "", details: Any = None):
        """Log workflow step with timestamp.
        
        Args:
            step: Step name
            status: Status (start, success, warning, error)
            message: Additional message
            details: Additional details to store
        """
        timestamp = datetime.now().isoformat()
        
        if step not in self.step_results:
            self.step_results[step] = {
                "start_time": timestamp if status == "start" else None,
                "end_time": None,
                "status": "running",
                "messages": [],
                "details": None
            }
        
        self.step_results[step]["messages"].append({
            "timestamp": timestamp,
            "status": status,
            "message": message
        })
        
        if status in ["success", "error", "warning"]:
            self.step_results[step]["end_time"] = timestamp
            self.step_results[step]["status"] = status
            self.step_results[step]["details"] = details
        
        # Print status with emoji
        emoji_map = {
            "start": "🚀",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        emoji = emoji_map.get(status, "ℹ️")
        print(f"{emoji} [{datetime.now().strftime('%H:%M:%S')}] {step}: {message}")
        
        if status == "error":
            self.overall_success = False
    
    def run_python_serve_docs(self, port: int = 8000) -> Dict:
        """Run the Python docs server for testing.
        
        Args:
            port: Port to serve on
            
        Returns:
            Server start result
        """
        self.log_step("python-serve", "start", f"Starting docs server on port {port}")
        
        try:
            serve_script = self.planning_tools_dir / "serve-docs.py"
            
            if not serve_script.exists():
                raise FileNotFoundError(f"serve-docs.py not found at {serve_script}")
            
            # Start server in background
            process = subprocess.Popen([
                sys.executable, str(serve_script), "--port", str(port)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Give server time to start
            time.sleep(2)
            
            # Check if server started successfully
            if process.poll() is None:
                self.log_step("python-serve", "success", f"Docs server running on port {port}")
                return {
                    "status": "success",
                    "port": port,
                    "process": process,
                    "url": f"http://localhost:{port}"
                }
            else:
                stdout, stderr = process.communicate()
                raise RuntimeError(f"Server failed to start: {stderr.decode()}")
        
        except Exception as e:
            self.log_step("python-serve", "error", str(e))
            return {"status": "error", "error": str(e)}
    
    def run_documentation_audit(self) -> Dict:
        """Run comprehensive documentation audit."""
        self.log_step("audit", "start", "Running comprehensive documentation audit")
        
        try:
            if not self.csa_integration:
                raise RuntimeError("CSA Documentation Tools not available")
            
            # Run audit
            audit_result = self.csa_integration.audit(output_format="json")
            
            # Extract key metrics
            summary = audit_result.get("executiveSummary", {})
            health_score = summary.get("healthScore", 0)
            total_issues = summary.get("totalIssues", 0)
            critical_issues = summary.get("criticalIssues", 0)
            
            status = "success" if critical_issues == 0 else "warning" if total_issues < 10 else "error"
            message = f"Health score: {health_score}/100, Issues: {total_issues} ({critical_issues} critical)"
            
            self.log_step("audit", status, message, audit_result)
            
            return {
                "status": status,
                "health_score": health_score,
                "total_issues": total_issues,
                "critical_issues": critical_issues,
                "audit_result": audit_result
            }
        
        except Exception as e:
            self.log_step("audit", "error", str(e))
            return {"status": "error", "error": str(e)}
    
    def run_diagram_generation(self) -> Dict:
        """Run diagram generation pipeline."""
        self.log_step("diagrams", "start", "Generating diagrams from Mermaid placeholders")
        
        try:
            if not self.csa_integration:
                raise RuntimeError("CSA Documentation Tools not available")
            
            # Generate diagrams
            gen_result = self.csa_integration.generate_diagrams()
            
            # Replace Mermaid blocks with PNG references
            replace_result = self.csa_integration.replace_mermaid()
            
            self.log_step("diagrams", "success", "Diagrams generated and replaced successfully", {
                "generation": gen_result,
                "replacement": replace_result
            })
            
            return {
                "status": "success",
                "generation_result": gen_result,
                "replacement_result": replace_result
            }
        
        except Exception as e:
            self.log_step("diagrams", "error", str(e))
            return {"status": "error", "error": str(e)}
    
    def run_automated_fixes(self) -> Dict:
        """Run automated documentation fixes."""
        self.log_step("fixes", "start", "Running automated documentation fixes")
        
        try:
            if not self.csa_integration:
                raise RuntimeError("CSA Documentation Tools not available")
            
            fix_result = self.csa_integration.fix_issues()
            
            self.log_step("fixes", "success", "Automated fixes applied successfully", fix_result)
            
            return {
                "status": "success",
                "fix_result": fix_result
            }
        
        except Exception as e:
            self.log_step("fixes", "error", str(e))
            return {"status": "error", "error": str(e)}
    
    def run_link_validation(self, include_external: bool = False) -> Dict:
        """Run comprehensive link validation."""
        self.log_step("validation", "start", "Validating internal and external links")
        
        try:
            if not self.link_checker:
                raise RuntimeError("Enhanced link checker not available")
            
            # Run comprehensive link check
            results = self.link_checker.comprehensive_check(
                use_legacy=True,
                external_links=include_external
            )
            
            total_broken = results.get("summary", {}).get("total_broken_links", 0)
            success = results.get("overall_success", False)
            
            status = "success" if success else "warning" if total_broken < 5 else "error"
            message = f"Broken links: {total_broken}"
            
            self.log_step("validation", status, message, results)
            
            return {
                "status": status,
                "total_broken_links": total_broken,
                "validation_results": results
            }
        
        except Exception as e:
            self.log_step("validation", "error", str(e))
            return {"status": "error", "error": str(e)}
    
    def run_mkdocs_build(self) -> Dict:
        """Run MkDocs build to test documentation generation."""
        self.log_step("mkdocs-build", "start", "Building documentation with MkDocs")
        
        try:
            # Check if mkdocs.yml exists
            mkdocs_config = self.project_root / "mkdocs.yml"
            if not mkdocs_config.exists():
                self.log_step("mkdocs-build", "warning", "mkdocs.yml not found, skipping MkDocs build")
                return {"status": "skipped", "reason": "No mkdocs.yml found"}
            
            # Run mkdocs build
            result = subprocess.run([
                "mkdocs", "build", "--clean"
            ], cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_step("mkdocs-build", "success", "MkDocs build successful")
                return {
                    "status": "success",
                    "stdout": result.stdout,
                    "build_dir": str(self.project_root / "site")
                }
            else:
                self.log_step("mkdocs-build", "error", f"MkDocs build failed: {result.stderr}")
                return {
                    "status": "error",
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
        
        except subprocess.SubprocessError as e:
            self.log_step("mkdocs-build", "error", f"Failed to run MkDocs: {e}")
            return {"status": "error", "error": str(e)}
        except Exception as e:
            self.log_step("mkdocs-build", "error", str(e))
            return {"status": "error", "error": str(e)}
    
    def run_full_workflow(self, include_external_links: bool = False,
                         serve_docs: bool = False, skip_mkdocs: bool = False) -> Dict:
        """Run the complete integrated documentation workflow.
        
        Args:
            include_external_links: Whether to validate external links
            serve_docs: Whether to start docs server
            skip_mkdocs: Whether to skip MkDocs build
            
        Returns:
            Complete workflow results
        """
        self.workflow_start_time = datetime.now()
        
        print("🚀 Starting Integrated Documentation Workflow")
        print("=" * 60)
        print(f"📁 Documentation Directory: {self.docs_dir}")
        print(f"🏗️ Project Root: {self.project_root}")
        print(f"🔧 Tools Directory: {self.tools_dir}")
        print("=" * 60)
        
        workflow_results = {
            "start_time": self.workflow_start_time.isoformat(),
            "steps": {},
            "overall_success": True,
            "summary": {}
        }
        
        # Step 1: Documentation Audit
        audit_result = self.run_documentation_audit()
        workflow_results["steps"]["audit"] = audit_result
        
        # Step 2: Automated Fixes (if audit found issues)
        if audit_result.get("status") in ["warning", "error"] and audit_result.get("total_issues", 0) > 0:
            fix_result = self.run_automated_fixes()
            workflow_results["steps"]["fixes"] = fix_result
            
            # Re-run audit to see improvements
            print("\n📊 Re-running audit after fixes...")
            audit_after_fixes = self.run_documentation_audit()
            workflow_results["steps"]["audit_after_fixes"] = audit_after_fixes
        
        # Step 3: Diagram Generation
        diagram_result = self.run_diagram_generation()
        workflow_results["steps"]["diagrams"] = diagram_result
        
        # Step 4: Link Validation
        validation_result = self.run_link_validation(include_external_links)
        workflow_results["steps"]["validation"] = validation_result
        
        # Step 5: MkDocs Build
        if not skip_mkdocs:
            mkdocs_result = self.run_mkdocs_build()
            workflow_results["steps"]["mkdocs_build"] = mkdocs_result
        
        # Step 6: Serve Documentation
        if serve_docs:
            serve_result = self.run_python_serve_docs()
            workflow_results["steps"]["serve_docs"] = serve_result
        
        # Calculate overall results
        workflow_results["end_time"] = datetime.now().isoformat()
        workflow_results["duration_minutes"] = (
            datetime.now() - self.workflow_start_time
        ).total_seconds() / 60
        workflow_results["overall_success"] = self.overall_success
        workflow_results["step_results"] = self.step_results
        
        # Generate summary
        workflow_results["summary"] = self._generate_workflow_summary(workflow_results)
        
        # Print final status
        print("\n" + "=" * 60)
        print("📊 WORKFLOW COMPLETE")
        print("=" * 60)
        
        if self.overall_success:
            print("✅ All steps completed successfully!")
        else:
            print("❌ Some steps had issues - check details above")
        
        print(f"⏱️ Total duration: {workflow_results['duration_minutes']:.1f} minutes")
        
        return workflow_results
    
    def _generate_workflow_summary(self, results: Dict) -> Dict:
        """Generate workflow summary statistics."""
        steps = results.get("steps", {})
        
        # Count step statuses
        step_counts = {"success": 0, "warning": 0, "error": 0, "skipped": 0}
        
        for step_result in steps.values():
            status = step_result.get("status", "unknown")
            if status in step_counts:
                step_counts[status] += 1
        
        # Extract key metrics
        audit_result = steps.get("audit", {})
        validation_result = steps.get("validation", {})
        
        return {
            "total_steps": len(steps),
            "successful_steps": step_counts["success"],
            "warning_steps": step_counts["warning"],
            "error_steps": step_counts["error"],
            "skipped_steps": step_counts["skipped"],
            "health_score": audit_result.get("health_score", 0),
            "total_issues": audit_result.get("total_issues", 0),
            "broken_links": validation_result.get("total_broken_links", 0),
            "overall_success": results.get("overall_success", False)
        }
    
    def save_workflow_report(self, results: Dict, output_file: str):
        """Save workflow results to JSON file.
        
        Args:
            results: Workflow results
            output_file: Output file path
        """
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            print(f"📄 Workflow report saved to: {output_path}")
            
        except Exception as e:
            print(f"❌ Failed to save workflow report: {e}")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Integrated Documentation Workflow"
    )
    
    parser.add_argument("--docs-dir", default="docs",
                       help="Documentation directory")
    parser.add_argument("--project-root",
                       help="Project root directory (default: current directory)")
    parser.add_argument("--include-external", action="store_true",
                       help="Include external link validation (slower)")
    parser.add_argument("--serve-docs", action="store_true",
                       help="Start documentation server after build")
    parser.add_argument("--skip-mkdocs", action="store_true",
                       help="Skip MkDocs build step")
    parser.add_argument("--output-report",
                       help="Save workflow report to JSON file")
    
    # Individual step options
    parser.add_argument("--audit-only", action="store_true",
                       help="Run only documentation audit")
    parser.add_argument("--fix-only", action="store_true",
                       help="Run only automated fixes")
    parser.add_argument("--diagrams-only", action="store_true",
                       help="Run only diagram generation")
    parser.add_argument("--validate-only", action="store_true",
                       help="Run only link validation")
    
    args = parser.parse_args()
    
    try:
        workflow = IntegratedDocsWorkflow(
            docs_dir=args.docs_dir,
            project_root=args.project_root
        )
        
        # Run individual steps if requested
        if args.audit_only:
            result = workflow.run_documentation_audit()
        elif args.fix_only:
            result = workflow.run_automated_fixes()
        elif args.diagrams_only:
            result = workflow.run_diagram_generation()
        elif args.validate_only:
            result = workflow.run_link_validation(args.include_external)
        else:
            # Run full workflow
            result = workflow.run_full_workflow(
                include_external_links=args.include_external,
                serve_docs=args.serve_docs,
                skip_mkdocs=args.skip_mkdocs
            )
        
        # Save report if requested
        if args.output_report:
            workflow.save_workflow_report(result, args.output_report)
        
        # Exit with appropriate code
        success = result.get("overall_success", True) if isinstance(result, dict) else result.get("status") == "success"
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"❌ Workflow failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()