# CSA Docs Testing Infrastructure

This document describes the comprehensive testing infrastructure for the CSA-in-a-Box documentation project.

## Overview

The testing infrastructure provides automated validation for:

- 📚 **Documentation Build Testing** - Validates MkDocs configuration and build process
- 🔗 **Link Validation** - Checks internal and external links for validity
- 📝 **Markdown Quality** - Enforces style guidelines and quality standards  
- 🖼️ **Image Reference Testing** - Validates image files and references
- 🧭 **Navigation Structure** - Ensures proper navigation organization

## Quick Start

### Prerequisites

- Python 3.9+ 
- Node.js 18+ (for markdownlint)
- Git

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-test.txt
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install -g markdownlint-cli
   ```

3. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

### Running Tests

**Run all tests:**
```bash
python run_tests.py
```

**Run specific test suites:**
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests  
pytest tests/integration/ -v

# With coverage
pytest --cov=src/csa_docs_tools --cov-report=html
```

**Use the CLI tool:**
```bash
# Run all validations
python -m src.csa_docs_tools.cli all

# Test specific components
python -m src.csa_docs_tools.cli build --strict
python -m src.csa_docs_tools.cli quality --min-score 80
python -m src.csa_docs_tools.cli links --no-external
python -m src.csa_docs_tools.cli images --report-unused
python -m src.csa_docs_tools.cli nav --max-depth 4
```

## Architecture

### Package Structure

```
src/csa_docs_tools/
├── __init__.py              # Package exports
├── build_tester.py          # Documentation build validation
├── link_validator.py        # Link checking (async)
├── markdown_quality.py      # Markdown quality analysis
├── image_validator.py       # Image reference validation
├── navigation_validator.py  # Navigation structure validation
└── cli.py                   # Command-line interface

tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests for individual modules
│   ├── test_build_tester.py
│   ├── test_link_validator.py
│   ├── test_markdown_quality.py
│   ├── test_image_validator.py
│   └── test_navigation_validator.py
├── integration/             # Integration and end-to-end tests
│   └── test_full_validation.py
└── fixtures/                # Test data and utilities
    └── test_data.py
```

### Core Components

#### 1. DocumentationBuildTester

Validates MkDocs configuration and tests the build process.

**Features:**
- MkDocs configuration validation
- Build testing with strict mode support
- Plugin dependency checking
- Navigation structure validation
- Build statistics generation

**Usage:**
```python
from src.csa_docs_tools import DocumentationBuildTester

tester = DocumentationBuildTester(docs_root)
is_valid, errors = tester.validate_mkdocs_config()
success, stdout, stderr = tester.test_build(strict=True)
```

#### 2. LinkValidator

Asynchronous link validation for internal and external links.

**Features:**
- Internal link validation (file existence)
- External link validation (HTTP status)
- Concurrent link checking
- Timeout handling
- Comprehensive reporting

**Usage:**
```python
from src.csa_docs_tools import LinkValidator

async with LinkValidator(docs_root) as validator:
    results = await validator.validate_all_links(check_external=True)
    report = validator.generate_report(results)
```

#### 3. MarkdownQualityChecker

Enforces markdown quality and style standards.

**Features:**
- Built-in quality rules (headings, line length, formatting)
- markdownlint CLI integration
- Configurable quality thresholds
- Detailed issue reporting
- Quality score calculation

**Usage:**
```python
from src.csa_docs_tools import MarkdownQualityChecker

checker = MarkdownQualityChecker(docs_root)
results = checker.check_all_files()
report = checker.generate_quality_report(results)
```

#### 4. ImageReferenceValidator

Validates image files and references in documentation.

**Features:**
- Image file existence validation
- Format validation (PNG, JPG, SVG, etc.)
- Alt text quality checking
- Unused image detection
- Image property analysis (size, dimensions)

**Usage:**
```python
from src.csa_docs_tools import ImageReferenceValidator

validator = ImageReferenceValidator(docs_root)
results = validator.validate_all_images()
report = validator.generate_image_report(results)
```

#### 5. NavigationStructureValidator

Validates MkDocs navigation structure and organization.

**Features:**
- Navigation consistency checking
- Orphaned file detection
- Navigation depth validation
- Index file validation
- Structure optimization suggestions

**Usage:**
```python
from src.csa_docs_tools import NavigationStructureValidator

validator = NavigationStructureValidator(docs_root)
results = validator.validate_all_navigation()
report = validator.generate_navigation_report(results)
```

## Testing Strategy

### Test Categories

1. **Unit Tests** (`tests/unit/`)
   - Test individual components in isolation
   - Mock external dependencies
   - Fast execution (< 30 seconds total)
   - 90%+ code coverage target

2. **Integration Tests** (`tests/integration/`) 
   - Test component interactions
   - Use real test data and files
   - Validate end-to-end workflows
   - Performance benchmarking

3. **Quality Gates**
   - Code coverage ≥ 90%
   - All linting checks pass
   - Documentation builds successfully
   - No broken internal links

### Test Fixtures

The testing infrastructure includes comprehensive fixtures:

- **Temporary documentation structures** with various scenarios
- **Sample markdown content** with common issues
- **Mock HTTP responses** for external link testing
- **Test images** in multiple formats
- **MkDocs configurations** for different scenarios

### Parameterized Testing

Tests use parameterization for comprehensive coverage:

```python
@pytest.mark.parametrize("test_scenario,expected_score", [
    ("perfect_docs", 100.0),
    ("problematic_docs", 60.0),
    ("broken_build", 0.0)
])
def test_quality_scores(test_scenario, expected_score):
    # Test implementation
```

## Configuration

### pytest.ini

Comprehensive pytest configuration with:
- Coverage reporting (HTML, XML, terminal)
- Test markers for categorization
- Strict mode for markers and configuration
- Warning filters

### pyproject.toml

Modern Python project configuration including:
- Ruff linting and formatting rules
- MyPy type checking configuration
- Coverage settings
- Package metadata

### .pre-commit-config.yaml

Pre-commit hooks for:
- Code formatting and linting
- Markdown quality checks
- Documentation validation
- Security scanning

## Continuous Integration

### GitHub Actions Workflow

The `.github/workflows/documentation-tests.yml` provides:

- **Multi-matrix testing** (unit, integration)
- **Code quality checks** (linting, formatting, type checking)
- **Documentation build testing**
- **Security scanning** 
- **Coverage reporting**
- **Artifact collection**

### Workflow Jobs

1. **test-documentation** - Core test execution
2. **lint-and-format** - Code quality validation
3. **test-documentation-build** - MkDocs build testing
4. **test-link-validation** - Link checking
5. **markdown-quality** - Content quality validation
6. **image-validation** - Image reference checking
7. **security-scan** - Security vulnerability scanning
8. **generate-report** - Consolidated reporting

## Performance Considerations

### Optimization Strategies

- **Async link validation** for concurrent external link checking
- **Selective file processing** to avoid unnecessary work
- **Caching mechanisms** for repeated operations
- **Configurable timeouts** for external services
- **Incremental validation** for large documentation sets

### Benchmarks

Performance targets for different documentation sizes:

| Site Size | Files | Max Build Time | Max Quality Check | Max Link Check |
|-----------|-------|----------------|-------------------|----------------|
| Small     | 10    | 5s             | 2s                | 3s             |
| Medium    | 100   | 15s            | 10s               | 20s            |
| Large     | 500   | 60s            | 30s               | 120s           |

## CLI Usage

### Available Commands

```bash
# Run all validations
csa-docs-validate all

# Individual validations
csa-docs-validate build --strict
csa-docs-validate quality --min-score 80
csa-docs-validate links --no-external
csa-docs-validate images --report-unused
csa-docs-validate nav --max-depth 4

# Output formats
csa-docs-validate all --output json
csa-docs-validate all --output summary
```

### Configuration Options

- `--docs-root` - Specify documentation root directory
- `--config` - Custom configuration file path
- `--output` - Output format (text, json, summary)
- `--quiet` - Suppress non-error output
- `--verbose` - Enable verbose logging

## Quality Standards

### Code Quality Requirements

- **100%** type hints coverage
- **90%+** test coverage
- **Zero** linting errors
- **Consistent** code formatting (Black, Ruff)
- **Comprehensive** documentation

### Documentation Quality Standards

- **Markdown compliance** per .markdownlint.json
- **Valid internal links** (no 404s)
- **Proper alt text** for all images
- **Consistent navigation** structure
- **Build success** in strict mode

## Troubleshooting

### Common Issues

**Import errors:**
```bash
# Ensure package is installed in development mode
pip install -e .
```

**Missing dependencies:**
```bash
# Install all test dependencies
pip install -r requirements-test.txt
```

**markdownlint not found:**
```bash
# Install globally
npm install -g markdownlint-cli
```

**Permission errors:**
```bash
# Check file permissions
chmod +x run_tests.py
```

### Debugging Tests

**Run with verbose output:**
```bash
pytest -v -s tests/unit/test_build_tester.py::TestBuildTester::test_specific
```

**Debug with PDB:**
```bash
pytest --pdb tests/unit/test_build_tester.py::TestBuildTester::test_specific
```

**Coverage debugging:**
```bash
pytest --cov=src/csa_docs_tools --cov-report=html
# Open htmlcov/index.html
```

## Contributing

### Adding New Tests

1. **Create test file** following naming convention `test_*.py`
2. **Use fixtures** from `conftest.py` for common setup
3. **Follow AAA pattern** (Arrange, Act, Assert)
4. **Add markers** for test categorization
5. **Update documentation** for new features

### Test Categories Markers

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests  
- `@pytest.mark.slow` - Long-running tests
- `@pytest.mark.network` - Tests requiring network access

### Code Coverage

Maintain high code coverage by:
- Testing both success and error paths
- Using parametrized tests for multiple scenarios  
- Mocking external dependencies appropriately
- Testing edge cases and boundary conditions

## Future Enhancements

### Planned Features

- **Spell checking** integration
- **Accessibility validation** for generated HTML
- **Performance regression testing**
- **Custom rule plugins** for organization-specific standards
- **Integration with documentation hosting platforms**

### Enhancement Opportunities

- **Machine learning** for content quality assessment
- **Visual regression testing** for documentation appearance
- **Automated fix suggestions** for common issues
- **Advanced analytics** and reporting dashboards
- **Integration with CMS systems**

---

For questions or support, please refer to the project documentation or open an issue in the repository.