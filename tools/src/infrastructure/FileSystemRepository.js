/**
 * Infrastructure layer for file system operations
 * Handles all file I/O operations and directory traversal
 */
import fs from 'fs-extra';
import path from 'path';
import { glob } from 'glob';
import { DocumentationFile } from '../domain/models/DocumentationFile.js';

export class FileSystemRepository {
  constructor(rootDir = process.cwd()) {
    this.rootDir = rootDir;
  }

  /**
   * Find all markdown files in a directory recursively
   * @param {string} dir - Directory to search (defaults to root)
   * @param {string[]} excludeDirs - Directories to exclude
   * @returns {Promise<DocumentationFile[]>} - Array of DocumentationFile objects
   */
  async findAllMarkdownFiles(dir = null, excludeDirs = ['node_modules', '.git', '.github', 'site']) {
    const searchDir = dir || this.rootDir;
    const pattern = path.join(searchDir, '**/*.md');
    
    try {
      const files = await glob(pattern, {
        ignore: excludeDirs.map(exclude => `**/${exclude}/**`)
      });

      const documentationFiles = [];
      
      for (const filePath of files) {
        const content = await this.readFile(filePath);
        const docFile = new DocumentationFile(filePath, content);
        docFile.setRelativePath(path.relative(this.rootDir, filePath));
        documentationFiles.push(docFile);
      }

      return documentationFiles;
    } catch (error) {
      throw new Error(`Failed to find markdown files: ${error.message}`);
    }
  }

  /**
   * Read file content
   * @param {string} filePath - File path to read
   * @returns {Promise<string>} - File content
   */
  async readFile(filePath) {
    try {
      return await fs.readFile(filePath, 'utf8');
    } catch (error) {
      throw new Error(`Failed to read file ${filePath}: ${error.message}`);
    }
  }

  /**
   * Write file content
   * @param {string} filePath - File path to write
   * @param {string} content - Content to write
   * @returns {Promise<void>}
   */
  async writeFile(filePath, content) {
    try {
      await fs.ensureDir(path.dirname(filePath));
      await fs.writeFile(filePath, content, 'utf8');
    } catch (error) {
      throw new Error(`Failed to write file ${filePath}: ${error.message}`);
    }
  }

  /**
   * Check if file exists
   * @param {string} filePath - File path to check
   * @returns {Promise<boolean>} - True if file exists
   */
  async fileExists(filePath) {
    try {
      await fs.access(filePath);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Delete file
   * @param {string} filePath - File path to delete
   * @returns {Promise<void>}
   */
  async deleteFile(filePath) {
    try {
      await fs.unlink(filePath);
    } catch (error) {
      throw new Error(`Failed to delete file ${filePath}: ${error.message}`);
    }
  }

  /**
   * Create directory if it doesn't exist
   * @param {string} dirPath - Directory path to create
   * @returns {Promise<void>}
   */
  async ensureDirectory(dirPath) {
    try {
      await fs.ensureDir(dirPath);
    } catch (error) {
      throw new Error(`Failed to create directory ${dirPath}: ${error.message}`);
    }
  }

  /**
   * Get file stats
   * @param {string} filePath - File path
   * @returns {Promise<fs.Stats>} - File stats
   */
  async getFileStats(filePath) {
    try {
      return await fs.stat(filePath);
    } catch (error) {
      throw new Error(`Failed to get stats for ${filePath}: ${error.message}`);
    }
  }

  /**
   * List directory contents
   * @param {string} dirPath - Directory path
   * @returns {Promise<string[]>} - Array of file/directory names
   */
  async listDirectory(dirPath) {
    try {
      return await fs.readdir(dirPath);
    } catch (error) {
      throw new Error(`Failed to list directory ${dirPath}: ${error.message}`);
    }
  }

  /**
   * Find all image files in a directory
   * @param {string} dir - Directory to search
   * @returns {Promise<string[]>} - Array of image file paths
   */
  async findAllImageFiles(dir) {
    const imageExtensions = ['png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'];
    const patterns = imageExtensions.map(ext => path.join(dir, `**/*.${ext}`));
    
    try {
      const allFiles = [];
      for (const pattern of patterns) {
        const files = await glob(pattern);
        allFiles.push(...files);
      }
      return allFiles;
    } catch (error) {
      throw new Error(`Failed to find image files: ${error.message}`);
    }
  }

  /**
   * Check for duplicate files in a directory
   * @param {string} dirPath - Directory to check
   * @param {string[]} fileNames - File names to check for duplicates
   * @returns {Promise<object[]>} - Array of duplicate sets
   */
  async findDuplicateFiles(dirPath, fileNames = ['index.md', 'README.md']) {
    try {
      const items = await this.listDirectory(dirPath);
      const subdirs = [];
      
      for (const item of items) {
        const itemPath = path.join(dirPath, item);
        const stats = await this.getFileStats(itemPath);
        if (stats.isDirectory()) {
          subdirs.push(itemPath);
        }
      }

      const duplicates = [];
      
      for (const subdir of subdirs) {
        const foundFiles = [];
        
        for (const fileName of fileNames) {
          const filePath = path.join(subdir, fileName);
          if (await this.fileExists(filePath)) {
            foundFiles.push(filePath);
          }
        }
        
        if (foundFiles.length > 1) {
          duplicates.push({
            directory: subdir,
            files: foundFiles
          });
        }
      }

      return duplicates;
    } catch (error) {
      throw new Error(`Failed to find duplicate files: ${error.message}`);
    }
  }

  /**
   * Get relative path from one file to another
   * @param {string} fromPath - Source file path
   * @param {string} toPath - Target file path
   * @returns {string} - Relative path
   */
  getRelativePath(fromPath, toPath) {
    const fromDir = path.dirname(fromPath);
    return path.relative(fromDir, toPath).replace(/\\/g, '/');
  }

  /**
   * Resolve a link path relative to a source file
   * @param {string} sourcePath - Source file path
   * @param {string} linkPath - Link path to resolve
   * @returns {string} - Resolved absolute path
   */
  resolveLinkPath(sourcePath, linkPath) {
    const sourceDir = path.dirname(sourcePath);
    
    if (linkPath.startsWith('/')) {
      // Absolute path from root
      return path.join(this.rootDir, linkPath.substring(1));
    } else {
      // Relative path
      return path.resolve(sourceDir, linkPath);
    }
  }

  /**
   * Find possible target paths for a link
   * @param {string} targetPath - Target path to find
   * @returns {Promise<string[]>} - Array of possible paths
   */
  async findPossiblePaths(targetPath) {
    const cleanPath = targetPath.split('#')[0]; // Remove anchor fragments
    
    const possiblePaths = [
      cleanPath,
      cleanPath + '.md',
      path.join(cleanPath, 'README.md'),
      path.join(cleanPath, 'index.md')
    ];

    const existingPaths = [];
    
    for (const possiblePath of possiblePaths) {
      if (await this.fileExists(possiblePath)) {
        existingPaths.push(possiblePath);
      }
    }

    return existingPaths;
  }

  /**
   * Copy file
   * @param {string} sourcePath - Source file path
   * @param {string} targetPath - Target file path
   * @returns {Promise<void>}
   */
  async copyFile(sourcePath, targetPath) {
    try {
      await fs.ensureDir(path.dirname(targetPath));
      await fs.copy(sourcePath, targetPath);
    } catch (error) {
      throw new Error(`Failed to copy file from ${sourcePath} to ${targetPath}: ${error.message}`);
    }
  }
}