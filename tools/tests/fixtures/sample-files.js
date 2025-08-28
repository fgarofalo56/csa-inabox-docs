/**
 * Sample files and content for testing
 */

export const SAMPLE_MARKDOWN_FILES = {
  'README.md': `# Test Documentation

This is a test README file with [internal link](./guide.md) and [broken link](./missing.md).

## Features

- Feature 1
- Feature 2
- Feature 3

## Diagram Example

\`\`\`mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]
\`\`\`

## Links

- [Valid internal link](./guide.md)
- [External link](https://example.com)
- [Broken internal link](./nonexistent.md)
`,

  'guide.md': `# User Guide

[Home](./README.md)

## Getting Started

This guide shows how to get started.

### Prerequisites

- Requirement 1
- Requirement 2

### Installation

Follow these steps...
`,

  'empty.md': '',

  'minimal.md': '# Title',

  'index.md': `# Index

This is an index file in the same directory as README.md
`,

  'architecture/README.md': `# Architecture

## Overview

System architecture documentation.

## Diagrams

\`\`\`mermaid
graph LR
    A[Client] --> B[Server]
    B --> C[Database]
\`\`\`
`,

  'images/diagrams/test-diagram.png.md': `# Test Diagram

\`\`\`mermaid
graph TD
    START[Start Process]
    PROCESS[Processing]
    END[End Process]
    
    START --> PROCESS
    PROCESS --> END
\`\`\`
`
};

export const SAMPLE_MERMAID_DIAGRAMS = {
  'simple-flowchart': `graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E`,

  'sequence-diagram': `sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello Bob
    B-->>A: Hello Alice`,

  'invalid-syntax': `graph TD
    A[Start] --> B[
    Missing closing bracket`,

  'integrated-data-governance': `graph TD
    subgraph "Governance Foundations"
        POLICY[Governance Policies]
        STANDARD[Data Standards]
        ROLES[Roles & Responsibilities]
    end
    
    subgraph "Azure Synapse Analytics"
        WORKSPACE[Synapse Workspace]
        SQLPOOL[Dedicated SQL Pool]
        SERVERLESS[Serverless SQL Pool]
    end
    
    POLICY --> WORKSPACE
    STANDARD --> SQLPOOL`
};

export const SAMPLE_BROKEN_LINKS = [
  {
    file: 'README.md',
    links: [
      { text: 'Missing Guide', url: './missing-guide.md', line: 5 },
      { text: 'Broken External', url: '/nonexistent/path.md', line: 8 }
    ]
  },
  {
    file: 'guide.md', 
    links: [
      { text: 'Missing Section', url: '../missing-section.md', line: 12 }
    ]
  }
];

export const SAMPLE_AUDIT_ISSUES = {
  emptyFiles: [
    { file: '/test/empty.md', reason: 'Completely empty file' }
  ],
  brokenLinks: [
    {
      sourceFile: '/test/README.md',
      linkText: 'Missing Guide',
      linkUrl: './missing-guide.md',
      line: 5,
      targetPath: '/test/missing-guide.md'
    }
  ],
  orphanedFiles: [
    { file: '/test/orphaned.md', relativePath: 'orphaned.md' }
  ],
  duplicateIndexReadme: [
    {
      directory: '/test/',
      files: ['/test/index.md', '/test/README.md']
    }
  ]
};

export const createTempFile = async (fileName, content) => {
  const fs = await import('fs-extra');
  const path = await import('path');
  
  const filePath = path.join(global.__TEMP_DIR__, fileName);
  await fs.ensureDir(path.dirname(filePath));
  await fs.writeFile(filePath, content);
  return filePath;
};

export const createTempDir = async (dirName) => {
  const fs = await import('fs-extra');
  const path = await import('path');
  
  const dirPath = path.join(global.__TEMP_DIR__, dirName);
  await fs.ensureDir(dirPath);
  return dirPath;
};

export const createSampleFileStructure = async () => {
  const tempDir = await createTempDir('sample-docs');
  
  for (const [fileName, content] of Object.entries(SAMPLE_MARKDOWN_FILES)) {
    const filePath = path.join(tempDir, fileName);
    await fs.ensureDir(path.dirname(filePath));
    await fs.writeFile(filePath, content);
  }
  
  return tempDir;
};