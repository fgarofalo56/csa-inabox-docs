# Installation Guide

> **[Home](../README.md)** | **Installation**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Language](https://img.shields.io/badge/Language-en--US-blue?style=flat-square)

Installation guide for Cloud Scale Analytics documentation site.

---

## Prerequisites

Before installing, ensure you have:

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Node.js (optional, for advanced features)

---

## Quick Start

### Clone Repository

```bash
git clone https://github.com/your-org/csa-inabox-docs.git
cd csa-inabox-docs
```

### Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Run Locally

```bash
# Start development server
mkdocs serve

# Access at http://localhost:8000
```

---

## Production Deployment

### Build Site

```bash
# Build static site
mkdocs build

# Output in /site directory
```

### Deploy to Azure

```bash
# Using Azure Static Web Apps
az staticwebapp create \
    --name csa-docs \
    --resource-group rg-docs \
    --source ./site \
    --branch main
```

---

## Configuration

### mkdocs.yml

```yaml
site_name: CSA in-a-Box Documentation
site_url: https://docs.example.com
repo_url: https://github.com/your-org/csa-inabox-docs

theme:
  name: material
  language: en
  features:
    - navigation.tabs
    - navigation.sections
    - search.suggest
    - content.code.copy

plugins:
  - search
  - i18n:
      default_language: en
      languages:
        - locale: en
          name: English
        - locale: fr
          name: Français
        - locale: de
          name: Deutsch
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Port in use | Use `mkdocs serve -a localhost:8001` |
| Missing dependencies | Run `pip install -r requirements.txt` |
| Build errors | Check YAML syntax in mkdocs.yml |

---

## Related Documentation

- [Contributing Guide](../guides/CONTRIBUTING_GUIDE.md)
- [Development Guide](../guides/DEVELOPMENT_GUIDE.md)
- [Markdown Style Guide](../guides/MARKDOWN_STYLE_GUIDE.md)

---

*Last Updated: January 2025*
