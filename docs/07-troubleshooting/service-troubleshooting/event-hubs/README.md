# Azure Event Hubs Troubleshooting Guide

> **[Home](../../../README.md)** | **[Troubleshooting](../../README.md)** | **Event Hubs**

![Status](https://img.shields.io/badge/Status-Active-brightgreen) ![Service](https://img.shields.io/badge/Service-Event_Hubs-blue)

Comprehensive troubleshooting guide for Azure Event Hubs including connection failures, throughput throttling, consumer lag, partition distribution, checkpoint store issues, and Kafka protocol compatibility.

---

## Common Issues

### Issue 1: Connection Failures

- Error: `Connection refused. Could not connect to <namespace>.servicebus.windows.net:5671`
- Error: `The SSL connection could not be established`
- AMQP connection drops intermittently

| Cause | Likelihood | Impact |
|:------|:-----------|:-------|
| Firewall blocking port 5671/5672 or 9093 | High | High |
| Expired or invalid SAS token / connection string | High | High |
| TLS version mismatch (requires TLS 1.2+) | Medium | Medium |
| AMQP connection limit reached | Low | Medium |

### Issue 2: Throughput Throttling (429 Errors)

- Error: `Server busy. The maximum number of throughput units exceeded.`
- Error: `QuotaExceeded: The messaging entity has reached its maximum allowed size.`
- HTTP 429 responses from the REST API; producer `Send` operations failing

### Issue 3: Consumer Lag

- Events accumulating faster than consumers process them
- `IncomingMessages` far exceeds `OutgoingMessages` over time
- Real-time analytics dashboards showing stale data

### Issue 4: Partition Key Distribution (Hot Partitions)

- Some partitions have significantly more events than others
- One partition's consumer running behind while others are caught up

### Issue 5: Checkpoint Store Problems

- Error: `The lease has been lost and cannot be renewed`
- Error: `The specified container does not exist`
- Consumers reprocessing events from the beginning after restart

### Issue 6: AMQP Connection Limits

- Error: `The maximum number of connections has been reached`

| SKU | Max AMQP Connections | Max Partitions |
|:----|:---------------------|:---------------|
| Basic | 100 | 32 |
| Standard | 5,000 | 32 |
| Premium | 10,000 | 100 |
| Dedicated | 100,000 | 1,024 |

---

## Diagnostic Steps

### Check Namespace Health

```bash
# Check namespace status and capacity
az eventhubs namespace show \
    --resource-group "<rg-name>" --name "<namespace>" \
    --query "{status:status, sku:sku.name, capacity:sku.capacity, autoInflate:isAutoInflateEnabled}"

# Get throughput metrics for the last hour
az monitor metrics list \
    --resource "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.EventHub/namespaces/<namespace>" \
    --metric "IncomingMessages" "OutgoingMessages" "ThrottledRequests" "IncomingBytes" \
    --interval PT5M --output table
```

### Check Consumer Group Lag

```python
from azure.eventhub import EventHubConsumerClient

def check_consumer_lag(connection_str, eventhub_name, consumer_group):
    """Check consumer lag across all partitions."""
    client = EventHubConsumerClient.from_connection_string(
        connection_str, consumer_group=consumer_group, eventhub_name=eventhub_name
    )
    try:
        props = client.get_eventhub_properties()
        print(f"Event Hub: {eventhub_name} | Partitions: {len(props['partition_ids'])}")
        for pid in props["partition_ids"]:
            p = client.get_partition_properties(pid)
            print(f"  Partition {pid}: last_seq={p['last_enqueued_sequence_number']}, empty={p['is_empty']}")
    finally:
        client.close()
```

### Test Connectivity

```python
import socket, ssl

def test_eventhub_connectivity(namespace):
    """Test network connectivity to Event Hubs endpoints."""
    for host, port, proto in [
        (f"{namespace}.servicebus.windows.net", 5671, "AMQP"),
        (f"{namespace}.servicebus.windows.net", 443,  "AMQP-WS"),
        (f"{namespace}.servicebus.windows.net", 9093, "Kafka"),
    ]:
        try:
            sock = socket.create_connection((host, port), timeout=10)
            ctx = ssl.create_default_context()
            ssock = ctx.wrap_socket(sock, server_hostname=host)
            print(f"{proto:10s} ({host}:{port}) -> OK (TLS: {ssock.version()})")
            ssock.close()
        except socket.timeout:
            print(f"{proto:10s} ({host}:{port}) -> TIMEOUT (check firewall)")
        except Exception as e:
            print(f"{proto:10s} ({host}:{port}) -> FAILED: {e}")
```

### Verify Checkpoint Store

```python
from azure.storage.blob import ContainerClient

def verify_checkpoint_store(storage_conn_str, container_name):
    """Verify checkpoint store container and contents."""
    container = ContainerClient.from_connection_string(storage_conn_str, container_name)
    if not container.exists():
        print(f"ERROR: Container '{container_name}' does not exist! Create it first.")
        return
    blobs = list(container.list_blobs())
    checkpoints = [b for b in blobs if "/checkpoint/" in b.name]
    ownership = [b for b in blobs if "/ownership/" in b.name]
    print(f"Container: {container_name} | Checkpoints: {len(checkpoints)} | Ownership: {len(ownership)}")
```

---

## Solutions

### Resolve Connection Failures

```python
from azure.eventhub import EventHubProducerClient, TransportType

# Use AMQP over WebSockets (port 443) when port 5671 is blocked
producer = EventHubProducerClient.from_connection_string(
    conn_str="<connection-string>",
    eventhub_name="<eventhub-name>",
    transport_type=TransportType.AmqpOverWebsocket,  # Uses port 443
    retry_total=5,
    retry_backoff_factor=0.8,
    retry_backoff_max=120
)
```

### Handle Throughput Throttling

```bash
# Enable Auto-Inflate to automatically scale throughput units
az eventhubs namespace update \
    --resource-group "<rg-name>" --name "<namespace>" \
    --enable-auto-inflate true --maximum-throughput-units 20

# Or manually increase TUs (1 TU = 1 MB/s in, 2 MB/s out)
az eventhubs namespace update \
    --resource-group "<rg-name>" --name "<namespace>" --capacity 10
```

```python
from azure.eventhub import EventHubProducerClient, EventData

async def send_events_batched(producer, events):
    """Send events in optimally-sized batches to maximize throughput."""
    batch = await producer.create_batch()
    for event_data in events:
        try:
            batch.add(EventData(event_data))
        except ValueError:  # Batch full
            await producer.send_batch(batch)
            batch = await producer.create_batch()
            batch.add(EventData(event_data))
    if len(batch) > 0:
        await producer.send_batch(batch)
```

### Fix Consumer Lag

Scale consumers and optimize checkpoint frequency:

```python
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblob.aio import BlobCheckpointStore

async def create_scaled_consumer(connection_str, eventhub_name, storage_conn_str):
    checkpoint_store = BlobCheckpointStore.from_connection_string(
        storage_conn_str, "eventhub-checkpoints"
    )
    consumer = EventHubConsumerClient.from_connection_string(
        connection_str, consumer_group="$Default", eventhub_name=eventhub_name,
        checkpoint_store=checkpoint_store,
        load_balancing_interval=10,
        partition_ownership_expiration_interval=60
    )

    async def on_event(partition_context, event):
        # Process event, then checkpoint
        await partition_context.update_checkpoint(event)

    async with consumer:
        await consumer.receive(on_event=on_event)
```

### Fix Partition Key Distribution

```python
import hashlib

def get_balanced_partition_key(entity_id, num_partitions=32):
    """Generate well-distributed partition keys using hashing."""
    hash_hex = hashlib.sha256(str(entity_id).encode()).hexdigest()
    return f"partition-{int(hash_hex, 16) % num_partitions}"
```

### Initialize Checkpoint Store

```python
from azure.storage.blob import ContainerClient

def initialize_checkpoint_store(storage_conn_str, container_name):
    """Ensure checkpoint store container exists and is writable."""
    container = ContainerClient.from_connection_string(storage_conn_str, container_name)
    try:
        container.create_container()
        print(f"Created checkpoint container: {container_name}")
    except Exception as e:
        if "ContainerAlreadyExists" not in str(e):
            raise
    # Verify write access
    test_blob = container.get_blob_client("__health_check__")
    test_blob.upload_blob(b"ok", overwrite=True)
    test_blob.delete_blob()
    print("Checkpoint store write access: OK")
```

---

## Kafka Protocol Compatibility

Azure Event Hubs exposes a Kafka-compatible endpoint on port 9093.

### Required Kafka Client Configuration

```properties
bootstrap.servers=<namespace>.servicebus.windows.net:9093
security.protocol=SASL_SSL
sasl.mechanism=PLAIN
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required \
    username="$ConnectionString" \
    password="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<key-name>;SharedAccessKey=<key>";
```

### Common Kafka Compatibility Errors

| Error | Cause | Solution |
|:------|:------|:---------|
| `UNKNOWN_TOPIC_OR_PARTITION` | Event Hub does not exist | Create the Event Hub first |
| `TOPIC_AUTHORIZATION_FAILED` | Missing `Send`/`Listen` claim | Update SAS policy |
| `GROUP_COORDINATOR_NOT_AVAILABLE` | Consumer group issue | Auto-created on Standard+ SKU |
| `UNSUPPORTED_VERSION` | API version mismatch | Use Kafka client 1.0+ |

**Unsupported Kafka features:** idempotent producer, transactions, log compaction, Kafka Streams (limited).

---

## Monitoring Alerts

```bash
# Alert on throttled requests
az monitor metrics alert create \
    --resource-group "<rg-name>" --name "eventhub-throttling-alert" \
    --scopes "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.EventHub/namespaces/<namespace>" \
    --condition "total ThrottledRequests > 10" \
    --window-size 5m --evaluation-frequency 1m --action "<action-group-id>"
```

---

## Related Resources

| Resource | Description |
|----------|-------------|
| [Stream Analytics](../stream-analytics/README.md) | Stream processing troubleshooting |
| [Event Hubs Documentation](https://learn.microsoft.com/azure/event-hubs/) | Official Microsoft documentation |
| [Event Hubs Quotas](https://learn.microsoft.com/azure/event-hubs/event-hubs-quotas) | SKU limits and quotas reference |
| [Kafka on Event Hubs](https://learn.microsoft.com/azure/event-hubs/azure-event-hubs-kafka-overview) | Kafka protocol compatibility guide |

---

> **Tip:** Always enable Auto-Inflate on Standard tier namespaces to handle unexpected traffic spikes. Monitor `ThrottledRequests` and `ServerErrors` metrics as leading indicators of capacity issues.

**Last Updated:** 2026-04-07
**Version:** 1.0.0
