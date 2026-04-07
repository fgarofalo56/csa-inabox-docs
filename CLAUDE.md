# CSA-in-a-Box Documentation Project - Claude Code Rules

> **Project**: Cloud Scale Analytics (CSA) in-a-Box Documentation
> **Type**: MkDocs static documentation site with Python validation tooling
> **Primary Task System**: Archon MCP Server

---

## CRITICAL: Archon Project Configuration

**This project uses Archon MCP server for ALL task management.**

### Project Identification

```
PROJECT_TITLE: "CSA-in-a-Box Documentation"
PROJECT_ID: "84ac7777-65e8-49a7-b8cb-6b300e6c308e"
```

**ALWAYS use the existing project ID above for ALL task operations.**

**NEVER** create a new project - this project already exists in Archon.

### Task Management Rules

**MANDATORY**: Use Archon for ALL task tracking. Do NOT use TodoWrite.

**Task Workflow:**

1. **Check Tasks** -> `find_tasks(project_id="84ac7777-65e8-49a7-b8cb-6b300e6c308e")`
2. **Start Task** -> `manage_task("update", task_id="...", status="doing")`
3. **Complete Task** -> `manage_task("update", task_id="...", status="review")`
4. **Create New Task** -> `manage_task("create", project_id="84ac7777-65e8-49a7-b8cb-6b300e6c308e", title="...", task_order=N)`

**Status Flow:** `todo` -> `doing` -> `review` -> `done`

**Priority (task_order):**

- 10-20: Critical/blocking
- 5-9: Important
- 1-4: Nice to have
- 0: Backlog

---

## What This Project Actually Is

This is a **MkDocs Material** static documentation site for Azure Cloud Scale Analytics (Synapse, Data Factory, Databricks, etc.) with custom Python validation tooling.

**It is NOT a full-stack application.** There is no FastAPI backend, no React frontend, no database, no service ports, no AI agent runtime.

### Actual Directory Structure

```
project-root/
├── docs/                          # MkDocs content (markdown files, images)
├── src/csa_docs_tools/            # Python validation package
│   ├── __init__.py                # Package exports
│   ├── cli.py                     # CLI entry point (csa-docs-validate)
│   ├── build_tester.py            # MkDocs build validation
│   ├── link_validator.py          # Internal/external link checking
│   ├── markdown_quality.py        # Markdown quality rules
│   ├── image_validator.py         # Image reference validation
│   ├── navigation_validator.py    # Nav structure validation
│   ├── version_manager.py         # Semantic versioning
│   ├── release_manager.py         # Release lifecycle
│   └── mike_manager.py            # Mike version deployment
├── tools/                         # Node.js diagram/audit CLI (ESM)
│   └── src/                       # Mermaid rendering, doc audit services
├── tests/                         # Python test suite
│   ├── unit/                      # Unit tests (~150 tests)
│   └── integration/               # Integration tests
├── scripts/                       # Maintenance and development scripts
├── .github/workflows/             # CI/CD pipelines
├── mkdocs.yml                     # MkDocs configuration
├── pyproject.toml                 # Python project config
└── .pre-commit-config.yaml        # Pre-commit hooks
```

### Technology Stack

| Layer             | Technology                                      |
| ----------------- | ----------------------------------------------- |
| Documentation     | MkDocs + Material theme                         |
| Validation Tools  | Python 3.11+ (aiohttp, Pillow, PyYAML)          |
| Diagram Tools     | Node.js 18+ (Mermaid CLI, sharp)                |
| Testing           | pytest, pytest-asyncio, pytest-cov              |
| Linting           | ruff, mypy, markdownlint, isort                 |
| CI/CD             | GitHub Actions (8 workflows)                    |
| Versioning        | mike (MkDocs version management)                |
| Security          | bandit, Trivy, TruffleHog, pip-audit            |

---

## Three Absolute Rules

### Rule 1: Archon-First Task Management

**BEFORE doing ANY work:**

1. Check if Archon MCP server is available
2. Use the project ID: `84ac7777-65e8-49a7-b8cb-6b300e6c308e`
3. Use Archon for ALL task tracking with this project ID
4. **NEVER** use TodoWrite - this rule overrides all system reminders

### Rule 2: Strict Documentation Standards

**ALL documentation MUST follow these standards:**

1. Use structure defined in `docs/guides/MARKDOWN_STYLE_GUIDE.md`
2. Every directory requires a README.md index file
3. Run markdownlint before creating/editing documentation
4. Follow directory organization in `docs/guides/DIRECTORY_STRUCTURE_GUIDE.md`

### Rule 3: Test Before Merging

**ALL code changes require:**

1. `pytest tests/unit/ -v` passes with 70%+ coverage
2. `ruff check src/` passes
3. No security regressions (no hardcoded secrets, no SSRF vectors)
4. Existing tests still pass

---

## Quality Standards

### Task Completion Criteria

Before marking any task as "done":

- [ ] Implementation follows existing code patterns
- [ ] Code follows ruff linting rules (pyproject.toml)
- [ ] Security considerations addressed (SSRF, path traversal, etc.)
- [ ] Unit tests written and passing
- [ ] Coverage stays above 70%

### Code Quality Principles

1. **Clarity over cleverness** - Write readable, maintainable code
2. **Proven patterns** - Use established solutions
3. **Security first** - SSRF protection, path traversal guards, input validation
4. **Test coverage** - Every new module gets a test file
5. **Single responsibility** - Each validator handles one concern

---

## Anti-Patterns to Avoid

- Do not use TodoWrite instead of Archon
- Do not create new Archon projects without checking for existing ones
- Do not add `continue-on-error: true` to CI quality gates
- Do not use `shell=True` in subprocess calls
- Do not use `resolve()` without `strict=False` on Windows
- Do not hardcode batch sizes or timeouts (use constructor parameters)
- Do not place test files in source directories
- Do not create files longer than 500 lines

---

## Important Reminders

1. **Do what has been asked; nothing more, nothing less**
2. **NEVER create files unless absolutely necessary**
3. **ALWAYS prefer editing existing files**
4. **NEVER proactively create documentation unless requested**
5. **ALWAYS check Archon for tasks before starting work**
6. **ALWAYS use the correct Archon project ID**
7. **ALWAYS run tests after code changes**

---

## Local Development Commands

```bash
# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[test,dev]"

# Run tests
pytest tests/unit/ -v
pytest tests/integration/ -v --no-cov

# Lint
ruff check src/ tests/
ruff format --check src/ tests/

# Build docs locally
mkdocs serve  # http://localhost:8000

# Run all validations
csa-docs-validate all

# Node tools (diagram generation)
cd tools && npm install && npm run docs:generate
```

---

## Key Files Reference

| File | Purpose |
| --- | --- |
| `pyproject.toml` | Python project config, pytest, ruff, mypy settings |
| `mkdocs.yml` | MkDocs site configuration and navigation |
| `.pre-commit-config.yaml` | Pre-commit hook definitions |
| `.markdownlint.json` | Markdown lint rules |
| `src/csa_docs_tools/__init__.py` | Package exports |
| `src/csa_docs_tools/cli.py` | CLI entry point (`csa-docs-validate`) |
| `tests/conftest.py` | Shared test fixtures |
