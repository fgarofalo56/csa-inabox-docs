# Monitoring Guide

> **[Home](../../README.md)** | **[Monitoring](../README.md)** | **Monitoring Guide**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Category](https://img.shields.io/badge/Category-Operations-blue?style=flat-square)

Comprehensive monitoring guide for Cloud Scale Analytics platforms.

---

## Overview

Effective monitoring covers:

- **Infrastructure**: Compute, storage, networking
- **Applications**: Pipelines, jobs, queries
- **Data Quality**: Completeness, accuracy, timeliness
- **Security**: Access patterns, anomalies
- **Cost**: Resource consumption, billing

---

## Azure Monitor Setup

### Enable Diagnostics

```bash
# Synapse workspace
az monitor diagnostic-settings create \
    --name "synapse-monitoring" \
    --resource "/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Synapse/workspaces/{ws}" \
    --workspace "/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.OperationalInsights/workspaces/{law}" \
    --logs '[{"categoryGroup": "allLogs", "enabled": true}]' \
    --metrics '[{"category": "AllMetrics", "enabled": true}]'

# Storage account
az monitor diagnostic-settings create \
    --name "storage-monitoring" \
    --resource "/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Storage/storageAccounts/{sa}" \
    --workspace "/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.OperationalInsights/workspaces/{law}" \
    --logs '[
        {"category": "StorageRead", "enabled": true},
        {"category": "StorageWrite", "enabled": true},
        {"category": "StorageDelete", "enabled": true}
    ]'
```

---

## Key Metrics

### Compute Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| CPU Utilization | < 70% | > 85% for 15 min |
| Memory Usage | < 80% | > 90% for 10 min |
| Disk I/O | Varies | > 90% sustained |
| Network Throughput | Varies | Sudden drops |

### Data Pipeline Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Pipeline Success Rate | > 99% | < 95% |
| Pipeline Duration | < 2x baseline | > 3x baseline |
| Data Freshness | < 1 hour | > 2 hours |
| Record Count | Within 10% | > 20% variance |

---

## Alerting Configuration

### Alert Rules

```json
{
    "alerts": [
        {
            "name": "Pipeline Failure",
            "description": "Alert when pipeline fails",
            "severity": 1,
            "evaluationFrequency": "PT5M",
            "windowSize": "PT5M",
            "criteria": {
                "allOf": [{
                    "metricName": "PipelineFailedRuns",
                    "operator": "GreaterThan",
                    "threshold": 0,
                    "timeAggregation": "Total"
                }]
            },
            "actions": ["action-group-oncall"]
        },
        {
            "name": "High CPU Usage",
            "severity": 2,
            "criteria": {
                "allOf": [{
                    "metricName": "cpu_percent",
                    "operator": "GreaterThan",
                    "threshold": 85,
                    "timeAggregation": "Average"
                }]
            }
        }
    ]
}
```

### Action Groups

```bash
# Create action group
az monitor action-group create \
    --name "oncall-team" \
    --resource-group rg-monitoring \
    --short-name "oncall" \
    --email-receiver name="Data Team" email-address="data-team@company.com" \
    --sms-receiver name="Oncall" country-code="1" phone-number="5551234567" \
    --webhook-receiver name="PagerDuty" uri="https://events.pagerduty.com/integration/{key}/enqueue"
```

---

## Dashboard Design

### Executive Dashboard

```kql
// Pipeline health summary
let PipelineHealth = SynapseIntegrationPipelineRuns
| where TimeGenerated > ago(24h)
| summarize
    Total = count(),
    Succeeded = countif(Status == "Succeeded"),
    Failed = countif(Status == "Failed")
| extend SuccessRate = round(Succeeded * 100.0 / Total, 2);

// Data freshness
let DataFreshness = StorageBlobLogs
| where TimeGenerated > ago(24h)
| where OperationName == "PutBlob"
| summarize LastUpdate = max(TimeGenerated) by Container = tostring(split(Uri, "/")[3])
| extend HoursSinceUpdate = datetime_diff('hour', now(), LastUpdate);

// Cost trend
let CostTrend = Usage
| where TimeGenerated > ago(30d)
| summarize DailyCost = sum(Quantity * UnitPrice) by bin(TimeGenerated, 1d);
```

### Operations Dashboard

- Active pipelines
- Query performance
- Resource utilization
- Error rates
- Data volume processed

---

## Log Analytics Queries

### Pipeline Monitoring

```kql
// Failed pipelines with details
SynapseIntegrationPipelineRuns
| where TimeGenerated > ago(24h)
| where Status == "Failed"
| project TimeGenerated, PipelineName, Error, RunId
| order by TimeGenerated desc

// Pipeline duration trend
SynapseIntegrationPipelineRuns
| where TimeGenerated > ago(7d)
| where Status == "Succeeded"
| summarize AvgDuration = avg(DurationInMs)/1000/60 by PipelineName, bin(TimeGenerated, 1d)
| render timechart
```

### Query Performance

```kql
// Slow queries
SynapseSqlPoolExecRequests
| where TimeGenerated > ago(24h)
| where TotalElapsedTimeMs > 300000  // > 5 minutes
| project TimeGenerated, RequestId, Command, TotalElapsedTimeMs/1000 as DurationSec
| order by DurationSec desc
| take 20
```

---

## Best Practices

### Monitoring Strategy

1. **Define SLOs**: Set clear service level objectives
2. **Baseline metrics**: Establish normal performance baselines
3. **Tiered alerting**: Use severity levels appropriately
4. **Runbooks**: Document response procedures
5. **Regular reviews**: Review and tune alerts monthly

### Cost Optimization

1. Set data retention policies
2. Sample high-volume logs
3. Use appropriate log levels
4. Archive historical data
5. Monitor monitoring costs

---

## Related Documentation

- [Service Monitoring](../../09-monitoring/README.md)
- [Troubleshooting Guide](../../troubleshooting/README.md)
- [Best Practices](../../best-practices/README.md)

---

*Last Updated: January 2025*
