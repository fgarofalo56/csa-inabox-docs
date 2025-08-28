#!/usr/bin/env node

/**
 * Direct Mermaid to PNG conversion script for GitHub compatibility
 * Extracts Mermaid blocks from markdown files and converts them to PNG
 */

import fs from 'fs-extra';
import path from 'path';
import { glob } from 'glob';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

class MermaidConverter {
  constructor(docsDir) {
    this.docsDir = docsDir;
    this.tempDir = path.join(process.cwd(), 'temp-mermaid');
    this.convertedDiagrams = [];
    this.modifiedFiles = [];
  }

  async init() {
    await fs.ensureDir(this.tempDir);
    console.log('🔄 Initializing Mermaid to PNG conversion...');
  }

  async findMermaidFiles() {
    const pattern = path.join(this.docsDir, '**/*.md');
    const files = await glob(pattern, {
      ignore: ['**/node_modules/**', '**/site/**', '**/.git/**']
    });

    const filesWithMermaid = [];
    
    for (const file of files) {
      const content = await fs.readFile(file, 'utf8');
      if (content.includes('```mermaid')) {
        filesWithMermaid.push({
          filePath: file,
          content: content,
          mermaidBlocks: this.extractMermaidBlocks(content)
        });
      }
    }

    return filesWithMermaid;
  }

  extractMermaidBlocks(content) {
    const blocks = [];
    const mermaidRegex = /```mermaid\n([\s\S]*?)\n```/g;
    let match;
    let blockIndex = 0;

    while ((match = mermaidRegex.exec(content)) !== null) {
      blockIndex++;
      blocks.push({
        fullMatch: match[0],
        code: match[1].trim(),
        startIndex: match.index,
        blockNumber: blockIndex,
        line: content.substring(0, match.index).split('\n').length
      });
    }

    return blocks;
  }

  async convertFile(fileData) {
    console.log(`📄 Processing: ${path.relative(this.docsDir, fileData.filePath)}`);
    
    let modifiedContent = fileData.content;
    let hasModifications = false;

    // Process blocks in reverse order to maintain indices
    for (let i = fileData.mermaidBlocks.length - 1; i >= 0; i--) {
      const block = fileData.mermaidBlocks[i];
      
      try {
        // Generate PNG
        const diagramName = this.generateDiagramName(fileData.filePath, block.blockNumber);
        const pngPath = await this.generatePNG(block.code, diagramName);
        
        // Create relative path for markdown
        const relativePngPath = path.relative(path.dirname(fileData.filePath), pngPath).replace(/\\/g, '/');
        
        // Generate alt text
        const altText = this.generateAltText(block.code, diagramName);
        
        // Replace Mermaid block with PNG reference
        const pngReference = `![${altText}](${relativePngPath})`;
        
        modifiedContent = modifiedContent.substring(0, block.startIndex) + 
                         pngReference + 
                         modifiedContent.substring(block.startIndex + block.fullMatch.length);
        
        hasModifications = true;
        
        console.log(`  ✅ Converted diagram ${block.blockNumber} -> ${relativePngPath}`);
        
        this.convertedDiagrams.push({
          sourceFile: fileData.filePath,
          diagramNumber: block.blockNumber,
          pngPath: pngPath,
          altText: altText
        });
        
      } catch (error) {
        console.error(`  ❌ Failed to convert diagram ${block.blockNumber}: ${error.message}`);
      }
    }

    if (hasModifications) {
      await fs.writeFile(fileData.filePath, modifiedContent, 'utf8');
      this.modifiedFiles.push(fileData.filePath);
      console.log(`  📝 Updated file with PNG references`);
    }
  }

  generateDiagramName(filePath, blockNumber) {
    const relativePath = path.relative(this.docsDir, filePath);
    const dirPath = path.dirname(relativePath);
    const baseName = path.basename(relativePath, '.md');
    
    return `${dirPath.replace(/\//g, '-')}-${baseName}-diagram-${blockNumber}`.replace(/^-/, '');
  }

  async generatePNG(mermaidCode, diagramName) {
    const tempMermaidFile = path.join(this.tempDir, `${diagramName}.mmd`);
    const outputDir = path.join(this.docsDir, 'images', 'diagrams');
    const outputPath = path.join(outputDir, `${diagramName}.png`);
    
    // Ensure output directory exists
    await fs.ensureDir(outputDir);
    
    // Write Mermaid code to temp file
    await fs.writeFile(tempMermaidFile, mermaidCode, 'utf8');
    
    // Generate PNG using mmdc
    const command = `mmdc -i "${tempMermaidFile}" -o "${outputPath}" -b transparent -t default --width 1920 --height 1080`;
    
    try {
      await execAsync(command, { timeout: 30000 });
      
      // Clean up temp file
      await fs.unlink(tempMermaidFile);
      
      return outputPath;
    } catch (error) {
      // Clean up temp file even if generation fails
      try {
        await fs.unlink(tempMermaidFile);
      } catch {}
      
      throw new Error(`PNG generation failed: ${error.message}`);
    }
  }

  generateAltText(mermaidCode, diagramName) {
    // Try to determine diagram type
    const firstLine = mermaidCode.split('\n')[0].trim();
    
    if (firstLine.includes('graph')) return `Architecture diagram: ${diagramName}`;
    if (firstLine.includes('flowchart')) return `Process flowchart: ${diagramName}`;
    if (firstLine.includes('sequenceDiagram')) return `Sequence diagram: ${diagramName}`;
    if (firstLine.includes('classDiagram')) return `Class diagram: ${diagramName}`;
    if (firstLine.includes('erDiagram')) return `Entity relationship diagram: ${diagramName}`;
    if (firstLine.includes('gitgraph')) return `Git workflow diagram: ${diagramName}`;
    
    return `Mermaid diagram: ${diagramName}`;
  }

  async cleanup() {
    try {
      await fs.remove(this.tempDir);
    } catch (error) {
      console.warn(`Warning: Could not clean up temp directory: ${error.message}`);
    }
  }

  printSummary() {
    console.log('\n📊 CONVERSION SUMMARY:');
    console.log('='*50);
    console.log(`Files processed: ${this.modifiedFiles.length}`);
    console.log(`Diagrams converted: ${this.convertedDiagrams.length}`);
    console.log(`Output directory: ${path.join(this.docsDir, 'images', 'diagrams')}`);
    
    if (this.convertedDiagrams.length > 0) {
      console.log('\n✅ Successfully converted diagrams:');
      this.convertedDiagrams.forEach(diagram => {
        console.log(`  - ${path.relative(this.docsDir, diagram.sourceFile)} (diagram ${diagram.diagramNumber})`);
      });
    }
    
    if (this.modifiedFiles.length > 0) {
      console.log('\n📝 Modified files:');
      this.modifiedFiles.forEach(file => {
        console.log(`  - ${path.relative(this.docsDir, file)}`);
      });
    }
  }

  async run() {
    try {
      await this.init();
      
      const filesWithMermaid = await this.findMermaidFiles();
      console.log(`🔍 Found ${filesWithMermaid.length} files with Mermaid diagrams`);
      
      if (filesWithMermaid.length === 0) {
        console.log('ℹ️  No Mermaid diagrams found to convert');
        return;
      }
      
      for (const fileData of filesWithMermaid) {
        await this.convertFile(fileData);
      }
      
      this.printSummary();
      
    } catch (error) {
      console.error('❌ Conversion failed:', error.message);
      throw error;
    } finally {
      await this.cleanup();
    }
  }
}

// Run the converter
const docsDir = process.argv[2] || '../docs';
const converter = new MermaidConverter(path.resolve(docsDir));
converter.run().catch(console.error);