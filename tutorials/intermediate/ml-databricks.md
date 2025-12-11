# Machine Learning on Databricks

> **[Home](../../README.md)** | **[Tutorials](../README.md)** | **ML on Databricks**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Level](https://img.shields.io/badge/Level-Intermediate-yellow?style=flat-square)

Guide to machine learning workflows on Azure Databricks.

---

## Overview

This tutorial covers:

- MLflow experiment tracking
- Feature engineering
- Model training and evaluation
- Model deployment

**Duration**: 2.5 hours | **Prerequisites**: Python, ML basics

---

## MLflow Setup

### Initialize Experiment

```python
import mlflow
from mlflow.tracking import MlflowClient

# Set experiment
mlflow.set_experiment("/Experiments/customer-churn")

# Get experiment info
client = MlflowClient()
experiment = client.get_experiment_by_name("/Experiments/customer-churn")
print(f"Experiment ID: {experiment.experiment_id}")
```

---

## Feature Engineering

### Create Features

```python
from pyspark.sql import functions as F
from pyspark.ml.feature import VectorAssembler, StandardScaler

# Load data
customers = spark.table("bronze.customers")
transactions = spark.table("bronze.transactions")

# Create features
features_df = transactions.groupBy("customer_id").agg(
    F.count("*").alias("transaction_count"),
    F.sum("amount").alias("total_spend"),
    F.avg("amount").alias("avg_transaction"),
    F.max("transaction_date").alias("last_transaction"),
    F.countDistinct("product_category").alias("unique_categories")
).join(
    customers.select("customer_id", "signup_date", "region"),
    "customer_id"
).withColumn(
    "tenure_days",
    F.datediff(F.current_date(), F.col("signup_date"))
).withColumn(
    "days_since_last_txn",
    F.datediff(F.current_date(), F.col("last_transaction"))
)

# Assemble features
feature_cols = [
    "transaction_count", "total_spend", "avg_transaction",
    "unique_categories", "tenure_days", "days_since_last_txn"
]

assembler = VectorAssembler(inputCols=feature_cols, outputCol="features_raw")
features_assembled = assembler.transform(features_df)

# Scale features
scaler = StandardScaler(inputCol="features_raw", outputCol="features")
scaler_model = scaler.fit(features_assembled)
features_scaled = scaler_model.transform(features_assembled)
```

---

## Model Training

### Train with MLflow Tracking

```python
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import pandas as pd

# Convert to pandas
pdf = features_scaled.select("customer_id", "features", "churned").toPandas()

# Prepare data
X = pdf["features"].apply(lambda x: x.toArray()).tolist()
X = pd.DataFrame(X, columns=feature_cols)
y = pdf["churned"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train with MLflow tracking
with mlflow.start_run(run_name="random_forest_v1"):
    # Log parameters
    params = {
        "n_estimators": 100,
        "max_depth": 10,
        "min_samples_split": 5,
        "random_state": 42
    }
    mlflow.log_params(params)

    # Train model
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_prob)
    }
    mlflow.log_metrics(metrics)

    # Log feature importance
    importance_df = pd.DataFrame({
        "feature": feature_cols,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)

    mlflow.log_table(importance_df, "feature_importance.json")

    # Log model
    mlflow.sklearn.log_model(
        model,
        "model",
        registered_model_name="customer_churn_model"
    )

    print(f"Metrics: {metrics}")
```

---

## Hyperparameter Tuning

### Using Hyperopt

```python
from hyperopt import fmin, tpe, hp, SparkTrials, STATUS_OK
import numpy as np

def objective(params):
    with mlflow.start_run(nested=True):
        # Log parameters
        mlflow.log_params(params)

        # Train model
        model = RandomForestClassifier(
            n_estimators=int(params["n_estimators"]),
            max_depth=int(params["max_depth"]),
            min_samples_split=int(params["min_samples_split"]),
            random_state=42
        )
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        mlflow.log_metric("accuracy", accuracy)

        return {"loss": -accuracy, "status": STATUS_OK}

# Define search space
search_space = {
    "n_estimators": hp.quniform("n_estimators", 50, 500, 50),
    "max_depth": hp.quniform("max_depth", 5, 30, 5),
    "min_samples_split": hp.quniform("min_samples_split", 2, 20, 2)
}

# Run hyperparameter search
with mlflow.start_run(run_name="hyperopt_search"):
    spark_trials = SparkTrials(parallelism=4)

    best_params = fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=20,
        trials=spark_trials
    )

    print(f"Best parameters: {best_params}")
```

---

## Model Deployment

### Register Model

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Get latest model version
model_name = "customer_churn_model"
latest_version = client.get_latest_versions(model_name, stages=["None"])[0]

# Transition to staging
client.transition_model_version_stage(
    name=model_name,
    version=latest_version.version,
    stage="Staging"
)

# After validation, promote to production
client.transition_model_version_stage(
    name=model_name,
    version=latest_version.version,
    stage="Production"
)
```

### Create Serving Endpoint

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Create model serving endpoint
endpoint_config = {
    "served_entities": [{
        "entity_name": "customer_churn_model",
        "entity_version": "1",
        "workload_size": "Small",
        "scale_to_zero_enabled": True
    }]
}

endpoint = w.serving_endpoints.create_and_wait(
    name="churn-prediction-endpoint",
    config=endpoint_config
)

print(f"Endpoint URL: {endpoint.url}")
```

### Score New Data

```python
import requests
import json

# Get endpoint URL
endpoint_url = "https://workspace.azuredatabricks.net/serving-endpoints/churn-prediction-endpoint/invocations"

# Prepare request
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

data = {
    "dataframe_records": [
        {
            "transaction_count": 50,
            "total_spend": 5000,
            "avg_transaction": 100,
            "unique_categories": 5,
            "tenure_days": 365,
            "days_since_last_txn": 30
        }
    ]
}

# Make prediction
response = requests.post(endpoint_url, headers=headers, json=data)
predictions = response.json()
print(f"Churn probability: {predictions['predictions'][0]}")
```

---

## Related Documentation

- [ML Pipeline Solution](../../docs/solutions/ml-pipeline/README.md)
- [Data Engineer Path](../data-engineer-path.md)
- [Spark SQL Tutorial](spark-sql-tutorial.md)

---

*Last Updated: January 2025*
