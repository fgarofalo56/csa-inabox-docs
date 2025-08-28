# Suggested Development Commands

## Documentation Development

### Serve Documentation Locally
```bash
# Using the Python script
python project_tracking/tools/serve-docs.py

# Or using MkDocs directly
mkdocs serve
```

### Build Documentation
```bash
mkdocs build
```

### Version Management
```bash
# Create new version
python project_tracking/tools/version-docs.py create <version> --alias <alias> --title <title>

# List versions
python project_tracking/tools/version-docs.py list

# Delete version
python project_tracking/tools/version-docs.py delete <version>
```

## Quality Checks

### Markdown Linting
```bash
# Check markdown files
npx markdownlint '**/*.md' -c .markdownlint.json

# Auto-fix issues
npx markdownlint '**/*.md' -c .markdownlint.json --fix
```

### Link Checking
```bash
# Run link checker
python project_tracking/tools/link_checker.py
```

## Git Operations

### Enable Git Hooks
```bash
git config core.hooksPath .githooks
```

### Common Git Commands
```bash
git status
git add .
git commit -m "descriptive message"
git push origin feature-branch
```

## Python Environment

### Setup Virtual Environment
```bash
python -m venv .venv
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install Markdown Linter
```bash
npm install -g markdownlint-cli
```

## Utility Commands

### Find files
```bash
find . -name "*.md" -not -path "./.venv/*"
```

### Search in files
```bash
grep -r "pattern" docs/ --include="*.md"
```

### Tree view
```bash
tree -L 3 -I 'node_modules|__pycache__|.git|*.pyc'
```