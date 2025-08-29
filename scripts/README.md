# 🔧 Scripts Directory

> **🏠 [Home](../README.md)** | **📚 [Documentation](../docs/README.md)** | **📊 [Project Tracking](../project_tracking/README.md)**

---

## 📋 Overview

This directory contains automation and utility scripts for the Cloud Scale Analytics (CSA) in-a-Box documentation project. Scripts are organized by purpose to support setup, deployment, maintenance, and development workflows.

## 🗂️ Directory Structure

```
scripts/
├── 📄 README.md                    # This file - Scripts hub
│
├── 📁 setup/                       # Environment setup scripts
│   ├── 📄 README.md               # Setup scripts documentation
│   └── (setup scripts)
│
├── 📁 deployment/                  # Deployment automation
│   ├── 📄 README.md               # Deployment scripts documentation
│   ├── 📁 azure/                  # Azure-specific deployment
│   ├── 📁 docker/                 # Container deployment
│   └── 📁 kubernetes/             # K8s deployment
│
├── 📁 maintenance/                 # System maintenance scripts
│   ├── 📄 README.md               # Maintenance documentation
│   ├── 📁 database/               # Database maintenance
│   ├── 📁 cleanup/                # Cleanup operations
│   └── 📁 monitoring/             # Monitoring scripts
│
├── 📁 development/                 # Development utilities
│   ├── 📄 README.md               # Development tools documentation
│   ├── 📁 code-generation/        # Code generation
│   ├── 📁 testing/                # Test utilities
│   └── 📁 linting/                # Code quality
│
└── 📁 automation/                  # CI/CD and automation
    ├── 📄 README.md               # Automation documentation
    └── (automation scripts)
```

## 📂 Current Scripts

### Available Scripts

| Script | Location | Purpose | Usage |
|--------|----------|---------|-------|
| `enable-monitoring.sh` | Root | Enable Azure monitoring | `./enable-monitoring.sh` |

### Planned Scripts (To Be Created)

| Category | Script | Purpose | Priority |
|----------|--------|---------|----------|
| **Setup** | `setup-environment.sh` | Initialize development environment | HIGH |
| **Setup** | `install-dependencies.sh` | Install all dependencies | HIGH |
| **Deployment** | `deploy-docs.sh` | Deploy documentation site | MEDIUM |
| **Maintenance** | `validate-links.sh` | Check all documentation links | HIGH |
| **Development** | `run-linters.sh` | Run all linting tools | MEDIUM |

## 🚀 Quick Start

### Running Scripts

```bash
# Make script executable (first time only)
chmod +x scripts/script-name.sh

# Run script
./scripts/script-name.sh

# Or run with bash
bash scripts/script-name.sh
```

### Script Permissions

All scripts should have appropriate permissions:
```bash
# Set executable permission
chmod +x scripts/*.sh
chmod +x scripts/**/*.sh
```

## 📝 Script Standards

### Naming Conventions

- **Shell scripts**: Use kebab-case with `.sh` extension
  - Good: `setup-environment.sh`
  - Bad: `SetupEnvironment.sh`, `setup_environment.sh`

- **Python scripts**: Use snake_case with `.py` extension
  - Good: `validate_markdown.py`
  - Bad: `validate-markdown.py`, `ValidateMarkdown.py`

### Script Template

All scripts should include:

```bash
#!/bin/bash
#
# Script: script-name.sh
# Purpose: Brief description
# Usage: ./script-name.sh [options]
# Author: CSA Documentation Team
# Date: YYYY-MM-DD
#

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Functions
function usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -h, --help    Show this help message"
    exit 0
}

# Main logic
main() {
    echo "Starting script execution..."
    # Script logic here
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
    shift
done

# Execute main function
main "$@"
```

## 🔧 Available Scripts

### Setup Scripts (`/setup/`)

These scripts help initialize and configure the development environment.

**Planned scripts:**
- `setup-environment.sh` - Complete environment setup
- `install-python-deps.sh` - Install Python dependencies
- `configure-azure.sh` - Configure Azure credentials
- `init-local-env.sh` - Initialize local development

### Deployment Scripts (`/deployment/`)

Scripts for deploying documentation and related services.

**Current:**
- `enable-monitoring.sh` - Enable Azure monitoring (to be moved here)

**Planned:**
- `deploy-docs-site.sh` - Deploy MkDocs site
- `deploy-to-azure.sh` - Azure deployment
- `build-containers.sh` - Build Docker containers

### Maintenance Scripts (`/maintenance/`)

Scripts for ongoing maintenance and monitoring.

**Planned:**
- `check-links.sh` - Validate all documentation links
- `cleanup-temp.sh` - Clean temporary files
- `backup-docs.sh` - Backup documentation
- `update-dependencies.sh` - Update project dependencies

### Development Scripts (`/development/`)

Tools to support development workflow.

**Planned:**
- `run-tests.sh` - Execute test suite
- `lint-markdown.sh` - Lint markdown files
- `format-code.sh` - Format code files
- `generate-toc.sh` - Generate table of contents

### Automation Scripts (`/automation/`)

CI/CD and automation workflows.

**Planned:**
- `ci-pipeline.sh` - CI pipeline script
- `validate-pr.sh` - PR validation
- `release.sh` - Release automation

## 🎯 Usage Examples

### Example 1: Enable Monitoring

```bash
# Current location (to be moved)
./scripts/enable-monitoring.sh

# Future location
./scripts/deployment/azure/enable-monitoring.sh
```

### Example 2: Validate Documentation (Planned)

```bash
# Check all links
./scripts/maintenance/check-links.sh

# Lint markdown
./scripts/development/lint-markdown.sh

# Run all validations
./scripts/automation/validate-all.sh
```

## 📋 Best Practices

### Script Development

1. **Always include error handling**
   - Use `set -e` to exit on error
   - Use `set -u` to exit on undefined variables
   - Add proper error messages

2. **Make scripts idempotent**
   - Scripts should be safe to run multiple times
   - Check conditions before making changes

3. **Use configuration files**
   - Store settings in `.env` or config files
   - Never hardcode sensitive information

4. **Add comprehensive logging**
   - Log important operations
   - Include timestamps
   - Provide verbose mode option

5. **Include help documentation**
   - Add `--help` flag support
   - Document all options
   - Provide usage examples

### Security Considerations

- **Never commit secrets** in scripts
- **Use environment variables** for sensitive data
- **Validate input** parameters
- **Set appropriate permissions** (not world-writable)
- **Use secure communication** (HTTPS, SSH)

## 🔄 Maintenance

### Regular Tasks

- Review and update scripts monthly
- Test scripts after dependency updates
- Archive deprecated scripts
- Update documentation when scripts change

### Version Control

- Commit scripts with descriptive messages
- Tag stable script versions
- Document breaking changes
- Maintain backwards compatibility when possible

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Permission denied | Run `chmod +x script.sh` |
| Command not found | Check PATH or use full path |
| Syntax error | Check shell compatibility (bash vs sh) |
| Missing dependencies | Run setup/install scripts first |

### Debug Mode

Enable debug mode in scripts:
```bash
# Add to script
set -x  # Enable debug output

# Or run with debug
bash -x script.sh
```

## 📚 Related Documentation

- [Project Tracking](../project_tracking/README.md)
- [Documentation Hub](../docs/README.md)
- [Development Guide](../docs/guides/DEVELOPMENT_GUIDE.md) (when created)
- [Deployment Guide](../docs/deployment/README.md)

## 🤝 Contributing

### Adding New Scripts

1. Determine appropriate category
2. Create script in correct subdirectory
3. Follow naming conventions
4. Include standard header
5. Add documentation to README
6. Test thoroughly
7. Submit PR with description

### Script Requirements

- [ ] Follows naming conventions
- [ ] Includes proper header
- [ ] Has error handling
- [ ] Includes help text
- [ ] Is documented in README
- [ ] Has been tested
- [ ] Is executable (`chmod +x`)

## 📞 Support

For script-related issues:

- **GitHub Issues**: [Create Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues)
- **Documentation**: Check script header and help text
- **Team Contact**: CSA Documentation Team

---

**Last Updated:** January 28, 2025  
**Version:** 1.0.0  
**Maintainer:** CSA Documentation Team