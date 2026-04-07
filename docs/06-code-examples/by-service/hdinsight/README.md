# Azure HDInsight Code Examples

> **[Home](../../../README.md)** | **[Code Examples](../../README.md)** | **HDInsight**

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Languages](https://img.shields.io/badge/Languages-Python%20%7C%20HiveQL%20%7C%20Shell-blue)
![Complexity](https://img.shields.io/badge/Complexity-Beginner_to_Advanced-orange)

Practical code examples for Azure HDInsight covering Spark job submission, Hive queries, Kafka producer/consumer patterns, and HBase shell operations.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Spark Job Submission](#spark-job-submission)
- [Hive Query Examples](#hive-query-examples)
- [Kafka Producer and Consumer](#kafka-producer-and-consumer)
- [HBase Shell Examples](#hbase-shell-examples)
- [Best Practices](#best-practices)

---

## Prerequisites

### Azure Resources

- Azure HDInsight cluster (Spark, Hadoop, Kafka, or HBase type depending on the example)
- Azure Data Lake Storage Gen2 or Azure Blob Storage as the default cluster storage
- Virtual network with NSG rules allowing cluster communication

### Development Environment

```bash
# Python libraries for Spark and Kafka examples
pip install requests>=2.28.0
pip install confluent-kafka>=2.3.0
pip install azure-identity>=1.12.0

# Hive CLI or Beeline (bundled with HDInsight SSH access)
# HBase shell (available via SSH on HBase clusters)
```

### Cluster Access

```bash
# SSH into the head node (replace with your cluster name)
ssh sshuser@mycluster-ssh.azurehdinsight.net

# Ambari dashboard (management UI)
# https://mycluster.azurehdinsight.net
```

---

## Spark Job Submission

### Using spark-submit via SSH

**Use Case**: Submit a PySpark application to the cluster from the head node.

```bash
# SSH into the head node first, then run:

# Submit a simple PySpark script
spark-submit \
    --master yarn \
    --deploy-mode cluster \
    --num-executors 4 \
    --executor-memory 4g \
    --executor-cores 2 \
    --conf spark.sql.adaptive.enabled=true \
    --conf spark.sql.shuffle.partitions=200 \
    wasbs://scripts@csadatalake.blob.core.windows.net/etl/daily_transform.py \
    --input-path wasbs://raw@csadatalake.blob.core.windows.net/sales/2024/ \
    --output-path wasbs://curated@csadatalake.blob.core.windows.net/sales_processed/

# Submit a Scala JAR application
spark-submit \
    --master yarn \
    --deploy-mode cluster \
    --class com.contoso.analytics.DailyAggregation \
    --num-executors 8 \
    --executor-memory 8g \
    --jars wasbs://libs@csadatalake.blob.core.windows.net/dependencies.jar \
    wasbs://jars@csadatalake.blob.core.windows.net/analytics-app-1.0.jar
```

### Submitting Jobs via Livy REST API

**Use Case**: Submit and monitor Spark jobs remotely without SSH access. The Livy API is useful for CI/CD pipelines and application integrations.

```python
"""
Submit and monitor a PySpark job through the HDInsight Livy REST API.
Livy provides a REST interface for interacting with Spark clusters.
"""

import requests
import time
import json

CLUSTER_NAME = "mycluster"
LIVY_URL = f"https://{CLUSTER_NAME}.azurehdinsight.net/livy/batches"
USERNAME = "admin"
PASSWORD = "your-cluster-password"  # Use Key Vault in production

HEADERS = {"Content-Type": "application/json"}


def submit_spark_job(script_path: str, args: list = None) -> int:
    """Submit a PySpark job and return the batch ID."""
    payload = {
        "file": script_path,
        "name": "daily-etl-job",
        "numExecutors": 4,
        "executorMemory": "4g",
        "executorCores": 2,
        "driverMemory": "2g",
        "conf": {
            "spark.sql.adaptive.enabled": "true"
        }
    }
    if args:
        payload["args"] = args

    response = requests.post(
        LIVY_URL,
        headers=HEADERS,
        auth=(USERNAME, PASSWORD),
        data=json.dumps(payload),
        verify=True
    )
    response.raise_for_status()

    batch_id = response.json()["id"]
    print(f"Job submitted. Batch ID: {batch_id}")
    return batch_id


def poll_job_status(batch_id: int, timeout_seconds: int = 1800) -> str:
    """Poll the job status until it completes or times out."""
    url = f"{LIVY_URL}/{batch_id}"
    start_time = time.time()

    while True:
        response = requests.get(url, auth=(USERNAME, PASSWORD), verify=True)
        response.raise_for_status()
        state = response.json()["state"]

        print(f"  Batch {batch_id} state: {state}")

        if state in ("success", "dead", "killed"):
            return state

        if time.time() - start_time > timeout_seconds:
            print("Job timed out.")
            return "timeout"

        time.sleep(15)


def get_job_log(batch_id: int) -> str:
    """Retrieve the job log for debugging."""
    url = f"{LIVY_URL}/{batch_id}/log"
    response = requests.get(url, auth=(USERNAME, PASSWORD), verify=True)
    response.raise_for_status()
    return "\n".join(response.json().get("log", []))


# --- Run the workflow ---
if __name__ == "__main__":
    script = "wasbs://scripts@csadatalake.blob.core.windows.net/etl/daily_transform.py"
    batch_id = submit_spark_job(script, args=["--date", "2024-06-15"])
    final_state = poll_job_status(batch_id)

    if final_state != "success":
        print("Job failed. Retrieving logs...")
        print(get_job_log(batch_id))
    else:
        print("Job completed successfully.")
```

**Expected Output**:

```text
Job submitted. Batch ID: 42
  Batch 42 state: starting
  Batch 42 state: running
  Batch 42 state: running
  Batch 42 state: success
Job completed successfully.
```

---

## Hive Query Examples

### Creating External Tables on ADLS

**Use Case**: Define external Hive tables that point to data stored in Azure Data Lake Storage so analysts can query files with SQL.

```sql
-- Connect via Beeline from the head node:
-- beeline -u "jdbc:hive2://headnodehost:10001/default;transportMode=http"

-- Create a database for the analytics domain
CREATE DATABASE IF NOT EXISTS sales_analytics
COMMENT 'Sales analytics domain'
LOCATION 'wasbs://curated@csadatalake.blob.core.windows.net/hive/sales_analytics';

USE sales_analytics;

-- External table over CSV files
CREATE EXTERNAL TABLE IF NOT EXISTS raw_orders (
    order_id       STRING,
    customer_id    STRING,
    order_date     STRING,
    product_id     STRING,
    quantity       INT,
    unit_price     DECIMAL(10,2),
    order_status   STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 'wasbs://raw@csadatalake.blob.core.windows.net/sales/orders/'
TBLPROPERTIES ('skip.header.line.count'='1');

-- Verify the table
SELECT COUNT(*) FROM raw_orders;
```

### Partitioned Tables with ORC/Parquet

**Use Case**: Create partitioned tables in columnar formats for efficient analytical queries.

```sql
-- Partitioned table stored as ORC (good compression, fast reads)
CREATE EXTERNAL TABLE IF NOT EXISTS orders_by_month (
    order_id       STRING,
    customer_id    STRING,
    order_date     DATE,
    product_id     STRING,
    quantity       INT,
    unit_price     DECIMAL(10,2),
    total_amount   DECIMAL(12,2),
    order_status   STRING
)
PARTITIONED BY (order_year INT, order_month INT)
STORED AS ORC
LOCATION 'wasbs://curated@csadatalake.blob.core.windows.net/hive/orders_orc/'
TBLPROPERTIES ('orc.compress'='SNAPPY');

-- Enable dynamic partitioning to auto-create partitions on insert
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

-- Populate the partitioned table from the raw table
INSERT OVERWRITE TABLE orders_by_month
PARTITION (order_year, order_month)
SELECT
    order_id,
    customer_id,
    CAST(order_date AS DATE),
    product_id,
    quantity,
    unit_price,
    quantity * unit_price AS total_amount,
    order_status,
    YEAR(order_date)  AS order_year,
    MONTH(order_date) AS order_month
FROM raw_orders
WHERE order_status IN ('completed', 'shipped');

-- Query with partition pruning (only scans the requested partition)
SELECT
    product_id,
    SUM(total_amount) AS product_revenue,
    SUM(quantity)      AS units_sold
FROM orders_by_month
WHERE order_year = 2024 AND order_month = 6
GROUP BY product_id
ORDER BY product_revenue DESC
LIMIT 20;

-- Parquet variant (preferred for Spark interoperability)
CREATE EXTERNAL TABLE IF NOT EXISTS orders_parquet (
    order_id       STRING,
    customer_id    STRING,
    order_date     DATE,
    total_amount   DECIMAL(12,2),
    order_status   STRING
)
PARTITIONED BY (region STRING)
STORED AS PARQUET
LOCATION 'wasbs://curated@csadatalake.blob.core.windows.net/hive/orders_parquet/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');
```

---

## Kafka Producer and Consumer

### Python Producer with confluent-kafka

**Use Case**: Publish messages to a Kafka topic running on an HDInsight Kafka cluster.

```python
"""
Kafka producer for HDInsight Kafka clusters.
Uses the confluent-kafka Python client which wraps librdkafka for high throughput.
"""

import json
import time
from confluent_kafka import Producer

# HDInsight Kafka broker list (get from Ambari or cluster properties)
KAFKA_BROKERS = "wn0-mykafka:9092,wn1-mykafka:9092,wn2-mykafka:9092"
TOPIC = "sensor-telemetry"


def delivery_report(err, msg):
    """Callback invoked once per message to report delivery result."""
    if err is not None:
        print(f"  FAILED: {err}")
    else:
        print(f"  Delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")


def create_producer() -> Producer:
    """Create a Kafka producer with recommended settings."""
    config = {
        "bootstrap.servers": KAFKA_BROKERS,
        "client.id": "sensor-producer-01",
        "acks": "all",               # Wait for all replicas
        "retries": 5,
        "retry.backoff.ms": 500,
        "linger.ms": 10,             # Small batch delay for throughput
        "batch.size": 65536,         # 64 KB batches
        "compression.type": "snappy"
    }
    return Producer(config)


def produce_sensor_events(producer: Producer, count: int = 100):
    """Generate and send sensor telemetry events."""
    for i in range(count):
        event = {
            "sensor_id": f"sensor-{i % 10:03d}",
            "temperature": 68.0 + (i % 30) * 0.5,
            "humidity": 40.0 + (i % 20),
            "timestamp": time.time()
        }

        # Use sensor_id as the key for partition affinity
        producer.produce(
            topic=TOPIC,
            key=event["sensor_id"],
            value=json.dumps(event),
            callback=delivery_report
        )

        # Trigger delivery reports periodically
        if i % 50 == 0:
            producer.poll(0)

    # Flush remaining messages
    remaining = producer.flush(timeout=30)
    print(f"Flush complete. {remaining} messages still in queue.")


if __name__ == "__main__":
    producer = create_producer()
    produce_sensor_events(producer, count=200)
    print("All events produced.")
```

### Python Consumer with confluent-kafka

**Use Case**: Consume and process messages from a Kafka topic with consumer group management.

```python
"""
Kafka consumer for HDInsight Kafka clusters.
Demonstrates consumer group management, offset commits, and graceful shutdown.
"""

import json
import signal
import sys
from confluent_kafka import Consumer, KafkaError, KafkaException

KAFKA_BROKERS = "wn0-mykafka:9092,wn1-mykafka:9092,wn2-mykafka:9092"
TOPIC = "sensor-telemetry"
GROUP_ID = "telemetry-processor-group"

running = True


def signal_handler(sig, frame):
    """Handle Ctrl+C for graceful shutdown."""
    global running
    print("\nShutdown requested...")
    running = False


signal.signal(signal.SIGINT, signal_handler)


def create_consumer() -> Consumer:
    """Create a Kafka consumer with recommended settings."""
    config = {
        "bootstrap.servers": KAFKA_BROKERS,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,     # Manual commit for at-least-once
        "max.poll.interval.ms": 300000,
        "session.timeout.ms": 45000
    }
    return Consumer(config)


def process_message(msg_value: dict):
    """Process a single sensor telemetry message."""
    sensor_id = msg_value.get("sensor_id", "unknown")
    temperature = msg_value.get("temperature", 0)

    # Example: alert on high temperature
    if temperature > 80.0:
        print(f"  ALERT: {sensor_id} temperature {temperature}F exceeds threshold")

    return True


def consume_loop():
    """Main consumer loop with manual offset commits."""
    consumer = create_consumer()
    consumer.subscribe([TOPIC])

    msg_count = 0

    try:
        while running:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"  Reached end of partition {msg.partition()}")
                    continue
                raise KafkaException(msg.error())

            # Deserialize and process
            value = json.loads(msg.value().decode("utf-8"))
            process_message(value)
            msg_count += 1

            # Commit offsets every 100 messages
            if msg_count % 100 == 0:
                consumer.commit(asynchronous=False)
                print(f"Committed offsets at message count {msg_count}")

    finally:
        # Commit final offsets and leave the consumer group cleanly
        consumer.commit(asynchronous=False)
        consumer.close()
        print(f"Consumer closed. Processed {msg_count} messages total.")


if __name__ == "__main__":
    consume_loop()
```

**Expected Output**:

```text
  ALERT: sensor-005 temperature 82.0F exceeds threshold
Committed offsets at message count 100
  ALERT: sensor-005 temperature 82.0F exceeds threshold
Committed offsets at message count 200
^C
Shutdown requested...
Consumer closed. Processed 213 messages total.
```

---

## HBase Shell Examples

### Table Operations

**Use Case**: Create tables, insert data, and run scans from the HBase shell on an HDInsight HBase cluster.

```bash
# SSH into the cluster, then start the HBase shell:
# hbase shell

# --- Create a table with two column families ---
create 'sensor_readings', \
  {NAME => 'data', VERSIONS => 3, COMPRESSION => 'SNAPPY', TTL => 7776000}, \
  {NAME => 'meta', VERSIONS => 1}

# TTL of 7776000 seconds = 90 days (data auto-expires)

# --- Insert rows (put) ---
# Row key format: <sensor_id>#<reverse_timestamp> for range scans by time
put 'sensor_readings', 'sensor-001#9999999999', 'data:temperature', '72.5'
put 'sensor_readings', 'sensor-001#9999999999', 'data:humidity', '45.2'
put 'sensor_readings', 'sensor-001#9999999999', 'meta:location', 'building-a'

put 'sensor_readings', 'sensor-001#9999999998', 'data:temperature', '73.1'
put 'sensor_readings', 'sensor-001#9999999998', 'data:humidity', '44.8'

put 'sensor_readings', 'sensor-002#9999999999', 'data:temperature', '68.3'
put 'sensor_readings', 'sensor-002#9999999999', 'meta:location', 'building-b'

# --- Get a single row ---
get 'sensor_readings', 'sensor-001#9999999999'

# --- Scan a range of rows ---
# All readings for sensor-001
scan 'sensor_readings', {STARTROW => 'sensor-001#', STOPROW => 'sensor-001~'}

# Scan with a filter (only rows where temperature > 70)
scan 'sensor_readings', {
  FILTER => "SingleColumnValueFilter('data', 'temperature', >, 'binary:70.0')"
}

# Count rows in the table
count 'sensor_readings'

# --- Table management ---
# Disable before altering or dropping
disable 'sensor_readings'

# Add a new column family
alter 'sensor_readings', {NAME => 'alerts', VERSIONS => 1}

# Re-enable
enable 'sensor_readings'

# Drop a table (must be disabled first)
# disable 'sensor_readings'
# drop 'sensor_readings'

# List all tables
list
```

---

## Best Practices

1. **Use Livy for remote job submission** instead of SSH-based spark-submit in automated pipelines
2. **Store credentials in Azure Key Vault** and retrieve them at runtime rather than embedding in scripts
3. **Use ORC or Parquet** for Hive tables to reduce storage costs and improve query performance
4. **Enable dynamic partitioning** in Hive for automatic partition management during inserts
5. **Set `acks=all`** on Kafka producers for durability and configure idempotence for exactly-once semantics
6. **Use manual offset commits** in Kafka consumers for at-least-once processing guarantees
7. **Design HBase row keys** for your access pattern (avoid hotspotting by salting or reversing timestamps)
8. **Monitor cluster health** through Ambari and set up Azure Monitor alerts for resource utilization

---

*Last Updated: 2026-04-07*
*Version: 1.0.0*
