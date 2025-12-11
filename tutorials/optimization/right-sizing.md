# Resource Right-Sizing Tutorial

> **[Home](../../README.md)** | **[Tutorials](../README.md)** | **Right-Sizing**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Level](https://img.shields.io/badge/Level-Intermediate-yellow?style=flat-square)

Learn to optimize resource allocation for cost efficiency and performance.

---

## Overview

This tutorial covers:

- Analyzing resource utilization
- Identifying over-provisioned resources
- Implementing right-sizing recommendations
- Continuous optimization

**Duration**: 1.5 hours | **Prerequisites**: Access to Azure Monitor metrics

---

## Step 1: Dedicated SQL Pool Analysis

### Collect Utilization Metrics

```sql
-- Query performance baseline
SELECT
    DATEPART(hour, start_time) AS hour_of_day,
    AVG(total_elapsed_time / 1000.0) AS avg_duration_sec,
    MAX(total_elapsed_time / 1000.0) AS max_duration_sec,
    COUNT(*) AS query_count
FROM sys.dm_pdw_exec_requests
WHERE start_time > DATEADD(day, -7, GETDATE())
    AND status = 'Completed'
GROUP BY DATEPART(hour, start_time)
ORDER BY hour_of_day;

-- Concurrency analysis
SELECT
    DATEPART(hour, submit_time) AS hour,
    MAX(concurrent_queries) AS peak_concurrent
FROM (
    SELECT
        submit_time,
        COUNT(*) OVER (
            ORDER BY submit_time
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) - COUNT(*) OVER (
            ORDER BY end_time
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS concurrent_queries
    FROM sys.dm_pdw_exec_requests
    WHERE submit_time > DATEADD(day, -7, GETDATE())
) subquery
GROUP BY DATEPART(hour, submit_time);
```

### Sizing Recommendations

| Current DWU | Avg CPU % | Recommendation |
|-------------|-----------|----------------|
| DW1000c | < 30% | Downsize to DW500c |
| DW1000c | 30-70% | Optimal |
| DW1000c | > 70% | Consider DW1500c |

```bash
# Scale dedicated SQL pool
az synapse sql pool update \
    --name dedicated-pool \
    --workspace-name synapse-ws \
    --resource-group rg-analytics \
    --performance-level DW500c
```

---

## Step 2: Spark Pool Analysis

### Analyze Job Metrics

```python
# PySpark: Analyze Spark job efficiency
def analyze_spark_efficiency(job_history_df):
    """Analyze Spark job resource efficiency."""

    analysis = job_history_df.groupBy("spark_pool").agg(
        F.avg("executor_count").alias("avg_executors"),
        F.max("executor_count").alias("max_executors"),
        F.avg("memory_used_gb").alias("avg_memory_gb"),
        F.avg("cpu_utilization").alias("avg_cpu_pct"),
        F.avg("duration_minutes").alias("avg_duration")
    )

    # Identify over-provisioned pools
    over_provisioned = analysis.filter(
        (F.col("avg_cpu_pct") < 50) |
        (F.col("avg_executors") < F.col("max_executors") * 0.5)
    )

    return over_provisioned
```

### KQL Analysis

```kusto
// Spark pool utilization
SynapseSparkPoolLogs
| where TimeGenerated > ago(7d)
| summarize
    AvgExecutors = avg(ExecutorCount),
    MaxExecutors = max(ExecutorCount),
    AvgMemoryGB = avg(MemoryUsedGB),
    P95MemoryGB = percentile(MemoryUsedGB, 95),
    JobCount = count()
    by SparkPoolName
| extend UtilizationRatio = AvgExecutors / MaxExecutors
| where UtilizationRatio < 0.5
| project SparkPoolName, AvgExecutors, MaxExecutors, UtilizationRatio,
          Recommendation = "Consider reducing max executors"
```

### Sizing Recommendations

| Pool Size | Avg Utilization | Recommendation |
|-----------|-----------------|----------------|
| Large (50+ nodes) | < 30% | Reduce to Medium |
| Medium (20-50) | 30-70% | Optimal |
| Any | > 80% consistent | Enable autoscale |

```json
// Spark pool autoscale configuration
{
    "autoScale": {
        "enabled": true,
        "minNodeCount": 3,
        "maxNodeCount": 20
    },
    "autoPause": {
        "enabled": true,
        "delayInMinutes": 15
    }
}
```

---

## Step 3: Storage Optimization

### Identify Unused Data

```python
# Find stale data in Data Lake
from azure.storage.filedatalake import DataLakeServiceClient

def find_stale_data(container_name, days_threshold=90):
    """Find files not accessed in X days."""

    service_client = DataLakeServiceClient(
        account_url=f"https://{storage_account}.dfs.core.windows.net",
        credential=credential
    )

    container = service_client.get_file_system_client(container_name)
    stale_files = []

    for path in container.get_paths(recursive=True):
        if path.is_directory:
            continue

        age_days = (datetime.now(timezone.utc) - path.last_modified).days
        if age_days > days_threshold:
            stale_files.append({
                "path": path.name,
                "size_gb": path.content_length / (1024**3),
                "age_days": age_days
            })

    return stale_files
```

### Implement Lifecycle Management

```json
{
    "rules": [
        {
            "name": "move-to-cool",
            "enabled": true,
            "type": "Lifecycle",
            "definition": {
                "filters": {
                    "blobTypes": ["blockBlob"],
                    "prefixMatch": ["bronze/", "staging/"]
                },
                "actions": {
                    "baseBlob": {
                        "tierToCool": {
                            "daysAfterModificationGreaterThan": 30
                        },
                        "tierToArchive": {
                            "daysAfterModificationGreaterThan": 90
                        }
                    }
                }
            }
        }
    ]
}
```

---

## Step 4: Continuous Optimization

### Weekly Review Process

1. **Collect Metrics** - Pull utilization data
2. **Analyze Trends** - Identify over/under-provisioned resources
3. **Implement Changes** - Scale resources appropriately
4. **Monitor Impact** - Verify performance maintained

### Automation Script

```python
def weekly_rightsizing_review():
    """Automated weekly right-sizing analysis."""

    recommendations = []

    # Check SQL pools
    sql_util = get_sql_pool_utilization()
    if sql_util["avg_cpu"] < 30:
        recommendations.append({
            "resource": "dedicated-pool",
            "action": "DOWNSIZE",
            "reason": f"Low CPU utilization: {sql_util['avg_cpu']}%"
        })

    # Check Spark pools
    spark_util = get_spark_pool_utilization()
    for pool in spark_util:
        if pool["avg_executors"] < pool["max_executors"] * 0.3:
            recommendations.append({
                "resource": pool["name"],
                "action": "REDUCE_MAX_NODES",
                "reason": f"Low executor utilization"
            })

    # Send report
    send_recommendations_report(recommendations)

    return recommendations
```

---

## Cost Impact Calculator

| Resource Change | Monthly Savings |
|----------------|-----------------|
| DW1000c → DW500c | ~$3,000 |
| Large Spark → Medium | ~$1,500 |
| Hot → Cool storage (100TB) | ~$1,000 |
| Auto-pause enabled | ~$2,000 |

---

## Related Documentation

- [Cost Tracking](../monitoring/cost-tracking.md)
- [Cost Optimization](../../best-practices/cost-optimization/README.md)
- [Performance Optimization](../../best-practices/performance-optimization/README.md)

---

*Last Updated: January 2025*
