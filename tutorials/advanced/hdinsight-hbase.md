# Apache HBase on HDInsight

> **[Home](../../README.md)** | **[Tutorials](../README.md)** | **HDInsight HBase**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Level](https://img.shields.io/badge/Level-Advanced-red?style=flat-square)

Comprehensive guide to Apache HBase on Azure HDInsight.

---

## Overview

This tutorial covers:

- HBase cluster deployment
- Table design and schema patterns
- Read/write optimization
- Integration with analytics pipelines

**Duration**: 3 hours | **Prerequisites**: NoSQL concepts, Azure networking

---

## Cluster Deployment

### Create HBase Cluster

```bash
# Create HDInsight HBase cluster
az hdinsight create \
    --name hbase-cluster \
    --resource-group rg-hbase \
    --type hbase \
    --version 4.0 \
    --component-version HBase=2.1 \
    --headnode-size Standard_D12_v2 \
    --workernode-size Standard_D12_v2 \
    --workernode-count 4 \
    --zookeepernode-size Standard_D3_v2 \
    --storage-account storageaccount \
    --storage-container hbase-data \
    --ssh-user admin \
    --ssh-password 'SecurePassword123!'
```

### Configuration Optimization

```xml
<!-- hbase-site.xml -->
<configuration>
    <property>
        <name>hbase.regionserver.handler.count</name>
        <value>100</value>
    </property>
    <property>
        <name>hbase.hregion.memstore.flush.size</name>
        <value>134217728</value> <!-- 128MB -->
    </property>
    <property>
        <name>hbase.hregion.max.filesize</name>
        <value>10737418240</value> <!-- 10GB -->
    </property>
    <property>
        <name>hbase.client.scanner.caching</name>
        <value>1000</value>
    </property>
</configuration>
```

---

## Table Design

### Schema Design Patterns

```java
// Create table with column families
Configuration config = HBaseConfiguration.create();
Connection connection = ConnectionFactory.createConnection(config);
Admin admin = connection.getAdmin();

// Table: user_activity
// Row key: user_id_reverse_timestamp (for time-series queries)
TableDescriptorBuilder tableBuilder = TableDescriptorBuilder.newBuilder(
    TableName.valueOf("user_activity")
);

// Column family for profile data (small, frequently updated)
ColumnFamilyDescriptor profileFamily = ColumnFamilyDescriptorBuilder
    .newBuilder(Bytes.toBytes("profile"))
    .setMaxVersions(1)
    .setCompressionType(Compression.Algorithm.SNAPPY)
    .setBloomFilterType(BloomType.ROW)
    .build();

// Column family for activity data (large, append-only)
ColumnFamilyDescriptor activityFamily = ColumnFamilyDescriptorBuilder
    .newBuilder(Bytes.toBytes("activity"))
    .setMaxVersions(5)
    .setTimeToLive(365 * 24 * 60 * 60) // 1 year TTL
    .setCompressionType(Compression.Algorithm.SNAPPY)
    .setBloomFilterType(BloomType.ROWCOL)
    .build();

tableBuilder.setColumnFamily(profileFamily);
tableBuilder.setColumnFamily(activityFamily);

// Pre-split for even distribution
byte[][] splitKeys = new byte[][] {
    Bytes.toBytes("2"),
    Bytes.toBytes("4"),
    Bytes.toBytes("6"),
    Bytes.toBytes("8"),
    Bytes.toBytes("a"),
    Bytes.toBytes("c"),
    Bytes.toBytes("e")
};

admin.createTable(tableBuilder.build(), splitKeys);
```

### Row Key Design

```python
# Good row key design for time-series data
def create_row_key(user_id: str, timestamp: int) -> bytes:
    """Create row key with reverse timestamp for latest-first ordering."""

    # Reverse timestamp (max - actual) for descending order
    reverse_ts = 9999999999999 - timestamp

    # Salt prefix for distribution (hash of user_id % num_regions)
    salt = hash(user_id) % 16

    # Format: salt_user_reverse_timestamp
    row_key = f"{salt:02d}_{user_id}_{reverse_ts:013d}"

    return row_key.encode('utf-8')

# Example
row_key = create_row_key("user123", 1705312800000)
# Result: "07_user123_8294687199999"
```

---

## Read/Write Operations

### Python Client (happybase)

```python
import happybase

# Connect to HBase
connection = happybase.Connection(
    host='hbase-cluster.azurehdinsight.net',
    port=9090,
    transport='framed',
    protocol='compact'
)

table = connection.table('user_activity')

# Write data
def write_activity(user_id: str, timestamp: int, activity: dict):
    row_key = create_row_key(user_id, timestamp)

    # Prepare data for column families
    data = {
        b'profile:name': activity.get('name', '').encode(),
        b'activity:type': activity['type'].encode(),
        b'activity:value': str(activity['value']).encode(),
        b'activity:metadata': json.dumps(activity.get('metadata', {})).encode()
    }

    table.put(row_key, data)

# Batch write
def batch_write(activities: list):
    with table.batch(batch_size=1000) as batch:
        for activity in activities:
            row_key = create_row_key(activity['user_id'], activity['timestamp'])
            data = {
                b'activity:type': activity['type'].encode(),
                b'activity:value': str(activity['value']).encode()
            }
            batch.put(row_key, data)

# Read latest activities for user
def get_user_activities(user_id: str, limit: int = 100):
    # Calculate row key prefix for scan
    salt = hash(user_id) % 16
    prefix = f"{salt:02d}_{user_id}_".encode()

    activities = []
    for key, data in table.scan(row_prefix=prefix, limit=limit):
        activities.append({
            'row_key': key.decode(),
            'type': data.get(b'activity:type', b'').decode(),
            'value': data.get(b'activity:value', b'').decode()
        })

    return activities
```

### Java Client

```java
// High-performance reads with async operations
AsyncConnection asyncConnection = ConnectionFactory.createAsyncConnection(config).get();
AsyncTable<AdvancedScanResultConsumer> table = asyncConnection.getTable(
    TableName.valueOf("user_activity")
);

// Async get
CompletableFuture<Result> future = table.get(new Get(rowKey));
future.thenAccept(result -> {
    byte[] value = result.getValue(Bytes.toBytes("activity"), Bytes.toBytes("type"));
    System.out.println("Activity type: " + Bytes.toString(value));
});

// Batch gets
List<Get> gets = userIds.stream()
    .map(id -> new Get(createRowKey(id, timestamp)))
    .collect(Collectors.toList());

List<CompletableFuture<Result>> futures = table.get(gets);
CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
```

---

## Integration with Spark

### Read HBase from Spark

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("HBaseReader") \
    .config("spark.hbase.host", "zookeeper:2181") \
    .getOrCreate()

# Using Spark HBase Connector
hbase_df = spark.read \
    .format("org.apache.hadoop.hbase.spark") \
    .option("hbase.table", "user_activity") \
    .option("hbase.columns.mapping", """
        row_key STRING :key,
        activity_type STRING activity:type,
        activity_value STRING activity:value
    """) \
    .load()

# Process and aggregate
daily_summary = hbase_df \
    .withColumn("date", extract_date_from_rowkey(col("row_key"))) \
    .groupBy("date", "activity_type") \
    .count()

# Write back to HBase
daily_summary.write \
    .format("org.apache.hadoop.hbase.spark") \
    .option("hbase.table", "activity_summary") \
    .option("hbase.columns.mapping", """
        key STRING :key,
        activity_type STRING cf:type,
        count LONG cf:count
    """) \
    .save()
```

---

## Monitoring

### Key Metrics

| Metric | Healthy Range | Action |
|--------|---------------|--------|
| RegionServer heap usage | < 80% | Increase heap or add nodes |
| Store file count | < 10 per region | Run major compaction |
| Read/Write latency | < 100ms | Optimize schema or add cache |
| Region count per server | 20-200 | Split/merge regions |

### HBase Shell Commands

```bash
# Check cluster status
hbase shell
> status 'detailed'

# Check table regions
> list_regions 'user_activity'

# Major compaction
> major_compact 'user_activity'

# Check region load
> hbase hbck -details
```

---

## Related Documentation

- [HDInsight Overview](../../docs/02-services/analytics-compute/azure-hdinsight/README.md)
- [NoSQL Patterns](../../docs/03-architecture-patterns/README.md)
- [Hadoop Migration](hadoop-migration-workshop.md)

---

*Last Updated: January 2025*
