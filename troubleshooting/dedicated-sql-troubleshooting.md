# Dedicated SQL Pool Troubleshooting

> **[Home](../README.md)** | **[Troubleshooting](index.md)** | **Dedicated SQL Pool**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Complexity](https://img.shields.io/badge/Complexity-Intermediate-yellow?style=flat-square)

Troubleshooting guide for Azure Synapse Dedicated SQL Pools.

---

## Common Issues

### 1. Query Performance Issues

#### Symptoms
- Queries running slower than expected
- High resource utilization
- Query timeouts

#### Diagnostic Steps

```sql
-- Check running queries and resource usage
SELECT
    r.request_id,
    r.session_id,
    r.status,
    r.submit_time,
    r.start_time,
    r.total_elapsed_time,
    r.resource_class,
    r.command
FROM sys.dm_pdw_exec_requests r
WHERE r.status NOT IN ('Completed', 'Failed', 'Cancelled')
ORDER BY r.submit_time DESC;

-- Check data movement operations
SELECT
    request_id,
    step_index,
    operation_type,
    distribution_type,
    location_type,
    status,
    start_time,
    end_time,
    total_elapsed_time,
    row_count
FROM sys.dm_pdw_request_steps
WHERE request_id = '<request_id>'
ORDER BY step_index;

-- Check for data skew
SELECT
    OBJECT_NAME(object_id) AS table_name,
    pdw_node_id,
    distribution_id,
    SUM(row_count) AS rows
FROM sys.dm_pdw_nodes_db_partition_stats
WHERE index_id < 2
GROUP BY object_id, pdw_node_id, distribution_id
ORDER BY table_name, pdw_node_id, distribution_id;
```

#### Solutions

1. **Optimize Distribution**
   ```sql
   -- Check current distribution
   SELECT
       t.name AS table_name,
       c.name AS distribution_column,
       d.distribution_policy_desc
   FROM sys.tables t
   JOIN sys.pdw_table_distribution_properties d ON t.object_id = d.object_id
   LEFT JOIN sys.columns c ON t.object_id = c.object_id AND c.column_id = d.distribution_ordinal
   WHERE d.distribution_policy_desc = 'HASH';

   -- Redistribute table if needed
   CREATE TABLE new_table
   WITH (
       DISTRIBUTION = HASH(customer_id),
       CLUSTERED COLUMNSTORE INDEX
   )
   AS SELECT * FROM old_table;
   ```

2. **Update Statistics**
   ```sql
   -- Update all statistics
   EXEC sp_updatestats;

   -- Update specific table statistics
   UPDATE STATISTICS schema_name.table_name;
   ```

3. **Optimize Resource Class**
   ```sql
   -- Check current resource class
   SELECT name, importance, min_percentage_resource
   FROM sys.workload_management_workload_classifiers;

   -- Assign user to larger resource class
   EXEC sp_addrolemember 'largerc', 'user_name';
   ```

---

### 2. Connection Issues

#### Symptoms
- Unable to connect to dedicated pool
- Connection timeouts
- Authentication failures

#### Diagnostic Steps

```sql
-- Check active connections
SELECT
    session_id,
    login_name,
    client_net_address,
    status,
    login_time,
    last_request_start_time
FROM sys.dm_pdw_exec_sessions
WHERE status = 'Active'
ORDER BY login_time DESC;

-- Check connection limits
SELECT
    active_session_count,
    queued_request_count,
    active_request_count
FROM sys.dm_pdw_nodes_resource_governor_workload_groups;
```

#### Solutions

1. **Check Firewall Rules**
   ```bash
   az synapse workspace firewall-rule list \
       --workspace-name my-workspace \
       --resource-group my-rg
   ```

2. **Verify Pool Status**
   ```bash
   az synapse sql pool show \
       --name dedicated-pool \
       --workspace-name my-workspace \
       --resource-group my-rg \
       --query "status"
   ```

3. **Resume Paused Pool**
   ```bash
   az synapse sql pool resume \
       --name dedicated-pool \
       --workspace-name my-workspace \
       --resource-group my-rg
   ```

---

### 3. Data Load Failures

#### Symptoms
- COPY command fails
- PolyBase errors
- Data type mismatches

#### Diagnostic Steps

```sql
-- Check load operation status
SELECT
    r.request_id,
    r.status,
    r.error_id,
    r.command
FROM sys.dm_pdw_exec_requests r
WHERE r.command LIKE '%COPY%' OR r.command LIKE '%INSERT%'
ORDER BY r.submit_time DESC;

-- Check for data load errors
SELECT * FROM sys.dm_pdw_errors
WHERE request_id = '<request_id>';
```

#### Solutions

1. **Fix COPY Command Issues**
   ```sql
   -- Proper COPY command format
   COPY INTO target_table
   FROM 'https://storage.blob.core.windows.net/container/path/'
   WITH (
       FILE_TYPE = 'PARQUET',
       CREDENTIAL = (IDENTITY = 'Managed Identity'),
       MAXERRORS = 10,
       ERRORFILE = 'https://storage.blob.core.windows.net/errors/'
   );
   ```

2. **Handle Schema Mismatches**
   ```sql
   -- Create staging table with flexible types
   CREATE TABLE staging_table
   WITH (
       DISTRIBUTION = ROUND_ROBIN,
       HEAP
   )
   AS SELECT
       CAST(column1 AS VARCHAR(100)) AS column1,
       CAST(column2 AS DECIMAL(18,4)) AS column2
   FROM external_table;
   ```

---

### 4. Concurrency and Blocking

#### Symptoms
- Queries stuck in queue
- Long wait times
- Blocking chains

#### Diagnostic Steps

```sql
-- Check waiting queries
SELECT
    r.request_id,
    r.status,
    r.resource_class,
    r.command,
    w.wait_id,
    w.wait_type,
    w.object_type,
    w.object_name
FROM sys.dm_pdw_exec_requests r
JOIN sys.dm_pdw_waits w ON r.request_id = w.request_id
WHERE r.status = 'Running'
ORDER BY w.wait_id;

-- Check blocking
SELECT
    blocking_request_id,
    request_id,
    object_type,
    object_name
FROM sys.dm_pdw_waits
WHERE state = 'Blocked';
```

#### Solutions

1. **Increase Concurrency Slots**
   ```sql
   -- Use smaller resource class for more concurrency
   EXEC sp_addrolemember 'smallrc', 'concurrent_user';
   ```

2. **Implement Workload Management**
   ```sql
   -- Create workload classifier
   CREATE WORKLOAD CLASSIFIER high_priority
   WITH (
       WORKLOAD_GROUP = 'high_priority_wg',
       MEMBERNAME = 'executive_user',
       IMPORTANCE = HIGH
   );
   ```

---

## Monitoring Queries

### Health Check Dashboard

```sql
-- Overall health check
SELECT
    'Active Sessions' AS metric,
    COUNT(*) AS value
FROM sys.dm_pdw_exec_sessions WHERE status = 'Active'
UNION ALL
SELECT
    'Running Queries',
    COUNT(*)
FROM sys.dm_pdw_exec_requests WHERE status = 'Running'
UNION ALL
SELECT
    'Queued Queries',
    COUNT(*)
FROM sys.dm_pdw_exec_requests WHERE status = 'Queued';
```

### Performance Baseline

```sql
-- Query execution statistics
SELECT
    DATEADD(hour, DATEDIFF(hour, 0, submit_time), 0) AS hour,
    COUNT(*) AS query_count,
    AVG(total_elapsed_time) AS avg_duration_ms,
    MAX(total_elapsed_time) AS max_duration_ms
FROM sys.dm_pdw_exec_requests
WHERE submit_time > DATEADD(day, -7, GETDATE())
GROUP BY DATEADD(hour, DATEDIFF(hour, 0, submit_time), 0)
ORDER BY hour DESC;
```

---

## Related Documentation

- [Synapse Analytics Overview](../docs/02-services/analytics-compute/azure-synapse/README.md)
- [Performance Optimization](../docs/05-best-practices/performance/README.md)
- [Full Troubleshooting Guide](../docs/troubleshooting/README.md)

---

*Last Updated: January 2025*
