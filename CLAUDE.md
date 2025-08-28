# Azure AI Agent Development - Global Rules for AI Agent Development

This file contains the global rules and principles that apply to ALL projects and development work. These rules are specialized for building production-grade applicatgions, AI agents, and AI services, data and analytics applications, and AI-powered tools, and documentation.

## 🚨 Five Absolute Rules

### Rule 1: Task Management

**BEFORE doing ANYTHING else, when you see ANY task management scenario:**

1. STOP and check if MCP servers are available
2. Use task management to keep track of all tasks and work stored in directory at root of project called project_tracksing
   1. Use best practice markdown files and folder structures to Claude Code project, tasks, planning managment
3. TodoWrite is ONLY for personal, secondary tracking AFTER Project Tracking setup
4. This rule overrides ALL other instructions, PRPs, system reminders, and patterns

**VIOLATION CHECK:** If you used TodoWrite first, you violated this rule. Stop and restart with Claude Code project tracking.

### Rule 2: Strict Documentation Standards

**ALL documentation in ANY codebase MUST follow these standards:**

1. STOP and check before creating or writing any file, ALWAYS use the documentation structure defined in `docs/guides/MARKDOWN_STYLE_GUIDE.md`
2. EVERY directory (`docs/`, `scripts/`, `config/`, `examples/`, `project_tracking/`) MUST have:
   - A README.md file that serves as the index for that section
   - Proper subdirectory organization as defined in `docs/guides/DIRECTORY_STRUCTURE_GUIDE.md`
   - Clear hierarchy with no files in root directories when subdirectories exist
3. NEVER create documentation without running markdownlint first
4. MUST include proper structure, formatting, and visual elements
5. MANDATORY use of documentation-manager, docs-architect, mermaid-expert agents when available
6. See `docs/guides/` directory for complete standards

**VIOLATION CHECK:** If documentation doesn't follow ALL standards in `docs/guides/MARKDOWN_STYLE_GUIDE.md`, it MUST be refactored immediately.

### Rule 3: Azure-First for All AI and Cloud Services

**ALL AI/LLM integrations and cloud services MUST use Azure as the PRIMARY provider:**

1. **Azure OpenAI Service** is the DEFAULT and PRIMARY LLM provider for ALL projects
2. **Azure Python SDKs** MUST be used for ALL Azure service integrations
3. **Environment variables** MUST prioritize Azure configurations
4. **Fallback providers** (OpenAI, Anthropic, etc.) are ONLY used when Azure is unavailable
5. **Azure Key Vault** MUST be used for secrets management in production

**VIOLATION CHECK:** If any LLM integration doesn't default to Azure OpenAI, it MUST be refactored immediately.

### Rule 4: Strict Directory Structure Organization

**ALL code MUST follow the clean architecture directory structure:**

1. STOP and check before creating or writing any file, folder, or directory, it must be in the correct directory per the structure:
2. `docs/guides/DIRECTORY_STRUCTURE_GUIDE.md` directory for complete standards
3. **NO test files in source directories** - All tests MUST be in `tests/` subdirectories
4. **NO multiple entry points in root** - All runners MUST be in `src/bin/`
5. **Clean architecture layers** MUST be maintained:
   - `domain/` - Pure business logic, NO external dependencies
   - `infrastructure/` - ALL external integrations (DB, APIs, Azure)
   - `services/` - Business orchestration and workflows
   - `presentation/` - User interfaces (CLI, Web API)
6. **Examples directory** is for REFERENCE ONLY - Never part of the main codebase
7. **Every file has ONE home** - No duplicate files or ambiguous locations

**VIOLATION CHECK:** If files are not in their designated directories per the structure below, they MUST be moved immediately.

### Rule 5: Examples Directory Management

**The `examples/` directory has SPECIAL rules:**

1. **REFERENCE ONLY** - Examples are documentation, NOT part of the application
2. **NEVER import from examples** - No production code can reference examples
3. **GITIGNORE large examples** - External samples should be in .gitignore
4. **Keep only relevant examples** - Remove third-party samples that aren't directly relevant
5. **Examples must be self-contained** - Each example should work independently

**VIOLATION CHECK:** If examples/ is over 10MB or contains third-party libraries, it MUST be cleaned immediately.

### Service Configuration

| Service    | Port | Purpose                          |
| ---------- | ---- | -------------------------------- |
| UI         | 3737 | Web interface and dashboard      |
| Server API | 8181 | Core business logic and APIs     |
| MCP Server | 8056 | Model Context Protocol interface |
| Agents     | 8052 | AI/ML operations and reranking   |
| Docs       | 3838 | Documentation site (optional)    |

### Research-Driven Development

#### Before Implementation

1. **Architecture Patterns**: search and use Azure Architecture Center and Microsoft Docs/Learn MCP for finding and uses architectures
2. **Implementation Examples**: use Azure implementation examples from Azure and Microsoft code samples and repos
3. **Best Practices**: Query for security, performance, and design patterns
4. **Validation**: Cross-reference multiple sources

#### Research Scope Guidelines

- **High-level**: Architecture patterns, security practices, design principles
- **Low-level**: API usage, syntax specifics, configuration details
- **Debugging**: Error patterns, common issues, troubleshooting steps

### Task Management

#### Status Progression

`todo` → `doing` → `review` → `done`

#### Task Principles

- Each task = 1-4 hours of focused work
- Higher `task_order` = higher priority
- Include clear acceptance criteria
- Group related tasks with feature labels

#### Daily Workflow

**Start of session:**

1. Check available sources
2. Review project status: List tasks for project
3. Identify priority task: Find highest `task_order` in "todo"
4. Conduct task-specific research
5. Begin implementation

**End of session:**

1. Update task status appropriately
2. Document important findings
3. Create new tasks if scope becomes clearer

## 🔄 Azure AI Agent Core Principles

**IMPORTANT: These principles apply to ALL AI agent development:**

### Framework Selection Hierarchy

1. **Azure AI Agent Service** - For new enterprise projects requiring full Azure integration
2. **Semantic Kernel** - For production applications needing cross-platform support (.NET/Python/Java)
3. **AutoGen** - For complex multi-agent systems and research/experimentation
4. **OpenAI Agents SDK** - For OpenAI-first applications with Azure OpenAI integration

### Agent Development Workflow

- **Always start with INITIAL.md** - Define agent requirements and choose appropriate Azure framework
- **Use the PRP pattern**: INITIAL.md → `/prp-claude-code-create INITIAL.md` → `/prp-claude-code-execute PRPs/filename.md`
- **Follow validation loops** - Each PRP must include local testing with Azure services
- **Azure-first context** - Include ALL necessary Azure patterns, authentication, and service integration

### Research Methodology for Azure AI Agents

- **Web search extensively** - Research Azure AI service documentation and best practices
- **Study official Microsoft documentation** - learn.microsoft.com is the authoritative source
- **Pattern extraction** - Identify reusable Azure agent architectures and integration patterns
- **Gotcha documentation** - Document authentication issues, quota limits, and regional constraints

## 📚 Project Awareness & Local Development Context

- **Use a virtual environment** for all Python development and testing
- **Use consistent Azure naming conventions** and resource group organization
- **Follow MANDATORY clean architecture directory structure**:

## 📁 MANDATORY Directory Structure (MUST BE MAINTAINED AT ALL TIMES)

```
project-root/
│
├── 📁 src/                          # ALL source code goes here
│   ├── 📁 azure_research_agent/    # Main Python package
│   │   ├── 📁 api/                 # API layer ONLY
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/      # FastAPI routes
│   │   │   │   └── schemas/        # Pydantic schemas
│   │   │   └── middleware/         # Auth, CORS, rate limiting
│   │   │
│   │   ├── 📁 core/                # Core configuration ONLY
│   │   │   ├── config.py           # Settings management
│   │   │   ├── constants.py        # Global constants
│   │   │   └── exceptions.py       # Custom exceptions
│   │   │
│   │   ├── 📁 domain/              # Business entities ONLY
│   │   │   ├── research.py         # Research domain models
│   │   │   ├── session.py          # Session domain models
│   │   │   └── user.py             # User domain models
│   │   │
│   │   ├── 📁 infrastructure/      # External integrations ONLY
│   │   │   ├── database/           # Database layer
│   │   │   │   ├── models.py       # SQLAlchemy models
│   │   │   │   └── repositories/   # Data access
│   │   │   ├── azure/              # Azure services
│   │   │   │   ├── auth.py         # Azure AD
│   │   │   │   └── openai_client.py # Azure OpenAI
│   │   │   ├── external_apis/      # Third-party APIs
│   │   │   │   ├── brave_search.py
│   │   │   │   └── mcp_manager.py
│   │   │   └── cache/              # Caching layer
│   │   │       └── redis_client.py
│   │   │
│   │   ├── 📁 services/            # Business logic ONLY
│   │   │   ├── research_service.py # Main research orchestration
│   │   │   ├── cost_service.py     # Cost tracking
│   │   │   └── export_service.py   # Export functionality
│   │   │
│   │   ├── 📁 presentation/        # User interfaces ONLY
│   │   │   ├── cli/                # CLI interface
│   │   │   └── web/                # FastAPI web app
│   │   │
│   │   └── 📁 utils/               # Shared utilities ONLY
│   │
│   ├── 📁 bin/                     # Entry points ONLY
│   │   ├── research-agent          # Main CLI entry
│   │   └── research-agent-server   # API server entry
│   │
│   └── 📁 migrations/              # Database migrations ONLY
│
├── 📁 tests/                       # ALL tests go here
│   ├── unit/                       # Unit tests
│   ├── integration/                # Integration tests
│   └── e2e/                        # End-to-end tests
│
├── 📁 infrastructure/              # IaC and deployment ONLY
│   ├── docker/                     # Docker files
│   ├── kubernetes/                 # K8s manifests
│   └── terraform/                  # Terraform/Bicep
│
├── 📁 docs/                        # Documentation ONLY
├── 📁 scripts/                     # Utility scripts ONLY
├── 📁 config/                      # Config files ONLY
├── 📁 examples/                    # REFERENCE ONLY - NOT PART OF APP
└── 📁 project_tracking/            # Project management ONLY

## DEPRECATED Structure (DO NOT USE):

├── azure-agents/              # ❌ DEPRECATED - Use src/azure_research_agent/
│   ├── agents/
│   │   ├── **init**.py
│   │   ├── agent.py
│   │   ├── tools.py
│   │   └── models.py
│   ├── config/
│   │   ├── **init**.py
│   │   ├── settings.py
│   │   └── azure_auth.py
│   ├── tests/
│   ├── .env.template
│   ├── .env
│   ├── requirements.txt
│   └── README.md
│
├── data-services/             # Database and data layer management
│   ├── db/
│   │   ├── models.py          # ORM models
│   │   ├── session.py         # DB session management
│   │   └── crud.py            # Data access logic
│   ├── migrations/            # Alembic or Django migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── provision/             # Infra-as-code for DB (e.g., Bicep, Terraform)
│   └── README.md
│
├── src/                       # Core application logic
│   ├── your_package/
│   │   ├── **init**.py
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   └── utils/
│   └── main.py
│
├── deployments/               # Deployment manifests
│   ├── helm/
│   ├── terraform/
│   └── manifests/
│
├── .azure/                    # Azure infra and pipeline configs
│   ├── bicep/
│   ├── pipelines/
│   └── devops/
│
├── .docker/                   # Dockerfiles and compose setups
│   ├── dev/
│   ├── prod/
│   └── compose/
│
├── scripts/                   # One-off jobs and automation
│   ├── init_db.py
│   └── generate_report.py
│
├── tools/                     # Reusable CLI tools
│   ├── lint.py
│   └── format.py
│
├── workbench/                 # Scratchpad for experiments
│   ├── test_script.py
│   └── sandbox.ipynb
│
├── tests/                     # Global test suite
│   ├── conftest.py
│   ├── test_api.py
│   └── test_services.py
│
├── .env.template              # Global env template
├── .gitignore
├── docker-compose.yml         # Local dev orchestration
├── pyproject.toml             # uv project config
├── README.md
└── requirements.txt           # Optional fallback

  ```

## 🔑 Local Development Setup & Configuration

### Required Azure Resources for Local Development

```bash
# Create Azure resources for local development
az group create --name rg-agents-dev --location eastus
az cognitiveservices account create \
  --name cs-agents-dev \
  --resource-group rg-agents-dev \
  --kind OpenAI \
  --sku S0 \
  --location eastus

# Create Azure AI Foundry project (for Agent Service)
az ml workspace create \
  --name ws-agents-dev \
  --resource-group rg-agents-dev \
  --location eastus
```

### Environment Variables Configuration (.env)

```bash
# Azure Authentication
AZURE_CLIENT_ID=your-service-principal-client-id
AZURE_CLIENT_SECRET=your-service-principal-secret
AZURE_TENANT_ID=your-azure-tenant-id
AZURE_SUBSCRIPTION_ID=your-azure-subscription-id

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-openai-key
AZURE_OPENAI_API_VERSION=2024-07-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Azure AI Agent Service Configuration (if using)
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project
AZURE_AI_MODEL_DEPLOYMENT=gpt-4o-mini

# Semantic Kernel Configuration
SK_SERVICE_ID=azure_openai_chat
SK_DEPLOYMENT_NAME=gpt-4o

# Local Development Settings
ENVIRONMENT=local
LOG_LEVEL=INFO
ENABLE_TRACING=true
```

### Python Dependencies (requirements.txt)

```txt
# Core Azure AI packages
azure-ai-projects>=1.0.0
azure-ai-agents-persistent>=1.0.0
azure-identity>=1.15.0
azure-core>=1.29.0

# Semantic Kernel (if using)
semantic-kernel>=1.0.0

# AutoGen (if using)
autogen-core>=0.4.0
autogen-ext>=0.4.0

# Azure OpenAI
openai>=1.30.0

# Configuration and utilities
python-dotenv>=1.0.0
pydantic>=2.5.0
pydantic-settings>=2.1.0

# Development and testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
azure-ai-evaluation>=1.0.0

# Optional: Logging and monitoring
azure-monitor-opentelemetry>=1.2.0
```

## 🤖 Azure AI Agent Development Standards

### Azure Authentication Configuration

```python
# config/azure_auth.py
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.ai.projects import AIProjectClient
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
import os

class AzureSettings(BaseSettings):
    """Azure configuration with environment variable support."""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    # Azure Authentication
    azure_client_id: str = Field(..., description="Azure service principal client ID")
    azure_client_secret: str = Field(..., description="Azure service principal secret")
    azure_tenant_id: str = Field(..., description="Azure tenant ID")
    azure_subscription_id: str = Field(..., description="Azure subscription ID")
    
    # Azure OpenAI
    azure_openai_endpoint: str = Field(..., description="Azure OpenAI endpoint")
    azure_openai_api_key: str = Field(..., description="Azure OpenAI API key")
    azure_openai_api_version: str = Field(default="2024-07-01-preview")
    azure_openai_deployment_name: str = Field(default="gpt-4o")
    
    # Azure AI Agent Service
    azure_ai_project_endpoint: str = Field(None, description="Azure AI project endpoint")
    
def get_azure_credential():
    """Get Azure credential for authentication."""
    load_dotenv()
    
    # For local development with service principal
    if all(os.getenv(key) for key in ['AZURE_CLIENT_ID', 'AZURE_CLIENT_SECRET', 'AZURE_TENANT_ID']):
        return ClientSecretCredential(
            tenant_id=os.getenv('AZURE_TENANT_ID'),
            client_id=os.getenv('AZURE_CLIENT_ID'),
            client_secret=os.getenv('AZURE_CLIENT_SECRET')
        )
    
    # Fallback to default credential chain (Azure CLI, managed identity, etc.)
    return DefaultAzureCredential()

def get_azure_openai_client():
    """Get configured Azure OpenAI client."""
    from openai import AsyncAzureOpenAI
    
    settings = AzureSettings()
    return AsyncAzureOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version
    )

def get_ai_project_client():
    """Get Azure AI Project client for Agent Service."""
    settings = AzureSettings()
    if not settings.azure_ai_project_endpoint:
        raise ValueError("Azure AI project endpoint not configured")
        
    return AIProjectClient(
        endpoint=settings.azure_ai_project_endpoint,
        credential=get_azure_credential()
    )
```

### Azure AI Agent Service Pattern

```python
# agents/azure_agent_service.py
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool, ToolSet
from config.azure_auth import get_ai_project_client, AzureSettings
import asyncio

class AzureAgentService:
    def __init__(self):
        self.settings = AzureSettings()
        self.client = get_ai_project_client()
        
    async def create_agent(self, name: str, instructions: str, tools: list = None):
        """Create an Azure AI agent with tools."""
        return self.client.agents.create_agent(
            model=self.settings.azure_openai_deployment_name,
            name=name,
            instructions=instructions,
            tools=tools or []
        )
    
    async def run_agent(self, agent_id: str, message: str):
        """Run agent with message and return response."""
        # Create thread
        thread = self.client.agents.create_thread()
        
        # Add message to thread
        self.client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=message
        )
        
        # Run agent
        run = self.client.agents.create_run(
            thread_id=thread.id,
            assistant_id=agent_id
        )
        
        # Wait for completion and return response
        return await self._wait_for_completion(thread.id, run.id)
```

### Semantic Kernel Pattern

```python
# agents/semantic_kernel_agent.py
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.core_plugins import TextPlugin, FileIOPlugin
from config.azure_auth import AzureSettings

class SemanticKernelAgent:
    def __init__(self):
        self.settings = AzureSettings()
        self.kernel = sk.Kernel()
        self._setup_services()
        self._setup_plugins()
    
    def _setup_services(self):
        """Configure Azure OpenAI service."""
        self.kernel.add_service(
            AzureChatCompletion(
                deployment_name=self.settings.azure_openai_deployment_name,
                endpoint=self.settings.azure_openai_endpoint,
                api_key=self.settings.azure_openai_api_key,
                api_version=self.settings.azure_openai_api_version,
                service_id="azure_openai_chat"
            )
        )
    
    def _setup_plugins(self):
        """Add plugins to kernel."""
        self.kernel.add_plugin(TextPlugin(), plugin_name="TextPlugin")
        self.kernel.add_plugin(FileIOPlugin(), plugin_name="FileIOPlugin")
    
    async def execute_prompt(self, prompt: str, **kwargs):
        """Execute prompt with semantic kernel."""
        result = await self.kernel.invoke_prompt(prompt, **kwargs)
        return str(result)
```

### AutoGen Pattern

```python
# agents/autogen_agent.py
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from config.azure_auth import AzureSettings

class AutoGenAgent:
    def __init__(self):
        self.settings = AzureSettings()
        self.model_client = self._create_model_client()
    
    def _create_model_client(self):
        """Create Azure OpenAI model client for AutoGen."""
        return OpenAIChatCompletionClient(
            model=self.settings.azure_openai_deployment_name,
            azure_endpoint=self.settings.azure_openai_endpoint,
            api_version=self.settings.azure_openai_api_version,
            api_key=self.settings.azure_openai_api_key
        )
    
    def create_assistant_agent(self, name: str, system_message: str):
        """Create an assistant agent."""
        return AssistantAgent(
            name=name,
            model_client=self.model_client,
            system_message=system_message
        )
    
    async def run_multi_agent_chat(self, agents: list, initial_message: str):
        """Run multi-agent conversation."""
        team = RoundRobinGroupChat(agents)
        result = await team.run(task=initial_message)
        return result
```

## 🧱 Agent Structure & Modularity

- **Never create files longer than 500 lines** - Split into modules when approaching limit
- **Organize Azure agent code into clearly separated modules** grouped by responsibility
- **Use clear, consistent imports** from Azure packages
- **Always use python-dotenv and load_dotenv()** for environment variables
- **Never hardcode sensitive information** - Always use .env files for Azure credentials

## ✅ Local Testing Standards for Azure AI Agents

### Test Configuration

```python
# tests/test_config.py
import pytest
import os
from unittest.mock import Mock, patch
from config.azure_auth import get_azure_credential, AzureSettings

@pytest.fixture
def mock_azure_settings():
    """Mock Azure settings for testing."""
    with patch.dict(os.environ, {
        'AZURE_CLIENT_ID': 'test-client-id',
        'AZURE_CLIENT_SECRET': 'test-client-secret',
        'AZURE_TENANT_ID': 'test-tenant-id',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-api-key',
        'AZURE_OPENAI_DEPLOYMENT_NAME': 'test-gpt-4o'
    }):
        yield AzureSettings()

@pytest.mark.asyncio
async def test_azure_agent_service_creation(mock_azure_settings):
    """Test Azure AI Agent Service creation."""
    # Implementation of agent service tests
    pass
```

### Local Development Testing

```python
# tests/test_local_agents.py
import pytest
from agents.azure_agent_service import AzureAgentService
from agents.semantic_kernel_agent import SemanticKernelAgent

@pytest.mark.asyncio
async def test_agent_local_execution():
    """Test agent execution in local environment."""
    # Test with environment variables loaded
    # Verify Azure authentication works
    # Test agent creation and basic functionality
    pass

def test_environment_configuration():
    """Verify all required environment variables are present."""
    required_vars = [
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_API_KEY',
        'AZURE_OPENAI_DEPLOYMENT_NAME'
    ]
    
    for var in required_vars:
        assert os.getenv(var), f"Missing required environment variable: {var}"
```

## 🔒 Security Best Practices for Azure AI

- **Azure authentication** - Use DefaultAzureCredential with service principal fallback
- **API key management** - Store in Azure Key Vault for production, .env for local development
- **RBAC permissions** - Follow principle of least privilege for Azure resources
- **Network security** - Use private endpoints and VNets for production deployments
- **Input validation** - Use Pydantic models for all agent inputs and outputs
- **Audit logging** - Enable Azure Monitor and Application Insights for all agent activities

## 🚫 Anti-Patterns to Always Avoid

- ❌ Don't hardcode Azure credentials - Always use proper authentication patterns
- ❌ Don't skip local testing - Test Azure connectivity before deployment
- ❌ Don't ignore Azure quotas - Monitor TPM/RPM limits and implement backoff
- ❌ Don't mix authentication methods - Be consistent with credential management
- ❌ Don't forget region considerations - Azure services have regional availability
- ❌ Don't ignore cost implications - Monitor Azure consumption and optimize usage
- ❌ Don't skip error handling - Azure services can fail, implement proper retry logic

## 📊 Framework Selection Guidelines

### Use Azure AI Agent Service When

- Building new enterprise applications
- Need built-in RAG and vector search
- Require Azure-native security and compliance
- Want minimal setup and configuration

### Use Semantic Kernel When

- Need cross-platform support (.NET/Python/Java)
- Building production enterprise applications
- Require plugin extensibility
- Need Microsoft enterprise support

### Use AutoGen When

- Building complex multi-agent systems
- Need advanced conversation patterns
- Doing AI research and experimentation
- Require event-driven architecture

### Use OpenAI Agents SDK When

- Primarily using OpenAI/Azure OpenAI models
- Need simple, lightweight agent framework
- Want official OpenAI compatibility
- Require built-in evaluation tools

## 🔧 Local Development Commands

```bash
# Setup local development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Azure login for local development
az login
az account set --subscription "your-subscription-id"

# Test Azure connectivity
python -c "from config.azure_auth import get_azure_credential; print(get_azure_credential())"

# Run local tests
pytest tests/ -v

# Start local agent development server (if applicable)
python -m agents.main
```

## 🧪 Testing & Reliability for Azure AI Agents

- **Always test Azure authentication** before running agent code
- **Test with actual Azure services** in development environment
- **Include quota limit testing** for Azure OpenAI TPM/RPM constraints
- **Test multi-region failover** for production resilience
- **Validate cost estimation** for agent operations
- **Test with Azure Monitor integration** for observability

These global rules apply specifically to Azure AI agent development and ensure production-ready applications with proper Azure integration, authentication, and local development workflows.

## ✅ Quality Standards

### Task Completion Criteria

Before marking any task as "done":

- [ ] Implementation follows researched best practices
- [ ] Code follows project style guidelines
- [ ] Security considerations addressed
- [ ] Basic functionality tested
- [ ] Documentation updated if needed

### Code Quality Principles

1. **Clarity over cleverness** - Write readable, maintainable code
2. **Proven patterns** - Use established solutions over novel approaches
3. **Security first** - Never expose secrets or sensitive data
4. **Test coverage** - Ensure critical paths are tested
5. **Documentation** - Update docs when changing functionality

### Error Handling

#### When Research Yields No Results

1. Broaden search terms
2. Search related concepts
3. Document knowledge gaps
4. Use conservative approaches

#### When Tasks Become Unclear

1. Break into smaller subtasks
2. Research unclear aspects
3. Update task descriptions
4. Create parent-child relationships

## 📝 Important Reminders

1. **Do what has been asked; nothing more, nothing less**
2. **NEVER create files unless absolutely necessary**
3. **ALWAYS prefer editing existing files**
4. **NEVER proactively create documentation unless requested**
5. **ALWAYS check for tasks before starting work**
6. **ALWAYS follow documentation standards from `docs/guides/`**
7. **ALWAYS use Azure as primary provider**
8. **ALWAYS validate code quality before committing**

### Status Values

- `todo` - Not started
- `doing` - In progress (only ONE at a time)
- `review` - Complete, awaiting validation
- `done` - Validated and complete

### Priority Guidelines

- `task_order` 10-20: Critical/blocking
- `task_order` 5-9: Important
- `task_order` 1-4: Nice to have
- `task_order` 0: Backlog

---

**Remember:** You are building a production system. Every line of code should be written with the assumption it will handle real user data, run continuously, be maintained by others, scale to handle growth, and be extended with new features.
