# 🚀 Deployment Scripts

> **🏠 [Home](../../README.md)** | **📚 [Documentation](../../docs/README.md)** | **📜 [Scripts](../README.md)** | **📊 [Project Tracking](../../project_tracking/README.md)**

---

## 📋 Overview

This directory contains scripts for deploying the Cloud Scale Analytics (CSA) in-a-Box documentation project to various environments and platforms. These scripts automate the build, deployment, and configuration processes for different deployment targets.

## 🎯 Purpose

The deployment scripts are designed to:

- **Build and deploy documentation** to various hosting platforms
- **Configure cloud infrastructure** for documentation hosting
- **Automate container deployment** for scalable hosting
- **Manage Kubernetes deployments** for enterprise environments
- **Set up monitoring and analytics** for deployed documentation

## 📂 Directory Structure

```
deployment/
├── 📄 README.md                    # This file
├── 📁 azure/                       # Azure deployment scripts
│   ├── 📄 README.md                # Azure deployment documentation
│   └── 📄 enable-monitoring.sh     # Enable Azure monitoring
├── 📁 docker/                      # Docker deployment scripts
│   ├── 📄 README.md                # Docker deployment documentation
│   └── (planned docker scripts)
└── 📁 kubernetes/                  # Kubernetes deployment scripts
    ├── 📄 README.md                # Kubernetes deployment documentation
    └── (planned k8s manifests)
```

## 📂 Current Scripts

### Available Scripts

| Script | Location | Purpose | Status |
|--------|----------|---------|---------|
| `enable-monitoring.sh` | `azure/` | Enable Azure monitoring and analytics | ✅ **Available** |

### Planned Scripts (To Be Created)

| Category | Script | Purpose | Priority |
|----------|--------|---------|----------|
| **General** | `deploy-docs.sh` | Deploy documentation to configured target | **HIGH** |
| **General** | `build-site.sh` | Build documentation site locally | **HIGH** |
| **Azure** | `deploy-to-azure.sh` | Deploy to Azure Static Web Apps | **HIGH** |
| **Azure** | `setup-azure-cdn.sh` | Configure Azure CDN for documentation | **MEDIUM** |
| **Docker** | `build-container.sh` | Build documentation container image | **MEDIUM** |
| **Docker** | `deploy-container.sh` | Deploy containerized documentation | **MEDIUM** |
| **Kubernetes** | `deploy-k8s.sh` | Deploy to Kubernetes cluster | **LOW** |

## 🚀 Usage Examples

### Quick Deployment

```bash
# Build and deploy to default target
./scripts/deployment/deploy-docs.sh

# Deploy to specific environment
./scripts/deployment/deploy-docs.sh --env production

# Build only (no deployment)
./scripts/deployment/build-site.sh
```

### Azure Deployment

```bash
# Enable monitoring (existing script)
./scripts/deployment/azure/enable-monitoring.sh

# Deploy to Azure Static Web Apps (planned)
./scripts/deployment/azure/deploy-to-azure.sh

# Set up Azure CDN (planned)
./scripts/deployment/azure/setup-azure-cdn.sh --domain docs.contoso.com
```

### Container Deployment

```bash
# Build container image (planned)
./scripts/deployment/docker/build-container.sh

# Deploy container (planned)
./scripts/deployment/docker/deploy-container.sh --port 8080
```

### Kubernetes Deployment

```bash
# Deploy to Kubernetes (planned)
./scripts/deployment/kubernetes/deploy-k8s.sh --namespace csa-docs
```

## 📋 Planned Script Details

### `deploy-docs.sh` (Priority: HIGH)

**Purpose:** Universal deployment script that can target multiple platforms

**Features:**
- Auto-detect deployment target from configuration
- Build documentation site using MkDocs
- Deploy to configured hosting platform
- Verify deployment success
- Rollback on failure

**Usage:**
```bash
./deploy-docs.sh [--env environment] [--target platform] [--dry-run]
```

### `build-site.sh` (Priority: HIGH)

**Purpose:** Build documentation site locally for testing or manual deployment

**Features:**
- Clean previous build artifacts
- Run MkDocs build with optimizations
- Generate static assets
- Validate build output
- Create deployment package

**Usage:**
```bash
./build-site.sh [--clean] [--optimize] [--output-dir path]
```

### Azure Deployment Scripts

See [Azure deployment documentation](./azure/README.md) for detailed information about Azure-specific deployment scripts.

### Docker Deployment Scripts

See [Docker deployment documentation](./docker/README.md) for detailed information about container deployment scripts.

### Kubernetes Deployment Scripts

See [Kubernetes deployment documentation](./kubernetes/README.md) for detailed information about Kubernetes deployment scripts.

## 🔧 Configuration

### Environment Configuration

Deployment scripts use environment-specific configuration files:

```bash
# Environment files
config/environments/development.env
config/environments/staging.env
config/environments/production.env
```

**Example configuration:**
```bash
# Deployment target
DEPLOYMENT_TARGET=azure-static-web-apps
DEPLOYMENT_ENVIRONMENT=production

# Build configuration
BUILD_COMMAND="mkdocs build"
BUILD_OUTPUT_DIR="site"
BUILD_CLEAN=true

# Azure configuration
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=rg-csa-docs
AZURE_STATIC_WEB_APP_NAME=csa-docs

# Docker configuration
DOCKER_REGISTRY=your-registry.azurecr.io
DOCKER_IMAGE_NAME=csa-docs
DOCKER_IMAGE_TAG=latest

# Monitoring
ENABLE_MONITORING=true
MONITORING_ENDPOINT=https://your-monitoring-endpoint
```

### Deployment Targets

| Target | Description | Configuration Required |
|--------|-------------|----------------------|
| **Azure Static Web Apps** | Azure-native static hosting | Subscription, Resource Group |
| **Azure Blob Storage** | Static website hosting on Blob Storage | Storage Account, Container |
| **GitHub Pages** | GitHub's static hosting | Repository, Branch |
| **Docker Container** | Containerized deployment | Registry, Image configuration |
| **Kubernetes** | Container orchestration platform | Cluster, Namespace, Ingress |

## 🛠️ Development Standards

### Script Standards

All deployment scripts must follow these standards:

1. **Environment validation** - Check all required environment variables
2. **Rollback capability** - Provide rollback on deployment failure  
3. **Health checks** - Verify deployment success
4. **Monitoring integration** - Report deployment status
5. **Security** - Use secure deployment practices

### Deployment Pipeline

```bash
1. Pre-deployment validation
   ├── Check environment configuration
   ├── Validate credentials and permissions
   └── Run pre-deployment tests

2. Build phase
   ├── Clean previous build artifacts
   ├── Run documentation build
   ├── Optimize assets
   └── Package for deployment

3. Deployment phase
   ├── Deploy to target platform
   ├── Configure routing and DNS
   ├── Enable monitoring
   └── Run health checks

4. Post-deployment
   ├── Verify deployment success
   ├── Run smoke tests
   ├── Update deployment status
   └── Notify stakeholders
```

## 📊 Monitoring and Analytics

### Deployment Monitoring

- **Build status tracking** - Monitor build success/failure rates
- **Deployment metrics** - Track deployment duration and success rates
- **Health monitoring** - Monitor deployed site availability and performance
- **Error tracking** - Capture and alert on deployment errors

### Available Monitoring

The `enable-monitoring.sh` script in the `azure/` directory provides:
- Analytics tracking for documentation usage
- Performance monitoring for page load times
- User feedback collection
- Health status dashboards

## 🔍 Troubleshooting

### Common Deployment Issues

| Issue | Cause | Solution |
|-------|--------|----------|
| **Build fails** | Missing dependencies | Run setup scripts first |
| **Authentication error** | Invalid credentials | Check Azure CLI login status |
| **Deployment timeout** | Large site size | Optimize images and assets |
| **DNS not resolving** | DNS propagation delay | Wait 24-48 hours or check DNS config |
| **SSL certificate error** | Certificate not configured | Configure SSL in hosting platform |

### Debug Mode

Enable debugging for deployment scripts:

```bash
# Run with debug output
export DEBUG=true
./scripts/deployment/deploy-docs.sh

# Or use bash debug mode
bash -x scripts/deployment/deploy-docs.sh
```

### Logs and Monitoring

Deployment logs are stored in:
- **Deployment log:** `logs/deployment.log`
- **Build log:** `logs/build.log`
- **Error log:** `logs/deployment-error.log`

## 🔄 CI/CD Integration

### GitHub Actions Integration

Deployment scripts are designed to work with GitHub Actions:

```yaml
# .github/workflows/deploy.yml
name: Deploy Documentation
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Azure
        run: ./scripts/deployment/azure/deploy-to-azure.sh
        env:
          AZURE_CREDENTIALS: ${{ secrets.AZURE_CREDENTIALS }}
```

### Azure DevOps Integration

Scripts are compatible with Azure DevOps pipelines:

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main

jobs:
  - job: Deploy
    pool:
      vmImage: 'ubuntu-latest'
    steps:
      - script: ./scripts/deployment/deploy-docs.sh --env production
        displayName: 'Deploy Documentation'
```

## 📚 Related Documentation

- [Azure Deployment Guide](./azure/README.md)
- [Docker Deployment Guide](./docker/README.md) *(planned)*
- [Kubernetes Deployment Guide](./kubernetes/README.md) *(planned)*
- [CI/CD Guide](../../docs/guides/CICD_GUIDE.md) *(planned)*
- [Monitoring Guide](../../docs/guides/MONITORING_GUIDE.md) *(planned)*

## 🤝 Contributing

### Adding New Deployment Scripts

1. **Identify deployment target** - Determine the platform/service
2. **Create in appropriate subdirectory** - azure/, docker/, or kubernetes/
3. **Follow deployment standards** - Include validation, rollback, monitoring
4. **Test thoroughly** - Test deployment and rollback scenarios
5. **Update documentation** - Update this README and subdirectory README
6. **Submit PR** - Include tests and documentation updates

### Script Requirements

- [ ] Follows naming conventions (`kebab-case.sh`)
- [ ] Includes proper header with metadata
- [ ] Has environment validation
- [ ] Supports rollback on failure
- [ ] Includes health checks
- [ ] Has comprehensive error handling
- [ ] Supports `--help` and `--dry-run` flags
- [ ] Is documented in appropriate README
- [ ] Has been tested in target environment

## 📞 Support

For deployment-related issues:

- **GitHub Issues:** [Create Deployment Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?labels=deployment)
- **Azure Support:** Check Azure portal for deployment status
- **Documentation:** Check platform-specific documentation in subdirectories
- **Team Contact:** CSA Documentation Team

---

**Last Updated:** January 28, 2025  
**Version:** 1.0.0  
**Maintainer:** CSA Documentation Team