# ⚙️ Configuration Directory

> **🏠 [Home](../README.md)** | **📚 [Documentation](../docs/README.md)** | **📊 [Project Tracking](../project_tracking/README.md)**

---

## 📋 Overview

This directory contains all configuration files for the Cloud Scale Analytics (CSA) in-a-Box documentation project. Configuration is organized by purpose and environment to support development, staging, and production deployments.

## 🗂️ Directory Structure

```
config/
├── 📄 README.md                    # This file - Configuration hub
│
├── 📁 application/                 # Application-specific configurations
│   ├── 📄 README.md               # Application config documentation
│   ├── 📄 mcp_servers.json       # MCP server configurations
│   ├── 📄 logging.yaml            # Logging configuration
│   ├── 📄 rate_limits.json        # Rate limiting rules
│   ├── 📄 features.json           # Feature flags
│   └── 📄 security.yaml           # Security settings
│
├── 📁 environments/                # Environment-specific configurations
│   ├── 📄 README.md               # Environment config guide
│   ├── 📁 development/            # Development environment
│   │   ├── 📄 app.yaml
│   │   ├── 📄 database.yaml
│   │   └── 📄 services.yaml
│   ├── 📁 staging/                # Staging environment
│   │   ├── 📄 app.yaml
│   │   ├── 📄 database.yaml
│   │   └── 📄 services.yaml
│   └── 📁 production/             # Production environment
│       ├── 📄 app.yaml
│       ├── 📄 database.yaml
│       └── 📄 services.yaml
│
├── 📁 azure/                      # Azure-specific configurations
│   ├── 📄 README.md              # Azure config documentation
│   ├── 📄 resources.json         # Azure resource definitions
│   ├── 📄 credentials.json.template # Credential template
│   └── 📄 regions.yaml           # Regional configurations
│
└── 📁 templates/                  # Configuration templates
    ├── 📄 README.md              # Template guide
    ├── 📄 env.template           # Environment variable template
    ├── 📄 docker.template        # Docker config template
    └── 📄 k8s.template           # Kubernetes config template
```

## 🔧 Configuration Types

### Application Configuration (`/application/`)

Core application settings that control behavior across all environments.

| File | Purpose | Format |
|------|---------|--------|
| `mcp_servers.json` | MCP server endpoints and settings | JSON |
| `logging.yaml` | Logging levels and outputs | YAML |
| `rate_limits.json` | API rate limiting rules | JSON |
| `features.json` | Feature flags and toggles | JSON |
| `security.yaml` | Security policies and settings | YAML |

### Environment Configuration (`/environments/`)

Environment-specific settings for different deployment stages.

| Environment | Purpose | Usage |
|-------------|---------|-------|
| **Development** | Local development settings | `NODE_ENV=development` |
| **Staging** | Pre-production testing | `NODE_ENV=staging` |
| **Production** | Live production settings | `NODE_ENV=production` |

### Azure Configuration (`/azure/`)

Azure-specific settings and resource definitions.

| File | Purpose | Sensitivity |
|------|---------|-------------|
| `resources.json` | Azure resource definitions | Public |
| `credentials.json.template` | Template for Azure credentials | Template only |
| `regions.yaml` | Regional deployment configurations | Public |

### Configuration Templates (`/templates/`)

Reusable templates for creating new configurations.

| Template | Purpose | Usage |
|----------|---------|-------|
| `env.template` | Environment variables template | Copy to `.env` |
| `docker.template` | Docker configuration template | Customize for deployment |
| `k8s.template` | Kubernetes manifest template | Deploy to cluster |

## 📝 Configuration Standards

### File Formats

| Format | Extensions | Use Cases |
|--------|------------|-----------|
| **JSON** | `.json` | Structured data, API configs |
| **YAML** | `.yaml`, `.yml` | Complex configurations, readable |
| **ENV** | `.env`, `.template` | Environment variables |
| **INI** | `.ini` | Simple key-value pairs |

### Naming Conventions

- **Files**: Use `snake_case.ext` (e.g., `mcp_servers.json`)
- **Keys**: Use `camelCase` in JSON, `snake_case` in YAML
- **Environments**: Use lowercase (e.g., `development`, `production`)
- **Templates**: Include `.template` suffix

### Security Guidelines

#### Never Commit

- ❌ Actual credentials or secrets
- ❌ API keys or tokens
- ❌ Database passwords
- ❌ Private certificates
- ❌ `.env` files with real values

#### Always Use

- ✅ Template files for sensitive configs
- ✅ Environment variables for secrets
- ✅ Azure Key Vault for production secrets
- ✅ `.gitignore` for sensitive files
- ✅ Encryption for sensitive data at rest

## 🚀 Usage

### Loading Configuration

#### Python Example

```python
import json
import yaml
from pathlib import Path

# Load JSON configuration
def load_json_config(filename):
    config_path = Path(__file__).parent / 'config' / 'application' / filename
    with open(config_path, 'r') as f:
        return json.load(f)

# Load YAML configuration
def load_yaml_config(filename):
    config_path = Path(__file__).parent / 'config' / 'application' / filename
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# Load environment-specific config
def load_env_config(env='development'):
    config_path = Path(__file__).parent / 'config' / 'environments' / env / 'app.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
```

#### Environment Variables

```bash
# Copy template
cp config/templates/env.template .env

# Edit with your values
nano .env

# Load in application
source .env  # Linux/Mac
# or
set -a; source .env; set +a  # Export all vars
```

### Configuration Hierarchy

Configuration is loaded in this order (later overrides earlier):

1. **Default configuration** (built into application)
2. **Application configuration** (`/application/`)
3. **Environment configuration** (`/environments/{env}/`)
4. **Environment variables** (`.env` file or system)
5. **Command-line arguments** (if applicable)

## 📋 Configuration Examples

### MCP Server Configuration

```json
{
  "servers": {
    "primary": {
      "url": "http://localhost:8056",
      "timeout": 30,
      "retries": 3
    },
    "secondary": {
      "url": "http://localhost:8057",
      "timeout": 30,
      "retries": 3
    }
  },
  "loadBalancing": "round-robin",
  "healthCheck": {
    "interval": 60,
    "timeout": 5
  }
}
```

### Logging Configuration

```yaml
version: 1
disable_existing_loggers: false

formatters:
  default:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  json:
    class: pythonjsonlogger.jsonlogger.JsonFormatter

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: default
    stream: ext://sys.stdout
  
  file:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: json
    filename: logs/app.log
    maxBytes: 10485760  # 10MB
    backupCount: 5

root:
  level: INFO
  handlers: [console, file]
```

### Feature Flags

```json
{
  "features": {
    "newDashboard": {
      "enabled": true,
      "rolloutPercentage": 100,
      "allowedUsers": ["*"]
    },
    "advancedAnalytics": {
      "enabled": false,
      "rolloutPercentage": 0,
      "allowedUsers": ["beta-testers"]
    },
    "experimentalApi": {
      "enabled": true,
      "rolloutPercentage": 50,
      "allowedUsers": ["developers"]
    }
  }
}
```

## 🔄 Configuration Management

### Version Control

- **Track all** configuration files except secrets
- **Use tags** for configuration versions
- **Document changes** in commit messages
- **Review changes** before merging

### Deployment Process

1. **Development**: Direct file editing
2. **Staging**: Configuration through CI/CD
3. **Production**: Managed through Azure DevOps/GitHub Actions

### Configuration Validation

```bash
# Validate JSON files
python -m json.tool config/application/*.json

# Validate YAML files
python -c "import yaml; yaml.safe_load(open('config/application/logging.yaml'))"

# Check for secrets
grep -r "password\|secret\|key\|token" config/ --exclude="*.template"
```

## 🛡️ Security Best Practices

### Secrets Management

1. **Never hardcode** secrets in configuration files
2. **Use Azure Key Vault** for production secrets
3. **Rotate secrets** regularly
4. **Audit access** to configuration files
5. **Encrypt sensitive** configuration at rest

### Access Control

| Environment | Who Has Access | Approval Required |
|-------------|---------------|-------------------|
| Development | All developers | No |
| Staging | Senior developers | No |
| Production | DevOps team only | Yes |

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Configuration not loading | Check file path and format |
| Environment variable not set | Verify `.env` file loaded |
| Wrong environment config | Check `NODE_ENV` or `ENVIRONMENT` variable |
| JSON parse error | Validate JSON syntax |
| YAML indentation error | Check YAML formatting |

### Debug Configuration Loading

```python
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_config():
    logger.debug(f"Environment: {os.getenv('ENVIRONMENT', 'not set')}")
    logger.debug(f"Config path: {os.path.abspath('config/')}")
    logger.debug(f"Files found: {os.listdir('config/')}")
```

## 📚 Related Documentation

- [Development Guide](../docs/guides/DEVELOPMENT_GUIDE.md)
- [Deployment Documentation](../docs/deployment/README.md)
- [Security Best Practices](../docs/security/best-practices.md)
- [Azure Configuration Guide](../docs/architecture/README.md)

## 🤝 Contributing

When adding new configuration:

1. **Determine correct location** based on purpose
2. **Follow naming conventions**
3. **Add documentation** to relevant README
4. **Include template** if configuration contains secrets
5. **Update `.gitignore`** if needed
6. **Test in all environments**
7. **Document in PR** what the configuration does

## 📞 Support

For configuration-related issues:

- **Documentation**: Check this README and subdirectory READMEs
- **GitHub Issues**: [Create Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues)
- **Team Contact**: CSA Documentation Team

---

**Last Updated:** January 28, 2025  
**Version:** 1.0.0  
**Maintainer:** CSA Documentation Team