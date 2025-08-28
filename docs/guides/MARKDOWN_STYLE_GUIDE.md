# 📝 Markdown Style Guide

This document defines the visual and structural standards for all markdown files.

## 📋 Table of Contents

- [File Organization](#file-organization)
- [Markdown Flavors](#markdown-flavors)
- [Formatting Standards](#formatting-standards)
- [Content Guidelines](#content-guidelines)
- [Code Documentation](#code-documentation)
- [Visual Elements](#visual-elements)
- [Images & Media](#images--media)
- [Cross-References](#cross-references)
- [Special Content](#special-content)
- [SEO & Discoverability](#seo--discoverability)
- [Testing & Validation](#testing--validation)
- [Automation & Enforcement](#automation--enforcement)
- [Templates](#templates)
- [Review Checklist](#review-checklist)
- [Additional Resources](#additional-resources)

## 📁 File Organization

### **File Naming**

- Use lowercase with hyphens: `api-reference.md`, `user-guide.md`
- Be descriptive and specific: `agent-configuration.md` not `config.md`
- Use consistent prefixes for related files: `test-unit.md`, `test-integration.md`
- Include version in filename when needed: `api-v2.md`, `migration-guide-v3.md`

### **Directory Structure**

```
docs/
├── api/              # API documentation
├── architecture/     # System design docs
├── guides/          # User and developer guides
├── diagrams/        # Visual documentation
├── assets/          # Images and media files
│   └── images/      # Screenshot and diagram storage
├── deployment/      # Deployment guides
├── changelog/       # Version history and changes
└── troubleshooting/ # Problem-solving docs
```

### **File Headers**

All markdown files should start with:

```markdown
# Document Title

Brief description of the document's purpose (1-2 sentences).

## Table of Contents
- [Section 1](#section-1)
- [Section 2](#section-2)
```

## 📋 Markdown Flavors

This guide follows **GitHub Flavored Markdown (GFM)** with these extensions:

- Task lists: `- [ ]` and `- [x]`
- Strikethrough: `~~text~~`
- Tables (with alignment support)
- Autolinked URLs
- Syntax highlighting in code blocks
- Emoji support via shortcodes `:emoji:` or Unicode
- Collapsible sections with `<details>` tags
- Mermaid diagram support

## 🎨 Formatting Standards

### **Headings**

- Use ATX style (`#`) with space after hash
- Only one H1 per document
- Don't skip heading levels
- Use sentence case: `## Getting started` not `## Getting Started`

```markdown
# Main Title (H1)
## Section Title (H2)
### Subsection Title (H3)
#### Detail Section (H4)
```

### **Lists**

- **Unordered**: Use `-` (hyphen) consistently
- **Ordered**: Use `1.` format with auto-numbering
- Add blank line before and after lists
- Use consistent indentation (2 spaces)

```markdown
## Features

- Feature one with description
- Feature two with description
  - Sub-feature with 2-space indent
  - Another sub-feature

## Steps

1. First step
2. Second step
   1. Sub-step with 3-space indent
   2. Another sub-step
```

### **Emphasis**

- **Bold**: Use `**text**` for important terms
- *Italic*: Use `*text*` for emphasis
- `Code`: Use backticks for inline code, filenames, commands
- ~~Strikethrough~~: Use `~~text~~` for deprecated items

### **Links**

- Use descriptive link text: `[API documentation](api.md)` not `[here](api.md)`
- Use reference-style for repeated URLs:

```markdown
Check the [official docs][anthropic] and [API reference][anthropic].

[anthropic]: https://docs.anthropic.com
```

### **Code Blocks**

- Always specify language for syntax highlighting
- Use descriptive comments
- Keep examples concise but complete

```python
# Good: Complete example with context
async def process_slides(slides: List[Slide]) -> ProcessingResult:
    """Process slides with error handling."""
    try:
        return await processor.process(slides)
    except ProcessingError as e:
        logger.error("Processing failed", error=str(e))
        raise
```

### **Inline Code vs Code Blocks**

**Use inline code for:**

- Single commands: `npm install`
- File/directory names: `src/main.py`
- Function names: `processData()`
- Short config values: `DEBUG=true`
- Package names: `pandas`, `react-router`

**Use code blocks for:**

- Multi-line code
- Complete examples
- Configuration files
- Command sequences
- Complex expressions

### **Enhanced Table Formatting**

#### Standard Table Structure

```markdown
| Column 1     | Column 2       | Column 3      |
| :----------- | :------------- | :------------ |
| Left-aligned | Center content | Right info    |
| Use icons 🎯  | Add badges     | Include links |
```

#### Feature Comparison Tables

```markdown
| Feature | Basic | Premium | Enterprise |
| :------ | :---: | :-----: | :--------: |
| Users   |  10   |   100   | Unlimited  |
| Storage |  1GB  |  10GB   |   100GB    |
| Support |   ❌   |    ✅    |     ✅      |
```

#### API Parameter Tables

| Parameter | Type        | Required | Description                       |
| --------- | ----------- | -------- | --------------------------------- |
| `slides`  | List[Slide] | ✅ Yes    | Input slides to process           |
| `theme`   | str         | ❌ No     | Theme name (default: "corporate") |

### **Line Length**

- Maximum 100 characters for prose
- Exceptions:
  - Tables
  - Long URLs (use reference-style when possible)
  - Code blocks
  - Badge definitions

## 📖 Content Guidelines

### **Writing Style**

- **Voice**: Use active voice when possible
- **Tense**: Present tense for instructions, past tense for examples
- **Person**: Second person for user-facing docs ("you"), first person plural for team docs ("we")
- **Tone**: Professional but approachable

### **Structure**

- Start with overview/summary
- Use progressive disclosure (general → specific)
- Include practical examples
- End with next steps or related links

### **Terminology**

- Use consistent terms throughout project
- Define acronyms on first use: "Large Language Model (LLM)"
- Maintain glossary for complex terms

### **Examples**

- Include realistic, working examples
- Show both success and error cases
- Provide context for when to use each approach

## 💻 Code Documentation

### **API Documentation**

```markdown
### `generate_presentation(markdown_path, **kwargs)`

Generate presentation from markdown file.

**Parameters:**
- `markdown_path` (str): Path to input markdown file
- `output_path` (str, optional): Output file path. Defaults to auto-generated name
- `theme` (str, default="corporate"): Presentation theme
- `max_slides` (int, default=100): Maximum number of slides

**Returns:**
- `str`: Path to generated presentation file

**Raises:**
- `FileNotFoundError`: If input file doesn't exist
- `ValidationError`: If markdown is malformed

**Example:**
```python
# Basic usage
output = await generator.generate("presentation.md")

# With custom options
output = await generator.generate(
    "presentation.md",
    theme="academic",
    max_slides=25,
    output_path="custom_output.pptx"
)
```

```

### **Configuration Examples**

```markdown
## Configuration

Create `.env` file:

```bash
# Required API keys
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here

# Optional settings
LOG_LEVEL=INFO
MAX_SLIDES=100
ENABLE_CACHING=true
```

```

## 🎯 Visual Elements

### **Icon Usage Guidelines**

#### 📋 Standard Icon Mappings
| Category             | Primary Icon | Alternative Icons | Usage                                   |
| :------------------- | :----------- | :---------------- | :-------------------------------------- |
| **Architecture**     | 🏗️            | 🏛️, 🌉, 🔧           | System design, patterns, infrastructure |
| **Code/Development** | 💻            | 🔧, ⚙️, 🛠️, 👨‍💻        | Code examples, tools, programming       |
| **Security**         | 🔒            | 🔐, 🛡️, 🔑, 🚨        | Security topics, authentication         |
| **Performance**      | ⚡            | 🚀, 📈, ⏱️, 🏃‍♂️        | Optimization, speed, efficiency         |
| **Best Practices**   | 💡            | 📋, ✨, 🎯, 🌟        | Guidelines, tips, recommendations       |
| **Warning/Caution**  | ⚠️            | 🚨, ❗, ⛔, 🔥        | Important notices, alerts               |
| **Success/Complete** | ✅            | ✔️, 🎉, 👍, 🟢        | Positive outcomes, completion           |
| **Error/Failed**     | ❌            | ❗, 🔴, 🚫, 💥        | Negative outcomes, failures             |
| **Documentation**    | 📚            | 📖, 📝, 📄, 📋        | Text content, guides, manuals           |
| **Data/Analytics**   | 📊            | 📈, 📉, 💾, 🗃️        | Data topics, charts, storage            |
| **Cloud/Services**   | ☁️            | 🌐, 🔷, 🌍, 🖥️        | External services, web, servers         |
| **Process/Workflow** | 🔄            | ➡️, 🔀, 📍, 🔁        | Steps, flows, procedures                |
| **Configuration**    | ⚙️            | 🔧, 🛠️, 📝, 🎛️        | Settings, setup, customization          |
| **Testing**          | 🧪            | ✅, 🔍, 🎯, 🧬        | Testing, validation, quality assurance  |
| **Deployment**       | 🚀            | 📦, 🌐, ⬆️, 🎯        | Releases, publishing, distribution      |
| **Monitoring**       | 👀            | 📊, 📈, 🔍, 📡        | Observability, tracking, alerts         |
| **Troubleshooting**  | 🔧            | 🩺, 🔍, ❓, 🛠️        | Problem solving, debugging              |
| **Getting Started**  | 🚀            | 🌟, ⭐, 🎯, 🏁        | Quick start, onboarding                 |
| **Resources**        | 📚            | 🔗, 📎, 🌐, 💼        | Links, references, tools                |
| **Examples**         | 💡            | 📝, 🎯, 🔍, 📋        | Code samples, demonstrations            |

#### 🎨 Heading Icon Rules
```markdown
# 🚀 Main Title (H1) - Use bold, distinctive icons
## 📖 Major Section (H2) - Use category-specific icons
### 🎯 Subsection (H3) - Use relevant contextual icons
#### 📝 Detail Level (H4) - Optional, smaller scope icons
```

### **Badge Standards**

#### 🏷️ Required Badge Types

**Status Badges:**

```markdown
![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)
![Status: Development](https://img.shields.io/badge/Status-Development-yellow)
![Status: Deprecated](https://img.shields.io/badge/Status-Deprecated-red)
```

**Version & Build Badges:**

```markdown
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen)
![Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen)
```

**Documentation Badges:**

```markdown
![Docs](https://img.shields.io/badge/Docs-Complete-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)
![Maintained](https://img.shields.io/badge/Maintained-Yes-brightgreen)
```

#### Badge URL Structure

Badge URLs follow this pattern:

```
https://img.shields.io/badge/{label}-{message}-{color}?style={style}
```

- Use `%20` for spaces in label/message
- Use `%25` for percentage signs
- Style options: `flat`, `flat-square`, `plastic`, `for-the-badge`

Example:

```markdown
![Test Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen?style=flat-square)
```

#### 🎨 Standard Color Coding

| Status               | Color         | Hex Code  | Usage                                |
| :------------------- | :------------ | :-------- | :----------------------------------- |
| **Success/Active**   | `brightgreen` | `#4c1`    | Completed, working, stable           |
| **Information**      | `blue`        | `#007ec6` | Version, documentation, general info |
| **Warning/Progress** | `yellow`      | `#dfb317` | In development, caution, pending     |
| **Error/Critical**   | `red`         | `#e05d44` | Failed, deprecated, broken           |
| **Neutral**          | `lightgrey`   | `#9f9f9f` | Unknown, not applicable              |

#### 📏 Badge Placement Rules

**Document Header Badges:**

```markdown
# 🚀 Project Name

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-blue)

Brief project description here.
```

**Section Status Badges:**

```markdown
## 📖 API Documentation ![Docs](https://img.shields.io/badge/Docs-Complete-brightgreen)

### 🔧 Configuration ![Status](https://img.shields.io/badge/Status-Beta-yellow)
```

#### Complexity Badges

```markdown
![Complexity](https://img.shields.io/badge/Complexity-Basic-green?style=flat-square)
![Complexity](https://img.shields.io/badge/Complexity-Intermediate-yellow?style=flat-square)
![Complexity](https://img.shields.io/badge/Complexity-Advanced-red?style=flat-square)
```

#### Performance Impact Badges

```markdown
![Impact](https://img.shields.io/badge/Impact-Low-green?style=flat-square)
![Impact](https://img.shields.io/badge/Impact-Medium-yellow?style=flat-square)
![Impact](https://img.shields.io/badge/Impact-High-red?style=flat-square)
```

### **Visual Element Rules & Standards**

#### 🎯 Consistent Visual Hierarchy

**Document Structure:**

```markdown
# 🚀 Project Title (H1) - Bold, project-defining icon
## 📖 Major Sections (H2) - Category-specific icons
### 🔧 Subsections (H3) - Functional icons
#### 📝 Details (H4) - Minimal, contextual icons
```

**Icon Consistency Rules:**

- **Use the same icon** for similar concepts across all documentation
- **Maintain visual balance** - avoid icon overload in headings
- **Follow the Standard Icon Mappings** table for all icon choices
- **Test icon visibility** across different themes and devices

#### 🎨 Visual Spacing Standards

**Required Spacing:**

```markdown
# 🚀 Title

![Badge](url) ![Badge](url)

Brief description paragraph.

## 📖 Section Header

Content with proper spacing around elements.

### 🔧 Subsection

- List items with proper spacing
- Second item

```code blocks with blank lines above and below```

More content continues...
```

#### 🔍 Accessibility Guidelines

**Icon Accessibility:**

- Always include descriptive alt text for images
- Use high-contrast icon combinations
- Ensure icons enhance, not replace, textual information
- Test with screen readers when possible

**Badge Accessibility:**

```markdown
![Status: Active - Project is currently maintained](https://img.shields.io/badge/Status-Active-brightgreen)
```

### **Header Navigation Standards**

#### 🧭 Required Header Format

**All markdown files must include a consistent header with breadcrumb navigation:**

```markdown
# 🎯 Document Title - Project Name

> **🏠 [Home](../../README.md)** | **📖 [Documentation](../README.md)** | **🔧 [Current Section](CURRENT_FILE.md)** | **👤 Current Page**

<!-- --- -->
```

#### 📍 Breadcrumb Navigation Rules

**Structure Requirements:**

- Start with Home icon (🏠) linking to root README.md
- Include Documentation link (📖) to docs/README.md
- Add relevant section link with appropriate icon
- End with current page name (no link, bold text)
- Use pipe separators (|) between navigation items
- Wrap entire navigation in blockquote (>)

**Icon Guidelines for Navigation:**

- 🏠 **Home** - Always links to root README.md
- 📖 **Documentation** - Links to docs/README.md
- 🔧 **Developer Guide** - For development-related docs
- 👤 **User Guide** - For user-facing documentation
- 📋 **API Reference** - For API documentation
- 🏗️ **Architecture** - For system design docs
- ⚙️ **Configuration** - For setup and config docs

**Path Examples:**

```markdown
<!-- Root level file -->
> **🏠 [Home](README.md)** | **📖 Current Page**

<!-- Docs folder file -->
> **🏠 [Home](../README.md)** | **📖 Documentation** | **👤 Current Page**

<!-- Docs subfolder file -->
> **🏠 [Home](../../README.md)** | **📖 [Documentation](../README.md)** | **🔧 [Guides](README.md)** | **👤 Current Page**
```

### **Color Coding Guidelines**

| Color        | Hex Code  | Usage                    | Examples              |
| :----------- | :-------- | :----------------------- | :-------------------- |
| 🟢 **Green**  | `#28a745` | Success, Good, Complete  | Active, Low Impact    |
| 🟡 **Yellow** | `#ffc107` | Warning, Caution, Medium | Beta, Medium Impact   |
| 🔴 **Red**    | `#dc3545` | Error, High Priority     | Critical, High Impact |
| 🔵 **Blue**   | `#007bff` | Information, Primary     | Default, Links        |
| ⚫ **Gray**   | `#6c757d` | Disabled, Inactive       | Deprecated, N/A       |

### **Callouts**

Use consistent formatting for special content:

```markdown
> **💡 Tip:** Use caching to improve performance in production environments.

> **⚠️ Warning:** This operation will overwrite existing files.

> **📝 Note:** The API key must have presentation generation permissions.

> **🚨 Important:** Always backup data before performing this operation.

> **ℹ️ Info:** This feature requires version 2.0 or higher.
```

### **Diagrams**

- Use mermaid for simple diagrams
- Store complex diagrams in `docs/diagrams/`
- Include alt text for accessibility

```mermaid
graph TD
    A[Markdown Input] --> B[Parser]
    B --> C[Content Agent]
    C --> D[Design Agent]
    D --> E[PowerPoint Output]
```

## 🖼️ Images & Media

### **Image Standards**

- **Format**: Prefer PNG for screenshots, SVG for diagrams, JPEG for photos
- **Size**: Optimize images under 500KB
- **Storage**: Place in `/docs/assets/images/`
- **Naming**: Use descriptive names: `api-flow-diagram.png`, `setup-step-1.png`
- **Dimensions**: Maximum width 1200px for readability

### **Alt Text Requirements**

Always provide descriptive alt text for accessibility:

```markdown
![Descriptive alt text explaining what the image shows](path/to/image.png)
```

### **Responsive Images**

For HTML embedding when markdown isn't sufficient:

```html
<img src="image.png" alt="Description" width="600" loading="lazy">
```

### **Image Captions**

```markdown
![Architecture Diagram](assets/images/architecture.png)
*Figure 1: System architecture showing component interactions*
```

### **Screenshots**

- Include relevant UI context
- Highlight important areas with arrows or boxes
- Use consistent styling across all screenshots
- Update screenshots when UI changes

## 🔗 Cross-References

### **Internal Links**

- Use relative paths: `[API Guide](../api/guide.md)`
- Link to specific sections: `[Configuration](../setup.md#configuration)`
- Verify links with tools before committing
- Use descriptive anchor text

### **Document Versioning**

- Include version in filename for major versions: `api-v2.md`
- Maintain changelog: `CHANGELOG.md`
- Link to version history
- Archive old versions in `/docs/archive/`

### **External Links**

- Always use HTTPS when available
- Check links periodically for dead URLs
- Consider using reference-style for frequently used links
- Add `target="_blank"` for external links in HTML

## 📦 Special Content

### **Collapsible Sections**

Use for lengthy optional content:

```markdown
<details>
<summary>🔍 Click to expand advanced configuration</summary>

Advanced configuration content here...

- Option 1: Description
- Option 2: Description

</details>
```

### **Task Lists & Checklists**

```markdown
## ✅ Implementation Checklist

- [x] Design approved
- [x] Code implemented
- [ ] Tests written
- [ ] Documentation updated
- [ ] Code review completed
```

### **Mathematical Notation**

For inline math: `$E = mc^2$`

For block math:

```markdown
$$
\frac{n!}{k!(n-k)!} = \binom{n}{k}
$$
```

### **Deprecation Notices**

```markdown
> **⚠️ DEPRECATED**: This feature will be removed in v3.0
>
> **Migration Path:** Use `new_function()` instead
> **Timeline:** Removal planned for January 2025
> **Migration Guide:** [View migration guide](migration-v3.md)
```

### **Changelog Format**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature X

### Changed
- Updated Y behavior

### Deprecated
- Feature Z will be removed in v3.0

### Removed
- Deleted obsolete feature W

### Fixed
- Bug fix in component V

### Security
- Patched vulnerability in dependency U
```

## 🔍 SEO & Discoverability

### **SEO Guidelines**

- Include primary keywords in H1 and H2 headings
- Add meta description in front matter (if supported)
- Use descriptive file names with keywords
- Include relevant tags/labels
- Create meaningful URLs/paths
- Add schema markup where appropriate

### **Front Matter Template**

```yaml
---
title: "API Reference Guide"
description: "Complete API reference for all endpoints and methods"
keywords: ["api", "reference", "documentation", "endpoints"]
author: "Team Name"
date: 2024-01-01
version: "2.0.0"
---
```

### **Searchability**

- Use consistent terminology
- Include common synonyms
- Add search tags
- Create index pages
- Build sitemap for docs

## 🧪 Testing & Validation

### **Documentation Testing Checklist**

- [ ] **Link Validation**
  - [ ] All internal links verified
  - [ ] External links checked
  - [ ] Anchor links tested
  - [ ] Image paths validated

- [ ] **Code Testing**
  - [ ] Code examples tested and working
  - [ ] API calls verified
  - [ ] Configuration samples validated
  - [ ] Dependencies listed correctly

- [ ] **Formatting Validation**
  - [ ] Markdown lints without errors
  - [ ] Tables render properly
  - [ ] Lists formatted consistently
  - [ ] Code blocks have language tags

- [ ] **Content Review**
  - [ ] Technical accuracy verified
  - [ ] Grammar and spelling checked
  - [ ] Terminology consistent
  - [ ] Examples relevant and current

### **Validation Tools**

```bash
# Markdown linting
markdownlint docs/**/*.md

# Link checking
markdown-link-check docs/**/*.md

# Spell checking
cspell docs/**/*.md

# Vale for style consistency
vale docs/**/*.md
```

## 🤖 Automation & Enforcement

### **Linting Rules**

This project uses markdownlint with the following key rules:

```json
{
  "MD013": {
    "line_length": 100,
    "heading_line_length": 100,
    "code_block_line_length": 120,
    "tables": false
  },
  "MD033": {
    "allowed_elements": ["br", "img", "div", "details", "summary", "kbd", "sup", "sub"]
  },
  "MD029": {
    "style": "one"
  },
  "MD026": {
    "punctuation": ".,;:!"
  }
}
```

### **Pre-commit Hooks**

Install and configure:

```bash
pip install pre-commit
pre-commit install
```

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.39.0
    hooks:
      - id: markdownlint
        args: ["--fix"]

  - repo: https://github.com/tcort/markdown-link-check
    rev: v3.11.2
    hooks:
      - id: markdown-link-check
```

### **IDE Setup**

**VS Code Extensions:**

- markdownlint
- Markdown All in One
- Markdown Preview Enhanced
- Mermaid Markdown Syntax Highlighting

**Settings:**

```json
{
  "markdownlint.config": {
    "extends": ".markdownlint.json"
  },
  "[markdown]": {
    "editor.formatOnSave": true,
    "editor.wordWrap": "wordWrapColumn",
    "editor.wordWrapColumn": 100,
    "editor.rulers": [100],
    "editor.defaultFormatter": "DavidAnson.vscode-markdownlint"
  },
  "markdown.preview.breaks": true,
  "markdown.extension.toc.levels": "2..6"
}
```

### **CI/CD Integration**

```yaml
name: Documentation Validation

on: [push, pull_request]

jobs:
  validate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lint Markdown
        uses: DavidAnson/markdownlint-cli2-action@v9
      - name: Check Links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
```

### **Git Commit Standards for Docs**

```
docs: <type>: <description>

Types:
- docs: add: New documentation added
- docs: update: Existing documentation updated
- docs: fix: Documentation errors corrected
- docs: remove: Documentation removed
- docs: style: Formatting/style changes only

Example:
docs: update: API reference for v2.0 endpoints
```

## 📋 Templates

### **README Template**

```markdown
# 🚀 Project Name

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-blue)

Brief description of what this project does and who it's for (1-2 sentences).

## ✨ Key Features

- **Feature 1**: Brief description
- **Feature 2**: Brief description
- **Feature 3**: Brief description

## 🚀 Quick Start

```bash
npm install package-name
npm run start
```

## 📦 Installation

Detailed installation instructions...

## 🔧 Usage

### Basic Example

```javascript
const package = require('package-name');
package.doSomething();
```

## 📖 Documentation

- [API Reference](docs/api-reference.md)
- [User Guide](docs/user-guide.md)
- [Examples](docs/examples.md)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- Credit to contributors
- Third-party libraries used

```

### **Document Header Template**

```markdown
# 🚀 Document Title

<div align="center">

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0-blue?style=for-the-badge)
![Complexity](https://img.shields.io/badge/Complexity-Basic-green?style=for-the-badge)

### 📚 Brief Description

</div>

---
```

### **Section Header Template**

```markdown
## 📖 Section Title

> **💡 Brief section description or key insight**

### 🎯 Subsection Title
```

### **Feature Table Template**

```markdown
| Feature         | Description      | Status    |
| :-------------- | :--------------- | :-------- |
| 🎯 **Feature 1** | Description here | ✅ Active  |
| 🚀 **Feature 2** | Description here | 🚧 Beta    |
| 💡 **Feature 3** | Description here | 📅 Planned |
```

### **API Documentation Template**

```markdown
### `function_name(parameters)`

Brief description of what the function does.

**Parameters:**
- `param1` (type): Description
- `param2` (type, optional): Description with default

**Returns:**
- `return_type`: Description of return value

**Raises:**
- `ErrorType`: When this error occurs

**Example:**
```python
result = function_name(param1="value")
print(result)
```

```

### **Troubleshooting Section Template**

```markdown
## 🔧 Troubleshooting

### Common Issues

**Problem:** Brief description of the issue
**Symptoms:** What the user observes
**Solution:** Step-by-step solution
**Prevention:** How to avoid this issue

### Getting Help
- Check [documentation link](url)
- Review [troubleshooting guide](url)
- Contact support at [email/link]
- Open issue on [GitHub](url)
```

## 🔍 Review Checklist

Before submitting documentation:

- [ ] **Structure**
  - [ ] Clear title and description
  - [ ] Table of contents for long documents
  - [ ] Logical section organization
  - [ ] Consistent heading hierarchy
  - [ ] Navigation breadcrumbs included

- [ ] **Content**
  - [ ] Active voice used
  - [ ] Examples included
  - [ ] Error cases covered
  - [ ] Next steps provided
  - [ ] Terminology consistent

- [ ] **Formatting**
  - [ ] Consistent list formatting
  - [ ] Code blocks have language specified
  - [ ] Links use descriptive text
  - [ ] Tables properly formatted
  - [ ] Line length within limits

- [ ] **Visual Elements**
  - [ ] Icons used consistently
  - [ ] Badges properly formatted
  - [ ] Images have alt text
  - [ ] Diagrams are clear

- [ ] **Technical**
  - [ ] All code examples tested
  - [ ] API signatures accurate
  - [ ] Configuration examples valid
  - [ ] Links work correctly
  - [ ] Version information current

## 📚 Additional Resources

### **Documentation Best Practices**

- [Write the Docs](https://www.writethedocs.org/)
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Microsoft Writing Style Guide](https://docs.microsoft.com/en-us/style-guide/welcome/)
- [The Documentation System](https://documentation.divio.com/)

### **Markdown Resources**

- [CommonMark Specification](https://commonmark.org/)
- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Mastering Markdown](https://guides.github.com/features/mastering-markdown/)

### **Visual Resources**

#### **Emoji Reference Tools**

- **[Emojipedia](https://emojipedia.org/)** - Comprehensive emoji database with copy-paste functionality
- **[Unicode Emoji Charts](https://unicode.org/emoji/charts/)** - Official Unicode emoji reference
- **[GitHub Emoji Cheat Sheet](https://github.com/ikatyang/emoji-cheat-sheet)** - Complete list of `:emoji_name:` codes
- **[Gitmoji](https://gitmoji.dev/)** - Emoji guide for commit messages

#### **Icon Libraries**

- **[Font Awesome](https://fontawesome.com/)** - Thousands of icons with HTML embedding support
- **[Heroicons](https://heroicons.com/)** - Beautiful hand-crafted SVG icons
- **[Feather Icons](https://feathericons.com/)** - Simply beautiful open source icons
- **[Lucide](https://lucide.dev/)** - Beautiful & consistent icon toolkit
- **[Simple Icons](https://simpleicons.org/)** - Brand icons for popular services
- **[Tabler Icons](https://tabler-icons.io/)** - Over 4,400+ free SVG icons
- **[Phosphor Icons](https://phosphoricons.com/)** - Flexible icon family

#### **Badge Services**

- **[Shields.io](https://shields.io/)** - Generate SVG badges and shields
- **[Badgen](https://badgen.net/)** - Fast badge generating service
- **[For the Badge](https://forthebadge.com/)** - Badges for your projects
- **[Badge Generator](https://badge-generator.com/)** - Custom badge creation

#### **Diagram Tools**

- **[Mermaid](https://mermaid.js.org/)** - Generate diagrams from text
- **[PlantUML](https://plantuml.com/)** - Create UML diagrams from text
- **[Draw.io/Diagrams.net](https://app.diagrams.net/)** - Online diagramming tool
- **[Excalidraw](https://excalidraw.com/)** - Virtual whiteboard for sketching
- **[ASCII Flow](https://asciiflow.com/)** - Draw ASCII diagrams

### **Validation & Testing Tools**

- **[markdownlint](https://github.com/DavidAnson/markdownlint)** - Markdown linter
- **[markdown-link-check](https://github.com/tcort/markdown-link-check)** - Link validation
- **[Vale](https://vale.sh/)** - Prose linting for documentation
- **[alex](https://alexjs.com/)** - Catch insensitive writing
- **[write-good](https://github.com/btford/write-good)** - Prose linter

### **Performance & Optimization**

- Keep document file size under 100KB for optimal loading
- Split large documents into multiple pages
- Use lazy loading for images where supported
- Compress images before adding to repository
- Consider using CDN for large media files

### **Multilingual Documentation**

When supporting multiple languages:

- Use language codes in filenames: `README.md`, `README.es.md`, `README.fr.md`
- Maintain language consistency within documents
- Keep all language versions synchronized
- Use professional translation services for accuracy
- Include language selector in documentation

### **Archive & Sunset Procedures**

For outdated documentation:

1. **Mark as Deprecated**: Add deprecation notice with date
2. **Provide Migration Path**: Link to updated documentation
3. **Set Sunset Date**: Announce removal timeline
4. **Archive**: Move to `/docs/archive/` folder
5. **Redirect**: Set up redirects to new documentation

## 🚀 Examples

### **Good Documentation Structure**

```markdown
# Agent Configuration Guide

This guide explains how to configure agents for optimal performance.

## Overview

Agents are configurable components that process different aspects of presentation generation.

## Configuration Files

### Basic Configuration

Create `config/agents.yaml`:

```yaml
---
research_agent:
  enabled: true
  max_results: 10
  timeout: 30
```

### Advanced Options

For production environments, consider these additional settings...

## Troubleshooting

### Common Issues

**Problem:** Agent fails to initialize
**Solution:** Check API key configuration in `.env` file

## Next Steps

- [Deploy agents to production](deployment-guide.md)
- [Monitor agent performance](monitoring.md)

```

### **Poor Documentation Example**

```markdown
# agents

how to setup agents

you need to configure them first. here's how:

put this in a file:
```

some_setting: true

```

then run it and it should work. if not, check the logs.
```

## 📞 Getting Help

- **Style Questions**: Reference this guide or ask in team discussions
- **Technical Issues**: Check existing documentation or create an issue
- **Tool Problems**: Verify markdownlint configuration and IDE setup
- **Updates**: Submit pull requests for style guide improvements

---

*Last Updated: January 2025*
*Version: 2.0.0*

*This style guide is a living document. Suggest improvements via pull request.*

```markdown
# 🎯 Document Title - Project Name

> **🏠 [Home](../../README.md)** | **📖 [Documentation](../README.md)** | **🔧 [Current Section](CURRENT_FILE.md)** | **👤 Current Page**

<!-- --- -->
```
