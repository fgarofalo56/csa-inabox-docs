#!/bin/bash

################################################################################
# Medallion Architecture - Deployment Script
# 
# This script deploys the complete Medallion Architecture infrastructure
# including Azure Synapse Analytics, Data Lake Gen2, Spark pools, and monitoring.
#
# Prerequisites:
# - Azure CLI installed and logged in
# - Appropriate permissions on Azure subscription
# - Bicep CLI installed (az bicep install)
#
# Usage:
#   ./deploy.sh
#
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
RESOURCE_GROUP_NAME="${RESOURCE_GROUP_NAME:-rg-medallion-tutorial}"
LOCATION="${LOCATION:-eastus}"
DEPLOYMENT_NAME="medallion-$(date +%Y%m%d-%H%M%S)"

# Generate unique names
UNIQUE_SUFFIX="${USER}-$(openssl rand -hex 3)"
SYNAPSE_WORKSPACE_NAME="synapse-med-${UNIQUE_SUFFIX}"
STORAGE_ACCOUNT_NAME="samed${UNIQUE_SUFFIX//[^a-z0-9]/}"
SQL_ADMIN_USER="sqladmin"
SQL_ADMIN_PASSWORD="$(openssl rand -base64 32 | tr -d /+= | cut -c1-20)Pass1!"

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Medallion Architecture Deployment Script                ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Verify Azure CLI login
echo -e "${YELLOW}[1/6] Verifying Azure CLI login...${NC}"
if ! az account show &> /dev/null; then
    echo -e "${RED}❌ Not logged into Azure. Running 'az login'...${NC}"
    az login
else
    echo -e "${GREEN}✓ Logged into Azure${NC}"
    az account show --output table
fi

# Step 2: Create or verify resource group
echo -e "\n${YELLOW}[2/6] Creating resource group...${NC}"
if az group show --name "$RESOURCE_GROUP_NAME" &> /dev/null; then
    echo -e "${GREEN}✓ Resource group already exists: $RESOURCE_GROUP_NAME${NC}"
else
    az group create \
        --name "$RESOURCE_GROUP_NAME" \
        --location "$LOCATION" \
        --tags "Environment=Tutorial" "Pattern=Medallion" "CostCenter=Learning"
    echo -e "${GREEN}✓ Created resource group: $RESOURCE_GROUP_NAME${NC}"
fi

# Step 3: Validate Bicep template
echo -e "\n${YELLOW}[3/6] Validating Bicep template...${NC}"
az deployment group validate \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --template-file main.bicep \
    --parameters \
        synapseWorkspaceName="$SYNAPSE_WORKSPACE_NAME" \
        storageAccountName="$STORAGE_ACCOUNT_NAME" \
        location="$LOCATION" \
        sqlAdministratorLogin="$SQL_ADMIN_USER" \
        sqlAdministratorLoginPassword="$SQL_ADMIN_PASSWORD" \
    --output none

echo -e "${GREEN}✓ Template validation successful${NC}"

# Step 4: Deploy infrastructure
echo -e "\n${YELLOW}[4/6] Deploying infrastructure (this may take 10-15 minutes)...${NC}"
az deployment group create \
    --name "$DEPLOYMENT_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --template-file main.bicep \
    --parameters \
        synapseWorkspaceName="$SYNAPSE_WORKSPACE_NAME" \
        storageAccountName="$STORAGE_ACCOUNT_NAME" \
        location="$LOCATION" \
        sqlAdministratorLogin="$SQL_ADMIN_USER" \
        sqlAdministratorLoginPassword="$SQL_ADMIN_PASSWORD" \
    --output json > deployment-output.json

echo -e "${GREEN}✓ Infrastructure deployed successfully${NC}"

# Step 5: Get deployment outputs
echo -e "\n${YELLOW}[5/6] Retrieving deployment information...${NC}"
SYNAPSE_WEB_URL=$(jq -r '.properties.outputs.synapseWebUrl.value' deployment-output.json)
SYNAPSE_SQL_ENDPOINT=$(jq -r '.properties.outputs.synapseSqlEndpoint.value' deployment-output.json)
DATA_LAKE_ENDPOINT=$(jq -r '.properties.outputs.dataLakePrimaryEndpoint.value' deployment-output.json)

# Step 6: Save configuration
echo -e "\n${YELLOW}[6/6] Saving configuration...${NC}"
cat > .deployment-config.env << EOF
# Medallion Architecture Deployment Configuration
# Generated: $(date)

export AZURE_SUBSCRIPTION_ID=$(az account show --query id --output tsv)
export RESOURCE_GROUP_NAME="$RESOURCE_GROUP_NAME"
export LOCATION="$LOCATION"

export SYNAPSE_WORKSPACE_NAME="$SYNAPSE_WORKSPACE_NAME"
export STORAGE_ACCOUNT_NAME="$STORAGE_ACCOUNT_NAME"
export SQL_ADMIN_USER="$SQL_ADMIN_USER"
export SQL_ADMIN_PASSWORD="$SQL_ADMIN_PASSWORD"

export SYNAPSE_WEB_URL="$SYNAPSE_WEB_URL"
export SYNAPSE_SQL_ENDPOINT="$SYNAPSE_SQL_ENDPOINT"
export DATA_LAKE_ENDPOINT="$DATA_LAKE_ENDPOINT"
EOF

chmod 600 .deployment-config.env

echo -e "${GREEN}✓ Configuration saved to .deployment-config.env${NC}"

# Display summary
echo -e "\n${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Deployment Summary                              ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Resource Group:       ${GREEN}$RESOURCE_GROUP_NAME${NC}"
echo -e "  Location:             ${GREEN}$LOCATION${NC}"
echo -e "  Synapse Workspace:    ${GREEN}$SYNAPSE_WORKSPACE_NAME${NC}"
echo -e "  Storage Account:      ${GREEN}$STORAGE_ACCOUNT_NAME${NC}"
echo ""
echo -e "  Synapse Studio:       ${GREEN}$SYNAPSE_WEB_URL${NC}"
echo -e "  SQL Endpoint:         ${GREEN}$SYNAPSE_SQL_ENDPOINT${NC}"
echo ""
echo -e "${YELLOW}⚠️  Important: SQL Admin Password has been saved in .deployment-config.env${NC}"
echo -e "${YELLOW}   Keep this file secure and do not commit to version control!${NC}"
echo ""
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo ""
echo -e "Next steps:"
echo -e "  1. Load environment: ${GREEN}source .deployment-config.env${NC}"
echo -e "  2. Open Synapse Studio: ${GREEN}$SYNAPSE_WEB_URL${NC}"
echo -e "  3. Run the tutorial notebooks"
echo ""
