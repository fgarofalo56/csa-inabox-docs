# Frequently Asked Questions

> **[Home](../README.md)** | **FAQ**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

Common questions about Cloud Scale Analytics on Azure.

---

## General Questions

### What is Cloud Scale Analytics (CSA)?

Cloud Scale Analytics is an architectural pattern for building enterprise-grade analytics platforms on Azure. It combines Azure Synapse Analytics, Azure Databricks, and Azure Data Lake Storage to provide a unified analytics solution.

### When should I use Synapse vs Databricks?

| Use Case | Recommended Service |
|----------|-------------------|
| SQL-heavy workloads | Synapse Dedicated/Serverless SQL |
| Data science & ML | Azure Databricks |
| ETL/ELT pipelines | Both (depends on team skills) |
| Real-time streaming | Databricks or Stream Analytics |
| Ad-hoc exploration | Synapse Serverless SQL |

---

## Architecture Questions

### What is the Medallion Architecture?

The Medallion Architecture organizes data into three layers:

- **Bronze**: Raw data (as-is from sources)
- **Silver**: Cleansed, conformed data
- **Gold**: Business-level aggregates

### Should I use Delta Lake?

Yes, Delta Lake is recommended for most scenarios because it provides:
- ACID transactions
- Time travel
- Schema enforcement
- Unified batch/streaming

---

## Performance Questions

### How do I optimize Spark jobs?

1. Use appropriate partition sizes (128MB-1GB)
2. Enable Adaptive Query Execution
3. Cache frequently used DataFrames
4. Use broadcast joins for small tables
5. Avoid shuffles when possible

### How do I reduce costs?

1. Use serverless SQL for ad-hoc queries
2. Pause dedicated resources when not in use
3. Right-size compute clusters
4. Implement data lifecycle policies
5. Use reserved capacity for predictable workloads

---

## Security Questions

### How do I secure my data lake?

1. Use Azure AD authentication
2. Implement RBAC with Unity Catalog or Synapse
3. Enable private endpoints
4. Encrypt data at rest and in transit
5. Enable auditing and monitoring

### What about data governance?

Use Azure Purview for:
- Data discovery and cataloging
- Data lineage tracking
- Data classification
- Access policies

---

## Integration Questions

### How do I connect Power BI?

- **Serverless SQL**: Use SQL endpoint connection string
- **Dedicated SQL**: Use dedicated pool endpoint
- **Databricks**: Use Databricks SQL endpoint or JDBC

### Can I use with Azure ML?

Yes, you can integrate with:
- MLflow on Databricks
- Azure ML linked service
- Model deployment to AKS/ACI

---

## Related Documentation

- [Troubleshooting Guide](../troubleshooting/README.md)
- [Best Practices](../best-practices/README.md)
- [Getting Started](../tutorials/README.md)

---

*Last Updated: January 2025*
