/**
 * TypeScript definitions for CSA Documentation Tools
 */

export interface DocumentationFileData {
  filePath: string;
  relativePath?: string;
  directory: string;
  filename: string;
  extension: string;
  isEmpty: boolean;
  hasMinimalContent: boolean;
  links: LinkData[];
  mermaidBlocks: MermaidBlockData[];
  issues: IssueData[];
  content?: string;
}

export interface LinkData {
  text: string;
  url: string;
  line: number;
}

export interface MermaidBlockData {
  content: string;
  fullMatch: string;
  startIndex: number;
  line: number;
}

export interface IssueData {
  type: string;
  description: string;
  details: Record<string, any>;
  file: string;
  severity?: 'critical' | 'warning' | 'info';
}

export interface AuditReportData {
  timestamp: string;
  totalFiles: number;
  issues: {
    emptyFiles: IssueData[];
    brokenLinks: IssueData[];
    orphanedFiles: IssueData[];
    duplicateIndexReadme: IssueData[];
    missingContent: IssueData[];
    inaccessibleFiles: IssueData[];
    diagramIssues: IssueData[];
    customIssues: IssueData[];
  };
  summary: {
    totalIssues: number;
    criticalIssues: number;
    warningIssues: number;
    infoIssues: number;
  };
  recommendations: RecommendationData[];
  executiveSummary: ExecutiveSummaryData;
}

export interface RecommendationData {
  recommendation: string;
  priority: number;
  type: string;
}

export interface ExecutiveSummaryData {
  totalFiles: number;
  totalIssues: number;
  totalIssueTypes: number;
  criticalIssues: number;
  warningIssues: number;
  infoIssues: number;
  healthScore: number;
  timestamp: string;
}

export interface DiagramGenerationOptions {
  theme?: 'default' | 'dark' | 'forest' | 'neutral';
  backgroundColor?: string;
  width?: number;
  height?: number;
  configFile?: string;
}

export interface DiagramGenerationResult {
  successful: DiagramData[];
  failed: DiagramData[];
  total: number;
}

export interface DiagramData {
  name?: string;
  code: string;
  outputPath: string;
  options?: DiagramGenerationOptions;
}

export interface MermaidValidationResult {
  valid: ValidationResultItem[];
  invalid: ValidationResultItem[];
  total: number;
}

export interface ValidationResultItem {
  file: string;
  line: number;
  content?: string;
}

export interface FixResults {
  filesCreated: number;
  filesRemoved: number;
  linksUpdated: number;
  navigationUpdated: number;
  contentGenerated?: number;
}

export interface AuditOptions {
  fixDuplicates?: boolean;
  output?: 'text' | 'json';
  saveReport?: string;
  quickMode?: boolean;
}

export interface GenerationOptions extends DiagramGenerationOptions {
  inputDir?: string;
  outputDir?: string;
}

export interface ReplacementOptions {
  dryRun?: boolean;
  verbose?: boolean;
}

export interface FixOptions {
  createMissing?: boolean;
  fixLinks?: boolean;
  removeOrphans?: boolean;
  updateNav?: boolean;
  preserveDiagramFiles?: boolean;
}

export interface ValidationOptions {
  external?: boolean;
  timeout?: number;
  concurrent?: number;
}

export interface OptimizationOptions {
  quality?: number;
  maxWidth?: number;
  maxHeight?: number;
  format?: 'original' | 'webp' | 'auto';
}

export interface BuildOptions {
  skipAudit?: boolean;
  skipDiagrams?: boolean;
  skipFixes?: boolean;
  skipValidation?: boolean;
}

export interface StatusOptions {
  detailed?: boolean;
}

export interface GlobalCLIOptions {
  verbose?: boolean;
  color?: boolean;
  logFile?: string;
  docsDir?: string;
}

export interface LoggerOptions {
  level?: 'error' | 'warn' | 'info' | 'verbose' | 'debug';
  logFile?: string | null;
  colorize?: boolean;
  timestamp?: boolean;
}

export interface ProgressBarInterface {
  start: (totalItems: number, message?: string) => void;
  update: (currentItem: number, message?: string) => void;
  finish: (message?: string) => void;
  fail: (message?: string) => void;
}

export interface FileSystemStats {
  totalFiles: number;
  markdownFiles: number;
  imageFiles: number;
  directories: number;
}

// Service Interfaces
export interface IAuditService {
  runFullAudit(docsDir: string, options?: AuditOptions): Promise<AuditReportData>;
  autoFixIssues(report: AuditReportData, options?: FixOptions): Promise<FixResults>;
}

export interface IDiagramService {
  generateAllDiagrams(inputDir: string, outputDir?: string, options?: GenerationOptions): Promise<DiagramGenerationResult>;
  replaceMermaidWithPNG(docsDir: string, options?: ReplacementOptions): Promise<{ filesProcessed: number; replacements: number; formattingFixes: number }>;
  validateMermaidDiagrams(docsDir: string): Promise<MermaidValidationResult>;
}

export interface IFixService {
  runAllFixes(docsDir: string, options?: FixOptions): Promise<FixResults>;
}

export interface IFileRepository {
  findAllMarkdownFiles(dir?: string, excludeDirs?: string[]): Promise<DocumentationFileData[]>;
  findAllImageFiles(dir: string): Promise<string[]>;
  readFile(filePath: string): Promise<string>;
  writeFile(filePath: string, content: string): Promise<void>;
  fileExists(filePath: string): Promise<boolean>;
  deleteFile(filePath: string): Promise<void>;
  ensureDirectory(dirPath: string): Promise<void>;
}

export interface IMermaidRenderer {
  generatePNG(mermaidCode: string, outputPath: string, options?: DiagramGenerationOptions): Promise<boolean>;
  generateMultiplePNGs(diagramData: DiagramData[], progressCallback?: (current: number, total: number, name: string) => void): Promise<DiagramGenerationResult>;
  validateMermaidSyntax(mermaidCode: string): Promise<boolean>;
  isAvailable(): Promise<boolean>;
  getVersion(): Promise<string>;
}

export interface ILogger {
  info(message: string, meta?: object): void;
  warn(message: string, meta?: object): void;
  error(message: string, meta?: object): void;
  debug(message: string, meta?: object): void;
  verbose(message: string, meta?: object): void;
  success(message: string): void;
  failure(message: string): void;
  progress(message: string): void;
  section(title: string): void;
  subsection(title: string): void;
  summary(stats: Record<string, any>): void;
  table(data: object[], columns?: string[]): void;
  custom(emoji: string, message: string, color?: string): void;
  createProgressBar(title: string): ProgressBarInterface;
  setLevel(level: string): void;
  child(context: object): ILogger;
}

// Error Types
export declare class DocumentationToolsError extends Error {
  code?: string;
  details?: any;
  constructor(message: string, code?: string, details?: any);
}

export declare class FileSystemError extends DocumentationToolsError {
  filePath?: string;
  constructor(message: string, filePath?: string);
}

export declare class MermaidRenderError extends DocumentationToolsError {
  diagramName?: string;
  constructor(message: string, diagramName?: string);
}

export declare class ValidationError extends DocumentationToolsError {
  validationTarget?: string;
  constructor(message: string, validationTarget?: string);
}

// Configuration Types
export interface ToolsConfig {
  docsDir: string;
  logging: LoggerOptions;
  mermaid: DiagramGenerationOptions;
  audit: {
    excludeDirectories: string[];
    autoFix: boolean;
    healthScoreThreshold: number;
  };
  diagram: {
    inputDir: string;
    outputDir: string;
    fallbackDiagrams: Record<string, string>;
  };
  fix: {
    createMissingFiles: boolean;
    updateNavigation: boolean;
    removeOrphans: boolean;
  };
}

// Utility Types
export type Severity = 'critical' | 'warning' | 'info';
export type IssueType = 'emptyFiles' | 'brokenLinks' | 'orphanedFiles' | 'duplicateIndexReadme' | 'missingContent' | 'inaccessibleFiles' | 'diagramIssues' | 'customIssues';
export type OutputFormat = 'text' | 'json';
export type DiagramTheme = 'default' | 'dark' | 'forest' | 'neutral';
export type ImageFormat = 'original' | 'webp' | 'auto';

// Constants (Declare only for typing, actual values in implementation files)
export declare const SUPPORTED_IMAGE_EXTENSIONS: readonly string[];
export declare const SUPPORTED_MARKDOWN_EXTENSIONS: readonly string[];
export declare const DEFAULT_EXCLUDE_DIRECTORIES: readonly string[];
export declare const DEFAULT_DIAGRAM_THEMES: readonly DiagramTheme[];
export declare const LOG_LEVELS: readonly string[];

export default {};