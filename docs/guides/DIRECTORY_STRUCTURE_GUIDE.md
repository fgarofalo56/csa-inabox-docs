# 📁 Directory Structure Guide

> **🎯 Purpose:** This is the authoritative guide for file and folder placement in this project. Use this for refrance on how you should structure your files. All developers and AI coding agents MUST follow this structure when creating new files or folders.

---

## 🚨 CRITICAL RULES - READ FIRST

### ⛔ STOP Before Creating Any File

Before creating or writing ANY file, folder, or directory, you MUST:

1. **CHECK** this guide to determine the correct location
2. **VERIFY** the path follows the structure below
3. **ENSURE** no duplicate functionality exists elsewhere
4. **CONFIRM** the file belongs in this location, not another

### 🔴 Violations Will Be Rejected

Files created in wrong locations MUST be moved immediately. This is NOT optional.

---

## 📋 Table of Contents

- [🚨 CRITICAL RULES - READ FIRST](#-critical-rules---read-first)
  - [⛔ STOP Before Creating Any File](#-stop-before-creating-any-file)
  - [🔴 Violations Will Be Rejected](#-violations-will-be-rejected)
- [📋 Table of Contents](#-table-of-contents)
- [🎯 Core Principles](#-core-principles)
- [📂 Project Root Structure](#-project-root-structure)
- [📦 Source Code (`src/`)](#-source-code-src)
  - [Main Package Structure](#main-package-structure)
- [🧪 Tests (`tests/`)](#-tests-tests)
- [📚 Documentation (`docs/`)](#-documentation-docs)
  - [Mandatory Structure with README Navigation](#mandatory-structure-with-readme-navigation)
- [🏗️ Infrastructure (`infrastructure/`)](#️-infrastructure-infrastructure)
- [🔧 Scripts (`scripts/`)](#-scripts-scripts)
  - [Mandatory Structure](#mandatory-structure)
- [⚙️ Configuration (`config/`)](#️-configuration-config)
  - [Mandatory Structure](#mandatory-structure-1)
- [📖 Examples (`examples/`)](#-examples-examples)
  - [Mandatory Structure](#mandatory-structure-2)
- [📊 Project Tracking (`project_tracking/`)](#-project-tracking-project_tracking)
  - [Mandatory Structure](#mandatory-structure-3)
- [📝 File Naming Conventions](#-file-naming-conventions)
  - [Python Files](#python-files)
  - [Configuration Files](#configuration-files)
  - [Documentation](#documentation)
  - [Scripts](#scripts)
- [🎯 What Goes Where - Quick Reference](#-what-goes-where---quick-reference)
- [❌ Anti-Patterns - NEVER Do This](#-anti-patterns---never-do-this)
  - [🚫 NEVER Place Files:](#-never-place-files)
  - [🚫 NEVER Create:](#-never-create)
- [✅ Validation Checklist](#-validation-checklist)
- [🔄 Keeping This Guide Updated](#-keeping-this-guide-updated)
- [📌 Remember](#-remember)

---

## 🎯 Core Principles

1. **Single Responsibility** - Each directory has ONE clear purpose
2. **No Ambiguity** - Every file has exactly ONE correct location
3. **Clean Architecture** - Maintain separation of concerns
4. **Predictability** - Anyone should know where to find/place files
5. **Consistency** - Same patterns throughout the project

---

## 📂 Project Root Structure

```
rag-researchAgent-Azure/
│
├── 📁 .azure/              # Azure DevOps pipelines and configs
├── 📁 .claude/             # Claude Code specific configurations
├── 📁 .github/             # GitHub specific files (workflows, issues templates)
├── 📁 .vscode/             # VS Code workspace settings
│
├── 📁 config/              # Application configuration files
├── 📁 docs/                # All documentation
├── 📁 examples/            # Example implementations (reference only)
├── 📁 infrastructure/      # IaC, Docker, Kubernetes files
├── 📁 project_tracking/    # Project management files
├── 📁 scripts/             # Utility and automation scripts
├── 📁 src/                 # ALL source code
├── 📁 tests/               # ALL test files
│
├── 📄 .env                 # Local environment variables (never commit)
├── 📄 .env.example         # Template for environment variables
├── 📄 .gitignore           # Git ignore rules
├── 📄 CLAUDE.md            # AI coding agent rules
├── 📄 LICENSE              # Project license
├── 📄 Makefile             # Build automation
├── 📄 pyproject.toml       # Python project configuration
├── 📄 README.md            # Project overview
└── 📄 requirements.txt     # Python dependencies (generated from pyproject.toml)
```

---

## 📦 Source Code (`src/`)

**Purpose:** Contains ALL application source code. No exceptions.

### Main Package Structure

```
src/
├── 📁 azure_research_agent/         # Main Python package
│   ├── 📄 __init__.py              # Package initialization
│   ├── 📄 __version__.py           # Version information
│   │
│   ├── 📁 api/                     # REST API layer
│   │   ├── 📄 __init__.py
│   │   ├── 📁 v1/                  # API version 1
│   │   │   ├── 📁 endpoints/       # FastAPI route handlers
│   │   │   │   ├── 📄 __init__.py
│   │   │   │   ├── 📄 health.py    # Health check endpoints
│   │   │   │   ├── 📄 research.py  # Research endpoints
│   │   │   │   └── 📄 sessions.py  # Session management endpoints
│   │   │   │
│   │   │   └── 📁 schemas/          # Pydantic models for API
│   │   │       ├── 📄 __init__.py
│   │   │       ├── 📄 requests.py  # Request models
│   │   │       └── 📄 responses.py # Response models
│   │   │
│   │   └── 📁 middleware/           # API middleware
│   │       ├── 📄 __init__.py
│   │       ├── 📄 auth.py          # Authentication middleware
│   │       ├── 📄 cors.py          # CORS configuration
│   │       ├── 📄 logging.py       # Request/response logging
│   │       └── 📄 rate_limit.py    # Rate limiting
│   │
│   ├── 📁 core/                     # Core application config
│   │   ├── 📄 __init__.py
│   │   ├── 📄 config.py            # Settings management (Pydantic)
│   │   ├── 📄 constants.py         # Global constants
│   │   ├── 📄 exceptions.py        # Custom exceptions
│   │   └── 📄 logging.py           # Logging configuration
│   │
│   ├── 📁 domain/                   # Business entities (pure Python)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 research.py          # Research domain models
│   │   ├── 📄 session.py           # Session domain models
│   │   ├── 📄 user.py              # User domain models
│   │   └── 📄 cost.py              # Cost tracking models
│   │
│   ├── 📁 infrastructure/          # External integrations
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📁 azure/               # Azure service integrations
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 auth.py          # Azure AD authentication
│   │   │   ├── 📄 key_vault.py     # Azure Key Vault client
│   │   │   ├── 📄 monitor.py       # Azure Monitor/App Insights
│   │   │   └── 📄 openai_client.py # Azure OpenAI client
│   │   │
│   │   ├── 📁 database/            # Database layer
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 azure_sql.py     # Azure SQL/PostgreSQL config
│   │   │   ├── 📄 models.py        # SQLAlchemy ORM models
│   │   │   ├── 📄 session.py       # Database session management
│   │   │   │
│   │   │   ├── 📁 repositories/    # Data access layer
│   │   │   │   ├── 📄 __init__.py
│   │   │   │   ├── 📄 base.py      # Base repository class
│   │   │   │   ├── 📄 research.py  # Research data access
│   │   │   │   └── 📄 session.py   # Session data access
│   │   │   │
│   │   │   └── 📁 migrations/       # Database migrations
│   │   │       └── 📄 __init__.py
│   │   │
│   │   ├── 📁 external_apis/       # Third-party API clients
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 brave_search.py  # Brave Search API client
│   │   │   ├── 📄 mcp_manager.py   # MCP server manager
│   │   │   └── 📄 search_providers.py # Search provider interface
│   │   │
│   │   └── 📁 cache/               # Caching implementations
│   │       ├── 📄 __init__.py
│   │       ├── 📄 redis_client.py  # Redis cache client
│   │       └── 📄 memory_cache.py  # In-memory cache
│   │
│   ├── 📁 services/                # Business logic orchestration
│   │   ├── 📄 __init__.py
│   │   ├── 📄 azure_agent.py      # Main Azure AI agent
│   │   ├── 📄 research_service.py # Research orchestration
│   │   ├── 📄 cost_service.py     # Cost tracking service
│   │   ├── 📄 export_service.py   # Export functionality
│   │   └── 📄 webhook_service.py  # Webhook integrations
│   │
│   ├── 📁 presentation/            # User interfaces
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📁 cli/                # Command-line interface
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 cli.py          # Main CLI app
│   │   │   ├── 📄 commands.py     # CLI commands
│   │   │   ├── 📄 display.py      # Rich display formatting
│   │   │   └── 📄 main.py         # CLI entry point
│   │   │
│   │   └── 📁 web/                # Web interface
│   │       ├── 📄 __init__.py
│   │       ├── 📄 app.py          # FastAPI application
│   │       ├── 📄 main.py         # Web server entry point
│   │       ├── 📄 websocket.py    # WebSocket handlers
│   │       │
│   │       └── 📁 frontend/       # React/Next.js frontend
│   │           ├── 📁 src/
│   │           ├── 📁 public/
│   │           └── 📄 package.json
│   │
│   └── 📁 utils/                   # Shared utilities
│       ├── 📄 __init__.py
│       ├── 📄 validators.py        # Input validators
│       ├── 📄 formatters.py        # Output formatters
│       └── 📄 helpers.py           # Helper functions
│
├── 📁 bin/                         # Executable entry points
│   ├── 📄 research-agent           # CLI executable
│   └── 📄 research-agent-server    # API server executable
│
└── 📁 migrations/                  # Alembic database migrations
    ├── 📄 alembic.ini             # Alembic configuration
    ├── 📄 env.py                  # Migration environment
    ├── 📄 script.py.mako          # Migration template
    └── 📁 versions/               # Migration files
        └── 📄 001_initial.py      # Initial migration
```

---

## 🧪 Tests (`tests/`)

**Purpose:** Contains ALL test files. Tests mirror the source structure.

```
tests/
├── 📄 __init__.py
├── 📄 conftest.py                 # Shared pytest fixtures
│
├── 📁 unit/                       # Unit tests (isolated)
│   ├── 📄 __init__.py
│   ├── 📁 domain/                # Domain model tests
│   │   ├── 📄 test_research.py
│   │   └── 📄 test_session.py
│   ├── 📁 services/              # Service layer tests
│   │   ├── 📄 test_azure_agent.py
│   │   └── 📄 test_cost_service.py
│   └── 📁 utils/                 # Utility tests
│       └── 📄 test_validators.py
│
├── 📁 integration/               # Integration tests (with dependencies)
│   ├── 📄 __init__.py
│   ├── 📄 conftest.py           # Integration test fixtures
│   ├── 📁 api/                  # API integration tests
│   │   └── 📄 test_research_endpoints.py
│   ├── 📁 database/             # Database integration tests
│   │   └── 📄 test_repositories.py
│   └── 📁 external/             # External API tests
│       └── 📄 test_brave_search.py
│
├── 📁 e2e/                      # End-to-end tests
│   ├── 📄 __init__.py
│   ├── 📄 test_research_flow.py # Full research workflow
│   └── 📄 test_cli_commands.py  # CLI command tests
│
└── 📁 fixtures/                 # Test data and mocks
    ├── 📁 data/                # Test data files
    │   └── 📄 sample_data.json
    └── 📁 mocks/               # Mock implementations
        └── 📄 azure_mocks.py
```

---

## 📚 Documentation (`docs/`)

**Purpose:** ALL project documentation except code comments. MUST maintain strict hierarchy.

### Mandatory Structure with README Navigation

```
docs/
├── 📄 README.md                   # Main documentation hub (MANDATORY)
│
├── 📁 guides/                     # Development and usage guides
│   ├── 📄 README.md              # Guide to all guides (MANDATORY)
│   ├── 📄 DIRECTORY_STRUCTURE_GUIDE.md  # This file
│   ├── 📄 MARKDOWN_STYLE_GUIDE.md       # Markdown standards
│   ├── 📄 DEVELOPMENT_GUIDE.md          # Development setup
│   ├── 📄 TESTING_GUIDE.md             # Testing guidelines
│   ├── 📄 CONTRIBUTING_GUIDE.md        # Contribution guidelines
│   └── 📄 CODE_REVIEW_GUIDE.md         # Code review standards
│
├── 📁 api/                        # API documentation
│   ├── 📄 README.md              # API documentation index (MANDATORY)
│   ├── 📄 openapi.json           # OpenAPI specification
│   ├── 📄 postman_collection.json # Postman collection
│   ├── 📁 endpoints/             # Endpoint documentation
│   │   ├── 📄 research.md       # Research endpoints
│   │   ├── 📄 sessions.md       # Session endpoints
│   │   └── 📄 health.md         # Health check endpoints
│   └── 📁 examples/              # API usage examples
│       ├── 📄 python_client.md  # Python client examples
│       └── 📄 curl_examples.md  # cURL examples
│
├── 📁 architecture/              # System design documentation
│   ├── 📄 README.md             # Architecture overview (MANDATORY)
│   ├── 📄 SYSTEM_DESIGN.md      # Overall system design
│   ├── 📄 DATABASE_DESIGN.md    # Database schema
│   ├── 📄 SECURITY_DESIGN.md    # Security architecture
│   ├── 📁 diagrams/             # Architecture diagrams
│   │   ├── 📄 system_flow.mermaid
│   │   ├── 📄 data_flow.mermaid
│   │   └── 📄 deployment.mermaid
│   └── 📁 decisions/            # Architecture Decision Records
│       ├── 📄 ADR-001-azure-first.md
│       └── 📄 ADR-002-clean-architecture.md
│
├── 📁 deployment/               # Deployment and operations
│   ├── 📄 README.md            # Deployment overview (MANDATORY)
│   ├── 📁 azure/               # Azure-specific deployment
│   │   ├── 📄 AZURE_SETUP.md
│   │   ├── 📄 AZURE_RESOURCES.md
│   │   └── 📄 AZURE_MONITORING.md
│   ├── 📁 docker/              # Container deployment
│   │   ├── 📄 DOCKER_BUILD.md
│   │   └── 📄 DOCKER_DEPLOY.md
│   └── 📁 kubernetes/          # K8s deployment
│       ├── 📄 K8S_SETUP.md
│       └── 📄 K8S_OPERATIONS.md
│
├── 📁 user-guide/              # End-user documentation
│   ├── 📄 README.md           # User guide index (MANDATORY)
│   ├── 📄 GETTING_STARTED.md  # Quick start guide
│   ├── 📄 CLI_USAGE.md        # CLI documentation
│   ├── 📄 WEB_USAGE.md        # Web interface guide
│   └── 📄 FAQ.md              # Frequently asked questions
│
└── 📁 reference/              # Technical reference
    ├── 📄 README.md          # Reference index (MANDATORY)
    ├── 📄 CONFIGURATION.md   # Configuration reference
    ├── 📄 ENVIRONMENT_VARS.md # Environment variables
    ├── 📄 ERROR_CODES.md     # Error code reference
    └── 📄 GLOSSARY.md        # Technical terms glossary
```

---

## 🏗️ Infrastructure (`infrastructure/`)

**Purpose:** Infrastructure as Code and deployment configurations.

```
infrastructure/
├── 📄 README.md
│
├── 📁 docker/                    # Docker configurations
│   ├── 📄 Dockerfile            # Application Dockerfile
│   ├── 📄 docker-compose.yml   # Local development
│   └── 📄 docker-compose.prod.yml # Production setup
│
├── 📁 kubernetes/               # Kubernetes manifests
│   ├── 📁 base/               # Base configurations
│   │   ├── 📄 deployment.yaml
│   │   ├── 📄 service.yaml
│   │   └── 📄 configmap.yaml
│   └── 📁 overlays/           # Environment-specific
│       ├── 📁 dev/
│       └── 📁 prod/
│
└── 📁 terraform/              # Terraform/Bicep IaC
    ├── 📁 modules/           # Reusable modules
    │   ├── 📁 azure_openai/
    │   └── 📁 azure_sql/
    └── 📁 environments/      # Environment configs
        ├── 📁 dev/
        └── 📁 prod/
```

---

## 🔧 Scripts (`scripts/`)

**Purpose:** Automation and utility scripts. MUST maintain strict hierarchy.

### Mandatory Structure

```
scripts/
├── 📄 README.md                 # Script documentation hub (MANDATORY)
│
├── 📁 setup/                    # Environment setup scripts
│   ├── 📄 README.md            # Setup scripts guide (MANDATORY)
│   ├── 📄 setup_venv.py        # Virtual environment setup
│   ├── 📄 install_deps.sh      # Dependency installation
│   ├── 📄 detect_platform.py   # Platform detection
│   ├── 📄 setup_azure.py       # Azure resource setup
│   └── 📄 init_database.py     # Database initialization
│
├── 📁 deployment/              # Deployment automation
│   ├── 📄 README.md           # Deployment scripts guide (MANDATORY)
│   ├── 📁 azure/              # Azure deployment scripts
│   │   ├── 📄 deploy_app.sh
│   │   ├── 📄 deploy_infra.sh
│   │   └── 📄 configure_monitoring.py
│   ├── 📁 docker/             # Docker deployment scripts
│   │   ├── 📄 build_images.sh
│   │   └── 📄 push_registry.sh
│   └── 📁 kubernetes/         # K8s deployment scripts
│       ├── 📄 deploy_k8s.sh
│       └── 📄 rollback_k8s.sh
│
├── 📁 maintenance/            # System maintenance scripts
│   ├── 📄 README.md          # Maintenance guide (MANDATORY)
│   ├── 📁 database/          # Database maintenance
│   │   ├── 📄 backup_db.sh
│   │   ├── 📄 restore_db.sh
│   │   └── 📄 migrate_db.py
│   ├── 📁 cleanup/           # Cleanup operations
│   │   ├── 📄 clean_logs.py
│   │   ├── 📄 clean_cache.py
│   │   └── 📄 clean_temp.sh
│   └── 📁 monitoring/        # Monitoring scripts
│       ├── 📄 check_health.py
│       └── 📄 collect_metrics.py
│
├── 📁 development/           # Development utilities
│   ├── 📄 README.md         # Development tools guide (MANDATORY)
│   ├── 📁 code-generation/  # Code generation scripts
│   │   ├── 📄 generate_api_docs.py
│   │   ├── 📄 generate_types.py
│   │   └── 📄 generate_client.py
│   ├── 📁 testing/          # Test utilities
│   │   ├── 📄 seed_database.py
│   │   ├── 📄 generate_fixtures.py
│   │   └── 📄 run_coverage.sh
│   └── 📁 linting/          # Code quality scripts
│       ├── 📄 run_linters.sh
│       ├── 📄 format_code.py
│       └── 📄 check_imports.py
│
└── 📁 automation/           # CI/CD and automation
    ├── 📄 README.md        # Automation guide (MANDATORY)
    ├── 📄 run_ci.sh       # CI pipeline script
    ├── 📄 run_cd.sh       # CD pipeline script
    └── 📄 validate_pr.py  # PR validation
```

---

## ⚙️ Configuration (`config/`)

**Purpose:** Application configuration files (not code). MUST maintain strict hierarchy.

### Mandatory Structure

```
config/
├── 📄 README.md                 # Configuration guide (MANDATORY)
│
├── 📁 application/             # Application-specific configs
│   ├── 📄 README.md           # App config guide (MANDATORY)
│   ├── 📄 mcp_servers.json    # MCP server configurations
│   ├── 📄 logging.yaml        # Logging configuration
│   ├── 📄 rate_limits.json    # Rate limiting rules
│   ├── 📄 features.json       # Feature flags
│   └── 📄 security.yaml       # Security settings
│
├── 📁 environments/           # Environment-specific configs
│   ├── 📄 README.md          # Environment guide (MANDATORY)
│   ├── 📁 development/       # Development environment
│   │   ├── 📄 app.yaml
│   │   ├── 📄 database.yaml
│   │   └── 📄 services.yaml
│   ├── 📁 staging/           # Staging environment
│   │   ├── 📄 app.yaml
│   │   ├── 📄 database.yaml
│   │   └── 📄 services.yaml
│   └── 📁 production/        # Production environment
│       ├── 📄 app.yaml
│       ├── 📄 database.yaml
│       └── 📄 services.yaml
│
├── 📁 azure/                 # Azure-specific configurations
│   ├── 📄 README.md         # Azure config guide (MANDATORY)
│   ├── 📄 resources.json    # Azure resource definitions
│   ├── 📄 credentials.json.template # Credential template
│   └── 📄 regions.yaml      # Regional configurations
│
└── 📁 templates/            # Configuration templates
    ├── 📄 README.md        # Template guide (MANDATORY)
    ├── 📄 env.template     # Environment variable template
    ├── 📄 docker.template  # Docker config template
    └── 📄 k8s.template     # Kubernetes config template
```

---

## 📖 Examples (`examples/`)

**Purpose:** Reference implementations. NEVER imported by main code. MUST maintain strict hierarchy.

### Mandatory Structure

```
examples/
├── 📄 README.md                 # Examples overview (MANDATORY)
│
├── 📁 quickstart/              # Getting started examples
│   ├── 📄 README.md           # Quickstart guide (MANDATORY)
│   ├── 📄 01_hello_world.py   # Minimal example
│   ├── 📄 02_basic_research.py # Basic research
│   ├── 📄 03_with_config.py   # With configuration
│   └── 📄 requirements.txt    # Example dependencies
│
├── 📁 use-cases/              # Real-world use cases
│   ├── 📄 README.md          # Use cases guide (MANDATORY)
│   ├── 📁 cli-application/   # CLI app example
│   │   ├── 📄 main.py
│   │   ├── 📄 config.yaml
│   │   └── 📄 README.md
│   ├── 📁 web-service/       # Web service example
│   │   ├── 📄 app.py
│   │   ├── 📄 Dockerfile
│   │   └── 📄 README.md
│   └── 📁 batch-processing/  # Batch job example
│       ├── 📄 processor.py
│       ├── 📄 scheduler.py
│       └── 📄 README.md
│
├── 📁 integrations/          # Third-party integrations
│   ├── 📄 README.md         # Integration guide (MANDATORY)
│   ├── 📁 slack/           # Slack integration
│   │   ├── 📄 bot.py
│   │   ├── 📄 handlers.py
│   │   └── 📄 README.md
│   ├── 📁 teams/           # Teams integration
│   │   ├── 📄 bot.py
│   │   ├── 📄 cards.py
│   │   └── 📄 README.md
│   └── 📁 discord/         # Discord integration
│       ├── 📄 bot.py
│       ├── 📄 commands.py
│       └── 📄 README.md
│
├── 📁 advanced/             # Advanced patterns
│   ├── 📄 README.md        # Advanced guide (MANDATORY)
│   ├── 📁 multi-agent/     # Multi-agent systems
│   │   ├── 📄 orchestrator.py
│   │   ├── 📄 agents.py
│   │   └── 📄 README.md
│   ├── 📁 custom-tools/    # Custom tool creation
│   │   ├── 📄 tool_builder.py
│   │   ├── 📄 tool_registry.py
│   │   └── 📄 README.md
│   └── 📁 performance/     # Performance optimization
│       ├── 📄 caching.py
│       ├── 📄 parallel.py
│       └── 📄 README.md
│
└── 📁 notebooks/           # Jupyter notebooks
    ├── 📄 README.md       # Notebook guide (MANDATORY)
    ├── 📄 01_exploration.ipynb
    ├── 📄 02_analysis.ipynb
    └── 📄 03_visualization.ipynb
```

---

## 📊 Project Tracking (`project_tracking/`)

**Purpose:** Project management and tracking. MUST maintain strict hierarchy.

### Mandatory Structure

```
project_tracking/
├── 📄 README.md                 # Project tracking hub (MANDATORY)
├── 📄 PROJECT_STATUS.md        # Current overall status
├── 📄 CHANGELOG.md            # Version history
│
├── 📁 planning/               # Project planning
│   ├── 📄 README.md          # Planning guide (MANDATORY)
│   ├── 📄 ROADMAP.md         # Project roadmap
│   ├── 📄 MILESTONES.md      # Major milestones
│   ├── 📁 sprints/           # Sprint planning
│   │   ├── 📄 SPRINT_01.md
│   │   ├── 📄 SPRINT_02.md
│   │   └── 📄 SPRINT_CURRENT.md
│   ├── 📁 epics/             # Epic tracking
│   │   ├── 📄 EPIC_001_CORE.md
│   │   └── 📄 EPIC_002_UI.md
│   └── 📁 backlog/           # Feature backlog
│       ├── 📄 FEATURES.md
│       ├── 📄 IMPROVEMENTS.md
│       └── 📄 TECH_DEBT.md
│
├── 📁 tasks/                 # Task management
│   ├── 📄 README.md         # Task guide (MANDATORY)
│   ├── 📄 TASK_BOARD.md     # Active task board
│   ├── 📁 active/           # Currently active tasks
│   │   ├── 📄 CRITICAL.md
│   │   ├── 📄 HIGH.md
│   │   └── 📄 NORMAL.md
│   ├── 📁 completed/        # Completed tasks archive
│   │   ├── 📄 2024_Q4.md
│   │   └── 📄 2025_Q1.md
│   └── 📁 blocked/          # Blocked tasks
│       └── 📄 BLOCKED.md
│
├── 📁 decisions/            # Decision records
│   ├── 📄 README.md        # Decision guide (MANDATORY)
│   ├── 📁 technical/       # Technical decisions
│   │   ├── 📄 TDR_001_FRAMEWORK.md
│   │   └── 📄 TDR_002_DATABASE.md
│   ├── 📁 business/        # Business decisions
│   │   └── 📄 BDR_001_PRICING.md
│   └── 📁 process/         # Process decisions
│       └── 📄 PDR_001_WORKFLOW.md
│
├── 📁 meetings/            # Meeting records
│   ├── 📄 README.md       # Meeting guide (MANDATORY)
│   ├── 📁 standup/        # Daily standups
│   │   └── 📄 2024_12.md
│   ├── 📁 planning/       # Planning meetings
│   │   └── 📄 2024_Q4.md
│   └── 📁 retrospective/  # Sprint retrospectives
│       └── 📄 SPRINT_01_RETRO.md
│
└── 📁 metrics/            # Project metrics
    ├── 📄 README.md      # Metrics guide (MANDATORY)
    ├── 📄 VELOCITY.md    # Team velocity
    ├── 📄 BURNDOWN.md    # Sprint burndown
    └── 📄 KPI.md         # Key performance indicators
```

---

## 📝 File Naming Conventions

### Python Files
- **Modules:** `snake_case.py` (e.g., `azure_agent.py`)
- **Classes:** Inside modules use `PascalCase` (e.g., `class AzureAgent`)
- **Tests:** `test_<module_name>.py` (e.g., `test_azure_agent.py`)
- **Constants:** `UPPER_SNAKE_CASE` in `constants.py`

### Configuration Files
- **YAML:** `snake_case.yaml` (e.g., `logging_config.yaml`)
- **JSON:** `snake_case.json` (e.g., `mcp_servers.json`)
- **Environment:** `.env`, `.env.example`, `.env.<environment>`

### Documentation
- **Markdown:** `UPPER_SNAKE_CASE.md` for guides (e.g., `SETUP_GUIDE.md`)
- **Markdown:** `PascalCase.md` for specific docs (e.g., `ApiReference.md`)

### Scripts
- **Python:** `snake_case.py` (e.g., `setup_venv.py`)
- **Shell:** `snake_case.sh` (e.g., `deploy_azure.sh`)
- **Batch:** `snake_case.bat` (e.g., `setup_windows.bat`)

---

## 🎯 What Goes Where - Quick Reference

| File Type | Location | Example |
|-----------|----------|---------|
| **Python business logic** | `src/azure_research_agent/services/` | `research_service.py` |
| **API endpoints** | `src/azure_research_agent/api/v1/endpoints/` | `research.py` |
| **Domain models** | `src/azure_research_agent/domain/` | `research.py` |
| **Database models** | `src/azure_research_agent/infrastructure/database/` | `models.py` |
| **External API clients** | `src/azure_research_agent/infrastructure/external_apis/` | `brave_search.py` |
| **Azure integrations** | `src/azure_research_agent/infrastructure/azure/` | `openai_client.py` |
| **CLI commands** | `src/azure_research_agent/presentation/cli/` | `commands.py` |
| **Unit tests** | `tests/unit/<mirror_of_src>` | `test_research_service.py` |
| **Integration tests** | `tests/integration/` | `test_api_endpoints.py` |
| **Docker files** | `infrastructure/docker/` | `Dockerfile` |
| **K8s manifests** | `infrastructure/kubernetes/` | `deployment.yaml` |
| **Setup scripts** | `scripts/setup/` | `setup_venv.py` |
| **API documentation** | `docs/api/` | `openapi.json` |
| **Guides** | `docs/guides/` | `DEVELOPMENT_GUIDE.md` |
| **Environment config** | Project root | `.env`, `.env.example` |
| **Python config** | Project root | `pyproject.toml` |
| **Task tracking** | `project_tracking/tasks/` | `TASK_BOARD.md` |

---

## ❌ Anti-Patterns - NEVER Do This

### 🚫 NEVER Place Files:
- ❌ Test files in `src/` directory
- ❌ Source code in `tests/` directory
- ❌ Documentation in source code directories (except docstrings)
- ❌ Configuration code in `config/` (use `src/azure_research_agent/core/config.py`)
- ❌ Business logic in `infrastructure/`
- ❌ Infrastructure code in `domain/`
- ❌ Multiple entry points in project root
- ❌ Hardcoded credentials anywhere
- ❌ Generated files in version control
- ❌ Third-party code in `src/`

### 🚫 NEVER Create:
- ❌ Ambiguous file names (e.g., `utils.py`, `helpers.py` without context)
- ❌ Duplicate functionality in different locations
- ❌ Circular dependencies between layers
- ❌ Mixed responsibilities in a single module
- ❌ Files larger than 500 lines
- ❌ Deeply nested directory structures (max 4 levels)

---

## ✅ Validation Checklist

Before creating a new file or folder, verify:

- [ ] I've checked this guide for the correct location
- [ ] The file has a single, clear purpose
- [ ] The name follows naming conventions
- [ ] No similar file exists elsewhere
- [ ] It's in the architecturally correct layer
- [ ] Tests will go in the corresponding test directory
- [ ] Documentation needs are considered
- [ ] The path is no more than 4 levels deep

---

## 🔄 Keeping This Guide Updated

This guide is the **single source of truth** for directory structure. When structural changes are needed:

1. Update this guide FIRST
2. Implement the changes
3. Update all affected documentation
4. Notify the team

---

**Last Updated:** 2024-12-27  
**Version:** 2.0.0  
**Maintainer:** Azure Research Agent Team

---

## 📌 Remember

> **"A place for everything, and everything in its place."**

When in doubt, refer to this guide. If something isn't covered, it probably shouldn't exist, or this guide needs updating.
