# 🔧 Environment Setup Scripts

> **🏠 [Home](../../README.md)** | **📚 [Documentation](../../docs/README.md)** | **📜 [Scripts](../README.md)** | **📊 [Project Tracking](../../project_tracking/README.md)**

---

## 📋 Overview

This directory contains scripts for setting up and configuring the development environment for the Cloud Scale Analytics (CSA) in-a-Box documentation project. These scripts automate the initial setup process, dependency installation, and environment configuration.

## 🎯 Purpose

The setup scripts are designed to:

- **Initialize development environment** from a clean state
- **Install required dependencies** (Python, Node.js, documentation tools)
- **Configure Azure authentication** and credentials
- **Set up local environment variables** and configuration files
- **Validate environment setup** and readiness

## 📂 Current Scripts

### Available Scripts

Currently, no scripts exist in this directory. All scripts listed below are planned for implementation.

### Planned Scripts (To Be Created)

| Script | Purpose | Priority | Dependencies |
|--------|---------|----------|--------------|
| `setup-environment.sh` | Complete environment initialization | **HIGH** | bash, git |
| `install-python-deps.sh` | Install Python dependencies for documentation | **HIGH** | python3, pip |
| `install-node-deps.sh` | Install Node.js dependencies for tooling | **MEDIUM** | node, npm |
| `configure-azure.sh` | Set up Azure CLI and authentication | **MEDIUM** | azure-cli |
| `init-local-env.sh` | Create local environment files | **HIGH** | - |
| `validate-setup.sh` | Validate environment configuration | **MEDIUM** | - |
| `setup-pre-commit.sh` | Configure pre-commit hooks | **LOW** | pre-commit |

## 🚀 Usage Examples

### Complete Environment Setup

```bash
# Run complete setup (planned)
./scripts/setup/setup-environment.sh

# Or step by step
./scripts/setup/install-python-deps.sh
./scripts/setup/install-node-deps.sh
./scripts/setup/init-local-env.sh
./scripts/setup/validate-setup.sh
```

### Python Dependencies Only

```bash
# Install only Python dependencies
./scripts/setup/install-python-deps.sh

# With virtual environment
./scripts/setup/install-python-deps.sh --venv
```

### Azure Configuration

```bash
# Configure Azure authentication
./scripts/setup/configure-azure.sh

# Non-interactive mode
./scripts/setup/configure-azure.sh --non-interactive
```

## 📋 Planned Script Details

### `setup-environment.sh` (Priority: HIGH)

**Purpose:** Complete environment initialization from scratch

**Features:**
- Check system requirements
- Install system dependencies
- Set up Python virtual environment
- Install Python and Node.js dependencies
- Create environment files
- Configure git hooks
- Validate setup

**Usage:**
```bash
./setup-environment.sh [--clean] [--skip-validation]
```

### `install-python-deps.sh` (Priority: HIGH)

**Purpose:** Install Python dependencies for documentation tools

**Features:**
- Create/activate virtual environment
- Install MkDocs and plugins
- Install linting tools (markdownlint-cli2, etc.)
- Install documentation analysis tools

**Usage:**
```bash
./install-python-deps.sh [--venv venv-name] [--requirements file]
```

### `install-node-deps.sh` (Priority: MEDIUM)

**Purpose:** Install Node.js dependencies for documentation tooling

**Features:**
- Check Node.js version compatibility
- Install markdown linting tools
- Install documentation build tools
- Install development utilities

**Usage:**
```bash
./install-node-deps.sh [--global] [--dev-only]
```

### `configure-azure.sh` (Priority: MEDIUM)

**Purpose:** Set up Azure CLI and authentication

**Features:**
- Install Azure CLI if not present
- Configure Azure authentication
- Set up service principal (if provided)
- Test Azure connectivity
- Configure default subscription and resource group

**Usage:**
```bash
./configure-azure.sh [--service-principal] [--subscription id]
```

### `init-local-env.sh` (Priority: HIGH)

**Purpose:** Create and configure local environment files

**Features:**
- Create `.env` files from templates
- Set up local configuration
- Generate secure API keys
- Configure paths and directories

**Usage:**
```bash
./init-local-env.sh [--overwrite] [--template path]
```

### `validate-setup.sh` (Priority: MEDIUM)

**Purpose:** Validate environment configuration and readiness

**Features:**
- Check all required tools are installed
- Validate environment variables
- Test Azure connectivity
- Check file permissions
- Generate setup report

**Usage:**
```bash
./validate-setup.sh [--verbose] [--fix-permissions]
```

## 📋 Prerequisites

### System Requirements

- **Operating System:** Linux, macOS, or Windows with WSL2
- **Shell:** Bash 4.0+ 
- **Git:** 2.20+ for repository operations
- **Internet:** Connection required for dependency downloads

### Optional Dependencies

- **Python 3.8+:** For documentation tools and analysis
- **Node.js 16+:** For advanced tooling and linting
- **Azure CLI 2.50+:** For Azure integration features
- **Docker:** For containerized development (optional)

## 🔧 Configuration

### Environment Variables Template

The setup scripts will create environment files with these variables:

```bash
# Development Environment
ENVIRONMENT=development
DEBUG_MODE=true

# Documentation Paths
DOCS_ROOT=/path/to/csa-inabox-docs
BUILD_DIR=${DOCS_ROOT}/site
CONFIG_DIR=${DOCS_ROOT}/config

# Python Configuration
PYTHON_VERSION=3.9
VENV_DIR=${DOCS_ROOT}/venv
REQUIREMENTS_FILE=${DOCS_ROOT}/requirements.txt

# Node.js Configuration
NODE_VERSION=18
NPM_REGISTRY=https://registry.npmjs.org

# Azure Configuration (optional)
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=rg-csa-docs
AZURE_REGION=eastus

# Tool Configuration
MARKDOWNLINT_CONFIG=${DOCS_ROOT}/.markdownlint.json
PRETTIER_CONFIG=${DOCS_ROOT}/.prettierrc
```

### Setup Validation Checklist

The validation script will check:

- [ ] **System Tools:** git, bash, curl, wget
- [ ] **Python Environment:** python3, pip, venv
- [ ] **Node.js Environment:** node, npm (if using)
- [ ] **Azure Tools:** az cli, authentication (if using)
- [ ] **File Permissions:** Script execution permissions
- [ ] **Environment Files:** .env files created and valid
- [ ] **Directory Structure:** All required directories exist
- [ ] **Dependencies:** All required packages installed

## 🛠️ Development Standards

### Script Standards

All setup scripts must follow these standards:

1. **Idempotent operations** - Safe to run multiple times
2. **Error handling** - Proper error checking and rollback
3. **User feedback** - Clear progress indicators and messages
4. **Logging** - Log all operations for debugging
5. **Cross-platform** - Work on Linux, macOS, and WSL2

### Template Structure

```bash
#!/bin/bash
#
# Script: script-name.sh
# Purpose: Brief description
# Usage: ./script-name.sh [options]
# Author: CSA Documentation Team
# Date: 2025-01-28
#

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
LOG_FILE="${PROJECT_ROOT}/logs/setup.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}✓${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}✗${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1" | tee -a "$LOG_FILE"
}

cleanup() {
    # Cleanup on exit
    echo "Cleaning up..."
}

trap cleanup EXIT

# Main function
main() {
    echo "Starting setup process..."
    # Script logic here
    echo "Setup completed successfully!"
}

# Execute
main "$@"
```

## 🔍 Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|--------|----------|
| **Permission denied** | Script not executable | `chmod +x scripts/setup/*.sh` |
| **Python not found** | Python not installed | Install Python 3.8+ |
| **Virtual environment fails** | Insufficient permissions | Check directory permissions |
| **Azure CLI errors** | Authentication issues | Run `az login` manually |
| **Dependencies fail** | Network issues | Check internet connection |

### Debug Mode

Enable detailed debugging:

```bash
# Run with debug output
bash -x scripts/setup/setup-environment.sh

# Or set debug in script
export DEBUG=true
./scripts/setup/setup-environment.sh
```

### Log Files

Setup operations are logged to:
- **Main log:** `logs/setup.log`
- **Error log:** `logs/setup-error.log`
- **Verbose log:** `logs/setup-verbose.log` (if enabled)

## 📚 Related Documentation

- [Project Setup Guide](../../docs/guides/PROJECT_SETUP.md) *(planned)*
- [Development Environment](../../docs/guides/DEVELOPMENT_GUIDE.md) *(planned)*
- [Azure Integration](../../docs/guides/AZURE_INTEGRATION.md) *(planned)*
- [Troubleshooting Guide](../../docs/guides/TROUBLESHOOTING.md) *(planned)*

## 🤝 Contributing

### Adding New Setup Scripts

1. **Identify need:** Determine what setup task needs automation
2. **Follow template:** Use the standard script template
3. **Test thoroughly:** Test on clean environment
4. **Document:** Update this README with script details
5. **Submit PR:** Include tests and documentation

### Script Requirements

- [ ] Follows naming conventions (`kebab-case.sh`)
- [ ] Includes proper header with metadata
- [ ] Has comprehensive error handling
- [ ] Supports `--help` flag
- [ ] Is idempotent (safe to run multiple times)
- [ ] Includes cleanup on failure
- [ ] Is documented in this README
- [ ] Has been tested on target platforms

## 📞 Support

For setup-related issues:

- **GitHub Issues:** [Create Setup Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?labels=setup)
- **Documentation:** Check individual script `--help` output
- **Team Contact:** CSA Documentation Team

---

**Last Updated:** January 28, 2025  
**Version:** 1.0.0  
**Maintainer:** CSA Documentation Team