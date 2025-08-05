# Git Hooks for Azure Synapse Analytics Documentation

This directory contains Git hooks to help maintain code quality and consistency in the Azure Synapse Analytics documentation project.

## Available Hooks

- **pre-commit**: Checks for markdown linting issues in staged files before committing

## Setup Instructions

To enable these git hooks in your local repository, run the following command from the root of the project:

```bash
git config core.hooksPath .githooks
```

### Prerequisites

The pre-commit hook requires the `markdownlint-cli` tool. Install it using npm:

```bash
npm install -g markdownlint-cli
```

## Using the Hooks

### Pre-commit Hook

The pre-commit hook automatically runs when you attempt to commit changes that include markdown files. If any linting issues are found, the commit will be blocked, and you'll see a list of issues that need to be fixed.

If you need to bypass the hook for a specific commit (not recommended), you can use:

```bash
git commit --no-verify -m "Your commit message"
```

## Resolving Common Issues

### Strong Style Formatting

Use underscores (`__text__`) instead of asterisks (`**text**`) for strong text.

### Inline HTML

When using inline HTML for Material for MkDocs features, add a comment above:

```markdown
<!-- Markdown lint exception: Inline HTML is used here for Material for MkDocs grid cards feature -->
<div class="grid cards" markdown>
```

### Blank Lines Around Code Blocks

Ensure fenced code blocks are surrounded by blank lines and include a language specifier:

```markdown
Text before code.

```python
def example():
    return "This is properly formatted"
```

Text after code.

### Trailing Spaces

Remove trailing spaces at the end of lines. Most code editors can be configured to automatically trim trailing whitespace.
