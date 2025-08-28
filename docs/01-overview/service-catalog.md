# 📖 Azure Cloud Scale Analytics Service Catalog

> **🏠 [Home](../../README.md)** | **📖 [Overview](README.md)** | **📋 Service Catalog**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Coverage](https://img.shields.io/badge/Services-15+-blue?style=flat-square)
![Updated](https://img.shields.io/badge/Updated-2025--01-green?style=flat-square)

Complete catalog of Azure analytics services with capabilities, use cases, and decision guidance.

---

## 📊 Service Overview Matrix

| Service | Category | Complexity | Pricing Model | Primary Use Case |
|---------|----------|------------|---------------|------------------|
| **Azure Synapse Analytics** | Analytics Compute | ![Advanced](https://img.shields.io/badge/-Advanced-red) | Pay-per-use + Reserved | Enterprise Data Warehousing |
| **Azure Databricks** | Analytics Compute | ![Advanced](https://img.shields.io/badge/-Advanced-red) | Compute + DBU | Data Science & ML |
| **HDInsight** | Analytics Compute | ![Intermediate](https://img.shields.io/badge/-Intermediate-yellow) | VM-based | Big Data Processing |
| **Stream Analytics** | Streaming | ![Intermediate](https://img.shields.io/badge/-Intermediate-yellow) | Streaming Units | Real-time Analytics |
| **Event Hubs** | Streaming | ![Basic](https://img.shields.io/badge/-Basic-green) | Throughput Units | Event Ingestion |
| **Event Grid** | Streaming | ![Basic](https://img.shields.io/badge/-Basic-green) | Per Operation | Event Routing |
| **Data Lake Gen2** | Storage | ![Basic](https://img.shields.io/badge/-Basic-green) | Storage + Transactions | Big Data Storage |
| **Cosmos DB** | Storage | ![Intermediate](https://img.shields.io/badge/-Intermediate-yellow) | Request Units | NoSQL Database |
| **Azure SQL** | Storage | ![Intermediate](https://img.shields.io/badge/-Intermediate-yellow) | vCore or DTU | Relational Database |
| **Data Factory** | Orchestration | ![Intermediate](https://img.shields.io/badge/-Intermediate-yellow) | Pipeline Runs | Data Integration |
| **Logic Apps** | Orchestration | ![Basic](https://img.shields.io/badge/-Basic-green) | Action-based | Workflow Automation |

---

## 🎯 Analytics Compute Services

### Azure Synapse Analytics ![Enterprise](https://img.shields.io/badge/Tier-Enterprise-purple)

**Purpose**: Unified analytics service combining data integration, data warehousing, and analytics.

**Key Capabilities**:
- **Serverless SQL Pools**: Query data directly from data lake
- **Dedicated SQL Pools**: Enterprise data warehousing
- **Spark Pools**: Big data processing and machine learning
- **Data Integration**: Built-in ETL/ELT pipelines
- **Shared Metadata**: Unified catalog across compute engines

**Best For**:
- Enterprise data warehousing
- Unified analytics workspaces
- Large-scale data processing
- Self-service analytics

**Pricing**: Pay-per-query (serverless) + Reserved capacity (dedicated)

**Documentation**: [Azure Synapse Guide](../02-services/analytics-compute/azure-synapse/README.md)

---

### Azure Databricks ![Data Science](https://img.shields.io/badge/Tier-Data%20Science-orange)

**Purpose**: Collaborative analytics platform optimized for machine learning and data science.

**Key Capabilities**:
- **Collaborative Notebooks**: Multi-language data science environment
- **Delta Live Tables**: Declarative ETL framework
- **MLflow Integration**: End-to-end ML lifecycle management
- **Unity Catalog**: Unified data governance
- **Photon Engine**: High-performance query engine

**Best For**:
- Data science and machine learning
- Collaborative analytics
- Advanced data engineering
- Real-time ML inference

**Pricing**: Compute costs + Databricks Unit (DBU) charges

**Documentation**: [Azure Databricks Guide](../02-services/analytics-compute/azure-databricks/README.md)

---

### HDInsight ![Migration](https://img.shields.io/badge/Tier-Migration-blue)

**Purpose**: Managed Apache Hadoop, Spark, and Kafka clusters in Azure.

**Key Capabilities**:
- **Multiple Cluster Types**: Hadoop, Spark, HBase, Kafka, Storm
- **Enterprise Security**: ESP integration with Active Directory
- **Custom Applications**: Support for custom Hadoop ecosystem tools
- **Hybrid Connectivity**: Integration with on-premises systems

**Best For**:
- Hadoop migration to cloud
- Custom big data applications
- Cost-optimized big data processing
- Open-source ecosystem requirements

**Pricing**: VM-based pricing model

**Documentation**: [HDInsight Guide](../02-services/analytics-compute/azure-hdinsight/README.md)

---

## 🔄 Streaming Services

### Azure Stream Analytics ![Real-time](https://img.shields.io/badge/Type-Real%20time-brightgreen)

**Purpose**: Real-time analytics service for streaming data processing.

**Key Capabilities**:
- **SQL-based Queries**: Familiar SQL syntax for stream processing
- **Windowing Functions**: Tumbling, hopping, and sliding windows
- **Anomaly Detection**: Built-in ML-based anomaly detection
- **Edge Deployment**: Run analytics on IoT Edge devices
- **Output Integration**: Direct integration with Power BI, SQL, Cosmos DB

**Best For**:
- IoT device telemetry processing
- Real-time dashboards
- Fraud detection
- Operational monitoring

**Pricing**: Streaming Units (SU) hourly billing

**Documentation**: [Stream Analytics Guide](../02-services/streaming-services/azure-stream-analytics/README.md)

---

### Azure Event Hubs ![Ingestion](https://img.shields.io/badge/Type-Ingestion-yellow)

**Purpose**: Big data streaming platform and event ingestion service.

**Key Capabilities**:
- **High Throughput**: Millions of events per second
- **Kafka Compatibility**: Drop-in replacement for Apache Kafka
- **Capture Feature**: Automatic data archival to storage
- **Schema Registry**: Centralized schema management
- **Dedicated Clusters**: Isolated, high-performance clusters

**Best For**:
- High-volume event ingestion
- Kafka migration scenarios
- Event-driven architectures
- IoT data collection

**Pricing**: Throughput Units or Dedicated Cluster Units

**Documentation**: [Event Hubs Guide](../02-services/streaming-services/azure-event-hubs/README.md)

---

### Azure Event Grid ![Routing](https://img.shields.io/badge/Type-Routing-lightblue)

**Purpose**: Event routing service for building event-driven applications.

**Key Capabilities**:
- **Event Routing**: Intelligent event routing to multiple destinations
- **Custom Topics**: Create custom event publishers
- **System Topics**: Built-in events from Azure services
- **Dead Letter Queues**: Handle failed event deliveries
- **Event Filtering**: Route events based on content

**Best For**:
- Event-driven application architectures
- Serverless workflows
- System integration
- Reactive applications

**Pricing**: Pay-per-operation model

**Documentation**: [Event Grid Guide](../02-services/streaming-services/azure-event-grid/README.md)

---

## 🗃️ Storage Services

### Azure Data Lake Storage Gen2 ![Big Data](https://img.shields.io/badge/Type-Big%20Data-darkgreen)

**Purpose**: Hierarchical namespace storage optimized for big data analytics.

**Key Capabilities**:
- **Hierarchical Namespace**: Directory and file-level operations
- **Fine-grained ACLs**: POSIX-compliant access control
- **Multi-protocol Access**: Blob and Data Lake APIs
- **Lifecycle Management**: Automated data tiering and archival
- **Performance Tiers**: Hot, cool, and archive storage

**Best For**:
- Data lake implementations
- Big data analytics storage
- Data archival and backup
- Multi-format data storage

**Pricing**: Storage capacity + transaction costs

**Documentation**: [Data Lake Gen2 Guide](../02-services/storage-services/azure-data-lake-gen2/README.md)

---

### Azure Cosmos DB ![NoSQL](https://img.shields.io/badge/Type-NoSQL-purple)

**Purpose**: Globally distributed, multi-model NoSQL database service.

**Key Capabilities**:
- **Multiple APIs**: SQL, MongoDB, Cassandra, Gremlin, Table
- **Global Distribution**: Multi-region writes and reads
- **Analytical Store**: HTAP capabilities with Synapse Link
- **Change Feed**: Real-time change data capture
- **Serverless Option**: Pay-per-request pricing model

**Best For**:
- Globally distributed applications
- Real-time applications requiring low latency
- Multi-model data scenarios
- HTAP workloads with Synapse integration

**Pricing**: Request Units (RU/s) or serverless

**Documentation**: [Cosmos DB Guide](../02-services/storage-services/azure-cosmos-db/README.md)

---

### Azure SQL Database ![Relational](https://img.shields.io/badge/Type-Relational-blue)

**Purpose**: Fully managed relational database service.

**Key Capabilities**:
- **Hyperscale**: Massively scalable database architecture
- **Elastic Pools**: Shared resources across multiple databases
- **Built-in Intelligence**: Automatic tuning and threat detection
- **Always Encrypted**: Column-level encryption
- **Temporal Tables**: Built-in data history tracking

**Best For**:
- Relational data workloads
- Transactional applications
- Data marts and reporting
- Application modernization

**Pricing**: vCore-based or DTU-based models

**Documentation**: [Azure SQL Guide](../02-services/storage-services/azure-sql-database/README.md)

---

## 🔧 Orchestration Services

### Azure Data Factory ![ETL](https://img.shields.io/badge/Type-ETL-orange)

**Purpose**: Cloud-based data integration service for creating ETL/ELT pipelines.

**Key Capabilities**:
- **Code-free ETL**: Visual pipeline designer
- **Data Flows**: Transformation logic with Spark execution
- **Hybrid Integration**: On-premises and cloud data sources
- **CI/CD Support**: Azure DevOps and GitHub integration
- **Monitoring**: Built-in pipeline monitoring and alerting

**Best For**:
- Data integration pipelines
- ETL/ELT processes
- Data migration projects
- Scheduled data processing

**Pricing**: Pipeline orchestration + activity execution costs

**Documentation**: [Data Factory Guide](../02-services/orchestration-services/azure-data-factory/README.md)

---

### Azure Logic Apps ![Workflow](https://img.shields.io/badge/Type-Workflow-green)

**Purpose**: Serverless workflow automation service.

**Key Capabilities**:
- **Visual Designer**: Drag-and-drop workflow creation
- **300+ Connectors**: Pre-built connectors for popular services
- **B2B Integration**: EDI and AS2 support
- **Event-driven**: Trigger-based workflow execution
- **Enterprise Integration**: Integration with on-premises systems

**Best For**:
- Business process automation
- System integrations
- Event-driven workflows
- B2B data exchange

**Pricing**: Pay-per-action execution

**Documentation**: [Logic Apps Guide](../02-services/orchestration-services/azure-logic-apps/README.md)

---

## 🎯 Service Selection Guide

### By Use Case

#### Real-time Analytics
**Primary**: Stream Analytics, Event Hubs
**Storage**: Cosmos DB, Data Lake Gen2
**Visualization**: Power BI Real-time Dashboards

#### Data Warehousing
**Primary**: Synapse Dedicated SQL Pools
**Storage**: Data Lake Gen2, Azure SQL
**Orchestration**: Data Factory

#### Data Science & ML
**Primary**: Databricks, Synapse Spark Pools
**Storage**: Data Lake Gen2, Cosmos DB
**Orchestration**: Data Factory, Databricks Workflows

#### IoT Analytics
**Primary**: Stream Analytics, Event Hubs
**Edge**: Stream Analytics on IoT Edge
**Storage**: Data Lake Gen2, Cosmos DB

### By Data Volume

#### Small to Medium (< 1TB)
- Azure SQL Database
- Cosmos DB
- Stream Analytics (< 100 SU)

#### Large (1-100TB)
- Synapse Dedicated SQL Pools
- Databricks
- HDInsight

#### Very Large (> 100TB)
- Synapse Serverless SQL Pools
- Data Lake Gen2 with Synapse
- Databricks with Delta Lake

### By Budget Considerations

#### Cost-Optimized
- HDInsight
- Synapse Serverless SQL Pools
- Event Grid

#### Balanced Performance/Cost
- Stream Analytics
- Data Factory
- Cosmos DB (provisioned throughput)

#### Performance-Optimized
- Synapse Dedicated SQL Pools
- Databricks Premium
- Event Hubs Dedicated Clusters

---

## 📊 Service Comparison Matrix

### Analytics Compute Comparison

| Feature | Synapse | Databricks | HDInsight |
|---------|---------|------------|-----------|
| **SQL Support** | ✅ Native | ✅ Spark SQL | ✅ Hive/SparkSQL |
| **Python/R** | ✅ Spark | ✅ Native | ✅ Spark |
| **Scala/Java** | ✅ Spark | ✅ Native | ✅ Native |
| **ML Integration** | ✅ Built-in | ✅ MLflow | ⚠️ Custom |
| **Serverless** | ✅ Yes | ❌ No | ❌ No |
| **Auto-scaling** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Enterprise Security** | ✅ AAD | ✅ Unity Catalog | ✅ ESP |
| **Cost Model** | Pay-per-use | DBU-based | VM-based |

### Streaming Services Comparison

| Feature | Stream Analytics | Event Hubs | Event Grid |
|---------|-----------------|------------|------------|
| **Processing** | ✅ Built-in | ❌ Storage only | ❌ Routing only |
| **Throughput** | Medium (SU-based) | ✅ Very High | High |
| **Latency** | Sub-second | Milliseconds | Seconds |
| **SQL Queries** | ✅ Yes | ❌ No | ❌ No |
| **Schema Registry** | ❌ No | ✅ Yes | ❌ No |
| **Event Filtering** | ✅ Yes | ❌ No | ✅ Yes |
| **Cost Model** | SU hourly | TU/CU | Per operation |

---

## 🔗 Next Steps

### 🚀 Quick Starts
- [**Get Started Guide**](../01-overview/README.md#quick-links)
- [**Architecture Patterns**](architecture-patterns.md)
- [**Service Decision Tree**](choosing-services.md)

### 📖 Deep Dive Documentation
- [**Services Documentation**](../02-services/README.md)
- [**Implementation Guides**](../04-implementation-guides/README.md)
- [**Best Practices**](../05-best-practices/README.md)

### 🛠️ Hands-on Learning
- [**Code Examples**](../06-code-examples/README.md)
- [**Tutorials**](../tutorials/README.md)
- [**Reference Architectures**](../03-architecture-patterns/reference-architectures/README.md)

---

*Last Updated: 2025-01-28*  
*Next Review: 2025-04-28*