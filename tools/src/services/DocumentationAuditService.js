/**
 * Service layer for documentation auditing
 * Orchestrates business logic for analyzing documentation quality
 */
import { AuditReport } from '../domain/models/AuditReport.js';
import { FileSystemRepository } from '../infrastructure/FileSystemRepository.js';

export class DocumentationAuditService {
  constructor(fileRepository = null, logger = null) {
    this.fileRepository = fileRepository || new FileSystemRepository();
    this.logger = logger;
    this.linkMap = new Map(); // file -> links it contains
    this.backLinkMap = new Map(); // file -> files that link to it
  }

  /**
   * Run comprehensive documentation audit
   * @param {string} docsDir - Documentation directory to audit
   * @param {object} options - Audit options
   * @returns {Promise<AuditReport>} - Complete audit report
   */
  async runFullAudit(docsDir, options = {}) {
    const report = new AuditReport();
    
    this.logger?.section('Documentation Audit');
    
    try {
      // Find all markdown files
      this.logger?.progress('Finding all markdown files...');
      const files = await this.fileRepository.findAllMarkdownFiles(docsDir);
      report.setTotalFiles(files.length);

      this.logger?.info(`Found ${files.length} markdown files to analyze`);

      // Run individual audit checks
      await this.checkFileContent(files, report);
      await this.checkBrokenLinks(files, report);
      await this.checkDuplicateIndexReadme(docsDir, report);
      await this.checkOrphanedFiles(files, report);
      await this.checkAccessibility(files, report);

      // Generate recommendations
      this.generateRecommendations(report);

      this.logger?.success('Documentation audit completed successfully');
      
      return report;
    } catch (error) {
      this.logger?.error(`Audit failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Check file content for empty or minimal files
   * @param {DocumentationFile[]} files - Files to check
   * @param {AuditReport} report - Report to update
   */
  async checkFileContent(files, report) {
    this.logger?.subsection('Checking file content quality');

    for (const file of files) {
      if (file.isEmpty) {
        report.addIssue('emptyFiles', {
          file: file.filePath,
          reason: 'Completely empty file'
        }, 'critical');
      } else if (file.hasMinimalContent) {
        report.addIssue('missingContent', {
          file: file.filePath,
          reason: `Minimal content (${file.content?.length || 0} characters)`,
          preview: file.content?.substring(0, 100) || ''
        }, 'warning');
      }
    }

    this.logger?.info(`Content check completed: ${report.getIssuesByType('emptyFiles').length} empty files, ${report.getIssuesByType('missingContent').length} minimal content files`);
  }

  /**
   * Check for broken internal links
   * @param {DocumentationFile[]} files - Files to check
   * @param {AuditReport} report - Report to update
   */
  async checkBrokenLinks(files, report) {
    this.logger?.subsection('Checking for broken links');

    // Build link maps
    this.linkMap.clear();
    this.backLinkMap.clear();

    for (const file of files) {
      this.linkMap.set(file.filePath, file.links);
      
      for (const link of file.links) {
        // Resolve link target
        const targetPath = this.fileRepository.resolveLinkPath(file.filePath, link.url);
        const possiblePaths = await this.fileRepository.findPossiblePaths(targetPath);

        if (possiblePaths.length === 0) {
          report.addIssue('brokenLinks', {
            sourceFile: file.filePath,
            linkText: link.text,
            linkUrl: link.url,
            line: link.line,
            targetPath: targetPath
          }, 'warning');
        } else {
          // Track back-links for orphan detection
          for (const possiblePath of possiblePaths) {
            if (!this.backLinkMap.has(possiblePath)) {
              this.backLinkMap.set(possiblePath, []);
            }
            this.backLinkMap.get(possiblePath).push(file.filePath);
          }
        }
      }
    }

    this.logger?.info(`Link check completed: ${report.getIssuesByType('brokenLinks').length} broken links found`);
  }

  /**
   * Check for duplicate index.md and README.md files
   * @param {string} docsDir - Documentation directory
   * @param {AuditReport} report - Report to update
   */
  async checkDuplicateIndexReadme(docsDir, report) {
    this.logger?.subsection('Checking for duplicate index/README files');

    const duplicates = await this.fileRepository.findDuplicateFiles(docsDir, ['index.md', 'README.md']);

    for (const duplicate of duplicates) {
      report.addIssue('duplicateIndexReadme', {
        directory: duplicate.directory,
        files: duplicate.files
      }, 'warning');
    }

    this.logger?.info(`Duplicate check completed: ${duplicates.length} duplicate pairs found`);
  }

  /**
   * Check for orphaned files (not linked from anywhere)
   * @param {DocumentationFile[]} files - Files to check
   * @param {AuditReport} report - Report to update
   */
  async checkOrphanedFiles(files, report) {
    this.logger?.subsection('Checking for orphaned files');

    const rootFiles = ['README.md', 'index.md'];

    for (const file of files) {
      const fileName = file.filename + file.extension;

      // Skip root-level files and certain special files
      if (rootFiles.includes(fileName) ||
          file.relativePath?.startsWith('project_tracking') ||
          fileName === 'CHANGELOG.md' ||
          fileName === 'LICENSE.md') {
        continue;
      }

      // Check if this file is referenced by any other file
      const isReferenced = this.backLinkMap.has(file.filePath) && 
                          this.backLinkMap.get(file.filePath).length > 0;

      if (!isReferenced) {
        report.addIssue('orphanedFiles', {
          file: file.filePath,
          relativePath: file.relativePath
        }, 'info');
      }
    }

    this.logger?.info(`Orphan check completed: ${report.getIssuesByType('orphanedFiles').length} orphaned files found`);
  }

  /**
   * Check file accessibility from root
   * @param {DocumentationFile[]} files - Files to check
   * @param {AuditReport} report - Report to update
   */
  async checkAccessibility(files, report) {
    this.logger?.subsection('Checking file accessibility from root');

    const visited = new Set();
    const queue = [];

    // Find root files
    const rootCandidates = files.filter(file => 
      (file.filename === 'README' || file.filename === 'index') && 
      file.directory === this.fileRepository.rootDir
    );

    for (const rootFile of rootCandidates) {
      queue.push(rootFile.filePath);
      visited.add(rootFile.filePath);
    }

    // BFS to find all reachable files
    while (queue.length > 0) {
      const currentFile = queue.shift();
      const links = this.linkMap.get(currentFile) || [];

      for (const link of links) {
        const targetPath = this.fileRepository.resolveLinkPath(currentFile, link.url);
        const possiblePaths = await this.fileRepository.findPossiblePaths(targetPath);

        for (const possiblePath of possiblePaths) {
          if (!visited.has(possiblePath)) {
            visited.add(possiblePath);
            queue.push(possiblePath);
          }
        }
      }
    }

    // Find files that are not reachable
    for (const file of files) {
      // Skip certain files that don't need to be accessible
      if (file.relativePath?.startsWith('project_tracking') ||
          file.filename === 'CHANGELOG' ||
          file.filename === 'LICENSE') {
        continue;
      }

      if (!visited.has(file.filePath)) {
        report.addIssue('inaccessibleFiles', {
          file: file.filePath,
          relativePath: file.relativePath
        }, 'info');
      }
    }

    this.logger?.info(`Accessibility check completed: ${report.getIssuesByType('inaccessibleFiles').length} inaccessible files found`);
  }

  /**
   * Generate recommendations based on audit results
   * @param {AuditReport} report - Report to update with recommendations
   */
  generateRecommendations(report) {
    const issues = report.issues;

    if (issues.emptyFiles.length > 0) {
      report.addRecommendation(
        'Remove empty files or add meaningful content to them',
        1
      );
    }

    if (issues.brokenLinks.length > 0) {
      report.addRecommendation(
        'Fix broken internal links to improve navigation',
        1
      );
    }

    if (issues.missingContent.length > 0) {
      report.addRecommendation(
        'Expand files with minimal content to provide more value',
        2
      );
    }

    if (issues.duplicateIndexReadme.length > 0) {
      report.addRecommendation(
        'Consolidate duplicate index.md and README.md files',
        2
      );
    }

    if (issues.orphanedFiles.length > 5) {
      report.addRecommendation(
        'Link orphaned files from parent documents or consider removing unused files',
        3
      );
    }

    if (issues.inaccessibleFiles.length > 0) {
      report.addRecommendation(
        'Ensure important files are accessible from the main navigation',
        3
      );
    }

    // Health-based recommendations
    const healthScore = report.calculateHealthScore();
    if (healthScore < 70) {
      report.addRecommendation(
        'Documentation health is below 70%. Prioritize fixing critical and warning issues',
        1
      );
    } else if (healthScore < 90) {
      report.addRecommendation(
        'Documentation health is good but could be improved. Address remaining warnings',
        3
      );
    }
  }

  /**
   * Auto-fix certain types of issues
   * @param {AuditReport} report - Audit report with issues
   * @param {object} options - Fix options
   * @returns {Promise<object>} - Fix results
   */
  async autoFixIssues(report, options = {}) {
    const results = {
      fixed: 0,
      failed: 0,
      skipped: 0
    };

    this.logger?.section('Auto-fixing Issues');

    // Fix duplicate index/README files
    if (options.fixDuplicates !== false) {
      const duplicates = report.getIssuesByType('duplicateIndexReadme');
      
      for (const duplicate of duplicates) {
        try {
          await this.fixDuplicateIndexReadme(duplicate);
          results.fixed++;
        } catch (error) {
          this.logger?.error(`Failed to fix duplicate in ${duplicate.directory}: ${error.message}`);
          results.failed++;
        }
      }
    }

    this.logger?.summary(results);
    return results;
  }

  /**
   * Fix duplicate index.md/README.md by removing index.md
   * @param {object} duplicate - Duplicate issue details
   */
  async fixDuplicateIndexReadme(duplicate) {
    const indexPath = duplicate.files.find(f => f.endsWith('index.md'));
    const readmePath = duplicate.files.find(f => f.endsWith('README.md'));

    if (!indexPath || !readmePath) return;

    // Read both files to compare content
    const indexContent = await this.fileRepository.readFile(indexPath);
    const readmeContent = await this.fileRepository.readFile(readmePath);

    this.logger?.info(`Fixing duplicate in ${duplicate.directory}:`);
    this.logger?.info(`  - index.md: ${indexContent.length} chars`);
    this.logger?.info(`  - README.md: ${readmeContent.length} chars`);

    // If README.md has more content or they're similar, remove index.md
    if (readmeContent.length >= indexContent.length * 0.8) {
      await this.fileRepository.deleteFile(indexPath);
      this.logger?.success(`Removed ${indexPath}`);
    } else {
      // If index.md has significantly more content, move it to README.md
      await this.fileRepository.writeFile(readmePath, indexContent);
      await this.fileRepository.deleteFile(indexPath);
      this.logger?.success(`Moved content from index.md to README.md and removed index.md`);
    }
  }
}