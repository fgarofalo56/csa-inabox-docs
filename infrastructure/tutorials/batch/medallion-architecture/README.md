# 🏗️ Medallion Architecture Infrastructure

> **Infrastructure as Code (IaC)** for deploying the Medallion Architecture pattern on Azure

![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen?style=flat-square)
![IaC](https://img.shields.io/badge/IaC-Bicep-blue?style=flat-square)

## 📁 Contents

- `main.bicep` - Main Bicep template for all resources
- `parameters.json` - Default parameters (customize before deploying)
- `deploy.sh` - Automated deployment script
- `README.md` - This file

## 🚀 Quick Deploy

```bash
# 1. Review and customize parameters
vim parameters.json

# 2. Run deployment script
./deploy.sh

# 3. Load environment variables
source .deployment-config.env
```

## 📦 Resources Deployed

| Resource | Purpose | Estimated Cost/Month |
|----------|---------|---------------------|
| **Azure Synapse Workspace** | Analytics platform | ~$0 (serverless) |
| **Spark Pool** | Data processing | ~$0.30/hour (auto-pause enabled) |
| **Data Lake Gen2** | Data storage | ~$0.02/GB |
| **Key Vault** | Secrets management | ~$0.03/10,000 operations |
| **Log Analytics** | Monitoring | ~$2.30/GB ingested |

**Total Estimated Cost**: $10-20 for tutorial completion (remember to cleanup after!)

## 🔒 Security Features

- **Managed Identity**: System-assigned identity for Synapse
- **RBAC**: Principle of least privilege
- **Encryption**: At rest and in transit
- **Private Endpoints**: Optional (not enabled by default for tutorial)
- **Key Vault Integration**: Secrets management
- **Soft Delete**: 7-day retention for accidental deletions

## 🎯 Customization

### Change Spark Pool Size

Edit `parameters.json`:

```json
{
  "sparkPoolNodeSize": {
    "value": "Medium"  // Small, Medium, or Large
  },
  "sparkPoolMinNodeCount": {
    "value": 3
  },
  "sparkPoolMaxNodeCount": {
    "value": 20
  }
}
```

### Change Region

```json
{
  "location": {
    "value": "westus2"  // Your preferred region
  }
}
```

### Enable Private Endpoints

Modify `main.bicep` to add private endpoint resources (see Azure documentation).

## 🧪 Validation

After deployment, verify resources:

```bash
# List all deployed resources
az resource list \
  --resource-group $RESOURCE_GROUP_NAME \
  --output table

# Check Synapse workspace
az synapse workspace show \
  --name $SYNAPSE_WORKSPACE_NAME \
  --resource-group $RESOURCE_GROUP_NAME

# Check Spark pool
az synapse spark pool show \
  --name sparkpool01 \
  --workspace-name $SYNAPSE_WORKSPACE_NAME \
  --resource-group $RESOURCE_GROUP_NAME
```

## 🧹 Cleanup

**⚠️ Warning**: This deletes ALL resources and data.

```bash
az group delete \
  --name $RESOURCE_GROUP_NAME \
  --yes \
  --no-wait
```

## 📚 Additional Resources

- [Bicep Documentation](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/)
- [Synapse Analytics](https://learn.microsoft.com/en-us/azure/synapse-analytics/)
- [Tutorial Guide](../../../../docs/tutorials/architecture-patterns/batch/medallion-architecture-tutorial.md)

---

**Last Updated**: 2025-12-12  
**Version**: 1.0.0
