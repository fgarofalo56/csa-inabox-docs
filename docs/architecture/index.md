[Home](../../README.md) > Architecture

# Azure Synapse Analytics Architecture

This section provides detailed architectural documentation for Azure Synapse Analytics components, focusing on two primary areas:

## Architecture Components

Azure Synapse Analytics offers multiple computation models to support various data processing and analytics scenarios:

### Delta Lakehouse

Delta Lakehouse architecture combines the best of data lakes and data warehouses, providing an open-format storage layer with ACID transactions, schema enforcement, and data versioning capabilities.

- [Delta Lakehouse Overview](./delta-lakehouse-overview.md) - Introduction to the Delta Lakehouse pattern in Azure Synapse

### Serverless SQL

Serverless SQL architecture allows you to query data directly in your data lake without moving or copying data, using familiar T-SQL syntax.

- [Serverless SQL Overview](./serverless-sql/serverless-overview.md) - Introduction to Serverless SQL capabilities

### Shared Metadata

Shared metadata architecture enables seamless integration between different compute engines while maintaining a single source of truth for your data.

- [Shared Metadata Architecture](./shared-metadata/index.md) - Overview of the shared metadata capabilities and integration points

## Related Resources

- [Best Practices](../best-practices/index.md) - Recommendations for optimizing your Synapse implementation
- [Code Examples](../code-examples/index.md) - Practical code samples for implementation
- [Reference Guides](../reference/index.md) - Technical reference documentation
