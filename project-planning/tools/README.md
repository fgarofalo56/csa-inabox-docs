# Documentation Tools

This directory contains utility tools for maintaining and validating the Azure Synapse Analytics documentation.

## Available Tools

### Link Checker (`link_checker.py`)

A Python utility that scans all Markdown files in the documentation project, extracts links, and verifies that they are working properly. It checks both internal relative links and external URLs.

#### Features

- Validates all internal relative links between documentation files
- Tests external URLs to ensure they're accessible
- Detects broken links and generates a detailed report
- Handles various link formats including standard markdown links and reference-style links
- Parallel processing for faster execution


#### Requirements

- Python 3.6+
- `requests` library (`pip install requests`)


#### Usage

```bash
# Navigate to the tools directory
cd project-planning/tools

# Run the link checker on the project root
python link_checker.py ../..

# Alternatively, specify a different root directory
python link_checker.py /path/to/project
```


#### Output

- Console output with progress and warnings
- A detailed markdown report saved to `project-planning/link_check_report.md`

### Automated Link Checking

The link checker has been configured to run automatically through GitHub Actions. This ensures documentation links remain valid over time without manual intervention.

#### Automation Schedule

- **On code push**: Runs automatically when changes are pushed to the main branch
- **On pull requests**: Validates documentation in proposed changes
- **Weekly check**: Runs every Monday at 9:00 AM to detect external links that may have broken
- **Manual trigger**: Can be executed on-demand through GitHub Actions interface


#### Workflow Process

1. The GitHub workflow defined in `.github/workflows/link-checker.yml` executes the link checker
2. If broken links are detected:
   - A detailed report is generated in `project-planning/link_check_report.md`
   - A GitHub issue is created or updated with the broken link information
   - Appropriate labels (`broken-links`, `documentation`, `bug`) are applied


#### Monitoring and Maintenance

- Review the link check report after significant documentation updates
- Check the GitHub repository issues for any automatically created broken link reports
- Fix broken links promptly to maintain documentation integrity

## Adding New Tools

When adding new tools to this directory:

1. Create a descriptive name for your script
2. Add proper documentation including usage instructions
3. Update this README with information about the new tool
4. Ensure the tool follows project coding standards
