/**
 * Domain model representing a documentation file
 * Pure business logic with no external dependencies
 */
import path from 'path';

export class DocumentationFile {
  constructor(filePath, content = null) {
    this.filePath = filePath;
    this.content = content;
    this.relativePath = null;
    this.directory = null;
    this.filename = null;
    this.extension = null;
    this.isEmpty = false;
    this.hasMinimalContent = false;
    this.links = [];
    this.mermaidBlocks = [];
    this.issues = [];
    this._parseFilePath();
  }

  _parseFilePath() {
    this.directory = path.dirname(this.filePath);
    this.filename = path.basename(this.filePath, path.extname(this.filePath));
    this.extension = path.extname(this.filePath);
  }

  setContent(content) {
    this.content = content;
    this._analyzeContent();
    return this;
  }

  setRelativePath(relativePath) {
    this.relativePath = relativePath;
    return this;
  }

  _analyzeContent() {
    if (!this.content) return;

    const trimmedContent = this.content.trim();
    const lines = trimmedContent.split('\n').filter(line => line.trim() !== '');

    // Check if empty
    this.isEmpty = trimmedContent.length === 0;

    // Check if minimal content
    this.hasMinimalContent = trimmedContent.length < 50 || lines.length <= 2;

    // Extract links
    this.links = this._extractLinks();

    // Extract mermaid blocks
    this.mermaidBlocks = this._extractMermaidBlocks();
  }

  _extractLinks() {
    if (!this.content) return [];

    const links = [];
    const markdownLinkRegex = /\[([^\]]*)\]\(([^)]+)\)/g;
    let match;

    while ((match = markdownLinkRegex.exec(this.content)) !== null) {
      const linkText = match[1];
      const linkUrl = match[2];

      // Skip external links, anchors, and email links
      if (!linkUrl.startsWith('http') && !linkUrl.startsWith('#') && !linkUrl.startsWith('mailto:')) {
        links.push({
          text: linkText,
          url: linkUrl,
          line: this.content.substring(0, match.index).split('\n').length
        });
      }
    }

    return links;
  }

  _extractMermaidBlocks() {
    if (!this.content) return [];

    const blocks = [];
    const mermaidRegex = /```mermaid\n([\s\S]*?)\n```/g;
    let match;

    while ((match = mermaidRegex.exec(this.content)) !== null) {
      blocks.push({
        content: match[1].trim(),
        fullMatch: match[0],
        startIndex: match.index,
        line: this.content.substring(0, match.index).split('\n').length
      });
    }

    return blocks;
  }

  addIssue(type, description, details = {}) {
    this.issues.push({
      type,
      description,
      details,
      file: this.filePath
    });
    return this;
  }

  hasIssues() {
    return this.issues.length > 0;
  }

  getIssuesByType(type) {
    return this.issues.filter(issue => issue.type === type);
  }

  isMarkdown() {
    return this.extension === '.md';
  }

  isImage() {
    const imageExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'];
    return imageExtensions.includes(this.extension.toLowerCase());
  }

  isDiagramPlaceholder() {
    return this.filename.endsWith('.png') && this.extension === '.md';
  }

  toJSON() {
    return {
      filePath: this.filePath,
      relativePath: this.relativePath,
      directory: this.directory,
      filename: this.filename,
      extension: this.extension,
      isEmpty: this.isEmpty,
      hasMinimalContent: this.hasMinimalContent,
      linksCount: this.links.length,
      mermaidBlocksCount: this.mermaidBlocks.length,
      issuesCount: this.issues.length,
      issues: this.issues
    };
  }
}