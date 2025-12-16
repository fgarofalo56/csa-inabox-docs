> Command for priming Claude Code with core knowledge about your project

# Prime Context for Claude Code

Use MCP the following servers to perform the your tasks:

- serena
- crawl4ai-rag
- microsoft-docs-mcp
- MCP_DOCKER

Use the command `tree` to get an understanding of the project structure.

Start with reading the CLAUDE.md file if it exists to get an understanding of the project.

Read Serena's initial instructions

Use MCP tools if needed to get more context about the project, its dependencies, and its configuration, code style, architecture, design patterns, and any other relevant information.

Read the README.md and all other markdown files to get an understanding of the project.

Read key files in the src/ or root directory
Read configuration files like package.json, requirements.txt, setup.py, Dockerfile, .env, etc.
Read any documentation files like docs/, CONTRIBUTING.md, etc.

IMPORTANT: Use Serena to search through the codebase. If you get any errors using Serena,
retry with different Serena tools.

IMPORTANT: Check if project is onboard to Serena. If not, onboard it.

IMPORTANT: Check if project is onboard to to Claude Code project_tracking. If not, onboard it.

IMPORTANT: Check  /project_tracking:

- Open tasks
- Planning items
- Backlog items
- Notes
- Status
- Planned items
- Backlog items
- Todos
- Phases
- Specs
- Constitions
- Design docs

> List any additional files that are important to understand the project.

Explain back to me:

- Project structure
- Project purpose and goals
- Key files and their purposes
- Any important dependencies
- Any important configuration files
- Potential issues found that should be addressed
- Missing documention
- Code test coverage
- Refactoring and enhancment opportunities
- All open and backlog tasks, items, and todos
- Suggested Tasks and items to work on
- Any other information or recomendation that you think would improve the codebase and should be addressed and implemented.
- Next steps to take