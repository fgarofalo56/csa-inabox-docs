[Home](/) > [Best Practices](./index.md) > Performance Optimization

# Performance Optimization Best Practices

## Query Performance Optimization

### Spark Pool Optimization

#### Resource Configuration

- **Autoscale Configuration**: Set appropriate min and max node counts based on workload patterns

- **Node Size Selection**: Choose the right memory-to-core ratio based on workload characteristics

- **Dynamic Allocation**: Enable dynamic executor allocation for variable workloads

- **Spark Configurations**:

  ```
  spark.sql.adaptive.enabled = true
  spark.sql.adaptive.coalescePartitions.enabled = true
  spark.sql.adaptive.skewJoin.enabled = true
  ```

#### Code Optimization

- **DataFrame Caching**: Cache intermediate DataFrames for reuse in complex workflows

  ```python
  df = spark.read.format("delta").load("/path/to/data")
  df.cache()  # Cache the DataFrame for repeated use
  ```

- **Partition Pruning**: Ensure your queries can leverage partition pruning

  ```python
  # Good - enables partition pruning
  df.filter(df.date_column == "2025-01-01").show()

  # Bad - prevents partition pruning
  df.filter(year(df.date_column) == 2025).show()
  ```

- **Broadcast Joins**: Use broadcast joins for small-to-large table joins

  ```python
  from pyspark.sql.functions import broadcast

  large_df = spark.table("large_table")
  small_df = spark.table("small_table")

  # Broadcast the smaller table
  result = large_df.join(broadcast(small_df), "join_key")
  ```

### Serverless SQL Optimization

#### Query Structure

- **Predicate Pushdown**: Structure queries to enable predicate pushdown to the storage layer

  ```sql
  -- Good: Enables pushdown
  SELECT * FROM external_table WHERE date_column = '2025-01-01'

  -- Avoid: Prevents pushdown
  SELECT * FROM external_table WHERE YEAR(date_column) = 2025
  ```

- **Column Pruning**: Select only necessary columns

  ```sql
  -- Good: Only reads required columns
  SELECT column1, column2 FROM large_table

  -- Avoid: Reads all columns
  SELECT * FROM large_table
  ```

#### External Table Design

- **Statistics**: Create and maintain statistics on frequently queried columns

  ```sql
  CREATE STATISTICS stats_column1 ON external_table (column1)
  ```

- **File Format Selection**: Prefer columnar formats (Parquet, Delta) over row-based formats (CSV, JSON)

- **Partitioning Strategy**: Align partitioning with common query filters

## Data Storage Optimization

### File Format Optimization

#### Delta Lake Optimization

- **File Compaction**: Regularly compact small files

  ```sql
  OPTIMIZE tableName
  ```

- **Z-Ordering**: Apply Z-ordering on commonly filtered columns

  ```sql
  OPTIMIZE tableName ZORDER BY (column1, column2)
  ```

- **Bloom Filter Indexes**: Create bloom filter indexes for selective string columns

  ```sql
  CREATE BLOOMFILTER INDEX ON TABLE tableName FOR COLUMNS(category_column)
  ```

#### Parquet Optimization

- **Compression**: Use appropriate compression codecs (Snappy for balance, Zstd for better compression)

  ```python
  df.write.option("compression", "snappy").format("parquet").save("/path/to/data")
  ```

- **Row Group Size**: Optimize row group size for your query patterns

  ```python
  df.write.option("parquet.block.size", 134217728).format("parquet").save("/path/to/data")
  ```

### Data Layout Optimization

#### Partitioning Strategies

- **Date-Based Partitioning**: Partition time series data by appropriate time granularity

  ```python
  # Daily partitioning for frequently accessed recent data
  df.write.partitionBy("year", "month", "day").format("delta").save("/path/to/data")

  # Monthly partitioning for historical data
  df.write.partitionBy("year", "month").format("delta").save("/path/to/historical_data")
  ```

- **Categorical Partitioning**: Partition by categorical columns with appropriate cardinality

  ```python
  # Good: Low to medium cardinality column
  df.write.partitionBy("region").format("delta").save("/path/to/data")

  # Avoid: High cardinality columns like customer_id
  ```

- **Hybrid Partitioning**: Combine date and categorical dimensions when appropriate

  ```python
  df.write.partitionBy("year", "month", "region").format("delta").save("/path/to/data")
  ```

## Memory Optimization

### Spark Memory Management

#### Memory Configuration

- **Executor Memory**: Allocate appropriate memory for executors based on data size

  ```
  spark.executor.memory = 8g
  ```

- **Memory Fraction**: Tune the fraction of heap used for execution and storage

  ```
  spark.memory.fraction = 0.8
  spark.memory.storageFraction = 0.5
  ```

#### Data Skew Handling

- **Salting**: Add a salt column for skewed keys

  ```python
  from pyspark.sql.functions import monotonically_increasing_id, lit

  # Add a salt column for skewed data
  df = df.withColumn("salt", (monotonically_increasing_id() % 10).cast("int"))
  ```

- **Adaptive Query Execution**: Enable adaptive query execution for automatic skew handling

  ```
  spark.sql.adaptive.enabled = true
  spark.sql.adaptive.skewJoin.enabled = true
  ```

## Monitoring and Tuning

### Performance Monitoring

#### Key Metrics to Monitor

- **Spark UI Metrics**: Regularly review stage duration, task skew, and shuffle data

- **Query Execution Plans**: Analyze physical and logical plans for optimization opportunities

  ```python
  df.explain(True)  # Show the query execution plan
  ```

- **I/O Metrics**: Monitor read/write throughput and latency

#### Tuning Methodology

- **Benchmarking**: Establish baseline performance metrics

- **Iterative Tuning**: Make one change at a time and measure impact

- **Workload Analysis**: Tune based on dominant workload patterns

## Cost Optimization

### Resource Utilization

#### Auto-Scaling

- Configure auto-scaling based on actual workload patterns

- Set appropriate idle timeout to reduce costs during inactive periods

#### Right-Sizing

- Start with smaller instances and scale up only when needed

- Monitor utilization metrics to identify over-provisioned resources

### Storage Costs

#### Data Lifecycle Management

- Archive infrequently accessed data to cooler storage tiers

- Implement retention policies for transient data

- Use the appropriate storage tier based on access patterns

#### Vacuum Operations

- Regularly clean up old Delta files

  ```sql
  VACUUM tableName RETAIN 7 DAYS
  ```

- Monitor and manage transaction log growth

## Conclusion

Optimizing performance in Azure Synapse Analytics requires a holistic approach covering storage organization, query design, resource configuration, and ongoing monitoring. By applying these best practices, you can achieve significant performance improvements and cost savings while meeting your analytical workload requirements.

Remember that performance optimization is an iterative process that should be tailored to your specific workload characteristics and business requirements.
