# Frequently Asked Questions

## General Questions

### What is Azure Synapse Analytics?

Azure Synapse Analytics is an integrated analytics service that brings together data integration, enterprise data warehousing, and big data analytics. It gives you the freedom to query data on your terms, using either serverless or dedicated resources at scale.

### How does Synapse Analytics differ from Azure SQL Data Warehouse?

Azure Synapse Analytics evolved from Azure SQL Data Warehouse, offering all its capabilities plus additional features including integrated Apache Spark, serverless SQL pools, data integration pipelines, and unified management.

### What are the main components of Azure Synapse Analytics?

- SQL pools (dedicated and serverless)
- Apache Spark pools
- Data integration pipelines
- Studio (web-based interface)
- Synapse Link for near real-time analytics

## Delta Lakehouse Questions

### What is a Delta Lakehouse?

A Delta Lakehouse combines the best features of data lakes and data warehouses, using Delta Lake format to provide ACID transactions, schema enforcement, and time travel capabilities on top of your data lake storage.

### What are the advantages of using Delta Lake format?

- ACID transactions
- Schema enforcement and evolution
- Time travel (data versioning)
- Support for batch and streaming data
- Improved query performance with optimized file layout and indexing

### How do I optimize performance with Delta Lake in Synapse?

- Use Z-ordering for frequently queried columns
- Implement regular OPTIMIZE commands to compact small files
- Configure auto-optimize settings for tables with frequent updates
- Use partitioning for large tables that are queried by partition columns

## Serverless SQL Questions

### What is a Serverless SQL pool?

A Serverless SQL pool is an on-demand, scalable compute service that enables you to run SQL queries on data stored in your data lake without the need to provision or manage infrastructure.

### What are the cost benefits of Serverless SQL?

Serverless SQL pools use a pay-per-query model where you're charged based on the data processed rather than provisioned compute resources, making it cost-effective for intermittent or unpredictable workloads.

### What file formats are supported by Serverless SQL?

- Parquet
- CSV
- JSON
- Delta Lake (using OPENROWSET with Parquet)

## Shared Metadata Questions

### How does shared metadata work between Spark and SQL in Synapse?

Azure Synapse Analytics uses a shared metadata model where tables created in Spark can be directly accessed from SQL pools without moving or copying data, using a common metadata store.

### What are the limitations of shared metadata?

- Some data types may have compatibility issues between Spark and SQL
- Three-part naming has specific limitations in both environments
- Some advanced Spark DataFrame operations may not translate directly to SQL

### Can I create views that work across both Spark and SQL?

Yes, you can create views that can be accessed from both environments, but you need to ensure compatible data types and follow naming conventions that work in both contexts.
