# Azure Databricks Code Examples

> **[Home](../../../README.md)** | **[Code Examples](../../README.md)** | **Databricks**

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Languages](https://img.shields.io/badge/Languages-PySpark%20%7C%20SQL%20%7C%20Python-blue)
![Complexity](https://img.shields.io/badge/Complexity-Beginner_to_Advanced-orange)

Practical code examples for Azure Databricks covering PySpark DataFrames, Databricks SQL, Unity Catalog governance, cluster management, and storage access patterns.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [PySpark DataFrame Operations](#pyspark-dataframe-operations)
- [Databricks SQL Examples](#databricks-sql-examples)
- [Unity Catalog Examples](#unity-catalog-examples)
- [Cluster API Usage](#cluster-api-usage)
- [Storage Access Patterns](#storage-access-patterns)
- [Best Practices](#best-practices)

---

## Prerequisites

### Azure Resources

- Azure Databricks workspace (Premium tier for Unity Catalog)
- Azure Data Lake Storage Gen2 account
- Azure Key Vault (for secrets management)

### Development Environment

```bash
pip install databricks-sdk>=0.20.0
pip install azure-identity>=1.12.0
pip install pyspark==3.5.0
```

### Permissions

- Contributor role on the Databricks workspace
- Storage Blob Data Contributor on ADLS Gen2
- Key Vault Secrets User (for secret-backed scopes)

---

## PySpark DataFrame Operations

### Reading Data from ADLS Gen2

**Use Case**: Load raw data from the data lake into a Spark DataFrame for processing.

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, year, month

spark = SparkSession.builder.getOrCreate()

# Read CSV from ADLS Gen2 using abfss protocol
raw_df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("abfss://raw@csadatalake.dfs.core.windows.net/sales/2024/")

raw_df.printSchema()
raw_df.show(5)

# Read Parquet files (schema is embedded in the file format)
parquet_df = spark.read \
    .parquet("abfss://curated@csadatalake.dfs.core.windows.net/customers/")

# Read JSON with a defined schema for better performance
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

event_schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("user_id", StringType(), False),
    StructField("action", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("event_time", TimestampType(), True)
])

events_df = spark.read \
    .schema(event_schema) \
    .json("abfss://raw@csadatalake.dfs.core.windows.net/events/")
```

### Transformations and Aggregations

**Use Case**: Clean, enrich, and summarize data before writing to the curated layer.

```python
from pyspark.sql.functions import (
    col, when, sum as _sum, avg, count,
    row_number, dense_rank, lag, datediff, current_date
)
from pyspark.sql.window import Window

# Filter, rename, and add computed columns
cleaned_df = raw_df \
    .filter(col("order_status").isin("completed", "shipped")) \
    .withColumnRenamed("cust_id", "customer_id") \
    .withColumn("order_date", to_date(col("order_date_str"), "yyyy-MM-dd")) \
    .withColumn("order_year", year(col("order_date"))) \
    .withColumn("order_month", month(col("order_date"))) \
    .withColumn(
        "order_size",
        when(col("total_amount") >= 500, "large")
        .when(col("total_amount") >= 100, "medium")
        .otherwise("small")
    ) \
    .drop("order_date_str")

# Window function: rank customers by spend within each region
window_spec = Window.partitionBy("region").orderBy(col("total_amount").desc())

ranked_df = cleaned_df \
    .withColumn("spend_rank", dense_rank().over(window_spec))

# Aggregation: monthly revenue summary
monthly_summary = cleaned_df \
    .groupBy("order_year", "order_month", "region") \
    .agg(
        _sum("total_amount").alias("total_revenue"),
        avg("total_amount").alias("avg_order_value"),
        count("order_id").alias("order_count")
    ) \
    .orderBy("order_year", "order_month")

monthly_summary.show()
```

### Writing to Delta Lake

**Use Case**: Persist processed data as Delta tables for reliable downstream consumption.

```python
# Write as a partitioned Delta table
cleaned_df.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("order_year", "order_month") \
    .save("abfss://curated@csadatalake.dfs.core.windows.net/delta/orders")

# Append new records (idempotent with merge shown below)
new_orders_df.write \
    .format("delta") \
    .mode("append") \
    .save("abfss://curated@csadatalake.dfs.core.windows.net/delta/orders")

# Upsert (merge) pattern using Delta Lake
from delta.tables import DeltaTable

target_table = DeltaTable.forPath(
    spark,
    "abfss://curated@csadatalake.dfs.core.windows.net/delta/orders"
)

target_table.alias("target").merge(
    new_orders_df.alias("source"),
    "target.order_id = source.order_id"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()

print("Delta merge completed successfully.")
```

---

## Databricks SQL Examples

### Creating and Managing Tables

**Use Case**: Define managed and external Delta tables for analysts to query with SQL.

```sql
-- Create a managed Delta table in the default catalog
CREATE TABLE IF NOT EXISTS sales.orders (
    order_id       STRING    NOT NULL,
    customer_id    STRING    NOT NULL,
    order_date     DATE,
    total_amount   DECIMAL(12,2),
    order_status   STRING,
    region         STRING
)
USING DELTA
PARTITIONED BY (region)
COMMENT 'Curated orders table partitioned by region';

-- Create an external table pointing to ADLS
CREATE TABLE IF NOT EXISTS sales.raw_events
USING DELTA
LOCATION 'abfss://curated@csadatalake.dfs.core.windows.net/delta/events'
COMMENT 'External table backed by Delta files on ADLS Gen2';

-- Insert data from a staging table
INSERT INTO sales.orders
SELECT order_id, customer_id, order_date, total_amount, order_status, region
FROM sales.staging_orders
WHERE order_date >= '2024-01-01';
```

### Analytical Queries

**Use Case**: Run reporting queries against Delta tables with window functions and CTEs.

```sql
-- Monthly revenue trend with running total
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date)  AS revenue_month,
        region,
        SUM(total_amount)                AS monthly_total,
        COUNT(DISTINCT customer_id)      AS unique_customers
    FROM sales.orders
    WHERE order_status = 'completed'
    GROUP BY 1, 2
)
SELECT
    revenue_month,
    region,
    monthly_total,
    unique_customers,
    SUM(monthly_total) OVER (
        PARTITION BY region
        ORDER BY revenue_month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_revenue
FROM monthly_revenue
ORDER BY region, revenue_month;

-- Delta Lake time travel: query data as of a prior version
SELECT COUNT(*) AS row_count
FROM sales.orders VERSION AS OF 5;

-- Show table history
DESCRIBE HISTORY sales.orders;

-- Optimize table layout for query performance
OPTIMIZE sales.orders
ZORDER BY (customer_id);
```

---

## Unity Catalog Examples

### Creating Catalogs and Schemas

**Use Case**: Set up a three-level namespace (catalog.schema.table) for data governance.

```sql
-- Create a new catalog for the analytics domain
CREATE CATALOG IF NOT EXISTS analytics
COMMENT 'Catalog for curated analytics datasets';

-- Create schemas within the catalog
CREATE SCHEMA IF NOT EXISTS analytics.sales
COMMENT 'Sales domain tables and views';

CREATE SCHEMA IF NOT EXISTS analytics.marketing
COMMENT 'Marketing analytics datasets';

-- Create a managed table inside the governed namespace
CREATE TABLE analytics.sales.daily_revenue (
    revenue_date   DATE,
    region         STRING,
    product_line   STRING,
    revenue        DECIMAL(14,2),
    units_sold     INT
)
USING DELTA
COMMENT 'Daily revenue aggregated by region and product line';

-- View the full namespace
SHOW CATALOGS;
SHOW SCHEMAS IN analytics;
SHOW TABLES IN analytics.sales;
```

### Setting Permissions

**Use Case**: Grant fine-grained access to data assets through Unity Catalog.

```sql
-- Grant read access to analysts on the sales schema
GRANT USE CATALOG ON CATALOG analytics TO `analysts_group`;
GRANT USE SCHEMA  ON SCHEMA analytics.sales TO `analysts_group`;
GRANT SELECT      ON SCHEMA analytics.sales TO `analysts_group`;

-- Grant full access to the data engineering team
GRANT ALL PRIVILEGES ON SCHEMA analytics.sales TO `data_engineers`;

-- Grant read access to a single table
GRANT SELECT ON TABLE analytics.sales.daily_revenue TO `dashboard_service`;

-- Revoke access
REVOKE SELECT ON TABLE analytics.sales.daily_revenue FROM `former_contractor`;

-- View current grants
SHOW GRANTS ON SCHEMA analytics.sales;
SHOW GRANTS ON TABLE analytics.sales.daily_revenue;
```

---

## Cluster API Usage

### Managing Clusters Programmatically

**Use Case**: Automate cluster lifecycle operations from CI/CD pipelines or management scripts.

```python
"""
Databricks Cluster API examples using the Databricks SDK.
Useful for automating cluster creation, scaling, and teardown.
"""

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.compute import (
    ClusterSpec, AutoScale, AzureAttributes, RuntimeEngine
)

# Authenticate using Azure AD (Managed Identity or service principal)
client = WorkspaceClient(
    host="https://adb-1234567890123456.7.azuredatabricks.net"
)

# --- List existing clusters ---
for cluster in client.clusters.list():
    print(f"{cluster.cluster_name}: {cluster.state.value}")


# --- Create a new job cluster specification ---
new_cluster = client.clusters.create(
    cluster_name="etl-processing-cluster",
    spark_version="14.3.x-scala2.12",
    node_type_id="Standard_DS4_v2",
    autoscale=AutoScale(min_workers=2, max_workers=8),
    azure_attributes=AzureAttributes(
        first_on_demand=1,
        availability="ON_DEMAND_AZURE",
        spot_bid_max_price=-1
    ),
    spark_conf={
        "spark.sql.adaptive.enabled": "true",
        "spark.databricks.delta.optimizeWrite.enabled": "true",
        "spark.databricks.delta.autoCompact.enabled": "true"
    },
    custom_tags={"project": "csa-inabox", "env": "dev"}
).result()  # .result() waits for the cluster to reach RUNNING state

print(f"Cluster created: {new_cluster.cluster_id}")


# --- Resize a running cluster ---
client.clusters.resize(
    cluster_id=new_cluster.cluster_id,
    autoscale=AutoScale(min_workers=4, max_workers=16)
)
print("Cluster resize initiated.")


# --- Terminate a cluster when the workload is complete ---
client.clusters.delete(cluster_id=new_cluster.cluster_id)
print("Cluster termination initiated.")
```

### Listing Cluster Events

**Use Case**: Audit cluster activity for cost tracking and troubleshooting.

```python
from databricks.sdk.service.compute import GetEvents, ClusterEventType

events = client.clusters.events(
    cluster_id="0101-123456-abcde123",
    event_types=[
        ClusterEventType.CREATING,
        ClusterEventType.RUNNING,
        ClusterEventType.TERMINATING,
        ClusterEventType.RESIZING
    ],
    limit=50
)

for event in events.events:
    print(f"{event.timestamp} | {event.type.value} | {event.details}")
```

---

## Storage Access Patterns

### Service Principal with Secret Scope

**Use Case**: Access ADLS Gen2 securely using a service principal whose credentials are stored in Azure Key Vault via a Databricks secret scope.

```python
# Configure Spark to use a service principal for ADLS access.
# The secrets are stored in a Databricks secret scope backed by Azure Key Vault.

storage_account = "csadatalake"

spark.conf.set(
    f"fs.azure.account.auth.type.{storage_account}.dfs.core.windows.net",
    "OAuth"
)
spark.conf.set(
    f"fs.azure.account.oauth.provider.type.{storage_account}.dfs.core.windows.net",
    "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider"
)
spark.conf.set(
    f"fs.azure.account.oauth2.client.id.{storage_account}.dfs.core.windows.net",
    dbutils.secrets.get(scope="keyvault-scope", key="sp-client-id")
)
spark.conf.set(
    f"fs.azure.account.oauth2.client.secret.{storage_account}.dfs.core.windows.net",
    dbutils.secrets.get(scope="keyvault-scope", key="sp-client-secret")
)
spark.conf.set(
    f"fs.azure.account.oauth2.client.endpoint.{storage_account}.dfs.core.windows.net",
    f"https://login.microsoftonline.com/{dbutils.secrets.get(scope='keyvault-scope', key='tenant-id')}/oauth2/token"
)

# Now you can read/write using abfss
df = spark.read.parquet(
    f"abfss://curated@{storage_account}.dfs.core.windows.net/delta/customers"
)
df.show(5)
```

### Mount Points (Legacy)

**Use Case**: Create a DBFS mount point for simplified path access. Note that Unity Catalog external locations are the recommended approach for new workspaces.

```python
# Mount an ADLS Gen2 container to DBFS (legacy approach).
configs = {
    "fs.azure.account.auth.type": "OAuth",
    "fs.azure.account.oauth.provider.type":
        "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
    "fs.azure.account.oauth2.client.id":
        dbutils.secrets.get(scope="keyvault-scope", key="sp-client-id"),
    "fs.azure.account.oauth2.client.secret":
        dbutils.secrets.get(scope="keyvault-scope", key="sp-client-secret"),
    "fs.azure.account.oauth2.client.endpoint":
        "https://login.microsoftonline.com/<tenant-id>/oauth2/token"
}

dbutils.fs.mount(
    source="abfss://curated@csadatalake.dfs.core.windows.net/",
    mount_point="/mnt/curated",
    extra_configs=configs
)

# Verify the mount
display(dbutils.fs.ls("/mnt/curated"))

# Read data using the mount point
df = spark.read.format("delta").load("/mnt/curated/delta/orders")
df.show(5)

# Unmount when no longer needed
# dbutils.fs.unmount("/mnt/curated")
```

---

## Best Practices

1. **Use Unity Catalog** instead of legacy HMS and mount points for new projects
2. **Prefer Delta Lake** for all persistent storage to get ACID transactions, time travel, and schema enforcement
3. **Enable Adaptive Query Execution** (`spark.sql.adaptive.enabled=true`) for automatic optimization
4. **Use Auto-Optimize** settings (`optimizeWrite` and `autoCompact`) to keep Delta tables healthy
5. **Store secrets in Azure Key Vault** and access them through Databricks secret scopes
6. **Use autoscaling clusters** for variable workloads to balance cost and performance
7. **Partition by low-cardinality columns** (date, region) and use Z-ordering for high-cardinality filter columns
8. **Schedule OPTIMIZE and VACUUM** to maintain table performance and manage storage costs

---

*Last Updated: 2026-04-07*
*Version: 1.0.0*
