# 📋 Prerequisites and Setup Guide

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎓 [Tutorials](../README.md)** | **🏗️ [Architecture Tutorials](README.md)** | **📋 Prerequisites**

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Level](https://img.shields.io/badge/Level-Beginner-green?style=flat-square)
![Time](https://img.shields.io/badge/Time-30--60_minutes-blue?style=flat-square)

Complete setup guide for running Azure Cloud Scale Analytics architecture pattern tutorials. This guide ensures you have all required tools, access, and configuration to successfully complete the tutorials.

---

## 🎯 Overview

Before starting any architecture pattern tutorial, you need to set up your development environment and Azure account. This guide walks you through:

- **Azure subscription setup**
- **Development tools installation**
- **IDE configuration** (VS Code)
- **Azure CLI setup and authentication**
- **Sample data and repository setup**

**Estimated Time**: 30-60 minutes (depending on your starting point)

---

## 📋 Table of Contents

- [Azure Account Setup](#azure-account-setup)
- [Development Tools](#development-tools)
- [VS Code Setup](#vs-code-setup)
- [Azure CLI Setup](#azure-cli-setup)
- [Python Environment](#python-environment)
- [Git and Repository Setup](#git-and-repository-setup)
- [Optional Tools](#optional-tools)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## 🔑 Azure Account Setup

### Create Azure Subscription

If you don't have an Azure subscription, create one:

1. **Free Account** (Recommended for beginners):
   - Visit [Azure Free Account](https://azure.microsoft.com/en-us/free/)
   - Get $200 credit for 30 days
   - 12 months of popular free services
   - Always-free services

2. **Pay-As-You-Go**:
   - Visit [Azure Portal](https://portal.azure.com)
   - Sign up for pay-as-you-go subscription
   - Only pay for what you use

### Required Permissions

Ensure you have the appropriate role in your Azure subscription:

| Role | Required For | Permissions |
|------|--------------|-------------|
| **Owner** | ✅ Recommended | Full access to all resources |
| **Contributor** | ✅ Minimum | Manage all resources (except access) |
| **Reader** | ❌ Insufficient | Read-only access |

**To check your role:**

```bash
# Login to Azure
az login

# List your subscriptions and roles
az role assignment list --assignee <your-email> --output table
```

### Get Subscription Information

You'll need these values for the tutorials:

```bash
# Get your subscription ID
az account show --query id --output tsv

# Get your tenant ID
az account show --query tenantId --output tsv

# Set environment variables (optional but recommended)
export AZURE_SUBSCRIPTION_ID=$(az account show --query id --output tsv)
export AZURE_TENANT_ID=$(az account show --query tenantId --output tsv)
```

> 💡 **Tip**: Save these IDs in a secure note for easy reference during tutorials.

---

## 💻 Development Tools

### Required Software

| Tool | Version | Purpose | Download Link |
|------|---------|---------|---------------|
| **Azure CLI** | 2.50+ | Deploy and manage Azure resources | [Download](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) |
| **Python** | 3.8+ | Run notebooks and scripts | [Download](https://www.python.org/downloads/) |
| **Git** | Latest | Version control and clone repository | [Download](https://git-scm.com/downloads) |
| **VS Code** | Latest | Primary IDE | [Download](https://code.visualstudio.com/) |

### Installation Instructions

#### Windows

```powershell
# Install using winget (Windows Package Manager)
winget install Microsoft.AzureCLI
winget install Python.Python.3.11
winget install Git.Git
winget install Microsoft.VisualStudioCode

# Verify installations
az version
python --version
git --version
code --version
```

#### macOS

```bash
# Install using Homebrew
brew install azure-cli
brew install python@3.11
brew install git
brew install --cask visual-studio-code

# Verify installations
az version
python3 --version
git --version
code --version
```

#### Linux (Ubuntu/Debian)

```bash
# Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Python 3.11
sudo apt update
sudo apt install python3.11 python3-pip python3-venv

# Git
sudo apt install git

# VS Code
sudo snap install code --classic

# Verify installations
az version
python3 --version
git --version
code --version
```

---

## 🔧 VS Code Setup

### Install VS Code Extensions

Install these essential extensions for Azure development:

```bash
# Install via VS Code command palette (Ctrl+P / Cmd+P)
ext install ms-python.python
ext install ms-azuretools.vscode-azureresourcegroups
ext install ms-azuretools.vscode-azurefunctions
ext install ms-dotnettools.csharp
ext install ms-toolsai.jupyter
ext install ms-vscode.azure-account
ext install msazurermtools.azurerm-vscode-tools
ext install redhat.vscode-yaml
```

### Recommended Extensions

| Extension | Purpose |
|-----------|---------|
| **Python** | Python language support |
| **Jupyter** | Run polyglot notebooks |
| **Azure Account** | Azure authentication |
| **Azure Resources** | Manage Azure resources |
| **Azure Functions** | Azure Functions development |
| **Bicep** | IaC template authoring |
| **YAML** | YAML file support |

### VS Code Settings

Create or update your VS Code settings (`.vscode/settings.json`):

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "jupyter.askForKernelRestart": false,
  "azure.tenant": "your-tenant-id",
  "azure.cloud": "AzureCloud",
  "files.associations": {
    "*.bicep": "bicep",
    "*.ipynb": "jupyter-notebook"
  },
  "editor.formatOnSave": true,
  "editor.rulers": [100],
  "files.trimTrailingWhitespace": true
}
```

---

## ⚙️ Azure CLI Setup

### Login to Azure

```bash
# Interactive browser login
az login

# Login with service principal (for automation)
az login --service-principal \
  --username <app-id> \
  --password <password-or-cert> \
  --tenant <tenant-id>
```

### Set Default Subscription

```bash
# List available subscriptions
az account list --output table

# Set default subscription
az account set --subscription "<subscription-name-or-id>"

# Verify current subscription
az account show --output table
```

### Configure CLI Defaults

```bash
# Set default resource group (optional)
az configure --defaults group=<resource-group-name>

# Set default location
az configure --defaults location=eastus

# View current configuration
az configure --list-defaults
```

### Install Azure CLI Extensions

```bash
# Install Bicep CLI
az bicep install

# Upgrade Bicep to latest version
az bicep upgrade

# Install Azure Synapse extension
az extension add --name synapse

# Install Azure Event Hubs extension
az extension add --name eventhubs

# List installed extensions
az extension list --output table
```

---

## 🐍 Python Environment

### Create Virtual Environment

```bash
# Navigate to tutorials directory
cd docs/tutorials/architecture-patterns

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Install Required Packages

```bash
# Install core packages
pip install jupyter notebook ipykernel
pip install azure-identity azure-mgmt-resource
pip install azure-storage-blob azure-eventhub
pip install pandas numpy matplotlib

# Install packages for specific services
pip install azure-synapse-spark azure-synapse-artifacts
pip install azure-cosmos azure-data-tables
pip install azure-ai-ml azure-monitor-query

# Save installed packages
pip freeze > requirements.txt
```

### Configure Jupyter Kernel

```bash
# Add virtual environment as Jupyter kernel
python -m ipykernel install --user --name=azure-tutorials --display-name="Azure Tutorials"

# List available kernels
jupyter kernelspec list

# Start Jupyter
jupyter notebook
```

---

## 📦 Git and Repository Setup

### Clone Repository

```bash
# Clone the documentation repository
git clone https://github.com/fgarofalo56/csa-inabox-docs.git

# Navigate to repository
cd csa-inabox-docs

# Navigate to tutorials directory
cd docs/tutorials/architecture-patterns
```

### Configure Git

```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Enable credential caching
git config --global credential.helper cache
```

---

## 🛠️ Optional Tools

### Azure Storage Explorer

**Purpose**: Browse and manage Azure storage accounts visually.

**Download**: [Azure Storage Explorer](https://azure.microsoft.com/en-us/products/storage/storage-explorer/)

**Key Features**:
- Browse blobs, tables, queues
- Upload/download data
- Manage access policies
- Generate SAS tokens

### Postman

**Purpose**: Test REST APIs and HTTP requests.

**Download**: [Postman](https://www.postman.com/downloads/)

**Use Cases**:
- Test Azure REST APIs
- Debug API responses
- Share API collections

### Power BI Desktop

**Purpose**: Create data visualizations and reports.

**Download**: [Power BI Desktop](https://powerbi.microsoft.com/en-us/desktop/)

**Use Cases**:
- Connect to Azure data sources
- Build dashboards
- Test analytics queries

### Azure Data Studio

**Purpose**: Query and manage Azure databases.

**Download**: [Azure Data Studio](https://learn.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio)

**Use Cases**:
- Query Azure SQL databases
- Manage Synapse dedicated pools
- Run T-SQL scripts

---

## ✅ Verification

### Verify All Tools

Run this verification script to ensure everything is set up correctly:

```bash
#!/bin/bash

echo "🔍 Verifying Prerequisites..."
echo ""

# Azure CLI
echo "✓ Checking Azure CLI..."
az version --output tsv | head -1 || echo "❌ Azure CLI not found"

# Python
echo "✓ Checking Python..."
python3 --version || echo "❌ Python not found"

# Git
echo "✓ Checking Git..."
git --version || echo "❌ Git not found"

# VS Code
echo "✓ Checking VS Code..."
code --version || echo "❌ VS Code not found"

# Jupyter
echo "✓ Checking Jupyter..."
jupyter --version || echo "❌ Jupyter not found"

# Azure Login Status
echo "✓ Checking Azure login..."
az account show --output table || echo "❌ Not logged into Azure"

# Bicep
echo "✓ Checking Bicep..."
az bicep version || echo "❌ Bicep not installed"

echo ""
echo "✅ Verification complete!"
```

### Quick Test Deployment

Test your setup with a simple resource group creation:

```bash
# Create test resource group
az group create \
  --name rg-test-setup \
  --location eastus

# Verify creation
az group show --name rg-test-setup --output table

# Clean up (delete test resource group)
az group delete --name rg-test-setup --yes --no-wait
```

---

## 🔧 Troubleshooting

### Azure CLI Issues

**Problem**: `az: command not found`

**Solution**:
```bash
# Windows: Add to PATH
# C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin

# macOS: Reinstall via Homebrew
brew reinstall azure-cli

# Linux: Verify installation path
which az
```

**Problem**: `az login` fails

**Solution**:
```bash
# Clear Azure CLI cache
az account clear

# Use device code flow
az login --use-device-code

# Check proxy settings
az configure --list-defaults
```

### Python Issues

**Problem**: `python: command not found`

**Solution**:
```bash
# Try python3 instead
python3 --version

# Create alias (add to ~/.bashrc or ~/.zshrc)
alias python=python3
```

**Problem**: Virtual environment not activating

**Solution**:
```bash
# Windows PowerShell: Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
```

### Jupyter Issues

**Problem**: Kernel not found

**Solution**:
```bash
# Reinstall kernel
python -m ipykernel install --user --name=azure-tutorials

# Restart Jupyter
jupyter notebook stop
jupyter notebook
```

**Problem**: Azure SDK import errors

**Solution**:
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Reinstall packages
pip install --upgrade azure-identity azure-mgmt-resource
```

### VS Code Issues

**Problem**: Extensions not installing

**Solution**:
```bash
# Clear extension cache
rm -rf ~/.vscode/extensions

# Reinstall extensions
code --install-extension ms-python.python
```

**Problem**: Azure account sign-in fails

**Solution**:
1. Open VS Code
2. Press `F1` or `Ctrl+Shift+P`
3. Type "Azure: Sign Out"
4. Type "Azure: Sign In"
5. Complete authentication in browser

---

## 📚 Additional Resources

### Documentation

- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)
- [Python Azure SDK](https://learn.microsoft.com/en-us/azure/developer/python/)
- [VS Code Azure Extensions](https://code.visualstudio.com/docs/azure/extensions)
- [Jupyter Documentation](https://jupyter.org/documentation)

### Learning Resources

- [Azure Fundamentals](https://learn.microsoft.com/en-us/training/paths/az-900-describe-cloud-concepts/)
- [Python for Beginners](https://learn.microsoft.com/en-us/training/paths/beginner-python/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)

### Community

- [Azure Community](https://azure.microsoft.com/en-us/community/)
- [Microsoft Q&A](https://learn.microsoft.com/en-us/answers/)
- [Stack Overflow - Azure](https://stackoverflow.com/questions/tagged/azure)

---

## ✅ Next Steps

Once you've completed this setup guide:

1. ✅ **Verify all tools** are installed and working
2. ✅ **Test Azure CLI** login and access
3. ✅ **Configure VS Code** with extensions
4. ✅ **Create Python environment** for notebooks
5. ✅ **Choose your first tutorial** from the [Architecture Patterns](README.md)

### Recommended First Tutorials

For beginners, start with:

1. [Medallion Architecture Tutorial](batch/medallion-architecture-tutorial.md) - Data quality focused
2. [Kappa Architecture Tutorial](streaming/kappa-architecture-tutorial.md) - Simple streaming
3. [Hub & Spoke Tutorial](batch/hub-spoke-tutorial.md) - Traditional warehouse

---

**Last Updated**: 2025-12-12  
**Estimated Completion Time**: 30-60 minutes  
**Difficulty**: ![Beginner](https://img.shields.io/badge/-Beginner-green?style=flat-square)

---

> 🎉 **Congratulations!** You're now ready to start building Azure Cloud Scale Analytics solutions. Choose a tutorial and begin your journey!
