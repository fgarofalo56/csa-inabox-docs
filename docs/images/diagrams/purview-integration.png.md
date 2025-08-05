# PLACEHOLDER FOR MICROSOFT PURVIEW INTEGRATION ARCHITECTURE

This file serves as a placeholder for the static image rendering of the Microsoft Purview Integration Architecture diagram.

## Diagram Description

This diagram illustrates how Microsoft Purview integrates with Azure Synapse Analytics for comprehensive data governance, featuring:

- Microsoft Purview components (Data Catalog, Scanning, Classifications, Glossary, Insights)
- Azure Synapse Analytics components (Workspace, SQL Pools, Serverless SQL, Spark Pools, ADLS)
- Integration points showing how Purview catalogs, scans, classifies, and monitors Synapse resources
- Data lineage tracking across the entire Synapse environment

## Original Mermaid Code

```mermaid
graph TB
    subgraph "Microsoft Purview"
        CATALOG[Data Catalog]
        SCANNING[Automated Scanning]
        CLASS[Classifications & Labels]
        LINEAGE[Data Lineage]
        GLOSSARY[Business Glossary]
        INSIGHTS[Data Insights]
    end
    
    subgraph "Azure Synapse Analytics"
        WORKSPACE[Synapse Workspace]
        SQLPOOL[Dedicated SQL Pool]
        SQLSERVER[Serverless SQL]
        SPARK[Spark Pools]
        ADLS[Data Lake Storage]
    end
    
    CATALOG --"Catalogs Assets in"--> WORKSPACE
    CATALOG --"Registers Tables in"--> SQLPOOL
    CATALOG --"Indexes Data in"--> ADLS
    
    SCANNING --"Scans"--> SQLPOOL
    SCANNING --"Discovers"--> SQLSERVER
    SCANNING --"Monitors"--> ADLS
    
    CLASS --"Classifies Data in"--> SQLPOOL
    CLASS --"Applies Labels to"--> ADLS
    
    LINEAGE --"Tracks Data Movement in"--> WORKSPACE
    LINEAGE --"Maps Transformations in"--> SQLPOOL
    LINEAGE --"Visualizes Code in"--> SPARK
    
    GLOSSARY --"Defines Terms"--> SQLPOOL
    GLOSSARY --"Standardizes Naming"--> SPARK
    
    INSIGHTS --"Reports on"--> WORKSPACE
    INSIGHTS --"Analyzes"--> SQLPOOL
    INSIGHTS --"Monitors"--> ADLS
```

## Instructions for Implementation

Replace this markdown file with an actual PNG image exported from a Mermaid rendering tool.
