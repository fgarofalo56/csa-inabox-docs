# Documentation Tools

This directory contains utility tools for maintaining and validating the Azure Synapse Analytics documentation.

## Available Tools

### Link Checker (`link_checker.py`)

A Python utility that scans all Markdown files in the documentation project, extracts links, and verifies that they are working properly. It checks both internal relative links and external URLs.

#### Features

- Validates all internal relative links between documentation files
- Tests external URLs to ensure they're accessible
- Detects broken links and generates a detailed report
- Handles various link formats including standard markdown links and reference-style links
- Parallel processing for faster execution


#### Requirements

- Python 3.6+
- `requests` library (`pip install requests`)


#### Usage

```bash
# Navigate to the tools directory
cd project_tracking/tools

# Run the link checker on the project root
python link_checker.py ../..

# Alternatively, specify a different root directory
python link_checker.py /path/to/project
```


#### Output

- Console output with progress and warnings
- A detailed markdown report saved to `project_tracking/planning/link_check_report.md`

### Automated Link Checking

The link checker has been configured to run automatically through GitHub Actions. This ensures documentation links remain valid over time without manual intervention.

#### Automation Schedule

- **On code push**: Runs automatically when changes are pushed to the main branch
- **On pull requests**: Validates documentation in proposed changes
- **Weekly check**: Runs every Monday at 9:00 AM to detect external links that may have broken
- **Manual trigger**: Can be executed on-demand through GitHub Actions interface


#### Workflow Process

1. The GitHub workflow defined in `.github/workflows/link-checker.yml` executes the link checker
2. If broken links are detected:
   - A detailed report is generated in `project_tracking/planning/link_check_report.md`
   - A GitHub issue is created or updated with the broken link information
   - Appropriate labels (`broken-links`, `documentation`, `bug`) are applied


#### Monitoring and Maintenance

- Review the link check report after significant documentation updates
- Check the GitHub repository issues for any automatically created broken link reports
- Fix broken links promptly to maintain documentation integrity

## Adding New Tools

When adding new tools to this directory:

1. Create a descriptive name for your script
2. Add proper documentation including usage instructions
3. Update this README with information about the new tool
4. Ensure the tool follows project coding standards

## 🔗 CSA Documentation Tools Integration

This directory now includes integration with the unified CSA Documentation Tools located in the `/tools` directory. The unified tooling provides a comprehensive Node.js-based solution for documentation management.

### New Integrated Tools

#### `csa-docs-integration.py`
Python wrapper for the unified CSA Documentation Tools:
```bash
# Run documentation audit
python csa-docs-integration.py audit --format json

# Check documentation health
python csa-docs-integration.py health --threshold 80

# Run complete build pipeline
python csa-docs-integration.py build
```

#### `enhanced_link_checker.py`
Enhanced link checker that combines legacy Python tools with new CSA tools:
```bash
# Run comprehensive link check with both tools
python enhanced_link_checker.py --use-legacy --external

# Quick health check for CI/CD
python enhanced_link_checker.py --quick-health

# Generate detailed report
python enhanced_link_checker.py --output-format markdown --output-file report.md
```

#### `integrated_docs_workflow.py`
Complete documentation workflow combining all tools:
```bash
# Run full integrated workflow
python integrated_docs_workflow.py --include-external --serve-docs

# Run specific steps
python integrated_docs_workflow.py --audit-only
python integrated_docs_workflow.py --fix-only

# Save workflow report
python integrated_docs_workflow.py --output-report workflow-report.json
```

### Migration Guide

The unified tooling replaces several individual JavaScript utilities:

| Old Tool | New Command | Description |
|----------|-------------|-------------|
| `comprehensive-audit.js` | `csa-docs audit` | Documentation quality audit |
| `generate-diagrams.js` | `csa-docs generate-diagrams` | Mermaid to PNG conversion |
| `replace-mermaid.js` | `csa-docs replace-mermaid` | Replace Mermaid with PNG refs |
| `fix-documentation-issues.js` | `csa-docs fix-issues` | Automated issue fixes |

### Installation

To use the integrated tooling:

1. **Install Node.js dependencies:**
   ```bash
   cd tools
   npm install
   npm install -g @mermaid-js/mermaid-cli
   ```

2. **Make CLI executable:**
   ```bash
   chmod +x tools/src/bin/csa-docs.js
   ```

3. **Test integration:**
   ```bash
   python project_tracking/tools/csa-docs-integration.py info
   ```

### CI/CD Integration

Update your CI/CD pipelines to use the new integrated workflow:

```yaml
- name: Run Documentation Validation
  run: |
    cd project_tracking/tools
    python integrated_docs_workflow.py --output-report validation-report.json
    
    # Check health score
    python enhanced_link_checker.py --quick-health
```

### Benefits of Integration

- **Unified Interface**: Single CLI for all documentation operations
- **Better Error Handling**: Comprehensive error reporting and logging
- **Clean Architecture**: Separation of concerns with domain/infrastructure layers
- **Type Safety**: TypeScript definitions for better maintainability
- **Comprehensive Testing**: Unit tests with >80% coverage
- **Rich Reporting**: JSON and markdown report formats

### Backward Compatibility

All existing Python tools continue to work as before. The integration layer provides:
- **Wrapper functions** for existing workflows
- **Enhanced capabilities** through CSA tools integration
- **Gradual migration path** from old to new tools

