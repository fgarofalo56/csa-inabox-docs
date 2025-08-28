/**
 * Main entry point for CSA Documentation Tools
 * Exports all public APIs for programmatic usage
 */

// Domain models
export { DocumentationFile } from './domain/models/DocumentationFile.js';
export { DiagramMapping } from './domain/models/DiagramMapping.js';
export { AuditReport } from './domain/models/AuditReport.js';

// Infrastructure
export { FileSystemRepository } from './infrastructure/FileSystemRepository.js';
export { MermaidRenderer } from './infrastructure/MermaidRenderer.js';
export { Logger } from './infrastructure/Logger.js';

// Services
export { DocumentationAuditService } from './services/DocumentationAuditService.js';
export { DiagramGenerationService } from './services/DiagramGenerationService.js';
export { DocumentationFixService } from './services/DocumentationFixService.js';

// Presentation
export { DocumentationToolsCLI } from './presentation/DocumentationToolsCLI.js';

// Types (if using TypeScript)
export * from './types/index.d.ts';