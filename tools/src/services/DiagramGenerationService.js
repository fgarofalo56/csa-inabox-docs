/**
 * Service layer for diagram generation
 * Orchestrates Mermaid to PNG conversion and diagram management
 */
import { DiagramMapping } from '../domain/models/DiagramMapping.js';
import { MermaidRenderer } from '../infrastructure/MermaidRenderer.js';
import { FileSystemRepository } from '../infrastructure/FileSystemRepository.js';

export class DiagramGenerationService {
  constructor(fileRepository = null, mermaidRenderer = null, logger = null) {
    this.fileRepository = fileRepository || new FileSystemRepository();
    this.mermaidRenderer = mermaidRenderer || new MermaidRenderer();
    this.logger = logger;
    this.diagramMapping = new DiagramMapping();
    this.hardcodedDiagrams = this.loadHardcodedDiagrams();
  }

  /**
   * Generate all diagrams from placeholder files
   * @param {string} placeholdersDir - Directory containing .png.md placeholder files
   * @param {string} outputDir - Directory to save PNG files
   * @param {object} options - Generation options
   * @returns {Promise<object>} - Generation results
   */
  async generateAllDiagrams(placeholdersDir, outputDir = null, options = {}) {
    this.logger?.section('Diagram Generation');

    const output = outputDir || placeholdersDir;
    
    try {
      await this.mermaidRenderer.initialize();
      
      // Find placeholder files
      const placeholderFiles = await this.findPlaceholderFiles(placeholdersDir);
      this.logger?.info(`Found ${placeholderFiles.length} placeholder files to process`);

      if (placeholderFiles.length === 0) {
        this.logger?.warn('No placeholder files found');
        return { successful: [], failed: [], total: 0 };
      }

      // Create progress tracker
      const progressBar = this.logger?.createProgressBar('Generating diagrams');
      progressBar?.start(placeholderFiles.length);

      const results = { successful: [], failed: [], total: placeholderFiles.length };

      // Process each placeholder file
      for (let i = 0; i < placeholderFiles.length; i++) {
        const file = placeholderFiles[i];
        progressBar?.update(i + 1, `Processing ${file.filename}`);

        try {
          const success = await this.generateDiagramFromPlaceholder(file, output, options);
          
          if (success) {
            results.successful.push(file);
          } else {
            results.failed.push(file);
          }
        } catch (error) {
          this.logger?.error(`Failed to process ${file.filePath}: ${error.message}`);
          results.failed.push(file);
        }
      }

      progressBar?.finish(`${results.successful.length}/${results.total} diagrams generated successfully`);
      
      // Cleanup
      await this.mermaidRenderer.cleanup();
      
      return results;
    } catch (error) {
      this.logger?.error(`Diagram generation failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Generate diagram from a single placeholder file
   * @param {DocumentationFile} placeholderFile - Placeholder file
   * @param {string} outputDir - Output directory
   * @param {object} options - Generation options
   * @returns {Promise<boolean>} - True if successful
   */
  async generateDiagramFromPlaceholder(placeholderFile, outputDir, options = {}) {
    // Extract Mermaid code from placeholder
    const mermaidCode = this.extractMermaidFromPlaceholder(placeholderFile);
    
    if (!mermaidCode) {
      this.logger?.warn(`No Mermaid code found in ${placeholderFile.filename}`);
      return false;
    }

    // Generate output path
    const outputPath = this.generateOutputPath(placeholderFile, outputDir);
    
    // Generate PNG
    return await this.mermaidRenderer.generatePNG(mermaidCode, outputPath, options);
  }

  /**
   * Extract Mermaid code from placeholder file
   * @param {DocumentationFile} placeholderFile - Placeholder file
   * @returns {string|null} - Mermaid code or null
   */
  extractMermaidFromPlaceholder(placeholderFile) {
    // Try to extract from file content first
    if (placeholderFile.mermaidBlocks.length > 0) {
      return placeholderFile.mermaidBlocks[0].content;
    }

    // Fall back to hardcoded diagrams
    const baseFileName = placeholderFile.filename.replace('.png', '');
    
    if (this.hardcodedDiagrams[baseFileName]) {
      this.logger?.info(`Using hardcoded diagram for: ${baseFileName}`);
      return this.hardcodedDiagrams[baseFileName];
    }

    return null;
  }

  /**
   * Generate output path for PNG file
   * @param {DocumentationFile} placeholderFile - Placeholder file
   * @param {string} outputDir - Output directory
   * @returns {string} - Output file path
   */
  generateOutputPath(placeholderFile, outputDir) {
    const path = require('path');
    const outputFileName = placeholderFile.filename; // This already includes .png
    return path.join(outputDir, outputFileName);
  }

  /**
   * Find placeholder files (.png.md files)
   * @param {string} dir - Directory to search
   * @returns {Promise<DocumentationFile[]>} - Array of placeholder files
   */
  async findPlaceholderFiles(dir) {
    const allFiles = await this.fileRepository.findAllMarkdownFiles(dir);
    return allFiles.filter(file => file.isDiagramPlaceholder());
  }

  /**
   * Replace Mermaid blocks with PNG references in markdown files
   * @param {string} docsDir - Documentation directory
   * @param {object} options - Replacement options
   * @returns {Promise<object>} - Replacement results
   */
  async replaceMermaidWithPNG(docsDir, options = {}) {
    this.logger?.section('Replacing Mermaid with PNG');

    const results = {
      filesProcessed: 0,
      replacements: 0,
      formattingFixes: 0
    };

    try {
      const markdownFiles = await this.fileRepository.findAllMarkdownFiles(docsDir);
      this.logger?.info(`Found ${markdownFiles.length} markdown files to process`);

      for (const file of markdownFiles) {
        const replacementResult = await this.replaceMermaidInFile(file, options);
        
        if (replacementResult.modified) {
          await this.fileRepository.writeFile(file.filePath, replacementResult.content);
          results.filesProcessed++;
          results.replacements += replacementResult.replacements;
          
          if (replacementResult.replacements > 0) {
            this.logger?.success(`Updated ${file.relativePath}: ${replacementResult.replacements} diagrams replaced`);
          }
        }
      }

      this.logger?.summary(results);
      return results;
    } catch (error) {
      this.logger?.error(`Mermaid replacement failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Replace Mermaid blocks in a single file
   * @param {DocumentationFile} file - File to process
   * @param {object} options - Replacement options
   * @returns {object} - Replacement result
   */
  replaceMermaidInFile(file, options = {}) {
    let content = file.content || '';
    let replacements = 0;
    let modified = false;

    // Fix formatting issues first
    const originalContent = content;
    content = this.fixFormattingIssues(content);
    
    if (content !== originalContent) {
      modified = true;
    }

    // Regular expression to match mermaid code blocks with optional indentation
    const mermaidRegex = /(\s*)(```mermaid\n[\s\S]*?\n```)/g;

    content = content.replace(mermaidRegex, (match, indentation, mermaidBlock) => {
      const context = this.getContextAroundMermaid(file.content, match);
      const diagramName = this.diagramMapping.identifyDiagram(
        mermaidBlock + ' ' + context, 
        file.filePath, 
        context
      );

      if (diagramName && this.diagramMapping.isAvailable(diagramName)) {
        const imagePath = this.diagramMapping.getRelativeImagePath(
          file.filePath,
          diagramName,
          this.fileRepository.rootDir
        );
        const altText = this.diagramMapping.getDiagramTitle(diagramName);

        replacements++;
        modified = true;
        // Preserve indentation and add proper spacing
        return `${indentation}![${altText}](${imagePath})\n`;
      }

      // If we can't identify the diagram, leave the mermaid block as is
      if (options.verbose) {
        this.logger?.warn(`Could not identify diagram for mermaid block in: ${file.relativePath}`);
      }
      
      return match;
    });

    return {
      content,
      replacements,
      modified
    };
  }

  /**
   * Fix formatting issues from previous runs
   * @param {string} content - Content to fix
   * @returns {string} - Fixed content
   */
  fixFormattingIssues(content) {
    // Fix cases where text got concatenated with image markdown
    content = content.replace(/(\!\[.*?\]\(.*?\))([a-zA-Z])/g, '$1\n\n$2');

    // Ensure proper spacing around images
    content = content.replace(/(\!\[.*?\]\(.*?\))\n(?!\n)/g, '$1\n\n');

    return content;
  }

  /**
   * Get context around mermaid blocks for better identification
   * @param {string} content - Full file content
   * @param {string} mermaidMatch - Matched mermaid block
   * @returns {string} - Context around the mermaid block
   */
  getContextAroundMermaid(content, mermaidMatch) {
    const beforeIndex = content.indexOf(mermaidMatch);
    const contextStart = Math.max(0, beforeIndex - 500);
    const contextEnd = Math.min(content.length, beforeIndex + mermaidMatch.length + 500);
    return content.substring(contextStart, contextEnd);
  }

  /**
   * Validate all Mermaid diagrams in documentation
   * @param {string} docsDir - Documentation directory
   * @returns {Promise<object>} - Validation results
   */
  async validateMermaidDiagrams(docsDir) {
    this.logger?.section('Validating Mermaid Diagrams');

    const results = {
      valid: [],
      invalid: [],
      total: 0
    };

    try {
      const markdownFiles = await this.fileRepository.findAllMarkdownFiles(docsDir);
      
      for (const file of markdownFiles) {
        for (const mermaidBlock of file.mermaidBlocks) {
          results.total++;
          
          const isValid = await this.mermaidRenderer.validateMermaidSyntax(mermaidBlock.content);
          
          if (isValid) {
            results.valid.push({
              file: file.relativePath,
              line: mermaidBlock.line
            });
          } else {
            results.invalid.push({
              file: file.relativePath,
              line: mermaidBlock.line,
              content: mermaidBlock.content.substring(0, 100) + '...'
            });
            
            this.logger?.warn(`Invalid Mermaid syntax in ${file.relativePath}:${mermaidBlock.line}`);
          }
        }
      }

      this.logger?.summary({
        totalDiagrams: results.total,
        validDiagrams: results.valid.length,
        invalidDiagrams: results.invalid.length
      });

      return results;
    } catch (error) {
      this.logger?.error(`Mermaid validation failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Load hardcoded diagram definitions for fallback
   * @returns {object} - Hardcoded diagram definitions
   */
  loadHardcodedDiagrams() {
    return {
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
        PURVIEW --"Automated Scanning"--> PIPELINE`,

      "governance-maturity-model": `graph TD
        L1[Level 1:<br>Initial]
        L2[Level 2:<br>Repeatable]
        L3[Level 3:<br>Defined]
        L4[Level 4:<br>Managed]
        L5[Level 5:<br>Optimized]
        
        L1 --> L2
        L2 --> L3
        L3 --> L4
        L4 --> L5`,

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
        
        GDPR --> PP
        HIPAA --> DP
        PCI --> DP
        SOX --> AM`
    };
  }
}