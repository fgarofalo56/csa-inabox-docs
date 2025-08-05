# PLACEHOLDER FOR DATA CLASSIFICATION FRAMEWORK

This file serves as a placeholder for the static image rendering of the Data Classification Framework diagram.

## Diagram Description

This diagram illustrates a comprehensive data classification framework for Azure Synapse Analytics, featuring:

- Classification Levels (Public, Internal, Confidential, Restricted)
- Regulatory Categories (PII, PCI DSS, IP, Corporate Data)
- Implementation through Sensitivity Labels in Microsoft Purview
- Protection methods including SQL Classification, Data Loss Prevention, Row-Level Security, Column-Level Security, Dynamic Data Masking, and Encryption

## Original Mermaid Code

```mermaid
graph TD
    subgraph "Classification Levels"
        PUBLIC[Public]
        INTERNAL[Internal]
        CONFID[Confidential]
        RESTRICT[Restricted]
    end
    
    subgraph "Regulatory Categories"
        PII[Personally Identifiable Information]
        PCI[Payment Card Information]
        IP[Intellectual Property]
        CORP[Corporate Data]
    end
    
    subgraph "Implementation"
        LABELS[Sensitivity Labels]
        PURVIEW[Microsoft Purview]
    end
    
    subgraph "SQL Protection"
        SQL_CLASS[SQL Classification]
        MASK[Dynamic Data Masking]
        ENCRYPT[Transparent Data Encryption]
        RLS[Row-Level Security]
        CLS[Column-Level Security]
    end
    
    subgraph "Storage Protection"
        DLP[Data Loss Prevention]
        ACL[Access Control Lists]
    end
    
    PUBLIC --> LABELS
    INTERNAL --> LABELS
    CONFID --> LABELS
    RESTRICT --> LABELS
    
    PII --> LABELS
    PCI --> LABELS
    IP --> LABELS
    CORP --> LABELS
    
    LABELS --> PURVIEW
    PURVIEW --> SQL_CLASS
    PURVIEW --> DLP
    
    SQL_CLASS --> MASK
    SQL_CLASS --> ENCRYPT
    SQL_CLASS --> RLS
    SQL_CLASS --> CLS
    
    DLP --> ACL
```

## Instructions for Implementation

Replace this markdown file with an actual PNG image exported from a Mermaid rendering tool.
