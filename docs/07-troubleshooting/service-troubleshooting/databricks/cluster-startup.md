# Azure Databricks Cluster Startup Troubleshooting

> **[Home](../../../README.md)** | **[Troubleshooting](../../README.md)** | **[Databricks](README.md)** | **Cluster Startup**

![Status](https://img.shields.io/badge/Status-Active-brightgreen) ![Complexity](https://img.shields.io/badge/Complexity-Intermediate-yellow)

Guide for diagnosing and resolving Azure Databricks cluster startup failures including provisioning errors, quota limits, VNet injection issues, and init script problems.

---

## Common Issues

### Issue 1: Cluster Creation Timeout

- Cluster remains in `PENDING` state for more than 15 minutes
- Event log shows: `CLUSTER_CREATION_TIMEOUT`
- Error: `Cluster creation was not successful. Please retry later.`

| Cause | Likelihood | Impact |
|:------|:-----------|:-------|
| Azure region capacity constraints | High | High |
| VNet subnet exhaustion | Medium | High |
| NSG rules blocking provisioning traffic | Medium | High |
| Large init scripts delaying startup | Low | Medium |

### Issue 2: Driver/Worker Node Provisioning Errors

- `CLOUD_PROVIDER_LAUNCH_FAILURE` in cluster events
- Error: `Azure error code: OperationNotAllowed. The server could not fulfill the request because the specified VM size is not available in the specified region.`
- Error: `Could not acquire <N> IP addresses for cluster.`

### Issue 3: DBU Quota Limits

- Error: `Cluster creation denied. Current DBU usage exceeds the quota.`
- Error: `QuotaExceeded: Operation could not be completed as it results in exceeding approved Total Regional Cores quota.`
- Cluster moves to `TERMINATED` state immediately after creation

### Issue 4: VNet Injection Failures

- Error: `VNET_CONFIGURATION_ERROR: Subnet <subnet-name> does not have enough IP addresses.`
- Error: `Network configuration failed. Check your VNet and subnet settings.`
- Error: `SubnetDelegationNotAllowed` or `SubnetWithServiceEndpointCannotBeUsed`

### Issue 5: Init Script Failures

- Cluster starts but enters `ERROR` state shortly after
- Event log shows: `INIT_SCRIPT_FAILURE`
- Error: `Init script execution failed with exit code <N> on <node-ip>`

### Issue 6: Spark Version Incompatibilities

- Error: `The Databricks Runtime version <version> is not supported.`
- Library installation failures after runtime upgrade
- `ClassNotFoundException` or `NoSuchMethodError` in driver logs

---

## Diagnostic Steps

### Check Cluster Events

```python
import requests

DATABRICKS_HOST = "https://<workspace>.azuredatabricks.net"
TOKEN = dbutils.secrets.get(scope="<scope>", key="<key>")

def get_cluster_events(cluster_id, event_types=None):
    """Retrieve cluster events to diagnose startup failures."""
    url = f"{DATABRICKS_HOST}/api/2.0/clusters/events"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {"cluster_id": cluster_id, "limit": 50, "order": "DESC"}
    if event_types:
        payload["event_types"] = event_types

    response = requests.post(url, headers=headers, json=payload)
    for event in response.json().get("events", []):
        etype = event.get("type", "UNKNOWN")
        reason = event.get("details", {}).get("reason", {})
        print(f"[{event.get('timestamp')}] {etype}")
        if reason:
            print(f"  Code: {reason.get('code', 'N/A')}")

get_cluster_events("<cluster-id>", event_types=[
    "CREATING", "STARTING", "TERMINATING",
    "INIT_SCRIPTS_STARTED", "INIT_SCRIPTS_FINISHED"
])
```

### Check Azure Subscription Quotas

```bash
# Check VM core quotas in your region
az vm list-usage --location "eastus2" --output table

# Check for specific VM family (e.g., Standard_DS for Databricks)
az vm list-usage --location "eastus2" \
    --query "[?contains(name.value, 'standardDS')]" --output table
```

### Validate VNet Configuration

```bash
# Check subnet available addresses
az network vnet subnet show \
    --resource-group "<rg-name>" --vnet-name "<vnet-name>" \
    --name "<subnet-name>" \
    --query "{addressPrefix: addressPrefix, availableIps: ipConfigurations | length(@)}"

# List NSG rules on the subnet
az network nsg rule list \
    --resource-group "<rg-name>" --nsg-name "<nsg-name>" --output table
```

### Check Init Script Logs

```python
def check_init_script_logs(cluster_id):
    """Read init script execution logs."""
    log_path = f"dbfs:/cluster-logs/{cluster_id}/init_scripts/"
    try:
        for f in dbutils.fs.ls(log_path):
            print(f"Log: {f.path} ({f.size} bytes)")
            if 0 < f.size < 1048576:
                print(dbutils.fs.head(f.path, 2000))
    except Exception as e:
        print(f"Could not read init script logs: {e}")
```

---

## Solutions

### Resolve Cluster Creation Timeout

Switch VM type or availability zone when the default region is capacity-constrained:

```python
cluster_config = {
    "cluster_name": "analytics-cluster",
    "spark_version": "14.3.x-scala2.12",
    "node_type_id": "Standard_DS3_v2",
    "num_workers": 4,
    "azure_attributes": {
        "first_on_demand": 1,
        "availability": "ON_DEMAND_AZURE",
        "spot_bid_max_price": -1
    },
    "autotermination_minutes": 60,
    "cluster_log_conf": {"dbfs": {"destination": "dbfs:/cluster-logs"}}
}
```

### Handle Quota Limits

```bash
# Request a quota increase via Azure CLI
az quota create \
    --resource-name "standardDSv2Family" \
    --scope "/subscriptions/<sub-id>/providers/Microsoft.Compute/locations/eastus2" \
    --limit-object value=100 limit-object-type=LimitValue \
    --resource-type "dedicated"

# Common Databricks VM families:
# Standard_DS3_v2  - General purpose (default)
# Standard_DS4_v2  - Memory-optimized workloads
# Standard_NC6     - GPU workloads
# Standard_L4s     - Storage-optimized
```

### Fix VNet Injection Issues

Subnets require `/26` minimum (64 addresses), `/24` recommended per subnet:

```bash
# Create properly sized subnets with required delegation
az network vnet subnet create \
    --resource-group "<rg-name>" --vnet-name "<vnet-name>" \
    --name "databricks-host-subnet" \
    --address-prefixes "10.0.1.0/24" \
    --delegations "Microsoft.Databricks/workspaces"

az network vnet subnet create \
    --resource-group "<rg-name>" --vnet-name "<vnet-name>" \
    --name "databricks-container-subnet" \
    --address-prefixes "10.0.2.0/24" \
    --delegations "Microsoft.Databricks/workspaces"

# Required NSG rule: worker-to-worker communication
az network nsg rule create \
    --resource-group "<rg-name>" --nsg-name "<nsg-name>" \
    --name "AllowDatabricksWorkerToWorker" \
    --priority 200 --direction Inbound \
    --source-address-prefixes VirtualNetwork \
    --destination-address-prefixes VirtualNetwork \
    --access Allow --protocol "*" --destination-port-ranges "*"
```

### Fix Init Script Failures

Write init scripts with error handling and retry logic:

```bash
#!/bin/bash
# Save to: dbfs:/databricks/scripts/init.sh
set -e
LOG_FILE="/tmp/init-script.log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "[$(date)] Init script starting..."

if ! command -v pip &> /dev/null; then
    echo "ERROR: pip not found, skipping package installation"
    exit 0  # Exit gracefully to avoid blocking cluster startup
fi

for attempt in 1 2 3; do
    echo "[$(date)] Installing packages (attempt $attempt)..."
    pip install --timeout 60 --retries 3 \
        pyodbc==5.1.0 azure-identity==1.16.0 && break
    sleep 10
done

echo "[$(date)] Init script completed successfully"
```

### Handle Spark Version Incompatibilities

Always use LTS runtimes in production (currently 14.3 LTS, 13.3 LTS):

```python
def get_supported_runtimes():
    """List available LTS Databricks runtimes."""
    url = f"{DATABRICKS_HOST}/api/2.0/clusters/spark-versions"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(url, headers=headers)
    for v in response.json().get("versions", []):
        if "LTS" in v.get("name", ""):
            print(f"  {v['key']} - {v['name']}")
```

### Cluster Policy to Prevent Issues

```json
{
    "spark_version": {
        "type": "regex",
        "pattern": "1[34]\\.3\\.x-scala2\\.12",
        "defaultValue": "14.3.x-scala2.12"
    },
    "node_type_id": {
        "type": "allowlist",
        "values": ["Standard_DS3_v2", "Standard_DS4_v2", "Standard_DS5_v2"],
        "defaultValue": "Standard_DS3_v2"
    },
    "autotermination_minutes": {
        "type": "range", "minValue": 10, "maxValue": 120, "defaultValue": 60
    }
}
```

---

## Related Resources

| Resource | Description |
|----------|-------------|
| [Memory Issues](memory-issues.md) | OOM errors and memory troubleshooting |
| [Networking](networking.md) | VNet peering and connectivity issues |
| [Azure Databricks Docs](https://learn.microsoft.com/azure/databricks/) | Official Microsoft documentation |
| [Cluster Configuration](https://docs.databricks.com/clusters/configure.html) | Databricks cluster configuration guide |

---

> **Tip:** Always use cluster policies to enforce consistent configuration and prevent common startup issues across your organization.

**Last Updated:** 2026-04-07
**Version:** 1.0.0
