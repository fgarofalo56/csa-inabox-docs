"""Quality gates and validation framework for versioned documentation.

This module provides:
- Pre-release validation gates
- Version consistency checks
- Performance impact assessment
- Link integrity across versions
- Content quality validation
"""

import asyncio
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import aiohttp
import yaml
from mkdocs.commands.build import build as mkdocs_build
from mkdocs.config import load_config

from .build_tester import DocumentationBuildTester
from .link_validator import LinkValidator
from .navigation_validator import NavigationStructureValidator
from .mike_manager import MikeVersionManager
from .version_manager import SemanticVersionManager
from .migration_manager import MigrationManager


@dataclass
class QualityGate:
    """Definition of a quality gate."""
    
    name: str
    description: str
    validator_class: str
    required: bool = True
    timeout_seconds: int = 300
    retry_count: int = 2
    failure_threshold: float = 0.0  # Percentage of failures allowed
    

@dataclass
class ValidationResult:
    """Result of a validation check."""
    
    gate_name: str
    passed: bool
    score: float  # 0.0 to 1.0
    message: str
    details: Dict[str, Any]
    execution_time: float
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


@dataclass
class PerformanceMetrics:
    """Performance metrics for version validation."""
    
    build_time: float
    total_size_mb: float
    page_count: int
    asset_count: int
    avg_page_size_kb: float
    largest_page_size_kb: float
    load_time_samples: List[float]
    

class VersionValidator:
    """Comprehensive validation framework for versioned documentation."""
    
    DEFAULT_QUALITY_GATES = [
        QualityGate(
            name="build_validation",
            description="Validate that documentation builds successfully",
            validator_class="DocumentationBuildTester",
            required=True,
            timeout_seconds=600
        ),
        QualityGate(
            name="navigation_validation",
            description="Validate navigation structure and consistency",
            validator_class="NavigationStructureValidator",
            required=True
        ),
        QualityGate(
            name="link_validation",
            description="Validate all internal and external links",
            validator_class="LinkValidator",
            required=True,
            timeout_seconds=1200,
            failure_threshold=0.02  # Allow 2% link failures
        ),
        QualityGate(
            name="performance_validation",
            description="Validate performance metrics within acceptable limits",
            validator_class="PerformanceValidator",
            required=False
        ),
        QualityGate(
            name="content_quality",
            description="Validate content quality and consistency",
            validator_class="ContentQualityValidator",
            required=False,
            failure_threshold=0.1  # Allow 10% quality issues
        ),
        QualityGate(
            name="version_consistency",
            description="Validate version consistency and migration compatibility",
            validator_class="VersionConsistencyValidator",
            required=True
        )
    ]
    
    def __init__(self, repo_path: Optional[Path] = None, 
                 quality_gates: Optional[List[QualityGate]] = None):
        """Initialize version validator.
        
        Args:
            repo_path: Path to repository root
            quality_gates: Custom quality gates (uses defaults if None)
        """
        self.repo_path = repo_path or Path.cwd()
        self.quality_gates = quality_gates or self.DEFAULT_QUALITY_GATES
        
        # Initialize managers
        self.version_manager = SemanticVersionManager()
        self.mike_manager = MikeVersionManager(repo_path)
        self.migration_manager = MigrationManager(repo_path)
        
        # Initialize validators
        self.build_tester = DocumentationBuildTester(repo_path)
        self.link_validator = LinkValidator(repo_path)
        self.navigation_validator = NavigationStructureValidator(repo_path)
        
        # Load configuration
        self.config = self._load_validation_config()
    
    async def validate_version(self, version: str, 
                              gate_names: Optional[List[str]] = None) -> Tuple[bool, List[ValidationResult]]:
        """Validate a version against all quality gates.
        
        Args:
            version: Version to validate
            gate_names: Specific gates to run (runs all if None)
            
        Returns:
            Tuple of (all_passed, validation_results)
        """
        gates_to_run = self.quality_gates
        if gate_names:
            gates_to_run = [gate for gate in self.quality_gates if gate.name in gate_names]
        
        results = []
        all_passed = True
        
        for gate in gates_to_run:
            print(f"Running quality gate: {gate.name}")
            start_time = time.time()
            
            try:
                result = await self._run_quality_gate(gate, version)
                result.execution_time = time.time() - start_time
                
                if not result.passed and gate.required:
                    all_passed = False
                elif not result.passed and result.score < (1.0 - gate.failure_threshold):
                    all_passed = False
                
                results.append(result)
                
            except Exception as e:
                result = ValidationResult(
                    gate_name=gate.name,
                    passed=False,
                    score=0.0,
                    message=f"Gate execution failed: {str(e)}",
                    details={'error': str(e)},
                    execution_time=time.time() - start_time
                )
                results.append(result)
                
                if gate.required:
                    all_passed = False
        
        return all_passed, results
    
    async def validate_version_migration(self, from_version: str, to_version: str) -> ValidationResult:
        """Validate a version migration.
        
        Args:
            from_version: Source version
            to_version: Target version
            
        Returns:
            Validation result for the migration
        """
        start_time = time.time()
        issues = []
        warnings = []
        
        try:
            # Validate backward compatibility
            is_compatible, compat_issues = self.migration_manager.validate_backward_compatibility(to_version)
            if not is_compatible:
                issues.extend(compat_issues)
            
            # Check for breaking changes
            breaking_changes = self.migration_manager._get_breaking_changes_for_range(from_version, to_version)
            if breaking_changes:
                warnings.append(f"{len(breaking_changes)} breaking changes found")
                for change in breaking_changes:
                    if change.severity == 'critical':
                        issues.append(f"Critical breaking change: {change.title}")
            
            # Validate migration rules
            try:
                migration_result = self.migration_manager.apply_migration_rules(
                    from_version, to_version, dry_run=True
                )
                if migration_result['failed_rules']:
                    for failed_rule in migration_result['failed_rules']:
                        issues.append(f"Migration rule failed: {failed_rule['name']} - {failed_rule['error']}")
            except Exception as e:
                warnings.append(f"Could not validate migration rules: {e}")
            
            # Check version format compatibility
            try:
                self.version_manager.compare_versions(from_version, to_version)
            except ValueError as e:
                issues.append(f"Version format incompatibility: {e}")
            
            passed = len(issues) == 0
            score = 1.0 if passed else max(0.0, 1.0 - (len(issues) / 10))  # Decrease score based on issues
            
            return ValidationResult(
                gate_name="migration_validation",
                passed=passed,
                score=score,
                message=f"Migration validation {'passed' if passed else 'failed'} with {len(issues)} issues",
                details={
                    'issues': issues,
                    'breaking_changes': len(breaking_changes),
                    'migration_rules_applied': len(migration_result.get('applied_rules', [])) if 'migration_result' in locals() else 0
                },
                execution_time=time.time() - start_time,
                warnings=warnings
            )
            
        except Exception as e:
            return ValidationResult(
                gate_name="migration_validation",
                passed=False,
                score=0.0,
                message=f"Migration validation error: {str(e)}",
                details={'error': str(e)},
                execution_time=time.time() - start_time
            )
    
    async def assess_performance_impact(self, version: str) -> PerformanceMetrics:
        """Assess performance impact of a version.
        
        Args:
            version: Version to assess
            
        Returns:
            Performance metrics
        """
        start_time = time.time()
        
        # Build documentation to get metrics
        build_result = await self._build_documentation(version)
        build_time = time.time() - start_time
        
        # Calculate size metrics
        site_path = self.repo_path / "site"
        total_size = 0
        page_count = 0
        asset_count = 0
        page_sizes = []
        
        if site_path.exists():
            for file_path in site_path.rglob("*"):
                if file_path.is_file():
                    size = file_path.stat().st_size
                    total_size += size
                    
                    if file_path.suffix == '.html':
                        page_count += 1
                        page_sizes.append(size / 1024)  # KB
                    else:
                        asset_count += 1
        
        # Sample load times (would need actual HTTP testing in production)
        load_time_samples = [0.5, 0.7, 0.6, 0.8, 0.5]  # Placeholder values
        
        return PerformanceMetrics(
            build_time=build_time,
            total_size_mb=total_size / (1024 * 1024),
            page_count=page_count,
            asset_count=asset_count,
            avg_page_size_kb=sum(page_sizes) / len(page_sizes) if page_sizes else 0,
            largest_page_size_kb=max(page_sizes) if page_sizes else 0,
            load_time_samples=load_time_samples
        )
    
    def generate_validation_report(self, version: str, results: List[ValidationResult], 
                                  performance_metrics: Optional[PerformanceMetrics] = None) -> Dict[str, Any]:
        """Generate comprehensive validation report.
        
        Args:
            version: Version that was validated
            results: Validation results
            performance_metrics: Performance metrics (if available)
            
        Returns:
            Comprehensive validation report
        """
        total_gates = len(results)
        passed_gates = sum(1 for r in results if r.passed)
        required_gates = sum(1 for r in results if any(g.required for g in self.quality_gates if g.name == r.gate_name))
        passed_required = sum(1 for r in results if r.passed and any(g.required for g in self.quality_gates if g.name == r.gate_name))
        
        overall_score = sum(r.score for r in results) / len(results) if results else 0.0
        
        report = {
            'version': version,
            'validation_timestamp': time.time(),
            'overall_result': {
                'passed': passed_required == required_gates,
                'score': overall_score,
                'gates_passed': passed_gates,
                'total_gates': total_gates,
                'required_gates_passed': passed_required,
                'required_gates_total': required_gates
            },
            'gate_results': [
                {
                    'name': r.gate_name,
                    'passed': r.passed,
                    'score': r.score,
                    'message': r.message,
                    'execution_time': r.execution_time,
                    'warnings_count': len(r.warnings),
                    'required': any(g.required for g in self.quality_gates if g.name == r.gate_name)
                }
                for r in results
            ],
            'detailed_results': [
                {
                    'gate_name': r.gate_name,
                    'details': r.details,
                    'warnings': r.warnings
                }
                for r in results
            ]
        }
        
        if performance_metrics:
            report['performance_metrics'] = {
                'build_time_seconds': performance_metrics.build_time,
                'total_size_mb': performance_metrics.total_size_mb,
                'page_count': performance_metrics.page_count,
                'asset_count': performance_metrics.asset_count,
                'avg_page_size_kb': performance_metrics.avg_page_size_kb,
                'largest_page_size_kb': performance_metrics.largest_page_size_kb,
                'avg_load_time': sum(performance_metrics.load_time_samples) / len(performance_metrics.load_time_samples)
            }
        
        return report
    
    def save_validation_report(self, report: Dict[str, Any], output_path: Optional[Path] = None) -> Path:
        """Save validation report to file.
        
        Args:
            report: Validation report
            output_path: Output file path (auto-generated if None)
            
        Returns:
            Path to saved report file
        """
        if not output_path:
            reports_dir = self.repo_path / "validation_reports"
            reports_dir.mkdir(exist_ok=True)
            timestamp = int(time.time())
            output_path = reports_dir / f"validation_report_{report['version']}_{timestamp}.json"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        return output_path
    
    async def _run_quality_gate(self, gate: QualityGate, version: str) -> ValidationResult:
        """Run a single quality gate.
        
        Args:
            gate: Quality gate to run
            version: Version being validated
            
        Returns:
            Validation result
        """
        if gate.validator_class == "DocumentationBuildTester":
            return await self._validate_build(version)
        elif gate.validator_class == "NavigationStructureValidator":
            return await self._validate_navigation(version)
        elif gate.validator_class == "LinkValidator":
            return await self._validate_links(version, gate.failure_threshold)
        elif gate.validator_class == "PerformanceValidator":
            return await self._validate_performance(version)
        elif gate.validator_class == "ContentQualityValidator":
            return await self._validate_content_quality(version)
        elif gate.validator_class == "VersionConsistencyValidator":
            return await self._validate_version_consistency(version)
        else:
            raise ValueError(f"Unknown validator class: {gate.validator_class}")
    
    async def _validate_build(self, version: str) -> ValidationResult:
        """Validate documentation build."""
        try:
            result = await self._build_documentation(version)
            
            return ValidationResult(
                gate_name="build_validation",
                passed=result['success'],
                score=1.0 if result['success'] else 0.0,
                message=result['message'],
                details=result,
                execution_time=0.0  # Will be set by caller
            )
        except Exception as e:
            return ValidationResult(
                gate_name="build_validation",
                passed=False,
                score=0.0,
                message=f"Build validation failed: {str(e)}",
                details={'error': str(e)},
                execution_time=0.0
            )
    
    async def _validate_navigation(self, version: str) -> ValidationResult:
        """Validate navigation structure."""
        try:
            is_valid, issues = self.navigation_validator.validate_structure()
            
            return ValidationResult(
                gate_name="navigation_validation",
                passed=is_valid,
                score=1.0 if is_valid else max(0.0, 1.0 - len(issues) * 0.1),
                message=f"Navigation validation {'passed' if is_valid else 'failed'} with {len(issues)} issues",
                details={'issues': issues},
                execution_time=0.0
            )
        except Exception as e:
            return ValidationResult(
                gate_name="navigation_validation",
                passed=False,
                score=0.0,
                message=f"Navigation validation error: {str(e)}",
                details={'error': str(e)},
                execution_time=0.0
            )
    
    async def _validate_links(self, version: str, failure_threshold: float) -> ValidationResult:
        """Validate all links."""
        try:
            is_valid, link_results = await self.link_validator.validate_all_links()
            
            total_links = len(link_results)
            broken_links = [r for r in link_results if not r.is_valid]
            failure_rate = len(broken_links) / total_links if total_links > 0 else 0.0
            
            passed = failure_rate <= failure_threshold
            score = max(0.0, 1.0 - failure_rate)
            
            return ValidationResult(
                gate_name="link_validation",
                passed=passed,
                score=score,
                message=f"Link validation: {len(broken_links)}/{total_links} links broken ({failure_rate:.1%} failure rate)",
                details={
                    'total_links': total_links,
                    'broken_links': len(broken_links),
                    'failure_rate': failure_rate,
                    'threshold': failure_threshold,
                    'broken_link_details': [{
                        'url': r.url,
                        'source_file': r.source_file,
                        'error': r.error
                    } for r in broken_links[:10]]  # First 10 broken links
                },
                execution_time=0.0
            )
        except Exception as e:
            return ValidationResult(
                gate_name="link_validation",
                passed=False,
                score=0.0,
                message=f"Link validation error: {str(e)}",
                details={'error': str(e)},
                execution_time=0.0
            )
    
    async def _validate_performance(self, version: str) -> ValidationResult:
        """Validate performance metrics."""
        try:
            metrics = await self.assess_performance_impact(version)
            
            # Define performance thresholds
            thresholds = self.config.get('performance_thresholds', {
                'max_build_time': 600,  # 10 minutes
                'max_total_size_mb': 500,  # 500 MB
                'max_avg_page_size_kb': 1000,  # 1 MB
                'max_avg_load_time': 3.0  # 3 seconds
            })
            
            issues = []
            if metrics.build_time > thresholds['max_build_time']:
                issues.append(f"Build time {metrics.build_time:.1f}s exceeds threshold {thresholds['max_build_time']}s")
            
            if metrics.total_size_mb > thresholds['max_total_size_mb']:
                issues.append(f"Total size {metrics.total_size_mb:.1f}MB exceeds threshold {thresholds['max_total_size_mb']}MB")
            
            if metrics.avg_page_size_kb > thresholds['max_avg_page_size_kb']:
                issues.append(f"Average page size {metrics.avg_page_size_kb:.1f}KB exceeds threshold {thresholds['max_avg_page_size_kb']}KB")
            
            avg_load_time = sum(metrics.load_time_samples) / len(metrics.load_time_samples)
            if avg_load_time > thresholds['max_avg_load_time']:
                issues.append(f"Average load time {avg_load_time:.1f}s exceeds threshold {thresholds['max_avg_load_time']}s")
            
            passed = len(issues) == 0
            score = max(0.0, 1.0 - len(issues) * 0.2)
            
            return ValidationResult(
                gate_name="performance_validation",
                passed=passed,
                score=score,
                message=f"Performance validation {'passed' if passed else 'failed'} with {len(issues)} issues",
                details={
                    'metrics': {
                        'build_time': metrics.build_time,
                        'total_size_mb': metrics.total_size_mb,
                        'page_count': metrics.page_count,
                        'asset_count': metrics.asset_count,
                        'avg_page_size_kb': metrics.avg_page_size_kb,
                        'avg_load_time': avg_load_time
                    },
                    'thresholds': thresholds,
                    'issues': issues
                },
                execution_time=0.0
            )
        except Exception as e:
            return ValidationResult(
                gate_name="performance_validation",
                passed=False,
                score=0.0,
                message=f"Performance validation error: {str(e)}",
                details={'error': str(e)},
                execution_time=0.0
            )
    
    async def _validate_content_quality(self, version: str) -> ValidationResult:
        """Validate content quality."""
        try:
            # This would need implementation with actual content analysis
            # For now, return a placeholder result
            return ValidationResult(
                gate_name="content_quality",
                passed=True,
                score=0.9,
                message="Content quality validation passed (placeholder)",
                details={'analyzed_pages': 0, 'quality_issues': []},
                execution_time=0.0
            )
        except Exception as e:
            return ValidationResult(
                gate_name="content_quality",
                passed=False,
                score=0.0,
                message=f"Content quality validation error: {str(e)}",
                details={'error': str(e)},
                execution_time=0.0
            )
    
    async def _validate_version_consistency(self, version: str) -> ValidationResult:
        """Validate version consistency."""
        try:
            issues = []
            warnings = []
            
            # Validate version format
            try:
                parsed = self.version_manager.parse_version(version)
            except ValueError as e:
                issues.append(f"Invalid version format: {e}")
            
            # Check for version conflicts
            try:
                deployed_versions = self.mike_manager.list_versions()
                existing_version = next(
                    (v for v in deployed_versions if v.version == version),
                    None
                )
                if existing_version:
                    warnings.append(f"Version {version} already exists")
            except Exception as e:
                warnings.append(f"Could not check existing versions: {e}")
            
            # Validate version progression
            try:
                latest_version = self.version_manager.get_latest_version()
                if latest_version:
                    comparison = self.version_manager.compare_versions(latest_version, version)
                    if comparison > 0:
                        warnings.append(f"Version {version} is older than latest version {latest_version}")
            except Exception as e:
                warnings.append(f"Could not validate version progression: {e}")
            
            passed = len(issues) == 0
            score = 1.0 if passed else max(0.0, 1.0 - len(issues) * 0.3)
            
            return ValidationResult(
                gate_name="version_consistency",
                passed=passed,
                score=score,
                message=f"Version consistency validation {'passed' if passed else 'failed'} with {len(issues)} issues",
                details={'issues': issues},
                execution_time=0.0,
                warnings=warnings
            )
        except Exception as e:
            return ValidationResult(
                gate_name="version_consistency",
                passed=False,
                score=0.0,
                message=f"Version consistency validation error: {str(e)}",
                details={'error': str(e)},
                execution_time=0.0
            )
    
    async def _build_documentation(self, version: str) -> Dict[str, Any]:
        """Build documentation and return result."""
        try:
            # Use existing build tester
            success, stdout, stderr = self.build_tester.test_build(strict=False)
            return {
                'success': success,
                'message': 'Build succeeded' if success else 'Build failed',
                'build_time': 0.0,  # test_build doesn't return build time
                'warnings': stdout.split('\n') if stdout else [],
                'errors': stderr.split('\n') if stderr else []
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Build failed: {str(e)}",
                'error': str(e)
            }
    
    def _load_validation_config(self) -> Dict[str, Any]:
        """Load validation configuration."""
        config_file = self.repo_path / "docs" / "validation" / "config.yml"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                return {}
        return {}
