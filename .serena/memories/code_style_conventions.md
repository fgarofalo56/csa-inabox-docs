# Code Style and Conventions

## Markdown Documentation Standards
- Follow guidelines in `docs/guides/MARKDOWN_STYLE_GUIDE.md`
- Use **underscores** for bold text (`__text__`), not asterisks
- Use dashes (`-`) for unordered lists
- Add blank lines around lists and headings
- Use consistent heading hierarchy (one H1 per file)
- Include proper code block syntax highlighting
- Add alt text to all images

## Directory Structure
- Every directory must have a README.md file as index
- Images go in `docs/images/` with subdirectories for organization
- Diagrams in `docs/diagrams/`
- Code examples in `docs/code-examples/`
- Follow structure defined in `docs/guides/DIRECTORY_STRUCTURE_GUIDE.md`

## Documentation Features
- Use admonitions for notes, tips, warnings (Material theme)
- Include Mermaid diagrams (converted to PNG for GitHub compatibility)
- Add breadcrumb navigation
- Include "related topics" sections
- Use card layouts for key information sections

## Git Conventions
- Feature branches: `feature/your-feature-name`
- Descriptive commit messages
- Pre-commit hooks for markdown linting
- Never commit sensitive information