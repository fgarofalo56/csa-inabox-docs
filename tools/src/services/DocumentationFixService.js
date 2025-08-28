/**
 * Service layer for fixing documentation issues
 * Orchestrates automated fixes for common documentation problems
 */
import { FileSystemRepository } from '../infrastructure/FileSystemRepository.js';
import path from 'path';

export class DocumentationFixService {
  constructor(fileRepository = null, logger = null) {
    this.fileRepository = fileRepository || new FileSystemRepository();
    this.logger = logger;
    this.fixResults = {
      filesCreated: 0,
      filesRemoved: 0,
      linksUpdated: 0,
      navigationUpdated: 0,
      contentGenerated: 0
    };
  }

  /**
   * Run all automated fixes
   * @param {string} docsDir - Documentation directory
   * @param {object} options - Fix options
   * @returns {Promise<object>} - Fix results
   */
  async runAllFixes(docsDir, options = {}) {
    this.logger?.section('Documentation Fixes');

    try {
      await this.createMissingFiles(docsDir, options);
      await this.fixBrokenLinks(docsDir, options);
      await this.removeOrphanedDiagramFiles(docsDir, options);
      await this.updateNavigation(docsDir, options);

      this.logger?.summary(this.fixResults);
      this.logger?.success('All fixes completed successfully');

      return this.fixResults;
    } catch (error) {
      this.logger?.error(`Fix process failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Create missing files that are referenced by other files
   * @param {string} docsDir - Documentation directory
   * @param {object} options - Fix options
   */
  async createMissingFiles(docsDir, options = {}) {
    this.logger?.subsection('Creating missing referenced files');

    const missingFiles = this.getMissingFileDefinitions();

    for (const fileInfo of missingFiles) {
      const fullPath = path.join(this.fileRepository.rootDir, fileInfo.path);
      
      // Ensure directory exists
      await this.fileRepository.ensureDirectory(path.dirname(fullPath));

      if (!(await this.fileRepository.fileExists(fullPath))) {
        if (fileInfo.type === 'content') {
          const content = this.generateContentFile(fileInfo);
          await this.fileRepository.writeFile(fullPath, content);
          this.logger?.success(`Created content file: ${fileInfo.path}`);
          this.fixResults.filesCreated++;
          this.fixResults.contentGenerated++;
        } else if (fileInfo.type === 'placeholder') {
          const content = this.generatePlaceholderFile(fileInfo);
          const placeholderPath = fullPath.replace('.png', '.md');
          await this.fileRepository.writeFile(placeholderPath, content);
          this.logger?.success(`Created placeholder file: ${fileInfo.path}.md`);
          this.fixResults.filesCreated++;
        }
      }
    }
  }

  /**
   * Get definitions for missing files to create
   * @returns {object[]} - Array of file definitions
   */
  getMissingFileDefinitions() {
    return [
      // Best practices files
      { path: 'docs/best-practices/pipeline-optimization.md', type: 'content', category: 'best-practices' },
      { path: 'docs/best-practices/serverless-sql-best-practices.md', type: 'content', category: 'best-practices' },
      { path: 'docs/best-practices/sql-performance.md', type: 'content', category: 'best-practices' },
      { path: 'docs/best-practices/spark-performance.md', type: 'content', category: 'best-practices' },
      
      // Monitoring files
      { path: 'docs/monitoring/sql-monitoring.md', type: 'content', category: 'monitoring' },
      { path: 'docs/monitoring/spark-monitoring.md', type: 'content', category: 'monitoring' },
      
      // Reference files
      { path: 'docs/reference/spark-configuration.md', type: 'content', category: 'reference' },
      
      // Image placeholders
      { path: 'docs/images/troubleshooting-process.png', type: 'placeholder' },
      { path: 'docs/images/architecture/serverless-sql-architecture.png', type: 'placeholder' },
      { path: 'docs/images/architecture/shared-metadata-architecture.png', type: 'placeholder' }
    ];
  }

  /**
   * Generate content for a documentation file
   * @param {object} fileInfo - File information
   * @returns {string} - Generated content
   */
  generateContentFile(fileInfo) {
    const fileName = path.basename(fileInfo.path, '.md');
    const title = fileName.split('-').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');

    const category = fileInfo.category || 'documentation';
    const breadcrumb = this.generateBreadcrumb(fileInfo.path);

    return `# ${title}

${breadcrumb}

## Overview

This document provides comprehensive guidance on ${title.toLowerCase()} for Azure Synapse Analytics and Cloud Scale Analytics solutions.

## Key Concepts

### Important Points

- **Concept 1**: Key principle or approach for ${title.toLowerCase()}
- **Concept 2**: Important consideration for implementation
- **Concept 3**: Best practice or recommendation

### Architecture Considerations

When implementing ${title.toLowerCase()}, consider the following architectural aspects:

1. **Scalability**: Ensure the solution can scale with your data volume
2. **Performance**: Optimize for query performance and resource utilization
3. **Security**: Implement appropriate security controls and access management
4. **Cost**: Balance performance requirements with cost optimization

## Implementation Guide

### Prerequisites

Before implementing ${title.toLowerCase()}, ensure you have:

- [ ] Azure Synapse Analytics workspace configured
- [ ] Appropriate permissions and access controls
- [ ] Required Azure services provisioned
- [ ] Development and testing environments set up

### Step-by-Step Implementation

#### Step 1: Initial Setup and Configuration

1. **Configure the environment**
   \`\`\`bash
   # Example configuration commands
   az synapse workspace create --name myworkspace --resource-group mygroup
   \`\`\`

2. **Set up required permissions**
   - Assign appropriate RBAC roles
   - Configure service principal access
   - Set up managed identities

#### Step 2: Implementation Details

1. **Core implementation**
   - Configure the main components
   - Set up data connections
   - Implement processing logic

2. **Testing and validation**
   - Run unit tests
   - Perform integration testing
   - Validate performance metrics

#### Step 3: Deployment and Monitoring

1. **Deploy to production**
   - Use CI/CD pipelines
   - Implement blue-green deployment
   - Monitor deployment status

2. **Set up monitoring and alerting**
   - Configure Azure Monitor
   - Set up performance alerts
   - Implement logging and diagnostics

## Best Practices

### Performance Optimization

| Practice | Description | Impact |
|----------|-------------|--------|
| **Optimize queries** | Use appropriate indexing and partitioning | High |
| **Resource sizing** | Right-size compute resources | Medium |
| **Caching strategies** | Implement effective caching | High |

### Security Best Practices

- **Access Control**: Implement least privilege access
- **Data Encryption**: Use encryption at rest and in transit
- **Network Security**: Configure private endpoints and firewalls
- **Auditing**: Enable comprehensive audit logging

### Cost Optimization

- **Resource Management**: Use pause/resume capabilities
- **Auto-scaling**: Implement dynamic scaling based on workload
- **Reserved Capacity**: Use reserved instances for predictable workloads

## Common Issues and Solutions

### Troubleshooting Guide

#### Issue: Performance degradation

**Symptoms:**
- Slow query execution
- High resource utilization
- Timeout errors

**Solutions:**
1. Check query execution plans
2. Review resource allocation
3. Optimize data distribution
4. Update statistics

#### Issue: Connection failures

**Symptoms:**
- Authentication errors
- Network connectivity issues
- Permission denied errors

**Solutions:**
1. Verify credentials and permissions
2. Check firewall and network configuration
3. Validate service endpoints
4. Review security group settings

## Monitoring and Observability

### Key Metrics to Monitor

- **Performance Metrics**: Query execution time, throughput
- **Resource Metrics**: CPU, memory, storage utilization
- **Error Metrics**: Failed queries, connection errors
- **Cost Metrics**: Compute usage, storage costs

### Monitoring Tools

- **Azure Monitor**: Comprehensive monitoring and alerting
- **Log Analytics**: Centralized log collection and analysis
- **Application Insights**: Application performance monitoring
- **Custom Dashboards**: Business-specific monitoring views

## Related Resources

- [Azure Synapse Analytics Documentation](https://docs.microsoft.com/azure/synapse-analytics/)
- [Best Practices Overview](../best-practices/README.md)
- [Architecture Patterns](../architecture/README.md)
- [Troubleshooting Guide](../troubleshooting/README.md)

## Next Steps

1. **Review implementation guidelines** and ensure alignment with your requirements
2. **Set up development environment** for testing and validation
3. **Implement in stages** starting with a proof of concept
4. **Monitor and optimize** based on performance metrics and feedback
5. **Document customizations** and share knowledge with your team

---

*This document is automatically generated and should be customized based on your specific requirements and implementation details.*
`;
  }

  /**
   * Generate breadcrumb navigation
   * @param {string} filePath - File path
   * @returns {string} - Breadcrumb HTML
   */
  generateBreadcrumb(filePath) {
    const parts = filePath.split('/').filter(part => part !== 'docs' && part !== '');
    const breadcrumbs = ['[Home](/README.md)', '[Documentation](../README.md)'];
    
    let currentPath = '';
    for (let i = 0; i < parts.length - 1; i++) {
      currentPath += '../';
      const part = parts[i];
      const title = part.split('-').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
      ).join(' ');
      breadcrumbs.push(`[${title}](${currentPath}${part}/README.md)`);
    }

    return breadcrumbs.join(' > ');
  }

  /**
   * Generate placeholder file content
   * @param {object} fileInfo - File information
   * @returns {string} - Placeholder content
   */
  generatePlaceholderFile(fileInfo) {
    const fileName = path.basename(fileInfo.path);
    
    return `# Placeholder Image

This is a placeholder for the image: ${fileName}

## Instructions

To replace this placeholder:

1. Create the actual image file (${fileName})
2. Remove this markdown file
3. Update any references to point to the image file directly

## Image Requirements

- **Format**: PNG (preferred) or SVG
- **Resolution**: Minimum 800x600, recommended 1200x800
- **File size**: Keep under 500KB for optimal loading
- **Alt text**: Ensure all references include descriptive alt text

## Related Documentation

- [Visual Style Guide](../../VISUAL-STYLE-GUIDE.md)
- [Image Guidelines](../README.md)
- [Architecture Diagrams](../diagrams/README.md)
`;
  }

  /**
   * Fix broken links by updating paths
   * @param {string} docsDir - Documentation directory
   * @param {object} options - Fix options
   */
  async fixBrokenLinks(docsDir, options = {}) {
    this.logger?.subsection('Fixing broken links');

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

    const markdownFiles = await this.fileRepository.findAllMarkdownFiles(docsDir);

    for (const file of markdownFiles) {
      let content = file.content;
      let modified = false;

      for (const fix of linkFixes) {
        if (content.includes(fix.from)) {
          const regex = new RegExp(fix.from.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
          content = content.replace(regex, fix.to);
          modified = true;
        }
      }

      // Fix malformed links with brackets in URLs
      const malformedLinkRegex = /\[([^\]]*)\]\(([^)]*\[[^\]]*\][^)]*)\)/g;
      const originalContent = content;
      content = content.replace(malformedLinkRegex, (match, text, url) => {
        if (url.includes('[') && url.includes(']')) {
          return `\`${text}\``; // Convert to code instead
        }
        return match;
      });

      if (content !== originalContent) {
        modified = true;
      }

      if (modified) {
        await this.fileRepository.writeFile(file.filePath, content);
        this.logger?.success(`Fixed links in: ${file.relativePath}`);
        this.fixResults.linksUpdated++;
      }
    }
  }

  /**
   * Remove orphaned diagram description files
   * @param {string} docsDir - Documentation directory
   * @param {object} options - Fix options
   */
  async removeOrphanedDiagramFiles(docsDir, options = {}) {
    if (options.preserveDiagramFiles) {
      this.logger?.info('Skipping removal of diagram files (preserveDiagramFiles option set)');
      return;
    }

    this.logger?.subsection('Removing orphaned diagram description files');

    const diagramsDir = path.join(docsDir, 'images', 'diagrams');
    const diagramMapping = ['compliance-controls', 'data-classification-framework', 'data-governance-decision-tree'];

    try {
      const files = await this.fileRepository.listDirectory(diagramsDir);
      
      for (const file of files) {
        if (file.endsWith('.png.md')) {
          const filePath = path.join(diagramsDir, file);
          
          // Check if corresponding PNG exists
          const pngPath = filePath.replace('.md', '');
          
          if (await this.fileRepository.fileExists(pngPath)) {
            await this.fileRepository.deleteFile(filePath);
            this.logger?.success(`Removed orphaned diagram file: ${file}`);
            this.fixResults.filesRemoved++;
          }
        }
      }
    } catch (error) {
      this.logger?.warn(`Could not process diagrams directory: ${error.message}`);
    }
  }

  /**
   * Update navigation in parent files
   * @param {string} docsDir - Documentation directory
   * @param {object} options - Fix options
   */
  async updateNavigation(docsDir, options = {}) {
    this.logger?.subsection('Updating navigation structure');

    // Update main README.md
    await this.updateMainReadme(docsDir);
    
    // Update section README files
    await this.updateSectionReadmes(docsDir);
  }

  /**
   * Update main README.md with missing sections
   * @param {string} docsDir - Documentation directory
   */
  async updateMainReadme(docsDir) {
    const mainReadmePath = path.join(docsDir, 'README.md');
    
    if (await this.fileRepository.fileExists(mainReadmePath)) {
      let content = await this.fileRepository.readFile(mainReadmePath);

      const additionalSections = [
        '- [Serverless SQL Overview](serverless-sql.md)',
        '- [Shared Metadata Overview](shared-metadata.md)', 
        '- [Troubleshooting Overview](troubleshooting.md)',
        '- [Performance Benchmarks](performance/benchmarks-guide.md)',
        '- [Security Best Practices](security/best-practices.md)'
      ];

      // Check if we need to add additional resources section
      if (!content.includes('serverless-sql.md')) {
        const additionalSection = `

## Additional Resources

${additionalSections.join('\n')}
`;
        content += additionalSection;
        await this.fileRepository.writeFile(mainReadmePath, content);
        this.logger?.success('Updated main README.md with additional resources');
        this.fixResults.navigationUpdated++;
      }
    }
  }

  /**
   * Update section README files
   * @param {string} docsDir - Documentation directory
   */
  async updateSectionReadmes(docsDir) {
    const sections = [
      {
        path: path.join(docsDir, 'diagrams', 'README.md'),
        additions: [
          '- [Data Governance Diagrams](data-governance-diagrams.md)',
          '- [Security Diagrams](security-diagrams.md)',
          '- [Process Flowcharts](process-flowcharts.md)'
        ],
        checkFor: 'data-governance-diagrams.md',
        sectionTitle: 'Diagram Collections'
      },
      {
        path: path.join(docsDir, 'architecture', 'README.md'),
        additions: [
          '- [Delta Lakehouse Overview](delta-lakehouse-overview.md)',
          '- [Delta Lakehouse Detailed Architecture](delta-lakehouse/detailed-architecture.md)'
        ],
        checkFor: 'delta-lakehouse-overview.md',
        sectionTitle: 'Architecture Guides'
      }
    ];

    for (const section of sections) {
      if (await this.fileRepository.fileExists(section.path)) {
        let content = await this.fileRepository.readFile(section.path);

        if (!content.includes(section.checkFor)) {
          const newSection = `

## ${section.sectionTitle}

${section.additions.join('\n')}
`;
          content += newSection;
          await this.fileRepository.writeFile(section.path, content);
          this.logger?.success(`Updated ${path.relative(docsDir, section.path)}`);
          this.fixResults.navigationUpdated++;
        }
      }
    }
  }

  /**
   * Create missing README files for directories
   * @param {string} docsDir - Documentation directory
   * @param {object} options - Fix options
   */
  async createMissingReadmeFiles(docsDir, options = {}) {
    this.logger?.subsection('Creating missing README files');

    const markdownFiles = await this.fileRepository.findAllMarkdownFiles(docsDir);
    const directories = new Set();

    // Get all directories that contain markdown files
    markdownFiles.forEach(file => {
      directories.add(file.directory);
    });

    for (const dir of directories) {
      const readmePath = path.join(dir, 'README.md');
      const indexPath = path.join(dir, 'index.md');

      // Skip if README.md or index.md already exists
      if (await this.fileRepository.fileExists(readmePath) || 
          await this.fileRepository.fileExists(indexPath)) {
        continue;
      }

      // Create README.md
      const dirName = path.basename(dir);
      const title = dirName.split('-').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
      ).join(' ');

      const content = this.generateDirectoryReadme(title, dir, docsDir);
      
      await this.fileRepository.writeFile(readmePath, content);
      this.logger?.success(`Created README.md for ${path.relative(docsDir, dir)}`);
      this.fixResults.filesCreated++;
    }
  }

  /**
   * Generate README content for a directory
   * @param {string} title - Directory title
   * @param {string} dirPath - Directory path
   * @param {string} docsDir - Documentation root directory
   * @returns {string} - Generated README content
   */
  generateDirectoryReadme(title, dirPath, docsDir) {
    const relativePath = path.relative(docsDir, dirPath);
    const breadcrumb = this.generateBreadcrumb(path.join(relativePath, 'README.md'));

    return `# ${title}

${breadcrumb}

## Overview

This section contains documentation related to ${title.toLowerCase()}.

## Contents

<!-- This section will be automatically populated -->

## Getting Started

To get started with ${title.toLowerCase()}, review the documentation in this section and follow the implementation guides.

## Related Resources

- [Main Documentation](../README.md)
- [Architecture Overview](../architecture/README.md)
- [Best Practices](../best-practices/README.md)

---

*This file was automatically generated. Please customize it based on the specific content in this directory.*
`;
  }
}