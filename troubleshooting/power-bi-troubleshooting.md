# Power BI Troubleshooting

> **[Home](../README.md)** | **[Troubleshooting](index.md)** | **Power BI**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Complexity](https://img.shields.io/badge/Complexity-Intermediate-yellow?style=flat-square)

Troubleshooting guide for Power BI integration with Cloud Scale Analytics.

---

## Common Issues

### 1. Connection Issues

#### DirectQuery to Synapse Serverless SQL

**Symptoms:**
- Connection timeout
- "Unable to connect" errors
- Slow initial connection

**Solutions:**

1. **Check Firewall Rules**
   ```bash
   az synapse workspace firewall-rule create \
       --workspace-name synapse-workspace \
       --name allow-powerbi \
       --start-ip-address 0.0.0.0 \
       --end-ip-address 255.255.255.255
   ```

2. **Use Service Principal Authentication**
   ```
   Server: synapse-workspace-ondemand.sql.azuresynapse.net
   Database: database_name
   Authentication: Azure Active Directory
   ```

3. **Verify AAD Permissions**
   - Ensure user has `db_datareader` role
   - Grant CONNECT permission on database

#### DirectQuery to Dedicated SQL Pool

**Connection String Format:**
```
Server=synapse-workspace.sql.azuresynapse.net;
Database=dedicated_pool;
Encrypt=True;
TrustServerCertificate=False;
Connection Timeout=30;
```

---

### 2. Performance Issues

#### Slow Report Load Times

**Diagnostic Steps:**

1. **Enable Performance Analyzer**
   - View > Performance Analyzer
   - Start Recording
   - Refresh visuals
   - Review DAX query times

2. **Optimize DAX Queries**
   ```dax
   // Inefficient - iterating row by row
   Sales Amount Bad = SUMX(Sales, Sales[Quantity] * Sales[Price])

   // Efficient - using aggregation
   Sales Amount Good = SUMX(
       VALUES(Sales[ProductID]),
       CALCULATE(SUM(Sales[Quantity]) * MAX(Sales[Price]))
   )
   ```

3. **Reduce Data Volume**
   ```sql
   -- Create aggregated view for Power BI
   CREATE VIEW vw_SalesSummary AS
   SELECT
       CAST(OrderDate AS DATE) AS OrderDate,
       ProductCategory,
       Region,
       SUM(Amount) AS TotalAmount,
       COUNT(*) AS OrderCount
   FROM Sales
   GROUP BY
       CAST(OrderDate AS DATE),
       ProductCategory,
       Region;
   ```

#### Query Folding Issues

**Check Query Folding:**
- Right-click step in Power Query
- Select "View Native Query"
- If grayed out, query folding is not occurring

**Enable Query Folding:**
```m
// Power Query - push filters to source
let
    Source = Sql.Database("server", "database"),
    FilteredRows = Table.SelectRows(
        Source{[Schema="dbo",Item="Sales"]}[Data],
        each [OrderDate] >= #date(2024,1,1)
    )
in
    FilteredRows
```

---

### 3. Refresh Failures

#### Scheduled Refresh Errors

**Common Errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| Credentials expired | Token timeout | Re-enter credentials in dataset settings |
| Gateway offline | IR not running | Restart gateway service |
| Query timeout | Long-running query | Optimize source query or increase timeout |
| Memory exceeded | Large dataset | Enable incremental refresh |

#### Configure Incremental Refresh

```m
// Power Query Parameters
RangeStart = #datetime(2024, 1, 1, 0, 0, 0)
RangeEnd = #datetime(2024, 12, 31, 23, 59, 59)

// Filter in query
let
    Source = Sql.Database("server", "database"),
    FilteredData = Table.SelectRows(
        Source{[Schema="dbo",Item="Sales"]}[Data],
        each [OrderDate] >= RangeStart and [OrderDate] < RangeEnd
    )
in
    FilteredData
```

**Incremental Refresh Policy:**
- Archive data: 3 years
- Incremental data: 30 days
- Detect data changes: Yes (using LastModified column)

---

### 4. Gateway Issues

#### On-Premises Data Gateway

**Check Gateway Status:**
```powershell
# Run on gateway machine
Get-Service "PBIEgwService"

# Check gateway logs
Get-EventLog -LogName Application -Source "On-premises data gateway" -Newest 50
```

**Common Fixes:**

1. **Update Gateway**
   - Download latest version
   - Run installer (preserves configuration)

2. **Configure Proxy**
   ```xml
   <!-- Microsoft.PowerBI.EnterpriseGateway.exe.config -->
   <system.net>
       <defaultProxy useDefaultCredentials="true">
           <proxy proxyaddress="http://proxy:8080" bypassonlocal="true"/>
       </defaultProxy>
   </system.net>
   ```

3. **Increase Timeout**
   ```xml
   <setting name="ADMashupQueryTimeout" serializeAs="String">
       <value>00:30:00</value>
   </setting>
   ```

---

### 5. Visual and Report Issues

#### Missing or Incorrect Data

**Diagnostic Steps:**

1. **Check Relationships**
   - Model view > Verify cardinality
   - Check cross-filter direction
   - Look for ambiguous relationships

2. **Verify Measures Context**
   ```dax
   // Debug measure with filter context
   Debug Measure =
   VAR CurrentFilters = CONCATENATEX(
       FILTERS(Table[Column]),
       Table[Column],
       ", "
   )
   RETURN CurrentFilters
   ```

3. **Check Row-Level Security**
   ```dax
   // RLS filter
   [Region] = USERPRINCIPALNAME()

   // Test RLS
   // View as > Select role > Enter username
   ```

#### Export Issues

**Large Export Failures:**
- Maximum rows: 150,000 (Excel), 30,000 (CSV)
- Use paginated reports for larger exports
- Enable "Allow end users to export underlying data"

---

## Monitoring and Diagnostics

### Power BI Activity Log

```powershell
# Get Power BI activity events
Connect-PowerBIServiceAccount
Get-PowerBIActivityEvent -StartDateTime (Get-Date).AddDays(-7) -EndDateTime (Get-Date) |
    ConvertFrom-Json |
    Where-Object { $_.Activity -eq "ViewReport" }
```

### Premium Capacity Metrics

```dax
// Query performance metrics
Premium Capacity Metrics =
SUMMARIZE(
    QueryMetrics,
    QueryMetrics[ReportName],
    "Avg Duration", AVERAGE(QueryMetrics[Duration]),
    "Max Duration", MAX(QueryMetrics[Duration]),
    "Query Count", COUNT(QueryMetrics[QueryID])
)
```

---

## Best Practices

### Performance Optimization Checklist

- [ ] Use Import mode when possible (vs DirectQuery)
- [ ] Implement aggregations for large datasets
- [ ] Enable query folding in Power Query
- [ ] Limit visuals per page (< 8 recommended)
- [ ] Use Star schema model design
- [ ] Avoid bidirectional relationships
- [ ] Remove unused columns and tables

### Security Checklist

- [ ] Implement Row-Level Security
- [ ] Use service principals for automation
- [ ] Configure workspace access appropriately
- [ ] Enable sensitivity labels for data classification

---

## Related Documentation

- [Power BI Integration](../docs/tutorials/integration/power-bi/README.md)
- [Power BI Optimization](../docs/05-best-practices/power-bi-optimization.md)
- [Serverless SQL for Power BI](../docs/02-services/analytics-compute/azure-synapse/serverless-sql/README.md)

---

*Last Updated: January 2025*
