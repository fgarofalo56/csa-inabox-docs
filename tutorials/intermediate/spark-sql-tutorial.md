# Spark SQL Tutorial

> **[Home](../../README.md)** | **[Tutorials](../README.md)** | **Spark SQL Tutorial**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Level](https://img.shields.io/badge/Level-Intermediate-yellow?style=flat-square)

Comprehensive guide to Spark SQL for data analytics.

---

## Overview

This tutorial covers:

- Spark SQL fundamentals
- DataFrame operations
- Window functions
- Performance optimization

**Duration**: 2 hours | **Prerequisites**: Basic SQL knowledge

---

## Getting Started

### Create SparkSession

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SparkSQLTutorial") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# Register tables
spark.sql("USE catalog.database")
```

---

## Basic Queries

### SELECT and Filtering

```python
# SQL style
result = spark.sql("""
    SELECT
        customer_id,
        customer_name,
        region,
        total_purchases
    FROM customers
    WHERE region = 'North'
        AND total_purchases > 1000
    ORDER BY total_purchases DESC
    LIMIT 100
""")

# DataFrame API equivalent
from pyspark.sql.functions import col, desc

result = spark.table("customers") \
    .select("customer_id", "customer_name", "region", "total_purchases") \
    .filter((col("region") == "North") & (col("total_purchases") > 1000)) \
    .orderBy(desc("total_purchases")) \
    .limit(100)
```

### Aggregations

```python
# SQL
spark.sql("""
    SELECT
        region,
        product_category,
        COUNT(*) AS order_count,
        SUM(amount) AS total_sales,
        AVG(amount) AS avg_order_value,
        PERCENTILE_APPROX(amount, 0.5) AS median_order
    FROM orders
    WHERE order_date >= '2024-01-01'
    GROUP BY region, product_category
    HAVING SUM(amount) > 10000
    ORDER BY total_sales DESC
""")

# DataFrame API
from pyspark.sql.functions import count, sum, avg, percentile_approx

orders = spark.table("orders") \
    .filter(col("order_date") >= "2024-01-01") \
    .groupBy("region", "product_category") \
    .agg(
        count("*").alias("order_count"),
        sum("amount").alias("total_sales"),
        avg("amount").alias("avg_order_value"),
        percentile_approx("amount", 0.5).alias("median_order")
    ) \
    .filter(col("total_sales") > 10000) \
    .orderBy(desc("total_sales"))
```

---

## Joins

### Multiple Join Types

```python
# Inner join
spark.sql("""
    SELECT
        o.order_id,
        o.amount,
        c.customer_name,
        p.product_name
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    INNER JOIN products p ON o.product_id = p.product_id
""")

# Left join with handling nulls
spark.sql("""
    SELECT
        c.customer_id,
        c.customer_name,
        COALESCE(SUM(o.amount), 0) AS total_spend
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
""")

# DataFrame API - broadcast join for small tables
from pyspark.sql.functions import broadcast

orders = spark.table("orders")
products = spark.table("products")  # Small dimension table

result = orders.join(
    broadcast(products),
    orders.product_id == products.product_id,
    "inner"
)
```

---

## Window Functions

### Ranking and Analytics

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, dense_rank, lag, lead, sum

# Define window
customer_window = Window.partitionBy("customer_id").orderBy("order_date")
category_window = Window.partitionBy("category").orderBy(desc("sales"))

# Running total
orders_with_running = spark.sql("""
    SELECT
        order_id,
        customer_id,
        order_date,
        amount,
        SUM(amount) OVER (
            PARTITION BY customer_id
            ORDER BY order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS running_total
    FROM orders
""")

# Ranking within category
product_rankings = spark.sql("""
    SELECT
        product_name,
        category,
        sales,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC) AS row_num,
        RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS rank,
        DENSE_RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS dense_rank
    FROM product_sales
""")

# Previous and next values
spark.sql("""
    SELECT
        customer_id,
        order_date,
        amount,
        LAG(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_amount,
        LEAD(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date) AS next_amount,
        amount - LAG(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date) AS change
    FROM orders
""")
```

### Moving Averages

```python
# 7-day moving average
spark.sql("""
    SELECT
        date,
        revenue,
        AVG(revenue) OVER (
            ORDER BY date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS moving_avg_7d,
        AVG(revenue) OVER (
            ORDER BY date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS moving_avg_30d
    FROM daily_revenue
""")
```

---

## Complex Queries

### CTEs and Subqueries

```python
spark.sql("""
    WITH monthly_sales AS (
        SELECT
            DATE_TRUNC('month', order_date) AS month,
            customer_id,
            SUM(amount) AS monthly_total
        FROM orders
        GROUP BY DATE_TRUNC('month', order_date), customer_id
    ),
    customer_segments AS (
        SELECT
            customer_id,
            CASE
                WHEN AVG(monthly_total) > 1000 THEN 'High Value'
                WHEN AVG(monthly_total) > 500 THEN 'Medium Value'
                ELSE 'Low Value'
            END AS segment
        FROM monthly_sales
        GROUP BY customer_id
    )
    SELECT
        cs.segment,
        COUNT(DISTINCT cs.customer_id) AS customer_count,
        AVG(ms.monthly_total) AS avg_monthly_spend
    FROM customer_segments cs
    JOIN monthly_sales ms ON cs.customer_id = ms.customer_id
    GROUP BY cs.segment
""")
```

### Pivot Tables

```python
# Pivot operation
spark.sql("""
    SELECT *
    FROM (
        SELECT region, product_category, amount
        FROM orders
    )
    PIVOT (
        SUM(amount)
        FOR product_category IN ('Electronics', 'Clothing', 'Food', 'Home')
    )
""")

# DataFrame API
orders.groupBy("region") \
    .pivot("product_category", ["Electronics", "Clothing", "Food", "Home"]) \
    .agg(sum("amount"))
```

---

## Performance Tips

### Optimize Joins

```python
# 1. Broadcast small tables
spark.sql("""
    SELECT /*+ BROADCAST(products) */
        o.*, p.product_name
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
""")

# 2. Filter before join
spark.sql("""
    WITH recent_orders AS (
        SELECT * FROM orders WHERE order_date >= '2024-01-01'
    )
    SELECT * FROM recent_orders o
    JOIN customers c ON o.customer_id = c.customer_id
""")

# 3. Use appropriate partitioning
spark.conf.set("spark.sql.shuffle.partitions", "200")
```

### Caching

```python
# Cache frequently used DataFrame
orders_2024 = spark.table("orders").filter(col("order_date") >= "2024-01-01")
orders_2024.cache()

# Use in multiple queries
orders_2024.groupBy("region").count().show()
orders_2024.groupBy("category").sum("amount").show()

# Uncache when done
orders_2024.unpersist()
```

---

## Related Documentation

- [HDInsight Spark](hdinsight-spark.md)
- [Delta Lake Guide](../../docs/code-examples/delta-lake/README.md)
- [Data Engineer Path](../data-engineer-path.md)

---

*Last Updated: January 2025*
