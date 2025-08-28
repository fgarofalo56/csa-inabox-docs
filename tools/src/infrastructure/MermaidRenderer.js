/**
 * Infrastructure layer for Mermaid diagram rendering
 * Handles external Mermaid CLI operations and PNG generation
 */
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs-extra';
import path from 'path';

const execAsync = promisify(exec);

export class MermaidRenderer {
  constructor(options = {}) {
    this.options = {
      backgroundColor: options.backgroundColor || 'transparent',
      theme: options.theme || 'default',
      width: options.width || 1920,
      height: options.height || 1080,
      puppeteerConfig: options.puppeteerConfig || {},
      ...options
    };
    this.tempDir = path.join(process.cwd(), 'temp');
  }

  /**
   * Initialize the renderer (ensure temp directory exists)
   */
  async initialize() {
    await fs.ensureDir(this.tempDir);
  }

  /**
   * Generate PNG from Mermaid code
   * @param {string} mermaidCode - Mermaid diagram code
   * @param {string} outputPath - Output PNG file path
   * @param {object} options - Additional options
   * @returns {Promise<boolean>} - True if successful
   */
  async generatePNG(mermaidCode, outputPath, options = {}) {
    const tempFile = path.join(this.tempDir, `diagram-${Date.now()}.mmd`);
    
    try {
      // Create temporary Mermaid file
      await fs.writeFile(tempFile, mermaidCode, 'utf8');
      
      // Ensure output directory exists
      await fs.ensureDir(path.dirname(outputPath));
      
      // Build command options
      const renderOptions = { ...this.options, ...options };
      const args = [
        `-i "${tempFile}"`,
        `-o "${outputPath}"`,
        `-b ${renderOptions.backgroundColor}`,
        `-t ${renderOptions.theme}`,
        `--width ${renderOptions.width}`,
        `--height ${renderOptions.height}`
      ];

      if (renderOptions.configFile) {
        args.push(`-c "${renderOptions.configFile}"`);
      }

      // Execute Mermaid CLI
      const command = `mmdc ${args.join(' ')}`;
      await execAsync(command, { timeout: 30000 });
      
      return true;
    } catch (error) {
      console.error(`Error generating diagram: ${error.message}`);
      return false;
    } finally {
      // Clean up temporary file
      await this.cleanupTempFile(tempFile);
    }
  }

  /**
   * Generate multiple PNGs from Mermaid code blocks
   * @param {object[]} diagramData - Array of {code, outputPath, name} objects
   * @param {function} progressCallback - Progress callback function
   * @returns {Promise<object>} - Generation results
   */
  async generateMultiplePNGs(diagramData, progressCallback = null) {
    const results = {
      successful: [],
      failed: [],
      total: diagramData.length
    };

    for (let i = 0; i < diagramData.length; i++) {
      const diagram = diagramData[i];
      
      if (progressCallback) {
        progressCallback(i + 1, results.total, diagram.name || diagram.outputPath);
      }

      const success = await this.generatePNG(diagram.code, diagram.outputPath, diagram.options);
      
      if (success) {
        results.successful.push(diagram);
      } else {
        results.failed.push(diagram);
      }
    }

    return results;
  }

  /**
   * Validate Mermaid syntax
   * @param {string} mermaidCode - Mermaid code to validate
   * @returns {Promise<boolean>} - True if valid
   */
  async validateMermaidSyntax(mermaidCode) {
    const tempFile = path.join(this.tempDir, `validate-${Date.now()}.mmd`);
    
    try {
      await fs.writeFile(tempFile, mermaidCode, 'utf8');
      
      // Try to parse the Mermaid file without generating output
      const command = `mmdc -i "${tempFile}" --parseMMDStr`;
      await execAsync(command, { timeout: 10000 });
      
      return true;
    } catch (error) {
      return false;
    } finally {
      await this.cleanupTempFile(tempFile);
    }
  }

  /**
   * Get Mermaid CLI version
   * @returns {Promise<string>} - Version string
   */
  async getVersion() {
    try {
      const { stdout } = await execAsync('mmdc --version', { timeout: 5000 });
      return stdout.trim();
    } catch (error) {
      throw new Error(`Failed to get Mermaid CLI version: ${error.message}`);
    }
  }

  /**
   * Check if Mermaid CLI is available
   * @returns {Promise<boolean>} - True if available
   */
  async isAvailable() {
    try {
      await this.getVersion();
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Generate PNG with hardcoded diagram data (fallback)
   * @param {string} diagramName - Diagram identifier
   * @param {string} outputPath - Output PNG file path
   * @param {object} hardcodedDiagrams - Hardcoded diagram definitions
   * @returns {Promise<boolean>} - True if successful
   */
  async generateWithFallback(diagramName, outputPath, hardcodedDiagrams) {
    if (!hardcodedDiagrams[diagramName]) {
      throw new Error(`No fallback diagram available for: ${diagramName}`);
    }

    return this.generatePNG(hardcodedDiagrams[diagramName], outputPath);
  }

  /**
   * Clean up temporary file
   * @param {string} tempFile - Temporary file path
   * @returns {Promise<void>}
   */
  async cleanupTempFile(tempFile) {
    try {
      if (await fs.pathExists(tempFile)) {
        await fs.unlink(tempFile);
      }
    } catch (error) {
      console.warn(`Failed to cleanup temp file ${tempFile}: ${error.message}`);
    }
  }

  /**
   * Clean up all temporary files
   * @returns {Promise<void>}
   */
  async cleanup() {
    try {
      if (await fs.pathExists(this.tempDir)) {
        await fs.emptyDir(this.tempDir);
      }
    } catch (error) {
      console.warn(`Failed to cleanup temp directory: ${error.message}`);
    }
  }

  /**
   * Create Mermaid config file for custom styling
   * @param {object} config - Mermaid configuration
   * @returns {Promise<string>} - Config file path
   */
  async createConfigFile(config = {}) {
    const defaultConfig = {
      theme: 'default',
      themeVariables: {
        primaryColor: '#ff0000'
      },
      flowchart: {
        htmlLabels: false
      }
    };

    const mergedConfig = { ...defaultConfig, ...config };
    const configPath = path.join(this.tempDir, 'mermaid-config.json');
    
    await fs.writeFile(configPath, JSON.stringify(mergedConfig, null, 2));
    
    return configPath;
  }
}