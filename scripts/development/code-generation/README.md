# 🏗️ Code and Content Generation Scripts

> **🏠 [Home](../../../README.md)** | **📚 [Documentation](../../../docs/README.md)** | **📜 [Scripts](../../README.md)** | **💻 [Development](../README.md)**

---

## 📋 Overview

This directory contains scripts for generating code, documentation templates, and automated content for the Cloud Scale Analytics (CSA) in-a-Box documentation project. These scripts help maintain consistency, reduce manual work, and ensure standardized documentation structure across the project.

## 🎯 Purpose

The code and content generation scripts are designed to:

- **Generate documentation templates** with consistent structure and metadata
- **Automate API documentation** creation from code and specifications
- **Create boilerplate content** for new documentation sections
- **Generate configuration files** with proper structure and validation
- **Maintain content consistency** through standardized templates
- **Update existing content** based on templates and data sources

## 📂 Current Scripts

### Available Scripts

Currently, no scripts exist in this directory. All scripts listed below are planned for implementation.

### Planned Scripts (To Be Created)

| Script | Purpose | Priority | Input Source |
|--------|---------|----------|--------------|
| `generate-doc-template.sh` | Create new documentation from templates | **HIGH** | Templates |
| `generate-api-docs.sh` | Generate API documentation from OpenAPI specs | **MEDIUM** | OpenAPI/Swagger |
| `generate-readme.sh` | Create standardized README files | **MEDIUM** | Templates |
| `generate-config-template.sh` | Create configuration file templates | **LOW** | JSON Schema |
| `update-toc.sh` | Update table of contents automatically | **MEDIUM** | File structure |
| `generate-changelog.sh` | Generate changelog from git history | **LOW** | Git commits |
| `generate-architecture-diagrams.sh` | Create diagrams from code/config | **LOW** | Code/Config |

## 🚀 Planned Script Details

### `generate-doc-template.sh` (Priority: HIGH)

**Purpose:** Generate new documentation files from standardized templates

**Features:**
- Support for multiple document types (guide, reference, tutorial, API)
- Customizable templates with metadata injection
- Automatic directory structure creation
- Template variable substitution
- Integration with project standards and style guides

**Planned Usage:**
```bash
./generate-doc-template.sh --type type --name name [--output-dir path] [--template template]

# Examples
./generate-doc-template.sh --type guide --name "azure-integration" --output-dir docs/guides/
./generate-doc-template.sh --type reference --name "api-reference" --template custom-api
./generate-doc-template.sh --type tutorial --name "getting-started" --author "John Doe"
```

**Template Types:**
```bash
Available Templates:
├── guide/           # How-to guides and procedures
├── reference/       # Reference documentation
├── tutorial/        # Step-by-step tutorials  
├── api/            # API documentation
├── architecture/   # Architecture documentation
├── troubleshooting/# Troubleshooting guides
└── custom/         # Custom templates
```

**Template Variables:**
```yaml
# Template variables for substitution
template_variables:
  title: "Document Title"
  author: "CSA Documentation Team"
  date: "2025-01-28"
  version: "1.0.0"
  category: "guides"
  tags: ["azure", "analytics", "documentation"]
  description: "Brief description of the document"
  audience: "developers" # developers, administrators, users
  difficulty: "intermediate" # beginner, intermediate, advanced
  estimated_time: "30 minutes"
```

### `generate-api-docs.sh` (Priority: MEDIUM)

**Purpose:** Generate comprehensive API documentation from OpenAPI specifications

**Features:**
- Parse OpenAPI/Swagger specifications
- Generate markdown documentation with examples
- Create interactive API documentation
- Support for multiple API versions
- Integration with existing documentation structure

**Planned Usage:**
```bash
./generate-api-docs.sh --spec-file path --output-dir path [--format format] [--include-examples]

# Examples
./generate-api-docs.sh --spec-file api/openapi.yml --output-dir docs/api/
./generate-api-docs.sh --spec-file api/v2/spec.json --format html --include-examples
```

**Generated Documentation Structure:**
```bash
docs/api/
├── overview.md          # API overview and getting started
├── authentication.md    # Authentication methods
├── endpoints/           # Individual endpoint documentation
│   ├── users.md
│   ├── data.md
│   └── analytics.md
├── schemas.md          # Data models and schemas
├── examples/           # Code examples and samples
└── changelog.md        # API version changelog
```

### `generate-readme.sh` (Priority: MEDIUM)

**Purpose:** Create standardized README files for directories and projects

**Features:**
- Template-based README generation
- Automatic content discovery and cataloging
- Navigation breadcrumb generation
- Standard section structure
- Integration with project metadata

**Planned Usage:**
```bash
./generate-readme.sh --directory path [--template template] [--update-existing]

# Examples
./generate-readme.sh --directory docs/guides/ --template directory-index
./generate-readme.sh --directory scripts/deployment/ --update-existing
```

**README Template Sections:**
```markdown
# Generated README Structure
1. Title and navigation breadcrumbs
2. Overview and purpose
3. Directory structure (if applicable)
4. Available content/scripts
5. Usage examples
6. Configuration (if applicable)
7. Related documentation
8. Contributing guidelines
9. Support information
```

### `update-toc.sh` (Priority: MEDIUM)

**Purpose:** Automatically update table of contents in documentation files

**Features:**
- Scan markdown files for heading structure
- Generate hierarchical table of contents
- Update existing TOC sections
- Support for multiple TOC formats (markdown, HTML)
- Integration with MkDocs navigation

**Planned Usage:**
```bash
./update-toc.sh --file path [--format format] [--max-depth level]

# Examples
./update-toc.sh --file docs/architecture/README.md --format markdown --max-depth 3
./update-toc.sh --directory docs/guides/ --update-all
```

## 🏗️ Template System

### Template Architecture

**Template Structure:**
```
templates/
├── documentation/           # Documentation templates
│   ├── guide.md.template
│   ├── reference.md.template
│   ├── tutorial.md.template
│   └── api.md.template
├── configuration/          # Configuration templates
│   ├── mkdocs.yml.template
│   ├── github-workflow.yml.template
│   └── docker.yml.template
└── code/                  # Code templates
    ├── python-script.py.template
    ├── shell-script.sh.template
    └── dockerfile.template
```

**Template Example:** `templates/documentation/guide.md.template`

```markdown
# {{title}}

> **🏠 [Home]({{home_path}})** | **📚 [Documentation]({{docs_path}})** | **{{breadcrumb}}**

---

## 📋 Overview

{{description}}

## 🎯 Purpose

This guide will help you:

- **{{purpose_1}}** - {{purpose_1_description}}
- **{{purpose_2}}** - {{purpose_2_description}}  
- **{{purpose_3}}** - {{purpose_3_description}}

## 📋 Prerequisites

Before following this guide, ensure you have:

- [ ] {{prerequisite_1}}
- [ ] {{prerequisite_2}}
- [ ] {{prerequisite_3}}

## 🚀 Step-by-Step Instructions

### Step 1: {{step_1_title}}

{{step_1_content}}

```{{step_1_code_language}}
{{step_1_code}}
```

### Step 2: {{step_2_title}}

{{step_2_content}}

## 🔍 Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|--------|----------|
| {{issue_1}} | {{cause_1}} | {{solution_1}} |
| {{issue_2}} | {{cause_2}} | {{solution_2}} |

## 📚 Related Documentation

- [{{related_doc_1}}]({{related_link_1}})
- [{{related_doc_2}}]({{related_link_2}})

## 🤝 Contributing

{{contributing_guidelines}}

---

**Last Updated:** {{date}}  
**Version:** {{version}}  
**Author:** {{author}}  
**Maintainer:** {{maintainer}}
```

### Template Variables System

**Variable Categories:**
```yaml
# Metadata variables
metadata:
  title: "Document title"
  author: "Author name"
  date: "Creation date" 
  version: "Document version"
  maintainer: "Maintainer contact"

# Navigation variables  
navigation:
  home_path: "../../README.md"
  docs_path: "../README.md"
  breadcrumb: "Category | Subcategory"

# Content variables
content:
  description: "Document description"
  purpose_1: "First purpose"
  purpose_2: "Second purpose"
  prerequisites: ["Prereq 1", "Prereq 2"]

# Structure variables
structure:
  sections: ["Overview", "Instructions", "Examples"]
  max_depth: 3
  include_toc: true
  include_troubleshooting: true

# Project variables
project:
  name: "CSA in-a-Box Documentation"
  repository: "csa-inabox-docs"
  team: "CSA Documentation Team"
```

## 🔧 Generation Configuration

### Configuration File

**Configuration File:** `config/generation.yml`

```yaml
# Content Generation Configuration
generation:
  # Template settings
  templates:
    base_path: "templates/"
    output_path: "generated/"
    
    # Default variables
    defaults:
      author: "CSA Documentation Team"
      maintainer: "CSA Documentation Team"
      version: "1.0.0"
      project: "CSA in-a-Box Documentation"
      
    # Template mappings
    types:
      guide:
        template: "documentation/guide.md.template"
        output_dir: "docs/guides/"
        
      reference:
        template: "documentation/reference.md.template"
        output_dir: "docs/reference/"
        
      api:
        template: "documentation/api.md.template"
        output_dir: "docs/api/"
  
  # API documentation
  api_docs:
    spec_formats: ["openapi", "swagger", "postman"]
    output_formats: ["markdown", "html", "json"]
    include_examples: true
    generate_client_code: false
    
  # README generation
  readme:
    auto_discovery: true
    include_navigation: true
    include_metrics: false
    
    sections:
      - "overview"
      - "structure" 
      - "usage"
      - "configuration"
      - "related"
      - "contributing"
  
  # Table of contents
  toc:
    max_depth: 4
    include_numbers: false
    format: "markdown"
    update_existing: true
    
  # Automation
  automation:
    auto_update_on_change: false
    git_integration: true
    pre_commit_hook: false
```

### Environment Variables

```bash
# Generation configuration
GENERATION_CONFIG_PATH=/path/to/config/generation.yml
TEMPLATES_PATH=/path/to/templates
OUTPUT_PATH=/path/to/generated

# Template defaults
DEFAULT_AUTHOR="CSA Documentation Team"
DEFAULT_VERSION="1.0.0"
DEFAULT_MAINTAINER="CSA Documentation Team"

# API documentation
API_SPEC_PATH=/path/to/api/specs
API_OUTPUT_PATH=/path/to/docs/api
INCLUDE_API_EXAMPLES=true

# Automation settings
AUTO_UPDATE_TOC=true
GIT_INTEGRATION=true
COMMIT_GENERATED_CONTENT=false
```

## 📊 Generation Metrics

### Content Generation Report

**Generation Summary:**
```
Content Generation Report - 2025-01-28

📊 Generation Statistics:
- Templates used: 8
- Files generated: 23  
- Content updated: 15
- Total processing time: 45s

Generated Content:
✅ Documentation:
   - Guides: 12 files (156KB)
   - References: 6 files (89KB)
   - Tutorials: 4 files (67KB)
   - API docs: 1 file (234KB)

✅ Configuration:
   - README files: 8 files (45KB)
   - TOC updates: 15 files
   - Config templates: 3 files (12KB)

Template Usage:
- guide.md.template: 12 uses
- reference.md.template: 6 uses  
- api.md.template: 1 use
- readme.md.template: 8 uses

Quality Metrics:
- Generated content passes linting: 100%
- All links valid: 98.7%
- Images accessible: 100%
- Consistent formatting: 100%

Issues:
- 3 external links need manual review
- 1 template variable needs updating

Next Generation: Scheduled for file changes
```

## 🔧 Advanced Features

### Dynamic Content Generation

**Data-Driven Templates:**
```yaml
# Data source for dynamic content
data_sources:
  api_endpoints: "api/endpoints.yml"
  configuration_options: "config/options.json"
  team_members: "data/team.csv"
  changelog: "git://commits"

# Dynamic template example
dynamic_templates:
  team_page:
    template: "team.md.template"
    data_source: "team_members"
    output: "docs/about/team.md"
    refresh: "weekly"
```

### Template Inheritance

**Base Template System:**
```markdown
<!-- base.md.template -->
# {{title}}

{{navigation_breadcrumbs}}

---

{{content}}

---

{{footer_metadata}}

<!-- guide.md.template extends base.md.template -->
{{extends "base.md.template"}}

{{block content}}
## 📋 Overview
{{description}}

{{guide_specific_content}}
{{endblock}}
```

### Integration with External Tools

**Tool Integrations:**
- **Swagger Codegen** - Generate client libraries from API specs
- **PlantUML** - Generate diagrams from text descriptions
- **Mermaid** - Create flowcharts and diagrams
- **JSON Schema** - Generate documentation from schemas
- **Git** - Extract information from commit history

## 🔍 Troubleshooting

### Common Generation Issues

| Issue | Symptoms | Cause | Solution |
|-------|----------|--------|----------|
| **Template not found** | Script fails with missing template | Template path incorrect | Check template path and existence |
| **Variable substitution fails** | Variables appear as {{var}} in output | Missing variable values | Check variable definitions and config |
| **Generated content invalid** | Linting fails on generated files | Template syntax issues | Fix template syntax and test generation |
| **Slow generation** | Scripts take too long to complete | Large templates or many files | Optimize templates and use parallel processing |
| **Encoding issues** | Special characters corrupted | Wrong file encoding | Ensure UTF-8 encoding for templates and output |

### Debug Commands

```bash
# Test template generation
./generate-doc-template.sh --type guide --name test --dry-run --verbose

# Validate template syntax
yamllint templates/config/*.yml.template
markdownlint templates/documentation/*.md.template

# Check variable substitution
grep -r "{{.*}}" generated/ # Should return no results if all variables substituted

# Verify generated content
./scripts/development/linting/lint-all.sh generated/
./scripts/development/testing/validate-examples.sh generated/
```

### Performance Optimization

**Generation Performance Tips:**
- **Use template caching** - Cache parsed templates for reuse
- **Parallel processing** - Generate multiple files simultaneously  
- **Incremental generation** - Only regenerate changed content
- **Optimize templates** - Minimize complex logic in templates
- **Batch operations** - Process multiple items in single script run

## 📚 Related Documentation

- [Template System Guide](../../../docs/guides/TEMPLATE_SYSTEM.md) *(planned)*
- [API Documentation Guide](../../../docs/guides/API_DOCUMENTATION.md) *(planned)*
- [Content Standards](../../../docs/guides/CONTENT_STANDARDS.md) *(planned)*
- [Development Scripts Overview](../README.md)
- [Testing Scripts Guide](../testing/README.md)

## 🤝 Contributing

### Adding New Generation Scripts

1. **Identify generation need** - Determine what content needs automation
2. **Design template structure** - Create flexible, reusable templates
3. **Implement variable system** - Support configurable content generation
4. **Add validation** - Ensure generated content meets quality standards
5. **Test thoroughly** - Test with various input scenarios and edge cases
6. **Document templates** - Document available templates and variables
7. **Update documentation** - Update this README with script details

### Script Requirements

- [ ] Supports multiple template types and formats
- [ ] Has comprehensive variable substitution system
- [ ] Includes template validation and error checking
- [ ] Generates valid, linting-compliant content
- [ ] Supports dry-run mode for testing
- [ ] Has configurable output paths and formats
- [ ] Includes comprehensive logging and progress reporting
- [ ] Is tested with various template configurations
- [ ] Integrates with existing development workflow
- [ ] Is documented in this README file

## 📞 Support

For code and content generation issues:

- **GitHub Issues:** [Create Generation Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?labels=code-generation,development)
- **Template Issues:** Check template syntax and variable definitions
- **Generation Errors:** Verify input data and configuration files
- **Content Quality:** Run linting tools on generated content
- **Performance Issues:** Check template complexity and file sizes
- **Team Contact:** CSA Documentation Team

---

**Last Updated:** January 28, 2025  
**Version:** 1.0.0  
**Maintainer:** CSA Documentation Team