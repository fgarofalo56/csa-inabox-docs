# 📥 Data Loading Tutorial

> **🏠 [Home](../../../README.md)** | **📚 Documentation** | **📖 [Guides](../README.md)** | **🎓 [Tutorials](./README.md)** | **📥 Data Loading**

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Complexity](https://img.shields.io/badge/Complexity-Basic-green)
![Duration](https://img.shields.io/badge/Duration-30%20min-blue)

---

## 📋 Overview

Learn how to load data from various sources into Azure Data Lake Storage using Azure Synapse Analytics. This hands-on tutorial covers batch and streaming data ingestion patterns.

## 🎯 Learning Objectives

By the end of this tutorial, you will:

- ✅ Load CSV files into Delta Lake
- ✅ Ingest data from Azure Blob Storage
- ✅ Stream data from Event Hubs
- ✅ Implement incremental loading patterns
- ✅ Handle schema evolution

## 📑 Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1: Setup Environment](#step-1-setup-environment)
- [Step 2: Load CSV Files](#step-2-load-csv-files)
- [Step 3: Batch Load from Blob Storage](#step-3-batch-load-from-blob-storage)
- [Step 4: Stream from Event Hubs](#step-4-stream-from-event-hubs)
- [Step 5: Incremental Loading](#step-5-incremental-loading)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

---

## ✅ Prerequisites

### Required Resources

- [ ] Azure Synapse Analytics workspace
- [ ] Azure Data Lake Storage Gen2 account
- [ ] Spark pool (Small or Medium size)
- [ ] Sample data files (provided below)

### Required Knowledge

- Basic Python programming
- Understanding of DataFrames
- Familiarity with Azure Portal

### Estimated Time

⏱️ **30 minutes**

---

## 🚀 Step 1: Setup Environment

### Connect to Synapse Workspace

1. Navigate to [Azure Portal](https://portal.azure.com)
2. Open your Synapse workspace
3. Click **"Open Synapse Studio"**
4. Go to **Develop** → **Notebooks**
5. Create a new notebook: **"Data Loading Tutorial"**

### Initialize Spark Session

```python
# Cell 1: Initialize Spark with Delta Lake
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Spark is pre-configured in Synapse, but we'll set Delta configs
spark.conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
spark.conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

print("✅ Spark session initialized")
print(f"Spark version: {spark.version}")
```

### Configure Storage Access

```python
# Cell 2: Configure storage access using Managed Identity
storage_account = "your_storage_account"  # Replace with your storage account name

# Configure OAuth authentication
spark.conf.set(
    f"fs.azure.account.auth.type.{storage_account}.dfs.core.windows.net",
    "OAuth"
)
spark.conf.set(
    f"fs.azure.account.oauth.provider.type.{storage_account}.dfs.core.windows.net",
    "org.apache.hadoop.fs.azurebfs.oauth2.MsiTokenProvider"
)

# Define base paths
bronze_path = f"abfss://bronze@{storage_account}.dfs.core.windows.net"
silver_path = f"abfss://silver@{storage_account}.dfs.core.windows.net"
gold_path = f"abfss://gold@{storage_account}.dfs.core.windows.net"

print("✅ Storage access configured")
```

---

## 📄 Step 2: Load CSV Files

### Create Sample Data

```python
# Cell 3: Create sample customer data
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType
from datetime import date

# Define schema
schema = StructType([
    StructField("customer_id", IntegerType(), False),
    StructField("first_name", StringType(), False),
    StructField("last_name", StringType(), False),
    StructField("email", StringType(), True),
    StructField("country", StringType(), False),
    StructField("registration_date", DateType(), False)
])

# Create sample data
data = [
    (1, "John", "Doe", "john.doe@email.com", "USA", date(2024, 1, 15)),
    (2, "Jane", "Smith", "jane.smith@email.com", "UK", date(2024, 2, 20)),
    (3, "Bob", "Johnson", "bob.j@email.com", "Canada", date(2024, 3, 10)),
    (4, "Alice", "Williams", "alice.w@email.com", "Australia", date(2024, 1, 25)),
    (5, "Charlie", "Brown", "charlie.b@email.com", "USA", date(2024, 2, 5))
]

df = spark.createDataFrame(data, schema)

# Save as CSV for testing
csv_path = f"{bronze_path}/landing/customers.csv"
df.write.mode("overwrite").option("header", "true").csv(csv_path)

print("✅ Sample CSV created")
df.show()
```

### Load CSV into Delta Lake

```python
# Cell 4: Load CSV into Bronze layer
# Read CSV
customers_df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(f"{bronze_path}/landing/customers.csv")

# Add ingestion metadata
from pyspark.sql.functions import current_timestamp, lit

customers_bronze = customers_df \
    .withColumn("ingestion_timestamp", current_timestamp()) \
    .withColumn("source_file", lit("customers.csv"))

# Write to Bronze Delta table
bronze_table_path = f"{bronze_path}/raw/customers"
customers_bronze.write \
    .format("delta") \
    .mode("overwrite") \
    .option("mergeSchema", "true") \
    .save(bronze_table_path)

print("✅ Data loaded to Bronze layer")
print(f"Table location: {bronze_table_path}")

# Verify
spark.read.format("delta").load(bronze_table_path).show()
```

---

## 📦 Step 3: Batch Load from Blob Storage

### Batch Load with Schema Validation

```python
# Cell 5: Load with schema enforcement
from pyspark.sql.types import StructType, StructField

# Define expected schema
expected_schema = StructType([
    StructField("customer_id", IntegerType(), False),
    StructField("first_name", StringType(), False),
    StructField("last_name", StringType(), False),
    StructField("email", StringType(), True),
    StructField("country", StringType(), False),
    StructField("registration_date", DateType(), False)
])

try:
    # Read with schema enforcement
    df = spark.read \
        .schema(expected_schema) \
        .option("header", "true") \
        .option("mode", "FAILFAST") \
        .csv(f"{bronze_path}/landing/customers.csv")

    print("✅ Schema validation passed")

    # Cleanse and write to Silver
    silver_df = df \
        .dropDuplicates(["customer_id"]) \
        .filter(col("email").isNotNull()) \
        .withColumn("full_name", concat(col("first_name"), lit(" "), col("last_name"))) \
        .withColumn("processed_timestamp", current_timestamp())

    silver_table_path = f"{silver_path}/cleansed/customers"
    silver_df.write \
        .format("delta") \
        .mode("overwrite") \
        .partitionBy("country") \
        .save(silver_table_path)

    print("✅ Data loaded to Silver layer")
    spark.read.format("delta").load(silver_table_path).show()

except Exception as e:
    print(f"❌ Schema validation failed: {e}")
```

### Load Multiple Files

```python
# Cell 6: Batch load multiple files
# Create additional sample files
for i in range(1, 4):
    data = [
        (100+i, f"User{i}", f"Last{i}", f"user{i}@email.com", "USA", date(2024, i, 1))
    ]
    temp_df = spark.createDataFrame(data, schema)
    temp_df.write.mode("overwrite").option("header", "true") \
        .csv(f"{bronze_path}/landing/batch/customers_part_{i}.csv")

# Load all files at once
all_files_path = f"{bronze_path}/landing/batch/*.csv"
batch_df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(all_files_path)

print(f"✅ Loaded {batch_df.count()} records from multiple files")
batch_df.show()
```

---

## 🌊 Step 4: Stream from Event Hubs

### Setup Event Hubs Connection

```python
# Cell 7: Configure Event Hubs connection
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Get Event Hubs connection string from Key Vault
credential = DefaultAzureCredential()
kv_client = SecretClient(
    vault_url="https://your-keyvault.vault.azure.net",
    credential=credential
)

# In production, get from Key Vault
# connection_string = kv_client.get_secret("EventHubsConnectionString").value

# For this tutorial, configure directly
eventhub_namespace = "your-eventhub-namespace"
eventhub_name = "customer-events"

# Event Hubs configuration
eventhub_config = {
    "eventhubs.connectionString": sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(
        f"Endpoint=sb://{eventhub_namespace}.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=YOUR_KEY;EntityPath={eventhub_name}"
    )
}
```

### Stream Data

```python
# Cell 8: Stream from Event Hubs
# Read stream
stream_df = spark.readStream \
    .format("eventhubs") \
    .options(**eventhub_config) \
    .load()

# Parse JSON payload
from pyspark.sql.functions import from_json, col

# Define schema for event data
event_schema = StructType([
    StructField("customer_id", IntegerType()),
    StructField("event_type", StringType()),
    StructField("event_timestamp", StringType()),
    StructField("properties", StringType())
])

# Parse events
parsed_stream = stream_df \
    .selectExpr("CAST(body AS STRING)") \
    .select(from_json(col("body"), event_schema).alias("data")) \
    .select("data.*") \
    .withColumn("processing_time", current_timestamp())

# Write stream to Delta Lake
checkpoint_path = f"{bronze_path}/checkpoints/customer_events"
output_path = f"{bronze_path}/streaming/customer_events"

query = parsed_stream.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", checkpoint_path) \
    .start(output_path)

print("✅ Streaming query started")
print(f"Query ID: {query.id}")

# Monitor for 30 seconds then stop
import time
time.sleep(30)
query.stop()
print("✅ Streaming query stopped")
```

---

## 🔄 Step 5: Incremental Loading

### Implement Watermark-Based Loading

```python
# Cell 9: Incremental load with watermark
from delta.tables import DeltaTable

# Check if target table exists
target_path = f"{silver_path}/incremental/customers"

try:
    target_table = DeltaTable.forPath(spark, target_path)
    # Get max timestamp from target
    max_timestamp = spark.read.format("delta").load(target_path) \
        .agg(max("registration_date")).collect()[0][0]

    print(f"✅ Found existing table, max date: {max_timestamp}")

    # Load only new records
    new_records = customers_bronze \
        .filter(col("registration_date") > max_timestamp)

except Exception as e:
    print(f"ℹ️ No existing table found, loading all records")
    new_records = customers_bronze

# Append new records
if new_records.count() > 0:
    new_records.write \
        .format("delta") \
        .mode("append") \
        .save(target_path)

    print(f"✅ Loaded {new_records.count()} new records")
else:
    print("ℹ️ No new records to load")

# Verify
spark.read.format("delta").load(target_path).show()
```

### Upsert (Merge) Pattern

```python
# Cell 10: Implement upsert with merge
from delta.tables import DeltaTable

# Create updated records
updates = spark.createDataFrame([
    (1, "John", "Doe-Updated", "john.new@email.com", "USA", date(2024, 1, 15)),
    (6, "New", "Customer", "new.customer@email.com", "Germany", date(2024, 4, 1))
], schema)

# Add metadata
updates_with_meta = updates \
    .withColumn("ingestion_timestamp", current_timestamp()) \
    .withColumn("source_file", lit("updates.csv"))

# Perform merge
target_table = DeltaTable.forPath(spark, bronze_table_path)

target_table.alias("target").merge(
    updates_with_meta.alias("source"),
    "target.customer_id = source.customer_id"
).whenMatchedUpdateAll(
).whenNotMatchedInsertAll(
).execute()

print("✅ Merge completed")

# Verify - should see updated email and new customer
spark.read.format("delta").load(bronze_table_path) \
    .orderBy("customer_id") \
    .show()
```

---

## ✅ Best Practices

### 1. Schema Management

```python
# Define and enforce schemas
schema = StructType([
    StructField("id", IntegerType(), False),  # Not nullable
    StructField("value", StringType(), True)  # Nullable
])

df = spark.read.schema(schema).csv(path)
```

### 2. Error Handling

```python
# Handle bad records
df = spark.read \
    .option("mode", "PERMISSIVE") \
    .option("columnNameOfCorruptRecord", "_corrupt_record") \
    .csv(path)

# Filter and log bad records
bad_records = df.filter(col("_corrupt_record").isNotNull())
if bad_records.count() > 0:
    bad_records.write.mode("append").parquet(f"{bronze_path}/errors/")
    print(f"⚠️ Found {bad_records.count()} bad records")
```

### 3. Add Ingestion Metadata

```python
# Always add metadata
df_with_metadata = df \
    .withColumn("ingestion_timestamp", current_timestamp()) \
    .withColumn("source_file", input_file_name()) \
    .withColumn("source_system", lit("ERP"))
```

### 4. Partition Strategy

```python
# Partition by frequently filtered columns
df.write.format("delta") \
    .partitionBy("year", "month") \  # Good for time-series
    .save(path)

# Avoid high-cardinality partitions
# DON'T: .partitionBy("customer_id")  # Too many partitions
```

---

## 🔧 Troubleshooting

### Issue: Permission Denied

**Error:** `java.nio.file.AccessDeniedException`

**Solution:**
```python
# Verify Managed Identity has "Storage Blob Data Contributor" role
# Check in Azure Portal:
# Storage Account → Access Control (IAM) → Role assignments
```

### Issue: Schema Mismatch

**Error:** `org.apache.spark.sql.AnalysisException: cannot resolve column`

**Solution:**
```python
# Use explicit schema
schema = StructType([...])
df = spark.read.schema(schema).csv(path)

# Or allow schema evolution
df.write.format("delta") \
    .option("mergeSchema", "true") \
    .mode("append") \
    .save(path)
```

### Issue: Out of Memory

**Error:** `java.lang.OutOfMemoryError: Java heap space`

**Solution:**
```python
# Process in batches
df.coalesce(10) \  # Reduce partitions
    .write.format("delta") \
    .save(path)

# Or increase executor memory in Spark pool configuration
```

---

## 🎓 Next Steps

Now that you've completed this tutorial, you're ready for:

1. ✅ **[First Pipeline Tutorial](./first-pipeline.md)** - Build end-to-end pipeline
2. ✅ **[Spark Basics Tutorial](./spark-basics.md)** - Learn PySpark fundamentals
3. ✅ **[Data Transformation Patterns](../../code-examples/delta-lake/README.md)** - Advanced transformations

### Additional Resources

- [Delta Lake Documentation](https://docs.delta.io/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Azure Synapse Best Practices](https://learn.microsoft.com/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-best-practices)

---

## 💬 Feedback

How was this tutorial?

- ✅ **Completed successfully** - [Share your experience](https://github.com/fgarofalo56/csa-inabox-docs/discussions)
- ⚠️ **Had issues** - [Report problem](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?title=[Tutorial]+Data-Loading)
- 💡 **Have suggestions** - [Improve tutorial](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?title=[Tutorial]+Suggestion)

---

*Last Updated: December 2025*
*Version: 1.0.0*
*Maintainer: CSA in-a-Box Team*
