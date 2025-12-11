# Compliance Guide

> **[Home](../../README.md)** | **[Security](../security)** | **Compliance Guide**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Category](https://img.shields.io/badge/Category-Security-red?style=flat-square)

Compliance guidance for Cloud Scale Analytics on Azure.

---

## Overview

This guide covers compliance requirements for:

- GDPR (General Data Protection Regulation)
- HIPAA (Health Insurance Portability and Accountability Act)
- SOC 2 (Service Organization Control 2)
- PCI DSS (Payment Card Industry Data Security Standard)
- Azure compliance certifications

---

## GDPR Compliance

### Key Requirements

| Requirement | Implementation |
|-------------|----------------|
| Data Subject Rights | Implement data access/deletion APIs |
| Consent Management | Track consent in metadata |
| Data Minimization | Collect only necessary data |
| Breach Notification | Enable monitoring and alerting |
| Data Protection | Encrypt data at rest and in transit |

### Implementation

```python
# Data subject deletion (Right to be Forgotten)
from delta.tables import DeltaTable

def delete_customer_data(customer_id: str):
    """Delete all data for a customer (GDPR compliance)."""

    tables = ["bronze.customers", "silver.customer_orders", "gold.customer_analytics"]

    for table in tables:
        delta_table = DeltaTable.forName(spark, table)
        delta_table.delete(f"customer_id = '{customer_id}'")

    # Log deletion for audit
    log_gdpr_action("DELETE", customer_id)
```

---

## HIPAA Compliance

### Security Controls

1. **Access Controls**: Role-based access with audit logging
2. **Audit Controls**: Complete activity logging
3. **Integrity Controls**: Data validation and checksums
4. **Transmission Security**: TLS 1.2+ for all connections

### PHI Protection

```sql
-- Column-level encryption for PHI
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'strong_password';

CREATE CERTIFICATE PHI_Certificate WITH SUBJECT = 'PHI Encryption';

CREATE SYMMETRIC KEY PHI_Key
WITH ALGORITHM = AES_256
ENCRYPTION BY CERTIFICATE PHI_Certificate;

-- Encrypt sensitive columns
UPDATE patients
SET ssn_encrypted = EncryptByKey(Key_GUID('PHI_Key'), ssn);
```

---

## SOC 2 Compliance

### Trust Service Criteria

| Criteria | Azure Controls |
|----------|---------------|
| Security | Network isolation, encryption, IAM |
| Availability | SLA, redundancy, DR |
| Processing Integrity | Data validation, monitoring |
| Confidentiality | Encryption, access controls |
| Privacy | Data governance, consent |

---

## PCI DSS Compliance

### Requirements

1. **Network Security**: Private endpoints, NSGs, firewalls
2. **Data Protection**: Encryption, tokenization
3. **Access Control**: Least privilege, MFA
4. **Monitoring**: Log all access to cardholder data
5. **Testing**: Regular vulnerability scans

### Tokenization Example

```python
# Tokenize PCI data
import hashlib
import secrets

def tokenize_pan(pan: str, salt: str) -> str:
    """Tokenize payment card number."""
    token = hashlib.sha256(f"{pan}{salt}".encode()).hexdigest()[:16]
    return f"TKN_{token}"

def store_pan_securely(pan: str) -> str:
    """Store PAN with tokenization."""
    salt = secrets.token_hex(16)
    token = tokenize_pan(pan, salt)

    # Store mapping in secure vault
    store_in_vault(token, pan, salt)

    return token
```

---

## Audit Logging

### Enable Comprehensive Logging

```bash
# Enable diagnostic settings
az monitor diagnostic-settings create \
    --name "compliance-logging" \
    --resource "/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Synapse/workspaces/{ws}" \
    --workspace "/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.OperationalInsights/workspaces/{law}" \
    --logs '[
        {"category": "SynapseRbacOperations", "enabled": true},
        {"category": "GatewayApiRequests", "enabled": true},
        {"category": "SQLSecurityAuditEvents", "enabled": true},
        {"category": "BuiltinSqlReqsEnded", "enabled": true}
    ]'
```

### Query Audit Logs

```kql
// Access audit
SynapseSqlPoolSecurityAuditEvents
| where TimeGenerated > ago(24h)
| where ActionName in ("SELECT", "INSERT", "UPDATE", "DELETE")
| project TimeGenerated, ActionName, ServerPrincipalName, DatabaseName, ObjectName
| summarize AccessCount = count() by ServerPrincipalName, ActionName
```

---

## Compliance Checklist

### Monthly Tasks

- [ ] Review access permissions
- [ ] Audit data access logs
- [ ] Verify encryption status
- [ ] Test backup restoration
- [ ] Update security patches

### Quarterly Tasks

- [ ] Vulnerability assessment
- [ ] Penetration testing
- [ ] Policy review
- [ ] Training verification

---

## Related Documentation

- [Security Best Practices](../../best-practices/security/README.md)
- [Network Security](../../best-practices/network-security/README.md)
- [Data Governance](../../best-practices/data-governance/README.md)

---

*Last Updated: January 2025*
