# Hadoop Migration Workshop

> **[Home](../../README.md)** | **[Tutorials](../README.md)** | **Hadoop Migration Workshop**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Level](https://img.shields.io/badge/Level-Advanced-red?style=flat-square)

Comprehensive workshop for migrating Hadoop workloads to Azure.

---

## Overview

This workshop covers:

- Assessment of existing Hadoop clusters
- Migration strategies and tooling
- Data migration to ADLS Gen2
- Workload migration to Databricks/Synapse
- Performance validation

**Duration**: 2 days | **Prerequisites**: Hadoop administration experience

---

## Workshop Agenda

### Day 1: Assessment & Planning

| Time | Topic |
|------|-------|
| 9:00-10:30 | Hadoop Architecture Review |
| 10:45-12:00 | Migration Assessment Tools |
| 13:00-14:30 | Target Architecture Design |
| 14:45-16:00 | Migration Planning |

### Day 2: Hands-On Migration

| Time | Topic |
|------|-------|
| 9:00-10:30 | Data Migration Lab |
| 10:45-12:00 | Hive to Spark Migration |
| 13:00-14:30 | Job Migration Workshop |
| 14:45-16:00 | Validation & Optimization |

---

## Module 1: Assessment

### Cluster Inventory Script

```python
#!/usr/bin/env python3
"""Hadoop cluster assessment script."""

import subprocess
import json

def assess_hadoop_cluster():
    """Collect Hadoop cluster information."""

    assessment = {
        "hdfs": {},
        "yarn": {},
        "hive": {},
        "spark": {}
    }

    # HDFS assessment
    hdfs_report = subprocess.run(
        ["hdfs", "dfsadmin", "-report"],
        capture_output=True, text=True
    )
    assessment["hdfs"]["capacity"] = parse_hdfs_capacity(hdfs_report.stdout)

    # YARN assessment
    yarn_nodes = subprocess.run(
        ["yarn", "node", "-list"],
        capture_output=True, text=True
    )
    assessment["yarn"]["nodes"] = parse_yarn_nodes(yarn_nodes.stdout)

    # Hive assessment
    hive_tables = subprocess.run(
        ["hive", "-e", "SHOW DATABASES; SHOW TABLES;"],
        capture_output=True, text=True
    )
    assessment["hive"]["tables"] = parse_hive_inventory(hive_tables.stdout)

    return assessment

def generate_migration_plan(assessment):
    """Generate migration recommendations."""

    recommendations = {
        "target_platform": "",
        "storage_tier": "",
        "compute_size": "",
        "estimated_cost": 0
    }

    hdfs_size_tb = assessment["hdfs"]["capacity"]["used_tb"]

    if hdfs_size_tb < 10:
        recommendations["target_platform"] = "Azure Synapse Spark"
        recommendations["storage_tier"] = "Hot"
    else:
        recommendations["target_platform"] = "Azure Databricks"
        recommendations["storage_tier"] = "Hot + Cool tiering"

    return recommendations
```

---

## Module 2: Data Migration

### HDFS to ADLS Gen2

```bash
# Using Azure Data Box for large migrations
# Step 1: Export data to Data Box
hdfs dfs -get /data/warehouse /mnt/databox/

# Step 2: After Data Box delivery, data appears in ADLS
# Verify with Azure CLI
az storage fs file list \
    --file-system data-lake \
    --account-name storageaccount \
    --path warehouse/

# Alternative: Use DistCp for online migration
hadoop distcp \
    -Dfs.azure.account.key.storageaccount.dfs.core.windows.net=<key> \
    hdfs://namenode:8020/data/warehouse \
    abfs://container@storageaccount.dfs.core.windows.net/warehouse/
```

### Data Factory Migration Pipeline

```json
{
    "name": "HadoopMigrationPipeline",
    "properties": {
        "activities": [
            {
                "name": "CopyFromHDFS",
                "type": "Copy",
                "inputs": [{"referenceName": "HDFSDataset", "type": "DatasetReference"}],
                "outputs": [{"referenceName": "ADLSGen2Dataset", "type": "DatasetReference"}],
                "typeProperties": {
                    "source": {
                        "type": "HdfsSource",
                        "recursive": true,
                        "distcpSettings": {
                            "resourceManagerEndpoint": "http://resourcemanager:8088",
                            "tempScriptPath": "/tmp/distcp"
                        }
                    },
                    "sink": {
                        "type": "ParquetSink",
                        "storeSettings": {
                            "type": "AzureBlobFSWriteSettings"
                        }
                    }
                }
            }
        ]
    }
}
```

---

## Module 3: Hive Migration

### Hive to Spark SQL

```python
# Original Hive Query
"""
SELECT
    customer_id,
    SUM(amount) as total_amount,
    COUNT(*) as order_count
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY customer_id
HAVING SUM(amount) > 1000
"""

# Equivalent Spark SQL
spark.sql("""
    SELECT
        customer_id,
        SUM(amount) as total_amount,
        COUNT(*) as order_count
    FROM delta.`abfss://data@storage.dfs.core.windows.net/orders`
    WHERE order_date >= '2024-01-01'
    GROUP BY customer_id
    HAVING SUM(amount) > 1000
""")

# Or using DataFrame API
from pyspark.sql import functions as F

orders_df = spark.read.format("delta").load("abfss://data@storage.dfs.core.windows.net/orders")

result = orders_df \
    .filter(F.col("order_date") >= "2024-01-01") \
    .groupBy("customer_id") \
    .agg(
        F.sum("amount").alias("total_amount"),
        F.count("*").alias("order_count")
    ) \
    .filter(F.col("total_amount") > 1000)
```

### Metastore Migration

```python
# Export Hive metastore
def export_hive_metastore():
    """Export Hive metastore to JSON for migration."""

    databases = spark.sql("SHOW DATABASES").collect()

    metastore = []
    for db in databases:
        db_name = db.databaseName
        tables = spark.sql(f"SHOW TABLES IN {db_name}").collect()

        for table in tables:
            table_info = {
                "database": db_name,
                "table": table.tableName,
                "schema": spark.sql(f"DESCRIBE {db_name}.{table.tableName}").collect(),
                "location": spark.sql(f"DESCRIBE FORMATTED {db_name}.{table.tableName}").collect()
            }
            metastore.append(table_info)

    return metastore

# Create equivalent tables in Unity Catalog
def create_unity_catalog_tables(metastore):
    """Create tables in Unity Catalog from Hive metadata."""

    for table in metastore:
        # Create external table pointing to migrated data
        spark.sql(f"""
            CREATE TABLE IF NOT EXISTS catalog.{table['database']}.{table['table']}
            USING DELTA
            LOCATION 'abfss://data@storage.dfs.core.windows.net/{table['database']}/{table['table']}'
        """)
```

---

## Module 4: Job Migration

### MapReduce to Spark

```python
# Original MapReduce word count (conceptual)
"""
public class WordCount {
    public static class Map extends Mapper<...> {
        public void map(...) { ... }
    }
    public static class Reduce extends Reducer<...> {
        public void reduce(...) { ... }
    }
}
"""

# Spark equivalent
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("WordCount").getOrCreate()

# Read text file
text_rdd = spark.sparkContext.textFile("abfss://data@storage.dfs.core.windows.net/input/")

# Word count
word_counts = text_rdd \
    .flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a + b)

# Save results
word_counts.toDF(["word", "count"]).write \
    .format("delta") \
    .save("abfss://data@storage.dfs.core.windows.net/output/wordcount")
```

---

## Module 5: Validation

### Data Validation Script

```python
def validate_migration(source_path, target_path):
    """Validate data migration completeness."""

    validation_results = {
        "row_count": {"source": 0, "target": 0, "match": False},
        "schema": {"match": False},
        "checksums": {"match": False}
    }

    # Compare row counts
    source_count = spark.read.parquet(source_path).count()
    target_count = spark.read.format("delta").load(target_path).count()

    validation_results["row_count"] = {
        "source": source_count,
        "target": target_count,
        "match": source_count == target_count
    }

    # Compare schemas
    source_schema = spark.read.parquet(source_path).schema
    target_schema = spark.read.format("delta").load(target_path).schema
    validation_results["schema"]["match"] = source_schema == target_schema

    return validation_results
```

---

## Related Documentation

- [Migration Strategies](../../best-practices/migration-strategies.md)
- [HDInsight Spark](../intermediate/hdinsight-spark.md)
- [Data Engineer Path](../data-engineer-path.md)

---

*Last Updated: January 2025*
