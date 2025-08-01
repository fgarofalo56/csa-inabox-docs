# Changelog

All notable changes to the Azure Synapse Analytics Documentation Project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-08-01

### Added

- Initial project structure and planning documentation
- Architecture documentation:
  - Delta Lakehouse overview
  - Detailed Delta Lakehouse architecture
  - Serverless SQL overview
  - Detailed Serverless SQL architecture
  - Shared Metadata overview
- Best practices overview document
- Code examples for:
  - Delta Lake operations
  - Serverless SQL queries
  - Integration patterns
- Diagrams documentation with architecture diagrams and flowcharts
- Reference documentation with detailed specifications and API references
- Project management files:
  - PLANNING.md
  - TASK.md
  - CHANGELOG.md
  - .ai-context
  - .gitignore

### Changed

- Organized project files according to established structure
- Moved planning files to project-planning directory

### Fixed

- Markdown formatting issues in documentation files

## [0.2.0] - 2025-08-02

### Fixed

- Updated all external Microsoft documentation links from docs.microsoft.com to learn.microsoft.com
- Fixed API reference links with updated paths
- Verified all internal file references exist (serverless-sql/index.md, shared-metadata/index.md, etc.)
- Updated diagram placeholders for architecture diagrams
- Added LICENSE file with MIT license
- Fixed markdown linting issues in security.md:
  - Added proper blank lines around all headings
  - Added blank lines around all lists
  - Added proper spacing before and after code blocks
  - Fixed first-line heading structure
  - Improved overall document formatting consistency

## [0.3.0] - 2025-08-05

### Added

- Implemented automated link checking via GitHub Actions workflow
  - Created `.github/workflows/link-checker.yml` configuration
  - Set up scheduled weekly checks (every Monday)
  - Added automated issue creation for broken link reports
  - Configured workflow to run on pushes, pull requests, and manual triggers
- Updated tools documentation with automated link checking information
- Fixed markdown linting issues across documentation files

## [Unreleased]

### Planned

- Integration with Azure DevOps for CI/CD
- Interactive demos and tutorials
- Performance benchmarks and recommendations
- Security best practices and compliance guides
