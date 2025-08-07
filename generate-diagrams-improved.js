const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

// Directory containing placeholder .md files
const placeholdersDir = path.join(__dirname, 'docs', 'images', 'diagrams');
// Output directory for PNG images (same as placeholders)
const outputDir = path.join(__dirname, 'docs', 'images', 'diagrams');

// Create output directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Mermaid diagram data - hardcoded for diagrams that have missing or problematic mermaid code sections
const diagramData = {
  "integrated-data-governance": `graph TD
    subgraph "Governance Foundations"
        POLICY[Governance Policies]
        STANDARD[Data Standards]
        ROLES[Roles & Responsibilities]
    end
    
    subgraph "Azure Synapse Analytics"
        WORKSPACE[Synapse Workspace]
        SQLPOOL[Dedicated SQL Pool]
        SQLSERVER[Serverless SQL Pool]
        SPARK[Spark Pool]
        PIPELINE[Synapse Pipeline]
    end
    
    subgraph "Governance Services"
        PURVIEW[Microsoft Purview]
        KV[Azure Key Vault]
        RBAC[Azure RBAC]
        MONITOR[Azure Monitor]
    end
    
    POLICY --> PURVIEW
    STANDARD --> PURVIEW
    ROLES --> RBAC
    
    PURVIEW --> WORKSPACE
    PURVIEW --"Data Discovery"--> SQLPOOL
    PURVIEW --"Data Classification"--> SQLSERVER
    PURVIEW --"Lineage Tracking"--> SPARK
    PURVIEW --"Automated Scanning"--> PIPELINE
    
    KV --"Secrets Management"--> WORKSPACE
    KV --"Encryption Keys"--> SQLPOOL
    
    RBAC --"Access Control"--> WORKSPACE
    RBAC --"Permission Management"--> SQLPOOL
    RBAC --"Role Assignment"--> SQLSERVER
    RBAC --"Security Principal"--> SPARK
    
    MONITOR --"Auditing"--> WORKSPACE
    MONITOR --"Performance Tracking"--> SQLPOOL
    MONITOR --"Resource Utilization"--> SPARK
    MONITOR --"Pipeline Monitoring"--> PIPELINE`,
            
  "governance-maturity-model": `graph TD
    L1[Level 1:<br>Initial]
    L2[Level 2:<br>Repeatable]
    L3[Level 3:<br>Defined]
    L4[Level 4:<br>Managed]
    L5[Level 5:<br>Optimized]
    
    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> L5
    
    subgraph "Level 1: Initial"
        L1_1[Ad-hoc governance]
        L1_2[Basic security]
        L1_3[Manual processes]
    end
    
    subgraph "Level 2: Repeatable"
        L2_1[Documented standards]
        L2_2[Basic classification]
        L2_3[Manual lineage tracking]
        L2_4[Regular reviews]
    end
    
    subgraph "Level 3: Defined"
        L3_1[Formal governance program]
        L3_2[Automated classification]
        L3_3[Basic lineage automation]
        L3_4[Defined metrics]
        L3_5[Integration with Purview]
    end
    
    subgraph "Level 4: Managed"
        L4_1[Quantitative management]
        L4_2[Automated compliance]
        L4_3[Full lineage automation]
        L4_4[Advanced security]
        L4_5[Comprehensive metadata]
    end
    
    subgraph "Level 5: Optimized"
        L5_1[Continuous improvement]
        L5_2[Predictive governance]
        L5_3[Self-service capabilities]
        L5_4[Business value alignment]
        L5_5[Cross-platform governance]
    end`,

  "end-to-end-governance": `graph TD
    subgraph "Data Sources"
        ERP[ERP Systems]
        CRM[CRM Platforms]
        IOT[IoT Devices]
        APP[Applications]
    end
    
    subgraph "Data Integration"
        ADF[Azure Data Factory]
        EVENTS[Event Hubs]
        STREAMS[Stream Analytics]
    end
    
    subgraph "Data Storage"
        ADLS[Azure Data Lake Storage]
        SYNAPSE[Synapse Analytics]
        COSMOS[Cosmos DB]
    end
    
    subgraph "Data Processing"
        SPARK[Synapse Spark]
        SQL[Synapse SQL]
        NOTEBOOKS[Synapse Notebooks]
    end
    
    subgraph "Data Consumption"
        POWERBI[Power BI]
        ML[Azure ML]
        API[Custom APIs]
    end
    
    subgraph "Governance Controls"
        PURVIEW[Microsoft Purview]
        ENTRA[Microsoft Entra ID]
        RBAC[Azure RBAC]
        POLICIES[Azure Policies]
        KV[Key Vault]
        MONITOR[Azure Monitor]
    end
    
    ERP --> ADF
    CRM --> ADF
    IOT --> EVENTS
    APP --> ADF
    
    ADF --> ADLS
    EVENTS --> STREAMS
    STREAMS --> ADLS
    
    ADLS --> SPARK
    ADLS --> SQL
    
    SPARK --> SYNAPSE
    SQL --> SYNAPSE
    
    SYNAPSE --> POWERBI
    SYNAPSE --> ML
    SYNAPSE --> API
    
    PURVIEW -.- ADLS
    PURVIEW -.- SYNAPSE
    PURVIEW -.- ADF
    
    ENTRA -.- ADF
    ENTRA -.- ADLS
    ENTRA -.- SYNAPSE
    ENTRA -.- POWERBI
    
    RBAC -.- ADLS
    RBAC -.- SYNAPSE
    
    POLICIES -.- ADLS
    POLICIES -.- SYNAPSE
    
    KV -.- ADF
    KV -.- SYNAPSE
    
    MONITOR -.- ADF
    MONITOR -.- SYNAPSE
    MONITOR -.- ADLS`,
    
  "compliance-controls": `graph TD
    subgraph "Regulatory Requirements"
        GDPR[GDPR]
        HIPAA[HIPAA]
        PCI[PCI DSS]
        SOX[Sarbanes-Oxley]
    end
    
    subgraph "Azure Synapse Controls"
        AC[Access Controls]
        DL[Data Lifecycle]
        PP[Privacy Protection]
        DP[Data Protection]
        AM[Activity Monitoring]
        DR[Disaster Recovery]
    end
    
    subgraph "Implementation Components"
        RBAC[Azure RBAC]
        PURVIEW[Microsoft Purview]
        MASKING[Dynamic Data Masking]
        ENC[Transparent Data Encryption]
        RLS[Row Level Security]
        AUD[Advanced Auditing]
        KV[Azure Key Vault]
        BACKUP[Automated Backups]
        GEO[Geo-Replication]
    end
    
    GDPR --> PP
    HIPAA --> DP
    PCI --> DP
    SOX --> AM
    
    AC --> RBAC
    DL --> PURVIEW
    PP --> MASKING
    PP --> RLS
    DP --> ENC
    DP --> KV
    AM --> AUD
    DR --> BACKUP
    DR --> GEO`,
    
  "data-protection-model": `graph TD
    subgraph "Data Classification"
        PUBLIC[Public]
        INTERNAL[Internal]
        CONFIDENTIAL[Confidential]
        RESTRICTED[Restricted]
    end
    
    subgraph "Protection Controls"
        AAD[Microsoft Entra ID]
        RBAC[Azure RBAC]
        FW[Firewall Rules]
        PE[Private Endpoints]
        ENCRYPT[Encryption]
        MASK[Dynamic Data Masking]
        RLS[Row-Level Security]
        CLS[Column-Level Security]
        AUDIT[Auditing]
        MFA[Multi-Factor Auth]
    end
    
    subgraph "Implementation Layer"
        NETWORK[Network Layer]
        STORAGE[Storage Layer]
        SQL[SQL Layer]
        ACCESS[Access Layer]
    end
    
    PUBLIC --> NETWORK
    INTERNAL --> NETWORK
    INTERNAL --> STORAGE
    CONFIDENTIAL --> STORAGE
    CONFIDENTIAL --> SQL
    RESTRICTED --> SQL
    RESTRICTED --> ACCESS
    
    NETWORK --> FW
    NETWORK --> PE
    STORAGE --> ENCRYPT
    STORAGE --> AAD
    SQL --> MASK
    SQL --> RLS
    SQL --> CLS
    ACCESS --> RBAC
    ACCESS --> MFA
    ACCESS --> AUDIT`,
    
  "identity-access-architecture": `graph LR
    subgraph "Identity Sources"
        AAD[Microsoft Entra ID]
        B2B[External Identities]
        MFA[Multi-Factor Auth]
    end
    
    subgraph "Access Management"
        RBAC[Azure RBAC]
        CM[Conditional Access]
        PIM[Privileged Identity Management]
    end
    
    subgraph "Azure Synapse Resources"
        WS[Workspace]
        SQLPOOL[Dedicated SQL Pool]
        SERVERLESS[Serverless SQL Pool]
        SPARK[Spark Pool]
        PIPELINE[Pipelines]
        ADLS[ADLS Gen2]
    end
    
    AAD --> RBAC
    B2B --> AAD
    MFA --> AAD
    AAD --> CM
    AAD --> PIM
    
    RBAC --"Control Plane"--> WS
    RBAC --"Data Plane"--> SQLPOOL
    RBAC --"Data Plane"--> SERVERLESS
    RBAC --"Data Plane"--> SPARK
    RBAC --"Data Plane"--> PIPELINE
    
    CM --> WS
    PIM --> RBAC
    
    WS --> ADLS
    SQLPOOL --> ADLS
    SERVERLESS --> ADLS
    SPARK --> ADLS`,
    
  "network-isolation-architecture": `graph TD
    subgraph "Client Access"
        VC[Virtual Client]
        VPN[VPN Gateway]
        ER[ExpressRoute]
    end
    
    subgraph "Network Security"
        VNET[Virtual Network]
        NSG[Network Security Groups]
        FW[Azure Firewall]
        PE[Private Endpoints]
    end
    
    subgraph "Synapse Components"
        WORKSPACE[Synapse Workspace]
        SQLPOOL[Dedicated SQL Pool]
        SERVERLESS[Serverless SQL]
        SPARK[Spark Pool]
        ADLS[Data Lake Storage]
    end
    
    VC --> FW
    VPN --> VNET
    ER --> VNET
    
    FW --> VNET
    NSG --> VNET
    VNET --> PE
    
    PE --> WORKSPACE
    PE --> SQLPOOL
    PE --> SERVERLESS
    PE --> SPARK
    PE --> ADLS
    
    WORKSPACE --> ADLS
    SQLPOOL --> ADLS
    SERVERLESS --> ADLS
    SPARK --> ADLS`,
    
  "sensitive-data-protection": `graph TD
    subgraph "Data Discovery & Classification"
        SCAN[Automated Scanning]
        CLASS[Data Classification]
        SENS[Sensitivity Labels]
        TAX[Taxonomy Management]
    end
    
    subgraph "Protection Methods"
        MASK[Dynamic Data Masking]
        RLS[Row-Level Security]
        CLS[Column-Level Security]
        TDE[Transparent Data Encryption]
        AKV[Azure Key Vault]
        CMEK[Customer Managed Keys]
    end
    
    subgraph "Monitoring & Compliance"
        AUDIT[Advanced Auditing]
        ALERT[Alerting]
        REPORT[Compliance Reporting]
        VULN[Vulnerability Assessment]
    end
    
    SCAN --> CLASS
    CLASS --> SENS
    SENS --> TAX
    
    SENS --> MASK
    SENS --> RLS
    SENS --> CLS
    
    MASK --> AUDIT
    RLS --> AUDIT
    CLS --> AUDIT
    
    TDE --> AKV
    AKV --> CMEK
    
    AUDIT --> ALERT
    ALERT --> REPORT
    VULN --> REPORT`
};

// Function to extract Mermaid code from markdown file
function extractMermaidCode(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  
  // Try different regex patterns to extract the Mermaid code
  let mermaidMatch = content.match(/```mermaid\n([\s\S]*?)```/);
  if (!mermaidMatch) {
    // Try without newline
    mermaidMatch = content.match(/```mermaid([\s\S]*?)```/);
  }
  
  if (mermaidMatch && mermaidMatch[1]) {
    return mermaidMatch[1].trim();
  }
  
  // Get the filename without extension to check hardcoded diagrams
  const baseFileName = path.basename(filePath, '.png.md');
  
  if (diagramData[baseFileName]) {
    console.log(`Using hardcoded diagram for: ${baseFileName}`);
    return diagramData[baseFileName];
  }
  
  console.error(`No Mermaid code found in ${filePath} and no hardcoded diagram available`);
  return null;
}

// Function to generate a PNG from Mermaid code using the CLI
async function generatePNG(mermaidCode, outputPath) {
  // Create a temporary file for the Mermaid code
  const tempFile = path.join(__dirname, `${path.basename(outputPath, '.png')}.mmd`);
  fs.writeFileSync(tempFile, mermaidCode);
  
  try {
    // Run the Mermaid CLI command
    console.log(`Generating: ${outputPath}`);
    await execPromise(`npx @mermaid-js/mermaid-cli -i "${tempFile}" -o "${outputPath}" -b transparent`);
    console.log(`Successfully generated: ${outputPath}`);
    return true;
  } catch (error) {
    console.error(`Error generating diagram: ${error.message}`);
    return false;
  } finally {
    // Clean up the temporary file
    if (fs.existsSync(tempFile)) {
      fs.unlinkSync(tempFile);
    }
  }
}

// Process all placeholder files
async function processAllDiagrams() {
  try {
    const files = fs.readdirSync(placeholdersDir);
    
    // Filter to only get the .png.md placeholder files
    const placeholderFiles = files.filter(file => file.endsWith('.png.md'));
    console.log(`Found ${placeholderFiles.length} placeholder files to process.`);
    
    let successCount = 0;
    let failCount = 0;
    
    // Process each file
    for (const file of placeholderFiles) {
      const filePath = path.join(placeholdersDir, file);
      const mermaidCode = extractMermaidCode(filePath);
      
      if (mermaidCode) {
        // Output PNG path is the same as the placeholder but without the .md extension
        const outputPath = path.join(outputDir, file.replace('.md', ''));
        const success = await generatePNG(mermaidCode, outputPath);
        if (success) {
          successCount++;
        } else {
          failCount++;
        }
      } else {
        failCount++;
      }
    }
    
    console.log(`All diagrams processed! Success: ${successCount}, Failed: ${failCount}`);
  } catch (error) {
    console.error(`Error processing diagrams: ${error.message}`);
  }
}

// Run the processing function
processAllDiagrams();
