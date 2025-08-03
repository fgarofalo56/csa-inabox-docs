# Serverless SQL Examples for Azure Synapse Analytics

[Home](/) > [Code Examples](/docs/code-examples/index.md) > Serverless SQL

This section provides examples and best practices for working with Serverless SQL pools in Azure Synapse Analytics. Serverless SQL pools allow you to query data directly from your data lake storage without the need for data movement or pre-loading.

## Available Examples

### Performance Optimization

- [Query Optimization](query-optimization.md) - Techniques to optimize serverless SQL queries
  - File format selection
  - Column pruning
  - Predicate pushdown
  - Partition elimination
  - External tables and statistics
  - Resource management

## Coming Soon

- **External Tables Management** - Best practices for creating and maintaining external tables
- **Complex Query Patterns** - Solutions for common analytical query scenarios
- **Security and Access Control** - Row-level security and column-level access
- **Data Virtualization** - Creating logical data warehouses using views and stored procedures

## Why Serverless SQL in Azure Synapse?

Serverless SQL pools in Azure Synapse Analytics offer several benefits:

1. **Pay-per-Query**: Only pay for the data processed during query execution
2. **No Infrastructure Management**: Eliminates the need to provision or scale resources
3. **Built-in Security**: Seamless integration with Azure AD and role-based access control
4. **Data Exploration**: Efficiently query and analyze data in various formats
5. **Integration with BI Tools**: Connect with PowerBI and other visualization tools

## Serverless SQL Architecture Patterns

Serverless SQL in Azure Synapse Analytics supports several architecture patterns:

1. **Data Lake Query Engine**: Direct querying of files in storage
2. **Data Virtualization Layer**: Creating views and stored procedures over external data
3. **Hybrid Architecture**: Combining serverless SQL with dedicated SQL pools
4. **Logical Data Warehouse**: Federated queries across multiple data sources

## Related Resources

- [Azure Synapse Analytics Documentation](https://learn.microsoft.com/en-us/azure/synapse-analytics/)
- [Serverless SQL Pool Best Practices](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/best-practices-serverless-sql-pool)
- [T-SQL Reference for Serverless SQL Pools](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/overview-features)
