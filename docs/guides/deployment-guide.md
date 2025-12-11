# Deployment Guide

> **Home [Home](../../README.md)** | **Documentation** | **Guides [Guides](./README.md)**

---

## Overview

This guide provides comprehensive deployment procedures for the CSA-in-a-Box documentation infrastructure, including local development, staging, and production deployments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Deployment](#local-deployment)
- [Staging Deployment](#staging-deployment)
- [Production Deployment](#production-deployment)
- [Azure Static Web Apps](#azure-static-web-apps)
- [GitHub Pages](#github-pages)
- [Continuous Deployment](#continuous-deployment)
- [Rollback Procedures](#rollback-procedures)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Tools

| Tool | Version | Purpose | Installation |
|------|---------|---------|--------------|
| **Python** | 3.8+ | Runtime environment | [Download](https://python.org) |
| **Git** | Latest | Version control | [Download](https://git-scm.com) |
| **Azure CLI** | Latest | Azure deployments | [Download](https://learn.microsoft.com/cli/azure/install-azure-cli) |
| **MkDocs** | 1.5+ | Documentation generator | `pip install mkdocs` |

### Required Permissions

- **GitHub**: Write access to repository
- **Azure**: Contributor role on resource group
- **Azure DevOps**: Build and release pipeline permissions

---

## Local Deployment

### Quick Start

```bash
# Clone repository
git clone https://github.com/fgarofalo56/csa-inabox-docs.git
cd csa-inabox-docs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Serve documentation locally
mkdocs serve
```

### Local Configuration

**mkdocs.yml** - Development settings:

```yaml
site_name: CSA-in-a-Box Documentation
site_url: http://localhost:8000
dev_addr: 127.0.0.1:8000

theme:
  name: material
  palette:
    scheme: default
```

### Accessing Local Site

- **URL**: `http://localhost:8000`
- **Admin**: No authentication required
- **Live Reload**: Enabled by default

---

## Staging Deployment

### Staging Environment

**Purpose:** Pre-production validation and testing

**Infrastructure:**

```yaml
Environment: Staging
URL: https://csa-docs-staging.azurewebsites.net
Region: East US 2
Resource Group: rg-csa-docs-staging
```

### Deploy to Staging

```bash
# Build documentation
mkdocs build --clean --strict

# Validate build output
ls -la site/

# Deploy to staging (Azure Static Web Apps)
az staticwebapp deploy \
  --name csa-docs-staging \
  --resource-group rg-csa-docs-staging \
  --source ./site \
  --token $AZURE_STATIC_WEB_APPS_API_TOKEN
```

### Staging Validation

```bash
# Run validation tests
pytest tests/integration/

# Check site health
curl -I https://csa-docs-staging.azurewebsites.net

# Validate links
python scripts/maintenance/link_checker.py --url https://csa-docs-staging.azurewebsites.net
```

---

## Production Deployment

### Production Environment

**Infrastructure:**

```yaml
Environment: Production
URL: https://csa-docs.azurewebsites.net
Region: East US 2 (Primary), West US 2 (Failover)
Resource Group: rg-csa-docs-prod
CDN: Azure Front Door
```

### Pre-Deployment Checklist

- [ ] All tests pass in staging
- [ ] Documentation reviewed and approved
- [ ] Breaking changes documented
- [ ] Rollback plan prepared
- [ ] Stakeholders notified

### Production Deployment Steps

#### 1. Build Production Artifacts

```bash
# Set production environment
export ENVIRONMENT=production

# Build optimized documentation
mkdocs build --clean --strict

# Compress assets
python scripts/maintenance/compress_assets.py

# Generate sitemap
mkdocs build --clean
```

#### 2. Deploy to Azure

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "CSA-in-a-Box-Prod"

# Deploy to production
az staticwebapp deploy \
  --name csa-docs-prod \
  --resource-group rg-csa-docs-prod \
  --source ./site \
  --token $AZURE_STATIC_WEB_APPS_API_TOKEN_PROD
```

#### 3. Post-Deployment Validation

```bash
# Verify deployment
curl -I https://csa-docs.azurewebsites.net

# Run smoke tests
pytest tests/smoke/

# Validate SEO
python scripts/maintenance/seo_validator.py

# Check performance
python scripts/maintenance/performance_check.py
```

---

## Azure Static Web Apps

### Infrastructure Setup

```bash
# Create resource group
az group create \
  --name rg-csa-docs-prod \
  --location eastus2

# Create static web app
az staticwebapp create \
  --name csa-docs-prod \
  --resource-group rg-csa-docs-prod \
  --source https://github.com/fgarofalo56/csa-inabox-docs \
  --location eastus2 \
  --branch main \
  --app-location "/" \
  --output-location "site"
```

### Configuration

**staticwebapp.config.json:**

```json
{
  "routes": [
    {
      "route": "/*",
      "headers": {
        "Cache-Control": "public, max-age=3600",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY"
      }
    }
  ],
  "navigationFallback": {
    "rewrite": "/404.html"
  },
  "responseOverrides": {
    "404": {
      "rewrite": "/404.html",
      "statusCode": 404
    }
  },
  "mimeTypes": {
    ".json": "application/json",
    ".woff2": "font/woff2"
  }
}
```

---

## GitHub Pages

### Alternative Deployment

```bash
# Build documentation
mkdocs build --clean

# Deploy to GitHub Pages
mkdocs gh-deploy --force
```

### GitHub Pages Configuration

**.github/workflows/deploy-docs.yml:**

```yaml
name: Deploy Documentation

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Build documentation
        run: mkdocs build --clean --strict

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

---

## Continuous Deployment

### Azure DevOps Pipeline

**azure-pipelines.yml:**

```yaml
trigger:
  branches:
    include:
      - main
      - dev

pool:
  vmImage: 'ubuntu-latest'

variables:
  pythonVersion: '3.11'

stages:
- stage: Build
  displayName: 'Build Documentation'
  jobs:
  - job: BuildJob
    displayName: 'Build and Test'
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '$(pythonVersion)'

    - script: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
      displayName: 'Install dependencies'

    - script: |
        pytest tests/
      displayName: 'Run tests'

    - script: |
        mkdocs build --clean --strict
      displayName: 'Build documentation'

    - task: PublishBuildArtifacts@1
      inputs:
        PathtoPublish: 'site'
        ArtifactName: 'documentation'

- stage: DeployStaging
  displayName: 'Deploy to Staging'
  dependsOn: Build
  condition: eq(variables['Build.SourceBranch'], 'refs/heads/dev')
  jobs:
  - deployment: DeployStaging
    environment: 'staging'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureStaticWebApp@0
            inputs:
              app_location: '$(Pipeline.Workspace)/documentation'
              azure_static_web_apps_api_token: $(STAGING_DEPLOY_TOKEN)

- stage: DeployProduction
  displayName: 'Deploy to Production'
  dependsOn: Build
  condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
  jobs:
  - deployment: DeployProduction
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureStaticWebApp@0
            inputs:
              app_location: '$(Pipeline.Workspace)/documentation'
              azure_static_web_apps_api_token: $(PRODUCTION_DEPLOY_TOKEN)
```

---

## Rollback Procedures

### Immediate Rollback

```bash
# List recent deployments
az staticwebapp deployment list \
  --name csa-docs-prod \
  --resource-group rg-csa-docs-prod

# Rollback to previous version
az staticwebapp deployment rollback \
  --name csa-docs-prod \
  --resource-group rg-csa-docs-prod \
  --deployment-id <previous-deployment-id>
```

### Git Rollback

```bash
# Identify last good commit
git log --oneline -10

# Revert to previous commit
git revert <commit-hash>

# Force push (use with caution)
git push origin main --force

# Trigger redeployment
mkdocs gh-deploy --force
```

---

## Troubleshooting

### Common Issues

#### Build Failures

**Problem:** MkDocs build fails with errors

**Solution:**

```bash
# Check configuration
mkdocs build --strict --verbose

# Validate mkdocs.yml
python -c "import yaml; yaml.safe_load(open('mkdocs.yml'))"

# Check for broken links
python scripts/maintenance/link_checker.py
```

#### Deployment Failures

**Problem:** Azure deployment fails

**Solution:**

```bash
# Check Azure CLI version
az --version

# Re-authenticate
az login --use-device-code

# Verify permissions
az role assignment list --assignee $(az account show --query user.name -o tsv)

# Check deployment logs
az staticwebapp logs show \
  --name csa-docs-prod \
  --resource-group rg-csa-docs-prod
```

#### Performance Issues

**Problem:** Slow site load times

**Solution:**

```bash
# Enable CDN caching
az cdn endpoint update \
  --name csa-docs \
  --profile-name csa-cdn \
  --resource-group rg-csa-docs-prod \
  --query-string-caching-behavior IgnoreQueryString

# Compress assets
python scripts/maintenance/compress_assets.py

# Optimize images
python scripts/maintenance/optimize_images.py
```

---

## Additional Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Azure Static Web Apps](https://learn.microsoft.com/azure/static-web-apps/)
- [GitHub Pages](https://pages.github.com/)
- [Azure DevOps Pipelines](https://learn.microsoft.com/azure/devops/pipelines/)

---

**Last Updated:** December 9, 2025
**Version:** 1.0.0
**Maintainer:** CSA DevOps Team
