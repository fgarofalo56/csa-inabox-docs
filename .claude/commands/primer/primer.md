# 🚀 Prime Claude Code Context - Project Initialization

## Context Management Strategy
> This primer follows best practices for context efficiency and token optimization.
> Use `/context` periodically to monitor token usage across components.

---

## Phase 1: Project Discovery & Structure Analysis

### 1.1 Initialize Project Understanding
Start by using the `tree` command to understand the overall project structure:
```bash
tree -L 3 -I 'node_modules|.git|dist|build|coverage'
```

### 1.2 Read Core Documentation (Priority Order)
Read files in this specific order to build context efficiently:

1. **CLAUDE.md** (if exists) - Primary context file for Claude Code
2. **README.md** - Project overview and setup
3. **CONTRIBUTING.md** - Development guidelines
4. **docs/** directory - Additional documentation

**Important**: Ask before reading large files (>1000 lines) to manage context wisely.

---

## Phase 2: MCP Server Integration & Tools

### 2.1 Available MCP Servers
Leverage these MCP servers strategically:
- **serena** - Codebase search and navigation
- **crawl4ai-rag** - Web content retrieval and analysis
- **microsoft-docs-mcp** - Microsoft/Azure documentation
- **MCP_DOCKER** - Docker operations

### 2.2 Serena Integration Check
**CRITICAL**: Verify Serena onboarding status:
```
Check if project is indexed in Serena knowledge base.
If not indexed: Request to onboard project to Serena.
If indexed: Proceed with codebase analysis.
```

### 2.3 Project Tracking Verification
Check Claude Code project tracking status:
```
Verify if project is configured in /project_tracking.
If not configured: Initialize project tracking.
Document current status for future reference.
```

---

## Phase 3: Configuration & Dependencies Analysis

### 3.1 Read Configuration Files
Examine these files to understand project setup:

**Package Management**:
- `package.json` / `package-lock.json` (Node.js)
- `requirements.txt` / `setup.py` / `pyproject.toml` (Python)
- `Cargo.toml` (Rust)
- `go.mod` (Go)
- `pom.xml` / `build.gradle` (JVM)

**Environment & Deployment**:
- `.env.example` / `.env.template`
- `Dockerfile` / `docker-compose.yml`
- `.github/workflows/` (CI/CD)
- `azure-pipelines.yml` / `cloudbuild.yaml`

**Code Quality**:
- `.eslintrc.*` / `tsconfig.json`
- `pytest.ini` / `tox.ini`
- `.editorconfig`

### 3.2 Dependency Analysis
Identify:
- Core dependencies and their versions
- Deprecated or outdated packages
- Security vulnerabilities (if scan results available)
- Missing or optional dependencies

---

## Phase 4: Codebase Deep Dive

### 4.1 Strategic File Reading
**Use Serena for efficient search** - Avoid reading unnecessary files:

```
Use Serena to search for:
1. Entry points (main.*, index.*, app.*)
2. Core business logic files
3. API/route definitions
4. Database models/schemas
5. Configuration loaders
```

**If Serena errors occur**: Retry with different Serena tools or fallback to direct file reading.

### 4.2 Architecture Pattern Recognition
Identify:
- Design patterns (MVC, MVVM, Clean Architecture, etc.)
- Dependency injection usage
- State management approaches
- API design patterns (REST, GraphQL, gRPC)
- Database access patterns (ORM, Query Builders, Raw SQL)

### 4.3 Code Quality Assessment
Analyze:
- Test coverage metrics (aim for >80%)
- Code organization and modularity
- Documentation completeness
- Error handling consistency
- Logging practices

---

## Phase 5: Project Tracking & Task Management

### 5.1 Review Current State
Check `/project_tracking` for:

**Active Work**:
- 🔴 Open tasks (immediate priority)
- 📋 Planning items (upcoming work)
- 🎯 Current sprint/milestone items

**Knowledge Base**:
- 📝 Notes and documentation
- ⚙️ Configurations and settings
- 📐 Design documents and specs
- 🏗️ Architecture diagrams

**Backlog**:
- 💡 Planned features
- 🐛 Known issues
- 🔧 Technical debt items
- ✅ Todos and reminders

**Project Structure**:
- 🔄 Development phases
- 📊 Status tracking
- 🎨 UI/UX specifications

---

## Phase 6: Analysis & Recommendations

### 6.1 Critical Issues Identification
Report on:
- **Security vulnerabilities** (HIGH PRIORITY)
- **Breaking changes** or deprecated code
- **Performance bottlenecks** (if detectable)
- **Missing error handling**
- **Inadequate test coverage** (<70%)

### 6.2 Documentation Gaps
Identify missing:
- API documentation
- Setup/installation guides
- Architecture decision records (ADRs)
- Deployment procedures
- Troubleshooting guides

### 6.3 Refactoring Opportunities
Suggest improvements for:
- Code duplication (DRY violations)
- Complex functions (high cyclomatic complexity)
- Long files (>500 lines)
- Inconsistent naming conventions
- Poorly structured modules

### 6.4 Enhancement Suggestions
Recommend:
- Modern best practices adoption
- Performance optimizations
- DevOps improvements (CI/CD, monitoring)
- Testing strategy enhancements
- Code organization improvements

---

## Phase 7: Comprehensive Summary Output

Provide a structured summary including:

### 📁 Project Structure
```
High-level organization overview
Key directories and their purposes
Module relationships and dependencies
```

### 🎯 Project Purpose & Goals
```
Primary business objectives
Target users/audience
Core functionality
Success metrics (if defined)
```

### 🔑 Key Files & Their Roles
```
Entry points and their purposes
Critical business logic locations
Configuration management
Infrastructure-as-code files
```

### 🧪 Test Coverage Analysis
```
Current coverage percentage
Well-tested areas
Under-tested areas
Missing test types (unit/integration/e2e)
```

### 📦 Dependencies Overview
```
Core runtime dependencies
Development dependencies
Potential security concerns
Update recommendations
```

### ⚠️ Critical Issues
```
Security vulnerabilities
Breaking changes needed
Technical debt
Missing documentation
Configuration issues
```

### 📝 Open Work Items
```
Tasks in progress
Blocked items
Backlog priorities
Estimated effort (if available)
```

### 🔧 Refactoring Opportunities
```
Code quality improvements
Performance optimizations
Architecture enhancements
Testing improvements
```

### 💡 Recommended Next Steps
```
Immediate actions (critical fixes)
Short-term improvements (1-2 weeks)
Long-term enhancements (1+ months)
Process improvements
```

### 📊 Project Health Score
```
Overall assessment (1-10)
Strengths
Weaknesses
Risk areas
Improvement trajectory
```

---

## Best Practices Reminders

### Context Management
- Use `/clear` between major tasks to reset context
- Use `/compact` to summarize when context is >70% full
- Monitor context usage with `/context` command
- Leverage subagents for isolated tasks

### Efficient Tool Usage
- Always use Serena first for codebase searches
- Batch related file reads to minimize tool calls
- Use MCP servers strategically based on task type
- Store important findings in project documentation

### Quality Standards
- Follow existing code style and conventions
- Maintain or improve test coverage with changes
- Document architectural decisions
- Keep CLAUDE.md updated with project changes

---

## Error Handling

If any errors occur during this process:
1. **Serena errors**: Retry with different Serena search methods
2. **File not found**: Verify file paths and retry
3. **Permission issues**: Request necessary access
4. **MCP server unavailable**: Document and proceed with alternatives
5. **Context limit approaching**: Use `/compact` before continuing

---

## Completion Checklist

Before concluding the primer, confirm:
- [ ] Project structure fully understood
- [ ] All critical files reviewed
- [ ] Dependencies mapped
- [ ] Test coverage assessed
- [ ] Issues identified and prioritized
- [ ] Recommendations documented
- [ ] Next steps clearly defined
- [ ] Project tracking updated
- [ ] Context usage optimized (<50%)

---

**Ready to begin priming? Respond with "Start primer" to proceed.**
