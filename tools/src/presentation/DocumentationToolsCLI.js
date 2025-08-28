/**
 * Presentation layer for documentation tools CLI
 * Handles user interface and command orchestration
 */
import { DocumentationAuditService } from '../services/DocumentationAuditService.js';
import { DiagramGenerationService } from '../services/DiagramGenerationService.js';
import { DocumentationFixService } from '../services/DocumentationFixService.js';
import { FileSystemRepository } from '../infrastructure/FileSystemRepository.js';
import { MermaidRenderer } from '../infrastructure/MermaidRenderer.js';
import { Logger } from '../infrastructure/Logger.js';
import path from 'path';
import fs from 'fs-extra';
import ora from 'ora';
import { Command } from 'commander';

export class DocumentationToolsCLI {
  constructor(logger = null) {
    this.logger = logger || new Logger();
    this.globalOptions = {};
    this.fileRepository = null;
    this.auditService = null;
    this.diagramService = null;
    this.fixService = null;
    this.program = null;
  }

  /**
   * Run the CLI with command-line arguments
   * @param {Array} argv - Command-line arguments
   */
  async run(argv) {
    this.program = new Command();
    
    this.program
      .name('csa-docs')
      .description('CSA Documentation Tools - Unified documentation management and validation')
      .version('1.0.0')
      .option('--verbose, -v', 'Enable verbose logging')
      .option('--no-color', 'Disable colored output')
      .option('--log-file <file>', 'Log output to file')
      .option('--docs-dir <dir>', 'Documentation directory (default: docs)', 'docs');

    // Add commands
    this.addCommands();

    // Parse global options first
    this.program.hook('preAction', (thisCommand, actionCommand) => {
      const opts = thisCommand.opts();
      this.setGlobalOptions(opts);
    });

    try {
      await this.program.parseAsync(argv);
    } catch (error) {
      this.logger.error(`CLI Error: ${error.message}`);
      process.exit(1);
    }
  }

  /**
   * Add all CLI commands
   */
  addCommands() {
    // Audit command
    this.program
      .command('audit')
      .description('Run comprehensive documentation audit')
      .option('--fix-duplicates', 'Auto-fix duplicate index/README files', true)
      .option('--output <format>', 'Output format: text|json', 'text')
      .option('--save-report <file>', 'Save report to file')
      .action(async (options) => {
        await this.audit(options);
      });

    // Generate diagrams command
    this.program
      .command('generate-diagrams')
      .description('Generate PNG diagrams from Mermaid placeholders')
      .option('--input-dir <dir>', 'Input directory with placeholder files')
      .option('--output-dir <dir>', 'Output directory for PNG files')
      .option('--theme <theme>', 'Mermaid theme: default|dark|forest|neutral', 'default')
      .option('--background <color>', 'Background color', 'transparent')
      .option('--width <pixels>', 'Diagram width', '1920')
      .option('--height <pixels>', 'Diagram height', '1080')
      .action(async (options) => {
        await this.generateDiagrams(options);
      });

    // Replace Mermaid command
    this.program
      .command('replace-mermaid')
      .description('Replace Mermaid blocks with PNG image references')
      .option('--dry-run', 'Preview changes without modifying files')
      .action(async (options) => {
        await this.replaceMermaid(options);
      });

    // Fix issues command
    this.program
      .command('fix-issues')
      .description('Automatically fix common documentation issues')
      .option('--create-missing', 'Create missing referenced files', true)
      .option('--fix-links', 'Fix broken internal links', true)
      .option('--remove-orphans', 'Remove orphaned diagram files', true)
      .option('--update-nav', 'Update navigation structure', true)
      .option('--preserve-diagram-files', 'Preserve .png.md diagram files')
      .action(async (options) => {
        await this.fixIssues(options);
      });

    // Validate links command
    this.program
      .command('validate-links')
      .description('Validate internal and external links')
      .option('--external', 'Include external link validation')
      .option('--timeout <ms>', 'Timeout for external checks', '5000')
      .option('--concurrent <num>', 'Concurrent link checks', '10')
      .action(async (options) => {
        await this.validateLinks(options);
      });

    // Optimize images command
    this.program
      .command('optimize-images')
      .description('Optimize images for web delivery')
      .option('--quality <num>', 'Image quality (1-100)', '85')
      .option('--max-width <pixels>', 'Maximum width', '1920')
      .option('--max-height <pixels>', 'Maximum height', '1080')
      .option('--format <format>', 'Output format: original|webp|auto', 'auto')
      .action(async (options) => {
        await this.optimizeImages(options);
      });

    // Build command
    this.program
      .command('build')
      .description('Run complete documentation build pipeline')
      .option('--skip-audit', 'Skip documentation audit')
      .option('--skip-diagrams', 'Skip diagram generation')
      .option('--skip-fixes', 'Skip automated fixes')
      .option('--skip-validation', 'Skip link validation')
      .action(async (options) => {
        await this.build(options);
      });

    // Status command
    this.program
      .command('status')
      .description('Show documentation status and health metrics')
      .option('--detailed', 'Show detailed status information')
      .action(async (options) => {
        await this.status(options);
      });

    // Info command
    this.program
      .command('info')
      .description('Show tool and environment information')
      .action(async () => {
        await this.info();
      });

    // Validate mermaid command
    this.program
      .command('validate-mermaid')
      .description('Validate Mermaid diagram syntax')
      .action(async (options) => {
        await this.validateMermaid(options);
      });
  }

  /**
   * Set global CLI options
   * @param {object} options - Global options
   */
  setGlobalOptions(options) {
    this.globalOptions = options;
    
    // Initialize services with configured logger and options
    this.fileRepository = new FileSystemRepository(
      path.resolve(options.docsDir || 'docs')
    );
    
    this.auditService = new DocumentationAuditService(this.fileRepository, this.logger);
    this.diagramService = new DiagramGenerationService(this.fileRepository, null, this.logger);
    this.fixService = new DocumentationFixService(this.fileRepository, this.logger);
  }

  /**
   * Run documentation audit
   * @param {object} options - Audit options
   */
  async audit(options) {
    const spinner = ora('Starting documentation audit...').start();
    
    try {
      const docsDir = path.resolve(this.globalOptions.docsDir || 'docs');
      
      spinner.text = 'Running comprehensive audit...';
      const report = await this.auditService.runFullAudit(docsDir, options);

      spinner.succeed('Audit completed successfully');

      // Display results
      if (options.output === 'json') {
        console.log(JSON.stringify(report.toJSON(), null, 2));
      } else {
        console.log(report.generateTextReport());
      }

      // Save report if requested
      if (options.saveReport) {
        const reportPath = path.resolve(options.saveReport);
        const content = options.output === 'json' ? 
          JSON.stringify(report.toJSON(), null, 2) : 
          report.generateTextReport();
        
        await fs.writeFile(reportPath, content);
        this.logger.success(`Report saved to: ${reportPath}`);
      }

      // Auto-fix if requested
      if (options.fixDuplicates) {
        this.logger.progress('Applying automatic fixes...');
        const fixResults = await this.auditService.autoFixIssues(report, options);
        
        if (fixResults.fixed > 0) {
          this.logger.success(`Applied ${fixResults.fixed} automatic fixes`);
        }
      }

      // Exit with error code if critical issues found
      const criticalIssues = report.getIssuesBySeverity('critical').length;
      if (criticalIssues > 0) {
        this.logger.warn(`Found ${criticalIssues} critical issues`);
        process.exit(1);
      }

    } catch (error) {
      spinner.fail('Audit failed');
      throw error;
    }
  }

  /**
   * Generate diagrams from Mermaid placeholders
   * @param {object} options - Generation options
   */
  async generateDiagrams(options) {
    const spinner = ora('Initializing diagram generation...').start();
    
    try {
      const docsDir = path.resolve(this.globalOptions.docsDir || 'docs');
      const inputDir = options.inputDir ? path.resolve(options.inputDir) : 
                      path.join(docsDir, 'images', 'diagrams');
      const outputDir = options.outputDir ? path.resolve(options.outputDir) : inputDir;

      // Configure Mermaid renderer
      const mermaidOptions = {
        theme: options.theme || 'default',
        backgroundColor: options.background || 'transparent',
        width: parseInt(options.width || '1920'),
        height: parseInt(options.height || '1080')
      };

      const mermaidRenderer = new MermaidRenderer(mermaidOptions);
      this.diagramService = new DiagramGenerationService(
        this.fileRepository, 
        mermaidRenderer, 
        this.logger
      );

      spinner.text = 'Checking Mermaid CLI availability...';
      const isAvailable = await mermaidRenderer.isAvailable();
      if (!isAvailable) {
        spinner.fail('Mermaid CLI not available');
        this.logger.error('Please install @mermaid-js/mermaid-cli: npm install -g @mermaid-js/mermaid-cli');
        process.exit(1);
      }

      spinner.text = 'Generating diagrams...';
      const results = await this.diagramService.generateAllDiagrams(inputDir, outputDir, mermaidOptions);

      spinner.succeed(`Generated ${results.successful.length}/${results.total} diagrams successfully`);

      // Show results
      this.logger.summary({
        totalDiagrams: results.total,
        successful: results.successful.length,
        failed: results.failed.length
      });

      if (results.failed.length > 0) {
        this.logger.warn('Failed diagrams:');
        results.failed.forEach(diagram => {
          this.logger.failure(`  - ${diagram.filename || diagram.outputPath}`);
        });
      }

      if (results.successful.length > 0) {
        this.logger.success('Successfully generated diagrams:');
        results.successful.forEach(diagram => {
          this.logger.success(`  - ${path.basename(diagram.outputPath || diagram.filename)}`);
        });
      }

    } catch (error) {
      spinner.fail('Diagram generation failed');
      throw error;
    }
  }

  /**
   * Replace Mermaid blocks with PNG references
   * @param {object} options - Replacement options
   */
  async replaceMermaid(options) {
    const spinner = ora('Replacing Mermaid blocks with PNG references...').start();
    
    try {
      const docsDir = path.resolve(this.globalOptions.docsDir || 'docs');
      
      if (options.dryRun) {
        spinner.text = 'Running in dry-run mode...';
        this.logger.warn('Dry-run mode: No files will be modified');
      }

      const results = await this.diagramService.replaceMermaidWithPNG(docsDir, {
        dryRun: options.dryRun,
        verbose: this.globalOptions.verbose
      });

      spinner.succeed('Mermaid replacement completed');

      this.logger.summary({
        filesProcessed: results.filesProcessed,
        totalReplacements: results.replacements,
        formattingFixes: results.formattingFixes || 0
      });

      if (results.replacements === 0) {
        this.logger.info('No Mermaid blocks found to replace');
      }

    } catch (error) {
      spinner.fail('Mermaid replacement failed');
      throw error;
    }
  }

  /**
   * Fix common documentation issues
   * @param {object} options - Fix options
   */
  async fixIssues(options) {
    const spinner = ora('Fixing documentation issues...').start();
    
    try {
      const docsDir = path.resolve(this.globalOptions.docsDir || 'docs');
      
      const fixOptions = {
        createMissing: options.createMissing,
        fixLinks: options.fixLinks,
        removeOrphans: options.removeOrphans,
        updateNav: options.updateNav,
        preserveDiagramFiles: options.preserveDiagramFiles
      };

      const results = await this.fixService.runAllFixes(docsDir, fixOptions);

      spinner.succeed('Documentation fixes completed');

      this.logger.summary({
        filesCreated: results.filesCreated,
        filesRemoved: results.filesRemoved,
        linksUpdated: results.linksUpdated,
        navigationUpdated: results.navigationUpdated
      });

      if (results.filesCreated > 0) {
        this.logger.success(`Created ${results.filesCreated} missing files`);
      }
      
      if (results.linksUpdated > 0) {
        this.logger.success(`Fixed links in ${results.linksUpdated} files`);
      }

    } catch (error) {
      spinner.fail('Fix process failed');
      throw error;
    }
  }

  /**
   * Validate internal and external links
   * @param {object} options - Validation options
   */
  async validateLinks(options) {
    const spinner = ora('Validating links...').start();
    
    try {
      const docsDir = path.resolve(this.globalOptions.docsDir || 'docs');
      
      spinner.text = 'Validating internal links...';
      
      // For now, use audit service to check broken links
      // In a full implementation, we'd create a dedicated LinkValidationService
      const report = await this.auditService.runFullAudit(docsDir, { quickMode: true });
      const brokenLinks = report.getIssuesByType('brokenLinks');

      spinner.succeed('Link validation completed');

      if (brokenLinks.length === 0) {
        this.logger.success('All internal links are valid');
      } else {
        this.logger.warn(`Found ${brokenLinks.length} broken internal links:`);
        brokenLinks.forEach(link => {
          this.logger.failure(`  ${link.sourceFile}:${link.line} - ${link.linkUrl}`);
        });
      }

      // TODO: Implement external link validation if options.external is true
      if (options.external) {
        this.logger.info('External link validation not yet implemented');
      }

    } catch (error) {
      spinner.fail('Link validation failed');
      throw error;
    }
  }

  /**
   * Optimize images for web delivery
   * @param {object} options - Optimization options
   */
  async optimizeImages(options) {
    const spinner = ora('Optimizing images...').start();
    
    try {
      // This would be implemented with Sharp or similar image processing library
      // For now, just show a placeholder implementation
      
      spinner.text = 'Finding images to optimize...';
      const docsDir = path.resolve(this.globalOptions.docsDir || 'docs');
      const imageFiles = await this.fileRepository.findAllImageFiles(docsDir);
      
      spinner.succeed(`Found ${imageFiles.length} images`);
      
      this.logger.info('Image optimization not yet fully implemented');
      this.logger.info('Optimization would include:');
      this.logger.info(`  - Quality: ${options.quality}%`);
      this.logger.info(`  - Max dimensions: ${options.maxWidth}x${options.maxHeight}`);
      this.logger.info(`  - Format: ${options.format}`);
      
      // TODO: Implement actual image optimization
      
    } catch (error) {
      spinner.fail('Image optimization failed');
      throw error;
    }
  }

  /**
   * Validate Mermaid diagram syntax
   * @param {object} options - Validation options
   */
  async validateMermaid(options) {
    const spinner = ora('Validating Mermaid diagrams...').start();
    
    try {
      const docsDir = path.resolve(this.globalOptions.docsDir || 'docs');
      const results = await this.diagramService.validateMermaidDiagrams(docsDir);

      spinner.succeed('Mermaid validation completed');

      this.logger.summary({
        totalDiagrams: results.total,
        validDiagrams: results.valid.length,
        invalidDiagrams: results.invalid.length
      });

      if (results.invalid.length > 0) {
        this.logger.warn('Invalid Mermaid diagrams found:');
        results.invalid.forEach(invalid => {
          this.logger.failure(`  ${invalid.file}:${invalid.line}`);
        });
        process.exit(1);
      } else {
        this.logger.success('All Mermaid diagrams have valid syntax');
      }

    } catch (error) {
      spinner.fail('Mermaid validation failed');
      throw error;
    }
  }

  /**
   * Run complete documentation build pipeline
   * @param {object} options - Build options
   */
  async build(options) {
    this.logger.section('Documentation Build Pipeline');
    
    try {
      const steps = [];
      
      if (!options.skipAudit) steps.push('audit');
      if (!options.skipDiagrams) steps.push('diagrams');
      if (!options.skipFixes) steps.push('fixes');
      if (!options.skipValidation) steps.push('validation');

      this.logger.info(`Build pipeline steps: ${steps.join(' → ')}`);

      // Step 1: Audit
      if (!options.skipAudit) {
        this.logger.subsection('Step 1: Documentation Audit');
        await this.audit({ output: 'text', fixDuplicates: true });
      }

      // Step 2: Generate Diagrams
      if (!options.skipDiagrams) {
        this.logger.subsection('Step 2: Diagram Generation');
        await this.generateDiagrams({});
        
        // Replace Mermaid blocks with PNG references
        await this.replaceMermaid({});
      }

      // Step 3: Fix Issues
      if (!options.skipFixes) {
        this.logger.subsection('Step 3: Fix Issues');
        await this.fixIssues({
          createMissing: true,
          fixLinks: true,
          removeOrphans: true,
          updateNav: true
        });
      }

      // Step 4: Validation
      if (!options.skipValidation) {
        this.logger.subsection('Step 4: Link Validation');
        await this.validateLinks({});
        
        this.logger.subsection('Step 4b: Mermaid Validation');
        await this.validateMermaid({});
      }

      this.logger.section('Build Pipeline Complete');
      this.logger.success('All build steps completed successfully!');

    } catch (error) {
      this.logger.failure('Build pipeline failed');
      throw error;
    }
  }

  /**
   * Show documentation status and health metrics
   * @param {object} options - Status options
   */
  async status(options) {
    const spinner = ora('Gathering documentation status...').start();
    
    try {
      const docsDir = path.resolve(this.globalOptions.docsDir || 'docs');
      const report = await this.auditService.runFullAudit(docsDir, { quickMode: true });
      const summary = report.getExecutiveSummary();

      spinner.succeed('Status check completed');

      this.logger.section('Documentation Status');
      
      // Health Score
      const healthScore = summary.healthScore;
      const healthColor = healthScore >= 90 ? 'green' : 
                         healthScore >= 70 ? 'yellow' : 'red';
      
      this.logger.custom('🏥', `Health Score: ${healthScore}/100`, healthColor);
      
      // Basic metrics
      this.logger.info(`Total Files: ${summary.totalFiles}`);
      this.logger.info(`Total Issues: ${summary.totalIssues}`);
      
      if (summary.criticalIssues > 0) {
        this.logger.custom('🚨', `Critical Issues: ${summary.criticalIssues}`, 'red');
      }
      
      if (summary.warningIssues > 0) {
        this.logger.custom('⚠️', `Warning Issues: ${summary.warningIssues}`, 'yellow');
      }
      
      if (summary.infoIssues > 0) {
        this.logger.custom('ℹ️', `Info Issues: ${summary.infoIssues}`, 'blue');
      }

      // Detailed status
      if (options.detailed) {
        this.logger.subsection('Detailed Status');
        
        Object.entries(report.issues).forEach(([type, issues]) => {
          if (issues.length > 0) {
            this.logger.info(`${type}: ${issues.length} issues`);
          }
        });

        // Show top recommendations
        const recommendations = report.getSortedRecommendations().slice(0, 3);
        if (recommendations.length > 0) {
          this.logger.subsection('Top Recommendations');
          recommendations.forEach((rec, index) => {
            const priority = rec.priority <= 2 ? '🔥 HIGH' : 
                           rec.priority <= 3 ? '📋 MEDIUM' : '📝 LOW';
            this.logger.info(`${index + 1}. [${priority}] ${rec.recommendation}`);
          });
        }
      }

    } catch (error) {
      spinner.fail('Status check failed');
      throw error;
    }
  }

  /**
   * Show tool and environment information
   */
  async info() {
    this.logger.section('CSA Documentation Tools - System Information');
    
    try {
      // Tool version
      const packagePath = path.join(process.cwd(), 'package.json');
      let version = '1.0.0';
      
      if (await fs.pathExists(packagePath)) {
        const pkg = await fs.readJSON(packagePath);
        version = pkg.version || version;
      }

      this.logger.info(`CSA Docs Tools Version: ${version}`);
      this.logger.info(`Node.js Version: ${process.version}`);
      this.logger.info(`Platform: ${process.platform}`);
      this.logger.info(`Architecture: ${process.arch}`);
      
      // Current configuration
      this.logger.subsection('Current Configuration');
      this.logger.info(`Documentation Directory: ${path.resolve(this.globalOptions.docsDir || 'docs')}`);
      this.logger.info(`Verbose Mode: ${this.globalOptions.verbose ? 'enabled' : 'disabled'}`);
      this.logger.info(`Color Output: ${this.globalOptions.color !== false ? 'enabled' : 'disabled'}`);
      
      if (this.globalOptions.logFile) {
        this.logger.info(`Log File: ${this.globalOptions.logFile}`);
      }

      // Check external dependencies
      this.logger.subsection('External Dependencies');
      
      const mermaidRenderer = new MermaidRenderer();
      const mermaidAvailable = await mermaidRenderer.isAvailable();
      
      this.logger.info(`Mermaid CLI: ${mermaidAvailable ? '✅ available' : '❌ not available'}`);
      
      if (mermaidAvailable) {
        try {
          const version = await mermaidRenderer.getVersion();
          this.logger.info(`  Version: ${version}`);
        } catch (error) {
          this.logger.info('  Version: unknown');
        }
      } else {
        this.logger.warn('  Install with: npm install -g @mermaid-js/mermaid-cli');
      }

      // Directory status
      const docsDir = path.resolve(this.globalOptions.docsDir || 'docs');
      const dirExists = await fs.pathExists(docsDir);
      
      this.logger.subsection('Directory Status');
      this.logger.info(`Documentation Directory Exists: ${dirExists ? '✅ yes' : '❌ no'}`);
      
      if (dirExists) {
        const files = await this.fileRepository.findAllMarkdownFiles(docsDir);
        this.logger.info(`Markdown Files Found: ${files.length}`);
        
        const imageFiles = await this.fileRepository.findAllImageFiles(docsDir);
        this.logger.info(`Image Files Found: ${imageFiles.length}`);
      }

    } catch (error) {
      this.logger.error('Failed to gather system information');
      throw error;
    }
  }
}