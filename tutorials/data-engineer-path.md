# Data Engineer Learning Path

> **[Home](../README.md)** | **[Tutorials](README.md)** | **Data Engineer Path**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Level](https://img.shields.io/badge/Level-Intermediate_to_Advanced-orange?style=flat-square)

Complete learning path for Data Engineers using Cloud Scale Analytics.

---

## Overview

This learning path covers:

- Building data pipelines with Data Factory
- Delta Lake and Spark processing
- Data orchestration and ETL
- MLOps and advanced patterns

**Duration**: 8-12 weeks | **Prerequisites**: SQL, Python basics

---

## Learning Modules

### Module 1: Platform Architecture (Week 1-2)

| Topic | Duration | Resources |
|-------|----------|-----------|
| Lakehouse Architecture | 4 hours | [Delta Lakehouse](../docs/architecture/delta-lakehouse/README.md) |
| Medallion Pattern | 2 hours | [Architecture Patterns](../docs/03-architecture-patterns/README.md) |
| Service Selection | 2 hours | [Service Catalog](../docs/01-overview/service-catalog.md) |

**Hands-on Lab:**
```python
# Understand medallion architecture
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("MedallionDemo").getOrCreate()

# Bronze: Raw data ingestion
bronze_df = spark.read.format("json").load("/raw/events/")
bronze_df.write.format("delta").mode("append").save("/bronze/events/")

# Silver: Cleaned and validated
silver_df = spark.read.format("delta").load("/bronze/events/") \
    .dropDuplicates(["event_id"]) \
    .filter("event_type IS NOT NULL")
silver_df.write.format("delta").mode("overwrite").save("/silver/events/")

# Gold: Business aggregations
gold_df = spark.read.format("delta").load("/silver/events/") \
    .groupBy("event_type", "date") \
    .agg({"value": "sum", "event_id": "count"})
gold_df.write.format("delta").mode("overwrite").save("/gold/event_summary/")
```

---

### Module 2: Data Factory & Pipelines (Week 3-4)

| Topic | Duration | Resources |
|-------|----------|-----------|
| ADF Fundamentals | 4 hours | [Data Factory Tutorials](data-factory/README.md) |
| Integration Runtime | 2 hours | [IR Setup](data-factory/03-integration-runtime.md) |
| Pipeline Patterns | 4 hours | [Pipeline Best Practices](../best-practices/pipeline-optimization.md) |

**Hands-on Lab:**
- Build incremental load pipeline
- Implement error handling
- Configure monitoring

---

### Module 3: Spark & Delta Lake (Week 5-6)

| Topic | Duration | Resources |
|-------|----------|-----------|
| PySpark Fundamentals | 6 hours | [PySpark Lab](code-labs/pyspark-fundamentals/README.md) |
| Delta Lake Deep Dive | 4 hours | [Delta Lake Guide](../docs/code-examples/delta-lake/README.md) |
| Performance Tuning | 4 hours | [Spark Performance](../best-practices/spark-performance.md) |

**Hands-on Lab:**
```python
# Delta Lake operations
from delta.tables import DeltaTable

# Enable Change Data Feed
spark.sql("""
    ALTER TABLE delta.`/gold/customers`
    SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")

# Merge/Upsert pattern
delta_table = DeltaTable.forPath(spark, "/gold/customers")

delta_table.alias("target").merge(
    updates_df.alias("source"),
    "target.customer_id = source.customer_id"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()

# Optimize table
spark.sql("OPTIMIZE gold.customers ZORDER BY (region, customer_type)")
```

---

### Module 4: Stream Processing (Week 7-8)

| Topic | Duration | Resources |
|-------|----------|-----------|
| Event Hubs Integration | 3 hours | [EventHub + Spark](../docs/04-implementation-guides/integration-scenarios/eventhub-databricks.md) |
| Structured Streaming | 4 hours | [Streaming Patterns](../docs/03-architecture-patterns/streaming-architectures/README.md) |
| Stream Analytics | 3 hours | [ASA Tutorials](stream-analytics/README.md) |

**Hands-on Lab:**
```python
# Structured Streaming from Event Hubs
stream_df = spark.readStream \
    .format("eventhubs") \
    .options(**eh_conf) \
    .load()

# Process and write to Delta
stream_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/checkpoints/events") \
    .trigger(processingTime="10 seconds") \
    .start("/silver/streaming_events")
```

---

### Module 5: Advanced Patterns (Week 9-10)

| Topic | Duration | Resources |
|-------|----------|-----------|
| CDC Implementation | 4 hours | [CDC Patterns](../docs/04-implementation-guides/integration-scenarios/capture-databricks.md) |
| Data Quality | 3 hours | [Data Quality](../best-practices/data-quality.md) |
| Data Lineage | 3 hours | [Lineage with Purview](purview/lineage-setup.md) |

---

### Module 6: MLOps & DataOps (Week 11-12)

| Topic | Duration | Resources |
|-------|----------|-----------|
| Feature Engineering | 4 hours | [Feature Store](../docs/solutions/ml-pipeline/README.md) |
| MLflow Integration | 4 hours | [MLOps Pipeline](../docs/solutions/ml-pipeline/README.md) |
| CI/CD for Data | 4 hours | [DataOps Guide](../docs/devops/README.md) |

---

## Certification Preparation

### Recommended Certifications

1. **DP-203**: Azure Data Engineer Associate
2. **DP-600**: Fabric Analytics Engineer
3. **Databricks Certified Data Engineer**

---

## Skills Assessment

### Intermediate Checkpoint
- [ ] Build end-to-end pipeline
- [ ] Implement Delta Lake tables
- [ ] Configure incremental loads

### Advanced Checkpoint
- [ ] Design streaming architecture
- [ ] Implement CDC patterns
- [ ] Build feature pipelines

---

## Related Documentation

- [Data Analyst Path](data-analyst-path.md)
- [Platform Admin Path](platform-admin-path.md)

---

*Last Updated: January 2025*
