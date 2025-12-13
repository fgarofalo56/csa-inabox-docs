# GitHub Copilot Instructions for CSA in-a-Box Documentation

## Project Overview

This repository contains comprehensive technical documentation for the __Azure Cloud Scale Analytics (CSA) in-a-Box__ ecosystem. The documentation covers streaming services, analytics compute, storage solutions, and orchestration services designed for data engineers, architects, and developers implementing modern data platforms on Azure.

### Key Technologies

- __Documentation Framework__: MkDocs with Material theme
- __Markup Language__: GitHub Flavored Markdown (GFM) with Mermaid diagrams
- __Python Version__: 3.8+ (recommended 3.11+)
- __Testing__: pytest with comprehensive coverage
- __Linting__: markdownlint-cli, black, flake8, isort, mypy
- __CI/CD__: GitHub Actions workflows

## Repository Structure

```text
csa-inabox-docs/
├── docs/                    # All documentation content
│   ├── 01-overview/        # Overview and introduction
│   ├── 02-services/        # Azure services documentation
│   ├── 03-architecture-patterns/  # Architecture patterns
│   ├── 04-implementation-guides/  # Step-by-step guides
│   ├── 05-best-practices/  # Best practices and recommendations
│   ├── guides/             # Development and contribution guides
│   └── assets/             # Images, diagrams, and media
├── tests/                  # All test files
├── scripts/                # Utility and automation scripts
├── config/                 # Configuration files
├── examples/               # Example implementations (reference only)
├── project_tracking/       # Project management files
├── .github/                # GitHub workflows and templates
├── mkdocs.yml             # MkDocs configuration
├── requirements.txt       # Python dependencies
└── requirements-test.txt  # Testing dependencies
```

## Documentation Standards

### File Organization

1. __Use lowercase with hyphens__: `api-reference.md`, `user-guide.md`
2. __Be descriptive and specific__: `agent-configuration.md` not `config.md`
3. __Follow directory structure guide__: See `docs/guides/DIRECTORY_STRUCTURE_GUIDE.md`
4. __Each directory must have a README.md__: Serves as index for that section

### Markdown Style

- __Follow GitHub Flavored Markdown (GFM)__ standards
- __Use ATX-style headings__ (`#`) with space after hash
- __Only one H1 per document__
- __Use sentence case for headings__: `## Getting started` not `## Getting Started`
- __Add blank lines__ before and after lists, code blocks, and headings
- __Use `-` (hyphen)__ for unordered lists consistently
- __Include table of contents__ for documents longer than 3 sections
- __Add emoji__ for visual hierarchy (`:emoji:` format or Unicode)
- __Reference complete style guide__: `docs/guides/MARKDOWN_STYLE_GUIDE.md`

### Code and Examples

Use triple backticks with language identifier for all code blocks:

- Python: ` ```python ... ``` `
- SQL: ` ```sql ... ``` `
- Bash: ` ```bash ... ``` `
- YAML: ` ```yaml ... ``` `
- JSON: ` ```json ... ``` `

Example Python code block:

```python
# Python code example
def example_function():
    return "Hello, World!"
```

Example SQL code block:

```sql
-- SQL example
SELECT * FROM table_name WHERE condition = 'value';
```

### Visual Elements

- __Use Mermaid diagrams__ for architecture and flow diagrams
- __Store images__ in `docs/assets/images/`
- __Use relative paths__ for images: `![Alt text](../assets/images/example.png)`
- __Include alt text__ for all images for accessibility
- __Use admonitions__ for notes, warnings, tips:

```markdown
!!! note "Important Information"
    This is a note admonition.

!!! warning "Caution"
    This is a warning admonition.

!!! tip "Best Practice"
    This is a tip admonition.
```

## Development Workflow

### Setup Environment

```bash
# Clone repository
git clone https://github.com/fgarofalo56/csa-inabox-docs.git
cd csa-inabox-docs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### Local Development

```bash
# Serve documentation locally (opens browser at http://localhost:8000)
python project_tracking/tools/serve-docs.py

# Or use mkdocs directly
mkdocs serve

# Build documentation
mkdocs build --strict

# Run tests
pytest tests/

# Run linting
markdownlint '**/*.md'
black .
flake8
isort . --check-only
mypy .
```

### Before Committing

1. __Lint markdown files__: `markdownlint '**/*.md' --fix`
2. __Validate MkDocs config__: `mkdocs build --strict`
3. __Run tests__: `pytest tests/`
4. __Check internal links__: Use link-checker workflow
5. __Review changes__: Ensure only necessary files are committed

### Branch Strategy

- __main/master__: Production-ready documentation
- __develop__: Development branch for ongoing work
- __feature/__*: Feature branches for new documentation
- __fix/__*: Bug fix branches

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_specific.py

# Run with verbose output
pytest tests/ -v
```

### Test Structure

- __Unit tests__: `tests/unit/`
- __Integration tests__: `tests/integration/`
- __Documentation tests__: Validate links, structure, and formatting

## Common Patterns and Gotchas

### Azure Service Documentation

- __Always include service overview__ at the start of service docs
- __Provide architecture diagrams__ using Mermaid
- __Include code examples__ for key concepts
- __Reference official Microsoft docs__ where appropriate
- __Follow medallion architecture__ patterns (Bronze-Silver-Gold)

### Cross-References

```markdown
# Internal links (relative paths)
[See Architecture Patterns](../03-architecture-patterns/README.md)

# Section anchors
[Jump to Configuration](#configuration)

# External links
[Azure Documentation](https://learn.microsoft.com/en-us/azure/)
```

### Common Mistakes to Avoid

1. __Don't skip heading levels__: H1 → H3 (missing H2)
2. __Don't use absolute paths__ for internal links
3. __Don't forget alt text__ for images
4. __Don't hardcode URLs__ that might change
5. __Don't place test files__ in source directories
6. __Don't create duplicate documentation__ in multiple locations
7. __Don't skip markdown linting__ before committing

### Special Considerations

- __Delta Lake configuration__: Requires specific Spark session setup
- __Serverless SQL syntax__: Different from standard T-SQL
- __Time travel queries__: Different syntax between Spark SQL and Serverless SQL
- __Access control__: Must be configured at both Azure Storage and Synapse levels
- __Examples directory__: For reference only, not part of main codebase

## CI/CD Workflows

### Active GitHub Actions

- __ci.yml__: Validates documentation and runs linters
- __deploy-docs.yml__: Deploys documentation to GitHub Pages
- __documentation-tests.yml__: Comprehensive documentation testing
- __link-checker.yml__: Validates internal and external links
- __markdown-lint.yml__: Enforces markdown style standards
- __pr-validation.yml__: PR checks before merge

### Workflow Triggers

- __Push to main/master/develop__: Runs CI validation
- __Pull requests__: Runs validation and testing
- __Manual dispatch__: Can be triggered manually via workflow_dispatch

## AI Coding Agent Guidance

### For Claude Code and AI Assistants

If you are an AI coding agent (like Claude Code), please also reference:

- __CLAUDE.md__: Comprehensive rules for AI agent development
- __docs/guides/CONTRIBUTING.md__: Contribution guidelines
- __docs/guides/DEVELOPMENT_GUIDE.md__: Detailed development instructions
- __docs/guides/CODE_REVIEW_GUIDE.md__: Code review standards

### Key AI Agent Rules

1. __ALWAYS follow documentation standards__ from `docs/guides/MARKDOWN_STYLE_GUIDE.md`
2. __CHECK directory structure__ before creating files using `docs/guides/DIRECTORY_STRUCTURE_GUIDE.md`
3. __NEVER create documentation__ without running markdownlint
4. __ALWAYS use Azure-first patterns__ for cloud services
5. __MAINTAIN clean architecture__ separation of concerns
6. __INCLUDE proper structure, formatting, and visual elements__
7. __RUN linting and tests__ before committing changes
8. __FOLLOW task management__ practices in `project_tracking/`

## Quick Reference

### Important Files

- __CLAUDE.md__: Global rules for AI agent development
- __README.md__: Project overview and getting started
- __mkdocs.yml__: MkDocs configuration
- __pyproject.toml__: Python project configuration
- __.markdownlint.json__: Markdown linting rules
- __.pre-commit-config.yaml__: Pre-commit hooks configuration

### Key Commands

```bash
# Development
mkdocs serve                          # Serve docs locally
mkdocs build --strict                 # Build with strict mode

# Testing
pytest tests/                         # Run all tests
pytest tests/ --cov                   # Run with coverage

# Linting
markdownlint '**/*.md' --fix          # Fix markdown issues
black .                               # Format Python code
flake8                                # Check Python code style
isort . --check-only                  # Check import sorting

# Git
git status                            # Check status
git diff                              # View changes
git add .                             # Stage all changes
git commit -m "message"               # Commit changes
git push origin branch-name           # Push to remote
```

### Documentation Ports

- __MkDocs Dev Server__: 8000 (default for both `mkdocs serve` and `serve-docs.py`)
- __UI__: 3737 (from general Azure agent architecture)
- __Server API__: 8181 (from general Azure agent architecture)
- __MCP Server__: 8056 (from general Azure agent architecture)
- __Agents__: 8052 (from general Azure agent architecture)

Note: This documentation project primarily uses MkDocs on port 8000. Other ports listed are from the general Azure AI agent architecture referenced in CLAUDE.md.

## Resources

### Official Documentation

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Mermaid Diagrams](https://mermaid.js.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)
- [Azure Documentation](https://learn.microsoft.com/en-us/azure/)
- [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)

### Internal Guides

- [Markdown Style Guide](docs/guides/MARKDOWN_STYLE_GUIDE.md)
- [Directory Structure Guide](docs/guides/DIRECTORY_STRUCTURE_GUIDE.md)
- [Development Guide](docs/guides/DEVELOPMENT_GUIDE.md)
- [Contributing Guide](docs/guides/CONTRIBUTING.md)
- [Testing Guide](docs/guides/TESTING_GUIDE.md)
- [Code Review Guide](docs/guides/CODE_REVIEW_GUIDE.md)

## Contact and Support

For questions or issues:

1. __Check existing documentation__ in `docs/guides/`
2. __Review issue templates__ in `.github/ISSUE_TEMPLATE/`
3. __Create an issue__ using appropriate template
4. __Submit a pull request__ following PR template

---

__Note__: This file provides instructions for GitHub Copilot and other AI coding assistants. For comprehensive project rules and standards, always reference __CLAUDE.md__ and the guides in __docs/guides/__ directory.
