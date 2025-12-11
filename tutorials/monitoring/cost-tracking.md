# Cost Tracking Tutorial

> **[Home](../../README.md)** | **[Tutorials](../README.md)** | **Cost Tracking**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Level](https://img.shields.io/badge/Level-Intermediate-yellow?style=flat-square)

Learn to track, analyze, and optimize costs for Cloud Scale Analytics.

---

## Overview

This tutorial covers:

- Setting up cost monitoring
- Creating budget alerts
- Analyzing cost trends
- Implementing cost optimization

**Duration**: 1.5 hours | **Prerequisites**: Azure subscription owner/contributor

---

## Step 1: Enable Cost Management

### Configure Cost Analysis

```bash
# Get current costs by service
az consumption usage list \
    --start-date 2025-01-01 \
    --end-date 2025-01-31 \
    --query "[?contains(instanceName, 'synapse')].{Name:instanceName, Cost:pretaxCost}" \
    --output table
```

### Tag Resources for Cost Allocation

```bash
# Add cost allocation tags
az synapse workspace update \
    --name synapse-ws \
    --resource-group rg-analytics \
    --tags Environment=Production CostCenter=Analytics Team=DataPlatform
```

---

## Step 2: Create Budget Alerts

### Monthly Budget

```bash
az consumption budget create \
    --budget-name analytics-monthly \
    --amount 10000 \
    --time-grain Monthly \
    --start-date 2025-01-01 \
    --end-date 2025-12-31 \
    --resource-group rg-analytics \
    --notifications '{
        "warning_80": {
            "enabled": true,
            "operator": "GreaterThan",
            "threshold": 80,
            "contactEmails": ["team@company.com"],
            "contactRoles": ["Owner"]
        },
        "critical_100": {
            "enabled": true,
            "operator": "GreaterThan",
            "threshold": 100,
            "contactEmails": ["team@company.com", "manager@company.com"]
        }
    }'
```

### Per-Service Budgets

```bash
# Dedicated SQL Pool budget
az consumption budget create \
    --budget-name dedicated-sql-budget \
    --amount 5000 \
    --time-grain Monthly \
    --start-date 2025-01-01 \
    --end-date 2025-12-31 \
    --filter '{
        "dimensions": {
            "name": "MeterCategory",
            "operator": "In",
            "values": ["Azure Synapse Analytics"]
        }
    }'
```

---

## Step 3: Cost Analysis Dashboard

### KQL Queries for Cost Monitoring

```kusto
// Daily cost trend
AzureDiagnostics
| where TimeGenerated > ago(30d)
| where ResourceType == "WORKSPACES"
| summarize
    DailyOperations = count(),
    EstimatedCost = sum(toreal(Quantity) * 0.001)
    by bin(TimeGenerated, 1d)
| render timechart

// Cost by pool type
SynapseIntegrationPipelineRuns
| where TimeGenerated > ago(7d)
| summarize
    PipelineRuns = count(),
    TotalDuration = sum(DurationMs) / 1000 / 60
    by PipelineName
| order by TotalDuration desc
```

### Azure Workbook Template

```json
{
    "version": "Notebook/1.0",
    "items": [
        {
            "type": 1,
            "content": {
                "json": "## Analytics Cost Dashboard"
            }
        },
        {
            "type": 3,
            "content": {
                "version": "KqlItem/1.0",
                "query": "// Cost trend query here",
                "size": 0,
                "title": "30-Day Cost Trend",
                "timeContext": {"durationMs": 2592000000},
                "queryType": 0,
                "visualization": "linechart"
            }
        }
    ]
}
```

---

## Step 4: Cost Optimization Actions

### Auto-Pause Dedicated SQL

```bash
# Enable auto-pause
az synapse sql pool update \
    --name dedicated-pool \
    --workspace-name synapse-ws \
    --resource-group rg-analytics \
    --enable-auto-pause true \
    --auto-pause-delay 60

# Manual pause during off-hours
az synapse sql pool pause \
    --name dedicated-pool \
    --workspace-name synapse-ws \
    --resource-group rg-analytics
```

### Right-Size Spark Pools

```python
# Analyze Spark job metrics
def analyze_spark_usage(workspace_name, days=30):
    """Analyze Spark pool utilization for right-sizing."""

    query = f"""
    SynapseSparkPoolLogs
    | where TimeGenerated > ago({days}d)
    | where WorkspaceName == '{workspace_name}'
    | summarize
        AvgExecutorCount = avg(ExecutorCount),
        MaxExecutorCount = max(ExecutorCount),
        AvgMemoryUsedGB = avg(MemoryUsedGB),
        TotalJobMinutes = sum(DurationMinutes)
        by SparkPoolName
    """

    # Recommendations based on usage
    # If AvgExecutorCount < 50% of configured max, reduce pool size
```

### Serverless SQL Cost Control

```sql
-- Check data processed
SELECT
    execution_type_desc,
    total_worker_time / 1000000.0 AS cpu_time_seconds,
    data_processed_mb = total_physical_reads * 8 / 1024.0
FROM sys.dm_exec_query_stats
ORDER BY data_processed_mb DESC;

-- Optimize queries to reduce data scanned
-- Use partitioning and column projection
```

---

## Step 5: Cost Alerting Automation

### Azure Function for Cost Alerts

```python
import azure.functions as func
from azure.mgmt.consumption import ConsumptionManagementClient

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 8 * * *", arg_name="timer")
async def daily_cost_check(timer: func.TimerRequest):
    """Daily cost check and alerting."""

    client = ConsumptionManagementClient(credential, subscription_id)

    # Get current month usage
    usage = client.usage_details.list(
        scope=f"/subscriptions/{subscription_id}",
        filter="properties/usageStart ge '2025-01-01'"
    )

    total_cost = sum(item.cost for item in usage)

    # Alert if exceeding daily threshold
    daily_budget = 500
    if total_cost / datetime.now().day > daily_budget:
        send_alert(f"Daily spend exceeds budget: ${total_cost:.2f}")
```

---

## Cost Optimization Checklist

- [ ] Tags applied to all resources
- [ ] Monthly budgets configured
- [ ] Auto-pause enabled for SQL pools
- [ ] Spark pools right-sized
- [ ] Storage lifecycle policies set
- [ ] Reserved capacity evaluated
- [ ] Cost anomaly alerts active

---

## Related Documentation

- [Cost Optimization Best Practices](../../best-practices/cost-optimization/README.md)
- [Right-Sizing Guide](../optimization/right-sizing.md)
- [Platform Admin Path](../platform-admin-path.md)

---

*Last Updated: January 2025*
