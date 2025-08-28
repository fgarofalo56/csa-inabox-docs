"""Tests for version validation framework."""

import asyncio
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock, MagicMock

from src.csa_docs_tools.version_validator import (
    VersionValidator,
    QualityGate,
    ValidationResult,
    PerformanceMetrics
)


class TestQualityGate:
    """Test cases for QualityGate dataclass."""
    
    def test_default_quality_gate(self):
        """Test creating quality gate with default values."""
        gate = QualityGate(
            name="test_gate",
            description="Test gate",
            validator_class="TestValidator"
        )
        
        assert gate.name == "test_gate"
        assert gate.description == "Test gate"
        assert gate.validator_class == "TestValidator"
        assert gate.required
        assert gate.timeout_seconds == 300
        assert gate.retry_count == 2
        assert gate.failure_threshold == 0.0
    
    def test_custom_quality_gate(self):
        """Test creating quality gate with custom values."""
        gate = QualityGate(
            name="performance_gate",
            description="Performance validation",
            validator_class="PerformanceValidator",
            required=False,
            timeout_seconds=600,
            failure_threshold=0.1
        )
        
        assert not gate.required
        assert gate.timeout_seconds == 600
        assert gate.failure_threshold == 0.1


class TestValidationResult:
    """Test cases for ValidationResult dataclass."""
    
    def test_validation_result_creation(self):
        """Test creating validation result."""
        result = ValidationResult(
            gate_name="test_gate",
            passed=True,
            score=0.95,
            message="Test passed",
            details={"test": "data"},
            execution_time=1.5
        )
        
        assert result.gate_name == "test_gate"
        assert result.passed
        assert result.score == 0.95
        assert result.message == "Test passed"
        assert result.details == {"test": "data"}
        assert result.execution_time == 1.5
        assert result.warnings == []  # Default empty list
    
    def test_validation_result_with_warnings(self):
        """Test creating validation result with warnings."""
        warnings = ["Warning 1", "Warning 2"]
        result = ValidationResult(
            gate_name="test_gate",
            passed=True,
            score=0.8,
            message="Test passed with warnings",
            details={},
            execution_time=2.0,
            warnings=warnings
        )
        
        assert result.warnings == warnings
        assert len(result.warnings) == 2


class TestPerformanceMetrics:
    """Test cases for PerformanceMetrics dataclass."""
    
    def test_performance_metrics_creation(self):
        """Test creating performance metrics."""
        metrics = PerformanceMetrics(
            build_time=120.5,
            total_size_mb=45.2,
            page_count=150,
            asset_count=75,
            avg_page_size_kb=32.1,
            largest_page_size_kb=128.5,
            load_time_samples=[0.5, 0.7, 0.6, 0.8]
        )
        
        assert metrics.build_time == 120.5
        assert metrics.total_size_mb == 45.2
        assert metrics.page_count == 150
        assert metrics.asset_count == 75
        assert metrics.avg_page_size_kb == 32.1
        assert metrics.largest_page_size_kb == 128.5
        assert len(metrics.load_time_samples) == 4


class TestVersionValidator:
    """Test cases for VersionValidator."""
    
    @pytest.fixture
    def version_validator(self, tmp_path):
        """Create VersionValidator instance for testing."""
        return VersionValidator(repo_path=tmp_path)
    
    @pytest.fixture
    def mock_validators(self):
        """Mock all validator dependencies."""
        with patch.multiple(
            'src.csa_docs_tools.version_validator',
            DocumentationBuilder=MagicMock(),
            LinkValidator=MagicMock(),
            NavigationValidator=MagicMock(),
            SemanticVersionManager=MagicMock(),
            MikeVersionManager=MagicMock(),
            MigrationManager=MagicMock()
        ) as mocks:
            yield mocks
    
    def test_default_quality_gates(self, version_validator):
        """Test that default quality gates are loaded."""
        assert len(version_validator.quality_gates) == 6
        
        gate_names = [gate.name for gate in version_validator.quality_gates]
        expected_gates = [
            "build_validation",
            "navigation_validation", 
            "link_validation",
            "performance_validation",
            "content_quality",
            "version_consistency"
        ]
        
        for expected_gate in expected_gates:
            assert expected_gate in gate_names
    
    def test_custom_quality_gates(self, tmp_path):
        """Test using custom quality gates."""
        custom_gates = [
            QualityGate(
                name="custom_gate",
                description="Custom validation",
                validator_class="CustomValidator"
            )
        ]
        
        validator = VersionValidator(repo_path=tmp_path, quality_gates=custom_gates)
        
        assert len(validator.quality_gates) == 1
        assert validator.quality_gates[0].name == "custom_gate"
    
    @pytest.mark.asyncio
    async def test_validate_build_success(self, version_validator, mock_validators):
        """Test successful build validation."""
        # Mock build result
        mock_build_result = {
            'success': True,
            'message': 'Build completed successfully',
            'build_time': 30.5,
            'warnings': [],
            'errors': []
        }
        
        with patch.object(version_validator, '_build_documentation', return_value=mock_build_result):
            result = await version_validator._validate_build("1.0.0")
        
        assert result.gate_name == "build_validation"
        assert result.passed
        assert result.score == 1.0
        assert "Build completed successfully" in result.message
    
    @pytest.mark.asyncio
    async def test_validate_build_failure(self, version_validator, mock_validators):
        """Test build validation failure."""
        mock_build_result = {
            'success': False,
            'message': 'Build failed with errors',
            'errors': ['Missing file: index.md']
        }
        
        with patch.object(version_validator, '_build_documentation', return_value=mock_build_result):
            result = await version_validator._validate_build("1.0.0")
        
        assert result.gate_name == "build_validation"
        assert not result.passed
        assert result.score == 0.0
        assert "Build failed with errors" in result.message
    
    @pytest.mark.asyncio
    async def test_validate_navigation_success(self, version_validator, mock_validators):
        """Test successful navigation validation."""
        version_validator.navigation_validator.validate_structure.return_value = (True, [])
        
        result = await version_validator._validate_navigation("1.0.0")
        
        assert result.gate_name == "navigation_validation"
        assert result.passed
        assert result.score == 1.0
        assert result.details['issues'] == []
    
    @pytest.mark.asyncio
    async def test_validate_navigation_issues(self, version_validator, mock_validators):
        """Test navigation validation with issues."""
        issues = ["Broken link in navigation", "Missing page reference"]
        version_validator.navigation_validator.validate_structure.return_value = (False, issues)
        
        result = await version_validator._validate_navigation("1.0.0")
        
        assert result.gate_name == "navigation_validation"
        assert not result.passed
        assert result.score == 0.8  # 1.0 - (2 issues * 0.1)
        assert result.details['issues'] == issues
    
    @pytest.mark.asyncio
    async def test_validate_links_success(self, version_validator, mock_validators):
        """Test successful link validation."""
        # Mock all links as valid
        mock_link_results = [
            Mock(is_valid=True, url="https://example.com"),
            Mock(is_valid=True, url="internal-link.html"),
            Mock(is_valid=True, url="another-page.html")
        ]
        
        version_validator.link_validator.validate_all_links = AsyncMock(
            return_value=(True, mock_link_results)
        )
        
        result = await version_validator._validate_links("1.0.0", 0.05)  # 5% threshold
        
        assert result.gate_name == "link_validation"
        assert result.passed
        assert result.score == 1.0
        assert result.details['total_links'] == 3
        assert result.details['broken_links'] == 0
        assert result.details['failure_rate'] == 0.0
    
    @pytest.mark.asyncio
    async def test_validate_links_with_failures(self, version_validator, mock_validators):
        """Test link validation with some failures."""
        # Mock some broken links
        mock_link_results = [
            Mock(is_valid=True, url="https://example.com"),
            Mock(is_valid=False, url="broken-link.html", error="404 Not Found"),
            Mock(is_valid=False, url="another-broken-link.html", error="Connection timeout"),
            Mock(is_valid=True, url="working-link.html")
        ]
        
        version_validator.link_validator.validate_all_links = AsyncMock(
            return_value=(False, mock_link_results)
        )
        
        result = await version_validator._validate_links("1.0.0", 0.1)  # 10% threshold
        
        assert result.gate_name == "link_validation"
        assert not result.passed  # 50% failure rate > 10% threshold
        assert result.score == 0.5  # 1.0 - 0.5 failure rate
        assert result.details['total_links'] == 4
        assert result.details['broken_links'] == 2
        assert result.details['failure_rate'] == 0.5
    
    @pytest.mark.asyncio
    async def test_validate_links_within_threshold(self, version_validator, mock_validators):
        """Test link validation with failures within acceptable threshold."""
        # Mock minimal failures
        mock_link_results = [
            Mock(is_valid=True, url="link1.html"),
            Mock(is_valid=True, url="link2.html"),
            Mock(is_valid=True, url="link3.html"),
            Mock(is_valid=True, url="link4.html"),
            Mock(is_valid=False, url="broken-link.html", error="404 Not Found")
        ]
        
        version_validator.link_validator.validate_all_links = AsyncMock(
            return_value=(False, mock_link_results)
        )
        
        result = await version_validator._validate_links("1.0.0", 0.25)  # 25% threshold
        
        assert result.gate_name == "link_validation"
        assert result.passed  # 20% failure rate < 25% threshold
        assert result.score == 0.8  # 1.0 - 0.2 failure rate
        assert result.details['failure_rate'] == 0.2
    
    @pytest.mark.asyncio
    async def test_assess_performance_impact(self, version_validator, mock_validators, tmp_path):
        """Test performance impact assessment."""
        # Create mock site directory with files
        site_path = tmp_path / "site"
        site_path.mkdir()
        
        # Create mock HTML files
        (site_path / "index.html").write_text("x" * 1024)  # 1KB
        (site_path / "page2.html").write_text("x" * 2048)   # 2KB
        
        # Create mock asset files
        assets_dir = site_path / "assets"
        assets_dir.mkdir()
        (assets_dir / "style.css").write_text("x" * 512)    # 0.5KB
        (assets_dir / "script.js").write_text("x" * 256)    # 0.25KB
        
        with patch.object(version_validator, '_build_documentation', return_value={'success': True}):
            metrics = await version_validator.assess_performance_impact("1.0.0")
        
        assert isinstance(metrics, PerformanceMetrics)
        assert metrics.page_count == 2
        assert metrics.asset_count == 2
        assert metrics.total_size_mb > 0
        assert metrics.avg_page_size_kb == 1.5  # (1KB + 2KB) / 2
        assert metrics.largest_page_size_kb == 2.0
        assert len(metrics.load_time_samples) > 0
    
    @pytest.mark.asyncio
    async def test_validate_performance_success(self, version_validator, mock_validators):
        """Test successful performance validation."""
        mock_metrics = PerformanceMetrics(
            build_time=120.0,      # Under 600s threshold
            total_size_mb=100.0,   # Under 500MB threshold
            page_count=50,
            asset_count=25,
            avg_page_size_kb=500.0,  # Under 1000KB threshold
            largest_page_size_kb=800.0,
            load_time_samples=[1.0, 1.2, 0.8, 1.1]  # Avg 1.025s under 3s threshold
        )
        
        with patch.object(version_validator, 'assess_performance_impact', return_value=mock_metrics):
            result = await version_validator._validate_performance("1.0.0")
        
        assert result.gate_name == "performance_validation"
        assert result.passed
        assert result.score == 1.0
        assert result.details['issues'] == []
    
    @pytest.mark.asyncio
    async def test_validate_performance_issues(self, version_validator, mock_validators):
        """Test performance validation with issues."""
        mock_metrics = PerformanceMetrics(
            build_time=700.0,      # Over 600s threshold
            total_size_mb=600.0,   # Over 500MB threshold
            page_count=50,
            asset_count=25,
            avg_page_size_kb=1200.0,  # Over 1000KB threshold
            largest_page_size_kb=1500.0,
            load_time_samples=[3.5, 4.0, 3.2, 3.8]  # Avg 3.625s over 3s threshold
        )
        
        with patch.object(version_validator, 'assess_performance_impact', return_value=mock_metrics):
            result = await version_validator._validate_performance("1.0.0")
        
        assert result.gate_name == "performance_validation"
        assert not result.passed
        assert result.score == 0.2  # 1.0 - (4 issues * 0.2)
        assert len(result.details['issues']) == 4
    
    @pytest.mark.asyncio
    async def test_validate_version_consistency_success(self, version_validator, mock_validators):
        """Test successful version consistency validation."""
        # Mock version manager methods
        version_validator.version_manager.parse_version.return_value = {
            'major': 1, 'minor': 0, 'patch': 0
        }
        version_validator.version_manager.get_latest_version.return_value = "0.9.0"
        version_validator.version_manager.compare_versions.return_value = -1  # New version is newer
        
        # Mock Mike manager
        version_validator.mike_manager.list_versions.return_value = []
        
        result = await version_validator._validate_version_consistency("1.0.0")
        
        assert result.gate_name == "version_consistency"
        assert result.passed
        assert result.score == 1.0
        assert result.details['issues'] == []
    
    @pytest.mark.asyncio
    async def test_validate_version_consistency_issues(self, version_validator, mock_validators):
        """Test version consistency validation with issues."""
        # Mock invalid version format
        version_validator.version_manager.parse_version.side_effect = ValueError("Invalid format")
        
        result = await version_validator._validate_version_consistency("invalid-version")
        
        assert result.gate_name == "version_consistency"
        assert not result.passed
        assert result.score == 0.7  # 1.0 - (1 issue * 0.3)
        assert "Invalid version format" in result.details['issues'][0]
    
    @pytest.mark.asyncio
    async def test_validate_version_full_workflow(self, version_validator, mock_validators):
        """Test complete version validation workflow."""
        # Mock all validation methods to return success
        successful_result = ValidationResult(
            gate_name="test",
            passed=True,
            score=1.0,
            message="Success",
            details={},
            execution_time=1.0
        )
        
        with patch.object(version_validator, '_run_quality_gate', return_value=successful_result) as mock_gate:
            all_passed, results = await version_validator.validate_version("1.0.0")
        
        assert all_passed
        assert len(results) == len(version_validator.quality_gates)
        assert all(result.passed for result in results)
        assert mock_gate.call_count == len(version_validator.quality_gates)
    
    @pytest.mark.asyncio
    async def test_validate_version_with_failures(self, version_validator, mock_validators):
        """Test version validation with some failures."""
        def mock_gate_results(gate, version):
            if gate.name == "build_validation":
                return ValidationResult(
                    gate_name="build_validation",
                    passed=False,
                    score=0.0,
                    message="Build failed",
                    details={},
                    execution_time=1.0
                )
            else:
                return ValidationResult(
                    gate_name=gate.name,
                    passed=True,
                    score=1.0,
                    message="Success",
                    details={},
                    execution_time=1.0
                )
        
        with patch.object(version_validator, '_run_quality_gate', side_effect=mock_gate_results):
            all_passed, results = await version_validator.validate_version("1.0.0")
        
        assert not all_passed  # Should fail because build_validation is required and failed
        assert len(results) == len(version_validator.quality_gates)
        
        # Find the failed result
        build_result = next(r for r in results if r.gate_name == "build_validation")
        assert not build_result.passed
    
    @pytest.mark.asyncio
    async def test_validate_specific_gates(self, version_validator, mock_validators):
        """Test validating only specific gates."""
        successful_result = ValidationResult(
            gate_name="test",
            passed=True,
            score=1.0,
            message="Success",
            details={},
            execution_time=1.0
        )
        
        with patch.object(version_validator, '_run_quality_gate', return_value=successful_result) as mock_gate:
            all_passed, results = await version_validator.validate_version(
                "1.0.0", 
                gate_names=["build_validation", "navigation_validation"]
            )
        
        assert all_passed
        assert len(results) == 2  # Only ran 2 specific gates
        assert mock_gate.call_count == 2
    
    @pytest.mark.asyncio 
    async def test_validate_version_migration(self, version_validator, mock_validators):
        """Test version migration validation."""
        # Mock migration manager methods
        version_validator.migration_manager.validate_backward_compatibility.return_value = (True, [])
        version_validator.migration_manager._get_breaking_changes_for_range.return_value = []
        version_validator.migration_manager.apply_migration_rules.return_value = {
            'applied_rules': [],
            'failed_rules': []
        }
        
        # Mock version manager
        version_validator.version_manager.compare_versions.return_value = -1
        
        result = await version_validator.validate_version_migration("1.0.0", "1.1.0")
        
        assert result.gate_name == "migration_validation"
        assert result.passed
        assert result.score == 1.0
        assert result.details['issues'] == []
    
    def test_generate_validation_report(self, version_validator):
        """Test validation report generation."""
        # Create mock results
        results = [
            ValidationResult(
                gate_name="build_validation",
                passed=True,
                score=1.0,
                message="Build success",
                details={},
                execution_time=30.0
            ),
            ValidationResult(
                gate_name="link_validation",
                passed=False,
                score=0.8,
                message="Some broken links",
                details={'broken_links': 2},
                execution_time=45.0,
                warnings=["Warning 1"]
            )
        ]
        
        # Mock performance metrics
        performance_metrics = PerformanceMetrics(
            build_time=60.0,
            total_size_mb=25.0,
            page_count=40,
            asset_count=20,
            avg_page_size_kb=150.0,
            largest_page_size_kb=500.0,
            load_time_samples=[0.5, 0.7, 0.6]
        )
        
        report = version_validator.generate_validation_report(
            "1.0.0", results, performance_metrics
        )
        
        assert report['version'] == "1.0.0"
        assert report['overall_result']['gates_passed'] == 1
        assert report['overall_result']['total_gates'] == 2
        assert report['overall_result']['score'] == 0.9  # (1.0 + 0.8) / 2
        
        assert len(report['gate_results']) == 2
        assert len(report['detailed_results']) == 2
        
        assert 'performance_metrics' in report
        assert report['performance_metrics']['build_time_seconds'] == 60.0
        assert report['performance_metrics']['page_count'] == 40
    
    def test_save_validation_report(self, version_validator, tmp_path):
        """Test saving validation report to file."""
        report = {
            'version': '1.0.0',
            'validation_timestamp': 1234567890,
            'overall_result': {
                'passed': True,
                'score': 0.95
            }
        }
        
        output_path = version_validator.save_validation_report(report)
        
        assert output_path.exists()
        assert output_path.name.startswith('validation_report_1.0.0_')
        
        # Load and verify content
        import json
        with open(output_path, 'r') as f:
            loaded_report = json.load(f)
        
        assert loaded_report['version'] == '1.0.0'
        assert loaded_report['overall_result']['passed']
    
    def test_save_validation_report_custom_path(self, version_validator, tmp_path):
        """Test saving validation report to custom path."""
        report = {'version': '1.0.0', 'test': 'data'}
        custom_path = tmp_path / "custom_report.json"
        
        output_path = version_validator.save_validation_report(report, custom_path)
        
        assert output_path == custom_path
        assert output_path.exists()
        
        import json
        with open(output_path, 'r') as f:
            loaded_report = json.load(f)
        
        assert loaded_report['version'] == '1.0.0'
        assert loaded_report['test'] == 'data'


class TestVersionValidatorIntegration:
    """Integration tests for VersionValidator."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_validation(self, tmp_path):
        """Test end-to-end version validation."""
        # Create a minimal project structure
        (tmp_path / "mkdocs.yml").write_text("site_name: Test Docs")
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "index.md").write_text("# Test Documentation")
        
        # Create validator with minimal gates for testing
        test_gates = [
            QualityGate(
                name="build_validation",
                description="Test build",
                validator_class="DocumentationBuilder",
                required=True
            )
        ]
        
        validator = VersionValidator(repo_path=tmp_path, quality_gates=test_gates)
        
        # Mock the build validation to return success
        async def mock_build_validation(version):
            return ValidationResult(
                gate_name="build_validation",
                passed=True,
                score=1.0,
                message="Build successful",
                details={'build_time': 10.0},
                execution_time=10.0
            )
        
        with patch.object(validator, '_validate_build', mock_build_validation):
            all_passed, results = await validator.validate_version("1.0.0")
        
        assert all_passed
        assert len(results) == 1
        assert results[0].gate_name == "build_validation"
        assert results[0].passed
        
        # Generate and save report
        report = validator.generate_validation_report("1.0.0", results)
        report_path = validator.save_validation_report(report)
        
        assert report_path.exists()
        assert report['version'] == "1.0.0"
        assert report['overall_result']['passed']


@pytest.fixture
def mock_async_context():
    """Fixture to handle asyncio context in tests."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


class TestVersionValidatorErrorHandling:
    """Test error handling in VersionValidator."""
    
    @pytest.mark.asyncio
    async def test_validation_gate_exception(self, tmp_path):
        """Test handling of exceptions in validation gates."""
        validator = VersionValidator(repo_path=tmp_path)
        
        # Mock a gate that raises an exception
        with patch.object(validator, '_validate_build', side_effect=Exception("Test error")):
            all_passed, results = await validator.validate_version(
                "1.0.0", 
                gate_names=["build_validation"]
            )
        
        assert not all_passed
        assert len(results) == 1
        result = results[0]
        assert not result.passed
        assert result.score == 0.0
        assert "Gate execution failed" in result.message
        assert "Test error" in result.details['error']
    
    @pytest.mark.asyncio
    async def test_unknown_validator_class(self, tmp_path):
        """Test handling of unknown validator class."""
        custom_gates = [
            QualityGate(
                name="unknown_gate",
                description="Unknown validator",
                validator_class="UnknownValidator"
            )
        ]
        
        validator = VersionValidator(repo_path=tmp_path, quality_gates=custom_gates)
        
        all_passed, results = await validator.validate_version("1.0.0")
        
        assert not all_passed
        assert len(results) == 1
        result = results[0]
        assert not result.passed
        assert "Unknown validator class" in result.details['error']
