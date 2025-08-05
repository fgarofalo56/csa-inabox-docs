# PLACEHOLDER FOR DEFENSE-IN-DEPTH SECURITY ARCHITECTURE DIAGRAM

This file serves as a placeholder for the static image rendering of the Defense-in-Depth Security Architecture diagram.

## Diagram Description

This diagram illustrates the defense-in-depth security model for Azure Synapse Analytics with four key layers:

- Network Security layer with Private Endpoints, Network Security Groups, Azure Firewall, and Virtual Network
- Identity & Access layer with Azure Active Directory, RBAC, Managed Identities, and Conditional Access
- Data Protection layer with Customer Managed Keys, Data Encryption, Advanced Threat Protection, and Private DNS
- Monitoring & Compliance layer with Log Analytics, Microsoft Defender for Cloud, Diagnostic Logs, and Azure Sentinel

## Instructions for Implementation

Replace this markdown file with an actual PNG image exported from a Mermaid rendering tool.

Original Mermaid Source:
```mermaid
graph TD
    subgraph "Network Security"
        PEP[Private Endpoints]
        NSG[Network Security Groups]
        FW[Azure Firewall]
        VNET[Virtual Network]
    end

    subgraph "Identity & Access"
        AAD[Azure Active Directory]
        RBAC[Role-Based Access Control]
        MSI[Managed Identities]
        COND[Conditional Access]
    end

    subgraph "Data Protection"
        CMK[Customer Managed Keys]
        DE[Data Encryption]
        ATP[Advanced Threat Protection]
        PD[Private DNS]
    end

    subgraph "Monitoring & Compliance"
        LA[Log Analytics]
        MDFC[Microsoft Defender for Cloud]
        DIAG[Diagnostic Logs]
        SIEM[Azure Sentinel]
    end

    VNET --> PEP
    VNET --> NSG
    FW --> VNET
    
    AAD --> RBAC
    AAD --> MSI
    AAD --> COND
    
    DE --> CMK
    ATP --> DE
    PD --> PEP
```
