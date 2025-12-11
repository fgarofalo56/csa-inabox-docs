# Platform Admin Learning Path

> **[Home](../README.md)** | **[Tutorials](README.md)** | **Platform Admin Path**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Level](https://img.shields.io/badge/Level-Intermediate_to_Advanced-orange?style=flat-square)

Complete learning path for Platform Administrators managing Cloud Scale Analytics.

---

## Overview

This learning path covers:

- Infrastructure provisioning and management
- Security and compliance
- Monitoring and operations
- Cost optimization

**Duration**: 6-8 weeks | **Prerequisites**: Azure fundamentals, networking basics

---

## Learning Modules

### Module 1: Infrastructure Setup (Week 1-2)

| Topic | Duration | Resources |
|-------|----------|-----------|
| Synapse Workspace Setup | 4 hours | [Environment Setup](synapse/01-environment-setup.md) |
| Network Architecture | 4 hours | [Private Link](../docs/architecture/private-link-architecture/README.md) |
| IaC with Bicep/Terraform | 4 hours | [Deployment Guide](../docs/guides/deployment-guide.md) |

**Hands-on Lab:**
```bash
# Deploy Synapse workspace with Bicep
az deployment group create \
    --resource-group rg-analytics \
    --template-file synapse-workspace.bicep \
    --parameters @parameters.json

# Configure private endpoints
az network private-endpoint create \
    --name pe-synapse-sql \
    --resource-group rg-analytics \
    --vnet-name vnet-analytics \
    --subnet subnet-private \
    --private-connection-resource-id $SYNAPSE_ID \
    --group-id Sql \
    --connection-name synapse-sql-connection
```

---

### Module 2: Security & Compliance (Week 3-4)

| Topic | Duration | Resources |
|-------|----------|-----------|
| Identity Management | 3 hours | [Security Best Practices](../best-practices/security/README.md) |
| Network Security | 3 hours | [Network Security](../best-practices/network-security/README.md) |
| Data Protection | 4 hours | [Data Governance](../best-practices/data-governance/README.md) |
| Compliance | 2 hours | [Compliance Guide](../docs/security/compliance-guide/README.md) |

**Hands-on Lab:**
```bash
# Configure managed identity
az synapse workspace update \
    --name synapse-ws \
    --resource-group rg-analytics \
    --identity-type SystemAssigned

# Assign RBAC roles
az role assignment create \
    --assignee $WORKSPACE_IDENTITY \
    --role "Storage Blob Data Contributor" \
    --scope $STORAGE_ACCOUNT_ID

# Enable diagnostic logging
az monitor diagnostic-settings create \
    --name synapse-diagnostics \
    --resource $SYNAPSE_ID \
    --workspace $LOG_ANALYTICS_ID \
    --logs '[{"category": "SynapseRbacOperations", "enabled": true}]'
```

---

### Module 3: Monitoring & Operations (Week 5-6)

| Topic | Duration | Resources |
|-------|----------|-----------|
| Azure Monitor Setup | 3 hours | [Monitoring Guide](../docs/09-monitoring/README.md) |
| Alerting Configuration | 2 hours | [Alert Setup](monitoring/cost-tracking.md) |
| Troubleshooting | 4 hours | [Troubleshooting Guide](../troubleshooting/index.md) |
| Automation | 3 hours | [Runbook Automation](../docs/devops/README.md) |

**Hands-on Lab:**
```kusto
// KQL queries for monitoring
// Spark job failures
SynapseSparkJobs
| where TimeGenerated > ago(24h)
| where Status == "Failed"
| summarize FailureCount = count() by JobName, bin(TimeGenerated, 1h)
| render timechart

// SQL pool utilization
SynapseSqlPoolRequestSteps
| where TimeGenerated > ago(1h)
| summarize
    AvgDuration = avg(DurationMs),
    MaxDuration = max(DurationMs)
    by OperationType, bin(TimeGenerated, 5m)
```

---

### Module 4: Cost Management (Week 7-8)

| Topic | Duration | Resources |
|-------|----------|-----------|
| Cost Analysis | 2 hours | [Cost Optimization](../best-practices/cost-optimization/README.md) |
| Resource Right-Sizing | 3 hours | [Right-Sizing Guide](optimization/right-sizing.md) |
| Budget Alerts | 2 hours | [Cost Tracking](monitoring/cost-tracking.md) |
| Reserved Capacity | 2 hours | [Cost Optimization](../best-practices/cost-optimization/README.md) |

**Hands-on Lab:**
```bash
# Create budget alert
az consumption budget create \
    --budget-name analytics-monthly \
    --amount 10000 \
    --time-grain Monthly \
    --start-date 2025-01-01 \
    --end-date 2025-12-31 \
    --notifications '{
        "80_percent": {
            "enabled": true,
            "operator": "GreaterThan",
            "threshold": 80,
            "contactEmails": ["admin@company.com"]
        }
    }'

# Configure auto-pause
az synapse sql pool update \
    --name dedicated-pool \
    --workspace-name synapse-ws \
    --resource-group rg-analytics \
    --enable-auto-pause true \
    --auto-pause-delay 60
```

---

## Certification Preparation

### Recommended Certifications

1. **AZ-104**: Azure Administrator
2. **AZ-500**: Azure Security Engineer
3. **AZ-400**: Azure DevOps Engineer

---

## Skills Assessment

### Intermediate Checkpoint
- [ ] Deploy Synapse with IaC
- [ ] Configure network security
- [ ] Set up monitoring dashboards

### Advanced Checkpoint
- [ ] Implement DR strategy
- [ ] Automate operations
- [ ] Optimize costs by 20%+

---

## Related Documentation

- [Data Analyst Path](data-analyst-path.md)
- [Data Engineer Path](data-engineer-path.md)

---

*Last Updated: January 2025*
