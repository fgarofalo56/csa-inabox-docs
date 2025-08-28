# Codebase Structure

## Root Directory
```
csa-inabox-docs/
├── docs/                      # Main documentation content
├── project_tracking/          # Project management and tracking
├── site/                      # Generated static site (gitignored)
├── .venv/                     # Python virtual environment
├── .githooks/                 # Git hooks for quality control
├── .github/                   # GitHub Actions workflows
├── .serena/                   # Serena MCP memories
├── .claude/                   # Claude configuration
```

## Documentation Structure
```
docs/
├── architecture/              # System architecture documentation
│   ├── delta-lakehouse/      # Delta Lake architecture
│   ├── serverless-sql/       # Serverless SQL architecture
│   └── shared-metadata/      # Shared metadata patterns
├── best-practices/           # Implementation best practices
├── code-examples/            # Code snippets and examples
├── reference/                # Technical reference docs
├── diagrams/                 # Visual documentation
├── troubleshooting/          # Problem-solving guides
├── guides/                   # Documentation guidelines
│   ├── MARKDOWN_STYLE_GUIDE.md
│   └── DIRECTORY_STRUCTURE_GUIDE.md
├── images/                   # Documentation images
├── assets/                   # Static assets (CSS, JS)
└── overrides/               # MkDocs theme overrides
```

## Project Tracking
```
project_tracking/
├── tasks/                    # Task management
├── planning/                 # Planning documents
├── status/                   # Status reports
├── backlogs/                # Product backlogs
├── sprints/                  # Sprint planning
├── roadmaps/                # Product roadmaps
├── architecture/            # Architecture decisions
├── research/                # Research notes
└── tools/                   # Python utility scripts
    ├── serve-docs.py        # Local documentation server
    ├── version-docs.py      # Version management
    ├── link_checker.py      # Link validation
    └── fix_markdown.py      # Markdown fixing utility
```

## Configuration Files
- `mkdocs.yml` - MkDocs configuration
- `.markdownlint.json` - Markdown linter rules
- `requirements.txt` - Python dependencies
- `.mike.yml` - Documentation versioning config
- `CLAUDE.md` - AI agent development rules