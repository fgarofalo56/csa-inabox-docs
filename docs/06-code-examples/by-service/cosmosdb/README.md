# Azure Cosmos DB Code Examples

> **[Home](../../../README.md)** | **[Code Examples](../../README.md)** | **Cosmos DB**

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Languages](https://img.shields.io/badge/Languages-Python%20%7C%20SQL-blue)
![Complexity](https://img.shields.io/badge/Complexity-Beginner_to_Advanced-orange)

Practical code examples for Azure Cosmos DB in analytics scenarios, covering the Python SDK, Synapse Link integration, change feed processing, partition key strategies, and cost-optimized query patterns.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Python SDK Examples](#python-sdk-examples)
- [Synapse Link Integration](#synapse-link-integration)
- [Change Feed Processing](#change-feed-processing)
- [Partition Key Strategy](#partition-key-strategy)
- [Cost Optimization Patterns](#cost-optimization-patterns)
- [Best Practices](#best-practices)

---

## Prerequisites

### Azure Resources

- Azure Cosmos DB account (NoSQL API)
- Azure Synapse Analytics workspace (for Synapse Link examples)
- Azure Data Lake Storage Gen2 (for analytical store export)

### Development Environment

```bash
pip install azure-cosmos>=4.5.0
pip install azure-identity>=1.12.0
pip install azure-cosmos-change-feed>=0.1.0  # optional, for change feed
```

### Connection Details

```python
import os

COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]  # https://myaccount.documents.azure.com:443/
COSMOS_KEY = os.environ["COSMOS_KEY"]             # Use Key Vault in production
DATABASE_NAME = "analytics"
```

---

## Python SDK Examples

### Creating a Database and Container

**Use Case**: Set up a Cosmos DB database and container with appropriate throughput and indexing for an analytics workload.

```python
"""
Create a Cosmos DB database and container with the Python SDK.
Demonstrates provisioned throughput, partition key selection, and custom indexing.
"""

from azure.cosmos import CosmosClient, PartitionKey, exceptions

client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)

# Create database with shared throughput (cost effective for multiple containers)
try:
    database = client.create_database_if_not_exists(
        id=DATABASE_NAME,
        offer_throughput=1000  # 1000 RU/s shared across containers
    )
    print(f"Database '{DATABASE_NAME}' ready.")
except exceptions.CosmosHttpResponseError as e:
    print(f"Error creating database: {e.message}")
    raise

# Define an indexing policy optimized for analytical queries
indexing_policy = {
    "indexingMode": "consistent",
    "automatic": True,
    "includedPaths": [{"path": "/*"}],
    "excludedPaths": [{"path": "/raw_payload/*"}],  # Skip large unqueried fields
    "compositeIndexes": [
        [
            {"path": "/customer_id", "order": "ascending"},
            {"path": "/order_date", "order": "descending"}
        ]
    ]
}

# Create container with hierarchical partition key
container = database.create_container_if_not_exists(
    id="orders",
    partition_key=PartitionKey(path="/customer_id"),
    indexing_policy=indexing_policy,
    default_ttl=None,  # No automatic expiration
    analytical_storage_ttl=-1  # Enable analytical store (Synapse Link)
)
print(f"Container 'orders' ready. Analytical store enabled.")
```

### CRUD Operations

**Use Case**: Insert, read, update, and delete items in Cosmos DB with proper error handling.

```python
"""
Basic CRUD operations against a Cosmos DB container.
Each operation shows the RU charge so you can understand cost impact.
"""

import uuid
from datetime import datetime

container = database.get_container_client("orders")

# --- Create (insert) ---
order = {
    "id": str(uuid.uuid4()),
    "customer_id": "cust-1001",
    "order_date": datetime.utcnow().isoformat(),
    "items": [
        {"product_id": "prod-A", "quantity": 2, "unit_price": 29.99},
        {"product_id": "prod-B", "quantity": 1, "unit_price": 49.99}
    ],
    "total_amount": 109.97,
    "status": "pending",
    "region": "westus"
}

response = container.create_item(body=order)
print(f"Created order {response['id']}  |  RU charge: {container.client_connection.last_response_headers['x-ms-request-charge']}")

# --- Point read (fastest and cheapest operation) ---
read_item = container.read_item(
    item=order["id"],
    partition_key=order["customer_id"]
)
print(f"Read order {read_item['id']}  |  Status: {read_item['status']}")

# --- Replace (full update) ---
read_item["status"] = "shipped"
read_item["shipped_date"] = datetime.utcnow().isoformat()

replaced = container.replace_item(
    item=read_item["id"],
    body=read_item
)
print(f"Updated order {replaced['id']}  |  New status: {replaced['status']}")

# --- Patch (partial update, lower RU cost than replace) ---
operations = [
    {"op": "set", "path": "/status", "value": "delivered"},
    {"op": "add", "path": "/delivered_date", "value": datetime.utcnow().isoformat()}
]
patched = container.patch_item(
    item=order["id"],
    partition_key=order["customer_id"],
    patch_operations=operations
)
print(f"Patched order {patched['id']}  |  Status: {patched['status']}")

# --- Delete ---
container.delete_item(
    item=order["id"],
    partition_key=order["customer_id"]
)
print(f"Deleted order {order['id']}")
```

### Querying with SQL API

**Use Case**: Run cross-partition queries with filters, aggregations, and projections.

```python
"""
Query examples using the Cosmos DB SQL API.
Note: cross-partition queries cost more RUs than single-partition queries.
"""

# Single-partition query (most efficient)
query = "SELECT * FROM c WHERE c.customer_id = @cust_id AND c.status = 'shipped'"
params = [{"name": "@cust_id", "value": "cust-1001"}]

results = list(container.query_items(
    query=query,
    parameters=params,
    partition_key="cust-1001"
))
print(f"Found {len(results)} shipped orders for cust-1001")

# Cross-partition aggregation (fan-out query)
agg_query = """
    SELECT
        c.region,
        COUNT(1)       AS order_count,
        SUM(c.total_amount) AS total_revenue
    FROM c
    WHERE c.order_date >= '2024-01-01'
    GROUP BY c.region
"""

agg_results = list(container.query_items(
    query=agg_query,
    enable_cross_partition_query=True
))

for row in agg_results:
    print(f"  {row['region']}: {row['order_count']} orders, ${row['total_revenue']:.2f}")

# Projection with VALUE keyword (returns scalar values)
ids_query = "SELECT VALUE c.id FROM c WHERE c.status = 'pending' OFFSET 0 LIMIT 50"

pending_ids = list(container.query_items(
    query=ids_query,
    enable_cross_partition_query=True
))
print(f"Pending order IDs: {pending_ids[:5]}...")
```

---

## Synapse Link Integration

### Querying the Analytical Store from Synapse SQL

**Use Case**: Use Azure Synapse Link to query Cosmos DB operational data with T-SQL in a serverless SQL pool without impacting transactional workloads. The analytical store is a columnar copy of your data automatically maintained by Cosmos DB.

```sql
-- Run this in a Synapse serverless SQL pool.
-- Cosmos DB analytical store must be enabled on the container.

-- Query the analytical store directly
SELECT TOP 100
    customer_id,
    order_date,
    total_amount,
    status,
    region
FROM OPENROWSET(
    'CosmosDB',
    'Account=mycosmosaccount;Database=analytics;Key=<your-key>',
    orders
) AS orders
WHERE status = 'shipped'
ORDER BY order_date DESC;

-- Aggregation: revenue by region and month
SELECT
    region,
    FORMAT(CAST(order_date AS DATE), 'yyyy-MM') AS order_month,
    COUNT(*)          AS order_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value
FROM OPENROWSET(
    'CosmosDB',
    'Account=mycosmosaccount;Database=analytics;Key=<your-key>',
    orders
) WITH (
    customer_id    VARCHAR(50),
    order_date     VARCHAR(30),
    total_amount   FLOAT,
    status         VARCHAR(20),
    region         VARCHAR(20)
) AS orders
WHERE order_date >= '2024-01-01'
GROUP BY region, FORMAT(CAST(order_date AS DATE), 'yyyy-MM')
ORDER BY region, order_month;

-- Create an external view for repeated use
CREATE OR ALTER VIEW dbo.vw_cosmos_orders AS
SELECT
    customer_id,
    CAST(order_date AS DATE)     AS order_date,
    CAST(total_amount AS DECIMAL(12,2)) AS total_amount,
    status,
    region
FROM OPENROWSET(
    'CosmosDB',
    'Account=mycosmosaccount;Database=analytics;Key=<your-key>',
    orders
) WITH (
    customer_id    VARCHAR(50),
    order_date     VARCHAR(30),
    total_amount   FLOAT,
    status         VARCHAR(20),
    region         VARCHAR(20)
) AS orders;
```

### Querying from Synapse Spark

**Use Case**: Load Cosmos DB analytical store data into a Spark DataFrame for machine learning or complex transformations.

```python
# Run this in a Synapse Spark notebook

# Read from Cosmos DB analytical store via Synapse Link
df = spark.read \
    .format("cosmos.olap") \
    .option("spark.synapse.linkedService", "CosmosDbAnalytics") \
    .option("spark.cosmos.container", "orders") \
    .load()

df.printSchema()

# Filter and aggregate
from pyspark.sql.functions import col, sum as _sum, count, month, year

monthly_stats = df \
    .filter(col("status") == "shipped") \
    .withColumn("order_year", year(col("order_date"))) \
    .withColumn("order_month", month(col("order_date"))) \
    .groupBy("order_year", "order_month", "region") \
    .agg(
        _sum("total_amount").alias("revenue"),
        count("*").alias("orders")
    ) \
    .orderBy("order_year", "order_month")

monthly_stats.show()

# Write results back to Delta Lake for reporting
monthly_stats.write \
    .format("delta") \
    .mode("overwrite") \
    .save("abfss://curated@datalake.dfs.core.windows.net/cosmos_reports/monthly_revenue")
```

---

## Change Feed Processing

### Reading the Change Feed

**Use Case**: React to data changes in Cosmos DB in near-real-time. Useful for materializing views, triggering downstream pipelines, or syncing data to other systems.

```python
"""
Process the Cosmos DB change feed to react to inserts and updates.
The change feed provides an ordered log of changes per partition key.
"""

import json
import time
from azure.cosmos import CosmosClient

client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
container = client.get_database_client(DATABASE_NAME).get_container_client("orders")


def process_changes(changes: list):
    """Handle a batch of changed documents."""
    for doc in changes:
        doc_id = doc["id"]
        status = doc.get("status", "unknown")
        print(f"  Change detected: order {doc_id} -> status={status}")

        # Example downstream actions:
        # - Update a materialized view
        # - Send a notification
        # - Write to an event stream


def read_change_feed():
    """
    Read the change feed from the beginning. In production, persist
    the continuation token to resume from the last processed position.
    """
    # Start from the beginning of the change feed
    change_feed = container.query_items_change_feed(
        is_start_from_beginning=True,
        partition_key_range_id="0"  # Process one partition range
    )

    continuation_token = None

    while True:
        response = list(change_feed)

        if response:
            print(f"Processing {len(response)} changes...")
            process_changes(response)

        # Get the continuation token for checkpointing
        continuation_token = change_feed.continuation_token
        print(f"Continuation token saved. Waiting for new changes...")

        time.sleep(5)  # Poll interval

        # Resume from the last position
        change_feed = container.query_items_change_feed(
            continuation=continuation_token,
            partition_key_range_id="0"
        )


if __name__ == "__main__":
    read_change_feed()
```

**Expected Output**:

```text
Processing 3 changes...
  Change detected: order abc-123 -> status=pending
  Change detected: order def-456 -> status=shipped
  Change detected: order ghi-789 -> status=delivered
Continuation token saved. Waiting for new changes...
```

---

## Partition Key Strategy

### Choosing and Validating a Partition Key

**Use Case**: Select a partition key that distributes data evenly and matches your most common query patterns to minimize RU consumption.

```python
"""
Analyze partition key distribution to ensure even data spread.
Hot partitions lead to throttling and wasted throughput.
"""

container = database.get_container_client("orders")

# Check partition key distribution using a cross-partition query
distribution_query = """
    SELECT
        c.customer_id AS partition_key,
        COUNT(1) AS doc_count
    FROM c
    GROUP BY c.customer_id
"""

results = list(container.query_items(
    query=distribution_query,
    enable_cross_partition_query=True
))

# Analyze the distribution
doc_counts = [r["doc_count"] for r in results]
total_docs = sum(doc_counts)
num_partitions = len(doc_counts)
max_count = max(doc_counts) if doc_counts else 0
avg_count = total_docs / num_partitions if num_partitions else 0
skew_ratio = max_count / avg_count if avg_count else 0

print(f"Total documents:       {total_docs}")
print(f"Logical partitions:    {num_partitions}")
print(f"Avg docs per partition: {avg_count:.1f}")
print(f"Max docs in partition:  {max_count}")
print(f"Skew ratio:            {skew_ratio:.2f}x")

if skew_ratio > 5:
    print("WARNING: High partition skew detected. Consider a different partition key.")
elif skew_ratio > 2:
    print("NOTICE: Moderate skew. Monitor for hot partition throttling.")
else:
    print("OK: Partition distribution looks healthy.")
```

### Hierarchical Partition Keys

**Use Case**: Use a hierarchical (sub-partitioned) key for multi-tenant scenarios where a single tenant could hold too much data for one logical partition.

```python
# Hierarchical partition keys allow splitting a logical partition
# across multiple physical partitions.

# Example: partition by tenant, then by region
container = database.create_container_if_not_exists(
    id="multi_tenant_orders",
    partition_key=PartitionKey(
        path=["/tenant_id", "/region"],
        kind="MultiHash"
    ),
    offer_throughput=4000
)

# Insert a document with the hierarchical key
order = {
    "id": "order-5001",
    "tenant_id": "tenant-acme",
    "region": "westus",
    "total_amount": 250.00,
    "status": "shipped"
}

container.create_item(body=order)

# Query scoped to a single sub-partition (most efficient)
results = list(container.query_items(
    query="SELECT * FROM c WHERE c.status = 'shipped'",
    partition_key=["tenant-acme", "westus"]
))
print(f"Found {len(results)} shipped orders for tenant-acme in westus")
```

---

## Cost Optimization Patterns

### Reducing RU Consumption

**Use Case**: Write queries that minimize Request Unit cost for common access patterns.

```python
"""
Patterns that reduce RU consumption and lower Cosmos DB costs.
"""

container = database.get_container_client("orders")

# 1. Point reads instead of queries (1 RU for a 1KB doc)
# BEST: direct point read by id + partition key
item = container.read_item(item="order-5001", partition_key="cust-1001")

# 2. Project only the fields you need (reduces RU and bandwidth)
query = "SELECT c.id, c.status, c.total_amount FROM c WHERE c.customer_id = @cid"
results = list(container.query_items(
    query=query,
    parameters=[{"name": "@cid", "value": "cust-1001"}],
    partition_key="cust-1001"
))

# 3. Use OFFSET/LIMIT for pagination instead of fetching all results
page_query = """
    SELECT c.id, c.order_date, c.total_amount
    FROM c
    WHERE c.customer_id = @cid
    ORDER BY c.order_date DESC
    OFFSET 0 LIMIT 20
"""
page = list(container.query_items(
    query=page_query,
    parameters=[{"name": "@cid", "value": "cust-1001"}],
    partition_key="cust-1001"
))

# 4. Exclude large fields from the indexing policy to save write RUs
# (configured at container creation, see indexing_policy above)

# 5. Use patch instead of replace for partial updates (lower RU)
container.patch_item(
    item="order-5001",
    partition_key="cust-1001",
    patch_operations=[
        {"op": "set", "path": "/status", "value": "delivered"}
    ]
)

# 6. Use autoscale throughput for unpredictable workloads
# (configured at container creation)
# container = database.create_container_if_not_exists(
#     id="orders_autoscale",
#     partition_key=PartitionKey(path="/customer_id"),
#     offer_throughput=None,
#     auto_scale_max_throughput=4000  # Scales between 400-4000 RU/s
# )
```

### Monitoring RU Consumption

**Use Case**: Track the RU cost of each operation to identify expensive queries.

```python
"""
Log the RU charge of every query to find optimization opportunities.
"""

query = "SELECT * FROM c WHERE c.region = 'westus' AND c.status = 'pending'"

# Use the response headers to get the RU charge
items = container.query_items(
    query=query,
    enable_cross_partition_query=True
)

total_ru = 0.0
item_count = 0

for item in items:
    item_count += 1

# Access the request charge from the last page header
# For a more accurate total, use the feed response directly:
query_iterable = container.query_items(
    query=query,
    enable_cross_partition_query=True,
    populate_query_metrics=True
)

results = []
for page in query_iterable.by_page():
    page_items = list(page)
    results.extend(page_items)
    ru_charge = query_iterable.get_response_headers().get("x-ms-request-charge", 0)
    total_ru += float(ru_charge)

print(f"Query returned {len(results)} items")
print(f"Total RU charge: {total_ru:.2f} RUs")
print(f"Avg RU per item: {total_ru / len(results):.2f} RUs" if results else "No results")
```

---

## Best Practices

1. **Use point reads** (`read_item`) whenever you have the id and partition key. They cost 1 RU per 1KB item and are the cheapest operation available.
2. **Scope queries to a single partition** by always including the partition key in WHERE clauses to avoid fan-out queries.
3. **Enable Synapse Link** and use the analytical store for reporting and aggregation queries so you never impact transactional throughput.
4. **Use patch operations** instead of full replace for partial updates to reduce RU cost and avoid race conditions.
5. **Project only needed fields** in SELECT clauses to reduce both RU cost and network transfer.
6. **Design your partition key** around your most common query filter and ensure even data distribution.
7. **Use autoscale throughput** for workloads with variable traffic to avoid over-provisioning.
8. **Monitor with Azure Monitor** and set alerts on normalized RU consumption exceeding 70% to prevent throttling.

---

*Last Updated: 2026-04-07*
*Version: 1.0.0*
