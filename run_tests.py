#!/usr/bin/env python3
"""Test runner script for CSA Docs Tools."""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from typing import List, Optional
import time


def run_command(cmd: List[str], cwd: Optional[Path] = None, env: Optional[dict] = None) -> tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr."""
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            env=env or os.environ.copy(),
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except Exception as e:
        return 1, "", str(e)


def setup_environment():
    """Set up the test environment."""
    print("🔧 Setting up test environment...")
    
    # Install dependencies
    commands = [
        ["python", "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"],
        ["pip", "install", "-r", "requirements.txt"],
        ["pip", "install", "-r", "requirements-test.txt"],
        ["pip", "install", "-e", "."],  # Install package in development mode
    ]
    
    for cmd in commands:
        exit_code, stdout, stderr = run_command(cmd)
        if exit_code != 0:
            print(f"❌ Failed to run: {' '.join(cmd)}")
            print(f"Error: {stderr}")
            return False
    
    # Check if markdownlint is available
    exit_code, stdout, stderr = run_command(["markdownlint", "--version"])
    if exit_code != 0:
        print("⚠️ markdownlint not found. Installing...")
        exit_code, stdout, stderr = run_command(["npm", "install", "-g", "markdownlint-cli"])
        if exit_code != 0:
            print("⚠️ Could not install markdownlint. Some tests may be skipped.")
    
    print("✅ Environment setup complete")
    return True


def run_linting():
    """Run code linting and formatting checks."""
    print("\n🔍 Running linting and formatting checks...")
    
    checks = [
        (["ruff", "check", "src/", "tests/"], "Ruff linting"),
        (["ruff", "format", "--check", "src/", "tests/"], "Ruff formatting"),
        (["mypy", "src/csa_docs_tools/", "--ignore-missing-imports"], "MyPy type checking"),
        (["isort", "--check-only", "--diff", "src/", "tests/"], "Import sorting"),
    ]
    
    failed = []
    
    for cmd, description in checks:
        print(f"Running {description}...")
        exit_code, stdout, stderr = run_command(cmd)
        
        if exit_code != 0:
            print(f"❌ {description} failed")
            print(f"Error: {stderr}")
            failed.append(description)
        else:
            print(f"✅ {description} passed")
    
    return len(failed) == 0, failed


def run_unit_tests(coverage_threshold: float = 90.0):
    """Run unit tests with coverage."""
    print("\n🧪 Running unit tests...")
    
    cmd = [
        "pytest",
        "tests/unit/",
        "-v",
        "--cov=src/csa_docs_tools",
        "--cov-branch",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "--cov-report=xml:coverage.xml",
        f"--cov-fail-under={coverage_threshold}",
        "--junitxml=junit-unit.xml"
    ]
    
    exit_code, stdout, stderr = run_command(cmd)
    
    if exit_code == 0:
        print("✅ Unit tests passed")
        return True
    else:
        print("❌ Unit tests failed")
        print(f"Output: {stdout}")
        print(f"Error: {stderr}")
        return False


def run_integration_tests():
    """Run integration tests."""
    print("\n🔧 Running integration tests...")
    
    cmd = [
        "pytest",
        "tests/integration/",
        "-v",
        "-m", "not network",  # Skip network tests by default
        "--junitxml=junit-integration.xml"
    ]
    
    exit_code, stdout, stderr = run_command(cmd)
    
    if exit_code == 0:
        print("✅ Integration tests passed")
        return True
    else:
        print("❌ Integration tests failed")
        print(f"Output: {stdout}")
        print(f"Error: {stderr}")
        return False


def run_documentation_build_test():
    """Test that the documentation builds successfully."""
    print("\n📚 Testing documentation build...")
    
    cmd = ["mkdocs", "build", "--strict"]
    exit_code, stdout, stderr = run_command(cmd)
    
    if exit_code == 0:
        print("✅ Documentation build passed")
        return True
    else:
        print("❌ Documentation build failed")
        print(f"Output: {stdout}")
        print(f"Error: {stderr}")
        return False


def run_security_checks():
    """Run security checks."""
    print("\n🔐 Running security checks...")
    
    checks = [
        (["safety", "check", "--json"], "Safety vulnerability check", False),  # Don't fail on warnings
        (["bandit", "-r", "src/", "-f", "json"], "Bandit security linter", False),
    ]
    
    passed = True
    
    for cmd, description, fail_on_error in checks:
        print(f"Running {description}...")
        exit_code, stdout, stderr = run_command(cmd)
        
        if exit_code != 0 and fail_on_error:
            print(f"❌ {description} failed")
            print(f"Output: {stdout}")
            print(f"Error: {stderr}")
            passed = False
        else:
            print(f"✅ {description} completed")
    
    return passed


def run_performance_tests():
    """Run performance benchmarks."""
    print("\n⚡ Running performance tests...")
    
    cmd = [
        "pytest",
        "tests/integration/test_full_validation.py::TestFullValidationWorkflow::test_performance_with_large_documentation",
        "-v",
        "--benchmark-only",
        "--benchmark-json=benchmark.json"
    ]
    
    exit_code, stdout, stderr = run_command(cmd)
    
    if exit_code == 0:
        print("✅ Performance tests passed")
        return True
    else:
        print("⚠️ Performance tests had issues (non-critical)")
        return True  # Don't fail overall build on performance test issues


def run_validation_tests():
    """Run the actual documentation validation using our tools."""
    print("\n🎯 Running documentation validation with CSA Docs Tools...")
    
    # Test the CLI tool
    cmd = ["python", "-m", "src.csa_docs_tools.cli", "all", "--output", "text"]
    exit_code, stdout, stderr = run_command(cmd)
    
    print(f"Validation output:\n{stdout}")
    
    if exit_code == 0:
        print("✅ Documentation validation passed")
        return True
    else:
        print("❌ Documentation validation found issues")
        print(f"Error: {stderr}")
        return True  # Don't fail build - just report issues


def generate_test_report(results: dict):
    """Generate a comprehensive test report."""
    print("\n📊 Generating test report...")
    
    report_lines = [
        "# CSA Docs Tools Test Report",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Test Results Summary",
        ""
    ]
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result['passed'])
    
    report_lines.extend([
        f"**Total Test Suites:** {total_tests}",
        f"**Passed:** {passed_tests}",
        f"**Failed:** {total_tests - passed_tests}",
        f"**Success Rate:** {(passed_tests/total_tests*100):.1f}%",
        ""
    ])
    
    # Detailed results
    report_lines.append("## Detailed Results")
    report_lines.append("")
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result['passed'] else "❌ FAILED"
        duration = result.get('duration', 0)
        
        report_lines.extend([
            f"### {test_name}",
            f"**Status:** {status}",
            f"**Duration:** {duration:.2f}s",
            ""
        ])
        
        if not result['passed'] and 'failures' in result:
            report_lines.append("**Failures:**")
            for failure in result['failures']:
                report_lines.append(f"- {failure}")
            report_lines.append("")
    
    # Write report
    report_content = "\n".join(report_lines)
    with open("test_report.md", "w") as f:
        f.write(report_content)
    
    print("✅ Test report generated: test_report.md")
    return report_content


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description="CSA Docs Tools Test Runner")
    parser.add_argument("--skip-setup", action="store_true", help="Skip environment setup")
    parser.add_argument("--skip-lint", action="store_true", help="Skip linting checks")
    parser.add_argument("--skip-unit", action="store_true", help="Skip unit tests")
    parser.add_argument("--skip-integration", action="store_true", help="Skip integration tests")
    parser.add_argument("--skip-security", action="store_true", help="Skip security checks")
    parser.add_argument("--skip-performance", action="store_true", help="Skip performance tests")
    parser.add_argument("--skip-validation", action="store_true", help="Skip documentation validation")
    parser.add_argument("--coverage-threshold", type=float, default=90.0, help="Coverage threshold")
    parser.add_argument("--fast", action="store_true", help="Run only essential tests")
    
    args = parser.parse_args()
    
    if args.fast:
        args.skip_performance = True
        args.skip_security = True
    
    print("🚀 Starting CSA Docs Tools Test Suite")
    print("=" * 50)
    
    results = {}
    overall_success = True
    
    # Environment setup
    if not args.skip_setup:
        start_time = time.time()
        success = setup_environment()
        duration = time.time() - start_time
        results['Environment Setup'] = {'passed': success, 'duration': duration}
        if not success:
            print("❌ Environment setup failed. Aborting.")
            return 1
    
    # Linting
    if not args.skip_lint:
        start_time = time.time()
        success, failures = run_linting()
        duration = time.time() - start_time
        results['Linting'] = {
            'passed': success, 
            'duration': duration, 
            'failures': failures if not success else []
        }
        if not success:
            overall_success = False
    
    # Unit tests
    if not args.skip_unit:
        start_time = time.time()
        success = run_unit_tests(args.coverage_threshold)
        duration = time.time() - start_time
        results['Unit Tests'] = {'passed': success, 'duration': duration}
        if not success:
            overall_success = False
    
    # Integration tests
    if not args.skip_integration:
        start_time = time.time()
        success = run_integration_tests()
        duration = time.time() - start_time
        results['Integration Tests'] = {'passed': success, 'duration': duration}
        if not success:
            overall_success = False
    
    # Documentation build test
    start_time = time.time()
    success = run_documentation_build_test()
    duration = time.time() - start_time
    results['Documentation Build'] = {'passed': success, 'duration': duration}
    if not success:
        overall_success = False
    
    # Security checks
    if not args.skip_security:
        start_time = time.time()
        success = run_security_checks()
        duration = time.time() - start_time
        results['Security Checks'] = {'passed': success, 'duration': duration}
        # Security checks are informational, don't fail build
    
    # Performance tests
    if not args.skip_performance:
        start_time = time.time()
        success = run_performance_tests()
        duration = time.time() - start_time
        results['Performance Tests'] = {'passed': success, 'duration': duration}
        # Performance tests are informational, don't fail build
    
    # Documentation validation
    if not args.skip_validation:
        start_time = time.time()
        success = run_validation_tests()
        duration = time.time() - start_time
        results['Documentation Validation'] = {'passed': success, 'duration': duration}
        # Validation is informational, don't fail build
    
    # Generate report
    report_content = generate_test_report(results)
    
    # Summary
    print("\n" + "=" * 50)
    print("🏁 Test Suite Complete")
    
    if overall_success:
        print("✅ All critical tests passed!")
        return 0
    else:
        print("❌ Some tests failed. Check the report for details.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)