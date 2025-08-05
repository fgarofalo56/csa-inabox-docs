# Shared Metadata Architecture

## Overview

The Shared Metadata Architecture in Azure Synapse Analytics enables a unified semantic layer across different compute engines, allowing consistent data access, governance, and business logic implementation regardless of the query engine used. This approach reduces redundancy, improves maintainability, and provides a consistent view of enterprise data.

## Architecture Components

![Shared Metadata Architecture](../assets/images/shared-metadata-architecture.png)

### Core Components

1. __Azure Synapse Analytics Workspace__
   - Central hub for all analytics activities
   - Integration point for different compute engines
   - Management of shared metadata artifacts

2. __Synapse SQL Pools (Dedicated and Serverless)__
   - T-SQL interface for data access
   - Support for external tables over data lake
   - View definitions for logical data modeling

3. __Synapse Spark Pools__
   - Apache Spark processing engine
   - Support for Delta, Parquet, and other formats
   - Integration with SQL through SparkSQL

4. __Azure Data Lake Storage Gen2__
   - Common storage layer for all data
   - Support for POSIX-compliant ACLs
   - Hierarchical namespace for organization

5. __Metadata Services__
   - Synapse Workspace Metadata
   - Azure Purview for cataloging and lineage
   - Git integration for metadata version control

## Implementation Patterns

### Cross-Engine Table Definitions

#### SQL External Tables

```sql
-- Create a database scoped credential for accessing ADLS
CREATE DATABASE SCOPED CREDENTIAL [ADLSCredential]
WITH
    IDENTITY = 'Managed Service Identity';

-- Create an external data source
CREATE EXTERNAL DATA SOURCE [DataLake]
WITH (
    LOCATION = 'abfss://data@youraccount.dfs.core.windows.net',
    CREDENTIAL = [ADLSCredential]
);

-- Create an external file format
CREATE EXTERNAL FILE FORMAT [ParquetFormat]
WITH (
    FORMAT_TYPE = PARQUET,
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
);

-- Create an external table
CREATE EXTERNAL TABLE [dbo].[Customer] (
    [CustomerId] INT,
    [Name] NVARCHAR(100),
    [Email] NVARCHAR(100),
    [RegistrationDate] DATETIME2
)
WITH (
    LOCATION = '/curated/customers/',
    DATA_SOURCE = [DataLake],
    FILE_FORMAT = [ParquetFormat]
);
```

#### Spark DataFrame Access

```python
# Access the same table from Spark
df = spark.read.format("delta").load("abfss://data@youraccount.dfs.core.windows.net/curated/customers/")

# Register as a temp view for SparkSQL access
df.createOrReplaceTempView("Customer")

# Query using SparkSQL
sparkDF = spark.sql("SELECT CustomerId, Name, Email FROM Customer WHERE RegistrationDate > '2023-01-01'")
```

### Unified Semantic Layer

#### SQL Views for Business Logic

```sql
-- Create a business view that can be accessed from multiple engines
CREATE VIEW [dbo].[CustomerSummary] AS
SELECT
    c.[CustomerId],
    c.[Name],
    c.[Email],
    c.[RegistrationDate],
    COUNT(o.[OrderId]) AS [TotalOrders],
    SUM(o.[OrderAmount]) AS [TotalSpend],
    DATEDIFF(day, c.[RegistrationDate], GETDATE()) AS [CustomerAgeInDays]
FROM [dbo].[Customer] c
LEFT JOIN [dbo].[Order] o ON c.[CustomerId] = o.[CustomerId]
GROUP BY c.[CustomerId], c.[Name], c.[Email], c.[RegistrationDate];
```

#### Spark to SQL View Access

```python
# Access SQL views from Spark using JDBC connector
server_name = "mysynapseworkspace-ondemand.sql.azuresynapse.net"
database_name = "MetadataDB"

customer_summary = spark.read \
    .format("com.microsoft.sqlserver.jdbc.spark") \
    .option("url", f"jdbc:sqlserver://{server_name}:1433;database={database_name}") \
    .option("query", "SELECT * FROM [dbo].[CustomerSummary]") \
    .option("authentication", "ActiveDirectoryMSI") \
    .option("encrypt", "true") \
    .option("trustServerCertificate", "false") \
    .load()
```

## Metadata Synchronization Patterns

### Schema Propagation

1. __Source of Truth Approach__
   - Designate one system (typically SQL) as the schema authority
   - Automate schema propagation to other engines
   - Use tools like Azure Data Factory or Synapse Pipelines for orchestration

2. __Schema Evolution Handling__
   - Implement version control for schema changes
   - Use schema compatibility modes in Delta Lake
   - Automate testing of schema compatibility

### Metadata Management

1. __Azure Purview Integration__
   - Central catalog for data assets
   - Automated scanning and classification
   - Lineage tracking across engines
   - Business glossary integration

2. __Custom Metadata Registry__
   - Create a metadata registry database
   - Track schema versions and changes
   - Store engine-specific optimizations

## Security Implementation

### Unified Security Model

```sql
-- Implement Row-Level Security
CREATE SECURITY POLICY [CustomerPolicy]
ADD FILTER PREDICATE [dbo].[fn_securitypredicate]([TenantId])
ON [dbo].[Customer];

-- Column-Level Security
GRANT SELECT ON [dbo].[Customer]([CustomerId], [Name]) TO [Analysts];
GRANT SELECT ON [dbo].[Customer]([Email]) TO [MarketingTeam];
```

### Synapse Workspace Permissions

- Workspace-level roles (Admin, Contributor, User)
- SQL permissions for database objects
- Spark pool permissions for notebooks and jobs
- Integration runtime permissions for pipelines

## Performance Optimization

### Cross-Engine Query Optimization

1. __Dedicated SQL Pool Optimizations__
   - Distribution keys aligned with join columns
   - Partition aligned with filtering patterns
   - Statistics maintenance

2. __Serverless SQL Optimizations__
   - Optimal file formats (Parquet/Delta)
   - Partition elimination strategies
   - File size optimization

3. __Spark Optimizations__
   - Spark configuration tuning
   - Broadcast joins for dimension tables
   - Partition pruning through predicate pushdown

## Common Use Cases

### Enterprise Data Warehouse Modernization

1. __Hybrid Approach__
   - Keep core EDW workloads in Dedicated SQL Pool
   - Use Spark for data preparation and ML
   - Use Serverless SQL for ad-hoc exploration
   - Maintain consistent business definitions across all engines

2. __Migration Pattern__
   - Start with shared metadata layer
   - Gradually migrate workloads to appropriate engines
   - Maintain backward compatibility

### Advanced Analytics Integration

1. __Machine Learning Pipeline__
   - Feature engineering in SQL or Spark
   - Model training in Spark
   - Model scoring in SQL or Spark
   - Consistent data access across pipeline stages

2. __Real-time Analytics__
   - Stream processing in Spark
   - Serving layer in SQL
   - Shared schema definitions

## DevOps and Governance

1. __CI/CD for Metadata__
   - Source control for all metadata definitions
   - Automated testing for cross-engine compatibility
   - Deployment pipelines for metadata changes

2. __Monitoring and Observability__
   - Track query performance across engines
   - Monitor metadata usage patterns
   - Audit access to sensitive data

## Best Practices

1. __Design for Compatibility__
   - Use data types supported across engines
   - Avoid engine-specific SQL extensions where possible
   - Document engine-specific behaviors

2. __Implement Data Governance Early__
   - Define data ownership and stewardship
   - Establish metadata management practices
   - Automate compliance and quality checks

3. __Balance Flexibility and Control__
   - Allow specialized optimizations per engine
   - Maintain core business logic consistency
   - Enable self-service while ensuring governance

4. __Optimize for Performance__
   - Profile workloads across engines
   - Apply engine-specific optimizations
   - Use appropriate compute for each workload type
