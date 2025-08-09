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

// Enhanced diagram identification with more patterns
function identifyDiagramFromContent(content, filePath, context = '') {
  const fileName = path.basename(filePath, '.md');
  const fullContent = (content + ' ' + filePath + ' ' + context).toLowerCase();
  
  // Direct filename matches
  for (const diagram of availableDiagrams) {
    if (fileName.includes(diagram) || filePath.includes(diagram)) {
      return diagram;
    }
  }
  
  // Content-based identification with more patterns
  const patterns = {
    'compliance-controls': ['compliance', 'control', 'regulatory', 'audit'],
    'data-classification-framework': ['data classification', 'classification framework', 'data types'],
    'data-governance-decision-tree': ['governance decision', 'decision tree', 'governance flow'],
    'data-pipeline-implementation': ['pipeline implementation', 'data pipeline', 'etl pipeline'],
    'data-protection-model': ['data protection', 'protection model', 'data security model'],
    'data-quality-framework': ['data quality', 'quality framework', 'data validation'],
    'defense-in-depth-security': ['defense in depth', 'security layers', 'layered security'],
    'delta-lake-optimization': ['delta optimization', 'delta lake optimization', 'optimize delta'],
    'delta-lake-write-flow': ['delta write', 'write flow', 'delta lake write'],
    'end-to-end-governance': ['end-to-end governance', 'e2e governance', 'complete governance'],
    'enterprise-scale-architecture': ['enterprise scale', 'enterprise architecture', 'large scale'],
    'governance-maturity-model': ['maturity model', 'governance maturity', 'maturity levels'],
    'governance-roles': ['governance roles', 'roles responsibilities', 'data steward', 'data owner'],
    'identity-access-architecture': ['identity access', 'iam architecture', 'authentication'],
    'incident-response-process': ['incident response', 'security incident', 'incident handling'],
    'integrated-data-governance': ['integrated governance', 'unified governance', 'holistic governance'],
    'multi-region-architecture': ['multi-region', 'multiple regions', 'regional deployment'],
    'network-isolation-architecture': ['network isolation', 'network security', 'network segmentation'],
    'performance-optimization': ['performance optimization', 'performance tuning', 'optimize performance'],
    'purview-integration': ['purview integration', 'microsoft purview', 'purview connector'],
    'sensitive-data-protection': ['sensitive data', 'pii protection', 'data privacy'],
    'serverless-sql-query-flow': ['serverless query', 'sql query flow', 'query execution'],
    'serverless-sql-troubleshooting': ['serverless troubleshooting', 'sql troubleshooting', 'query issues']
  };
  
  for (const [diagram, keywords] of Object.entries(patterns)) {
    if (keywords.some(keyword => fullContent.includes(keyword))) {
      return diagram;
    }
  }
  
  // Fallback: try to match based on section headers or nearby content
  if (fullContent.includes('roles') && fullContent.includes('responsibilities')) return 'governance-roles';
  if (fullContent.includes('enterprise') && fullContent.includes('architecture')) return 'enterprise-scale-architecture';
  if (fullContent.includes('security') && fullContent.includes('defense')) return 'defense-in-depth-security';
  if (fullContent.includes('incident') && fullContent.includes('process')) return 'incident-response-process';
  if (fullContent.includes('optimization') && fullContent.includes('performance')) return 'performance-optimization';
  
  return null;
}

// Function to get relative path from current file to images directory
function getRelativeImagePath(currentFilePath, imageName) {
  const currentDir = path.dirname(currentFilePath);
  const imagesDir = path.join(__dirname, 'docs', 'images', 'diagrams');
  const relativePath = path.relative(currentDir, imagesDir);
  return path.join(relativePath, `${imageName}.png`).replace(/\\/g, '/');
}

// Function to extract context around mermaid blocks
function getContextAroundMermaid(content, mermaidMatch) {
  const beforeIndex = content.indexOf(mermaidMatch);
  const contextStart = Math.max(0, beforeIndex - 500);
  const contextEnd = Math.min(content.length, beforeIndex + mermaidMatch.length + 500);
  return content.substring(contextStart, contextEnd);
}

// Function to replace mermaid blocks with PNG references
function replaceMermaidWithPNG(content, filePath) {
  let updatedContent = content;
  let replacements = 0;
  
  // Regular expression to match mermaid code blocks with optional indentation
  const mermaidRegex = /(\s*)(```mermaid\n[\s\S]*?\n```)/g;
  
  updatedContent = updatedContent.replace(mermaidRegex, (match, indentation, mermaidBlock) => {
    const context = getContextAroundMermaid(content, match);
    const diagramName = identifyDiagramFromContent(mermaidBlock + ' ' + context, filePath, context);
    
    if (diagramName && availableDiagrams.includes(diagramName)) {
      const imagePath = getRelativeImagePath(filePath, diagramName);
      const altText = diagramTitles[diagramName] || diagramName.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      
      replacements++;
      // Preserve indentation and add proper spacing
      return `${indentation}![${altText}](${imagePath})\n`;
    }
    
    // If we can't identify the diagram, leave the mermaid block as is
    console.log(`⚠️  Could not identify diagram for mermaid block in: ${filePath}`);
    console.log(`   Context: ${context.substring(0, 100)}...`);
    return match;
  });
  
  return { content: updatedContent, replacements };
}

// Function to fix formatting issues from previous run
function fixFormattingIssues(content) {
  // Fix cases where text got concatenated with image markdown
  content = content.replace(/(\!\[.*?\]\(.*?\))([a-zA-Z])/g, '$1\n\n$2');
  
  // Ensure proper spacing around images
  content = content.replace(/(\!\[.*?\]\(.*?\))\n(?!\n)/g, '$1\n\n');
  
  return content;
}

// Function to process all markdown files
function processMarkdownFiles(dir) {
  let totalReplacements = 0;
  let filesProcessed = 0;
  let formattingFixes = 0;
  
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
          let content = fs.readFileSync(itemPath, 'utf8');
          
          // Fix formatting issues first
          const originalContent = content;
          content = fixFormattingIssues(content);
          if (content !== originalContent) {
            formattingFixes++;
          }
          
          // Replace mermaid diagrams
          const result = replaceMermaidWithPNG(content, itemPath);
          
          if (result.replacements > 0 || content !== originalContent) {
            fs.writeFileSync(itemPath, result.content, 'utf8');
            if (result.replacements > 0) {
              console.log(`✅ Updated ${itemPath}: ${result.replacements} diagrams replaced`);
            }
            if (content !== originalContent) {
              console.log(`🔧 Fixed formatting in ${itemPath}`);
            }
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
  console.log(`Formatting fixes: ${formattingFixes}`);
  console.log(`Available PNG diagrams: ${availableDiagrams.length}`);
}

// Start processing from the docs directory
const docsDir = path.join(__dirname, 'docs');
console.log('🔄 Starting improved Mermaid to PNG replacement...\n');
processMarkdownFiles(docsDir);
console.log('\n✨ Improved diagram replacement complete!');
