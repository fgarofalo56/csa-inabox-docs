// Medallion Architecture - Azure Infrastructure as Code (Bicep)
// Deploys complete Medallion Architecture with Synapse, Data Lake Gen2, and Delta Lake

targetScope = 'resourceGroup'

// Parameters
@description('Name of the Azure Synapse workspace')
param synapseWorkspaceName string

@description('Name of the storage account for Data Lake Gen2')
@maxLength(24)
param storageAccountName string

@description('Primary location for all resources')
param location string = resourceGroup().location

@description('SQL Administrator login username')
param sqlAdministratorLogin string = 'sqladmin'

@description('SQL Administrator login password')
@secure()
param sqlAdministratorLoginPassword string

@description('Name of the Spark pool')
param sparkPoolName string = 'sparkpool01'

@description('Spark pool node size')
@allowed(['Small', 'Medium', 'Large'])
param sparkPoolNodeSize string = 'Small'

@description('Minimum number of Spark pool nodes')
@minValue(3)
@maxValue(200)
param sparkPoolMinNodeCount int = 3

@description('Maximum number of Spark pool nodes')
@minValue(3)
@maxValue(200)
param sparkPoolMaxNodeCount int = 10

// Variables
var dataLakeFileSystemName = 'datalake'
var keyVaultName = 'kv-${uniqueString(resourceGroup().id)}'
var logAnalyticsWorkspaceName = 'law-${synapseWorkspaceName}'

// Storage Account with Data Lake Gen2
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    isHnsEnabled: true  // Hierarchical namespace for Data Lake Gen2
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    allowBlobPublicAccess: false
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
    }
    encryption: {
      services: {
        blob: {
          enabled: true
          keyType: 'Account'
        }
        file: {
          enabled: true
          keyType: 'Account'
        }
      }
      keySource: 'Microsoft.Storage'
    }
  }
  
  tags: {
    Environment: 'Tutorial'
    Pattern: 'Medallion'
    Layer: 'Storage'
  }
}

// Blob service for storage account
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storageAccount
  name: 'default'
  properties: {
    deleteRetentionPolicy: {
      enabled: true
      days: 7
    }
    containerDeleteRetentionPolicy: {
      enabled: true
      days: 7
    }
  }
}

// Data Lake container
resource dataLakeContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobService
  name: dataLakeFileSystemName
  properties: {
    publicAccess: 'None'
  }
}

// Key Vault for secrets management
resource keyVault 'Microsoft.KeyVault/vaults@2023-02-01' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    enableRbacAuthorization: true
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
    }
  }
  
  tags: {
    Environment: 'Tutorial'
    Pattern: 'Medallion'
    Layer: 'Security'
  }
}

// Log Analytics Workspace
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsWorkspaceName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
  
  tags: {
    Environment: 'Tutorial'
    Pattern: 'Medallion'
    Layer: 'Monitoring'
  }
}

// Synapse Workspace
resource synapseWorkspace 'Microsoft.Synapse/workspaces@2021-06-01' = {
  name: synapseWorkspaceName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    defaultDataLakeStorage: {
      accountUrl: storageAccount.properties.primaryEndpoints.dfs
      filesystem: dataLakeFileSystemName
    }
    sqlAdministratorLogin: sqlAdministratorLogin
    sqlAdministratorLoginPassword: sqlAdministratorLoginPassword
    managedResourceGroupName: 'synapsemrg-${synapseWorkspaceName}'
    publicNetworkAccess: 'Enabled'
  }
  
  tags: {
    Environment: 'Tutorial'
    Pattern: 'Medallion'
    Layer: 'Analytics'
  }
  
  dependsOn: [
    dataLakeContainer
  ]
}

// Synapse Spark Pool
resource sparkPool 'Microsoft.Synapse/workspaces/bigDataPools@2021-06-01' = {
  parent: synapseWorkspace
  name: sparkPoolName
  location: location
  properties: {
    sparkVersion: '3.3'
    nodeCount: 0
    nodeSizeFamily: 'MemoryOptimized'
    nodeSize: sparkPoolNodeSize
    autoScale: {
      enabled: true
      minNodeCount: sparkPoolMinNodeCount
      maxNodeCount: sparkPoolMaxNodeCount
    }
    autoPause: {
      enabled: true
      delayInMinutes: 15
    }
    dynamicExecutorAllocation: {
      enabled: true
      minExecutors: 1
      maxExecutors: 4
    }
    sessionLevelPackagesEnabled: true
    cacheSize: 50
  }
  
  tags: {
    Environment: 'Tutorial'
    Pattern: 'Medallion'
    Component: 'SparkPool'
  }
}

// Firewall rule to allow all Azure services
resource firewallRuleAzureServices 'Microsoft.Synapse/workspaces/firewallRules@2021-06-01' = {
  parent: synapseWorkspace
  name: 'AllowAllWindowsAzureIps'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

// RBAC: Grant Synapse workspace Storage Blob Data Contributor on Data Lake
resource synapseStorageRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, synapseWorkspace.id, 'StorageBlobDataContributor')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe') // Storage Blob Data Contributor
    principalId: synapseWorkspace.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// Diagnostic settings for Synapse workspace
resource synapseDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'diag-${synapseWorkspaceName}'
  scope: synapseWorkspace
  properties: {
    workspaceId: logAnalyticsWorkspace.id
    logs: [
      {
        category: 'SynapseRbacOperations'
        enabled: true
      }
      {
        category: 'GatewayApiRequests'
        enabled: true
      }
      {
        category: 'BuiltinSqlReqsEnded'
        enabled: true
      }
      {
        category: 'IntegrationPipelineRuns'
        enabled: true
      }
      {
        category: 'IntegrationActivityRuns'
        enabled: true
      }
      {
        category: 'IntegrationTriggerRuns'
        enabled: true
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
      }
    ]
  }
}

// Outputs
output synapseWorkspaceName string = synapseWorkspace.name
output synapseWorkspaceId string = synapseWorkspace.id
output synapseDevelopmentEndpoint string = synapseWorkspace.properties.connectivityEndpoints.dev
output synapseSqlEndpoint string = synapseWorkspace.properties.connectivityEndpoints.sql
output synapseWebUrl string = synapseWorkspace.properties.connectivityEndpoints.web

output storageAccountName string = storageAccount.name
output storageAccountId string = storageAccount.id
output dataLakePrimaryEndpoint string = storageAccount.properties.primaryEndpoints.dfs

output sparkPoolName string = sparkPool.name
output sparkPoolId string = sparkPool.id

output keyVaultName string = keyVault.name
output keyVaultUri string = keyVault.properties.vaultUri

output logAnalyticsWorkspaceId string = logAnalyticsWorkspace.id
output logAnalyticsWorkspaceName string = logAnalyticsWorkspace.name
