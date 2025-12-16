# 🧪 Testing Guide

> __🏠 [Home](../../README.md)__ | __📚 Documentation__ | __📖 [Guides](./README.md)__

---

## 📋 Overview

This guide provides comprehensive testing strategies, standards, and procedures for the Cloud Scale Analytics (CSA) in-a-Box documentation project. It covers unit testing, integration testing, documentation validation, and quality assurance processes.

## 📑 Table of Contents

- [Testing Philosophy](#testing-philosophy)
- [Testing Types](#testing-types)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [Documentation Testing](#documentation-testing)
- [Link Validation](#link-validation)
- [Performance Testing](#performance-testing)
- [Continuous Integration](#continuous-integration)
- [Test Coverage](#test-coverage)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Testing Philosophy

### Core Principles

1. __Test Early, Test Often__ - Integrate testing into development workflow
2. __Comprehensive Coverage__ - Test all critical paths and edge cases
3. __Fast Feedback__ - Quick test execution for rapid iteration
4. __Maintainable Tests__ - Clear, documented, and easy to update
5. __Automated Validation__ - Minimize manual testing through automation

### Testing Pyramid

```text
        /\
       /  \  E2E Tests (5%)
      /    \
     /------\ Integration Tests (25%)
    /        \
   /----------\ Unit Tests (70%)
```

---

## 🔍 Testing Types

### Test Categories

| Type | Purpose | Scope | Speed | Frequency |
|------|---------|-------|-------|-----------|
| __Unit Tests__ | Test individual components | Single function/class | Fast (ms) | Every commit |
| __Integration Tests__ | Test component interactions | Multiple components | Medium (seconds) | Every PR |
| __E2E Tests__ | Test complete workflows | Full system | Slow (minutes) | Before release |
| __Documentation Tests__ | Validate docs quality | Markdown files | Fast | Every change |
| __Link Tests__ | Check link validity | All links | Medium | Daily |
| __Performance Tests__ | Measure performance | Critical paths | Varies | Weekly |

---

## 📁 Test Structure

### Directory Organization

```text
tests/
├── __init__.py
├── conftest.py                    # Shared fixtures
│
├── unit/                          # Unit tests
│   ├── __init__.py
│   ├── conftest.py               # Unit test fixtures
│   ├── test_build_tester.py
│   ├── test_image_validator.py
│   ├── test_link_validator.py
│   ├── test_markdown_quality.py
│   └── test_navigation_validator.py
│
├── integration/                   # Integration tests
│   ├── __init__.py
│   ├── conftest.py               # Integration fixtures
│   └── test_full_validation.py
│
├── e2e/                          # End-to-end tests
│   ├── __init__.py
│   └── test_documentation_flow.py
│
└── fixtures/                     # Test data
    ├── test_data.py
    ├── sample_docs/
    └── mock_responses/
```

---

## 🚀 Running Tests

### Quick Start

```bash
# Run all tests
pytest

# Run with output
pytest -v

# Run specific test file
pytest tests/unit/test_link_validator.py

# Run specific test
pytest tests/unit/test_link_validator.py::TestLinkValidator::test_validate_internal_links
```

### Test Commands

#### Basic Testing

```bash
# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run e2e tests only
pytest tests/e2e/

# Run tests matching pattern
pytest -k "test_validate"

# Run tests with specific marker
pytest -m "slow"
```

#### Advanced Options

```bash
# Run with coverage report
pytest --cov=src/csa_docs_tools --cov-report=html

# Run in parallel
pytest -n auto

# Run with detailed output
pytest -vvs

# Stop on first failure
pytest -x

# Run failed tests from last run
pytest --lf

# Run tests that failed first
pytest --ff
```

### Documentation Testing

```bash
# Validate all markdown files
python src/csa_docs_tools/cli.py validate --all

# Check markdown quality
python src/csa_docs_tools/cli.py quality-check

# Validate links
python src/csa_docs_tools/cli.py validate-links

# Check images
python src/csa_docs_tools/cli.py validate-images

# Test MkDocs build
python src/csa_docs_tools/cli.py test-build
```

---

## ✍️ Writing Tests

### Test Structure Template

```python
"""Test module for ComponentName."""
import pytest
from unittest.mock import Mock, patch
from csa_docs_tools.component import ComponentName


class TestComponentName:
    """Test cases for ComponentName."""
    
    @pytest.fixture
    def component(self):
        """Create component instance for testing."""
        return ComponentName(config={"test": True})
    
    @pytest.fixture
    def mock_data(self):
        """Sample data for testing."""
        return {
            "valid": "test_data",
            "invalid": None
        }
    
    def test_initialization(self, component):
        """Test component initialization."""
        assert component is not None
        assert component.config["test"] is True
    
    def test_valid_input(self, component, mock_data):
        """Test component with valid input."""
        result = component.process(mock_data["valid"])
        assert result.success is True
        assert result.data == "processed_test_data"
    
    def test_invalid_input(self, component, mock_data):
        """Test component with invalid input."""
        with pytest.raises(ValueError) as exc_info:
            component.process(mock_data["invalid"])
        assert "Invalid input" in str(exc_info.value)
    
    @patch('csa_docs_tools.component.external_service')
    def test_with_mock(self, mock_service, component):
        """Test component with mocked external service."""
        mock_service.return_value = {"status": "success"}
        result = component.call_service()
        assert result["status"] == "success"
        mock_service.assert_called_once()
```

### Assertion Examples

```python
# Basic assertions
assert value == expected
assert value is not None
assert len(items) > 0
assert "substring" in text

# Exception assertions
with pytest.raises(ValueError):
    function_that_raises()

# Warning assertions
with pytest.warns(UserWarning):
    function_that_warns()

# Approximate comparisons
assert value == pytest.approx(0.3, rel=1e-2)

# Collection assertions
assert set(result) == {"a", "b", "c"}
assert all(x > 0 for x in values)
assert any(x == target for x in values)
```

### Fixtures Best Practices

```python
@pytest.fixture
def temp_directory(tmp_path):
    """Create temporary directory for testing."""
    test_dir = tmp_path / "test_docs"
    test_dir.mkdir()
    
    # Setup test files
    (test_dir / "README.md").write_text("# Test")
    (test_dir / "guide.md").write_text("## Guide")
    
    yield test_dir
    
    # Cleanup (automatic with tmp_path)

@pytest.fixture(scope="session")
def shared_config():
    """Shared configuration for all tests."""
    return {
        "base_url": "http://localhost:8000",
        "timeout": 30,
        "retry_count": 3
    }

@pytest.fixture
def mock_http_client():
    """Mock HTTP client for testing."""
    with patch('aiohttp.ClientSession') as mock_client:
        mock_response = Mock()
        mock_response.status = 200
        mock_response.text.return_value = "Success"
        mock_client.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response
        yield mock_client
```

---

## 📄 Documentation Testing

### Markdown Validation

```python
"""Test markdown documentation quality."""
import pytest
from pathlib import Path
from csa_docs_tools.markdown_quality import MarkdownValidator


class TestMarkdownQuality:
    """Test markdown file quality."""
    
    @pytest.fixture
    def validator(self):
        """Create markdown validator."""
        return MarkdownValidator()
    
    def test_heading_structure(self, validator):
        """Test proper heading hierarchy."""
        content = """
        # Title
        ## Section
        ### Subsection
        """
        result = validator.validate_headings(content)
        assert result.valid is True
    
    def test_code_blocks(self, validator):
        """Test code block formatting."""
        content = """
        ```python
        def example():
            return True
        ```
        """
        result = validator.validate_code_blocks(content)
        assert result.valid is True
        assert result.language == "python"
    
    def test_link_format(self, validator):
        """Test markdown link formatting."""
        content = "[Link Text](https://example.com)"
        result = validator.validate_links(content)
        assert result.valid is True
```

### Link Validation Testing

```python
"""Test link validation functionality."""
import pytest
from csa_docs_tools.link_validator import LinkValidator


class TestLinkValidation:
    """Test link validation."""
    
    @pytest.fixture
    def validator(self):
        """Create link validator."""
        return LinkValidator(base_path="docs/")
    
    @pytest.mark.asyncio
    async def test_internal_links(self, validator):
        """Test internal link validation."""
        links = [
            "../README.md",
            "./guides/TESTING_GUIDE.md",
            "#section-anchor"
        ]
        
        results = await validator.validate_links(links)
        assert all(r.valid for r in results)
    
    @pytest.mark.asyncio
    async def test_external_links(self, validator, mock_http_client):
        """Test external link validation."""
        links = [
            "https://docs.microsoft.com",
            "https://github.com/org/repo"
        ]
        
        results = await validator.validate_links(links)
        assert all(r.status_code == 200 for r in results)
```

---

## 🔗 Link Validation

### Running Link Tests

```bash
# Validate all links
python src/csa_docs_tools/cli.py validate-links

# Validate specific directory
python src/csa_docs_tools/cli.py validate-links --path docs/guides/

# Generate link report
python src/csa_docs_tools/cli.py validate-links --report link_report.md

# Check external links only
python src/csa_docs_tools/cli.py validate-links --external-only

# Check with timeout
python src/csa_docs_tools/cli.py validate-links --timeout 10
```

### Link Test Configuration

```python
# config/link_validation.yaml
link_validation:
  internal:
    check_anchors: true
    follow_redirects: true
    case_sensitive: false
    
  external:
    enabled: true
    timeout: 30
    retry_count: 3
    user_agent: "CSA-Docs-Bot/1.0"
    
  ignore_patterns:
    - "localhost"
    - "127.0.0.1"
    - "example.com"
    
  ignore_status_codes:
    - 429  # Too many requests
    - 503  # Service unavailable
```

---

## ⚡ Performance Testing

### Documentation Build Performance

```python
"""Test documentation build performance."""
import pytest
import time
from csa_docs_tools.build_tester import BuildTester


class TestBuildPerformance:
    """Test build performance metrics."""
    
    @pytest.fixture
    def builder(self):
        """Create build tester."""
        return BuildTester()
    
    def test_build_time(self, builder):
        """Test documentation build time."""
        start_time = time.time()
        result = builder.build()
        build_time = time.time() - start_time
        
        assert result.success is True
        assert build_time < 60  # Should build in under 60 seconds
    
    def test_incremental_build(self, builder):
        """Test incremental build performance."""
        # Initial build
        builder.build()
        
        # Incremental build
        start_time = time.time()
        result = builder.build(incremental=True)
        incremental_time = time.time() - start_time
        
        assert result.success is True
        assert incremental_time < 10  # Should be much faster
```

### Load Testing

```bash
# Test documentation server under load
locust -f tests/performance/load_test.py --host http://localhost:8000

# Run with specific parameters
locust -f tests/performance/load_test.py \
  --host http://localhost:8000 \
  --users 100 \
  --spawn-rate 10 \
  --time 60s
```

---

## 🔄 Continuous Integration

### GitHub Actions Configuration

```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src/csa_docs_tools --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
    
    - name: Validate documentation
      run: |
        python src/csa_docs_tools/cli.py validate --all
    
    - name: Build documentation
      run: |
        mkdocs build --strict
```

---

## 📊 Test Coverage

### Coverage Requirements

| Component | Minimum Coverage | Target Coverage |
|-----------|-----------------|-----------------|
| Core Libraries | 80% | 90% |
| Validators | 90% | 95% |
| Utilities | 70% | 85% |
| CLI Commands | 75% | 85% |
| Overall | 80% | 90% |

### Generating Coverage Reports

```bash
# Generate terminal report
pytest --cov=src/csa_docs_tools

# Generate HTML report
pytest --cov=src/csa_docs_tools --cov-report=html
# Open htmlcov/index.html in browser

# Generate XML report for CI
pytest --cov=src/csa_docs_tools --cov-report=xml

# Show missing lines
pytest --cov=src/csa_docs_tools --cov-report=term-missing
```

### Coverage Configuration

```ini
# pyproject.toml or .coveragerc
[tool.coverage.run]
source = ["src/csa_docs_tools"]
omit = [
    "*/tests/*",
    "*/__init__.py",
    "*/conftest.py"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:"
]
```

---

## 💡 Best Practices

### Test Writing Guidelines

1. __Clear Test Names__ - Describe what is being tested

   ```python
   def test_validate_returns_true_for_valid_markdown():  # Good
   def test_1():  # Bad
   ```

2. __Arrange-Act-Assert Pattern__

   ```python
   def test_process_data():
       # Arrange
       processor = DataProcessor()
       data = {"key": "value"}
       
       # Act
       result = processor.process(data)
       
       # Assert
       assert result.success is True
   ```

3. __One Assertion Per Test__ - Keep tests focused
4. __Use Fixtures__ - DRY principle for test setup
5. __Mock External Dependencies__ - Isolate unit tests
6. __Test Edge Cases__ - Empty, null, boundary values
7. __Use Descriptive Assertions__ - Clear failure messages

### Test Markers

```python
# Mark slow tests
@pytest.mark.slow
def test_complex_validation():
    pass

# Mark tests requiring network
@pytest.mark.network
def test_external_links():
    pass

# Skip tests conditionally
@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows")
def test_unix_only():
    pass

# Mark expected failures
@pytest.mark.xfail(reason="Feature not implemented")
def test_future_feature():
    pass
```

---

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Tests not discovered | Check file naming (`test_*.py` or `*_test.py`) |
| Import errors | Verify PYTHONPATH includes project root |
| Async test failures | Use `@pytest.mark.asyncio` decorator |
| Fixture not found | Check fixture scope and imports |
| Coverage missing | Ensure source paths are correct |

### Debug Commands

```bash
# Show test collection
pytest --collect-only

# Run with debugging
pytest --pdb

# Show fixture availability
pytest --fixtures

# Verbose test output
pytest -vvs

# Show test durations
pytest --durations=10

# Generate JUnit XML
pytest --junitxml=test-results.xml
```

### Test Isolation

```python
# Reset global state
@pytest.fixture(autouse=True)
def reset_globals():
    """Reset global state before each test."""
    import csa_docs_tools.globals as g
    original_state = g.STATE.copy()
    yield
    g.STATE = original_state

# Isolate file system changes
@pytest.fixture
def isolated_filesystem(tmp_path, monkeypatch):
    """Isolate file system operations."""
    monkeypatch.chdir(tmp_path)
    return tmp_path
```

---

## 📚 Resources

### Internal Documentation

- [Development Guide](./DEVELOPMENT_GUIDE.md)
- [Contributing Guide](./CONTRIBUTING_GUIDE.md)
- [Code Review Guide](./CODE_REVIEW_GUIDE.md)

### External Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://testdriven.io/blog/testing-best-practices/)
- [Python Testing 101](https://realpython.com/python-testing/)

### Testing Tools

- __pytest__ - Test framework
- __pytest-cov__ - Coverage plugin
- __pytest-asyncio__ - Async support
- __pytest-mock__ - Mock helpers
- __pytest-xdist__ - Parallel execution
- __tox__ - Test automation
- __hypothesis__ - Property-based testing

---

__Last Updated:__ January 28, 2025  
__Version:__ 1.0.0  
__Maintainer:__ CSA Documentation Team
