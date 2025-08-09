const fs = require('fs');
const path = require('path');

class DocumentationFixer {
  constructor(docsDir) {
    this.docsDir = docsDir;
    this.fixes = {
      brokenLinksFixed: 0,
      filesCreated: 0,
      filesRemoved: 0,
      linksUpdated: 0,
      navigationUpdated: 0
    };
  }

  // Create missing files that are referenced by other files
  createMissingFiles() {
    console.log('📝 Creating missing referenced files...');
    
    const missingFiles = [
      // Architecture images
      { path: 'docs/images/architecture/serverless-sql-architecture.png', type: 'placeholder' },
      { path: 'docs/images/architecture/shared-metadata-architecture.png', type: 'placeholder' },
      
      // Best practices files
      { path: 'docs/best-practices/pipeline-optimization.md', type: 'content' },
      { path: 'docs/best-practices/serverless-sql-best-practices.md', type: 'content' },
      { path: 'docs/best-practices/sql-performance.md', type: 'content' },
      { path: 'docs/best-practices/spark-performance.md', type: 'content' },
      
      // Monitoring files
      { path: 'docs/monitoring/sql-monitoring.md', type: 'content' },
      { path: 'docs/monitoring/spark-monitoring.md', type: 'content' },
      
      // Reference files
      { path: 'docs/reference/spark-configuration.md', type: 'content' },
      
      // Images
      { path: 'docs/images/troubleshooting-process.png', type: 'placeholder' }
    ];
    
    for (const file of missingFiles) {
      const fullPath = path.join(__dirname, file.path);
      const dir = path.dirname(fullPath);
      
      // Create directory if it doesn't exist
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log(`📁 Created directory: ${path.relative(__dirname, dir)}`);
      }
      
      if (!fs.existsSync(fullPath)) {
        if (file.type === 'content') {
          const fileName = path.basename(fullPath, '.md');
          const title = fileName.split('-').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
          ).join(' ');
          
          const content = `# ${title}

[Home](/README.md) > [Documentation](../README.md) > ${title}

## Overview

This document provides comprehensive guidance on ${title.toLowerCase()}.

## Key Concepts

### Important Points

- Key concept 1
- Key concept 2
- Key concept 3

## Best Practices

### Recommended Approaches

1. **First Practice**: Description of the first best practice
2. **Second Practice**: Description of the second best practice
3. **Third Practice**: Description of the third best practice

## Implementation Guide

### Step-by-Step Instructions

1. **Step 1**: Initial setup and configuration
2. **Step 2**: Implementation details
3. **Step 3**: Testing and validation

## Common Issues and Solutions

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Common Issue 1 | Solution description |
| Common Issue 2 | Solution description |

## Related Resources

- [Azure Synapse Analytics Documentation](https://docs.microsoft.com/azure/synapse-analytics/)
- [Best Practices Overview](../best-practices/README.md)

## Next Steps

- Review implementation guidelines
- Test configurations in development environment
- Monitor performance and optimize as needed
`;
          
          fs.writeFileSync(fullPath, content);
          console.log(`✅ Created content file: ${file.path}`);
          this.fixes.filesCreated++;
        } else if (file.type === 'placeholder') {
          // Create a placeholder file for images
          const content = `# Placeholder Image

This is a placeholder for the image: ${path.basename(fullPath)}

To replace this placeholder:
1. Create the actual image file
2. Remove this markdown file
3. Update any references to point to the image file directly
`;
          fs.writeFileSync(fullPath.replace('.png', '.md'), content);
          console.log(`📷 Created image placeholder: ${file.path}.md`);
          this.fixes.filesCreated++;
        }
      }
    }
  }

  // Fix broken links by updating paths
  fixBrokenLinks() {
    console.log('🔗 Fixing broken links...');
    
    const linkFixes = [
      // Fix double /docs/ paths
      { from: '/docs/docs/', to: '/docs/' },
      { from: '../docs/', to: '../' },
      
      // Fix specific broken links
      { from: '/docs/code-examples/', to: '../code-examples/' },
      { from: '/docs/best-practices/', to: '../best-practices/' },
      { from: '/docs/troubleshooting/', to: '../troubleshooting/' },
      { from: '/docs/reference/', to: '../reference/' },
      { from: '/docs/monitoring/', to: '../monitoring/' }
    ];
    
    const allMarkdownFiles = this.findAllMarkdownFiles();
    
    for (const filePath of allMarkdownFiles) {
      try {
        let content = fs.readFileSync(filePath, 'utf8');
        let modified = false;
        
        for (const fix of linkFixes) {
          if (content.includes(fix.from)) {
            content = content.replace(new RegExp(fix.from.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), fix.to);
            modified = true;
          }
        }
        
        // Fix malformed links with brackets in URLs
        const malformedLinkRegex = /\[([^\]]*)\]\(([^)]*\[[^\]]*\][^)]*)\)/g;
        content = content.replace(malformedLinkRegex, (match, text, url) => {
          // If the URL contains brackets, it's likely malformed
          if (url.includes('[') && url.includes(']')) {
            return `\`${text}\``;  // Convert to code instead
          }
          return match;
        });
        
        if (modified) {
          fs.writeFileSync(filePath, content);
          console.log(`🔧 Fixed links in: ${path.relative(this.docsDir, filePath)}`);
          this.fixes.linksUpdated++;
        }
      } catch (error) {
        console.error(`❌ Error fixing links in ${filePath}:`, error.message);
      }
    }
  }

  // Remove orphaned diagram description files (keep the PNGs)
  removeOrphanedDiagramFiles() {
    console.log('🗑️ Removing orphaned diagram description files...');
    
    const diagramDescFiles = [
      'docs/images/diagrams/compliance-controls.png.md',
      'docs/images/diagrams/data-classification-framework.png.md',
      'docs/images/diagrams/data-governance-decision-tree.png.md',
      'docs/images/diagrams/data-pipeline-implementation.png.md',
      'docs/images/diagrams/data-protection-model.png.md',
      'docs/images/diagrams/data-quality-framework.png.md',
      'docs/images/diagrams/defense-in-depth-security.png.md',
      'docs/images/diagrams/delta-lake-optimization.png.md',
      'docs/images/diagrams/delta-lake-write-flow.png.md',
      'docs/images/diagrams/end-to-end-governance.png.md',
      'docs/images/diagrams/enterprise-scale-architecture.png.md',
      'docs/images/diagrams/governance-maturity-model.png.md',
      'docs/images/diagrams/governance-roles.png.md',
      'docs/images/diagrams/identity-access-architecture.png.md',
      'docs/images/diagrams/incident-response-process.png.md',
      'docs/images/diagrams/integrated-data-governance.png.md',
      'docs/images/diagrams/multi-region-architecture.png.md',
      'docs/images/diagrams/network-isolation-architecture.png.md',
      'docs/images/diagrams/performance-optimization.png.md',
      'docs/images/diagrams/purview-integration.png.md',
      'docs/images/diagrams/sensitive-data-protection.png.md',
      'docs/images/diagrams/serverless-sql-query-flow.png.md',
      'docs/images/diagrams/serverless-sql-troubleshooting.png.md'
    ];
    
    for (const file of diagramDescFiles) {
      const fullPath = path.join(__dirname, file);
      if (fs.existsSync(fullPath)) {
        fs.unlinkSync(fullPath);
        console.log(`🗑️ Removed: ${file}`);
        this.fixes.filesRemoved++;
      }
    }
  }

  // Update navigation in parent files to include orphaned content
  updateNavigation() {
    console.log('🧭 Updating navigation to include orphaned files...');
    
    // Update main README.md to include missing sections
    const mainReadmePath = path.join(this.docsDir, 'README.md');
    if (fs.existsSync(mainReadmePath)) {
      let content = fs.readFileSync(mainReadmePath, 'utf8');
      
      // Add links to orphaned files if they don't exist
      const orphanedSections = [
        '- [Serverless SQL Overview](serverless-sql.md)',
        '- [Shared Metadata Overview](shared-metadata.md)',
        '- [Troubleshooting Overview](troubleshooting.md)',
        '- [Interactive Data Pipeline Tutorial](tutorials/interactive-data-pipeline.md)',
        '- [Performance Benchmarks](performance/benchmarks-guide.md)',
        '- [Security Best Practices](security/best-practices.md)'
      ];
      
      // Find the appropriate section to add these links
      if (!content.includes('serverless-sql.md')) {
        // Add a new section for additional resources
        const additionalSection = `

## Additional Resources

${orphanedSections.join('\n')}
`;
        content += additionalSection;
        fs.writeFileSync(mainReadmePath, content);
        console.log('📝 Updated main README.md with additional resources');
        this.fixes.navigationUpdated++;
      }
    }
    
    // Update diagrams README to include diagram files
    const diagramsReadmePath = path.join(this.docsDir, 'diagrams', 'README.md');
    if (fs.existsSync(diagramsReadmePath)) {
      let content = fs.readFileSync(diagramsReadmePath, 'utf8');
      
      const diagramSections = [
        '- [Data Governance Diagrams](data-governance-diagrams.md)',
        '- [Security Diagrams](security-diagrams.md)',
        '- [Process Flowcharts](process-flowcharts.md)'
      ];
      
      if (!content.includes('data-governance-diagrams.md')) {
        content += `

## Diagram Collections

${diagramSections.join('\n')}
`;
        fs.writeFileSync(diagramsReadmePath, content);
        console.log('📝 Updated diagrams README.md');
        this.fixes.navigationUpdated++;
      }
    }
    
    // Update architecture README to include delta lakehouse overview
    const archReadmePath = path.join(this.docsDir, 'architecture', 'README.md');
    if (fs.existsSync(archReadmePath)) {
      let content = fs.readFileSync(archReadmePath, 'utf8');
      
      if (!content.includes('delta-lakehouse-overview.md')) {
        content = content.replace(
          '## Architecture Guides',
          `## Architecture Guides

- [Delta Lakehouse Overview](delta-lakehouse-overview.md)
- [Delta Lakehouse Detailed Architecture](delta-lakehouse/detailed-architecture.md)`
        );
        fs.writeFileSync(archReadmePath, content);
        console.log('📝 Updated architecture README.md');
        this.fixes.navigationUpdated++;
      }
    }
  }

  // Find all markdown files
  findAllMarkdownFiles(dir = this.docsDir) {
    const files = [];
    const items = fs.readdirSync(dir);
    
    for (const item of items) {
      const itemPath = path.join(dir, item);
      const stat = fs.statSync(itemPath);
      
      if (stat.isDirectory()) {
        if (item !== 'node_modules' && item !== '.git' && item !== '.github') {
          files.push(...this.findAllMarkdownFiles(itemPath));
        }
      } else if (item.endsWith('.md')) {
        files.push(itemPath);
      }
    }
    
    return files;
  }

  // Run all fixes
  async runAllFixes() {
    console.log('🚀 Starting comprehensive documentation fixes...\n');
    
    this.createMissingFiles();
    this.fixBrokenLinks();
    this.removeOrphanedDiagramFiles();
    this.updateNavigation();
    
    console.log('\n📊 FIX SUMMARY:');
    console.log(`Files created: ${this.fixes.filesCreated}`);
    console.log(`Files removed: ${this.fixes.filesRemoved}`);
    console.log(`Links updated: ${this.fixes.linksUpdated}`);
    console.log(`Navigation sections updated: ${this.fixes.navigationUpdated}`);
    
    console.log('\n✨ All fixes completed!');
    return this.fixes;
  }
}

// Run the fixes
const docsDir = path.join(__dirname, 'docs');
const fixer = new DocumentationFixer(docsDir);

fixer.runAllFixes().then(fixes => {
  console.log('\n🎯 RECOMMENDED NEXT STEPS:');
  console.log('1. Run the audit again to verify fixes');
  console.log('2. Review created content files and customize as needed');
  console.log('3. Test all navigation links');
  console.log('4. Update any remaining broken external links');
}).catch(error => {
  console.error('❌ Fix process failed:', error);
});
