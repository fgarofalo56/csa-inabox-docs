# Apache Kafka on HDInsight

> **[Home](../../README.md)** | **[Tutorials](../README.md)** | **HDInsight Kafka**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Level](https://img.shields.io/badge/Level-Advanced-red?style=flat-square)

Comprehensive guide to Apache Kafka on Azure HDInsight.

---

## Overview

This tutorial covers:

- HDInsight Kafka cluster deployment
- Topic management and configuration
- Producer and consumer patterns
- Integration with analytics services

**Duration**: 3 hours | **Prerequisites**: Messaging concepts, Azure networking

---

## Cluster Deployment

### Create HDInsight Kafka Cluster

```bash
# Create resource group
az group create --name rg-kafka --location eastus

# Create virtual network
az network vnet create \
    --name vnet-kafka \
    --resource-group rg-kafka \
    --address-prefix 10.0.0.0/16 \
    --subnet-name subnet-kafka \
    --subnet-prefix 10.0.0.0/24

# Create HDInsight Kafka cluster
az hdinsight create \
    --name kafka-cluster \
    --resource-group rg-kafka \
    --type kafka \
    --version 2.4 \
    --component-version Kafka=2.4 \
    --headnode-size Standard_E4_v3 \
    --workernode-size Standard_E4_v3 \
    --workernode-count 4 \
    --zookeepernode-size Standard_A4_v2 \
    --ssh-user admin \
    --ssh-password 'SecurePassword123!' \
    --storage-account storageaccount \
    --storage-container kafka-data \
    --vnet-name vnet-kafka \
    --subnet subnet-kafka
```

### Cluster Configuration

```json
{
    "kafka-broker": {
        "auto.create.topics.enable": "false",
        "delete.topic.enable": "true",
        "log.retention.hours": "168",
        "log.segment.bytes": "1073741824",
        "num.partitions": "8",
        "default.replication.factor": "3",
        "min.insync.replicas": "2",
        "compression.type": "lz4"
    }
}
```

---

## Topic Management

### Create Topics

```bash
# Get Zookeeper hosts
export KAFKAZKHOSTS=$(curl -sS -u admin:password -G \
    "https://kafka-cluster.azurehdinsight.net/api/v1/clusters/kafka-cluster/services/ZOOKEEPER/components/ZOOKEEPER_SERVER" \
    | jq -r '[.host_components[].HostRoles.host_name + ":2181"] | join(",")')

# Create topic
/usr/hdp/current/kafka-broker/bin/kafka-topics.sh \
    --create \
    --zookeeper $KAFKAZKHOSTS \
    --topic events \
    --partitions 8 \
    --replication-factor 3 \
    --config retention.ms=604800000 \
    --config segment.bytes=1073741824

# List topics
/usr/hdp/current/kafka-broker/bin/kafka-topics.sh \
    --list \
    --zookeeper $KAFKAZKHOSTS

# Describe topic
/usr/hdp/current/kafka-broker/bin/kafka-topics.sh \
    --describe \
    --zookeeper $KAFKAZKHOSTS \
    --topic events
```

### Topic Configuration

```bash
# Alter topic configuration
/usr/hdp/current/kafka-broker/bin/kafka-configs.sh \
    --zookeeper $KAFKAZKHOSTS \
    --entity-type topics \
    --entity-name events \
    --alter \
    --add-config retention.ms=259200000

# Increase partitions
/usr/hdp/current/kafka-broker/bin/kafka-topics.sh \
    --alter \
    --zookeeper $KAFKAZKHOSTS \
    --topic events \
    --partitions 16
```

---

## Producer Patterns

### Python Producer

```python
from confluent_kafka import Producer
import json

def delivery_report(err, msg):
    """Delivery callback."""
    if err:
        print(f'Delivery failed: {err}')
    else:
        print(f'Delivered to {msg.topic()} [{msg.partition()}]')

# Configure producer
config = {
    'bootstrap.servers': 'wn0-kafka:9092,wn1-kafka:9092',
    'acks': 'all',
    'retries': 3,
    'compression.type': 'lz4',
    'batch.size': 65536,
    'linger.ms': 10
}

producer = Producer(config)

# Send events
def send_events(events):
    for event in events:
        producer.produce(
            topic='events',
            key=event['id'].encode('utf-8'),
            value=json.dumps(event).encode('utf-8'),
            callback=delivery_report
        )

    producer.flush()

# Example usage
events = [
    {'id': '1', 'type': 'click', 'timestamp': '2025-01-15T10:00:00Z'},
    {'id': '2', 'type': 'purchase', 'timestamp': '2025-01-15T10:01:00Z'}
]
send_events(events)
```

### Java Producer with Schema Registry

```java
import org.apache.kafka.clients.producer.*;
import io.confluent.kafka.serializers.KafkaAvroSerializer;

Properties props = new Properties();
props.put("bootstrap.servers", "wn0-kafka:9092,wn1-kafka:9092");
props.put("key.serializer", StringSerializer.class.getName());
props.put("value.serializer", KafkaAvroSerializer.class.getName());
props.put("schema.registry.url", "http://schema-registry:8081");
props.put("acks", "all");

Producer<String, GenericRecord> producer = new KafkaProducer<>(props);

// Create Avro record
Schema schema = new Schema.Parser().parse(schemaString);
GenericRecord record = new GenericData.Record(schema);
record.put("id", "123");
record.put("type", "click");
record.put("timestamp", System.currentTimeMillis());

ProducerRecord<String, GenericRecord> producerRecord =
    new ProducerRecord<>("events", record.get("id").toString(), record);

producer.send(producerRecord, (metadata, exception) -> {
    if (exception != null) {
        exception.printStackTrace();
    } else {
        System.out.printf("Sent to partition %d, offset %d%n",
            metadata.partition(), metadata.offset());
    }
});
```

---

## Consumer Patterns

### Python Consumer

```python
from confluent_kafka import Consumer, KafkaError
import json

config = {
    'bootstrap.servers': 'wn0-kafka:9092,wn1-kafka:9092',
    'group.id': 'analytics-consumer',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
}

consumer = Consumer(config)
consumer.subscribe(['events'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f'Error: {msg.error()}')
                break

        # Process message
        event = json.loads(msg.value().decode('utf-8'))
        process_event(event)

        # Manual commit after processing
        consumer.commit(asynchronous=False)

finally:
    consumer.close()
```

---

## Integration with Analytics

### Spark Streaming from Kafka

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("KafkaStreaming") \
    .getOrCreate()

# Read from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "wn0-kafka:9092,wn1-kafka:9092") \
    .option("subscribe", "events") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse JSON
event_schema = StructType([
    StructField("id", StringType()),
    StructField("type", StringType()),
    StructField("timestamp", TimestampType())
])

events_df = kafka_df \
    .select(from_json(col("value").cast("string"), event_schema).alias("data")) \
    .select("data.*")

# Write to Delta Lake
events_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/checkpoints/kafka-events") \
    .start("/delta/events")
```

---

## Monitoring

### Consumer Lag Monitoring

```bash
# Check consumer group lag
/usr/hdp/current/kafka-broker/bin/kafka-consumer-groups.sh \
    --bootstrap-server wn0-kafka:9092 \
    --group analytics-consumer \
    --describe
```

### Key Metrics

| Metric | Healthy Range | Action |
|--------|---------------|--------|
| Consumer Lag | < 10000 | Scale consumers |
| Under-replicated Partitions | 0 | Check broker health |
| Request Latency | < 100ms | Optimize config |
| Disk Usage | < 80% | Add brokers or cleanup |

---

## Related Documentation

- [Kafka Streaming](hdinsight-kafka-streaming.md)
- [Event Hubs Integration](../../docs/04-implementation-guides/integration-scenarios/eventhub-databricks.md)
- [Streaming Architectures](../../docs/03-architecture-patterns/streaming-architectures/README.md)

---

*Last Updated: January 2025*
