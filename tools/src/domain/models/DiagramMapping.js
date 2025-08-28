/**
 * Domain model for diagram mapping and identification
 * Contains business rules for mapping Mermaid content to PNG diagrams
 */
export class DiagramMapping {
  constructor() {
    this.availableDiagrams = [
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

    this.diagramTitles = {
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

    this.contentPatterns = {
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
  }

  /**
   * Identify diagram name from content and file path
   * @param {string} content - Mermaid content or surrounding context
   * @param {string} filePath - File path for filename-based matching
   * @param {string} context - Additional context around the mermaid block
   * @returns {string|null} - Diagram name or null if not identified
   */
  identifyDiagram(content, filePath, context = '') {
    const path = require('path');
    const fileName = path.basename(filePath, '.md');
    const fullContent = (content + ' ' + filePath + ' ' + context).toLowerCase();

    // Direct filename matches
    for (const diagram of this.availableDiagrams) {
      if (fileName.includes(diagram) || filePath.includes(diagram)) {
        return diagram;
      }
    }

    // Content-based identification
    for (const [diagram, keywords] of Object.entries(this.contentPatterns)) {
      if (keywords.some(keyword => fullContent.includes(keyword))) {
        return diagram;
      }
    }

    // Fallback pattern matching
    if (fullContent.includes('roles') && fullContent.includes('responsibilities')) return 'governance-roles';
    if (fullContent.includes('enterprise') && fullContent.includes('architecture')) return 'enterprise-scale-architecture';
    if (fullContent.includes('security') && fullContent.includes('defense')) return 'defense-in-depth-security';
    if (fullContent.includes('incident') && fullContent.includes('process')) return 'incident-response-process';
    if (fullContent.includes('optimization') && fullContent.includes('performance')) return 'performance-optimization';

    return null;
  }

  /**
   * Get diagram title for alt text
   * @param {string} diagramName - The diagram identifier
   * @returns {string} - Human-readable title
   */
  getDiagramTitle(diagramName) {
    return this.diagramTitles[diagramName] || 
           diagramName.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  }

  /**
   * Check if diagram is available
   * @param {string} diagramName - The diagram identifier
   * @returns {boolean} - True if diagram is available
   */
  isAvailable(diagramName) {
    return this.availableDiagrams.includes(diagramName);
  }

  /**
   * Get all available diagrams
   * @returns {string[]} - Array of available diagram names
   */
  getAvailableDiagrams() {
    return [...this.availableDiagrams];
  }

  /**
   * Get relative path from current file to images directory
   * @param {string} currentFilePath - Current file path
   * @param {string} imageName - Image name (without extension)
   * @param {string} baseDir - Base directory for relative path calculation
   * @returns {string} - Relative path to image
   */
  getRelativeImagePath(currentFilePath, imageName, baseDir) {
    const path = require('path');
    const currentDir = path.dirname(currentFilePath);
    const imagesDir = path.join(baseDir, 'docs', 'images', 'diagrams');
    const relativePath = path.relative(currentDir, imagesDir);
    return path.join(relativePath, `${imageName}.png`).replace(/\\/g, '/');
  }
}