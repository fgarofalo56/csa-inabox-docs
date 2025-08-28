/**
 * Unit tests for FileSystemRepository infrastructure
 */
import { FileSystemRepository } from '../../../src/infrastructure/FileSystemRepository.js';
import { createTempDir, createTempFile, SAMPLE_MARKDOWN_FILES } from '../../fixtures/sample-files.js';
import fs from 'fs-extra';
import path from 'path';

describe('FileSystemRepository', () => {
  let repository;
  let tempDir;

  beforeEach(async () => {
    tempDir = await createTempDir(`test-${Date.now()}`);
    repository = new FileSystemRepository(tempDir);
  });

  afterEach(async () => {
    if (await fs.pathExists(tempDir)) {
      await fs.remove(tempDir);
    }
  });

  describe('constructor', () => {
    test('should initialize with root directory', () => {
      expect(repository.rootDir).toBe(tempDir);
    });

    test('should use current directory as default', () => {
      const defaultRepo = new FileSystemRepository();
      expect(defaultRepo.rootDir).toBe(process.cwd());
    });
  });

  describe('file operations', () => {
    test('should read file content', async () => {
      const content = 'Test file content';
      const filePath = await createTempFile('test.txt', content);

      const result = await repository.readFile(filePath);
      expect(result).toBe(content);
    });

    test('should write file content', async () => {
      const filePath = path.join(tempDir, 'new-file.txt');
      const content = 'New file content';

      await repository.writeFile(filePath, content);

      const written = await fs.readFile(filePath, 'utf8');
      expect(written).toBe(content);
    });

    test('should write file with directory creation', async () => {
      const filePath = path.join(tempDir, 'subdir', 'deep', 'file.txt');
      const content = 'Deep file content';

      await repository.writeFile(filePath, content);

      expect(await fs.pathExists(filePath)).toBe(true);
      const written = await fs.readFile(filePath, 'utf8');
      expect(written).toBe(content);
    });

    test('should check file existence', async () => {
      const existingFile = await createTempFile('existing.txt', 'content');
      const nonExistentFile = path.join(tempDir, 'nonexistent.txt');

      const existsResult = await repository.fileExists(existingFile);
      const notExistsResult = await repository.fileExists(nonExistentFile);

      expect(existsResult).toBe(true);
      expect(notExistsResult).toBe(false);
    });

    test('should delete file', async () => {
      const filePath = await createTempFile('to-delete.txt', 'content');

      expect(await repository.fileExists(filePath)).toBe(true);

      await repository.deleteFile(filePath);

      expect(await repository.fileExists(filePath)).toBe(false);
    });

    test('should handle file operation errors', async () => {
      // Test read error
      await expect(repository.readFile('/nonexistent/file.txt'))
        .rejects.toThrow(/Failed to read file/);

      // Test delete error
      await expect(repository.deleteFile('/nonexistent/file.txt'))
        .rejects.toThrow(/Failed to delete file/);
    });
  });

  describe('directory operations', () => {
    test('should ensure directory exists', async () => {
      const dirPath = path.join(tempDir, 'new', 'directory', 'structure');

      await repository.ensureDirectory(dirPath);

      expect(await fs.pathExists(dirPath)).toBe(true);
    });

    test('should list directory contents', async () => {
      // Create test files and directories
      await createTempFile('file1.txt', 'content1');
      await createTempFile('file2.md', 'content2');
      await fs.ensureDir(path.join(tempDir, 'subdir'));

      const contents = await repository.listDirectory(tempDir);

      expect(contents).toContain('file1.txt');
      expect(contents).toContain('file2.md');
      expect(contents).toContain('subdir');
    });

    test('should get file stats', async () => {
      const filePath = await createTempFile('stats-test.txt', 'content');

      const stats = await repository.getFileStats(filePath);

      expect(stats.isFile()).toBe(true);
      expect(stats.size).toBeGreaterThan(0);
    });
  });

  describe('markdown file discovery', () => {
    test('should find all markdown files', async () => {
      // Create test structure
      await createTempFile('README.md', SAMPLE_MARKDOWN_FILES['README.md']);
      await createTempFile('guide.md', SAMPLE_MARKDOWN_FILES['guide.md']);
      await createTempFile('docs/architecture.md', '# Architecture');
      await createTempFile('other.txt', 'Not markdown');

      const files = await repository.findAllMarkdownFiles();

      expect(files.length).toBe(3);
      files.forEach(file => {
        expect(file.extension).toBe('.md');
        expect(file.content).toBeDefined();
        expect(file.relativePath).toBeDefined();
      });
    });

    test('should exclude specified directories', async () => {
      // Create files in excluded directories
      await createTempFile('README.md', '# Root');
      await createTempFile('node_modules/package.md', '# Package');
      await createTempFile('.git/info.md', '# Git');

      const files = await repository.findAllMarkdownFiles();

      expect(files.length).toBe(1);
      expect(files[0].filename).toBe('README');
    });

    test('should handle empty directories', async () => {
      const files = await repository.findAllMarkdownFiles();
      expect(files).toEqual([]);
    });
  });

  describe('image file discovery', () => {
    test('should find all image files', async () => {
      // Create test images
      await createTempFile('image1.png', 'fake png data');
      await createTempFile('image2.jpg', 'fake jpg data');
      await createTempFile('docs/diagram.svg', 'fake svg data');
      await createTempFile('other.txt', 'not an image');

      const images = await repository.findAllImageFiles(tempDir);

      expect(images.length).toBe(3);
      expect(images.some(img => img.endsWith('.png'))).toBe(true);
      expect(images.some(img => img.endsWith('.jpg'))).toBe(true);
      expect(images.some(img => img.endsWith('.svg'))).toBe(true);
    });
  });

  describe('duplicate file detection', () => {
    test('should find duplicate index/README files', async () => {
      // Create duplicates in subdirectories
      await createTempFile('docs/README.md', '# Docs README');
      await createTempFile('docs/index.md', '# Docs Index');
      await createTempFile('guides/README.md', '# Guides README');
      // No index.md in guides - should not be detected

      const duplicates = await repository.findDuplicateFiles(tempDir);

      expect(duplicates.length).toBe(1);
      expect(duplicates[0].directory).toContain('docs');
      expect(duplicates[0].files.length).toBe(2);
    });

    test('should handle directories without duplicates', async () => {
      await createTempFile('docs/README.md', '# Docs');
      await createTempFile('guides/index.md', '# Guides');

      const duplicates = await repository.findDuplicateFiles(tempDir);
      expect(duplicates.length).toBe(0);
    });
  });

  describe('path utilities', () => {
    test('should get relative path between files', () => {
      const fromPath = '/docs/guides/guide.md';
      const toPath = '/docs/images/diagram.png';

      const relativePath = repository.getRelativePath(fromPath, toPath);

      expect(relativePath).toBe('../images/diagram.png');
    });

    test('should resolve link paths', () => {
      repository.rootDir = '/project';
      const sourcePath = '/project/docs/guide.md';

      // Test relative path
      const relativePath = repository.resolveLinkPath(sourcePath, './images/diagram.png');
      expect(relativePath).toBe(path.resolve('/project/docs/images/diagram.png'));

      // Test absolute path
      const absolutePath = repository.resolveLinkPath(sourcePath, '/images/root-diagram.png');
      expect(absolutePath).toBe('/project/images/root-diagram.png');
    });

    test('should find possible paths for links', async () => {
      // Create test files that could be link targets
      await createTempFile('guide.md', '# Guide');
      await createTempFile('docs/README.md', '# Docs');

      const targetPath = path.join(tempDir, 'guide');
      const possiblePaths = await repository.findPossiblePaths(targetPath);

      expect(possiblePaths.length).toBeGreaterThan(0);
      expect(possiblePaths.some(p => p.endsWith('guide.md'))).toBe(true);
    });

    test('should handle anchor fragments in paths', async () => {
      await createTempFile('guide.md', '# Guide');

      const targetPath = path.join(tempDir, 'guide#section');
      const possiblePaths = await repository.findPossiblePaths(targetPath);

      expect(possiblePaths.length).toBeGreaterThan(0);
    });
  });

  describe('file copying', () => {
    test('should copy file to new location', async () => {
      const sourceFile = await createTempFile('source.txt', 'source content');
      const targetFile = path.join(tempDir, 'subdir', 'target.txt');

      await repository.copyFile(sourceFile, targetFile);

      expect(await fs.pathExists(targetFile)).toBe(true);
      const targetContent = await fs.readFile(targetFile, 'utf8');
      expect(targetContent).toBe('source content');
    });

    test('should handle copy errors gracefully', async () => {
      const nonExistentSource = path.join(tempDir, 'nonexistent.txt');
      const targetFile = path.join(tempDir, 'target.txt');

      await expect(repository.copyFile(nonExistentSource, targetFile))
        .rejects.toThrow(/Failed to copy file/);
    });
  });

  describe('error handling', () => {
    test('should provide descriptive error messages', async () => {
      const invalidPath = '/invalid/path/file.txt';

      await expect(repository.readFile(invalidPath))
        .rejects.toThrow(`Failed to read file ${invalidPath}`);

      await expect(repository.getFileStats(invalidPath))
        .rejects.toThrow(`Failed to get stats for ${invalidPath}`);
    });

    test('should handle permission errors', async () => {
      // This test might be skipped on systems where we can't create permission issues
      const restrictedDir = path.join(tempDir, 'restricted');
      await fs.ensureDir(restrictedDir);

      try {
        await fs.chmod(restrictedDir, 0o000); // Remove all permissions
        
        await expect(repository.listDirectory(restrictedDir))
          .rejects.toThrow(/Failed to list directory/);
      } catch (error) {
        // Skip test if we can't modify permissions
        if (error.code === 'EPERM' || error.code === 'EACCES') {
          console.warn('Skipping permission test - insufficient privileges');
        } else {
          throw error;
        }
      } finally {
        try {
          await fs.chmod(restrictedDir, 0o755); // Restore permissions for cleanup
        } catch {
          // Ignore cleanup errors
        }
      }
    });
  });
});