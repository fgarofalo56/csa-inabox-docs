#!/usr/bin/env node

/**
 * Replace Material Design icons with GitHub-compatible Unicode alternatives
 */

import fs from 'fs-extra';
import path from 'path';
import { glob } from 'glob';

class MaterialIconReplacer {
  constructor(docsDir) {
    this.docsDir = docsDir;
    this.iconMappings = {
      // Office and workspace icons
      ':material-office-building:': '🏢',
      ':material-account-supervisor:': '👥',
      ':material-tag-multiple:': '🏷️',
      ':material-backup-restore:': '💾',
      ':material-finance:': '💰',
      
      // Security and network icons
      ':material-lock-network:': '🔐',
      ':material-connection:': '🔗',
      ':material-dns:': '🌐',
      ':material-virtual-reality:': '📡',
      ':material-check-network:': '✅',
      ':material-private-network:': '🔒',
      ':material-firewall:': '🛡️',
      ':material-shield-lock:': '🛡️',
      ':material-transit-connection-variant:': '🚀',
      ':material-security-network:': '🔐',
      
      // Performance and optimization icons
      ':material-speedometer:': '⚡',
      ':material-file-cabinet:': '📁',
      ':material-order-alphabetical-ascending:': '📊',
      ':material-memory:': '💻',
      ':material-text-search:': '🔍',
      ':material-cog-refresh:': '🔄',
      ':material-chart-bar:': '📊',
      ':material-chart-line:': '📈',
      ':material-chart-timeline:': '📊',
      
      // Data and database icons
      ':material-database-import:': '📥',
      ':material-database-search:': '🔍',
      ':material-database-search-outline:': '🔍',
      ':material-history:': '📜',
      ':material-table:': '📋',
      ':material-table-link:': '🔗',
      ':material-brain:': '🧠',
      ':material-pipe-wrench:': '🔧',
      
      // Testing and monitoring icons
      ':material-test-tube:': '🧪',
      ':material-pipe:': '⚡',
      ':material-notebook-edit:': '📝',
      ':material-monitor-dashboard:': '📊',
      ':material-pipeline-alert:': '🚨',
      ':material-alert-circle-outline:': '⚠️',
      ':material-alert-circle:': '⚠️',
      ':material-cog-outline:': '⚙️',
      ':material-file-search:': '🔍',
      ':material-bell-ring:': '🔔',
      ':material-file-document-multiple:': '📄',
      ':material-clipboard-check:': '✅',
      
      // Security monitoring icons  
      ':material-shield-lock:': '🛡️',
      ':material-eye-scan:': '👁️',
      
      // Business and finance icons
      ':material-credit-card-outline:': '💳',
      ':material-account-group-outline:': '👥',
      ':material-chart-box-outline:': '📦'
    };
    
    this.modifiedFiles = [];
    this.totalReplacements = 0;
  }

  async findFilesWithIcons() {
    const pattern = path.join(this.docsDir, '**/*.md');
    const files = await glob(pattern, {
      ignore: ['**/node_modules/**', '**/site/**', '**/.git/**']
    });

    const filesWithIcons = [];
    
    for (const file of files) {
      const content = await fs.readFile(file, 'utf8');
      const hasIcons = Object.keys(this.iconMappings).some(icon => content.includes(icon));
      
      if (hasIcons) {
        filesWithIcons.push({
          filePath: file,
          content: content
        });
      }
    }

    return filesWithIcons;
  }

  async replaceIconsInFile(fileData) {
    console.log(`📄 Processing: ${path.relative(this.docsDir, fileData.filePath)}`);
    
    let modifiedContent = fileData.content;
    let fileReplacements = 0;
    
    // Replace each Material Design icon with its Unicode equivalent
    for (const [materialIcon, unicodeIcon] of Object.entries(this.iconMappings)) {
      const regex = new RegExp(this.escapeRegExp(materialIcon), 'g');
      const matches = modifiedContent.match(regex);
      
      if (matches) {
        modifiedContent = modifiedContent.replace(regex, unicodeIcon);
        fileReplacements += matches.length;
        console.log(`  ✅ Replaced ${matches.length}x ${materialIcon} -> ${unicodeIcon}`);
      }
    }
    
    // Also handle the inline styling patterns like { .lg .middle }
    modifiedContent = modifiedContent.replace(/\{ \.lg \.middle \}/g, '');
    
    if (fileReplacements > 0) {
      await fs.writeFile(fileData.filePath, modifiedContent, 'utf8');
      this.modifiedFiles.push(fileData.filePath);
      this.totalReplacements += fileReplacements;
      console.log(`  📝 Updated file with ${fileReplacements} replacements`);
    }
  }

  escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  printSummary() {
    console.log('\n📊 ICON REPLACEMENT SUMMARY:');
    console.log('='*50);
    console.log(`Files processed: ${this.modifiedFiles.length}`);
    console.log(`Total replacements: ${this.totalReplacements}`);
    
    if (this.modifiedFiles.length > 0) {
      console.log('\n📝 Modified files:');
      this.modifiedFiles.forEach(file => {
        console.log(`  - ${path.relative(this.docsDir, file)}`);
      });
    }
    
    console.log('\n🎨 Icon Mapping Reference:');
    Object.entries(this.iconMappings).forEach(([material, unicode]) => {
      console.log(`  ${material} -> ${unicode}`);
    });
  }

  async run() {
    try {
      console.log('🔄 Initializing Material Design icon replacement...');
      
      const filesWithIcons = await this.findFilesWithIcons();
      console.log(`🔍 Found ${filesWithIcons.length} files with Material Design icons`);
      
      if (filesWithIcons.length === 0) {
        console.log('ℹ️  No Material Design icons found to replace');
        return;
      }
      
      for (const fileData of filesWithIcons) {
        await this.replaceIconsInFile(fileData);
      }
      
      this.printSummary();
      
    } catch (error) {
      console.error('❌ Icon replacement failed:', error.message);
      throw error;
    }
  }
}

// Run the replacer
const docsDir = process.argv[2] || '../docs';
const replacer = new MaterialIconReplacer(path.resolve(docsDir));
replacer.run().catch(console.error);