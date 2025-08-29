# 🔍 Linting and Code Quality Scripts

> **🏠 [Home](../../../README.md)** | **📚 [Documentation](../../../docs/README.md)** | **📜 [Scripts](../../README.md)** | **💻 [Development](../README.md)**

---

## 📋 Overview

This directory contains scripts for code quality checking, linting, and formatting across all file types in the Cloud Scale Analytics (CSA) in-a-Box documentation project. These scripts ensure consistent code style, catch potential issues, and maintain high-quality standards for all project files.

## 🎯 Purpose

The linting and code quality scripts are designed to:

- **Enforce consistent code style** across all file types and formats
- **Detect potential issues** in code, configuration, and documentation
- **Automate formatting** to maintain consistency without manual effort
- **Validate syntax and structure** for various file formats
- **Generate quality reports** to track and improve code health
- **Integrate with development workflow** for automated quality checks

## 📂 Current Scripts

### Available Scripts

Currently, no scripts exist in this directory. All scripts listed below are planned for implementation.

### Planned Scripts (To Be Created)

| Script | Purpose | Priority | File Types |
|--------|---------|----------|------------|
| `lint-all.sh` | Run all linting tools across project | **HIGH** | All |
| `format-code.sh` | Format all code and configuration files | **HIGH** | All |
| `lint-markdown.sh` | Lint markdown documentation files | **MEDIUM** | Markdown |
| `lint-yaml.sh` | Lint YAML configuration files | **MEDIUM** | YAML |
| `lint-scripts.sh` | Lint shell and Python scripts | **MEDIUM** | Scripts |
| `check-formatting.sh` | Check if files need formatting | **LOW** | All |
| `quality-report.sh` | Generate comprehensive quality report | **LOW** | All |

## 🚀 Planned Script Details

### `lint-all.sh` (Priority: HIGH)

**Purpose:** Execute comprehensive linting across all file types in the project

**Features:**
- Detect all file types automatically
- Run appropriate linters for each file type
- Support for parallel linting execution
- Generate unified quality report
- Auto-fix issues where possible
- Integration with CI/CD pipelines

**Planned Usage:**
```bash
./lint-all.sh [--fix] [--parallel] [--report-format format] [--file-types types]

# Examples
./lint-all.sh --fix --parallel  # Lint all files, fix issues, use parallel processing
./lint-all.sh --file-types "md,yml,sh" --report-format json
./lint-all.sh --ci --fail-on-error  # CI mode with non-zero exit on errors
```

**Supported File Types:**
```bash
# File type detection and linting
*.md        -> markdownlint, markdown-link-check
*.yml,*.yaml-> yamllint, yaml-validator  
*.json      -> jsonlint, jq validation
*.sh        -> shellcheck, shfmt
*.py        -> flake8, black, bandit
*.js        -> eslint, prettier
*.ts        -> tslint, prettier
*.css       -> stylelint, prettier
*.html      -> htmlhint, prettier
*.xml       -> xmllint
*.dockerfile-> hadolint
```

### `format-code.sh` (Priority: HIGH)

**Purpose:** Automatically format all code and configuration files to maintain consistency

**Features:**
- Format multiple file types with appropriate tools
- Preserve original files with backup option
- Support for custom formatting rules
- Integration with editor configurations
- Batch processing for large codebases

**Planned Usage:**
```bash
./format-code.sh [--check-only] [--backup] [--file-types types] [--config path]

# Examples
./format-code.sh --backup  # Format files and create backups
./format-code.sh --check-only  # Check formatting without changing files
./format-code.sh --file-types "md,yml" --config custom-config.yml
```

**Formatting Tools:**
```yaml
formatting_tools:
  markdown:
    tool: "prettier"
    config: ".prettierrc"
    options: "--prose-wrap always --print-width 120"
    
  yaml:
    tool: "prettier" 
    config: ".prettierrc"
    options: "--tab-width 2"
    
  json:
    tool: "jq"
    options: ". --indent 2 --sort-keys"
    
  shell:
    tool: "shfmt"
    options: "-i 2 -ci -bn"
    
  python:
    tool: "black"
    config: "pyproject.toml"
    options: "--line-length 120"
```

### `lint-markdown.sh` (Priority: MEDIUM)

**Purpose:** Comprehensive linting specifically for markdown documentation files

**Features:**
- Validate markdown syntax and structure
- Check heading hierarchy and consistency
- Validate links and references
- Check table formatting and structure
- Ensure consistent metadata and frontmatter

**Planned Usage:**
```bash
./lint-markdown.sh [--fix] [--config path] [--rules rules] [--exclude pattern]

# Examples
./lint-markdown.sh --fix --config .markdownlint.json
./lint-markdown.sh --rules "MD013,MD033" --exclude "node_modules/**"
```

**Markdown Rules Categories:**
```yaml
markdown_rules:
  structure:
    - MD001: "Heading levels should only increment by one level at a time"
    - MD003: "Heading style should be consistent"
    - MD022: "Headings should be surrounded by blank lines"
    
  formatting:
    - MD009: "Trailing spaces are not allowed"
    - MD010: "Hard tabs are not allowed"
    - MD012: "Multiple consecutive blank lines are not allowed"
    
  content:
    - MD013: "Line length should not exceed specified limit"
    - MD034: "Bare URL used instead of proper link syntax" 
    - MD045: "Images should have alternate text"
    
  links:
    - MD051: "Link fragments should be valid"
    - MD052: "Reference links should be valid"
```

### `lint-yaml.sh` (Priority: MEDIUM)

**Purpose:** Validate YAML configuration files for syntax and style consistency

**Features:**
- Validate YAML syntax and structure
- Check indentation and formatting consistency
- Validate against JSON schemas where available
- Detect common YAML pitfalls and errors
- Support for custom validation rules

**Planned Usage:**
```bash
./lint-yaml.sh [--schema path] [--strict] [--config path] [--fix-basic]

# Examples
./lint-yaml.sh --schema schemas/config.schema.json --strict
./lint-yaml.sh --fix-basic --config .yamllint.yml
```

**YAML Validation Rules:**
```yaml
yaml_rules:
  syntax:
    - "Valid YAML syntax"
    - "Proper key-value structure"
    - "Correct list and mapping formats"
    
  formatting:
    - "Consistent indentation (2 spaces)"
    - "No trailing whitespace"
    - "Proper line breaks"
    - "Quote consistency"
    
  structure:
    - "Alphabetical key ordering (where appropriate)"
    - "Consistent boolean values (true/false)"
    - "Proper null value handling"
    
  schemas:
    - "JSON Schema validation"
    - "Custom schema compliance"
    - "Required field validation"
```

### `lint-scripts.sh` (Priority: MEDIUM)

**Purpose:** Lint shell scripts and Python files for quality and security

**Features:**
- Shell script validation with shellcheck
- Python code quality with flake8/pylint
- Security scanning for common vulnerabilities
- Best practices enforcement
- Performance and maintainability checks

**Planned Usage:**
```bash
./lint-scripts.sh [--language lang] [--security] [--fix] [--severity level]

# Examples
./lint-scripts.sh --language bash --security --severity warning
./lint-scripts.sh --language python --fix --severity error
```

**Script Quality Checks:**
```bash
# Shell script checks (shellcheck)
SC2034: "Variable appears unused"
SC2086: "Double quote to prevent globbing"
SC2129: "Use >> instead of > for multiple lines"
SC2155: "Declare and assign separately"

# Python checks (flake8)
E501: "Line too long (>120 characters)"
W503: "Line break before binary operator"
F401: "Module imported but unused"
E302: "Expected 2 blank lines"

# Security checks (bandit for Python)
B101: "Use of assert detected"
B602: "Subprocess call with shell=True"
B108: "Probable insecure usage of temp file"
```

## 🔧 Linting Configuration

### Global Linting Configuration

**Configuration File:** `config/linting.yml`

```yaml
# Linting Configuration
linting:
  # General settings
  general:
    parallel_execution: true
    max_workers: 4
    fail_fast: false
    auto_fix: false
    
  # File discovery
  file_discovery:
    include_patterns:
      - "**/*.md"
      - "**/*.yml" 
      - "**/*.yaml"
      - "**/*.json"
      - "**/*.sh"
      - "**/*.py"
      
    exclude_patterns:
      - "node_modules/**"
      - ".git/**"
      - "venv/**"
      - "*.min.*"
      - "generated/**"
  
  # Tool configurations
  tools:
    # Markdown linting
    markdownlint:
      config_file: ".markdownlint.json"
      auto_fix: true
      severity: "warning"
      
    # YAML linting
    yamllint:
      config_file: ".yamllint.yml"
      strict: true
      
    # Shell script linting
    shellcheck:
      severity: "warning"
      shell: "bash"
      exclude_codes: ["SC1091"]  # Can't follow sourced files
      
    # Python linting
    flake8:
      config_file: "setup.cfg"
      max_line_length: 120
      ignore: ["W503", "E203"]
      
    # JSON linting
    jsonlint:
      strict: true
      sort_keys: true
      indent: 2
  
  # Quality standards
  quality:
    # Minimum quality scores
    thresholds:
      markdown: 95    # % of rules passed
      yaml: 100       # % of files valid
      shell: 90       # % of shellcheck rules passed  
      python: 85      # % of flake8 rules passed
      
    # Reporting
    report_formats: ["text", "json", "html"]
    include_metrics: true
    include_trends: true
```

### Tool-Specific Configurations

**Markdown Linting:** `.markdownlint.json`

```json
{
  "default": true,
  "line_length": {
    "line_length": 120,
    "heading_line_length": 80,
    "code_block_line_length": false
  },
  "MD013": {
    "line_length": 120,
    "heading_line_length": 80,
    "code_blocks": false,
    "tables": false
  },
  "MD033": {
    "allowed_elements": ["details", "summary", "br", "sub", "sup"]
  },
  "MD046": {
    "style": "fenced"
  }
}
```

**YAML Linting:** `.yamllint.yml`

```yaml
extends: default

rules:
  line-length:
    max: 120
    level: warning
    
  indentation:
    spaces: 2
    indent-sequences: true
    check-multi-line-strings: false
    
  key-ordering:
    level: warning
    
  truthy:
    allowed-values: ['true', 'false']
    check-keys: true
    
  comments:
    min-spaces-from-content: 2
    
ignore: |
  generated/
  node_modules/
  .git/
```

**Python Linting:** `setup.cfg`

```ini
[flake8]
max-line-length = 120
ignore = 
    W503,  # Line break before binary operator
    E203,  # Whitespace before ':'
    E501   # Line too long (handled by black)
    
exclude =
    .git,
    __pycache__,
    venv,
    build,
    dist,
    generated

per-file-ignores =
    __init__.py:F401  # Unused imports in __init__ files

[bandit]
exclude_dirs = tests,venv,build
```

## 📊 Quality Reports

### Linting Quality Report

**Comprehensive Quality Summary:**
```
Code Quality Report - 2025-01-28
Linting Suite: Full | Duration: 3m 45s | Status: ⚠️ WARNINGS

📊 Overall Quality Score: 92/100

📝 Markdown Files: ✅ EXCELLENT (98.7%)
- Total files: 156
- Rules passed: 154/156 (98.7%)
- Issues found: 3 (2 fixable)
- Common issues: Line length (MD013), HTML usage (MD033)

📋 YAML Files: ✅ EXCELLENT (100%)
- Total files: 23  
- Valid syntax: 23/23 (100%)
- Style compliance: 23/23 (100%)
- Schema validation: 20/20 applicable files (100%)

📜 Shell Scripts: ⚠️ GOOD (87.5%)
- Total files: 8
- Shellcheck passed: 7/8 (87.5%)
- Issues found: 12 (8 fixable)
- Common issues: Quoting (SC2086), Unused variables (SC2034)

🐍 Python Files: ⚠️ GOOD (89.3%)
- Total files: 14
- Flake8 passed: 12/14 (85.7%)
- Security scan: ✅ No high-risk issues
- Issues found: 23 (18 fixable)
- Common issues: Line length (E501), Import order (E402)

🔧 JSON Files: ✅ EXCELLENT (100%)
- Total files: 12
- Valid syntax: 12/12 (100%)
- Formatted correctly: 12/12 (100%)

📈 Quality Trends (vs last week):
- Overall score: 89/100 → 92/100 (↑3%)
- Fixable issues: 45 → 28 (↓38%)
- Critical issues: 2 → 0 (✅ resolved)

🔧 Auto-Fixable Issues: 28/42 (66.7%)
- Markdown formatting: 2 issues
- YAML formatting: 0 issues  
- Shell script formatting: 8 issues
- Python formatting: 18 issues

❌ Manual Fix Required: 14 issues
- Complex logic issues: 6
- Structural problems: 5
- Security considerations: 3

💡 Recommendations:
1. Run ./format-code.sh --fix to address 28 auto-fixable issues
2. Review shell scripts for quoting and variable usage
3. Consider using black for Python formatting
4. Add pre-commit hooks to prevent future issues

Next Quality Check: Scheduled for code changes or daily at 06:00
```

### Quality Metrics Dashboard

**Quality Trends Over Time:**
```bash
Code Quality Trends (Past 30 Days):

Overall Quality Score:
Week 1: 85% → Week 2: 87% → Week 3: 89% → Week 4: 92% (📈 +7%)

Issue Resolution:
- Total issues resolved: 67
- Auto-fixed issues: 45 (67%)
- Manually fixed issues: 22 (33%)
- New issues introduced: 12
- Net improvement: 55 issues

File Type Quality:
- Markdown: 94% → 98.7% (📈 +4.7%)
- YAML: 97% → 100% (📈 +3%)
- Shell: 82% → 87.5% (📈 +5.5%)  
- Python: 86% → 89.3% (📈 +3.3%)
- JSON: 100% → 100% (📊 stable)

Developer Adoption:
- Pre-commit hook usage: 78% of commits
- Auto-fix usage: 65% of linting runs
- Manual review completion: 91% of flagged issues

Top Quality Improvements:
1. Standardized markdown formatting (+15 points)
2. Fixed shell script quoting issues (+12 points)
3. Improved Python import ordering (+8 points)
4. Enhanced YAML consistency (+6 points)
```

## 🔧 Advanced Features

### Incremental Linting

**Change-Based Linting:**
```bash
# Lint only changed files
git diff --name-only HEAD~1 | xargs ./lint-all.sh --files-from-stdin

# Lint files changed in current branch
git diff --name-only main...HEAD | ./lint-all.sh --stdin

# Lint files with uncommitted changes
git diff --name-only | ./lint-all.sh --stdin
```

### Custom Rule Development

**Custom Linting Rules:**
```python
# custom_rules/markdown_custom.py
"""Custom markdown linting rules"""

def check_csa_specific_terms(line, line_number):
    """Check for CSA-specific terminology consistency"""
    terms = {
        'cloud scale analytics': 'Cloud Scale Analytics',
        'csa': 'CSA',
        'azure synapse': 'Azure Synapse Analytics'
    }
    
    for incorrect, correct in terms.items():
        if incorrect.lower() in line.lower() and correct not in line:
            return f"Line {line_number}: Use '{correct}' instead of '{incorrect}'"
    
    return None
```

### Integration with Development Tools

**VS Code Integration:**
```json
{
  "emeraldwalk.runonsave": {
    "commands": [
      {
        "match": "\\.md$",
        "cmd": "./scripts/development/linting/lint-markdown.sh --fix ${file}"
      },
      {
        "match": "\\.ya?ml$", 
        "cmd": "./scripts/development/linting/lint-yaml.sh --fix ${file}"
      }
    ]
  }
}
```

## 🔍 Troubleshooting

### Common Linting Issues

| Issue | Symptoms | Cause | Solution |
|-------|----------|--------|----------|
| **False positives** | Valid code flagged as error | Overly strict rules or tool bugs | Adjust rule configuration or add exceptions |
| **Tool not found** | Linter command fails | Tool not installed or not in PATH | Install required tools or update PATH |
| **Configuration conflicts** | Inconsistent results between tools | Conflicting configuration files | Standardize configuration across tools |
| **Performance issues** | Linting takes too long | Large files or inefficient rules | Use parallel processing, optimize rules |
| **Encoding issues** | Linter fails on special characters | File encoding problems | Ensure UTF-8 encoding for all files |

### Debug Commands

```bash
# Test individual linters
markdownlint --config .markdownlint.json docs/README.md
yamllint --config .yamllint.yml config/development.yml
shellcheck scripts/setup/install-deps.sh
flake8 --config setup.cfg src/

# Check tool versions and availability
markdownlint --version && yamllint --version && shellcheck --version

# Validate configuration files
markdownlint --config .markdownlint.json --help
yamllint --config .yamllint.yml --help

# Debug specific rules
markdownlint --config .markdownlint.json --disable MD013 docs/
flake8 --select E501 src/
```

### Performance Optimization

**Linting Performance Tips:**
- **Use parallel processing** - Run multiple linters simultaneously
- **Exclude unnecessary files** - Use .gitignore patterns to skip files
- **Cache results** - Skip linting unchanged files
- **Optimize rule sets** - Disable expensive rules for large files
- **Use incremental linting** - Only lint changed files in CI/CD

## 📚 Related Documentation

- [Code Style Guide](../../../docs/guides/CODE_STYLE_GUIDE.md) *(planned)*
- [Quality Standards](../../../docs/guides/QUALITY_STANDARDS.md) *(planned)*
- [Pre-commit Hooks Guide](../../../docs/guides/PRECOMMIT_HOOKS.md) *(planned)*
- [Development Scripts Overview](../README.md)
- [Testing Scripts Guide](../testing/README.md)

## 🤝 Contributing

### Adding New Linting Scripts

1. **Identify linting need** - Determine what file type or quality aspect needs checking
2. **Choose appropriate tools** - Select industry-standard linters for the file type
3. **Configure rules properly** - Balance strictness with practicality
4. **Add auto-fix capability** - Implement automatic fixing where safe
5. **Include comprehensive reporting** - Provide detailed, actionable feedback
6. **Test with real codebase** - Validate rules work with actual project files
7. **Update documentation** - Update this README with script details

### Script Requirements

- [ ] Supports multiple file types or focuses on specific type
- [ ] Has configurable rules and severity levels
- [ ] Includes auto-fix capability where appropriate
- [ ] Generates detailed reports with line numbers and descriptions
- [ ] Supports parallel processing for performance
- [ ] Has comprehensive error handling and logging
- [ ] Includes dry-run mode for validation
- [ ] Is tested with various file scenarios
- [ ] Integrates with existing development workflow
- [ ] Is documented in this README file

## 📞 Support

For linting and code quality issues:

- **GitHub Issues:** [Create Linting Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?labels=linting,development)
- **Rule Configuration:** Check tool documentation for specific rule details
- **Performance Issues:** Use profiling and optimization techniques
- **Tool Issues:** Check tool versions and installation
- **False Positives:** Review rule configuration and add exceptions as needed
- **Team Contact:** CSA Documentation Team

---

**Last Updated:** January 28, 2025  
**Version:** 1.0.0  
**Maintainer:** CSA Documentation Team