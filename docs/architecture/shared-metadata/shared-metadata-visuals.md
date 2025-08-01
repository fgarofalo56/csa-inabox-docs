# Azure Synapse Shared Metadata Architecture - Visual Guides

[Home](/README.md) > [Architecture](../index.md) > [Shared Metadata](index.md) > Visual Guides

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

```mermaid
graph TD
    Storage[ADLS Gen2 Storage]
    
    subgraph "Data Layers"
        Raw[Raw Layer]
        Silver[Silver/Curated Layer]
        Gold[Gold/Business Layer]
        
        Storage --> Raw
        Raw --> Silver
        Silver --> Gold
    end
    
    subgraph "Engine Access Patterns"
        SparkRaw[Direct Spark access]
        SQLRaw[Direct SQL access]
        
        SparkSilver[Spark with metadata sync]
        SQLSilver[SQL with metadata sync]
        
        SparkGold[Full shared metadata]
        SQLGold[Full shared metadata]
        
        Raw --> SparkRaw
        Raw --> SQLRaw
        
        Silver --> SparkSilver
        Silver --> SQLSilver
        
        Gold --> SparkGold
        Gold --> SQLGold
    end
    
    subgraph "Recommendations"
        RecRaw[Minimal shared metadata]
        RecSilver[Begin applying shared metadata]
        RecGold[Fully leverage shared metadata]
        
        SparkRaw --> RecRaw
        SQLRaw --> RecRaw
        
        SparkSilver --> RecSilver
        SQLSilver --> RecSilver
        
        SparkGold --> RecGold
        SQLGold --> RecGold
    end
```

## Creating and Accessing Synchronized Tables - Process Flow

```mermaid
flowchart TD
    Start([Start]) --> CreateDB[Create Database in Spark]
    CreateDB --> CreateTable[Create Table in Spark using Parquet/Delta/CSV]
    CreateTable --> InsertData[Insert Data in Spark]
    InsertData --> Wait[Wait for Async Sync ~few seconds]
    Wait --> QuerySQL[Query from Serverless SQL Pool]
    
    QuerySQL --> UseCase1[Use Case: Analytics]
    QuerySQL --> UseCase2[Use Case: Reporting]
    QuerySQL --> UseCase3[Use Case: Data Exploration]
    
    subgraph "Code Examples"
        SparkCode["
        // Spark SQL
        CREATE DATABASE mydb;
        
        CREATE TABLE mydb.sales (
            id INT,
            date DATE,
            amount DOUBLE,
            customer STRING
        ) USING PARQUET;
        
        INSERT INTO mydb.sales 
        VALUES (1, '2023-01-15', 199.99, 'Contoso');
        "]
        
        SQLCode["
        -- Serverless SQL Pool
        USE mydb;
        
        -- View available tables
        SELECT * FROM sys.tables;
        
        -- Query synchronized table
        SELECT * FROM mydb.dbo.sales
        WHERE date >= '2023-01-01';
        "]
    end
    
    UseCase1 --> SparkCode
    UseCase2 --> SQLCode
```
