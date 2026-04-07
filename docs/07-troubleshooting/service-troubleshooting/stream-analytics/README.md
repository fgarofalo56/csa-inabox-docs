# Azure Stream Analytics Troubleshooting Guide

> **[Home](../../../README.md)** | **[Troubleshooting](../../README.md)** | **Stream Analytics**

![Status](https://img.shields.io/badge/Status-Active-brightgreen) ![Service](https://img.shields.io/badge/Service-Stream_Analytics-purple)

Comprehensive troubleshooting guide for Azure Stream Analytics including job start failures, input deserialization errors, output sink failures, watermark delays, query execution errors, and windowing function problems.

---

## Common Issues

### Issue 1: Job Start Failures

- Job transitions from `Starting` to `Failed`
- Error: `StreamingJobStartFailure` in Activity Log
- Error: `The streaming job failed to start because of an error in the query or input/output configuration.`

| Cause | Likelihood | Impact |
|:------|:-----------|:-------|
| Input source not accessible | High | High |
| Invalid query syntax | High | High |
| Output sink authentication failure | Medium | High |
| Incompatible serialization format | Medium | Medium |
| Insufficient Streaming Units | Low | Medium |

### Issue 2: Input Deserialization Errors

- Error: `Could not deserialize the input event(s) from resource '<input>' as JSON`
- Error: `CSV parsing error: unexpected number of fields`
- Events in input metrics but not in query output

### Issue 3: Output Sink Failures

- Error: `OutputDataConversionError` in diagnostics logs
- Error: `AuthorizationFailed` for SQL Database or Blob Storage output
- Events processed but not appearing in the output destination

### Issue 4: Watermark Delays

- `OutputWatermarkDelaySeconds` exceeds threshold (> 60s)
- Late-arriving events being dropped; job health shows `Degraded`

| Cause | Likelihood | Impact |
|:------|:-----------|:-------|
| Insufficient Streaming Units | High | High |
| High computational complexity query | High | High |
| Data skew across partitions | Medium | High |
| Slow output sink writes | Medium | Medium |

### Issue 5: Query Execution Errors

- Error: `Unable to cast value '<value>' to type '<type>'`
- Error: `Reference data lookup failed`
- Null or unexpected values in query output

### Issue 6: Reference Data Join Issues

- Error: `Reference data input '<name>' is not available`
- Joins returning NULLs for all reference columns
- Reference data not refreshing on schedule

---

## Diagnostic Steps

### Check Job Status

```bash
# Get current job status
az stream-analytics job show \
    --resource-group "<rg-name>" --name "<job-name>" \
    --query "{status:jobState, lastOutput:lastOutputEventTime, su:sku.capacity}"

# Check Activity Log for errors
az monitor activity-log list \
    --resource-group "<rg-name>" --offset 1h \
    --query "[?contains(resourceType.value, 'StreamAnalytics')].{time:eventTimestamp, status:status.value, message:properties.statusMessage}" \
    --output table
```

### Test Input and Output Connections

```bash
# Test input connection
az stream-analytics input test \
    --resource-group "<rg-name>" --job-name "<job-name>" --input-name "<input-name>"

# Test output connection
az stream-analytics output test \
    --resource-group "<rg-name>" --job-name "<job-name>" --output-name "<output-name>"
```

### Enable Diagnostic Logging

```bash
az monitor diagnostic-settings create \
    --resource "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.StreamAnalytics/streamingjobs/<job-name>" \
    --name "asa-diagnostics" \
    --workspace "<log-analytics-workspace-id>" \
    --logs '[{"category": "Execution", "enabled": true}, {"category": "Authoring", "enabled": true}]' \
    --metrics '[{"category": "AllMetrics", "enabled": true}]'
```

### Monitor Key Metrics

```bash
az monitor metrics list \
    --resource "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.StreamAnalytics/streamingjobs/<job-name>" \
    --metric "InputEvents" "OutputEvents" "DroppedOrAdjustedEvents" \
        "Errors" "OutputWatermarkDelaySeconds" "ResourceUtilization" \
    --interval PT5M --output table
```

### Validate Query Logic

```sql
-- Check input schema types
SELECT
    GetType(temperature) AS temp_type,
    GetType(deviceId) AS device_type,
    COUNT(*) AS event_count
FROM [input] TIMESTAMP BY timestamp
GROUP BY GetType(temperature), GetType(deviceId), TumblingWindow(minute, 1)

-- Diagnose reference data join misses
SELECT i.deviceId, r.deviceName,
    CASE WHEN r.deviceName IS NULL THEN 'MISSING_REF' ELSE 'OK' END AS join_status
FROM [input] i
LEFT JOIN [reference] r ON i.deviceId = r.deviceId
```

---

## Solutions

### Fix Job Start Failures

```bash
# Create a dedicated consumer group for ASA (avoid sharing $Default)
az eventhubs eventhub consumer-group create \
    --resource-group "<rg-name>" --namespace-name "<eh-namespace>" \
    --eventhub-name "<eventhub>" --name "asa-consumer-group"

# Start from last output time to avoid reprocessing
az stream-analytics job start \
    --resource-group "<rg-name>" --name "<job-name>" \
    --output-start-mode LastOutputEventTime
```

### Fix Input Deserialization Errors

```sql
-- Use TRY_CAST to handle malformed data gracefully
SELECT
    IoTHub.ConnectionDeviceId AS deviceId,
    TRY_CAST(temperature AS float) AS temperature,
    TRY_CAST(humidity AS float) AS humidity,
    EventEnqueuedUtcTime AS eventTime
INTO [output]
FROM [input]
WHERE TRY_CAST(temperature AS float) IS NOT NULL
```

```bash
# Verify serialization settings if using CSV
az stream-analytics input update \
    --resource-group "<rg-name>" --job-name "<job-name>" --input-name "<input-name>" \
    --properties '{"serialization": {"type": "Csv", "properties": {"fieldDelimiter": ",", "encoding": "UTF8"}}}'
```

### Fix Output Sink Failures

```bash
# For SQL Database output - allow Azure services through firewall
az sql server firewall-rule create \
    --resource-group "<rg-name>" --server "<sql-server>" \
    --name "AllowAzureServices" --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0

# For Blob Storage output - ensure container exists
az storage container create \
    --name "<container-name>" --account-name "<storage-account>" --auth-mode login
```

### Resolve Watermark Delays

```bash
# Scale up Streaming Units (minimum: 1 SU per 3 input partitions)
az stream-analytics job update \
    --resource-group "<rg-name>" --name "<job-name>" \
    --transformation '{"name": "Transformation", "properties": {"streamingUnits": 12, "query": "<your-query>"}}'
```

```sql
-- Use PARTITION BY for parallel processing (reduces watermark delay)
SELECT deviceId, AVG(temperature) AS avg_temp, System.Timestamp() AS window_end
FROM [input] PARTITION BY PartitionId
TIMESTAMP BY eventTime
GROUP BY deviceId, PartitionId, TumblingWindow(minute, 5)
```

### Fix Reference Data Joins

```bash
# Upload reference data to the correct blob path pattern
az storage blob upload \
    --account-name "<storage-account>" --container-name "reference" \
    --name "2026/04/07/devices.json" --file "./devices.json" --auth-mode login
```

---

## Windowing Function Problems

| Window Type | Common Issue | Solution |
|:------------|:-------------|:---------|
| Tumbling | Events in wrong window | Verify `TIMESTAMP BY` uses correct event field |
| Hopping | Duplicate output events | Expected when hop size < window size |
| Sliding | No output for long periods | Only fires when events enter or exit window |
| Session | Sessions never closing | Reduce `SessionWindow` timeout |
| Snapshot | Incorrect grouping | Groups events with identical timestamps |

### Debug Tumbling Windows

```sql
SELECT
    System.Timestamp() AS WindowEnd,
    COUNT(*) AS EventCount,
    MIN(EventEnqueuedUtcTime) AS EarliestEvent,
    MAX(EventEnqueuedUtcTime) AS LatestEvent
INTO [debug-output]
FROM [input] TIMESTAMP BY EventEnqueuedUtcTime
GROUP BY TumblingWindow(minute, 5)
```

### Configure Late Arrival Policy

```bash
az stream-analytics job update \
    --resource-group "<rg-name>" --name "<job-name>" \
    --events-late-arrival-max-delay-in-seconds 30 \
    --events-out-of-order-max-delay-in-seconds 10 \
    --events-out-of-order-policy Adjust
```

---

## Job Design Checklist

- [ ] Each input uses a dedicated consumer group (not `$Default`)
- [ ] Query uses `PARTITION BY` for parallel processing
- [ ] `TIMESTAMP BY` uses the correct event-time field
- [ ] Late arrival and out-of-order tolerances are configured
- [ ] Output sink permissions tested with `Test Connection`
- [ ] Streaming Units: minimum 1 SU per 3 input partitions
- [ ] Reference data path pattern and refresh interval configured
- [ ] Diagnostic logs enabled and forwarded to Log Analytics

---

## Related Resources

| Resource | Description |
|----------|-------------|
| [Event Hubs](../event-hubs/README.md) | Event Hubs troubleshooting (common ASA input) |
| [ASA Documentation](https://learn.microsoft.com/azure/stream-analytics/) | Official Microsoft documentation |
| [ASA Query Reference](https://learn.microsoft.com/stream-analytics-query/stream-analytics-query-language-reference) | Complete query language reference |
| [ASA Troubleshooting](https://learn.microsoft.com/azure/stream-analytics/stream-analytics-troubleshoot-query) | Official troubleshooting guide |

---

> **Tip:** Always use the **Test Query** feature in the Azure portal with sample data before deploying query changes to a running production job.

**Last Updated:** 2026-04-07
**Version:** 1.0.0
