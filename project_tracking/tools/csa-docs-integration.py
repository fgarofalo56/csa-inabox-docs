#!/usr/bin/env python3
"""
Integration script for CSA Documentation Tools with existing Python tooling
Provides Python interface to the unified Node.js documentation tooling
"""

import subprocess
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Union
import argparse


class CSADocsIntegration:
    """Python integration layer for CSA Documentation Tools."""
    
    def __init__(self, tools_dir: Optional[str] = None):
        """Initialize the integration layer.
        
        Args:
            tools_dir: Path to the tools directory. If None, auto-detected.
        """
        if tools_dir is None:
            # Auto-detect tools directory
            current_dir = Path(__file__).parent
            self.tools_dir = current_dir.parent.parent / "tools"
        else:
            self.tools_dir = Path(tools_dir)
        
        self.csa_docs_cmd = self.tools_dir / "src" / "bin" / "csa-docs.js"
        
        if not self.csa_docs_cmd.exists():
            raise FileNotFoundError(f"CSA Docs CLI not found at {self.csa_docs_cmd}")
    
    def _run_command(self, cmd: List[str], capture_output: bool = True) -> subprocess.CompletedProcess:
        """Run a CSA docs command and return the result.
        
        Args:
            cmd: Command arguments
            capture_output: Whether to capture stdout/stderr
            
        Returns:
            Completed process result
        """
        full_cmd = ["node", str(self.csa_docs_cmd)] + cmd
        
        try:
            result = subprocess.run(
                full_cmd,
                capture_output=capture_output,
                text=True,
                cwd=self.tools_dir,
                check=False
            )
            return result
        except subprocess.SubprocessError as e:
            raise RuntimeError(f"Failed to run CSA docs command: {e}")
    
    def audit(self, output_format: str = "json", save_report: Optional[str] = None, 
              fix_duplicates: bool = True) -> Dict:
        """Run documentation audit.
        
        Args:
            output_format: Output format ('json' or 'text')
            save_report: Path to save report file
            fix_duplicates: Whether to auto-fix duplicate files
            
        Returns:
            Audit report as dictionary (if JSON format)
        """
        cmd = ["audit", f"--output={output_format}"]
        
        if fix_duplicates:
            cmd.append("--fix-duplicates")
        
        if save_report:
            cmd.extend(["--save-report", save_report])
        
        result = self._run_command(cmd)
        
        if result.returncode != 0:
            raise RuntimeError(f"Audit failed: {result.stderr}")
        
        if output_format == "json":
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON output: {e}")
        else:
            print(result.stdout)
            return {"status": "completed", "output": result.stdout}
    
    def generate_diagrams(self, input_dir: Optional[str] = None, output_dir: Optional[str] = None,
                         theme: str = "default", background: str = "transparent") -> Dict:
        """Generate diagrams from Mermaid placeholders.
        
        Args:
            input_dir: Input directory with placeholder files
            output_dir: Output directory for PNG files
            theme: Mermaid theme
            background: Background color
            
        Returns:
            Generation results
        """
        cmd = ["generate-diagrams", f"--theme={theme}", f"--background={background}"]
        
        if input_dir:
            cmd.extend(["--input-dir", input_dir])
        if output_dir:
            cmd.extend(["--output-dir", output_dir])
        
        result = self._run_command(cmd)
        
        if result.returncode != 0:
            raise RuntimeError(f"Diagram generation failed: {result.stderr}")
        
        return {"status": "completed", "output": result.stdout}
    
    def replace_mermaid(self, dry_run: bool = False) -> Dict:
        """Replace Mermaid blocks with PNG references.
        
        Args:
            dry_run: Preview changes without modifying files
            
        Returns:
            Replacement results
        """
        cmd = ["replace-mermaid"]
        
        if dry_run:
            cmd.append("--dry-run")
        
        result = self._run_command(cmd)
        
        if result.returncode != 0:
            raise RuntimeError(f"Mermaid replacement failed: {result.stderr}")
        
        return {"status": "completed", "output": result.stdout}
    
    def fix_issues(self, create_missing: bool = True, fix_links: bool = True,
                   remove_orphans: bool = True, update_nav: bool = True) -> Dict:
        """Fix common documentation issues.
        
        Args:
            create_missing: Create missing referenced files
            fix_links: Fix broken internal links
            remove_orphans: Remove orphaned diagram files
            update_nav: Update navigation structure
            
        Returns:
            Fix results
        """
        cmd = ["fix-issues"]
        
        if create_missing:
            cmd.append("--create-missing")
        if fix_links:
            cmd.append("--fix-links")
        if remove_orphans:
            cmd.append("--remove-orphans")
        if update_nav:
            cmd.append("--update-nav")
        
        result = self._run_command(cmd)
        
        if result.returncode != 0:
            raise RuntimeError(f"Fix issues failed: {result.stderr}")
        
        return {"status": "completed", "output": result.stdout}
    
    def validate_links(self, external: bool = False, timeout: int = 5000,
                      concurrent: int = 10) -> Dict:
        """Validate internal and external links.
        
        Args:
            external: Include external link validation
            timeout: Timeout for external checks (ms)
            concurrent: Concurrent link checks
            
        Returns:
            Validation results
        """
        cmd = ["validate-links", f"--timeout={timeout}", f"--concurrent={concurrent}"]
        
        if external:
            cmd.append("--external")
        
        result = self._run_command(cmd)
        
        if result.returncode != 0:
            raise RuntimeError(f"Link validation failed: {result.stderr}")
        
        return {"status": "completed", "output": result.stdout}
    
    def build(self, skip_audit: bool = False, skip_diagrams: bool = False,
              skip_fixes: bool = False, skip_validation: bool = False) -> Dict:
        """Run complete documentation build pipeline.
        
        Args:
            skip_audit: Skip documentation audit
            skip_diagrams: Skip diagram generation
            skip_fixes: Skip automated fixes
            skip_validation: Skip link validation
            
        Returns:
            Build results
        """
        cmd = ["build"]
        
        if skip_audit:
            cmd.append("--skip-audit")
        if skip_diagrams:
            cmd.append("--skip-diagrams")
        if skip_fixes:
            cmd.append("--skip-fixes")
        if skip_validation:
            cmd.append("--skip-validation")
        
        result = self._run_command(cmd)
        
        if result.returncode != 0:
            raise RuntimeError(f"Build failed: {result.stderr}")
        
        return {"status": "completed", "output": result.stdout}
    
    def status(self, detailed: bool = False) -> Dict:
        """Get documentation status and health metrics.
        
        Args:
            detailed: Show detailed status information
            
        Returns:
            Status information
        """
        cmd = ["status"]
        
        if detailed:
            cmd.append("--detailed")
        
        result = self._run_command(cmd)
        
        if result.returncode != 0:
            raise RuntimeError(f"Status check failed: {result.stderr}")
        
        return {"status": "completed", "output": result.stdout}
    
    def info(self) -> Dict:
        """Get tool and environment information.
        
        Returns:
            Tool information
        """
        result = self._run_command(["info"])
        
        if result.returncode != 0:
            raise RuntimeError(f"Info command failed: {result.stderr}")
        
        return {"status": "completed", "output": result.stdout}
    
    def get_health_score(self) -> float:
        """Get current documentation health score.
        
        Returns:
            Health score (0-100)
        """
        try:
            audit_result = self.audit(output_format="json")
            return audit_result.get("executiveSummary", {}).get("healthScore", 0.0)
        except Exception as e:
            print(f"Warning: Could not get health score: {e}")
            return 0.0
    
    def is_healthy(self, threshold: float = 80.0) -> bool:
        """Check if documentation health is above threshold.
        
        Args:
            threshold: Health score threshold
            
        Returns:
            True if documentation is healthy
        """
        return self.get_health_score() >= threshold


def main():
    """Main CLI interface for Python integration."""
    parser = argparse.ArgumentParser(description="CSA Documentation Tools Python Integration")
    parser.add_argument("--tools-dir", help="Path to tools directory")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Audit command
    audit_parser = subparsers.add_parser("audit", help="Run documentation audit")
    audit_parser.add_argument("--format", choices=["json", "text"], default="text",
                             help="Output format")
    audit_parser.add_argument("--save-report", help="Save report to file")
    audit_parser.add_argument("--no-fix-duplicates", action="store_true",
                             help="Don't auto-fix duplicate files")
    
    # Build command
    build_parser = subparsers.add_parser("build", help="Run build pipeline")
    build_parser.add_argument("--skip-audit", action="store_true", help="Skip audit")
    build_parser.add_argument("--skip-diagrams", action="store_true", help="Skip diagrams")
    build_parser.add_argument("--skip-fixes", action="store_true", help="Skip fixes")
    build_parser.add_argument("--skip-validation", action="store_true", help="Skip validation")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show status")
    status_parser.add_argument("--detailed", action="store_true", help="Detailed status")
    
    # Health command
    health_parser = subparsers.add_parser("health", help="Check documentation health")
    health_parser.add_argument("--threshold", type=float, default=80.0,
                              help="Health score threshold")
    
    # Info command
    subparsers.add_parser("info", help="Show tool information")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        integration = CSADocsIntegration(args.tools_dir)
        
        if args.command == "audit":
            result = integration.audit(
                output_format=args.format,
                save_report=args.save_report,
                fix_duplicates=not args.no_fix_duplicates
            )
            if args.format == "json":
                print(json.dumps(result, indent=2))
        
        elif args.command == "build":
            result = integration.build(
                skip_audit=args.skip_audit,
                skip_diagrams=args.skip_diagrams,
                skip_fixes=args.skip_fixes,
                skip_validation=args.skip_validation
            )
            print(result["output"])
        
        elif args.command == "status":
            result = integration.status(detailed=args.detailed)
            print(result["output"])
        
        elif args.command == "health":
            score = integration.get_health_score()
            is_healthy = integration.is_healthy(args.threshold)
            
            print(f"Documentation Health Score: {score:.1f}/100")
            print(f"Threshold: {args.threshold}")
            print(f"Status: {'✅ HEALTHY' if is_healthy else '❌ NEEDS ATTENTION'}")
            
            if not is_healthy:
                sys.exit(1)
        
        elif args.command == "info":
            result = integration.info()
            print(result["output"])
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()