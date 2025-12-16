# 🚀 Development Guide

> __🏠 [Home](../../README.md)__ | __📚 Documentation__ | __📖 [Guides](./README.md)__

---

## 📋 Overview

This guide provides comprehensive instructions for developers working on the Cloud Scale Analytics (CSA) in-a-Box documentation project. It covers environment setup, development workflows, coding standards, and best practices.

## 📑 Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Debugging](#debugging)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

---

## 📋 Prerequisites

### System Requirements

| Component | Minimum Version | Recommended Version | Notes |
|-----------|----------------|-------------------|--------|
| __Python__ | 3.8+ | 3.11+ | Required for documentation tools |
| __Node.js__ | 14.x | 18.x LTS | For markdown linting |
| __Git__ | 2.25+ | Latest | Version control |
| __Docker__ | 20.10+ | Latest | Optional for containerized development |

### Required Software

```bash
# Check Python version
python --version  # Should be 3.8+

# Check Node.js version
node --version    # Should be 14+

# Check Git version
git --version     # Should be 2.25+

# Check pip version
pip --version     # Should be recent
```

### Azure Prerequisites

- __Azure Subscription__ (for deployment and testing)
- __Azure CLI__ installed and configured
- __Service Principal__ with appropriate permissions
- __Azure DevOps__ access (optional)

---

## 🛠️ Environment Setup

### 1. Clone the Repository

```bash
# Clone via HTTPS
git clone https://github.com/fgarofalo56/csa-inabox-docs.git

# Or clone via SSH
git clone git@github.com:fgarofalo56/csa-inabox-docs.git

# Navigate to project directory
cd csa-inabox-docs
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Verify activation
which python  # Should point to venv/bin/python
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-test.txt

# Install Node.js dependencies (for linting)
npm install -g markdownlint-cli
```

### 4. Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# Required variables:
# - AZURE_SUBSCRIPTION_ID
# - AZURE_TENANT_ID
# - AZURE_CLIENT_ID
# - AZURE_CLIENT_SECRET
```

### 5. Verify Installation

```bash
# Run validation script
python src/csa_docs_tools/cli.py validate --all

# Serve documentation locally
mkdocs serve

# Open browser to http://localhost:8000
```

---

## 📁 Project Structure

### Key Directories

```text
csa-inabox-docs/
├── docs/                  # Documentation content
│   ├── guides/           # Development guides
│   ├── architecture/     # Architecture docs
│   └── ...
├── src/                  # Source code
│   └── csa_docs_tools/  # Documentation tools
├── tests/               # Test suites
├── scripts/            # Automation scripts
├── project_tracking/   # Project management
└── site/              # Generated documentation
```

### Important Files

| File | Purpose |
|------|---------|
| `mkdocs.yml` | MkDocs configuration |
| `pyproject.toml` | Python project configuration |
| `requirements.txt` | Python dependencies |
| `.markdownlint.json` | Markdown linting rules |
| `CLAUDE.md` | AI agent development rules |

---

## 🔄 Development Workflow

### 1. Create Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name

# Naming conventions:
# - feature/add-azure-guide
# - fix/broken-links
# - docs/update-readme
# - refactor/reorganize-structure
```

### 2. Make Changes

Follow these guidelines:

1. __Check existing documentation__ before creating new files
2. __Follow directory structure__ from [DIRECTORY_STRUCTURE_GUIDE.md](./DIRECTORY_STRUCTURE_GUIDE.md)
3. __Apply markdown standards__ from [MARKDOWN_STYLE_GUIDE.md](./MARKDOWN_STYLE_GUIDE.md)
4. __Update navigation__ in `mkdocs.yml` if adding new pages
5. __Add/update tests__ for any code changes

### 3. Test Changes

```bash
# Run markdown linter
markdownlint "**/*.md" -c .markdownlint.json

# Run link validator
python src/csa_docs_tools/cli.py validate-links

# Run all tests
pytest tests/

# Build documentation
mkdocs build

# Serve locally and review
mkdocs serve
```

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add Azure Synapse performance guide

- Add performance optimization techniques
- Include code examples
- Update navigation in mkdocs.yml"

# Push to remote
git push origin feature/your-feature-name
```

### 5. Create Pull Request

1. Go to GitHub repository
2. Click "New Pull Request"
3. Select your branch
4. Fill out PR template
5. Request reviews
6. Address feedback
7. Merge when approved

---

## 📝 Coding Standards

### Python Code Standards

```python
"""
Module docstring describing purpose.
"""
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class DocumentValidator:
    """Validates documentation files."""
    
    def __init__(self, config: dict) -> None:
        """Initialize validator with configuration.
        
        Args:
            config: Validation configuration dictionary
        """
        self.config = config
    
    def validate_file(self, file_path: str) -> bool:
        """Validate a single file.
        
        Args:
            file_path: Path to file to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Implementation
            return True
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return False
```

### Markdown Standards

```markdown
# Document Title

> **Navigation breadcrumb**

## Overview

Brief description with **bold** and *italic* text.

## Section with Code

\```python
# Code example with syntax highlighting
def example():
    return "Hello, World!"
\```

## Table Example

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |

## Links

- [External link](https://azure.microsoft.com)
\```

### Shell Script Standards

```bash
#!/bin/bash
#
# Script: example-script.sh
# Purpose: Demonstrate script standards
#

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Functions
main() {
    echo "Running script..."
    # Implementation
}

# Execute
main "$@"
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/unit/test_link_validator.py

# Run with coverage
pytest --cov=src/csa_docs_tools tests/

# Run with verbose output
pytest -v tests/

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/
```

### Writing Tests

```python
"""Test module for example functionality."""
import pytest
from csa_docs_tools.validator import Validator


class TestValidator:
    """Test cases for Validator class."""
    
    @pytest.fixture
    def validator(self):
        """Create validator instance."""
        return Validator()
    
    def test_validate_valid_file(self, validator):
        """Test validation of valid file."""
        result = validator.validate("valid.md")
        assert result is True
    
    def test_validate_invalid_file(self, validator):
        """Test validation of invalid file."""
        result = validator.validate("invalid.md")
        assert result is False
```

---

## 📚 Documentation

### Adding New Documentation

1. __Determine location__ using [DIRECTORY_STRUCTURE_GUIDE.md](./DIRECTORY_STRUCTURE_GUIDE.md)
2. __Create markdown file__ following [MARKDOWN_STYLE_GUIDE.md](./MARKDOWN_STYLE_GUIDE.md)
3. __Update navigation__ in `mkdocs.yml`
4. __Add cross-references__ to related documents
5. __Test locally__ with `mkdocs serve`

### Documentation Types

| Type | Location | Template |
|------|----------|----------|
| Guides | `/docs/guides/` | Guide template |
| API Docs | `/docs/api/` | API template |
| Architecture | `/docs/architecture/` | Architecture template |
| Tutorials | `/docs/tutorials/` | Tutorial template |

---

## 🐛 Debugging

### Common Issues

| Issue | Solution |
|-------|----------|
| Import errors | Check virtual environment activation |
| Module not found | Verify PYTHONPATH includes project root |
| Markdown errors | Run markdownlint and fix issues |
| Broken links | Use link validator tool |
| Build failures | Check mkdocs.yml syntax |

### Debug Tools

```bash
# Debug Python code
python -m pdb script.py

# Debug shell scripts
bash -x script.sh

# Check markdown syntax
markdownlint file.md --verbose

# Validate links
python src/csa_docs_tools/cli.py validate-links --verbose
```

---

## 🚀 Deployment

### Local Deployment

```bash
# Build documentation
mkdocs build

# Serve locally
mkdocs serve
# Access at http://localhost:8000

# Build with strict mode
mkdocs build --strict
```

### GitHub Pages Deployment

```bash
# Deploy to GitHub Pages
mkdocs gh-deploy

# Deploy specific version
mike deploy 1.0 latest --update-aliases

# List deployed versions
mike list
```

### Azure Static Web Apps

```bash
# Build for production
mkdocs build --clean

# Deploy to Azure
az staticwebapp deploy \
  --app-location "site" \
  --output-location "" \
  --name "csa-docs"
```

---

## 🔧 Troubleshooting

### Environment Issues

```bash
# Reset virtual environment
deactivate
rm -rf venv/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Git Issues

```bash
# Reset to clean state
git reset --hard HEAD
git clean -fd

# Fix line endings
git config core.autocrlf true  # Windows
git config core.autocrlf input # macOS/Linux
```

### Build Issues

```bash
# Clean build
rm -rf site/
mkdocs build --clean

# Verbose build
mkdocs build --verbose

# Check configuration
python -m mkdocs.config
```

---

## 📚 Resources

### Internal Documentation

- [Directory Structure Guide](./DIRECTORY_STRUCTURE_GUIDE.md)
- [Markdown Style Guide](./MARKDOWN_STYLE_GUIDE.md)
- [Testing Guide](./TESTING_GUIDE.md)
- [Contributing Guide](./CONTRIBUTING_GUIDE.md)

### External Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Python Documentation](https://docs.python.org/)
- [Azure Documentation](https://docs.microsoft.com/azure/)
- [Markdown Guide](https://www.markdownguide.org/)

### Tools and Extensions

#### VS Code Extensions

- Python
- Markdown All in One
- markdownlint
- Azure Tools
- GitLens

#### Command Line Tools

- `mkdocs` - Documentation generator
- `markdownlint` - Markdown linter
- `pytest` - Testing framework
- `ruff` - Python linter
- `black` - Code formatter

---

## 🤝 Getting Help

### Support Channels

- __GitHub Issues__: [Create Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues)
- __Discussions__: [GitHub Discussions](https://github.com/fgarofalo56/csa-inabox-docs/discussions)
- __Team Slack__: #csa-documentation
- __Email__: <csa-docs@microsoft.com>

### Useful Commands

```bash
# Get help for CLI tools
python src/csa_docs_tools/cli.py --help

# MkDocs help
mkdocs --help

# Markdown lint help
markdownlint --help

# Pytest help
pytest --help
```

---

__Last Updated:__ January 28, 2025  
__Version:__ 1.0.0  
__Maintainer:__ CSA Documentation Team
