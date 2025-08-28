# 🚀 Tutorial 1: Environment Setup and Prerequisites

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎓 [Tutorials](../README.md)** | **🏗️ [Synapse Series](README.md)** | **🚀 Environment Setup**

![Tutorial](https://img.shields.io/badge/Tutorial-01_Environment_Setup-blue)
![Duration](https://img.shields.io/badge/Duration-30_minutes-green)
![Level](https://img.shields.io/badge/Level-Beginner-brightgreen)

**Set up your Azure environment and local development tools for the complete Synapse Analytics tutorial series. This foundation ensures smooth execution of all subsequent tutorials.**

## 🎯 Learning Objectives

After completing this tutorial, you will be able to:

- ✅ **Configure Azure subscription** with necessary permissions and quotas
- ✅ **Install and authenticate** essential development tools
- ✅ **Validate environment setup** using automated testing scripts
- ✅ **Understand cost implications** and set up budget monitoring
- ✅ **Prepare resource naming conventions** for consistent deployments

## ⏱️ Time Estimate: 30 minutes

- **Azure Setup**: 15 minutes
- **Tool Installation**: 10 minutes  
- **Validation & Testing**: 5 minutes

## 📋 Prerequisites

### **Required Access**
- [ ] **Azure Subscription** with Owner or Contributor role
- [ ] **Sufficient credits** or payment method configured (~$100 recommended for full series)
- [ ] **Administrative access** to local machine for tool installation

### **Basic Knowledge**
- [ ] **Azure fundamentals** - Understanding of resource groups and subscriptions
- [ ] **Command line basics** - Comfortable with PowerShell or Bash
- [ ] **JSON/YAML familiarity** - For configuration file modifications

## 🛠️ Step 1: Azure Subscription Setup

### **1.1 Verify Subscription Access**

First, let's ensure your Azure subscription has the necessary permissions and quotas:

```powershell
# Login to Azure (will open browser for authentication)
az login

# List available subscriptions
az account list --output table

# Set the subscription you want to use for tutorials
az account set --subscription "your-subscription-id-here"

# Verify current subscription
az account show --output table
```

**Expected Output:**
```
EnvironmentName    HomeTenantId    Id          Name               State    TenantId
-----------------  --------------  ----------  -----------------  -------  -----------
AzureCloud         xxxx-xxxx-...   yyyy-yyyy-... Your Subscription  Enabled  xxxx-xxxx-...
```

### **1.2 Check Service Quotas**

Verify your subscription has sufficient quotas for the tutorial series:

```powershell
# Check Synapse Analytics quota
az synapse quota list --location "East US" --output table

# Check compute quotas (for Spark pools)
az vm list-usage --location "East US" --output table | Where-Object {$_.Name.LocalizedValue -like "*Standard D*"}

# Check storage account quotas
az storage account check-quota --output table
```

**Required Minimums:**
- **Synapse Workspaces**: 2 workspaces per subscription
- **Spark Pool Cores**: 50 cores (for medium-sized pools)
- **Storage Accounts**: 10 accounts per subscription
- **Dedicated SQL Pool**: DW100c or higher capability

> **💡 Quota Increase:** If quotas are insufficient, request increases through Azure Portal → Subscriptions → Usage + quotas

### **1.3 Enable Required Resource Providers**

Register necessary Azure resource providers:

```powershell
# Register required providers
$providers = @(
    'Microsoft.Synapse',
    'Microsoft.Storage', 
    'Microsoft.EventHub',
    'Microsoft.StreamAnalytics',
    'Microsoft.DataFactory',
    'Microsoft.PowerBI',
    'Microsoft.Purview'
)

foreach ($provider in $providers) {
    Write-Host "Registering $provider..." -ForegroundColor Green
    az provider register --namespace $provider
}

# Check registration status
foreach ($provider in $providers) {
    az provider show --namespace $provider --query "registrationState" --output tsv
}
```

**Expected Output:** All providers should show `Registered` status.

## 🔧 Step 2: Local Development Tools

### **2.1 Install Azure CLI (if not already installed)**

**Windows:**
```powershell
# Install via PowerShell
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
Start-Process msiexec.exe -ArgumentList '/i AzureCLI.msi /quiet' -Wait
```

**macOS:**
```bash
# Install via Homebrew
brew update && brew install azure-cli
```

**Linux:**
```bash
# Install via package manager (Ubuntu/Debian)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### **2.2 Install Azure PowerShell Module**

```powershell
# Install Azure PowerShell module
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Install-Module -Name Az -Repository PSGallery -Force -AllowClobber

# Verify installation
Get-Module Az -ListAvailable | Select-Object Name, Version
```

### **2.3 Install Visual Studio Code with Extensions**

1. **Download and install VS Code** from [https://code.visualstudio.com/](https://code.visualstudio.com/)

2. **Install essential extensions:**
```powershell
# Install VS Code extensions via command line
code --install-extension ms-vscode.azure-account
code --install-extension ms-azuretools.vscode-azureresourcegroups  
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension ms-mssql.mssql
code --install-extension redhat.vscode-yaml
```

### **2.4 Install Git and Configure**

**Windows:**
```powershell
# Install Git via winget
winget install --id Git.Git -e --source winget
```

**macOS/Linux:**
```bash
# macOS
brew install git

# Ubuntu/Debian
sudo apt update && sudo apt install git
```

**Configure Git:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### **2.5 Install Python and Required Packages**

```powershell
# Install Python 3.9+ (Windows)
winget install python.python.3

# Install required Python packages
pip install azure-cli azure-storage-blob azure-identity pandas numpy jupyter
```

## 📊 Step 3: Cost Management Setup

### **3.1 Create Budget Alerts**

Set up budget monitoring to prevent unexpected charges:

```powershell
# Create a budget for tutorial expenses
az consumption budget create \
  --budget-name "synapse-tutorial-budget" \
  --amount 100 \
  --time-grain Monthly \
  --start-date "$(Get-Date -Format 'yyyy-MM-01')" \
  --end-date "$(Get-Date -Year $((Get-Date).Year + 1) -Format 'yyyy-MM-01')" \
  --resource-group-filter "synapse-tutorial-rg"
```

### **3.2 Set Up Billing Alerts**

Configure email notifications when costs exceed thresholds:

```powershell
# Create action group for budget alerts
az monitor action-group create \
  --name "budget-alerts" \
  --resource-group "synapse-tutorial-rg" \
  --short-name "budget" \
  --email-receiver name="admin" email="your-email@example.com"
```

### **3.3 Implement Resource Tagging Strategy**

Define consistent tags for cost tracking:

```powershell
# Set default tags for tutorial resources
$defaultTags = @{
    'Project' = 'SynapseTutorial'
    'Environment' = 'Learning'
    'Owner' = 'YourName'
    'CostCenter' = 'Training'
    'AutoShutdown' = 'Enabled'
}

# Save tags for later use in tutorials
$defaultTags | ConvertTo-Json | Out-File "tutorial-tags.json"
```

## 🏗️ Step 4: Resource Naming Convention

### **4.1 Define Naming Standards**

Establish consistent naming patterns for all tutorial resources:

```powershell
# Define naming convention variables
$subscriptionId = (az account show --query "id" --output tsv)
$location = "East US"
$locationShort = "eus"
$environment = "dev"
$project = "syntut"  # synapse tutorial abbreviated

# Generate unique suffix
$uniqueSuffix = [System.Guid]::NewGuid().ToString().Substring(0, 8)

# Create naming convention object
$namingConvention = @{
    'ResourceGroupName' = "rg-$project-$environment-$locationShort"
    'SynapseWorkspace' = "syn-$project-$environment-$uniqueSuffix"
    'StorageAccount' = "st$project$environment$uniqueSuffix"  # Storage names must be globally unique
    'KeyVault' = "kv-$project-$environment-$uniqueSuffix"
    'SqlPool' = "sql-$project-$environment"
    'SparkPool' = "spark-$project-$environment"
}

# Save naming convention for use in subsequent tutorials
$namingConvention | ConvertTo-Json | Out-File "naming-convention.json"
Write-Host "Naming convention saved to naming-convention.json" -ForegroundColor Green
```

### **4.2 Validate Naming Convention**

Ensure names comply with Azure requirements:

```powershell
# Function to validate Azure resource names
function Test-AzureResourceName {
    param(
        [string]$Name,
        [string]$ResourceType
    )
    
    switch ($ResourceType) {
        'StorageAccount' {
            if ($Name.Length -gt 24 -or $Name -notmatch '^[a-z0-9]+$') {
                Write-Warning "Storage account name '$Name' is invalid. Must be 3-24 characters, lowercase letters and numbers only."
                return $false
            }
        }
        'SynapseWorkspace' {
            if ($Name.Length -gt 50 -or $Name -notmatch '^[a-zA-Z0-9-]+$') {
                Write-Warning "Synapse workspace name '$Name' is invalid. Must be 1-50 characters, letters, numbers, and hyphens only."
                return $false
            }
        }
    }
    return $true
}

# Validate our naming convention
$namingConvention = Get-Content "naming-convention.json" | ConvertFrom-Json
Test-AzureResourceName -Name $namingConvention.StorageAccount -ResourceType "StorageAccount"
Test-AzureResourceName -Name $namingConvention.SynapseWorkspace -ResourceType "SynapseWorkspace"
```

## ✅ Step 5: Environment Validation

### **5.1 Run Comprehensive Validation Script**

Create and execute a validation script to ensure everything is properly configured:

```powershell
# Create comprehensive validation script
$validationScript = @'
# Azure Synapse Tutorial Environment Validation Script
Write-Host "🔍 Validating Azure Synapse Tutorial Environment..." -ForegroundColor Cyan

$errors = @()
$warnings = @()

# Test 1: Azure CLI Authentication
Write-Host "Testing Azure CLI authentication..." -ForegroundColor Yellow
try {
    $account = az account show --query "id" --output tsv
    if ($account) {
        Write-Host "✅ Azure CLI authenticated successfully" -ForegroundColor Green
    } else {
        $errors += "❌ Azure CLI not authenticated"
    }
} catch {
    $errors += "❌ Azure CLI authentication failed: $_"
}

# Test 2: Required PowerShell Modules
Write-Host "Checking PowerShell modules..." -ForegroundColor Yellow
$requiredModules = @('Az.Accounts', 'Az.Synapse', 'Az.Storage', 'Az.Resources')
foreach ($module in $requiredModules) {
    if (Get-Module -ListAvailable -Name $module) {
        Write-Host "✅ Module $module installed" -ForegroundColor Green
    } else {
        $warnings += "⚠️ Module $module not installed (will install when needed)"
    }
}

# Test 3: Tool Availability  
Write-Host "Checking tool availability..." -ForegroundColor Yellow
$tools = @{
    'az' = 'Azure CLI'
    'git' = 'Git'
    'python' = 'Python'
    'code' = 'VS Code (optional)'
}

foreach ($tool in $tools.GetEnumerator()) {
    try {
        $null = Get-Command $tool.Key -ErrorAction Stop
        Write-Host "✅ $($tool.Value) available" -ForegroundColor Green
    } catch {
        if ($tool.Key -eq 'code') {
            $warnings += "⚠️ $($tool.Value) not found (optional)"
        } else {
            $errors += "❌ $($tool.Value) not found"
        }
    }
}

# Test 4: Resource Provider Registration
Write-Host "Checking resource provider registration..." -ForegroundColor Yellow
$providers = @('Microsoft.Synapse', 'Microsoft.Storage', 'Microsoft.EventHub')
foreach ($provider in $providers) {
    $status = az provider show --namespace $provider --query "registrationState" --output tsv
    if ($status -eq 'Registered') {
        Write-Host "✅ $provider registered" -ForegroundColor Green
    } else {
        $warnings += "⚠️ $provider not registered (status: $status)"
    }
}

# Test 5: Subscription Quotas
Write-Host "Checking subscription quotas..." -ForegroundColor Yellow
try {
    $location = "East US"
    $quotas = az vm list-usage --location $location --output json | ConvertFrom-Json
    $coresQuota = $quotas | Where-Object {$_.name.localizedValue -eq "Total Regional Cores"}
    
    if ($coresQuota.currentValue -lt ($coresQuota.limit - 20)) {
        Write-Host "✅ Sufficient compute quota available" -ForegroundColor Green
    } else {
        $warnings += "⚠️ Limited compute quota remaining"
    }
} catch {
    $warnings += "⚠️ Unable to check compute quotas"
}

# Summary
Write-Host "`n🎯 Validation Summary:" -ForegroundColor Cyan
if ($errors.Count -eq 0) {
    Write-Host "✅ Environment validation passed! Ready to proceed with tutorials." -ForegroundColor Green
    if ($warnings.Count -gt 0) {
        Write-Host "`nWarnings:" -ForegroundColor Yellow
        $warnings | ForEach-Object { Write-Host $_ -ForegroundColor Yellow }
    }
} else {
    Write-Host "❌ Environment validation failed. Please resolve the following issues:" -ForegroundColor Red
    $errors | ForEach-Object { Write-Host $_ -ForegroundColor Red }
    if ($warnings.Count -gt 0) {
        Write-Host "`nAdditional warnings:" -ForegroundColor Yellow
        $warnings | ForEach-Object { Write-Host $_ -ForegroundColor Yellow }
    }
}
'@

# Save and execute validation script
$validationScript | Out-File "validate-environment.ps1"
.\validate-environment.ps1
```

### **5.2 Create Resource Group for Tutorials**

Create the main resource group that will contain all tutorial resources:

```powershell
# Load naming convention
$naming = Get-Content "naming-convention.json" | ConvertFrom-Json

# Create resource group
az group create \
  --name $naming.ResourceGroupName \
  --location "East US" \
  --tags Project=SynapseTutorial Environment=Learning

Write-Host "✅ Resource group '$($naming.ResourceGroupName)' created successfully" -ForegroundColor Green
```

### **5.3 Test Azure Connectivity**

Verify network connectivity to Azure services:

```powershell
# Test connectivity to key Azure endpoints
$endpoints = @(
    'https://management.azure.com',
    'https://login.microsoftonline.com',
    'https://graph.microsoft.com'
)

foreach ($endpoint in $endpoints) {
    try {
        $response = Invoke-WebRequest -Uri $endpoint -Method Head -TimeoutSec 10
        Write-Host "✅ Connectivity to $endpoint: OK" -ForegroundColor Green
    } catch {
        Write-Host "❌ Connectivity to $endpoint: Failed" -ForegroundColor Red
    }
}
```

## 📊 Step 6: Cost Estimation and Budget Planning

### **6.1 Estimate Tutorial Costs**

Understand the cost implications of running the complete tutorial series:

```powershell
# Tutorial cost estimation (approximate monthly costs)
$costEstimate = @{
    'Synapse Workspace' = '$0 (free tier available)'
    'Spark Pool (Medium)' = '$50-100/month (auto-pause enabled)'
    'Dedicated SQL Pool' = '$1,000+/month (DW100c, pause when not in use)'
    'Storage (ADLS Gen2)' = '$5-15/month'
    'Event Hubs' = '$10-20/month'
    'Power BI Premium' = '$20/user/month (Pro tier sufficient for tutorials)'
}

Write-Host "💰 Estimated Monthly Costs for Tutorial Environment:" -ForegroundColor Cyan
$costEstimate.GetEnumerator() | Sort-Object Key | ForEach-Object {
    Write-Host "  $($_.Key): $($_.Value)" -ForegroundColor White
}
```

### **6.2 Configure Auto-Pause and Scaling**

Set up automatic resource management to minimize costs:

```powershell
# Create configuration for auto-scaling and pausing
$autoScaleConfig = @{
    'SparkPool' = @{
        'AutoPause' = @{
            'Enabled' = $true
            'DelayInMinutes' = 15
        }
        'AutoScale' = @{
            'Enabled' = $true
            'MinNodeCount' = 3
            'MaxNodeCount' = 10
        }
    }
    'DedicatedSQLPool' = @{
        'AutoPause' = @{
            'Enabled' = $true
            'DelayInMinutes' = 60
        }
        'AutoScale' = @{
            'Enabled' = $false  # Manual scaling recommended
            'TargetServiceLevelObjective' = 'DW100c'
        }
    }
}

# Save configuration for use in later tutorials
$autoScaleConfig | ConvertTo-Json -Depth 3 | Out-File "auto-scale-config.json"
```

## 🎯 Step 7: Next Steps Preparation

### **7.1 Download Tutorial Assets**

Prepare sample data and scripts for upcoming tutorials:

```powershell
# Create directory structure for tutorial assets
$assetDirs = @(
    'sample-data',
    'scripts',
    'notebooks',
    'sql-scripts',
    'config-files'
)

foreach ($dir in $assetDirs) {
    New-Item -ItemType Directory -Path $dir -Force
    Write-Host "✅ Created directory: $dir" -ForegroundColor Green
}

# Download sample datasets (placeholder URLs - replace with actual assets)
$sampleData = @{
    'customer-data.csv' = 'https://raw.githubusercontent.com/your-org/synapse-tutorials/main/data/customers.csv'
    'transaction-data.json' = 'https://raw.githubusercontent.com/your-org/synapse-tutorials/main/data/transactions.json'
    'product-catalog.parquet' = 'https://raw.githubusercontent.com/your-org/synapse-tutorials/main/data/products.parquet'
}

foreach ($dataset in $sampleData.GetEnumerator()) {
    try {
        Invoke-WebRequest -Uri $dataset.Value -OutFile "sample-data\$($dataset.Key)"
        Write-Host "✅ Downloaded: $($dataset.Key)" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Could not download $($dataset.Key) - will create synthetic data in next tutorial" -ForegroundColor Yellow
    }
}
```

### **7.2 Create Environment Summary**

Document your setup for reference:

```powershell
# Create environment summary document
$environmentSummary = @"
# Azure Synapse Tutorial Environment Summary

## Setup Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## Azure Configuration
- Subscription ID: $(az account show --query "id" --output tsv)
- Default Location: East US
- Resource Group: $($naming.ResourceGroupName)

## Naming Convention
$(Get-Content "naming-convention.json" | ConvertFrom-Json | ConvertTo-Json)

## Tools Installed
- Azure CLI: $(az version --query '\"azure-cli\"' --output tsv)
- Azure PowerShell: $(if (Get-Module Az.Accounts -ListAvailable) { 'Installed' } else { 'Not Installed' })
- Git: $(if (Get-Command git -ErrorAction SilentlyContinue) { git --version } else { 'Not Available' })
- Python: $(if (Get-Command python -ErrorAction SilentlyContinue) { python --version } else { 'Not Available' })

## Cost Management
- Budget Name: synapse-tutorial-budget
- Budget Amount: $100/month
- Auto-pause Configuration: Enabled
- Resource Tags: Applied for cost tracking

## Next Steps
1. Proceed to Tutorial 2: Synapse Workspace Basics
2. Review cost monitoring dashboard regularly
3. Remember to pause/stop resources when not in use

## Support
- Documentation: https://docs.microsoft.com/azure/synapse-analytics/
- Community: https://techcommunity.microsoft.com/t5/azure-synapse-analytics/bd-p/AzureSynapseAnalytics
- Issues: Create issues in the tutorial repository
"@

$environmentSummary | Out-File "environment-summary.md" -Encoding UTF8
Write-Host "✅ Environment summary saved to environment-summary.md" -ForegroundColor Green
```

## ✅ Checkpoint Validation

Before proceeding to the next tutorial, verify your setup:

### **Validation Checklist**
- [ ] **Azure CLI authenticated** and connected to correct subscription
- [ ] **Resource providers registered** for all required services
- [ ] **Development tools installed** (VS Code, Git, Python)
- [ ] **Resource group created** with proper naming convention
- [ ] **Budget and cost alerts configured**
- [ ] **Sample data downloaded** and organized
- [ ] **Environment validation script passed** without errors

### **Quick Validation Command**
```powershell
# Run final validation
Write-Host "🔍 Final Environment Check..." -ForegroundColor Cyan

# Check resource group exists
$rgExists = az group exists --name (Get-Content "naming-convention.json" | ConvertFrom-Json).ResourceGroupName
if ($rgExists -eq 'true') {
    Write-Host "✅ Resource group exists and ready" -ForegroundColor Green
} else {
    Write-Host "❌ Resource group not found" -ForegroundColor Red
}

# Check configuration files exist
$configFiles = @('naming-convention.json', 'auto-scale-config.json', 'environment-summary.md')
foreach ($file in $configFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Configuration file exists: $file" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Configuration file missing: $file" -ForegroundColor Yellow
    }
}

Write-Host "`n🎯 Environment setup complete! Ready for Tutorial 2." -ForegroundColor Green
```

## 🎉 Congratulations!

You've successfully set up your Azure environment for the Synapse Analytics tutorial series. Your setup includes:

- ✅ **Authenticated Azure environment** with proper permissions
- ✅ **Essential development tools** installed and configured
- ✅ **Cost management** and budget monitoring in place
- ✅ **Consistent naming convention** for all resources
- ✅ **Validated environment** ready for hands-on learning

## 🚀 What's Next?

**Continue to Tutorial 2**: [Synapse Workspace Basics](02-workspace-basics.md)

In the next tutorial, you'll:
- Create your first Synapse workspace
- Explore the Synapse Studio interface
- Configure basic security and networking
- Set up your first Spark and SQL pools

## 💡 Troubleshooting

### **Common Issues and Solutions**

**Issue**: Azure CLI login fails
```powershell
# Clear cached credentials and retry
az account clear
az login --use-device-code
```

**Issue**: Insufficient permissions error  
```powershell
# Verify your role assignments
az role assignment list --assignee $(az account show --query user.name --output tsv) --output table
```

**Issue**: Resource provider registration stuck
```powershell
# Force re-registration
az provider register --namespace Microsoft.Synapse --wait
```

**Issue**: PowerShell execution policy blocks scripts
```powershell
# Set execution policy for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

**Tutorial Progress**: 1 of 14 completed  
**Next**: [02. Synapse Workspace Basics →](02-workspace-basics.md)  
**Time Investment**: 30 minutes ✅

*Environment setup is the foundation of success. Take time to ensure everything is properly configured before proceeding.*