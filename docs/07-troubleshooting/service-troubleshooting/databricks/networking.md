# Azure Databricks Networking Troubleshooting

> **[Home](../../../README.md)** | **[Troubleshooting](../../README.md)** | **[Databricks](README.md)** | **Networking**

![Status](https://img.shields.io/badge/Status-Active-brightgreen) ![Complexity](https://img.shields.io/badge/Complexity-Advanced-red)

Guide for diagnosing and resolving Azure Databricks networking issues including VNet peering, NSG misconfigurations, DNS resolution, private endpoints, and connectivity to dependent Azure services.

---

## Common Issues

### Issue 1: VNet Peering Failures

- Databricks cluster cannot reach resources in peered VNets
- Error: `Connection timed out` when accessing databases or services in another VNet
- Spark jobs fail with `java.net.ConnectException: Connection refused`

| Cause | Likelihood | Impact |
|:------|:-----------|:-------|
| Peering not established in both directions | High | High |
| Address space overlap between VNets | Medium | High |
| Missing UDR for peered traffic | Medium | Medium |
| Gateway transit not enabled | Low | Medium |

### Issue 2: NSG Rule Misconfigurations

- Cluster fails to start with `CLOUD_PROVIDER_LAUNCH_FAILURE`
- Workers cannot communicate with the driver node
- Error: `Rpc to <ip>:<port> failed: Connection refused`

**Required NSG rules:**

| Direction | Source | Destination | Port | Purpose |
|:----------|:-------|:------------|:-----|:--------|
| Inbound | AzureDatabricks | VirtualNetwork | * | Control plane to cluster |
| Inbound | VirtualNetwork | VirtualNetwork | * | Worker-to-worker |
| Outbound | VirtualNetwork | AzureDatabricks | 443 | Cluster to control plane |
| Outbound | VirtualNetwork | Sql | 3306 | Metastore connectivity |
| Outbound | VirtualNetwork | Storage | 443 | DBFS and log storage |
| Outbound | VirtualNetwork | EventHub | 9093 | Log delivery |

### Issue 3: DNS Resolution Failures

- Error: `java.net.UnknownHostException: <hostname>`
- Cannot resolve Azure service private endpoints
- `nslookup` from cluster returns `NXDOMAIN`

### Issue 4: Connectivity to Azure Storage

- `403 Forbidden` when accessing ADLS Gen2 or Blob Storage
- Timeout when reading/writing data to storage accounts with firewalls enabled

### Issue 5: Private Endpoint Connectivity

- Resources accessible via public endpoint but not via private endpoint
- DNS resolves to public IP instead of private IP
- Error: `Connection to <service>.privatelink.<domain> timed out`

---

## Diagnostic Steps

### Test Network Connectivity from Cluster

```python
import socket

def test_connectivity(targets):
    """Test network connectivity to Azure service endpoints."""
    for name, host, port in targets:
        try:
            sock = socket.create_connection((host, port), timeout=10)
            sock.close()
            status = "OK"
        except socket.timeout:
            status = "TIMEOUT"
        except socket.gaierror:
            status = "DNS_FAILURE"
        except ConnectionRefusedError:
            status = "REFUSED"
        except Exception as e:
            status = f"ERROR: {e}"
        print(f"{name:30s} {host}:{port} -> {status}")

test_connectivity([
    ("ADLS Gen2",      "<storage>.dfs.core.windows.net",      443),
    ("Blob Storage",   "<storage>.blob.core.windows.net",     443),
    ("Azure SQL",      "<server>.database.windows.net",       1433),
    ("Key Vault",      "<vault>.vault.azure.net",             443),
    ("Databricks CP",  "<region>.azuredatabricks.net",        443),
])
```

### Verify DNS Resolution

```python
import socket

def check_dns_resolution(hostnames):
    """Check if hostnames resolve to private or public IPs."""
    for hostname in hostnames:
        try:
            ip = socket.gethostbyname(hostname)
            is_private = ip.startswith("10.") or ip.startswith("192.168.") or \
                any(ip.startswith(f"172.{i}.") for i in range(16, 32))
            print(f"{hostname} -> {ip} ({'PRIVATE' if is_private else 'PUBLIC'})")
        except socket.gaierror as e:
            print(f"{hostname} -> DNS FAILURE: {e}")
```

### Check VNet Peering Status

```bash
# Check peering status from both sides
az network vnet peering list \
    --resource-group "<databricks-rg>" --vnet-name "<databricks-vnet>" \
    --output table \
    --query "[].{Name:name, State:peeringState, RemoteVnet:remoteVirtualNetwork.id}"

# Verify peering is connected (should show "Connected")
az network vnet peering show \
    --resource-group "<databricks-rg>" --vnet-name "<databricks-vnet>" \
    --name "<peering-name>" \
    --query "{state:peeringState, allowForwardedTraffic:allowForwardedTraffic, allowVnetAccess:allowVirtualNetworkAccess}"
```

### Check NSG Flow Logs

```bash
# Enable NSG flow logs for troubleshooting
az network watcher flow-log create \
    --resource-group "<rg-name>" --nsg "<nsg-name>" \
    --name "databricks-nsg-flowlog" \
    --storage-account "<storage-account-id>" \
    --enabled true --format JSON --log-version 2 --retention 7

# Query for denied traffic from Databricks subnets
az monitor log-analytics query \
    --workspace "<workspace-id>" \
    --analytics-query "
        AzureNetworkAnalytics_CL
        | where FlowStatus_s == 'D'
        | where SrcIP_s startswith '10.0'
        | project TimeGenerated, SrcIP_s, DestIP_s, DestPort_d
        | order by TimeGenerated desc | take 50
    "
```

---

## Solutions

### Fix VNet Peering

Peering must exist in **both** directions:

```bash
# Direction 1: Databricks VNet -> Target VNet
az network vnet peering create \
    --resource-group "<databricks-rg>" --vnet-name "<databricks-vnet>" \
    --name "databricks-to-data" \
    --remote-vnet "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Network/virtualNetworks/<target-vnet>" \
    --allow-vnet-access true --allow-forwarded-traffic true

# Direction 2: Target VNet -> Databricks VNet
az network vnet peering create \
    --resource-group "<target-rg>" --vnet-name "<target-vnet>" \
    --name "data-to-databricks" \
    --remote-vnet "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Network/virtualNetworks/<databricks-vnet>" \
    --allow-vnet-access true --allow-forwarded-traffic true
```

### Fix NSG Rules for Databricks

```bash
# Inbound: Allow control plane
az network nsg rule create \
    --resource-group "<rg-name>" --nsg-name "<nsg-name>" \
    --name "AllowAzureDatabricksInbound" --priority 100 \
    --direction Inbound --access Allow --protocol "*" \
    --source-address-prefixes AzureDatabricks \
    --destination-address-prefixes VirtualNetwork --destination-port-ranges "*"

# Outbound: Allow control plane, storage, metastore
az network nsg rule create \
    --resource-group "<rg-name>" --nsg-name "<nsg-name>" \
    --name "AllowDatabricksControlPlane" --priority 100 \
    --direction Outbound --access Allow --protocol Tcp \
    --source-address-prefixes VirtualNetwork \
    --destination-address-prefixes AzureDatabricks --destination-port-ranges 443

az network nsg rule create \
    --resource-group "<rg-name>" --nsg-name "<nsg-name>" \
    --name "AllowStorageOutbound" --priority 110 \
    --direction Outbound --access Allow --protocol Tcp \
    --source-address-prefixes VirtualNetwork \
    --destination-address-prefixes Storage --destination-port-ranges 443

az network nsg rule create \
    --resource-group "<rg-name>" --nsg-name "<nsg-name>" \
    --name "AllowSqlOutbound" --priority 120 \
    --direction Outbound --access Allow --protocol Tcp \
    --source-address-prefixes VirtualNetwork \
    --destination-address-prefixes Sql --destination-port-ranges 3306
```

### Fix DNS for Private Endpoints

```bash
# Create Private DNS Zone for the service
az network private-dns zone create \
    --resource-group "<rg-name>" --name "privatelink.dfs.core.windows.net"

# Link the DNS zone to the Databricks VNet
az network private-dns zone vnet-link create \
    --resource-group "<rg-name>" --zone-name "privatelink.dfs.core.windows.net" \
    --name "databricks-vnet-link" \
    --virtual-network "<databricks-vnet-id>" --registration-enabled false

# Verify the DNS record resolves to the private IP
az network private-dns record-set a list \
    --resource-group "<rg-name>" \
    --zone-name "privatelink.dfs.core.windows.net" --output table
```

### Configure Storage Firewall for Databricks

```bash
# Add Databricks subnets to the storage firewall allow list
az storage account network-rule add \
    --resource-group "<rg-name>" --account-name "<storage-account>" \
    --subnet "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Network/virtualNetworks/<vnet>/subnets/<host-subnet>"

az storage account network-rule add \
    --resource-group "<rg-name>" --account-name "<storage-account>" \
    --subnet "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Network/virtualNetworks/<vnet>/subnets/<container-subnet>"

# Allow trusted Azure services
az storage account update \
    --resource-group "<rg-name>" --name "<storage-account>" --bypass AzureServices
```

### Verify Secure Cluster Connectivity (No Public IP)

```bash
# Check if workspace uses SCC
az databricks workspace show \
    --resource-group "<rg-name>" --name "<workspace-name>" \
    --query "parameters.enableNoPublicIp.value"

# SCC requires outbound HTTPS to Databricks control plane on port 443
# Ensure NSG rules above are in place before enabling
```

---

## Network Architecture Checklist

Before deploying Databricks with VNet injection:

- [ ] Host and container subnets are at least `/24` each
- [ ] NSG allows all required inbound/outbound service tags
- [ ] No overlapping address spaces with peered VNets
- [ ] Private DNS zones created and linked for each private endpoint
- [ ] UDRs do not force-tunnel Databricks control plane traffic
- [ ] Storage firewalls allow Databricks subnet access
- [ ] VNet peering established bidirectionally where needed

---

## Related Resources

| Resource | Description |
|----------|-------------|
| [Cluster Startup](cluster-startup.md) | Cluster creation and startup issues |
| [Memory Issues](memory-issues.md) | OOM errors and memory troubleshooting |
| [VNet Injection Docs](https://learn.microsoft.com/azure/databricks/administration-guide/cloud-configurations/azure/vnet-inject) | Official VNet injection documentation |
| [NSG Rules Reference](https://learn.microsoft.com/azure/databricks/security/network/classic/vnet-inject#network-security-group-rules) | Required NSG rule reference |

---

> **Tip:** Always test connectivity to dependent services from a running Databricks notebook before deploying production workloads.

**Last Updated:** 2026-04-07
**Version:** 1.0.0
