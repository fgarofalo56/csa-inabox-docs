# Azure Synapse Analytics Shared Metadata Architecture

[Home](../../README.md) > [Architecture](../architecture/index.md) > Shared Metadata

## Overview

The Shared Metadata architecture in Azure Synapse Analytics provides a unified metadata layer that enables seamless integration between Spark and SQL engines. This powerful capability allows you to define data once and query it from multiple engines, significantly improving productivity and data consistency.

## Architecture Components

![Shared Metadata Architecture](../diagrams/shared-metadata-architecture.png)

### Key Components

- **Metastore**: A unified catalog that stores metadata about databases, tables, and views
- **Database Objects**: Databases, tables, and views that can be accessed from either SQL or Spark
- **Synapse Runtime**: Unified runtime that understands both SQL and Spark semantics
- **Access Control**: Shared security model across query engines

## Features and Capabilities

### Serverless Replicated Databases

Synapse Analytics supports the replication of databases between Spark and SQL pools:

- **Lake Databases**: Created and managed by Spark, accessible from SQL serverless
- **Managed Serverless Databases**: Created from SQL serverless, accessible from Spark
- **Auto-Creation of External Tables**: Automatic creation of external tables in serverless based on Spark tables

### Limitations of Replicated Databases

- Schema changes may not immediately propagate between engines
- Some advanced data types have limited cross-engine compatibility
- Performance characteristics differ between native and cross-engine access

### Three-Part Name Support

#### Spark Database Three-Part Naming

```python
# Python example using three-part naming in Spark
df = spark.sql("SELECT * FROM database_name.schema_name.table_name")
```

Limitations:
- Schema names must follow specific naming conventions
- Some Spark-specific features may not be available when using three-part names

#### SQL Serverless Three-Part Naming

```sql
-- SQL example using three-part naming
SELECT * FROM database_name.schema_name.table_name;
```

Limitations:
- Not all SQL features are available when accessing Spark-created tables
- Performance optimization differs from native SQL tables

### Workarounds for Three-Part Naming in Spark

```python
# Using Spark SQL with database context
spark.sql("USE database_name")
df = spark.sql("SELECT * FROM schema_name.table_name")

# Alternative approach using DataFrame API
df = spark.table("database_name.schema_name.table_name")
```

## Implementation Guidance

### Creating Managed Serverless Databases Using Spark Schema

```sql
-- Create a serverless database from Spark schema
CREATE DATABASE managed_db FROM EXTERNAL DATABASE spark_db;
```

### Auto-Creation of External Tables in Serverless

When you create a table in Spark, it becomes automatically available in SQL serverless:

```python
# Create table in Spark
spark.sql("CREATE TABLE demo_db.sales (id INT, amount DECIMAL(10,2), date DATE) USING DELTA")

# The table is automatically available in SQL serverless
# You can query it using:
# SELECT * FROM demo_db.dbo.sales;
```

### Layered Architecture Best Practices

#### Raw Layer (Bronze)
- Store data in its original format
- Minimal transformations
- Focus on data ingestion speed

#### Processed Layer (Silver)
- Cleansed and conformed data
- Business entity alignment
- Optimized storage formats (Delta)

#### Consumption Layer (Gold)
- Aggregated, enriched data
- Purpose-built for specific use cases
- Optimized for query performance

## Code Examples

For detailed code examples demonstrating shared metadata implementation, see the [code examples section](../code-examples/index.md).

## Best Practices

- Use Delta Lake format for optimal cross-engine compatibility
- Design a consistent naming convention across engines
- Implement proper access control at both storage and Synapse levels
- Consider performance implications when accessing tables across engines

## Related Resources

- [Delta Lakehouse Overview](../architecture/delta-lakehouse-overview.md)
- [Serverless SQL Architecture](../serverless-sql/index.md)
- [Security Best Practices](../best-practices/security.md)

## Next Steps

- Explore [implementation patterns](../best-practices/implementation-patterns.md)
- Review [performance optimization guidelines](../best-practices/performance.md)
- Learn about [data governance practices](../best-practices/data-governance.md)
