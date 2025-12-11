# Spark on HDInsight

> **[Home](../../README.md)** | **[Tutorials](../README.md)** | **HDInsight Spark**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Level](https://img.shields.io/badge/Level-Intermediate-yellow?style=flat-square)

Guide to Apache Spark on Azure HDInsight.

---

## Overview

This tutorial covers:

- HDInsight Spark cluster setup
- Jupyter notebook development
- Spark job optimization
- Integration with Azure services

**Duration**: 2 hours | **Prerequisites**: Basic Spark knowledge

---

## Cluster Setup

### Create Spark Cluster

```bash
az hdinsight create \
    --name spark-cluster \
    --resource-group rg-spark \
    --type spark \
    --version 3.1 \
    --component-version Spark=3.1 \
    --headnode-size Standard_E4_v3 \
    --workernode-size Standard_E4_v3 \
    --workernode-count 4 \
    --ssh-user admin \
    --ssh-password 'SecurePassword123!' \
    --storage-account storageaccount \
    --storage-container spark-data
```

---

## Jupyter Notebooks

### Access Jupyter

1. Navigate to cluster in Azure Portal
2. Click "Jupyter notebook" under Cluster dashboards
3. Authenticate with cluster credentials

### PySpark Example

```python
# Initialize Spark session (auto-configured in HDInsight)
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("HDInsightDemo").getOrCreate()

# Read from Azure Storage
df = spark.read \
    .format("parquet") \
    .load("wasbs://container@storageaccount.blob.core.windows.net/data/")

# Transform data
result = df \
    .filter(col("date") >= "2024-01-01") \
    .groupBy("category") \
    .agg(
        count("*").alias("count"),
        sum("amount").alias("total_amount"),
        avg("amount").alias("avg_amount")
    ) \
    .orderBy(desc("total_amount"))

# Write results
result.write \
    .format("parquet") \
    .mode("overwrite") \
    .save("wasbs://container@storageaccount.blob.core.windows.net/results/")

display(result)
```

---

## Spark Configuration

### Memory and Executors

```python
# In notebook or spark-defaults.conf
spark.conf.set("spark.executor.memory", "8g")
spark.conf.set("spark.executor.cores", "4")
spark.conf.set("spark.executor.instances", "8")
spark.conf.set("spark.driver.memory", "4g")

# Dynamic allocation
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.dynamicAllocation.minExecutors", "2")
spark.conf.set("spark.dynamicAllocation.maxExecutors", "20")
```

### Performance Tuning

```python
# Enable Adaptive Query Execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")

# Broadcast join threshold
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "50MB")

# Shuffle partitions
spark.conf.set("spark.sql.shuffle.partitions", "200")
```

---

## Azure Integration

### Read from ADLS Gen2

```python
# Configure ADLS access
spark.conf.set(
    "fs.azure.account.key.storageaccount.dfs.core.windows.net",
    dbutils.secrets.get(scope="keyvault", key="storage-key")
)

# Read from ADLS Gen2
df = spark.read \
    .format("delta") \
    .load("abfss://container@storageaccount.dfs.core.windows.net/delta/table")
```

### Write to Synapse

```python
# Write to Synapse dedicated pool
df.write \
    .format("com.databricks.spark.sqldw") \
    .option("url", "jdbc:sqlserver://synapse.sql.azuresynapse.net:1433;database=pool") \
    .option("tempDir", "wasbs://temp@storageaccount.blob.core.windows.net/") \
    .option("forwardSparkAzureStorageCredentials", "true") \
    .option("dbTable", "dbo.results") \
    .mode("overwrite") \
    .save()
```

---

## Submit Jobs

### Livy REST API

```bash
# Submit Spark job via Livy
curl -X POST \
    -u admin:password \
    -H "Content-Type: application/json" \
    https://spark-cluster.azurehdinsight.net/livy/batches \
    -d '{
        "file": "wasbs://jars@storageaccount.blob.core.windows.net/app.jar",
        "className": "com.example.SparkApp",
        "args": ["arg1", "arg2"],
        "driverMemory": "4g",
        "executorMemory": "8g",
        "executorCores": 4,
        "numExecutors": 8
    }'

# Check job status
curl -u admin:password \
    https://spark-cluster.azurehdinsight.net/livy/batches/0
```

---

## Monitoring

### Spark UI

Access via: `https://spark-cluster.azurehdinsight.net/sparkhistory`

### Key Metrics

| Metric | Target | Action |
|--------|--------|--------|
| Task duration | < 1 min | Optimize partitions |
| Shuffle read/write | Minimize | Use broadcast joins |
| GC time | < 10% | Increase memory |
| Failed tasks | 0 | Check data skew |

---

## Related Documentation

- [Spark SQL Tutorial](spark-sql-tutorial.md)
- [ML on Databricks](ml-databricks.md)
- [Data Engineer Path](../data-engineer-path.md)

---

*Last Updated: January 2025*
