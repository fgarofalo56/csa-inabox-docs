# 💻 Development Scripts

> **🏠 [Home](../../README.md)** | **📚 [Documentation](../../docs/README.md)** | **📜 [Scripts](../README.md)** | **📊 [Project Tracking](../../project_tracking/README.md)**

---

## 📋 Overview

This directory contains scripts that support the development workflow for the Cloud Scale Analytics (CSA) in-a-Box documentation project. These scripts automate code quality checks, testing procedures, content generation, and other development tasks to ensure high-quality documentation and efficient development processes.

## 🎯 Purpose

The development scripts are designed to:

- **Generate and scaffold content** automatically from templates
- **Run comprehensive testing** of documentation and code examples
- **Perform code quality checks** and linting across all file types
- **Automate formatting** and style standardization
- **Support development workflow** with productivity tools
- **Validate development standards** and best practices compliance

## 📂 Directory Structure

```
development/
├── 📄 README.md                    # This file
├── 📁 code-generation/             # Code and content generation scripts
│   ├── 📄 README.md                # Code generation documentation
│   └── (planned generation scripts)
├── 📁 testing/                     # Testing and validation scripts
│   ├── 📄 README.md                # Testing scripts documentation
│   └── (planned testing scripts)
└── 📁 linting/                     # Code quality and linting scripts
    ├── 📄 README.md                # Linting scripts documentation
    └── (planned linting scripts)
```

## 📂 Current Scripts

### Available Scripts

Currently, no scripts exist in this directory. All scripts listed below are planned for implementation.

### Planned Scripts (To Be Created)

| Category | Script | Purpose | Priority |
|----------|--------|---------|----------|
| **General** | `run-all-checks.sh` | Run all quality checks and tests | **HIGH** |
| **General** | `setup-dev-environment.sh` | Set up development environment | **MEDIUM** |
| **Code Generation** | `generate-doc-template.sh` | Generate documentation templates | **HIGH** |
| **Code Generation** | `generate-api-docs.sh` | Generate API documentation | **MEDIUM** |
| **Testing** | `run-tests.sh` | Run comprehensive test suite | **HIGH** |
| **Testing** | `validate-examples.sh` | Validate code examples and snippets | **MEDIUM** |
| **Linting** | `lint-all.sh` | Run all linting tools | **HIGH** |
| **Linting** | `format-code.sh` | Format all code and configuration files | **MEDIUM** |

## 🚀 Usage Examples

### Development Workflow

```bash
# Set up development environment (planned)
./scripts/development/setup-dev-environment.sh

# Run all quality checks before committing
./scripts/development/run-all-checks.sh

# Generate new documentation from template
./scripts/development/code-generation/generate-doc-template.sh --type guide --name "new-guide"
```

### Quality Assurance Workflow

```bash
# Run comprehensive testing
./scripts/development/testing/run-tests.sh --verbose

# Lint all files
./scripts/development/linting/lint-all.sh --fix

# Format all code
./scripts/development/linting/format-code.sh --check
```

### Content Generation Workflow

```bash
# Generate API documentation (planned)
./scripts/development/code-generation/generate-api-docs.sh --source src/ --output docs/api/

# Validate all code examples
./scripts/development/testing/validate-examples.sh --format json
```

## 📋 Planned Script Details

### `run-all-checks.sh` (Priority: HIGH)

**Purpose:** Comprehensive quality check suite that runs all validation, testing, and linting

**Features:**
- Run all linting tools (markdown, YAML, JSON, shell)
- Execute test suites for documentation and code examples
- Validate links and content integrity
- Check formatting and style consistency
- Generate comprehensive quality report
- Support for CI/CD integration

**Planned Usage:**
```bash
./run-all-checks.sh [--fix] [--report-format format] [--output-dir path]

# Examples
./run-all-checks.sh --fix  # Auto-fix issues where possible
./run-all-checks.sh --report-format html --output-dir reports/
./run-all-checks.sh --ci  # CI mode with non-zero exit on failures
```

### `setup-dev-environment.sh` (Priority: MEDIUM)

**Purpose:** Set up complete development environment with all tools and dependencies

**Features:**
- Install development dependencies (Node.js, Python packages)
- Configure development tools (pre-commit hooks, linters)
- Set up local development server
- Configure IDE settings and extensions
- Create development configuration files

**Planned Usage:**
```bash
./setup-dev-environment.sh [--ide vscode] [--skip-optional] [--minimal]

# Examples
./setup-dev-environment.sh --ide vscode  # Include VS Code configuration
./setup-dev-environment.sh --minimal  # Basic setup only
```

## 🔧 Development Categories

### Code and Content Generation

See [Code generation documentation](./code-generation/README.md) for detailed information about:
- Documentation template generation
- API documentation automation
- Content scaffolding and boilerplates
- Automated content updates

### Testing and Validation

See [Testing scripts documentation](./testing/README.md) for detailed information about:
- Documentation testing frameworks
- Code example validation
- Link checking and content validation
- Performance and accessibility testing

### Code Quality and Linting

See [Linting scripts documentation](./linting/README.md) for detailed information about:
- Multi-format linting (Markdown, YAML, JSON, Shell)
- Code formatting and style enforcement
- Configuration validation
- Quality metrics and reporting

## 🛠️ Development Standards

### Code Quality Standards

**File Type Standards:**
```yaml
quality_standards:
  markdown:
    - markdownlint (MD rules)
    - consistent heading structure
    - proper link formatting
    - table formatting
    
  yaml:
    - yamllint configuration
    - consistent indentation (2 spaces)
    - proper key ordering
    - no trailing spaces
    
  json:
    - valid JSON syntax
    - consistent formatting (2-space indent)
    - alphabetical key ordering
    - no trailing commas
    
  shell:
    - shellcheck for script validation
    - consistent shebang (#!/bin/bash)
    - proper error handling (set -e)
    - comprehensive comments
```

### Development Workflow

**Pre-commit Quality Checks:**
1. **Format check** - Ensure all files follow formatting standards
2. **Lint check** - Run appropriate linters for each file type
3. **Test execution** - Run relevant tests for changed components
4. **Link validation** - Check any new or modified links
5. **Build validation** - Ensure documentation builds successfully

**Development Process:**
```bash
1. Create feature branch
   git checkout -b feature/new-documentation

2. Make changes and validate locally
   ./scripts/development/run-all-checks.sh

3. Commit with quality validation
   git add .
   git commit -m "docs: add new architecture guide"

4. Push and create pull request
   git push origin feature/new-documentation

5. CI validates changes automatically
   - All quality checks pass
   - Documentation builds successfully
   - No broken links introduced
```

## 🔧 Configuration

### Development Environment Configuration

**Configuration File:** `config/development.yml`

```yaml
# Development Configuration
development:
  # Environment setup
  environment:
    python_version: "3.9+"
    node_version: "18+"
    required_tools:
      - "git"
      - "docker"
      - "curl"
    
    optional_tools:
      - "azure-cli"
      - "kubectl"
  
  # Code generation
  code_generation:
    templates_path: "templates/"
    output_path: "generated/"
    
    # Template settings
    templates:
      documentation:
        default_author: "CSA Documentation Team"
        default_version: "1.0.0"
        include_toc: true
        
      api:
        format: "openapi"
        include_examples: true
        generate_schemas: true
  
  # Testing configuration
  testing:
    parallel_execution: true
    max_workers: 4
    
    # Test suites
    test_suites:
      - "documentation"
      - "links"
      - "code_examples"
      - "accessibility"
    
    # Test settings
    link_check:
      timeout: 30
      retry_count: 3
      parallel_requests: 5
  
  # Linting configuration
  linting:
    # Markdown linting
    markdownlint:
      config_file: ".markdownlint.json"
      fix_auto: true
      
    # YAML linting  
    yamllint:
      config_file: ".yamllint.yml"
      strict: true
      
    # Shell script linting
    shellcheck:
      shell: "bash"
      severity: "warning"
      
    # Formatting
    formatting:
      line_length: 120
      indent_size: 2
      trim_trailing_whitespace: true
```

### Development Tools Integration

**VS Code Configuration:** `.vscode/settings.json`

```json
{
  "editor.formatOnSave": true,
  "editor.rulers": [120],
  "files.trimTrailingWhitespace": true,
  
  "markdownlint.config": {
    "MD013": { "line_length": 120 },
    "MD033": false
  },
  
  "yaml.schemas": {
    "./schemas/config.schema.json": ["config/*.yml"]
  },
  
  "recommendations": [
    "davidanson.vscode-markdownlint",
    "redhat.vscode-yaml",
    "timonwong.shellcheck",
    "ms-python.python"
  ]
}
```

**Pre-commit Configuration:** `.pre-commit-config.yaml`

```yaml
repos:
  - repo: local
    hooks:
      - id: run-all-checks
        name: Run All Quality Checks
        entry: ./scripts/development/run-all-checks.sh
        language: script
        pass_filenames: false
        always_run: true
        
      - id: lint-shell-scripts
        name: Lint Shell Scripts
        entry: shellcheck
        language: system
        files: \.sh$
        
      - id: format-yaml
        name: Format YAML Files
        entry: yamllint
        language: system
        files: \.(yaml|yml)$
```

## 📊 Development Metrics

### Quality Metrics

**Code Quality Dashboard:**
```
Development Quality Report - 2025-01-28

📊 Overall Quality Score: 94/100

File Quality:
✅ Markdown: 156/158 files pass linting (98.7%)
✅ YAML: 23/23 files pass validation (100%)
✅ JSON: 12/12 files pass validation (100%) 
⚠️ Shell: 8/10 files pass shellcheck (80%)

Content Quality:
✅ Links: 1,244/1,247 working (99.8%)
✅ Images: 89/89 accessible (100%)
✅ Code Examples: 45/47 validate (95.7%)
✅ Accessibility: WCAG AA compliant

Build Quality:
✅ Documentation Build: Success (2.3s)
✅ Test Suite: 47/47 tests pass (100%)
⚠️ Performance: 2 pages >2.5s LCP

Issues Found:
- 2 shell scripts need shellcheck fixes
- 3 broken external links 
- 2 code examples need updates
- 2 pages need performance optimization

Actions Recommended:
- Fix shell script issues (priority: medium)
- Update code examples with latest versions
- Optimize page performance (images, resources)
```

### Development Activity Metrics

**Weekly Development Summary:**
```bash
Development Activity (Past 7 Days):

Commits: 23 commits by 4 contributors
Files Changed: 67 files modified
Quality Improvements: 
- Fixed 15 linting issues
- Updated 8 code examples
- Optimized 4 images

Pre-commit Hook Stats:
- Triggered: 23 times
- Passed: 21 times (91.3%)
- Failed: 2 times (fixed and re-committed)

Test Execution:
- Total test runs: 156
- Average execution time: 3.2 minutes
- Success rate: 97.4%

Most Active Areas:
- Architecture documentation (12 changes)
- Development guides (8 changes)
- Configuration examples (6 changes)
```

## 🔍 Troubleshooting

### Common Development Issues

| Issue | Symptoms | Cause | Solution |
|-------|----------|--------|----------|
| **Linting failures** | CI fails on quality checks | Files don't meet style standards | Run local linting and fix issues |
| **Test failures** | Tests fail locally or in CI | Code examples or links broken | Update examples and fix broken references |
| **Build failures** | Documentation won't build | Syntax errors or missing files | Check build logs and fix syntax issues |
| **Performance issues** | Slow development workflow | Too many checks or large files | Optimize scripts and use parallel processing |
| **Environment issues** | Tools not working properly | Missing dependencies or versions | Re-run environment setup script |

### Development Debug Commands

```bash
# Check development environment
./scripts/development/setup-dev-environment.sh --check

# Run specific quality checks
./scripts/development/linting/lint-all.sh --verbose --type markdown
./scripts/development/testing/run-tests.sh --debug

# Check build process
mkdocs build --verbose --clean

# Validate specific components
./scripts/development/testing/validate-examples.sh --file specific-example.py
./scripts/maintenance/monitoring/check-links.sh --internal-only
```

### Performance Optimization

**Development Performance Tips:**
- **Use parallel processing** - Run multiple checks simultaneously
- **Cache validation results** - Avoid re-checking unchanged content
- **Skip expensive checks** - Use fast checks for frequent validation
- **Optimize file patterns** - Focus checks on changed files only
- **Use incremental validation** - Only validate modified content

## 🔄 CI/CD Integration

### GitHub Actions Integration

**Development Workflow:** `.github/workflows/development.yml`

```yaml
name: Development Quality Checks
on:
  pull_request:
    branches: [main]
  push:
    branches: [develop, feature/*]

jobs:
  quality-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Development Environment
        run: ./scripts/development/setup-dev-environment.sh --ci
        
      - name: Run All Quality Checks
        run: ./scripts/development/run-all-checks.sh --ci --report-format json
        
      - name: Upload Quality Report
        uses: actions/upload-artifact@v3
        with:
          name: quality-report
          path: reports/quality-report.json
```

### Pre-commit Hook Integration

**Hook Installation:**
```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run hooks manually
pre-commit run --all-files

# Update hooks
pre-commit autoupdate
```

## 📚 Related Documentation

- [Code Generation Guide](./code-generation/README.md)
- [Testing Framework Guide](./testing/README.md)
- [Linting and Quality Guide](./linting/README.md)
- [Development Setup Guide](../../docs/guides/DEVELOPMENT_SETUP.md) *(planned)*
- [Contributing Guide](../../CONTRIBUTING.md) *(planned)*

## 🤝 Contributing

### Adding New Development Scripts

1. **Identify development need** - Determine what development task needs automation
2. **Choose appropriate category** - code-generation, testing, or linting
3. **Follow development standards** - Use consistent patterns and error handling
4. **Include comprehensive testing** - Test scripts with various scenarios
5. **Add configuration support** - Make scripts configurable via environment variables
6. **Document thoroughly** - Update this README and category-specific READMEs
7. **Integrate with CI/CD** - Ensure scripts work in automated environments

### Script Requirements

- [ ] Follows naming conventions (`kebab-case.sh`)
- [ ] Includes proper header with metadata
- [ ] Has comprehensive error handling and logging
- [ ] Supports `--help`, `--dry-run`, and `--verbose` flags
- [ ] Is configurable via environment variables or config files
- [ ] Includes progress indicators for long-running operations
- [ ] Generates reports in multiple formats (text, JSON, HTML)
- [ ] Is tested with various input scenarios
- [ ] Integrates with existing development workflow
- [ ] Is documented in appropriate README files

## 📞 Support

For development script issues:

- **GitHub Issues:** [Create Development Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?labels=development)
- **Development Setup:** Check environment setup and dependency installation
- **Quality Issues:** Run individual linting tools for specific error details
- **Testing Issues:** Check test logs and validate individual components
- **CI/CD Issues:** Check GitHub Actions logs and workflow configuration
- **Team Contact:** CSA Documentation Team

---

**Last Updated:** January 28, 2025  
**Version:** 1.0.0  
**Maintainer:** CSA Documentation Team