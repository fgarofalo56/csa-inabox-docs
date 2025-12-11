# Serverless SQL Guide

> **[Home](README.md)** | **Serverless SQL Guide**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Service](https://img.shields.io/badge/Service-Synapse%20Serverless-purple?style=flat-square)

Comprehensive guide to Azure Synapse Serverless SQL pools.

---

## Overview

Serverless SQL pool is a query service over data in your data lake. Key benefits:

- **Pay-per-query** - Only pay for data processed
- **No infrastructure** - No clusters to manage
- **T-SQL interface** - Standard SQL for data exploration
- **Built-in formats** - Parquet, Delta Lake, CSV, JSON support

---

## Getting Started

### Query Parquet Files

```sql
-- Query Parquet files directly
SELECT TOP 100 *
FROM OPENROWSET(
    BULK 'https://storage.dfs.core.windows.net/container/data/*.parquet',
    FORMAT = 'PARQUET'
) AS rows;

-- With explicit schema
SELECT
    customer_id,
    customer_name,
    region,
    total_purchases
FROM OPENROWSET(
    BULK 'https://storage.dfs.core.windows.net/container/customers/*.parquet',
    FORMAT = 'PARQUET'
) WITH (
    customer_id INT,
    customer_name VARCHAR(100),
    region VARCHAR(50),
    total_purchases DECIMAL(10,2)
) AS customers
WHERE region = 'North';
```

---

## Query Delta Lake

### Basic Delta Query

```sql
-- Query Delta Lake table
SELECT *
FROM OPENROWSET(
    BULK 'https://storage.dfs.core.windows.net/container/delta/customers/',
    FORMAT = 'DELTA'
) AS delta_data;

-- Time travel with Delta
SELECT *
FROM OPENROWSET(
    BULK 'https://storage.dfs.core.windows.net/container/delta/customers/',
    FORMAT = 'DELTA'
) AS delta_data
OPTION (TIMESTAMP AS OF '2024-01-15T00:00:00');
```

---

## External Tables

### Create External Data Source

```sql
-- Create database
CREATE DATABASE analytics;
GO
USE analytics;
GO

-- Create credentials
CREATE DATABASE SCOPED CREDENTIAL StorageCredential
WITH IDENTITY = 'Managed Identity';

-- Create external data source
CREATE EXTERNAL DATA SOURCE DataLake
WITH (
    LOCATION = 'https://storage.dfs.core.windows.net/container',
    CREDENTIAL = StorageCredential
);

-- Create external file format
CREATE EXTERNAL FILE FORMAT ParquetFormat
WITH (
    FORMAT_TYPE = PARQUET,
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
);
```

### Create External Table

```sql
-- External table over Parquet
CREATE EXTERNAL TABLE customers (
    customer_id INT,
    customer_name VARCHAR(100),
    email VARCHAR(200),
    region VARCHAR(50),
    created_date DATE
)
WITH (
    LOCATION = '/bronze/customers/',
    DATA_SOURCE = DataLake,
    FILE_FORMAT = ParquetFormat
);

-- External table over Delta Lake
CREATE EXTERNAL TABLE orders
WITH (
    LOCATION = '/silver/orders/',
    DATA_SOURCE = DataLake,
    FILE_FORMAT = DeltaLakeFormat
);

-- Query like regular table
SELECT c.customer_name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_name;
```

---

## Views for Abstraction

### Create Views

```sql
-- Create view for data abstraction
CREATE VIEW vw_active_customers AS
SELECT
    customer_id,
    customer_name,
    email,
    region,
    created_date,
    DATEDIFF(day, created_date, GETDATE()) as tenure_days
FROM OPENROWSET(
    BULK 'https://storage.dfs.core.windows.net/container/customers/*.parquet',
    FORMAT = 'PARQUET'
) WITH (
    customer_id INT,
    customer_name VARCHAR(100),
    email VARCHAR(200),
    region VARCHAR(50),
    created_date DATE,
    is_active BIT
) AS customers
WHERE is_active = 1;

-- Use view
SELECT region, COUNT(*) as customer_count
FROM vw_active_customers
GROUP BY region;
```

---

## Partitioned Data

### Query Partitioned Data

```sql
-- Query partitioned Parquet (year/month/day structure)
SELECT
    r.filepath(1) AS year,
    r.filepath(2) AS month,
    COUNT(*) as record_count,
    SUM(amount) as total_amount
FROM OPENROWSET(
    BULK 'https://storage.dfs.core.windows.net/container/sales/year=*/month=*/*.parquet',
    FORMAT = 'PARQUET'
) AS r
GROUP BY r.filepath(1), r.filepath(2)
ORDER BY year, month;

-- Partition pruning (filter pushdown)
SELECT *
FROM OPENROWSET(
    BULK 'https://storage.dfs.core.windows.net/container/sales/year=*/month=*/*.parquet',
    FORMAT = 'PARQUET'
) AS r
WHERE r.filepath(1) = '2024' AND r.filepath(2) = '01';
```

---

## Query CSV and JSON

### CSV Files

```sql
-- Query CSV with headers
SELECT *
FROM OPENROWSET(
    BULK 'https://storage.dfs.core.windows.net/container/data/file.csv',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n'
) AS csv_data;

-- Explicit schema for CSV
SELECT *
FROM OPENROWSET(
    BULK 'https://storage.dfs.core.windows.net/container/data/*.csv',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    FIRSTROW = 2
) WITH (
    id INT 1,
    name VARCHAR(100) 2,
    value DECIMAL(10,2) 3
) AS csv_data;
```

### JSON Files

```sql
-- Query JSON
SELECT
    JSON_VALUE(doc, '$.id') AS id,
    JSON_VALUE(doc, '$.name') AS name,
    JSON_VALUE(doc, '$.details.category') AS category
FROM OPENROWSET(
    BULK 'https://storage.dfs.core.windows.net/container/data/*.json',
    FORMAT = 'CSV',
    FIELDQUOTE = '0x0b',
    FIELDTERMINATOR = '0x0b',
    ROWTERMINATOR = '\n'
) WITH (doc NVARCHAR(MAX)) AS json_data;

-- Query JSON Lines (JSONL)
SELECT
    JSON_VALUE(jsonContent, '$.event_type') as event_type,
    JSON_VALUE(jsonContent, '$.timestamp') as event_time,
    JSON_QUERY(jsonContent, '$.properties') as properties
FROM OPENROWSET(
    BULK 'https://storage.dfs.core.windows.net/container/events/*.jsonl',
    FORMAT = 'CSV',
    FIELDQUOTE = '0x0b',
    FIELDTERMINATOR = '0x0b'
) WITH (jsonContent NVARCHAR(MAX)) AS events;
```

---

## Performance Optimization

### Best Practices

```sql
-- Use column projection
SELECT customer_id, customer_name  -- Only needed columns
FROM OPENROWSET(...) AS data;

-- Filter early with WHERE
SELECT *
FROM OPENROWSET(
    BULK 'https://storage.dfs.core.windows.net/container/sales/year=2024/*.parquet',
    FORMAT = 'PARQUET'
) AS sales
WHERE region = 'North';  -- Pushed down to storage

-- Use statistics for complex queries
CREATE STATISTICS customer_region_stats
ON customers (region)
WITH FULLSCAN;
```

### Cost Control

```sql
-- Monitor data processed
SELECT
    start_time,
    end_time,
    data_processed_mb,
    error_id,
    request_id
FROM sys.dm_exec_requests_history
WHERE start_time > DATEADD(hour, -24, GETDATE())
ORDER BY data_processed_mb DESC;

-- Set cost control
ALTER DATABASE analytics
SET DATA_PROCESSED_MB_MAX = 10000;  -- 10 GB limit
```

---

## Security

### Row-Level Security

```sql
-- Create security policy
CREATE SCHEMA Security;
GO

CREATE FUNCTION Security.fn_securitypredicate(@region AS VARCHAR(50))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS result
WHERE @region = USER_NAME()
   OR USER_NAME() = 'admin';
GO

CREATE SECURITY POLICY RegionFilter
ADD FILTER PREDICATE Security.fn_securitypredicate(region)
ON dbo.customers;
```

### Column-Level Security

```sql
-- Mask sensitive columns
CREATE VIEW vw_customers_masked AS
SELECT
    customer_id,
    customer_name,
    CONCAT(LEFT(email, 2), '***@', SUBSTRING(email, CHARINDEX('@', email) + 1, 100)) as email_masked,
    region
FROM customers;
```

---

## Related Documentation

- [Serverless SQL Code Examples](code-examples/serverless-sql/README.md)
- [Serverless SQL Architecture](architecture/serverless-sql/README.md)
- [Serverless SQL Best Practices](best-practices/serverless-sql-best-practices/README.md)

---

*Last Updated: January 2025*
