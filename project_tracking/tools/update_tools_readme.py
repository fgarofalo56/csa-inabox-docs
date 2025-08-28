#!/usr/bin/env python3
"""
Update the project_tracking/tools/README.md to include information about
the new unified CSA Documentation Tools integration
"""

from pathlib import Path
import sys


def update_tools_readme():
    """Update the tools README with integration information."""
    
    readme_path = Path(__file__).parent / "README.md"
    
    # Read existing README if it exists
    existing_content = ""
    if readme_path.exists():
        existing_content = readme_path.read_text()
    
    # New content to add about the unified tooling
    new_section = """
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

"""
    
    # Check if integration section already exists
    if "CSA Documentation Tools Integration" in existing_content:
        print("ℹ️  Integration section already exists in README.md")
        return
    
    # Add the new section
    if existing_content.strip():
        # Append to existing README
        updated_content = existing_content.rstrip() + "\n" + new_section
    else:
        # Create new README with header
        updated_content = f"""# Project Planning Tools

This directory contains tools for managing and validating the CSA documentation project.

{new_section}
"""
    
    # Write updated README
    readme_path.write_text(updated_content)
    print(f"✅ Updated {readme_path} with CSA Documentation Tools integration info")


def main():
    """Main entry point."""
    try:
        update_tools_readme()
        print("\n📋 Next steps:")
        print("1. Review the updated README.md")
        print("2. Test the integration tools")
        print("3. Update your CI/CD pipelines")
        print("4. Train team members on new workflow")
    except Exception as e:
        print(f"❌ Failed to update README: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()