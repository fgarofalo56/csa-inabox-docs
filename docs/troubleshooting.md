# Troubleshooting Guide

[Home](../README.md) > Troubleshooting

!!! note "Comprehensive Troubleshooting Documentation Available"
    This page has been replaced with a comprehensive troubleshooting section. Please visit the [Troubleshooting Documentation](troubleshooting/README.md) for detailed guides on resolving common issues with Azure Synapse Analytics.

## Quick Links

- [Spark Issues](troubleshooting/spark-troubleshooting.md)
- [Serverless SQL Issues](troubleshooting/serverless-sql-troubleshooting.md)
- [Connectivity Issues](troubleshooting/connectivity-troubleshooting.md)
- [Authentication Issues](troubleshooting/authentication-troubleshooting.md)
- [Delta Lake Issues](troubleshooting/delta-lake-troubleshooting.md)
- [Pipeline Issues](troubleshooting/pipeline-troubleshooting.md)

## Connection Issues

### Cannot connect to Synapse workspace

__Symptoms__: Unable to access Synapse Studio or connect to the workspace.

__Possible Causes and Solutions__:

1. __Network Connectivity__:
   - Ensure your network allows connections to the Azure Synapse service endpoints
   - Check if firewall rules are properly configured in the Azure portal
   - Verify you're using the correct workspace URL

2. __Authentication Issues__:
   - Confirm you have the appropriate permissions to access the workspace
   - Check if your Azure Active Directory credentials are valid
   - Try signing out and signing back in to refresh authentication tokens

3. __Service Outage__:
   - Check the [Azure Status page](https://status.azure.com) for any ongoing service issues

## Performance Problems

### Slow Query Performance in Dedicated SQL Pools

__Symptoms__: Queries take longer than expected to complete.

__Possible Causes and Solutions__:

1. __Suboptimal Distribution__:
   - Verify table distribution keys are appropriate for common query patterns
   - Check for data skew using `DBCC PDW_SHOWSPACEUSED`
   - Consider redistributing tables with high skew

2. __Statistics Issues__:
   - Ensure statistics are up-to-date using `UPDATE STATISTICS`
   - Check for missing statistics in execution plans

3. __Resource Constraints__:
   - Monitor resource utilization during query execution
   - Consider scaling up the SQL pool during peak workloads
   - Implement query concurrency management

### Spark Jobs Failing or Running Slowly

__Symptoms__: Spark notebooks or jobs time out, fail, or perform poorly.

__Possible Causes and Solutions__:

1. __Resource Allocation__:
   - Check if the Spark pool has sufficient memory and cores
   - Monitor executor memory usage and adjust configurations
   - Consider increasing the executor count for large datasets

2. __Data Skew__:
   - Inspect the Spark UI for task skew
   - Use appropriate partitioning strategies to balance data
   - Implement salting for join operations on skewed keys

3. __Code Optimization__:
   - Review and optimize transformations (prefer narrow over wide)
   - Tune caching strategies for frequently accessed DataFrames
   - Use appropriate file formats (Parquet, Delta) and compression

## Delta Lake Issues

### Delta Lake Transaction Conflicts

__Symptoms__: Transaction conflicts when multiple writers update the same Delta table.

__Possible Causes and Solutions__:

1. __Concurrent Writers__:
   - Implement optimistic concurrency control with retry logic
   - Consider using Delta Lake's optimistic concurrency control features
   - Schedule jobs to avoid concurrent writes to the same table

2. __Long-Running Transactions__:
   - Break down large operations into smaller batches
   - Avoid holding open transactions for extended periods

### Missing Delta Table History

__Symptoms__: Unable to access previous versions of Delta tables.

__Possible Causes and Solutions__:

1. __Vacuum Operations__:
   - Check if aggressive VACUUM commands have removed needed history
   - Adjust retention period in VACUUM commands
   - Use time travel only within the configured retention window

## Serverless SQL Pool Issues

### Cannot Query Delta Tables Directly

__Symptoms__: Error when trying to query Delta tables directly from Serverless SQL.

__Solution__:
Use the OPENROWSET function with the Parquet format, pointing to the Delta table's location, and include the latest file version:

```sql
SELECT TOP 100 *
FROM OPENROWSET(
    BULK 'https://youraccount.dfs.core.windows.net/container/table/_delta_log/*.json',
    FORMAT = 'CSV',
    FIELDTERMINATOR = '|',
    FIELDQUOTE = '',
    ROWTERMINATOR = '0x0b'
) WITH (json_content VARCHAR(8000)) AS [rows]
CROSS APPLY OPENJSON(json_content)
WITH (
    add BIT '$.add',
    path VARCHAR(400) '$.path'
)
WHERE add = 1;
```

## Metadata and Catalog Issues

### Tables Created in Spark Not Visible in SQL

__Symptoms__: Tables created in Spark notebooks don't appear in Serverless SQL.

__Possible Causes and Solutions__:

1. __Metadata Sync Issues__:
   - Ensure tables are created in the proper database/schema
   - Verify the table is registered in the metastore
   - Check for name conflicts or case sensitivity issues

2. __Permissions Problems__:
   - Confirm the SQL user has proper permissions to the storage location
   - Verify storage access using SAS token or managed identity

## Pipeline and Integration Issues

### Pipeline Failures with Integration Datasets

__Symptoms__: Integration pipelines fail when connecting to external sources.

__Possible Causes and Solutions__:

1. __Connectivity Issues__:
   - Check if the linked service configuration is correct
   - Verify network connectivity to external sources
   - Confirm firewall rules allow connections from Azure

2. __Authentication Problems__:
   - Verify credentials in linked services
   - Check for expired secrets or certificates
   - Test connections independently of the pipeline

## Getting Further Help

If you continue experiencing issues after trying these troubleshooting steps, consider the following resources:

1. [Azure Synapse Analytics Documentation](https://learn.microsoft.com/en-us/azure/synapse-analytics/)
2. [Microsoft Q&A for Synapse](https://learn.microsoft.com/en-us/answers/topics/azure-synapse-analytics.html)
3. [Azure Support](https://azure.microsoft.com/en-us/support/create-ticket/)
4. [Stack Overflow - Azure Synapse](https://stackoverflow.com/questions/tagged/azure-synapse)
