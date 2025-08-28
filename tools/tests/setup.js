/**
 * Test setup and global configuration
 */
import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Global test configuration
global.__TEST_TIMEOUT__ = 30000;
global.__TEST_ROOT__ = path.join(__dirname, '..');
global.__FIXTURES_DIR__ = path.join(__dirname, 'fixtures');
global.__TEMP_DIR__ = path.join(__dirname, 'temp');

// Setup test directories
beforeAll(async () => {
  // Ensure temp directory exists for tests
  await fs.ensureDir(global.__TEMP_DIR__);
  
  // Ensure fixtures directory exists
  await fs.ensureDir(global.__FIXTURES_DIR__);
});

// Cleanup after all tests
afterAll(async () => {
  // Clean up temp directory
  try {
    await fs.remove(global.__TEMP_DIR__);
  } catch (error) {
    console.warn('Failed to clean up temp directory:', error.message);
  }
});

// Mock console methods for cleaner test output
const originalConsole = { ...console };

beforeEach(() => {
  // Mock console methods to reduce noise in tests
  jest.spyOn(console, 'log').mockImplementation(() => {});
  jest.spyOn(console, 'info').mockImplementation(() => {});
  jest.spyOn(console, 'warn').mockImplementation(() => {});
  jest.spyOn(console, 'error').mockImplementation(() => {});
});

afterEach(() => {
  // Restore console methods
  console.log.mockRestore?.();
  console.info.mockRestore?.();
  console.warn.mockRestore?.();
  console.error.mockRestore?.();
});