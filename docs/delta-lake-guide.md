# Delta Lake Comprehensive Guide

> **[Home](README.md)** | **Delta Lake Guide**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Technology](https://img.shields.io/badge/Technology-Delta%20Lake-00ADD8?style=flat-square)

Comprehensive guide to Delta Lake on Azure analytics platforms.

---

## Overview

Delta Lake is an open-source storage layer that brings ACID transactions, scalable metadata handling, and data versioning to data lakes.

### Key Features

| Feature | Description |
|---------|-------------|
| ACID Transactions | Serializable isolation for concurrent reads/writes |
| Time Travel | Query data at any point in history |
| Schema Enforcement | Prevent bad data from being written |
| Schema Evolution | Add columns without breaking downstream consumers |
| Unified Batch/Streaming | Same table for batch and streaming workloads |
| Data Versioning | Full audit trail of all changes |

---

## Getting Started

### Create Delta Table

```python
from pyspark.sql import SparkSession
from delta.tables import DeltaTable

spark = SparkSession.builder \
    .appName("DeltaLakeDemo") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Create Delta table from DataFrame
df = spark.createDataFrame([
    (1, "Alice", "2024-01-15"),
    (2, "Bob", "2024-01-16"),
    (3, "Charlie", "2024-01-17")
], ["id", "name", "created_date"])

df.write.format("delta").mode("overwrite").save("/delta/customers")

# Create managed Delta table
spark.sql("""
    CREATE TABLE IF NOT EXISTS customers (
        id INT,
        name STRING,
        created_date DATE
    )
    USING DELTA
    LOCATION '/delta/customers'
""")
```

---

## CRUD Operations

### Insert

```python
# Append new data
new_data = spark.createDataFrame([
    (4, "David", "2024-01-18")
], ["id", "name", "created_date"])

new_data.write.format("delta").mode("append").save("/delta/customers")
```

### Update

```python
from delta.tables import DeltaTable

delta_table = DeltaTable.forPath(spark, "/delta/customers")

# Update specific records
delta_table.update(
    condition="id = 1",
    set={"name": "'Alice Smith'"}
)
```

### Delete

```python
# Delete specific records
delta_table.delete(condition="id = 3")
```

### Merge (Upsert)

```python
# Source data with updates and inserts
updates = spark.createDataFrame([
    (1, "Alice Johnson", "2024-01-15"),  # Update
    (5, "Eve", "2024-01-19")              # Insert
], ["id", "name", "created_date"])

delta_table.alias("target").merge(
    updates.alias("source"),
    "target.id = source.id"
).whenMatchedUpdate(set={
    "name": "source.name"
}).whenNotMatchedInsert(values={
    "id": "source.id",
    "name": "source.name",
    "created_date": "source.created_date"
}).execute()
```

---

## Time Travel

### Query Historical Data

```python
# Query by version
df_v0 = spark.read.format("delta").option("versionAsOf", 0).load("/delta/customers")

# Query by timestamp
df_yesterday = spark.read.format("delta") \
    .option("timestampAsOf", "2024-01-17") \
    .load("/delta/customers")

# View table history
history = delta_table.history()
history.select("version", "timestamp", "operation", "operationParameters").show()
```

### Restore Table

```python
# Restore to previous version
delta_table.restoreToVersion(0)

# Restore to timestamp
delta_table.restoreToTimestamp("2024-01-17")
```

---

## Schema Management

### Schema Enforcement

```python
# Schema enforcement (default) - rejects incompatible writes
try:
    bad_data = spark.createDataFrame([
        (1, "Alice", 100)  # Wrong type for third column
    ], ["id", "name", "invalid_col"])
    bad_data.write.format("delta").mode("append").save("/delta/customers")
except Exception as e:
    print(f"Schema mismatch: {e}")
```

### Schema Evolution

```python
# Enable schema evolution
spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")

# Or use merge schema option
df_with_new_col = spark.createDataFrame([
    (6, "Frank", "2024-01-20", "frank@email.com")
], ["id", "name", "created_date", "email"])

df_with_new_col.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save("/delta/customers")
```

---

## Optimization

### OPTIMIZE Command

```python
# Optimize table (compact small files)
spark.sql("OPTIMIZE delta.`/delta/customers`")

# Optimize with Z-ordering
spark.sql("OPTIMIZE delta.`/delta/customers` ZORDER BY (id)")
```

### VACUUM

```python
# Remove old files (default 7 days retention)
spark.sql("VACUUM delta.`/delta/customers`")

# Remove files older than 24 hours (use with caution)
spark.sql("VACUUM delta.`/delta/customers` RETAIN 24 HOURS")
```

### Auto Optimization

```python
# Enable auto-optimization
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
spark.conf.set("spark.databricks.delta.autoOptimize.optimizeWrite", "true")
```

---

## Change Data Capture

### Enable CDC

```python
# Create CDC-enabled table
spark.sql("""
    CREATE TABLE orders (
        order_id INT,
        customer_id INT,
        amount DECIMAL(10,2),
        status STRING
    )
    USING DELTA
    TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")

# Read changes
changes = spark.read.format("delta") \
    .option("readChangeDataFeed", "true") \
    .option("startingVersion", 1) \
    .table("orders")

changes.select("order_id", "_change_type", "_commit_version", "_commit_timestamp").show()
```

---

## Streaming

### Read Stream

```python
# Read Delta table as stream
stream_df = spark.readStream \
    .format("delta") \
    .load("/delta/customers")

# Process stream
query = stream_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()
```

### Write Stream

```python
# Write stream to Delta
incoming_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "host:9092") \
    .option("subscribe", "events") \
    .load()

incoming_stream.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/checkpoints/events") \
    .start("/delta/events")
```

---

## Best Practices

### Table Design

- Use appropriate partition columns (low cardinality)
- Enable auto-optimization for write-heavy workloads
- Set appropriate data retention policies
- Use Z-ordering for frequently filtered columns

### Performance

- Run OPTIMIZE regularly for read-heavy tables
- Use VACUUM to manage storage costs
- Monitor file sizes (target 128MB-1GB)
- Enable statistics collection for predicate pushdown

### Data Quality

- Enable schema enforcement
- Use constraints for data validation
- Implement data quality checks with expectations
- Monitor CDC for auditing

---

## Related Documentation

- [Delta Lake Code Examples](code-examples/delta-lake/README.md)
- [Delta Lakehouse Architecture](architecture/delta-lakehouse/README.md)
- [Spark Performance Tuning](best-practices/spark-performance/README.md)

---

*Last Updated: January 2025*
