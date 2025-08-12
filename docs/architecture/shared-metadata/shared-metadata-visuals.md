# Azure Synapse Shared Metadata Architecture - Visual Guides

[Home](/README.md) > [Architecture](../README.md) > [Shared Metadata](README.md) > Visual Guides

## Serverless Replicated Database Synchronization

```mermaid
sequenceDiagram
    participant Spark as Apache Spark Pool
    participant MetaStore as Spark Metastore
    participant SyncService as Metadata Sync Service
    participant SQLPool as Serverless SQL Pool
    
    Spark->>MetaStore: Create database (mydb)
    MetaStore-->>Spark: Database created
    Note over MetaStore: Database stored in metastore
    MetaStore->>SyncService: Notify new database
    SyncService->>SQLPool: Create corresponding database
    Note over SQLPool: Database 'mydb' created in SQL Pool
    
    Spark->>MetaStore: Create table (mydb.mytable) USING PARQUET
    MetaStore-->>Spark: Table created
    Note over MetaStore: Table metadata stored in metastore
    MetaStore->>SyncService: Notify new table
    SyncService->>SQLPool: Create external table
    Note over SQLPool: External table 'mydb.dbo.mytable' created
    
    Spark->>MetaStore: Update table schema
    MetaStore-->>Spark: Schema updated
    MetaStore->>SyncService: Notify schema change
    SyncService->>SQLPool: Update external table schema
    Note over SQLPool: External table schema updated (async)
```

## Three-Part Naming Limitations and Workarounds

```mermaid
graph TD
    subgraph "Spark Environment"
        SparkDB1[Spark Database 1]
        SparkDB2[Spark Database 2]
        SparkTable1[Table 1 - Parquet]
        SparkTable2[Table 2 - Delta]
        SparkTable3[Table 3 - CSV]
        SparkTable4[Table 4 - JSON]
        SparkView[Spark View]
        
        SparkDB1 --> SparkTable1
        SparkDB1 --> SparkTable2
        SparkDB2 --> SparkTable3
        SparkDB2 --> SparkTable4
        SparkDB1 --> SparkView
    end
    
    subgraph "Serverless SQL Environment"
        SQLDB1[SQL Database 1]
        SQLDB2[SQL Database 2]
        SQLTable1[External Table 1]
        SQLTable2[External Table 2]
        SQLTable3[External Table 3]
        
        SQLDB1 --> SQLTable1
        SQLDB1 --> SQLTable2
        SQLDB2 --> SQLTable3
    end
    
    %% Sync relationships
    SparkTable1 -.Sync.-> SQLTable1
    SparkTable2 -.Sync.-> SQLTable2
    SparkTable3 -.Sync.-> SQLTable3
    
    %% Not synced
    SparkTable4 -. Not Synced .-> Limitations([JSON format not supported])
    SparkView -. Not Synced .-> Limitations2([Views require Spark engine])
    
    %% Three-part naming
    ThreePart[Three-part naming: database.schema.table]
    ThreePart --> SQLAccess[SQL: USE database; SELECT * FROM schema.table]
    ThreePart --> SparkAccess[Spark: SELECT * FROM database.table]
    
    %% Workaround
    Workaround[Workaround Pattern]
    Workaround --> Step1[1. Create tables in Spark with supported formats]
    Step1 --> Step2[2. Let tables sync to serverless SQL]
    Step2 --> Step3[3. Use database.dbo.table in SQL queries]
```

## Layered Data Architecture with Shared Metadata

![Azure Synapse SQL Architecture](https://learn.microsoft.com/en-us/azure/synapse-analytics/media/overview-architecture/sql-architecture.png)


## Creating and Accessing Synchronized Tables - Process Flow

![Azure Synapse SQL Architecture](https://learn.microsoft.com/en-us/azure/synapse-analytics/media/overview-architecture/sql-architecture.png)

