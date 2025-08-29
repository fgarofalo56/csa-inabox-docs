# ☁️ Azure Deployment Scripts

> **🏠 [Home](../../../README.md)** | **📚 [Documentation](../../../docs/README.md)** | **📜 [Scripts](../../README.md)** | **🚀 [Deployment](../README.md)**

---

## 📋 Overview

This directory contains scripts specifically for deploying the Cloud Scale Analytics (CSA) in-a-Box documentation to Microsoft Azure services. These scripts leverage Azure's static web hosting, CDN, and monitoring capabilities to provide a scalable, performant documentation platform.

## 🎯 Purpose

The Azure deployment scripts are designed to:

- **Deploy documentation to Azure Static Web Apps** for fast, global delivery
- **Configure Azure CDN** for optimal performance and caching
- **Set up Azure monitoring and analytics** for usage insights
- **Manage Azure resource provisioning** for documentation infrastructure
- **Integrate with Azure DevOps** for CI/CD pipelines

## 📂 Current Scripts

### Available Scripts

| Script | Purpose | Status | Last Updated |
|--------|---------|---------|--------------|
| `enable-monitoring.sh` | Configure Azure monitoring, analytics, and health dashboards | ✅ **Available** | 2025-01-28 |

### Planned Scripts (To Be Created)

| Script | Purpose | Priority | Dependencies |
|--------|---------|----------|--------------|
| `deploy-to-azure.sh` | Deploy documentation to Azure Static Web Apps | **HIGH** | Azure CLI, Static Web Apps |
| `setup-azure-cdn.sh` | Configure Azure CDN with custom domain | **MEDIUM** | Azure CLI, CDN Profile |
| `provision-resources.sh` | Create Azure resources using ARM/Bicep templates | **MEDIUM** | Azure CLI, ARM templates |
| `configure-ssl.sh` | Set up SSL certificates and custom domains | **LOW** | Azure CLI, Domain access |
| `backup-to-storage.sh` | Backup documentation to Azure Blob Storage | **LOW** | Azure CLI, Storage Account |

## 🛠️ Available Script Details

### `enable-monitoring.sh` ✅

**Purpose:** Complete monitoring system setup for Azure-hosted documentation

**Features:**
- **Analytics System:** Real-time user behavior tracking
- **Performance Monitoring:** Page load times, Core Web Vitals
- **Health Dashboards:** System status and metrics visualization
- **Feedback Collection:** User rating and comment system
- **Privacy Compliance:** GDPR-compliant analytics with consent management
- **API Server:** FastAPI-based monitoring backend (port 8056)
- **Database:** SQLite analytics database with performance tracking
- **Reporting:** Automated report generation capabilities

**Usage:**
```bash
# Enable monitoring system
./scripts/deployment/azure/enable-monitoring.sh

# Access monitoring dashboards
# - Health: http://localhost:8056/dashboards/health.html
# - Analytics: http://localhost:8056/dashboards/analytics
# - API: http://localhost:8056/
```

**Configuration:**
- Creates monitoring infrastructure in `docs/monitoring/`
- Configures analytics database and API endpoints
- Sets up privacy-compliant tracking with consent management
- Integrates with MkDocs for seamless documentation monitoring

**Output:**
- Monitoring API server on port 8056
- SQLite analytics database
- Real-time dashboards
- Privacy consent system
- Performance tracking widgets

## 🚀 Planned Script Details

### `deploy-to-azure.sh` (Priority: HIGH)

**Purpose:** Deploy documentation site to Azure Static Web Apps

**Features:**
- Build documentation using MkDocs
- Deploy to Azure Static Web Apps
- Configure routing and redirects
- Set up environment-specific configurations
- Verify deployment success

**Planned Usage:**
```bash
./deploy-to-azure.sh [--env environment] [--resource-group name] [--app-name name]

# Examples
./deploy-to-azure.sh --env production
./deploy-to-azure.sh --resource-group rg-csa-docs --app-name csa-docs-prod
```

### `setup-azure-cdn.sh` (Priority: MEDIUM)

**Purpose:** Configure Azure CDN for global content delivery

**Features:**
- Create CDN profile and endpoint
- Configure caching rules for optimal performance
- Set up custom domains
- Configure SSL certificates
- Optimize for documentation content

**Planned Usage:**
```bash
./setup-azure-cdn.sh --domain docs.contoso.com [--ssl-cert path]
```

### `provision-resources.sh` (Priority: MEDIUM)

**Purpose:** Provision Azure infrastructure using Infrastructure as Code

**Features:**
- Deploy ARM/Bicep templates
- Create resource groups, storage accounts, CDN profiles
- Configure security and access policies
- Set up monitoring and diagnostics
- Apply consistent tagging strategy

**Planned Usage:**
```bash
./provision-resources.sh --template bicep/main.bicep --env production
```

## 🔧 Azure Service Integration

### Azure Static Web Apps

**Benefits:**
- **Global CDN:** Built-in Azure CDN for fast global delivery
- **Custom domains:** Free SSL certificates with custom domains  
- **Staging environments:** Preview deployments for pull requests
- **Authentication:** Integrated Azure AD authentication
- **API integration:** Serverless API functions support

**Configuration:**
```json
{
  "routes": [
    {
      "route": "/api/*",
      "allowedRoles": ["authenticated"]
    },
    {
      "route": "/*",
      "serve": "/index.html",
      "statusCode": 200
    }
  ],
  "navigationFallback": {
    "rewrite": "/index.html"
  },
  "mimeTypes": {
    ".json": "application/json",
    ".woff2": "font/woff2"
  }
}
```

### Azure CDN Premium

**Benefits:**
- **Advanced caching:** Customizable caching rules
- **Compression:** Automatic gzip compression
- **Security:** WAF and DDoS protection
- **Analytics:** Detailed usage analytics
- **Purge API:** Programmatic cache invalidation

### Azure Monitor Integration

The `enable-monitoring.sh` script sets up comprehensive monitoring:

**Monitoring Components:**
- **Application Insights:** Performance and usage analytics
- **Azure Monitor Logs:** Centralized logging
- **Custom Dashboards:** Real-time metrics visualization
- **Alerts:** Proactive notifications for issues
- **SLA Monitoring:** Availability and performance tracking

## 📊 Monitoring and Analytics

### Available Monitoring Features

The monitoring system provides:

1. **User Analytics**
   - Page views and unique visitors
   - User flow and navigation patterns
   - Geographic distribution
   - Device and browser analytics

2. **Performance Monitoring**
   - Core Web Vitals (LCP, FID, CLS)
   - Page load times and TTFB
   - Resource loading performance
   - Server response times

3. **Content Analytics**
   - Most/least popular content
   - Search queries and results
   - Download tracking
   - External link clicks

4. **Health Monitoring**
   - System availability and uptime
   - Error rates and types
   - API response times
   - Database performance

### Privacy and Compliance

- **GDPR Compliance:** Consent management and data anonymization
- **Privacy Mode:** Strict privacy controls for sensitive environments
- **Data Retention:** Configurable data retention policies
- **User Rights:** Data export and deletion capabilities

## 🔧 Configuration

### Environment Variables

Azure deployment scripts use these environment variables:

```bash
# Azure Authentication
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret

# Azure Static Web Apps
AZURE_RESOURCE_GROUP=rg-csa-docs
AZURE_STATIC_WEB_APP_NAME=csa-docs
AZURE_STATIC_WEB_APP_LOCATION=eastus2

# Azure CDN (optional)
AZURE_CDN_PROFILE_NAME=csa-docs-cdn
AZURE_CDN_ENDPOINT_NAME=csa-docs
AZURE_CUSTOM_DOMAIN=docs.contoso.com

# Monitoring Configuration
AZURE_APP_INSIGHTS_KEY=your-instrumentation-key
AZURE_LOG_ANALYTICS_WORKSPACE=your-workspace-id
MONITORING_ENABLED=true

# Build Configuration
BUILD_OUTPUT_DIR=site
BUILD_CLEAN=true
ENABLE_OPTIMIZATION=true
```

### Azure CLI Prerequisites

Ensure Azure CLI is configured:

```bash
# Login to Azure
az login

# Set default subscription
az account set --subscription "your-subscription-id"

# Verify authentication
az account show
```

### Required Azure Permissions

The deployment scripts require these Azure RBAC permissions:

- **Contributor** on resource group for resource creation
- **Static Web App Contributor** for Static Web Apps deployment
- **CDN Profile Contributor** for CDN configuration  
- **Monitoring Contributor** for Azure Monitor setup
- **Storage Blob Data Contributor** for backup operations (if used)

## 🔍 Troubleshooting

### Common Azure Deployment Issues

| Issue | Cause | Solution |
|-------|--------|----------|
| **Azure CLI not authenticated** | Not logged in to Azure | Run `az login` and set subscription |
| **Insufficient permissions** | Missing RBAC permissions | Check Azure permissions for service principal |
| **Static Web App deployment fails** | Invalid configuration | Check `staticwebapp.config.json` |
| **CDN not serving content** | Cache not purged | Purge CDN cache manually |
| **SSL certificate error** | Domain validation failed | Verify domain ownership and DNS settings |
| **Monitoring not working** | Missing Application Insights key | Check monitoring configuration |

### Debug Commands

```bash
# Check Azure authentication
az account show

# List resource groups
az group list --output table

# Check Static Web App status
az staticwebapp show --name $AZURE_STATIC_WEB_APP_NAME --resource-group $AZURE_RESOURCE_GROUP

# View deployment logs
az staticwebapp logs --name $AZURE_STATIC_WEB_APP_NAME --resource-group $AZURE_RESOURCE_GROUP
```

### Monitoring Troubleshooting

```bash
# Check monitoring system status
curl http://localhost:8056/api/health

# View monitoring logs
tail -f docs/monitoring/logs/monitoring.log

# Test database connection
sqlite3 docs/monitoring/data/analytics.db ".tables"

# Restart monitoring system
cd docs/monitoring && ./start.sh
```

## 💰 Cost Optimization

### Azure Service Costs

Estimated monthly costs for documentation hosting:

| Service | Tier | Estimated Cost | Notes |
|---------|------|----------------|-------|
| **Static Web Apps** | Standard | $9/month | Includes CDN and SSL |
| **Application Insights** | Basic | $2-5/month | Based on telemetry volume |
| **Azure Monitor** | Pay-as-you-go | $1-3/month | Log ingestion and retention |
| **Custom Domain SSL** | Free | $0/month | Included with Static Web Apps |

**Total estimated cost:** $12-17/month for production documentation site

### Cost Optimization Tips

- Use **Free tier** of Static Web Apps for development/testing
- Configure **log retention policies** to manage Monitor costs
- Implement **sampling** in Application Insights for high-traffic sites
- Use **shared CDN profiles** across multiple documentation sites

## 🔄 CI/CD Integration

### GitHub Actions Integration

```yaml
name: Deploy to Azure
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Azure CLI
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Deploy to Azure
        run: ./scripts/deployment/azure/deploy-to-azure.sh
        env:
          AZURE_STATIC_WEB_APP_DEPLOYMENT_TOKEN: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
```

### Azure DevOps Integration

```yaml
trigger:
  branches:
    include:
      - main

variables:
  azureServiceConnection: 'azure-service-connection'

stages:
  - stage: Deploy
    jobs:
      - job: DeployToAzure
        pool:
          vmImage: 'ubuntu-latest'
        steps:
          - task: AzureCLI@2
            displayName: 'Deploy Documentation'
            inputs:
              azureSubscription: $(azureServiceConnection)
              scriptType: bash
              scriptLocation: scriptPath
              scriptPath: scripts/deployment/azure/deploy-to-azure.sh
```

## 📚 Related Documentation

- [Azure Static Web Apps Documentation](https://docs.microsoft.com/en-us/azure/static-web-apps/)
- [Azure CDN Documentation](https://docs.microsoft.com/en-us/azure/cdn/)
- [Azure Monitor Documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/)
- [MkDocs Deployment Guide](../../../docs/guides/MKDOCS_DEPLOYMENT.md) *(planned)*

## 🤝 Contributing

### Adding New Azure Scripts

1. **Follow Azure best practices** - Use ARM/Bicep templates when possible
2. **Include error handling** - Check Azure CLI command success
3. **Support multiple environments** - dev, staging, production
4. **Add monitoring** - Include Azure Monitor integration
5. **Document costs** - Include cost estimates for new resources
6. **Test thoroughly** - Test in clean Azure subscription

### Script Requirements

- [ ] Uses Azure CLI for Azure operations
- [ ] Supports `--dry-run` for testing
- [ ] Includes comprehensive error handling
- [ ] Has rollback capabilities where applicable
- [ ] Integrates with monitoring system
- [ ] Documents required Azure permissions
- [ ] Includes cost estimates
- [ ] Is tested in multiple Azure regions

## 📞 Support

For Azure deployment issues:

- **GitHub Issues:** [Create Azure Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?labels=azure,deployment)
- **Azure Support:** Use Azure portal support for Azure-specific issues
- **Azure CLI Help:** `az --help` or `az <command> --help`
- **Monitoring Issues:** Check monitoring logs and health endpoints
- **Team Contact:** CSA Documentation Team

---

**Last Updated:** January 28, 2025  
**Version:** 1.0.0  
**Maintainer:** CSA Documentation Team