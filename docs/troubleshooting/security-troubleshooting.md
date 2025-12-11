# Security Troubleshooting

> **[🏠 Home](../../README.md)** | **[📖 Documentation](../README.md)** | **[🔧 Troubleshooting](README.md)** | **👤 Security Issues**

![Status](https://img.shields.io/badge/Status-Active-brightgreen) ![Complexity](https://img.shields.io/badge/Complexity-Advanced-red)

Comprehensive guide for troubleshooting authentication, authorization, encryption, and security-related issues in Azure Synapse Analytics.

## Table of Contents

- [Overview](#overview)
- [Authentication Issues](#authentication-issues)
- [Authorization and Permissions](#authorization-and-permissions)
- [Managed Identity Issues](#managed-identity-issues)
- [Data Encryption Problems](#data-encryption-problems)
- [Network Security](#network-security)
- [Audit and Compliance](#audit-and-compliance)
- [Resolution Procedures](#resolution-procedures)

---

## Overview

Security issues in Azure Synapse can prevent access to workspaces, data, or services. This guide helps diagnose and resolve authentication failures, permission issues, managed identity problems, and encryption concerns.

> **🚨 Important:** Security incidents should be treated with high priority. Document all troubleshooting steps for compliance and audit purposes.

---

## Authentication Issues

### Issue 1: Azure AD Authentication Failure

**Symptoms:**
- Login failed for user
- Token validation errors
- Multi-factor authentication (MFA) failures
- "User is not authorized" messages

**Error Messages:**
```text
Error 18456: Login failed for user 'user@domain.com'
Error 40515: Reference to database and/or server name is not supported in this version
Error 40613: Database is currently unavailable (authentication context)
AADSTS errors (various Azure AD authentication errors)
```

**Step-by-Step Resolution:**

#### 1. Verify Azure AD Administrator

```bash
# Check current Azure AD admin
az synapse workspace show \
    --name <workspace-name> \
    --resource-group <rg-name> \
    --query "sqlAdministratorLogin"

# Get Azure AD admin details
az synapse workspace show \
    --name <workspace-name> \
    --resource-group <rg-name> \
    --query "azureAdAdministrators"
```

**PowerShell:**
```powershell
# Get workspace Azure AD admin
Get-AzSynapseWorkspace `
    -Name <workspace-name> `
    -ResourceGroupName <rg-name> |
    Select-Object -ExpandProperty ActiveDirectoryAdministrators
```

#### 2. Set Azure AD Administrator

```bash
# Set Azure AD admin using Azure CLI
az synapse workspace update \
    --name <workspace-name> \
    --resource-group <rg-name> \
    --sql-admin-login-user <admin-user@domain.com>
```

**Portal Steps:**
1. Navigate to Synapse workspace
2. Select **Azure Active Directory** under Security
3. Click **Set admin**
4. Search and select user or group
5. Click **Select**

#### 3. Test Azure AD Authentication

**Using sqlcmd:**
```bash
# Test with Azure AD interactive authentication
sqlcmd -S <workspace-name>.sql.azuresynapse.net -d master -G -U <user@domain.com>

# Test with Azure AD password authentication
sqlcmd -S <workspace-name>.sql.azuresynapse.net -d master -U <user@domain.com> -P <password> -G

# Test with Azure AD integrated authentication (Windows only)
sqlcmd -S <workspace-name>.sql.azuresynapse.net -d master -G
```

**Connection String Examples:**

```csharp
// C# - Azure AD Interactive
var connectionString = "Server=<workspace>.sql.azuresynapse.net;" +
                      "Authentication=Active Directory Interactive;" +
                      "Database=<db-name>;";

// C# - Azure AD Password
var connectionString = "Server=<workspace>.sql.azuresynapse.net;" +
                      "Authentication=Active Directory Password;" +
                      "UID=user@domain.com;PWD=password;" +
                      "Database=<db-name>;";

// C# - Azure AD Service Principal
var connectionString = "Server=<workspace>.sql.azuresynapse.net;" +
                      "Authentication=Active Directory Service Principal;" +
                      "UID=<app-id>;PWD=<client-secret>;" +
                      "Database=<db-name>;";
```

**Python:**
```python
import pyodbc

# Azure AD Interactive
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=<workspace>.sql.azuresynapse.net;"
    "DATABASE=<db-name>;"
    "Authentication=ActiveDirectoryInteractive;"
    "UID=user@domain.com"
)

connection = pyodbc.connect(conn_str)
```

#### 4. Check Azure AD Token

```bash
# Get Azure AD access token for troubleshooting
az account get-access-token \
    --resource https://database.windows.net/ \
    --query "{AccessToken:accessToken, ExpiresOn:expiresOn}" \
    --output json

# Decode token at https://jwt.ms to verify claims
```

**Common Token Issues:**
- **Expired Token**: Re-authenticate
- **Wrong Audience**: Ensure resource is `https://database.windows.net/`
- **Missing Claims**: Check group memberships and licenses

---

### Issue 2: Service Principal Authentication

**Symptoms:**
- Application cannot authenticate
- "Invalid client secret" errors
- "Application not found in directory" errors

**Diagnostic Steps:**

#### 1. Verify Service Principal

```bash
# Check if service principal exists
az ad sp show \
    --id <app-id> \
    --query "{DisplayName:displayName, AppId:appId, ObjectId:id}"

# List service principal credentials
az ad sp credential list \
    --id <app-id> \
    --query "[].{KeyId:keyId, EndDate:endDate}" \
    --output table
```

#### 2. Test Service Principal Authentication

```bash
# Login as service principal
az login --service-principal \
    --username <app-id> \
    --password <client-secret> \
    --tenant <tenant-id>

# Get access token
az account get-access-token \
    --resource https://database.windows.net/
```

#### 3. Grant Database Access

```sql
-- Connect as Azure AD admin and run:

-- Create user for service principal
CREATE USER [<app-name>] FROM EXTERNAL PROVIDER;

-- Grant permissions
ALTER ROLE db_datareader ADD MEMBER [<app-name>];
ALTER ROLE db_datawriter ADD MEMBER [<app-name>];

-- Or grant specific permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::dbo TO [<app-name>];

-- Verify permissions
SELECT
    dp.name AS user_name,
    dp.type_desc AS user_type,
    o.name AS object_name,
    p.permission_name,
    p.state_desc
FROM sys.database_permissions p
INNER JOIN sys.database_principals dp ON p.grantee_principal_id = dp.principal_id
LEFT JOIN sys.objects o ON p.major_id = o.object_id
WHERE dp.name = '<app-name>';
```

---

## Authorization and Permissions

### Issue 1: Access Denied to Database Objects

**Error Message:**
```text
The SELECT permission was denied on the object 'TableName', database 'DatabaseName', schema 'dbo'.
Msg 229, Level 14, State 5
```

**Diagnostic Queries:**

```sql
-- Check current user
SELECT USER_NAME() AS current_user,
       SUSER_SNAME() AS login_name,
       IS_SRVROLEMEMBER('sysadmin') AS is_sysadmin;

-- Check user permissions
SELECT
    pr.name AS principal_name,
    pr.type_desc AS principal_type,
    pe.permission_name,
    pe.state_desc,
    OBJECT_NAME(pe.major_id) AS object_name
FROM sys.database_permissions pe
INNER JOIN sys.database_principals pr ON pe.grantee_principal_id = pr.principal_id
WHERE pr.name = USER_NAME()
ORDER BY object_name, permission_name;

-- Check role memberships
SELECT
    USER_NAME() AS user_name,
    r.name AS role_name,
    r.type_desc
FROM sys.database_role_members rm
INNER JOIN sys.database_principals r ON rm.role_principal_id = r.principal_id
WHERE rm.member_principal_id = USER_ID();

-- Check object-level permissions
SELECT
    o.name AS object_name,
    o.type_desc AS object_type,
    dp.name AS grantee,
    dp.type_desc AS grantee_type,
    p.permission_name,
    p.state_desc
FROM sys.database_permissions p
INNER JOIN sys.objects o ON p.major_id = o.object_id
INNER JOIN sys.database_principals dp ON p.grantee_principal_id = dp.principal_id
WHERE o.name = '<table-name>'
ORDER BY dp.name, p.permission_name;
```

**Grant Access:**

```sql
-- Grant table-level permissions
GRANT SELECT ON dbo.TableName TO [user@domain.com];
GRANT INSERT, UPDATE, DELETE ON dbo.TableName TO [user@domain.com];

-- Grant schema-level permissions
GRANT SELECT ON SCHEMA::dbo TO [user@domain.com];
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::dbo TO [user@domain.com];

-- Add user to database role
ALTER ROLE db_datareader ADD MEMBER [user@domain.com];
ALTER ROLE db_datawriter ADD MEMBER [user@domain.com];

-- Create custom role
CREATE ROLE analytics_users;
GRANT SELECT ON SCHEMA::dbo TO analytics_users;
ALTER ROLE analytics_users ADD MEMBER [user@domain.com];
```

---

### Issue 2: Column-Level Security

**Symptoms:**
- Users can see some columns but not others
- Errors when selecting specific columns

**Implement Column-Level Security:**

```sql
-- Grant permission on specific columns
GRANT SELECT ON dbo.Customers (CustomerID, CustomerName, City) TO [user@domain.com];
GRANT UPDATE ON dbo.Customers (CustomerName, City) TO [user@domain.com];

-- Deny access to sensitive columns
DENY SELECT ON dbo.Customers (SSN, CreditCard) TO [user@domain.com];

-- Verify column permissions
SELECT
    o.name AS table_name,
    c.name AS column_name,
    dp.name AS grantee,
    p.permission_name,
    p.state_desc
FROM sys.database_permissions p
INNER JOIN sys.objects o ON p.major_id = o.object_id
INNER JOIN sys.columns c ON p.major_id = c.object_id AND p.minor_id = c.column_id
INNER JOIN sys.database_principals dp ON p.grantee_principal_id = dp.principal_id
WHERE o.name = 'Customers'
ORDER BY c.name, dp.name;
```

---

### Issue 3: Row-Level Security Not Working

**Symptoms:**
- Users see data they shouldn't
- Row-level security policy not filtering correctly

**Verify and Fix RLS:**

```sql
-- Check if RLS is enabled
SELECT
    s.name AS schema_name,
    t.name AS table_name,
    t.is_rls_enabled
FROM sys.tables t
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE t.name = '<table-name>';

-- Create RLS predicate function
CREATE FUNCTION dbo.fn_SecurityPredicate(@RegionID INT)
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN
    SELECT 1 AS result
    WHERE @RegionID = CAST(SESSION_CONTEXT(N'RegionID') AS INT)
        OR IS_MEMBER('db_owner') = 1;
GO

-- Create security policy
CREATE SECURITY POLICY dbo.RegionSecurityPolicy
ADD FILTER PREDICATE dbo.fn_SecurityPredicate(RegionID) ON dbo.Sales
WITH (STATE = ON);

-- Enable RLS on table
ALTER TABLE dbo.Sales SET (SYSTEM_VERSIONING = ON);

-- Set session context (user should do this)
EXEC sp_set_session_context @key = N'RegionID', @value = 1;

-- Test RLS
SELECT * FROM dbo.Sales; -- Should only show RegionID = 1

-- Disable RLS for troubleshooting
ALTER SECURITY POLICY dbo.RegionSecurityPolicy WITH (STATE = OFF);

-- Re-enable
ALTER SECURITY POLICY dbo.RegionSecurityPolicy WITH (STATE = ON);
```

---

## Managed Identity Issues

### Issue 1: System-Assigned Managed Identity Not Working

**Symptoms:**
- Cannot access storage accounts
- Authentication failures for Azure resources
- "Identity not found" errors

**Diagnostic Steps:**

#### 1. Verify Managed Identity is Enabled

```bash
# Check if managed identity is enabled
az synapse workspace show \
    --name <workspace-name> \
    --resource-group <rg-name> \
    --query "{Name:name, ManagedIdentity:identity.type, PrincipalId:identity.principalId}"

# Enable system-assigned managed identity
az synapse workspace update \
    --name <workspace-name> \
    --resource-group <rg-name> \
    --assign-identity
```

**PowerShell:**
```powershell
# Get managed identity details
Get-AzSynapseWorkspace `
    -Name <workspace-name> `
    -ResourceGroupName <rg-name> |
    Select-Object -ExpandProperty Identity

# Enable managed identity
Set-AzSynapseWorkspace `
    -Name <workspace-name> `
    -ResourceGroupName <rg-name> `
    -IdentityType SystemAssigned
```

#### 2. Grant Storage Access

```bash
# Get workspace principal ID
PRINCIPAL_ID=$(az synapse workspace show \
    --name <workspace-name> \
    --resource-group <rg-name> \
    --query "identity.principalId" \
    --output tsv)

# Grant Storage Blob Data Contributor role
az role assignment create \
    --assignee $PRINCIPAL_ID \
    --role "Storage Blob Data Contributor" \
    --scope "/subscriptions/<sub-id>/resourceGroups/<rg-name>/providers/Microsoft.Storage/storageAccounts/<storage-account>"

# Verify role assignment
az role assignment list \
    --assignee $PRINCIPAL_ID \
    --query "[].{Role:roleDefinitionName, Scope:scope}" \
    --output table
```

#### 3. Test Managed Identity Access

```sql
-- Test from SQL pool using OPENROWSET
SELECT TOP 10 *
FROM OPENROWSET(
    BULK 'https://<storage-account>.dfs.core.windows.net/<container>/<path>/*.parquet',
    FORMAT = 'PARQUET'
) AS data;

-- If error, check:
-- 1. Managed identity has correct role
-- 2. Storage firewall allows Synapse
-- 3. Network configuration
```

**Python (Spark):**
```python
# Test managed identity in Spark
from notebookutils import mssparkutils

# Set storage account using managed identity
spark.conf.set(
    f"fs.azure.account.auth.type.<storage-account>.dfs.core.windows.net",
    "OAuth"
)
spark.conf.set(
    f"fs.azure.account.oauth.provider.type.<storage-account>.dfs.core.windows.net",
    "org.apache.hadoop.fs.azurebfs.oauth2.MsiTokenProvider"
)
spark.conf.set(
    f"fs.azure.account.oauth2.msi.tenant.<storage-account>.dfs.core.windows.net",
    "<tenant-id>"
)

# Test read
df = spark.read.parquet("abfss://<container>@<storage-account>.dfs.core.windows.net/<path>")
df.show()
```

---

### Issue 2: User-Assigned Managed Identity

**Symptoms:**
- Need specific identity with pre-configured permissions
- Multiple workspaces sharing same identity

**Setup User-Assigned Managed Identity:**

```bash
# Create user-assigned managed identity
az identity create \
    --name <identity-name> \
    --resource-group <rg-name> \
    --location <region>

# Get identity details
IDENTITY_ID=$(az identity show \
    --name <identity-name> \
    --resource-group <rg-name> \
    --query "id" \
    --output tsv)

PRINCIPAL_ID=$(az identity show \
    --name <identity-name> \
    --resource-group <rg-name> \
    --query "principalId" \
    --output tsv)

# Assign to Synapse workspace
az synapse workspace update \
    --name <workspace-name> \
    --resource-group <rg-name> \
    --uai-action Add \
    --user-assigned-identities $IDENTITY_ID

# Grant permissions to storage
az role assignment create \
    --assignee $PRINCIPAL_ID \
    --role "Storage Blob Data Contributor" \
    --scope "/subscriptions/<sub-id>/resourceGroups/<rg-name>/providers/Microsoft.Storage/storageAccounts/<storage-account>"
```

---

## Data Encryption Problems

### Issue 1: Transparent Data Encryption (TDE)

**Symptoms:**
- Cannot access database after TDE changes
- Key rotation failures
- Performance degradation

**Check TDE Status:**

```sql
-- Check TDE status
SELECT
    db.name AS database_name,
    db.is_encrypted,
    dm.encryption_state,
    dm.percent_complete,
    dm.key_algorithm,
    dm.key_length
FROM sys.databases db
LEFT JOIN sys.dm_database_encryption_keys dm ON db.database_id = dm.database_id
WHERE db.name NOT IN ('master', 'tempdb', 'model', 'msdb');

-- Check encryption scan progress
SELECT
    database_id,
    encryption_state,
    CASE encryption_state
        WHEN 0 THEN 'No encryption'
        WHEN 1 THEN 'Unencrypted'
        WHEN 2 THEN 'Encryption in progress'
        WHEN 3 THEN 'Encrypted'
        WHEN 4 THEN 'Key change in progress'
        WHEN 5 THEN 'Decryption in progress'
        WHEN 6 THEN 'Protection change in progress'
    END AS encryption_state_desc,
    percent_complete,
    GETDATE() AS current_time
FROM sys.dm_database_encryption_keys;
```

**Enable/Disable TDE:**

```bash
# Azure CLI - Enable TDE with service-managed key
az synapse sql pool tde set \
    --workspace-name <workspace-name> \
    --sql-pool-name <pool-name> \
    --resource-group <rg-name> \
    --status Enabled

# Check TDE status
az synapse sql pool tde show \
    --workspace-name <workspace-name> \
    --sql-pool-name <pool-name> \
    --resource-group <rg-name>
```

---

### Issue 2: Customer-Managed Keys (CMK)

**Symptoms:**
- Key vault access denied
- Encryption key rotation failures
- Cannot access encrypted data

**Setup Customer-Managed Key:**

```bash
# Create Key Vault key
az keyvault key create \
    --vault-name <keyvault-name> \
    --name <key-name> \
    --protection software \
    --size 2048

# Get key URI
KEY_URI=$(az keyvault key show \
    --vault-name <keyvault-name> \
    --name <key-name> \
    --query "key.kid" \
    --output tsv)

# Grant workspace access to Key Vault
WORKSPACE_PRINCIPAL=$(az synapse workspace show \
    --name <workspace-name> \
    --resource-group <rg-name> \
    --query "identity.principalId" \
    --output tsv)

az keyvault set-policy \
    --name <keyvault-name> \
    --object-id $WORKSPACE_PRINCIPAL \
    --key-permissions get unwrapKey wrapKey

# Configure workspace encryption
az synapse workspace key create \
    --workspace-name <workspace-name> \
    --resource-group <rg-name> \
    --name <key-name> \
    --key-identifier $KEY_URI

# Activate the key
az synapse workspace update \
    --name <workspace-name> \
    --resource-group <rg-name> \
    --key-name <key-name>
```

**Troubleshoot CMK Issues:**

```bash
# Verify Key Vault access
az keyvault key show \
    --vault-name <keyvault-name> \
    --name <key-name>

# Check Key Vault diagnostic logs
az monitor diagnostic-settings list \
    --resource "/subscriptions/<sub-id>/resourceGroups/<rg-name>/providers/Microsoft.KeyVault/vaults/<keyvault-name>"

# Rotate key
az keyvault key rotate \
    --vault-name <keyvault-name> \
    --name <key-name>
```

---

## Network Security

### Issue 1: Firewall Blocking Access

**See also:** [Connectivity Troubleshooting](../07-troubleshooting/service-troubleshooting/synapse/connectivity.md)

**Quick Checks:**

```bash
# List firewall rules
az synapse workspace firewall-rule list \
    --workspace-name <workspace-name> \
    --resource-group <rg-name> \
    --output table

# Add current IP
MY_IP=$(curl -s https://api.ipify.org)
az synapse workspace firewall-rule create \
    --name "AllowMyIP" \
    --workspace-name <workspace-name> \
    --resource-group <rg-name> \
    --start-ip-address $MY_IP \
    --end-ip-address $MY_IP
```

---

### Issue 2: Private Link Configuration

**See also:** [Connectivity Troubleshooting](../07-troubleshooting/service-troubleshooting/synapse/connectivity.md#private-endpoints)

**Verify Private Endpoint:**

```bash
# List private endpoints
az network private-endpoint list \
    --resource-group <rg-name> \
    --query "[].{Name:name, State:privateLinkServiceConnections[0].privateLinkServiceConnectionState.status}" \
    --output table

# Test DNS resolution
nslookup <workspace-name>.sql.azuresynapse.net

# Should return private IP (10.x.x.x)
```

---

## Audit and Compliance

### Enable Auditing

```bash
# Enable workspace-level auditing
az synapse workspace audit-policy update \
    --workspace-name <workspace-name> \
    --resource-group <rg-name> \
    --state Enabled \
    --blob-storage-target-state Enabled \
    --storage-account <storage-account> \
    --storage-endpoint "https://<storage-account>.blob.core.windows.net"

# Enable SQL pool auditing
az synapse sql pool audit-policy update \
    --workspace-name <workspace-name> \
    --sql-pool-name <pool-name> \
    --resource-group <rg-name> \
    --state Enabled \
    --blob-storage-target-state Enabled \
    --storage-account <storage-account>
```

### Query Audit Logs

```sql
-- View audit logs (if using SQL pool)
SELECT
    event_time,
    action_name,
    succeeded,
    database_name,
    schema_name,
    object_name,
    statement,
    server_principal_name,
    client_ip
FROM sys.fn_get_audit_file(
    'https://<storage-account>.blob.core.windows.net/sqldbauditlogs/**/*.xel',
    DEFAULT,
    DEFAULT
)
WHERE event_time >= DATEADD(DAY, -7, GETDATE())
ORDER BY event_time DESC;
```

---

## Resolution Procedures

### Procedure 1: Reset User Access

**When to Use:** User reporting access denied

**Steps:**

1. **Verify User Exists:**
   ```sql
   SELECT name, type_desc, create_date
   FROM sys.database_principals
   WHERE name = 'user@domain.com';
   ```

2. **Drop and Recreate User:**
   ```sql
   DROP USER IF EXISTS [user@domain.com];
   CREATE USER [user@domain.com] FROM EXTERNAL PROVIDER;
   ```

3. **Grant Appropriate Permissions:**
   ```sql
   ALTER ROLE db_datareader ADD MEMBER [user@domain.com];
   ALTER ROLE db_datawriter ADD MEMBER [user@domain.com];
   ```

4. **Test Access:**
   ```sql
   -- Have user test connection and query
   ```

---

### Procedure 2: Managed Identity Troubleshooting

**When to Use:** Storage access failures

**Steps:**

1. **Verify Identity:**
   ```bash
   az synapse workspace show \
       --name <workspace-name> \
       --resource-group <rg-name> \
       --query "identity"
   ```

2. **Check Role Assignments:**
   ```bash
   az role assignment list \
       --assignee <principal-id> \
       --all
   ```

3. **Grant Required Access:**
   ```bash
   az role assignment create \
       --assignee <principal-id> \
       --role "Storage Blob Data Contributor" \
       --scope <storage-resource-id>
   ```

4. **Test Access:**
   ```sql
   SELECT TOP 1 * FROM OPENROWSET(...) AS data;
   ```

---

## When to Contact Support

Contact Microsoft Support if:

- [ ] Azure AD authentication fails despite correct configuration
- [ ] Managed identity permissions not working after verification
- [ ] TDE key rotation failures
- [ ] Suspected security breach or unauthorized access
- [ ] Compliance audit failures
- [ ] Private endpoint issues persist

**Information to Provide:**
- User/principal IDs involved
- Error messages and codes
- Timeline of issue
- Authentication method used
- Role assignments and permissions
- Network configuration details

---

## Related Resources

- [Authentication Troubleshooting](authentication-troubleshooting.md)
- [Connectivity Issues](../07-troubleshooting/service-troubleshooting/synapse/connectivity.md)
- [Security Best Practices](../best-practices/security.md)
- [Network Security](../best-practices/network-security.md)
- [Azure Synapse Security Documentation](https://docs.microsoft.com/azure/synapse-analytics/security/synapse-workspace-security-overview)

---

> **🔒 Security Reminder:** Always follow the principle of least privilege. Grant only the minimum permissions required for users to perform their tasks.
