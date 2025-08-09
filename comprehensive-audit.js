const fs = require('fs');
const path = require('path');

class DocumentationAuditor {
  constructor(docsDir) {
    this.docsDir = docsDir;
    this.issues = {
      emptyFiles: [],
      brokenLinks: [],
      orphanedFiles: [],
      duplicateIndexReadme: [],
      missingContent: [],
      inaccessibleFiles: []
    };
    this.allMarkdownFiles = [];
    this.linkMap = new Map(); // file -> links it contains
    this.backLinkMap = new Map(); // file -> files that link to it
  }

  // Find all markdown files
  findAllMarkdownFiles(dir = this.docsDir) {
    const items = fs.readdirSync(dir);
    
    for (const item of items) {
      const itemPath = path.join(dir, item);
      const stat = fs.statSync(itemPath);
      
      if (stat.isDirectory()) {
        if (item !== 'node_modules' && item !== '.git' && item !== '.github') {
          this.findAllMarkdownFiles(itemPath);
        }
      } else if (item.endsWith('.md')) {
        this.allMarkdownFiles.push(itemPath);
      }
    }
  }

  // Check for empty or minimal content files
  checkFileContent() {
    console.log('🔍 Checking file content...');
    
    for (const filePath of this.allMarkdownFiles) {
      try {
        const content = fs.readFileSync(filePath, 'utf8').trim();
        const lines = content.split('\n').filter(line => line.trim() !== '');
        
        if (content.length === 0) {
          this.issues.emptyFiles.push({
            file: filePath,
            reason: 'Completely empty file'
          });
        } else if (content.length < 50) {
          this.issues.missingContent.push({
            file: filePath,
            reason: 'Very minimal content (< 50 characters)',
            content: content.substring(0, 100)
          });
        } else if (lines.length <= 2) {
          this.issues.missingContent.push({
            file: filePath,
            reason: 'Only title/header, no substantial content',
            content: content.substring(0, 100)
          });
        }
      } catch (error) {
        console.error(`❌ Error reading ${filePath}:`, error.message);
      }
    }
  }

  // Extract links from markdown content
  extractLinks(content, filePath) {
    const links = [];
    
    // Markdown links: [text](url)
    const markdownLinkRegex = /\[([^\]]*)\]\(([^)]+)\)/g;
    let match;
    
    while ((match = markdownLinkRegex.exec(content)) !== null) {
      const linkText = match[1];
      const linkUrl = match[2];
      
      // Skip external links, anchors, and email links
      if (!linkUrl.startsWith('http') && !linkUrl.startsWith('#') && !linkUrl.startsWith('mailto:')) {
        links.push({
          text: linkText,
          url: linkUrl,
          line: content.substring(0, match.index).split('\n').length
        });
      }
    }
    
    return links;
  }

  // Check for broken internal links
  checkBrokenLinks() {
    console.log('🔗 Checking for broken links...');
    
    for (const filePath of this.allMarkdownFiles) {
      try {
        const content = fs.readFileSync(filePath, 'utf8');
        const links = this.extractLinks(content, filePath);
        this.linkMap.set(filePath, links);
        
        for (const link of links) {
          const currentDir = path.dirname(filePath);
          let targetPath;
          
          // Handle different link formats
          if (link.url.startsWith('/')) {
            // Absolute path from docs root
            targetPath = path.join(this.docsDir, link.url.substring(1));
          } else {
            // Relative path
            targetPath = path.resolve(currentDir, link.url);
          }
          
          // Remove anchor fragments
          const cleanPath = targetPath.split('#')[0];
          
          // Check if target exists (try both .md and without extension)
          let exists = false;
          const possiblePaths = [
            cleanPath,
            cleanPath + '.md',
            path.join(cleanPath, 'README.md'),
            path.join(cleanPath, 'index.md')
          ];
          
          for (const possiblePath of possiblePaths) {
            if (fs.existsSync(possiblePath)) {
              exists = true;
              // Track back-links
              if (!this.backLinkMap.has(possiblePath)) {
                this.backLinkMap.set(possiblePath, []);
              }
              this.backLinkMap.get(possiblePath).push(filePath);
              break;
            }
          }
          
          if (!exists) {
            this.issues.brokenLinks.push({
              sourceFile: filePath,
              linkText: link.text,
              linkUrl: link.url,
              line: link.line,
              targetPath: cleanPath
            });
          }
        }
      } catch (error) {
        console.error(`❌ Error checking links in ${filePath}:`, error.message);
      }
    }
  }

  // Check for duplicate index.md and README.md files
  checkDuplicateIndexReadme() {
    console.log('📄 Checking for duplicate index.md and README.md files...');
    
    const directories = new Set();
    
    // Get all directories that contain markdown files
    for (const filePath of this.allMarkdownFiles) {
      directories.add(path.dirname(filePath));
    }
    
    for (const dir of directories) {
      const indexPath = path.join(dir, 'index.md');
      const readmePath = path.join(dir, 'README.md');
      
      if (fs.existsSync(indexPath) && fs.existsSync(readmePath)) {
        this.issues.duplicateIndexReadme.push({
          directory: dir,
          indexFile: indexPath,
          readmeFile: readmePath
        });
      }
    }
  }

  // Check for orphaned files (files not linked from anywhere)
  checkOrphanedFiles() {
    console.log('🏝️ Checking for orphaned files...');
    
    const rootFiles = ['README.md', 'index.md'];
    
    for (const filePath of this.allMarkdownFiles) {
      const fileName = path.basename(filePath);
      const relativePath = path.relative(this.docsDir, filePath);
      
      // Skip root-level files and certain special files
      if (rootFiles.includes(fileName) || 
          relativePath.startsWith('project-planning') ||
          fileName === 'CHANGELOG.md' ||
          fileName === 'LICENSE.md') {
        continue;
      }
      
      // Check if this file is referenced by any other file
      const isReferenced = this.backLinkMap.has(filePath) && this.backLinkMap.get(filePath).length > 0;
      
      if (!isReferenced) {
        this.issues.orphanedFiles.push({
          file: filePath,
          relativePath: relativePath
        });
      }
    }
  }

  // Generate accessibility report (files that can't be reached from root)
  checkAccessibility() {
    console.log('🚪 Checking file accessibility from root...');
    
    const visited = new Set();
    const queue = [];
    
    // Start from root README.md files
    const rootCandidates = [
      path.join(this.docsDir, 'README.md'),
      path.join(this.docsDir, 'index.md'),
      path.join(path.dirname(this.docsDir), 'README.md')
    ];
    
    for (const rootFile of rootCandidates) {
      if (fs.existsSync(rootFile)) {
        queue.push(rootFile);
        visited.add(rootFile);
      }
    }
    
    // BFS to find all reachable files
    while (queue.length > 0) {
      const currentFile = queue.shift();
      const links = this.linkMap.get(currentFile) || [];
      
      for (const link of links) {
        const currentDir = path.dirname(currentFile);
        let targetPath;
        
        if (link.url.startsWith('/')) {
          targetPath = path.join(this.docsDir, link.url.substring(1));
        } else {
          targetPath = path.resolve(currentDir, link.url);
        }
        
        const cleanPath = targetPath.split('#')[0];
        const possiblePaths = [
          cleanPath,
          cleanPath + '.md',
          path.join(cleanPath, 'README.md'),
          path.join(cleanPath, 'index.md')
        ];
        
        for (const possiblePath of possiblePaths) {
          if (fs.existsSync(possiblePath) && !visited.has(possiblePath)) {
            visited.add(possiblePath);
            queue.push(possiblePath);
          }
        }
      }
    }
    
    // Find files that are not reachable
    for (const filePath of this.allMarkdownFiles) {
      const relativePath = path.relative(this.docsDir, filePath);
      
      // Skip certain files that don't need to be accessible
      if (relativePath.startsWith('project-planning') ||
          path.basename(filePath) === 'CHANGELOG.md' ||
          path.basename(filePath) === 'LICENSE.md') {
        continue;
      }
      
      if (!visited.has(filePath)) {
        this.issues.inaccessibleFiles.push({
          file: filePath,
          relativePath: relativePath
        });
      }
    }
  }

  // Fix duplicate index.md/README.md by removing index.md
  fixDuplicateIndexReadme() {
    console.log('🔧 Fixing duplicate index.md/README.md files...');
    
    for (const duplicate of this.issues.duplicateIndexReadme) {
      try {
        // Read both files to compare content
        const indexContent = fs.readFileSync(duplicate.indexFile, 'utf8');
        const readmeContent = fs.readFileSync(duplicate.readmeFile, 'utf8');
        
        console.log(`📁 Found duplicate in ${duplicate.directory}:`);
        console.log(`   - index.md: ${indexContent.length} chars`);
        console.log(`   - README.md: ${readmeContent.length} chars`);
        
        // If README.md has more content or they're similar, remove index.md
        if (readmeContent.length >= indexContent.length * 0.8) {
          fs.unlinkSync(duplicate.indexFile);
          console.log(`   ✅ Removed ${duplicate.indexFile}`);
        } else {
          // If index.md has significantly more content, move it to README.md
          fs.writeFileSync(duplicate.readmeFile, indexContent);
          fs.unlinkSync(duplicate.indexFile);
          console.log(`   ✅ Moved content from index.md to README.md and removed index.md`);
        }
      } catch (error) {
        console.error(`   ❌ Error fixing ${duplicate.directory}:`, error.message);
      }
    }
  }

  // Generate comprehensive report
  generateReport() {
    console.log('\n📊 COMPREHENSIVE DOCUMENTATION AUDIT REPORT');
    console.log('=' .repeat(60));
    
    console.log(`\n📈 SUMMARY:`);
    console.log(`Total markdown files found: ${this.allMarkdownFiles.length}`);
    console.log(`Empty files: ${this.issues.emptyFiles.length}`);
    console.log(`Files with minimal content: ${this.issues.missingContent.length}`);
    console.log(`Broken links: ${this.issues.brokenLinks.length}`);
    console.log(`Orphaned files: ${this.issues.orphanedFiles.length}`);
    console.log(`Duplicate index/README pairs: ${this.issues.duplicateIndexReadme.length}`);
    console.log(`Inaccessible files: ${this.issues.inaccessibleFiles.length}`);
    
    if (this.issues.emptyFiles.length > 0) {
      console.log(`\n🚫 EMPTY FILES (${this.issues.emptyFiles.length}):`);
      this.issues.emptyFiles.forEach(issue => {
        console.log(`   - ${path.relative(this.docsDir, issue.file)}: ${issue.reason}`);
      });
    }
    
    if (this.issues.missingContent.length > 0) {
      console.log(`\n📝 FILES WITH MINIMAL CONTENT (${this.issues.missingContent.length}):`);
      this.issues.missingContent.forEach(issue => {
        console.log(`   - ${path.relative(this.docsDir, issue.file)}: ${issue.reason}`);
        console.log(`     Content: "${issue.content}..."`);
      });
    }
    
    if (this.issues.brokenLinks.length > 0) {
      console.log(`\n🔗 BROKEN LINKS (${this.issues.brokenLinks.length}):`);
      this.issues.brokenLinks.forEach(issue => {
        console.log(`   - ${path.relative(this.docsDir, issue.sourceFile)}:${issue.line}`);
        console.log(`     Link: [${issue.linkText}](${issue.linkUrl})`);
        console.log(`     Target: ${issue.targetPath}`);
      });
    }
    
    if (this.issues.orphanedFiles.length > 0) {
      console.log(`\n🏝️ ORPHANED FILES (${this.issues.orphanedFiles.length}):`);
      this.issues.orphanedFiles.forEach(issue => {
        console.log(`   - ${issue.relativePath}`);
      });
    }
    
    if (this.issues.duplicateIndexReadme.length > 0) {
      console.log(`\n📄 DUPLICATE INDEX/README FILES (${this.issues.duplicateIndexReadme.length}):`);
      this.issues.duplicateIndexReadme.forEach(issue => {
        console.log(`   - ${path.relative(this.docsDir, issue.directory)}`);
      });
    }
    
    if (this.issues.inaccessibleFiles.length > 0) {
      console.log(`\n🚪 INACCESSIBLE FILES (${this.issues.inaccessibleFiles.length}):`);
      this.issues.inaccessibleFiles.forEach(issue => {
        console.log(`   - ${issue.relativePath}`);
      });
    }
    
    console.log('\n✨ AUDIT COMPLETE!');
    
    return this.issues;
  }

  // Run full audit
  async runFullAudit(fixDuplicates = true) {
    console.log('🚀 Starting comprehensive documentation audit...\n');
    
    this.findAllMarkdownFiles();
    this.checkFileContent();
    this.checkBrokenLinks();
    this.checkDuplicateIndexReadme();
    this.checkOrphanedFiles();
    this.checkAccessibility();
    
    if (fixDuplicates && this.issues.duplicateIndexReadme.length > 0) {
      this.fixDuplicateIndexReadme();
    }
    
    return this.generateReport();
  }
}

// Run the audit
const docsDir = path.join(__dirname, 'docs');
const auditor = new DocumentationAuditor(docsDir);

auditor.runFullAudit(true).then(issues => {
  console.log('\n🎯 NEXT STEPS:');
  
  if (issues.emptyFiles.length > 0) {
    console.log('1. Add content to empty files or remove them if not needed');
  }
  
  if (issues.missingContent.length > 0) {
    console.log('2. Expand files with minimal content');
  }
  
  if (issues.brokenLinks.length > 0) {
    console.log('3. Fix broken internal links');
  }
  
  if (issues.orphanedFiles.length > 0) {
    console.log('4. Link orphaned files from parent documents or remove if not needed');
  }
  
  if (issues.inaccessibleFiles.length > 0) {
    console.log('5. Ensure all important files are accessible from the main navigation');
  }
  
  console.log('\n📋 Audit results can be used to systematically improve documentation quality.');
}).catch(error => {
  console.error('❌ Audit failed:', error);
});
