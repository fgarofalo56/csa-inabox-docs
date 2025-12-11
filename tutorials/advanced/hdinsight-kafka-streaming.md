# Kafka Streaming on HDInsight

> **[Home](../../README.md)** | **[Tutorials](../README.md)** | **HDInsight Kafka Streaming**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Level](https://img.shields.io/badge/Level-Advanced-red?style=flat-square)

Advanced streaming patterns with Kafka Streams on HDInsight.

---

## Overview

This tutorial covers:

- Kafka Streams applications
- Stream processing patterns
- Exactly-once semantics
- Stateful processing

**Duration**: 3 hours | **Prerequisites**: [HDInsight Kafka](hdinsight-kafka.md)

---

## Kafka Streams Fundamentals

### Application Setup

```java
import org.apache.kafka.streams.*;
import org.apache.kafka.streams.kstream.*;

public class EventStreamProcessor {

    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "event-processor");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "wn0-kafka:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, StreamsConfig.EXACTLY_ONCE_V2);

        StreamsBuilder builder = new StreamsBuilder();

        // Build topology
        KStream<String, String> events = builder.stream("raw-events");

        events
            .filter((key, value) -> value != null && !value.isEmpty())
            .mapValues(value -> parseAndEnrich(value))
            .to("enriched-events");

        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        streams.start();

        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
}
```

---

## Stream Processing Patterns

### Aggregation with Windows

```java
// Tumbling window aggregation
KStream<String, Event> events = builder.stream("events",
    Consumed.with(Serdes.String(), eventSerde));

KTable<Windowed<String>, Long> eventCounts = events
    .groupBy((key, event) -> event.getType())
    .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
    .count(Materialized.as("event-counts-store"));

// Convert to stream and output
eventCounts.toStream()
    .map((windowedKey, count) -> new KeyValue<>(
        windowedKey.key(),
        new AggregatedEvent(
            windowedKey.key(),
            windowedKey.window().start(),
            windowedKey.window().end(),
            count
        )
    ))
    .to("aggregated-events", Produced.with(Serdes.String(), aggregatedEventSerde));
```

### Joins

```java
// Stream-Stream Join
KStream<String, Order> orders = builder.stream("orders");
KStream<String, Payment> payments = builder.stream("payments");

KStream<String, OrderWithPayment> ordersWithPayments = orders.join(
    payments,
    (order, payment) -> new OrderWithPayment(order, payment),
    JoinWindows.of(Duration.ofMinutes(10)),
    StreamJoined.with(Serdes.String(), orderSerde, paymentSerde)
);

// Stream-Table Join
KTable<String, Customer> customers = builder.table("customers");

KStream<String, EnrichedOrder> enrichedOrders = orders.join(
    customers,
    (order, customer) -> new EnrichedOrder(order, customer)
);
```

### Stateful Processing

```java
// Custom state store for deduplication
StoreBuilder<KeyValueStore<String, Long>> storeBuilder = Stores.keyValueStoreBuilder(
    Stores.persistentKeyValueStore("dedup-store"),
    Serdes.String(),
    Serdes.Long()
);
builder.addStateStore(storeBuilder);

KStream<String, Event> deduplicated = events.transform(
    () -> new DeduplicationTransformer(),
    "dedup-store"
);

public class DeduplicationTransformer implements Transformer<String, Event, KeyValue<String, Event>> {
    private KeyValueStore<String, Long> store;

    @Override
    public void init(ProcessorContext context) {
        this.store = context.getStateStore("dedup-store");
    }

    @Override
    public KeyValue<String, Event> transform(String key, Event event) {
        String eventId = event.getId();
        Long existing = store.get(eventId);

        if (existing != null) {
            return null; // Duplicate, skip
        }

        store.put(eventId, System.currentTimeMillis());
        return KeyValue.pair(key, event);
    }

    @Override
    public void close() {}
}
```

---

## Python Alternative: Faust

```python
import faust
from datetime import timedelta

app = faust.App(
    'event-processor',
    broker='kafka://wn0-kafka:9092',
    store='rocksdb://'
)

# Define models
class Event(faust.Record):
    id: str
    type: str
    value: float
    timestamp: float

# Topics
events_topic = app.topic('events', value_type=Event)
aggregated_topic = app.topic('aggregated', value_type=dict)

# Tumbling window table
event_counts = app.Table(
    'event_counts',
    default=int,
    partitions=8
).tumbling(
    timedelta(minutes=5),
    expires=timedelta(hours=1)
)

@app.agent(events_topic)
async def process_events(events):
    async for event in events:
        # Update windowed count
        event_counts[event.type] += 1

@app.timer(interval=60.0)
async def emit_aggregations():
    """Emit aggregations every minute."""
    for key, count in event_counts.items():
        await aggregated_topic.send(value={
            'type': key,
            'count': count,
            'window_end': datetime.utcnow().isoformat()
        })

if __name__ == '__main__':
    app.main()
```

---

## Integration with Azure Services

### Stream to Event Hubs

```java
// Mirror from Kafka to Event Hubs
Properties mirrorProps = new Properties();
mirrorProps.put("bootstrap.servers", "wn0-kafka:9092");
mirrorProps.put("group.id", "eh-mirror");

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(mirrorProps);
consumer.subscribe(Arrays.asList("events"));

EventHubProducerClient ehProducer = new EventHubClientBuilder()
    .connectionString(eventHubConnStr)
    .buildProducerClient();

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));

    EventDataBatch batch = ehProducer.createBatch();
    for (ConsumerRecord<String, String> record : records) {
        batch.tryAdd(new EventData(record.value()));
    }

    ehProducer.send(batch);
    consumer.commitSync();
}
```

### Stream to Delta Lake

```python
# Spark Structured Streaming from Kafka to Delta
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("KafkaToDelta").getOrCreate()

# Read from Kafka
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "wn0-kafka:9092") \
    .option("subscribe", "aggregated-events") \
    .option("startingOffsets", "latest") \
    .load()

# Parse and transform
events = kafka_stream \
    .select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("processed_at", current_timestamp())

# Write to Delta with merge
def merge_to_delta(batch_df, batch_id):
    from delta.tables import DeltaTable

    delta_table = DeltaTable.forPath(spark, "/delta/aggregations")

    delta_table.alias("target").merge(
        batch_df.alias("source"),
        "target.type = source.type AND target.window_end = source.window_end"
    ).whenMatchedUpdateAll() \
     .whenNotMatchedInsertAll() \
     .execute()

events.writeStream \
    .foreachBatch(merge_to_delta) \
    .option("checkpointLocation", "/checkpoints/kafka-delta") \
    .start()
```

---

## Monitoring and Operations

### Stream Metrics

```java
// Add metrics reporter
props.put(StreamsConfig.METRICS_RECORDING_LEVEL_CONFIG, "DEBUG");

// Access metrics
for (Metric metric : streams.metrics().values()) {
    if (metric.metricName().name().contains("process-rate")) {
        System.out.printf("%s: %s%n", metric.metricName(), metric.metricValue());
    }
}
```

### Health Check Endpoint

```java
@RestController
public class HealthController {

    @Autowired
    private KafkaStreams streams;

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        KafkaStreams.State state = streams.state();

        Map<String, Object> health = new HashMap<>();
        health.put("state", state.toString());
        health.put("running", state.isRunningOrRebalancing());

        if (state == KafkaStreams.State.RUNNING) {
            return ResponseEntity.ok(health);
        }
        return ResponseEntity.status(503).body(health);
    }
}
```

---

## Related Documentation

- [HDInsight Kafka](hdinsight-kafka.md)
- [Stream Analytics](../../docs/02-services/streaming-services/azure-stream-analytics/README.md)
- [Event Hubs Integration](../../docs/04-implementation-guides/integration-scenarios/eventhub-stream-analytics.md)

---

*Last Updated: January 2025*
