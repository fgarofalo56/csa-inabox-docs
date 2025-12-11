# Synapse Migration Tutorial

> **[Home](../../README.md)** | **[Tutorials](../README.md)** | **Synapse Migration**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Level](https://img.shields.io/badge/Level-Advanced-red?style=flat-square)

Complete guide to migrating data warehouses to Azure Synapse.

---

## Overview

This tutorial covers:

- Migration assessment
- Schema migration
- Data migration strategies
- Validation and cutover

**Duration**: Multi-week project | **Prerequisites**: Source DW access, Azure Synapse workspace

---

## Migration Approaches

| Source | Recommended Approach | Complexity |
|--------|---------------------|------------|
| SQL Server DW | Direct migration | Medium |
| Oracle | Schema conversion + ADF | High |
| Teradata | Azure Migrate + ADF | High |
| Netezza | Schema conversion + ADF | High |
| Redshift | Schema conversion + ADF | Medium |

---

## Phase 1: Assessment

### Database Assessment

```python
# Assessment script for source database
def assess_database(connection_string):
    """Comprehensive database assessment."""

    assessment = {
        "database_info": {},
        "tables": [],
        "stored_procedures": [],
        "compatibility_issues": [],
        "recommendations": []
    }

    # Get database size
    cursor.execute("""
        SELECT
            SUM(size * 8 / 1024) AS size_mb
        FROM sys.database_files
    """)
    assessment["database_info"]["size_mb"] = cursor.fetchone()[0]

    # Get table inventory
    cursor.execute("""
        SELECT
            t.name AS table_name,
            SUM(p.rows) AS row_count,
            SUM(a.total_pages * 8 / 1024) AS size_mb
        FROM sys.tables t
        JOIN sys.partitions p ON t.object_id = p.object_id
        JOIN sys.allocation_units a ON p.partition_id = a.container_id
        GROUP BY t.name
    """)
    assessment["tables"] = cursor.fetchall()

    # Check for incompatible features
    assessment["compatibility_issues"] = check_compatibility()

    return assessment

def check_compatibility():
    """Check for Synapse-incompatible features."""

    issues = []

    # Check for unsupported data types
    cursor.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE data_type IN ('xml', 'geography', 'geometry', 'hierarchyid')
    """)
    for row in cursor.fetchall():
        issues.append({
            "type": "UNSUPPORTED_DATATYPE",
            "table": row[0],
            "column": row[1],
            "data_type": row[2]
        })

    return issues
```

### Sizing Recommendation

```python
def recommend_synapse_size(assessment):
    """Recommend Synapse configuration based on assessment."""

    size_gb = assessment["database_info"]["size_mb"] / 1024
    total_rows = sum(t["row_count"] for t in assessment["tables"])

    if size_gb < 250:
        return {"type": "Serverless SQL", "reason": "Small dataset, ad-hoc queries"}
    elif size_gb < 1000:
        return {"type": "Dedicated SQL DW1000c", "reason": "Medium dataset"}
    elif size_gb < 10000:
        return {"type": "Dedicated SQL DW3000c", "reason": "Large dataset"}
    else:
        return {"type": "Dedicated SQL DW6000c+", "reason": "Very large dataset"}
```

---

## Phase 2: Schema Migration

### Schema Conversion

```sql
-- Source: SQL Server
CREATE TABLE dbo.FactSales (
    SalesKey INT IDENTITY(1,1) PRIMARY KEY,
    DateKey INT NOT NULL,
    CustomerKey INT NOT NULL,
    ProductKey INT NOT NULL,
    Quantity INT,
    Amount DECIMAL(18,2),
    CONSTRAINT FK_Date FOREIGN KEY (DateKey) REFERENCES DimDate(DateKey)
);

-- Target: Synapse Dedicated SQL
CREATE TABLE dbo.FactSales (
    SalesKey INT NOT NULL,  -- No IDENTITY, use CTAS or sequence
    DateKey INT NOT NULL,
    CustomerKey INT NOT NULL,
    ProductKey INT NOT NULL,
    Quantity INT,
    Amount DECIMAL(18,2)
)
WITH (
    DISTRIBUTION = HASH(CustomerKey),  -- Choose distribution key
    CLUSTERED COLUMNSTORE INDEX,       -- Columnstore for analytics
    PARTITION (DateKey RANGE RIGHT FOR VALUES (
        20230101, 20240101, 20250101
    ))
);

-- Note: Foreign keys not enforced in Synapse (metadata only)
```

### Data Type Mappings

| Source Type | Synapse Type | Notes |
|-------------|--------------|-------|
| INT IDENTITY | INT | Use sequences or CTAS |
| DATETIME | DATETIME2 | Better precision |
| VARCHAR(MAX) | VARCHAR(8000) | Max limit |
| XML | VARCHAR(MAX) | Convert to JSON/string |
| GEOGRAPHY | VARCHAR | Store as WKT string |

---

## Phase 3: Data Migration

### Using Azure Data Factory

```json
{
    "name": "MigrateFactSales",
    "properties": {
        "activities": [
            {
                "name": "CopyFactSales",
                "type": "Copy",
                "inputs": [{"referenceName": "SourceSQLServer", "type": "DatasetReference"}],
                "outputs": [{"referenceName": "SynapseFactSales", "type": "DatasetReference"}],
                "typeProperties": {
                    "source": {
                        "type": "SqlServerSource",
                        "sqlReaderQuery": "SELECT * FROM dbo.FactSales WHERE DateKey >= 20200101"
                    },
                    "sink": {
                        "type": "SqlDWSink",
                        "allowPolyBase": true,
                        "polyBaseSettings": {
                            "rejectType": "percentage",
                            "rejectValue": 0,
                            "rejectSampleValue": 100
                        }
                    },
                    "enableStaging": true,
                    "stagingSettings": {
                        "linkedServiceName": {
                            "referenceName": "AzureBlobStorage",
                            "type": "LinkedServiceReference"
                        },
                        "path": "staging/factsales"
                    }
                }
            }
        ]
    }
}
```

### Incremental Migration

```python
# Incremental migration with watermark
def migrate_incrementally(table_name, watermark_column, batch_size=1000000):
    """Migrate data incrementally using watermark."""

    # Get current watermark
    last_watermark = get_watermark(table_name)

    while True:
        # Get next batch
        query = f"""
            SELECT TOP {batch_size} *
            FROM {table_name}
            WHERE {watermark_column} > '{last_watermark}'
            ORDER BY {watermark_column}
        """

        batch_df = read_source(query)

        if batch_df.empty:
            break

        # Load to Synapse
        load_to_synapse(batch_df, table_name)

        # Update watermark
        last_watermark = batch_df[watermark_column].max()
        update_watermark(table_name, last_watermark)

        print(f"Migrated batch up to {last_watermark}")
```

---

## Phase 4: Validation

### Data Validation Queries

```sql
-- Row count comparison
SELECT 'Source' AS System, COUNT(*) AS RowCount FROM SourceDB.dbo.FactSales
UNION ALL
SELECT 'Target', COUNT(*) FROM SynapseDB.dbo.FactSales;

-- Aggregate comparison
SELECT
    'Source' AS System,
    SUM(Amount) AS TotalAmount,
    AVG(Amount) AS AvgAmount,
    COUNT(DISTINCT CustomerKey) AS UniqueCustomers
FROM SourceDB.dbo.FactSales
UNION ALL
SELECT
    'Target',
    SUM(Amount),
    AVG(Amount),
    COUNT(DISTINCT CustomerKey)
FROM SynapseDB.dbo.FactSales;

-- Sample data comparison
SELECT TOP 100 *
FROM SourceDB.dbo.FactSales
EXCEPT
SELECT TOP 100 *
FROM SynapseDB.dbo.FactSales;
```

---

## Phase 5: Cutover

### Cutover Checklist

- [ ] All data migrated and validated
- [ ] Stored procedures converted
- [ ] Reports connected to Synapse
- [ ] Performance baseline established
- [ ] Rollback plan documented
- [ ] Monitoring configured
- [ ] Users trained

### Post-Cutover Tasks

```sql
-- Update statistics
EXEC sp_updatestats;

-- Create result set cache
ALTER DATABASE SynapseDB SET RESULT_SET_CACHING ON;

-- Monitor initial queries
SELECT TOP 20
    request_id,
    command,
    total_elapsed_time,
    resource_class
FROM sys.dm_pdw_exec_requests
WHERE status = 'Completed'
ORDER BY total_elapsed_time DESC;
```

---

## Related Documentation

- [Migration Strategies](../../best-practices/migration-strategies.md)
- [Data Factory Tutorials](../data-factory/README.md)
- [SQL Performance](../../best-practices/sql-performance/README.md)

---

*Last Updated: January 2025*
