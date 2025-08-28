/**
 * Unit tests for DocumentationFile domain model
 */
import { DocumentationFile } from '../../../src/domain/models/DocumentationFile.js';
import { SAMPLE_MARKDOWN_FILES } from '../../fixtures/sample-files.js';

describe('DocumentationFile', () => {
  describe('constructor', () => {
    test('should create instance with file path', () => {
      const file = new DocumentationFile('/test/README.md');
      
      expect(file.filePath).toBe('/test/README.md');
      expect(file.filename).toBe('README');
      expect(file.extension).toBe('.md');
      expect(file.directory).toBe('/test');
    });

    test('should create instance with content', () => {
      const content = '# Test\n\nContent here';
      const file = new DocumentationFile('/test/test.md', content);
      
      expect(file.content).toBe(content);
      expect(file.isEmpty).toBe(false);
    });
  });

  describe('content analysis', () => {
    test('should detect empty content', () => {
      const file = new DocumentationFile('/test/empty.md');
      file.setContent('');
      
      expect(file.isEmpty).toBe(true);
      expect(file.hasMinimalContent).toBe(false);
    });

    test('should detect minimal content', () => {
      const file = new DocumentationFile('/test/minimal.md');
      file.setContent('# Title');
      
      expect(file.isEmpty).toBe(false);
      expect(file.hasMinimalContent).toBe(true);
    });

    test('should detect sufficient content', () => {
      const file = new DocumentationFile('/test/full.md');
      file.setContent(SAMPLE_MARKDOWN_FILES['README.md']);
      
      expect(file.isEmpty).toBe(false);
      expect(file.hasMinimalContent).toBe(false);
    });
  });

  describe('link extraction', () => {
    test('should extract internal links', () => {
      const file = new DocumentationFile('/test/README.md');
      file.setContent(SAMPLE_MARKDOWN_FILES['README.md']);
      
      expect(file.links.length).toBeGreaterThan(0);
      
      const internalLinks = file.links.filter(link => 
        !link.url.startsWith('http') && !link.url.startsWith('#')
      );
      
      expect(internalLinks.length).toBeGreaterThan(0);
      expect(internalLinks[0]).toHaveProperty('text');
      expect(internalLinks[0]).toHaveProperty('url');
      expect(internalLinks[0]).toHaveProperty('line');
    });

    test('should ignore external links', () => {
      const content = '[External](https://example.com) and [Internal](./test.md)';
      const file = new DocumentationFile('/test/test.md');
      file.setContent(content);
      
      const externalLinks = file.links.filter(link => link.url.startsWith('http'));
      expect(externalLinks.length).toBe(0);
      
      const internalLinks = file.links.filter(link => !link.url.startsWith('http'));
      expect(internalLinks.length).toBe(1);
    });

    test('should ignore anchor links', () => {
      const content = '[Anchor](#section) and [File](./file.md)';
      const file = new DocumentationFile('/test/test.md');
      file.setContent(content);
      
      const anchorLinks = file.links.filter(link => link.url.startsWith('#'));
      expect(anchorLinks.length).toBe(0);
      
      const fileLinks = file.links.filter(link => !link.url.startsWith('#'));
      expect(fileLinks.length).toBe(1);
    });
  });

  describe('mermaid block extraction', () => {
    test('should extract mermaid blocks', () => {
      const file = new DocumentationFile('/test/with-mermaid.md');
      file.setContent(SAMPLE_MARKDOWN_FILES['README.md']);
      
      expect(file.mermaidBlocks.length).toBe(1);
      expect(file.mermaidBlocks[0]).toHaveProperty('content');
      expect(file.mermaidBlocks[0]).toHaveProperty('fullMatch');
      expect(file.mermaidBlocks[0]).toHaveProperty('line');
      expect(file.mermaidBlocks[0].content).toContain('graph TD');
    });

    test('should handle multiple mermaid blocks', () => {
      const content = `# Test

\`\`\`mermaid
graph TD
A --> B
\`\`\`

Some text

\`\`\`mermaid
sequenceDiagram
A->>B: Hello
\`\`\`
`;
      const file = new DocumentationFile('/test/multi-mermaid.md');
      file.setContent(content);
      
      expect(file.mermaidBlocks.length).toBe(2);
    });

    test('should handle no mermaid blocks', () => {
      const content = '# Test\n\nNo diagrams here.';
      const file = new DocumentationFile('/test/no-mermaid.md');
      file.setContent(content);
      
      expect(file.mermaidBlocks.length).toBe(0);
    });
  });

  describe('issue management', () => {
    test('should add and retrieve issues', () => {
      const file = new DocumentationFile('/test/test.md');
      
      file.addIssue('test-issue', 'Test issue description', { detail: 'value' });
      
      expect(file.hasIssues()).toBe(true);
      expect(file.issues.length).toBe(1);
      expect(file.issues[0]).toMatchObject({
        type: 'test-issue',
        description: 'Test issue description',
        details: { detail: 'value' },
        file: '/test/test.md'
      });
    });

    test('should get issues by type', () => {
      const file = new DocumentationFile('/test/test.md');
      
      file.addIssue('type-a', 'Issue A');
      file.addIssue('type-b', 'Issue B');
      file.addIssue('type-a', 'Another Issue A');
      
      const typeAIssues = file.getIssuesByType('type-a');
      expect(typeAIssues.length).toBe(2);
      
      const typeBIssues = file.getIssuesByType('type-b');
      expect(typeBIssues.length).toBe(1);
    });
  });

  describe('file type detection', () => {
    test('should detect markdown files', () => {
      const file = new DocumentationFile('/test/file.md');
      expect(file.isMarkdown()).toBe(true);
      
      const txtFile = new DocumentationFile('/test/file.txt');
      expect(txtFile.isMarkdown()).toBe(false);
    });

    test('should detect image files', () => {
      const pngFile = new DocumentationFile('/test/image.png');
      expect(pngFile.isImage()).toBe(true);
      
      const jpgFile = new DocumentationFile('/test/image.jpg');
      expect(jpgFile.isImage()).toBe(true);
      
      const mdFile = new DocumentationFile('/test/file.md');
      expect(mdFile.isImage()).toBe(false);
    });

    test('should detect diagram placeholder files', () => {
      const placeholder = new DocumentationFile('/test/diagram.png.md');
      expect(placeholder.isDiagramPlaceholder()).toBe(true);
      
      const regular = new DocumentationFile('/test/regular.md');
      expect(regular.isDiagramPlaceholder()).toBe(false);
    });
  });

  describe('serialization', () => {
    test('should serialize to JSON', () => {
      const file = new DocumentationFile('/test/test.md');
      file.setContent('# Test\n\n[Link](./other.md)');
      file.setRelativePath('test.md');
      file.addIssue('test', 'Test issue');
      
      const json = file.toJSON();
      
      expect(json).toHaveProperty('filePath', '/test/test.md');
      expect(json).toHaveProperty('relativePath', 'test.md');
      expect(json).toHaveProperty('filename', 'test');
      expect(json).toHaveProperty('extension', '.md');
      expect(json).toHaveProperty('linksCount', 1);
      expect(json).toHaveProperty('issuesCount', 1);
      expect(json).toHaveProperty('issues');
    });
  });

  describe('fluent interface', () => {
    test('should support method chaining', () => {
      const file = new DocumentationFile('/test/test.md')
        .setContent('# Test')
        .setRelativePath('test.md')
        .addIssue('test', 'Test issue');
      
      expect(file.content).toBe('# Test');
      expect(file.relativePath).toBe('test.md');
      expect(file.issues.length).toBe(1);
    });
  });
});