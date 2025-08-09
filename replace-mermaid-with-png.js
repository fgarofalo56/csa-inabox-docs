const fs = require('fs');
const path = require('path');

// Available PNG diagrams
const availableDiagrams = [
  'compliance-controls',
  'data-classification-framework',
  'data-governance-decision-tree',
  'data-pipeline-implementation',
  'data-protection-model',
  'data-quality-framework',
  'defense-in-depth-security',
  'delta-lake-optimization',
  'delta-lake-write-flow',
  'end-to-end-governance',
  'enterprise-scale-architecture',
  'governance-maturity-model',
  'governance-roles',
  'identity-access-architecture',
  'incident-response-process',
  'integrated-data-governance',
  'multi-region-architecture',
  'network-isolation-architecture',
  'performance-optimization',
  'purview-integration',
  'sensitive-data-protection',
  'serverless-sql-query-flow',
  'serverless-sql-troubleshooting'
];

// Mapping of diagram names to their titles for alt text
const diagramTitles = {
  'compliance-controls': 'Compliance Controls Framework',
  'data-classification-framework': 'Data Classification Framework',
  'data-governance-decision-tree': 'Data Governance Decision Tree',
  'data-pipeline-implementation': 'Data Pipeline Implementation',
  'data-protection-model': 'Data Protection Model',
  'data-quality-framework': 'Data Quality Framework',
  'defense-in-depth-security': 'Defense in Depth Security Architecture',
  'delta-lake-optimization': 'Delta Lake Optimization Process',
  'delta-lake-write-flow': 'Delta Lake Write Flow',
  'end-to-end-governance': 'End-to-End Data Governance',
  'enterprise-scale-architecture': 'Enterprise Scale Architecture',
  'governance-maturity-model': 'Governance Maturity Model',
  'governance-roles': 'Data Governance Roles and Responsibilities',
  'identity-access-architecture': 'Identity and Access Management Architecture',
  'incident-response-process': 'Security Incident Response Process',
  'integrated-data-governance': 'Integrated Data Governance Architecture',
  'multi-region-architecture': 'Multi-Region Architecture',
  'network-isolation-architecture': 'Network Isolation Architecture',
  'performance-optimization': 'Performance Optimization Framework',
  'purview-integration': 'Microsoft Purview Integration',
  'sensitive-data-protection': 'Sensitive Data Protection Framework',
  'serverless-sql-query-flow': 'Serverless SQL Query Flow',
  'serverless-sql-troubleshooting': 'Serverless SQL Troubleshooting Process'
};

// Function to find diagram name from mermaid content or context
function identifyDiagramFromContent(content, filePath) {
  const fileName = path.basename(filePath, '.md');
  
  // Check if filename matches a diagram
  for (const diagram of availableDiagrams) {
    if (fileName.includes(diagram) || filePath.includes(diagram)) {
      return diagram;
    }
  }
  
  // Check content for keywords
  const contentLower = content.toLowerCase();
  
  if (contentLower.includes('compliance') && contentLower.includes('control')) return 'compliance-controls';
  if (contentLower.includes('data classification')) return 'data-classification-framework';
  if (contentLower.includes('governance') && contentLower.includes('decision')) return 'data-governance-decision-tree';
  if (contentLower.includes('pipeline') && contentLower.includes('implementation')) return 'data-pipeline-implementation';
  if (contentLower.includes('data protection')) return 'data-protection-model';
  if (contentLower.includes('data quality')) return 'data-quality-framework';
  if (contentLower.includes('defense') && contentLower.includes('depth')) return 'defense-in-depth-security';
  if (contentLower.includes('delta') && contentLower.includes('optimization')) return 'delta-lake-optimization';
  if (contentLower.includes('delta') && contentLower.includes('write')) return 'delta-lake-write-flow';
  if (contentLower.includes('end-to-end') && contentLower.includes('governance')) return 'end-to-end-governance';
  if (contentLower.includes('enterprise') && contentLower.includes('scale')) return 'enterprise-scale-architecture';
  if (contentLower.includes('maturity') && contentLower.includes('model')) return 'governance-maturity-model';
  if (contentLower.includes('governance') && contentLower.includes('roles')) return 'governance-roles';
  if (contentLower.includes('identity') && contentLower.includes('access')) return 'identity-access-architecture';
  if (contentLower.includes('incident') && contentLower.includes('response')) return 'incident-response-process';
  if (contentLower.includes('integrated') && contentLower.includes('governance')) return 'integrated-data-governance';
  if (contentLower.includes('multi-region')) return 'multi-region-architecture';
  if (contentLower.includes('network') && contentLower.includes('isolation')) return 'network-isolation-architecture';
  if (contentLower.includes('performance') && contentLower.includes('optimization')) return 'performance-optimization';
  if (contentLower.includes('purview') && contentLower.includes('integration')) return 'purview-integration';
  if (contentLower.includes('sensitive') && contentLower.includes('data')) return 'sensitive-data-protection';
  if (contentLower.includes('serverless') && contentLower.includes('query')) return 'serverless-sql-query-flow';
  if (contentLower.includes('serverless') && contentLower.includes('troubleshooting')) return 'serverless-sql-troubleshooting';
  
  return null;
}

// Function to get relative path from current file to images directory
function getRelativeImagePath(currentFilePath, imageName) {
  const currentDir = path.dirname(currentFilePath);
  const imagesDir = path.join(__dirname, 'docs', 'images', 'diagrams');
  const relativePath = path.relative(currentDir, imagesDir);
  return path.join(relativePath, `${imageName}.png`).replace(/\\/g, '/');
}

// Function to replace mermaid blocks with PNG references
function replaceMermaidWithPNG(content, filePath) {
  let updatedContent = content;
  let replacements = 0;
  
  // Regular expression to match mermaid code blocks
  const mermaidRegex = /```mermaid\n([\s\S]*?)\n```/g;
  
  updatedContent = updatedContent.replace(mermaidRegex, (match, mermaidContent) => {
    const diagramName = identifyDiagramFromContent(mermaidContent + ' ' + filePath, filePath);
    
    if (diagramName && availableDiagrams.includes(diagramName)) {
      const imagePath = getRelativeImagePath(filePath, diagramName);
      const altText = diagramTitles[diagramName] || diagramName.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      
      replacements++;
      return `![${altText}](${imagePath})`;
    }
    
    // If we can't identify the diagram, leave the mermaid block as is
    console.log(`⚠️  Could not identify diagram for mermaid block in: ${filePath}`);
    return match;
  });
  
  return { content: updatedContent, replacements };
}

// Function to process all markdown files
function processMarkdownFiles(dir) {
  let totalReplacements = 0;
  let filesProcessed = 0;
  
  function processDirectory(currentDir) {
    const items = fs.readdirSync(currentDir);
    
    for (const item of items) {
      const itemPath = path.join(currentDir, item);
      const stat = fs.statSync(itemPath);
      
      if (stat.isDirectory()) {
        // Skip node_modules and .git directories
        if (item !== 'node_modules' && item !== '.git') {
          processDirectory(itemPath);
        }
      } else if (item.endsWith('.md')) {
        try {
          const content = fs.readFileSync(itemPath, 'utf8');
          const result = replaceMermaidWithPNG(content, itemPath);
          
          if (result.replacements > 0) {
            fs.writeFileSync(itemPath, result.content, 'utf8');
            console.log(`✅ Updated ${itemPath}: ${result.replacements} diagrams replaced`);
            totalReplacements += result.replacements;
            filesProcessed++;
          }
        } catch (error) {
          console.error(`❌ Error processing ${itemPath}:`, error.message);
        }
      }
    }
  }
  
  processDirectory(dir);
  
  console.log(`\n📊 Summary:`);
  console.log(`Files processed: ${filesProcessed}`);
  console.log(`Total diagram replacements: ${totalReplacements}`);
  console.log(`Available PNG diagrams: ${availableDiagrams.length}`);
}

// Start processing from the docs directory
const docsDir = path.join(__dirname, 'docs');
console.log('🔄 Starting to replace Mermaid diagrams with PNG images...\n');
processMarkdownFiles(docsDir);
console.log('\n✨ Diagram replacement complete!');
