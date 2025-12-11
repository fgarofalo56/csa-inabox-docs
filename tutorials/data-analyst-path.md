# Data Analyst Learning Path

> **[Home](../README.md)** | **[Tutorials](README.md)** | **Data Analyst Path**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Level](https://img.shields.io/badge/Level-Beginner_to_Intermediate-blue?style=flat-square)

Complete learning path for Data Analysts using Cloud Scale Analytics.

---

## Overview

This learning path covers:

- Querying data with Serverless SQL
- Building reports with Power BI
- Data exploration and visualization
- Self-service analytics

**Duration**: 4-6 weeks | **Prerequisites**: Basic SQL knowledge

---

## Learning Modules

### Module 1: Platform Fundamentals (Week 1)

| Topic | Duration | Resources |
|-------|----------|-----------|
| Azure Synapse Overview | 2 hours | [Synapse Fundamentals](synapse/README.md) |
| Data Lake Concepts | 1 hour | [Data Lake Architecture](../docs/architecture/delta-lakehouse/README.md) |
| Security Basics | 1 hour | [Security Overview](../docs/reference/security/README.md) |

**Hands-on Lab:**
```sql
-- Connect to Serverless SQL and explore data
SELECT TOP 100 *
FROM OPENROWSET(
    BULK 'https://storage.dfs.core.windows.net/sample-data/*.parquet',
    FORMAT = 'PARQUET'
) AS sample_data;
```

---

### Module 2: Serverless SQL Mastery (Week 2)

| Topic | Duration | Resources |
|-------|----------|-----------|
| OPENROWSET Queries | 2 hours | [Serverless SQL Guide](../docs/code-examples/serverless-sql/README.md) |
| External Tables | 2 hours | [External Tables](../docs/02-services/analytics-compute/azure-synapse/serverless-sql/README.md) |
| Query Optimization | 2 hours | [SQL Best Practices](../best-practices/serverless-sql-best-practices/README.md) |

**Hands-on Lab:**
```sql
-- Create database and external data sources
CREATE DATABASE analytics;
GO

USE analytics;
GO

CREATE EXTERNAL DATA SOURCE DataLake
WITH (
    LOCATION = 'https://storage.dfs.core.windows.net/data/'
);

-- Create view for self-service queries
CREATE VIEW dbo.vw_SalesSummary AS
SELECT
    YEAR(OrderDate) AS Year,
    MONTH(OrderDate) AS Month,
    ProductCategory,
    SUM(Amount) AS TotalSales,
    COUNT(*) AS OrderCount
FROM OPENROWSET(
    BULK 'sales/**/*.parquet',
    DATA_SOURCE = 'DataLake',
    FORMAT = 'PARQUET'
) AS sales
GROUP BY YEAR(OrderDate), MONTH(OrderDate), ProductCategory;
```

---

### Module 3: Power BI Integration (Week 3)

| Topic | Duration | Resources |
|-------|----------|-----------|
| DirectQuery Setup | 2 hours | [Power BI Integration](integration/power-bi/README.md) |
| Data Modeling | 3 hours | [Power BI Optimization](../best-practices/power-bi-optimization.md) |
| DAX Fundamentals | 3 hours | External resources |

**Hands-on Lab:**
1. Connect Power BI to Serverless SQL
2. Create star schema model
3. Build sales dashboard with KPIs

---

### Module 4: Advanced Analytics (Week 4)

| Topic | Duration | Resources |
|-------|----------|-----------|
| Window Functions | 2 hours | [SQL Performance](../best-practices/sql-performance/README.md) |
| Time Intelligence | 2 hours | DAX patterns |
| What-If Analysis | 2 hours | Power BI parameters |

**Hands-on Lab:**
```sql
-- Advanced analytics queries
SELECT
    OrderDate,
    ProductCategory,
    Amount,
    SUM(Amount) OVER (PARTITION BY ProductCategory ORDER BY OrderDate) AS RunningTotal,
    AVG(Amount) OVER (PARTITION BY ProductCategory ORDER BY OrderDate ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS MovingAvg7Day,
    LAG(Amount, 1) OVER (PARTITION BY ProductCategory ORDER BY OrderDate) AS PreviousDayAmount
FROM Sales
ORDER BY ProductCategory, OrderDate;
```

---

## Certification Preparation

### Recommended Certifications

1. **DP-900**: Azure Data Fundamentals
2. **PL-300**: Power BI Data Analyst
3. **DP-500**: Azure Enterprise Data Analyst

### Study Resources

- Microsoft Learn modules
- Practice assessments
- Hands-on labs in this documentation

---

## Skills Assessment

### Beginner Checkpoint
- [ ] Query Parquet files with OPENROWSET
- [ ] Create external tables
- [ ] Connect Power BI to Serverless SQL

### Intermediate Checkpoint
- [ ] Optimize queries for performance
- [ ] Build star schema models
- [ ] Create DAX measures

### Advanced Checkpoint
- [ ] Implement row-level security
- [ ] Design aggregations
- [ ] Troubleshoot performance issues

---

## Related Documentation

- [Data Engineer Path](data-engineer-path.md)
- [Platform Admin Path](platform-admin-path.md)
- [Power BI Tutorials](power-bi/README.md)

---

*Last Updated: January 2025*
