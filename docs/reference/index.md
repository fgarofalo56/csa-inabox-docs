[Home](../../README.md) > Reference Guide

# Azure Synapse Analytics Reference Guide

This reference guide provides detailed technical specifications, API references, and configuration options for Azure Synapse Analytics components related to Delta Lakehouse and Serverless SQL.

## Delta Lake Reference

### Delta Table Specifications

| Property | Description | Default Value |
|----------|-------------|--------------|
| delta.logRetentionDuration | Duration for which log files are kept | "30 days" |
| delta.deletedFileRetentionDuration | Duration for which deleted data files are kept | "30 days" |
| delta.enableChangeDataFeed | Whether to record row-level changes | false |
| delta.autoOptimize.autoCompact | Whether to compact small files automatically | false |
| delta.autoOptimize.optimizeWrite | Whether to optimize writes automatically | false |
| delta.columnMapping.mode | Column mapping mode (name or id) | "none" |

### Delta Lake Operations

| Operation | Syntax | Description |
|-----------|--------|-------------|
| Time Travel | `SELECT * FROM tableName VERSION AS OF version` | Query a table at a specific version |
| Optimize | `OPTIMIZE tableName [WHERE condition]` | Compact small files into larger ones |
| Vacuum | `VACUUM tableName RETAIN n HOURS` | Delete files no longer needed |
| Describe History | `DESCRIBE HISTORY tableName` | View transaction history of a table |
| Convert to Delta | `CONVERT TO DELTA tableName` | Convert Parquet table to Delta format |
| Merge | `MERGE INTO target USING source ON condition WHEN MATCHED THEN UPDATE SET... WHEN NOT MATCHED THEN INSERT...` | Perform upsert operations |

### Delta Lake System Requirements

| Component | Requirement |
|-----------|-------------|
| Spark Version | 3.0 or later |
| JVM | 8 or 11 |
| Azure Synapse Spark Pool | Recommended minimum: Medium (8 vCores) |
| Storage | ADLS Gen2 |

## Serverless SQL Reference

### Supported Data Formats

| Format | Read Support | Write Support | Notes |
|--------|-------------|--------------|-------|
| Parquet | Yes | Yes | Recommended for best performance |
| Delta | Yes | Limited | Supports Delta Lake tables |
| CSV | Yes | Yes | Multiple delimiters supported |
| JSON | Yes | Yes | Nested structures supported |
| ORC | Yes | No | Read-only support |

### System Views

| View Name | Description |
|-----------|-------------|
| sys.external_file_formats | Lists all external file formats defined |
| sys.external_data_sources | Lists all external data sources |
| sys.external_tables | Lists all external tables |
| sys.database_scoped_credentials | Lists all database scoped credentials |
| sys.database_principals | Lists all users and roles in the database |

### Query Syntax Extensions

```sql
-- OPENROWSET syntax for querying external data
SELECT *
FROM OPENROWSET(
    BULK 'path_to_data',
    FORMAT = 'format_type',
    [PARSER_VERSION = '1.0'],
    [HEADER_ROW = {TRUE | FALSE}],
    [FIELDTERMINATOR = 'field_terminator'],
    [ROWTERMINATOR = 'row_terminator'],
    [FIELDQUOTE = 'field_quote'],
    [ENCODING = 'encoding']
) AS alias

-- CREATE EXTERNAL TABLE syntax
CREATE EXTERNAL TABLE [schema_name].[table_name]
(
    column_name data_type [NULL | NOT NULL],
    ...
)
WITH
(
    LOCATION = 'folder_or_filepath',
    DATA_SOURCE = external_data_source_name,
    FILE_FORMAT = external_file_format_name,
    [REJECT_TYPE = {VALUE | ROW}],
    [REJECT_VALUE = reject_value],
    [REJECTED_ROW_LOCATION = 'path']
)

-- CREATE DATABASE SCOPED CREDENTIAL syntax
CREATE DATABASE SCOPED CREDENTIAL credential_name
WITH IDENTITY = 'identity_name',
     SECRET = 'secret_value'
```

### Limitations and Quotas

| Resource | Limit |
|----------|-------|
| Query execution time | 60 minutes maximum |
| Memory per query | Up to 1 GB per node |
| Concurrent queries | Varies by workload and resource class |
| Result set size | Maximum 10 GB |
| Storage account access | Up to 10 storage accounts per query |

## Azure Synapse Integration

### Integration with Azure Services

| Azure Service | Integration Type | Use Cases |
|--------------|-----------------|-----------|
| Azure Active Directory | Authentication | Identity management, access control |
| Azure Key Vault | Security | Secrets management, encryption |
| Azure Monitor | Monitoring | Performance tracking, logging |
| Azure Event Hubs | Data ingestion | Real-time analytics |
| Power BI | Data visualization | Dashboards, reports |
| Azure Machine Learning | ML integration | Model training, inference |

### REST API Reference

For programmatic access to Azure Synapse Analytics services, refer to the official REST API documentation:

- [Synapse Analytics REST API Reference](https://learn.microsoft.com/en-us/rest/api/synapse/)
- [Spark Batch API Reference](https://learn.microsoft.com/en-us/azure/synapse-analytics/spark/apache-spark-development-overview)
- [SQL API Reference](https://learn.microsoft.com/en-us/rest/api/synapse/sql-api)

## Resource Optimization

### Performance Optimization Techniques

| Technique | Description | Benefit |
|-----------|-------------|---------|
| Data partitioning | Divide data by date, region, etc. | Improved query performance, data pruning |
| File size optimization | Target 100MB-1GB file sizes | Better parallelism, reduced overhead |
| Statistics | Create statistics on key columns | Better query plans |
| Caching | Use result set caching | Faster repeated queries |
| Resource classes | Use appropriate resource class | Memory and concurrency management |

### Cost Optimization

| Strategy | Description | Impact |
|----------|-------------|--------|
| Serverless vs. Dedicated | Choose correct compute model | Pay-per-use vs. reserved capacity |
| Auto-pause | Configure auto-pause for dedicated resources | Reduce idle costs |
| Query optimization | Reduce data scanned | Lower data processing costs |
| Storage tiers | Use appropriate storage tier | Balance performance and cost |
| Monitoring | Track usage patterns | Identify optimization opportunities |

## Appendix

### Common Error Codes

| Error Code | Description | Troubleshooting |
|------------|-------------|----------------|
| 401 | Unauthorized | Check authentication credentials |
| 403 | Forbidden | Verify access permissions |
| 404 | Not found | Verify resource existence and path |
| 429 | Too many requests | Implement retry with backoff strategy |
| 500 | Internal server error | Contact support with request ID |

### Glossary

- **ADLS Gen2**: Azure Data Lake Storage Gen2
- **ACID**: Atomicity, Consistency, Isolation, Durability
- **CDC**: Change Data Capture
- **MPP**: Massively Parallel Processing
- **OLAP**: Online Analytical Processing
- **SCD**: Slowly Changing Dimension
- **TTL**: Time to Live
- **UDF**: User-Defined Function
- **RBAC**: Role-Based Access Control
