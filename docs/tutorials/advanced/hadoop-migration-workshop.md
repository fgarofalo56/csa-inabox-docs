# 🔄 Hadoop Migration Workshop

> __🏠 [Home](../../../README.md)__ | __📖 [Documentation](../../README.md)__ | __🎓 [Tutorials](../README.md)__ | __🚀 Advanced__ | __🔄 Migration__

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Level](https://img.shields.io/badge/Level-Advanced-red)
![Duration](https://img.shields.io/badge/Duration-120--150_minutes-blue)

__Migrate on-premises Hadoop workloads to Azure. Learn assessment, planning, and execution strategies.__

## 🎯 Learning Objectives

- Assess on-premises Hadoop clusters
- Plan migration strategy
- Migrate data and workloads
- Optimize for Azure
- Validate and cutover

## 📋 Prerequisites

- [ ] __On-premises Hadoop cluster__ or access
- [ ] __Azure subscription__ with adequate quota
- [ ] __HDInsight or Databricks experience__
- [ ] __Understanding of Hadoop architecture__

## 🔍 Step 1: Assessment

### __Inventory Collection__

```bash
# Collect cluster metrics
yarn node -list > cluster-nodes.txt
hdfs dfsadmin -report > hdfs-report.txt
yarn application -list -appStates ALL > applications.txt
hive -e "SHOW TABLES" > hive-tables.txt
```

### __Workload Analysis__

- Identify data sources and sizes
- Map job dependencies
- Document SLAs and performance requirements
- List security and compliance needs

## 📊 Step 2: Migration Strategy

### __Lift and Shift vs Modernization**

__Lift and Shift (HDInsight)__
✅ Fastest migration
✅ Minimal code changes
❌ Limited modernization

__Modernize (Databricks/Synapse)__
✅ Better performance
✅ Modern features
❌ More effort

### __Migration Phases__

1. **Pilot** - 1-2 workloads
2. **Wave 1** - Non-critical workloads
3. **Wave 2** - Production workloads
4. **Decommission** - Turn off on-prem

## 🚀 Step 3: Data Migration

### __Use AzCopy or DistCp**

```bash
# DistCp from on-prem to Azure
hadoop distcp \
  hdfs://onprem-namenode:8020/data/* \
  wasb://container@storageaccount.blob.core.windows.net/data/

# AzCopy
azcopy copy \
  "hdfs://onprem-namenode:8020/data/*" \
  "https://storageaccount.blob.core.windows.net/container" \
  --recursive
```

## 🔧 Step 4: Workload Migration

### __Hive Scripts**

```sql
-- Migrate Hive tables
CREATE EXTERNAL TABLE sales_azure
STORED AS ORC
LOCATION 'wasb://data@storageaccount.blob.core.windows.net/sales/'
AS
SELECT * FROM sales_onprem;
```

### __MapReduce to Spark**

```python
# Modernize MapReduce to Spark
# Old MapReduce
# New Spark
df = spark.read.csv("wasb:///data/sales.csv")
result = df.groupBy("category").sum("amount")
```

## ✅ Step 5: Validation

- Compare data counts
- Run test queries
- Benchmark performance
- Verify security

## 📚 Resources

- [Azure Migration Guide](https://learn.microsoft.com/azure/architecture/data-guide/)
- [HDInsight Migration](https://learn.microsoft.com/azure/hdinsight/hdinsight-hadoop-on-premises-migration-best-practices-architecture)

---

*Last Updated: January 2025*
