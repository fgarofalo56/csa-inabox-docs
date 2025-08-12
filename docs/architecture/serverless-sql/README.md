# Serverless SQL Architecture

[Home](../../) > [Architecture](../) > Serverless SQL

Serverless SQL architecture in Azure Synapse Analytics allows you to query data directly in your data lake without moving or copying data, using familiar T-SQL syntax.

## Documentation

- [Serverless SQL Overview](./serverless-overview.md) - Introduction to Serverless SQL capabilities
- [Detailed Architecture](./detailed-architecture.md) - Comprehensive technical architecture of Serverless SQL implementation

## Key Features

- On-demand querying with no infrastructure to manage
- Pay-per-query cost model
- T-SQL compatibility
- Native integration with Azure Data Lake Storage
- Built-in data virtualization
- Seamless integration with visualization tools

## Architecture Overview

![Azure Synapse SQL Architecture](https://learn.microsoft.com/en-us/azure/synapse-analytics/media/overview-architecture/sql-architecture.png)

Serverless SQL pools in Azure Synapse Analytics provide a serverless distributed query processing engine for big data analytics. The architecture is designed to support on-demand query execution over data stored in your data lake without the need to manage infrastructure.

## Implementation Considerations

### Data Organization

Organize your data lake with a clear folder structure to optimize query performance:

```
adls://data/
├── raw/
├── curated/
│   ├── dimensions/
│   └── facts/
└── external/
```

### File Formats and Optimization

For best performance with Serverless SQL:

- Use Parquet for columnar storage benefits
- Partition large datasets appropriately
- Create statistics on frequently queried columns
- Use external tables with OPENROWSET for flexibility

## Related Resources

- [Best Practices for Serverless SQL](../../best-practices/#serverless-sql)
- [Serverless SQL Guide](../../code-examples/serverless-sql-guide.md)
- [Performance Optimization](../../best-practices/performance.md)
- [Cost Management](../../best-practices/cost-optimization.md)
