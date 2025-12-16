# 📚 SDK Documentation Guide

> **🏠 [Home](../../../README.md)** | **📚 Documentation** | **📖 [Guides](../README.md)** | **📋 [Docs](./README.md)** | **📚 SDKs**

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Complexity](https://img.shields.io/badge/Complexity-Intermediate-yellow)

---

## 📋 Overview

This guide provides comprehensive documentation for Azure SDKs used in the CSA in-a-Box solution. Learn how to effectively use Python SDKs for Azure Synapse, Storage, Key Vault, and other Azure services.

## 📑 Table of Contents

- [Azure SDK Overview](#azure-sdk-overview)
- [Installation and Setup](#installation-and-setup)
- [Azure Identity SDK](#azure-identity-sdk)
- [Azure Storage SDK](#azure-storage-sdk)
- [Azure Synapse SDK](#azure-synapse-sdk)
- [Azure Key Vault SDK](#azure-key-vault-sdk)
- [Azure Monitor SDK](#azure-monitor-sdk)
- [PySpark and Delta Lake](#pyspark-and-delta-lake)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Related Documentation](#related-documentation)

---

## 🎯 Azure SDK Overview

### Why Use Azure SDKs?

| Benefit | Description |
|---------|-------------|
| **Consistency** | Unified patterns across all Azure services |
| **Type Safety** | Full IntelliSense support and type hints |
| **Async Support** | Built-in async/await for Python 3.7+ |
| **Automatic Retry** | Intelligent retry policies |
| **Logging** | Integrated Azure Monitor logging |

### SDK Versioning

```python
# Azure SDK follows semantic versioning
azure-storage-blob>=12.19.0  # Major.Minor.Patch
azure-identity>=1.14.0
azure-synapse-spark>=0.7.0
```

---

## 📦 Installation and Setup

### Install Azure SDKs

```bash
# Core SDKs
pip install azure-identity
pip install azure-storage-blob
pip install azure-storage-file-datalake
pip install azure-synapse-spark
pip install azure-keyvault-secrets
pip install azure-monitor-query

# Optional SDKs
pip install azure-ai-openai
pip install azure-mgmt-synapse
pip install azure-eventhub
```

### Requirements File

```txt
# requirements.txt - Azure SDKs
azure-identity>=1.14.0
azure-storage-blob>=12.19.0
azure-storage-file-datalake>=12.14.0
azure-synapse-spark>=0.7.0
azure-synapse-artifacts>=0.17.0
azure-keyvault-secrets>=4.7.0
azure-monitor-query>=1.2.0
azure-ai-openai>=1.0.0

# PySpark and Delta Lake
pyspark>=3.4.0
delta-spark>=3.0.0

# Utilities
python-dotenv>=1.0.0
```

### Environment Setup

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="csa-inabox",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "azure-identity>=1.14.0",
        "azure-storage-blob>=12.19.0",
        # ... other dependencies
    ],
    python_requires=">=3.9",
)
```

---

## 🔐 Azure Identity SDK

### Overview

The Azure Identity library provides Azure Active Directory token authentication support.

### Installation

```bash
pip install azure-identity
```

### DefaultAzureCredential

```python
from azure.identity import DefaultAzureCredential

# Automatically handles authentication
# Works in: local dev, CI/CD, Azure resources
credential = DefaultAzureCredential()

# Use with any Azure service
from azure.storage.blob import BlobServiceClient
blob_client = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential=credential
)
```

### Specific Credentials

```python
from azure.identity import (
    ManagedIdentityCredential,  # Azure resources
    ClientSecretCredential,     # Service principals
    InteractiveBrowserCredential,  # Interactive login
    AzureCliCredential,         # Azure CLI
    EnvironmentCredential       # Environment variables
)

# Managed Identity (Production)
credential = ManagedIdentityCredential()

# Service Principal (CI/CD)
credential = ClientSecretCredential(
    tenant_id="<tenant-id>",
    client_id="<client-id>",
    client_secret="<client-secret>"
)

# Interactive (Development)
credential = InteractiveBrowserCredential()

# Azure CLI (Local Development)
credential = AzureCliCredential()
```

### Custom Credential Chain

```python
from azure.identity import ChainedTokenCredential, ManagedIdentityCredential, AzureCliCredential

# Try Managed Identity first, fall back to CLI
credential = ChainedTokenCredential(
    ManagedIdentityCredential(),
    AzureCliCredential()
)
```

---

## 💾 Azure Storage SDK

### Blob Storage Client

```python
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

# Service client (account-level operations)
blob_service_client = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential=credential
)

# Container client (container-level operations)
container_client = blob_service_client.get_container_client("mycontainer")

# Blob client (blob-level operations)
blob_client = blob_service_client.get_blob_client(
    container="mycontainer",
    blob="myblob.txt"
)
```

### Upload and Download

```python
# Upload blob
with open("local_file.txt", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

# Upload from string
blob_client.upload_blob("Hello, Azure!", overwrite=True)

# Download blob
with open("downloaded_file.txt", "wb") as download_file:
    download_file.write(blob_client.download_blob().readall())

# Download to stream
stream = blob_client.download_blob()
content = stream.readall()
```

### List and Delete

```python
# List blobs
for blob in container_client.list_blobs():
    print(f"Blob: {blob.name}, Size: {blob.size}")

# Delete blob
blob_client.delete_blob()

# Delete container
container_client.delete_container()
```

### Data Lake Storage Gen2

```python
from azure.storage.filedatalake import DataLakeServiceClient

# Data Lake client
datalake_client = DataLakeServiceClient(
    account_url="https://mystorageaccount.dfs.core.windows.net",
    credential=credential
)

# File system client (container)
file_system_client = datalake_client.get_file_system_client("myfilesystem")

# Directory client
directory_client = file_system_client.get_directory_client("myfolder")

# File client
file_client = directory_client.get_file_client("myfile.csv")

# Upload file
with open("local_file.csv", "rb") as data:
    file_client.upload_data(data, overwrite=True)

# Download file
download = file_client.download_file()
content = download.readall()
```

---

## ⚡ Azure Synapse SDK

### Synapse Spark Client

```python
from azure.synapse.spark import SparkClient
from azure.synapse.spark.models import SparkBatchJobOptions
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

# Create Spark client
spark_client = SparkClient(
    endpoint="https://myworkspace.dev.azuresynapse.net",
    credential=credential
)

# Submit Spark job
job_options = SparkBatchJobOptions(
    file="abfss://container@storage.dfs.core.windows.net/scripts/etl.py",
    class_name=None,
    arguments=["--input", "/mnt/data/input", "--output", "/mnt/data/output"],
    jars=[],
    python_files=[],
    files=[],
    archives=[],
    conf={
        "spark.dynamicAllocation.enabled": "true",
        "spark.dynamicAllocation.minExecutors": "1",
        "spark.dynamicAllocation.maxExecutors": "10"
    },
    name="ETL Pipeline",
    driver_memory="4g",
    driver_cores=2,
    executor_memory="4g",
    executor_cores=2,
    executor_count=4
)

# Submit job
spark_job = spark_client.spark_batch.create_spark_batch_job(
    workspace_name="myworkspace",
    spark_pool_name="sparkpool01",
    spark_batch_job_options=job_options
)

print(f"Job ID: {spark_job.id}")
print(f"Job State: {spark_job.state}")

# Monitor job
job_id = spark_job.id
while True:
    job = spark_client.spark_batch.get_spark_batch_job(
        workspace_name="myworkspace",
        spark_pool_name="sparkpool01",
        batch_id=job_id
    )

    print(f"Job State: {job.state}")

    if job.state in ["success", "dead", "error"]:
        break

    time.sleep(10)
```

### Synapse Artifacts Client

```python
from azure.synapse.artifacts import ArtifactsClient
from azure.synapse.artifacts.models import PipelineResource, Activity

credential = DefaultAzureCredential()

# Create artifacts client
artifacts_client = ArtifactsClient(
    endpoint="https://myworkspace.dev.azuresynapse.net",
    credential=credential
)

# List pipelines
pipelines = artifacts_client.pipeline.get_pipelines_by_workspace()
for pipeline in pipelines:
    print(f"Pipeline: {pipeline.name}")

# Get pipeline
pipeline = artifacts_client.pipeline.get_pipeline("MyPipeline")

# Create pipeline run
run_response = artifacts_client.pipeline.create_pipeline_run(
    pipeline_name="MyPipeline",
    parameters={"param1": "value1"}
)

print(f"Run ID: {run_response.run_id}")

# Monitor pipeline run
run_id = run_response.run_id
while True:
    run = artifacts_client.pipeline_run.get_pipeline_run(run_id)
    print(f"Run Status: {run.status}")

    if run.status in ["Succeeded", "Failed", "Cancelled"]:
        break

    time.sleep(10)
```

---

## 🔑 Azure Key Vault SDK

### Secret Management

```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

# Create Key Vault client
kv_client = SecretClient(
    vault_url="https://mykeyvault.vault.azure.net",
    credential=credential
)

# Set secret
kv_client.set_secret("DatabasePassword", "P@ssw0rd123!")

# Get secret
secret = kv_client.get_secret("DatabasePassword")
print(f"Secret value: {secret.value}")

# List secrets
for secret_properties in kv_client.list_properties_of_secrets():
    print(f"Secret: {secret_properties.name}")

# Delete secret
kv_client.begin_delete_secret("DatabasePassword").wait()

# Recover deleted secret
kv_client.begin_recover_deleted_secret("DatabasePassword").wait()
```

### Secret Versions

```python
# Get specific version
secret = kv_client.get_secret("DatabasePassword", version="abc123")

# List versions
versions = kv_client.list_properties_of_secret_versions("DatabasePassword")
for version in versions:
    print(f"Version: {version.version}, Created: {version.created_on}")

# Update secret properties
kv_client.update_secret_properties(
    "DatabasePassword",
    enabled=True,
    content_type="password",
    tags={"environment": "production"}
)
```

---

## 📊 Azure Monitor SDK

### Query Logs

```python
from azure.monitor.query import LogsQueryClient
from azure.identity import DefaultAzureCredential
from datetime import timedelta

credential = DefaultAzureCredential()

# Create logs query client
logs_client = LogsQueryClient(credential)

# Query logs
query = """
SynapseRbacOperations
| where TimeGenerated > ago(1d)
| summarize Count = count() by OperationName
| order by Count desc
"""

response = logs_client.query_workspace(
    workspace_id="<workspace-id>",
    query=query,
    timespan=timedelta(days=1)
)

# Process results
for table in response.tables:
    for row in table.rows:
        print(f"Operation: {row[0]}, Count: {row[1]}")
```

### Query Metrics

```python
from azure.monitor.query import MetricsQueryClient

# Create metrics query client
metrics_client = MetricsQueryClient(credential)

# Query metrics
response = metrics_client.query_resource(
    resource_uri="/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Synapse/workspaces/<workspace>",
    metric_names=["DataProcessedGB", "IntegrationActivityRunsEnded"],
    timespan=timedelta(hours=24),
    granularity=timedelta(minutes=15)
)

# Process results
for metric in response.metrics:
    print(f"Metric: {metric.name}")
    for timeseries in metric.timeseries:
        for data in timeseries.data:
            print(f"  Time: {data.time_stamp}, Value: {data.total}")
```

---

## 🔥 PySpark and Delta Lake

### PySpark Initialization

```python
from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("CSA in-a-Box ETL") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.databricks.delta.optimizeWrite.enabled", "true") \
    .config("spark.databricks.delta.autoCompact.enabled", "true") \
    .getOrCreate()

# Configure storage access
spark.conf.set(
    "fs.azure.account.auth.type.mystorageaccount.dfs.core.windows.net",
    "OAuth"
)
spark.conf.set(
    "fs.azure.account.oauth.provider.type.mystorageaccount.dfs.core.windows.net",
    "org.apache.hadoop.fs.azurebfs.oauth2.MsiTokenProvider"
)
```

### Delta Lake Operations

```python
from delta.tables import DeltaTable
from pyspark.sql.functions import col, current_timestamp

# Read Delta table
df = spark.read.format("delta").load("/mnt/delta/gold/customers")

# Write Delta table
df.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .partitionBy("country") \
    .save("/mnt/delta/gold/customers")

# Merge (Upsert)
delta_table = DeltaTable.forPath(spark, "/mnt/delta/gold/customers")

delta_table.alias("target").merge(
    source_df.alias("source"),
    "target.customer_id = source.customer_id"
).whenMatchedUpdateAll(
).whenNotMatchedInsertAll(
).execute()

# Optimize
delta_table.optimize().executeCompaction()
delta_table.optimize().executeZOrderBy("customer_id", "country")

# Vacuum
delta_table.vacuum(retentionHours=168)

# Time travel
historical_df = spark.read.format("delta") \
    .option("versionAsOf", 5) \
    .load("/mnt/delta/gold/customers")

# Read specific timestamp
historical_df = spark.read.format("delta") \
    .option("timestampAsOf", "2024-01-01") \
    .load("/mnt/delta/gold/customers")
```

---

## ✅ Best Practices

### Error Handling

```python
from azure.core.exceptions import (
    ResourceNotFoundError,
    ResourceExistsError,
    HttpResponseError
)

try:
    blob_client.upload_blob(data, overwrite=False)
except ResourceExistsError:
    print("Blob already exists")
    # Handle existing resource
except HttpResponseError as e:
    print(f"HTTP error: {e.status_code}, {e.message}")
    # Handle HTTP errors
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle unexpected errors
```

### Async Operations

```python
from azure.storage.blob.aio import BlobServiceClient
from azure.identity.aio import DefaultAzureCredential
import asyncio

async def upload_blobs_async():
    """Upload multiple blobs concurrently."""
    credential = DefaultAzureCredential()
    async with BlobServiceClient(
        account_url="https://mystorageaccount.blob.core.windows.net",
        credential=credential
    ) as blob_service_client:

        tasks = []
        for i in range(10):
            blob_client = blob_service_client.get_blob_client(
                container="mycontainer",
                blob=f"file_{i}.txt"
            )
            task = blob_client.upload_blob(f"Content {i}", overwrite=True)
            tasks.append(task)

        # Upload concurrently
        await asyncio.gather(*tasks)

# Run async function
asyncio.run(upload_blobs_async())
```

### Logging

```python
import logging

# Enable Azure SDK logging
logging.basicConfig(level=logging.INFO)

# Configure specific loggers
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("azure.storage.blob").setLevel(logging.DEBUG)
```

---

## 🔧 Troubleshooting

### Common Issues

#### Issue: Import Error

```python
# Error: ModuleNotFoundError: No module named 'azure.storage.blob'

# Solution: Install package
pip install azure-storage-blob

# Verify installation
pip show azure-storage-blob
```

#### Issue: Authentication Failed

```python
# Error: ClientAuthenticationError: Authentication failed

# Solution 1: Check Azure login
az login
az account show

# Solution 2: Grant permissions
az role assignment create \
  --role "Storage Blob Data Contributor" \
  --assignee <identity-id> \
  --scope <storage-account-id>

# Solution 3: Wait for propagation (5-10 minutes)
```

#### Issue: Connection Timeout

```python
# Error: ServiceRequestError: Connection timeout

# Solution: Configure retry policy
from azure.core.pipeline.policies import RetryPolicy
from azure.storage.blob import BlobServiceClient

retry_policy = RetryPolicy(
    retry_total=3,
    retry_backoff_factor=2,
    retry_backoff_max=60
)

blob_client = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential=credential,
    retry_policy=retry_policy
)
```

---

## 📚 Related Documentation

### Internal Guides

- [Authentication Guide](./authentication.md) - Authentication methods
- [Best Practices Guide](./best-practices.md) - Best practices
- [Technical Setup](../technical-setup.md) - Setup instructions

### Azure SDK Documentation

- [Azure SDK for Python](https://learn.microsoft.com/python/api/overview/azure/)
- [Azure Identity](https://learn.microsoft.com/python/api/overview/azure/identity-readme)
- [Azure Storage Blob](https://learn.microsoft.com/python/api/overview/azure/storage-blob-readme)
- [Azure Synapse](https://learn.microsoft.com/python/api/overview/azure/synapse-readme)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Delta Lake Documentation](https://docs.delta.io/latest/index.html)

---

*Last Updated: December 2025*
*Version: 1.0.0*
*Maintainer: CSA in-a-Box Team*
