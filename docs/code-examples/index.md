[Home](../../README.md) > Code Examples

# Azure Synapse Analytics Code Examples

This section provides practical code examples for working with Azure Synapse Analytics features, focusing on Spark Delta Lakehouse and Serverless SQL implementations.

## Delta Lake Operations

### Creating a Delta Table

```python
# PySpark example for creating a Delta table
from pyspark.sql import SparkSession
from delta.tables import DeltaTable

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Delta Lake Example") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Create a simple DataFrame
data = [("John", 25), ("Jane", 30), ("Bob", 45)]
df = spark.createDataFrame(data, ["name", "age"])

# Write as Delta format
df.write.format("delta").save("/mnt/delta/people")

# Create a Delta table object
deltaTable = DeltaTable.forPath(spark, "/mnt/delta/people")

print("Delta table created successfully!")
```

### Updating Delta Tables with Merge

```python
# PySpark Delta Lake merge operation example
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from delta.tables import DeltaTable

# Initialize Spark session with Delta support
spark = SparkSession.builder \
    .appName("Delta Lake Merge Example") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Assuming we have an existing Delta table
deltaTable = DeltaTable.forPath(spark, "/mnt/delta/people")

# Create a new DataFrame with updates
updates = [("John", 26), ("Jane", 31), ("Mike", 50)]
updatesDF = spark.createDataFrame(updates, ["name", "age"])

# Perform merge operation
deltaTable.alias("target") \
    .merge(
        updatesDF.alias("updates"),
        "target.name = updates.name") \
    .whenMatchedUpdate(set={"age": "updates.age"}) \
    .whenNotMatchedInsert(values={"name": "updates.name", "age": "updates.age"}) \
    .execute()

print("Merge operation completed!")
```

## Serverless SQL Queries

### Querying External Data Sources

```sql
-- SQL query for Serverless SQL Pool to query Parquet files in storage
SELECT TOP 100 *
FROM OPENROWSET(
    BULK 'https://yourstorageaccount.dfs.core.windows.net/container/path/to/data/*.parquet',
    FORMAT = 'PARQUET'
) AS rows

-- Using Delta table format
SELECT TOP 100 *
FROM OPENROWSET(
    BULK 'https://yourstorageaccount.dfs.core.windows.net/container/path/to/delta/',
    FORMAT = 'DELTA'
) AS rows
```

### Creating External Tables

```sql
-- Create an external file format for Parquet
CREATE EXTERNAL FILE FORMAT ParquetFormat
WITH (
    FORMAT_TYPE = PARQUET,
    DATA_COMPRESSION = 'SNAPPY'
);

-- Create an external data source
CREATE EXTERNAL DATA SOURCE MyDataSource
WITH (
    LOCATION = 'https://yourstorageaccount.dfs.core.windows.net/container/'
);

-- Create an external table
CREATE EXTERNAL TABLE dbo.ExternalTable (
    Column1 INT,
    Column2 VARCHAR(100),
    Column3 DATETIME2
)
WITH (
    LOCATION = 'path/to/data/',
    DATA_SOURCE = MyDataSource,
    FILE_FORMAT = ParquetFormat
);
```

## Integration Examples

### Combining Spark and SQL

```python
# Example of using Spark to prepare data and then query with SQL
from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder.appName("Spark SQL Integration").getOrCreate()

# Load and process data with Spark
df = spark.read.format("csv").option("header", "true").load("/path/to/data.csv")
processed_df = df.filter(df.column > 0).withColumn("new_column", df.column * 2)

# Save as Delta for SQL querying
processed_df.write.format("delta").mode("overwrite").save("/mnt/delta/processed_data")

# Register as a temp view for SQL operations
processed_df.createOrReplaceTempView("processed_data_view")

# Run SQL query on the data
result = spark.sql("""
    SELECT 
        column1, 
        AVG(new_column) as avg_value
    FROM 
        processed_data_view
    GROUP BY 
        column1
    HAVING 
        COUNT(*) > 5
""")

result.show()
```

## Additional Resources

- [Azure Synapse Analytics Documentation](https://docs.microsoft.com/en-us/azure/synapse-analytics/)
- [Delta Lake Documentation](https://docs.delta.io/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/index.html)
