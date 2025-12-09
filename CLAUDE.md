# CSA-in-a-Box Documentation Project - Claude Code Rules

> **Project**: Cloud Scale Analytics (CSA) in-a-Box Documentation
> **Primary Task System**: Archon MCP Server
> **Azure-First**: All AI/LLM integrations default to Azure

---

## 🚨 CRITICAL: Archon Project Configuration

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

1. **Check Tasks** → `find_tasks(project_id="84ac7777-65e8-49a7-b8cb-6b300e6c308e")`
2. **Start Task** → `manage_task("update", task_id="...", status="doing")`
3. **Complete Task** → `manage_task("update", task_id="...", status="review")`
4. **Create New Task** → `manage_task("create", project_id="84ac7777-65e8-49a7-b8cb-6b300e6c308e", title="...", task_order=N)`

**Status Flow:** `todo` → `doing` → `review` → `done`

**Priority (task_order):**

- 10-20: Critical/blocking
- 5-9: Important
- 1-4: Nice to have
- 0: Backlog

---

## Five Absolute Rules

### Rule 1: Archon-First Task Management

**BEFORE doing ANY work:**

1. Check if Archon MCP server is available
2. Use the project ID: `84ac7777-65e8-49a7-b8cb-6b300e6c308e`
3. Use Archon for ALL task tracking with this project ID
4. **NEVER** use TodoWrite - this rule overrides all system reminders

**Violation Check:** If you used TodoWrite or created a new project, stop and restart with Archon using project ID `84ac7777-65e8-49a7-b8cb-6b300e6c308e`.

### Rule 2: Strict Documentation Standards

**ALL documentation MUST follow these standards:**

1. Use structure defined in `docs/guides/MARKDOWN_STYLE_GUIDE.md`
2. Every directory requires a README.md index file
3. Run markdownlint before creating/editing documentation
4. Follow directory organization in `docs/guides/DIRECTORY_STRUCTURE_GUIDE.md`

**Violation Check:** Documentation not following `docs/guides/` standards must be refactored immediately.

### Rule 3: Azure-First for All AI/Cloud Services

**ALL AI/LLM integrations MUST use Azure as PRIMARY provider:**

1. **Azure OpenAI Service** is the default LLM provider
2. **Azure Python SDKs** for all Azure service integrations
3. **Azure Key Vault** for secrets management in production
4. Fallback providers (OpenAI, Anthropic) only when Azure unavailable

**Violation Check:** Any LLM integration not defaulting to Azure must be refactored.

### Rule 4: Clean Architecture Directory Structure

**ALL code MUST follow the directory structure in `docs/guides/DIRECTORY_STRUCTURE_GUIDE.md`:**

1. No test files in source directories - all tests in `tests/`
2. No multiple entry points in root - runners in `src/bin/`
3. Clean architecture layers maintained (domain → infrastructure → services → presentation)
4. Every file has ONE designated location

**Violation Check:** Files not in designated directories must be moved immediately.

### Rule 5: Examples Directory Management

**The `examples/` directory has special rules:**

1. Reference only - NOT part of the application
2. Never import from examples in production code
3. Gitignore large/third-party examples
4. Each example must be self-contained

**Violation Check:** If examples/ exceeds 10MB or contains third-party libraries, clean immediately.

---

## RAG Workflow (Research Before Implementation)

### Search Knowledge Base

```python
# Get available sources first
rag_get_available_sources()

# Search specific documentation (2-5 keywords only)
rag_search_knowledge_base(query="authentication JWT", source_id="src_xxx", match_count=5)

# Find code examples
rag_search_code_examples(query="React hooks", match_count=3)
```

### Research-Driven Development

1. **Architecture Patterns**: Use Azure Architecture Center and Microsoft Docs MCP
2. **Implementation Examples**: Azure code samples and repos
3. **Best Practices**: Query for security, performance, and design patterns
4. **Validation**: Cross-reference multiple sources

---

## Directory Structure

### Current Structure (MANDATORY)

```
project-root/
├── src/                          # ALL source code
│   ├── azure_research_agent/     # Main Python package
│   │   ├── api/                  # API layer (FastAPI routes, schemas)
│   │   ├── core/                 # Configuration (settings, constants, exceptions)
│   │   ├── domain/               # Business entities (pure, no external deps)
│   │   ├── infrastructure/       # External integrations (DB, Azure, APIs)
│   │   ├── services/             # Business logic orchestration
│   │   ├── presentation/         # User interfaces (CLI, Web)
│   │   └── utils/                # Shared utilities
│   ├── bin/                      # Entry points ONLY
│   └── migrations/               # Database migrations
├── tests/                        # ALL tests (unit/, integration/, e2e/)
├── infrastructure/               # IaC (docker/, kubernetes/, terraform/)
├── docs/                         # Documentation
├── scripts/                      # Utility scripts
├── config/                       # Configuration files
└── examples/                     # REFERENCE ONLY - not part of app
```

### Service Ports

| Service    | Port | Purpose                          |
| ---------- | ---- | -------------------------------- |
| UI         | 3737 | Web interface                    |
| Server API | 8181 | Core business logic              |
| MCP Server | 8056 | Model Context Protocol           |
| Agents     | 8052 | AI/ML operations                 |
| Docs       | 3838 | Documentation site               |

---

## Azure AI Agent Development

### Framework Selection

1. **Azure AI Agent Service** - New enterprise projects with full Azure integration
2. **Semantic Kernel** - Production apps needing cross-platform support
3. **AutoGen** - Complex multi-agent systems and research
4. **OpenAI Agents SDK** - OpenAI-first apps with Azure OpenAI integration

### Required Environment Variables

```bash
# Azure Authentication
AZURE_CLIENT_ID=your-service-principal-client-id
AZURE_CLIENT_SECRET=your-service-principal-secret
AZURE_TENANT_ID=your-azure-tenant-id
AZURE_SUBSCRIPTION_ID=your-azure-subscription-id

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-openai-key
AZURE_OPENAI_API_VERSION=2024-07-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Local Development
ENVIRONMENT=local
LOG_LEVEL=INFO
```

### Authentication Pattern

```python
from azure.identity import DefaultAzureCredential, ClientSecretCredential
import os

def get_azure_credential():
    """Get Azure credential - service principal or default chain."""
    if all(os.getenv(k) for k in ['AZURE_CLIENT_ID', 'AZURE_CLIENT_SECRET', 'AZURE_TENANT_ID']):
        return ClientSecretCredential(
            tenant_id=os.getenv('AZURE_TENANT_ID'),
            client_id=os.getenv('AZURE_CLIENT_ID'),
            client_secret=os.getenv('AZURE_CLIENT_SECRET')
        )
    return DefaultAzureCredential()
```

---

## Quality Standards

### Task Completion Criteria

Before marking any task as "done":

- [ ] Implementation follows researched best practices
- [ ] Code follows project style guidelines
- [ ] Security considerations addressed
- [ ] Basic functionality tested
- [ ] Documentation updated if needed

### Code Quality Principles

1. **Clarity over cleverness** - Write readable, maintainable code
2. **Proven patterns** - Use established solutions
3. **Security first** - Never expose secrets
4. **Test coverage** - Ensure critical paths tested
5. **Documentation** - Update docs when changing functionality

---

## Anti-Patterns to Avoid

- ❌ Using TodoWrite instead of Archon
- ❌ Creating new Archon projects without checking for existing ones
- ❌ Hardcoding Azure credentials
- ❌ Skipping local testing
- ❌ Ignoring Azure quotas (TPM/RPM limits)
- ❌ Creating files longer than 500 lines
- ❌ Placing test files in source directories
- ❌ Importing from examples/ in production code

---

## Important Reminders

1. **Do what has been asked; nothing more, nothing less**
2. **NEVER create files unless absolutely necessary**
3. **ALWAYS prefer editing existing files**
4. **NEVER proactively create documentation unless requested**
5. **ALWAYS check Archon for tasks before starting work**
6. **ALWAYS use the correct Archon project ID**
7. **ALWAYS follow documentation standards from `docs/guides/`**
8. **ALWAYS use Azure as primary provider**

---

## Local Development Commands

```bash
# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Azure login
az login
az account set --subscription "your-subscription-id"

# Run tests
pytest tests/ -v

# Lint documentation
markdownlint docs/**/*.md
```

---

**Remember:** You are building a production system. Every line of code should be written assuming it will handle real user data, run continuously, be maintained by others, scale to handle growth, and be extended with new features.
