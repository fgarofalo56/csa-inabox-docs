# Quick Start Guide: CSA Documentation Versioning

This guide helps you get started with the comprehensive versioning workflow for Cloud Scale Analytics documentation.

## Overview

The CSA documentation now supports:
- **Semantic versioning** with automated releases
- **Multi-version navigation** for users
- **Quality gates** ensuring release quality
- **Migration tools** for smooth upgrades
- **Automated deployment** via GitHub Actions

## Prerequisites

- Python 3.9+ installed
- Git repository access
- GitHub repository with Pages enabled
- Basic understanding of MkDocs and Mike

## Quick Setup

### 1. Install Dependencies

```bash
# Install the documentation tools
pip install -e .

# Or install specific requirements
pip install mkdocs mkdocs-material mike
```

### 2. Initialize Versioning

```bash
# Create initial version configuration
python -c "
from src.csa_docs_tools.version_manager import SemanticVersionManager, VersionInfo, VersionType
manager = SemanticVersionManager()
version_info = VersionInfo(
    version='1.0.0',
    version_type=VersionType.STABLE,
    title='CSA Documentation v1.0.0',
    aliases=['latest'],
    is_default=True
)
manager.add_version(version_info)
print('Initial version configuration created')
"
```

### 3. Deploy First Version

```bash
# Build and deploy version 1.0.0
mkdocs build
mike deploy 1.0.0 latest --update-aliases
mike set-default 1.0.0
```

## Creating a New Release

### Option 1: Automated Release (Recommended)

1. **Create and push a version tag**:
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```

2. **Monitor the GitHub Actions workflow**:
   - Go to your repository's Actions tab
   - Watch the "Versioned Documentation Release" workflow
   - The workflow will automatically:
     - Validate the release
     - Run quality gates
     - Build documentation
     - Deploy the new version
     - Create GitHub release with assets

### Option 2: Manual Release

1. **Validate release readiness**:
   ```bash
   python -c "
   from src.csa_docs_tools.release_manager import ReleaseManager
   from pathlib import Path
   
   manager = ReleaseManager(repo_path=Path('.'))
   is_ready, issues = manager.validate_release_readiness('1.1.0')
   
   if is_ready:
       print('✓ Release validation passed')
   else:
       print('✗ Release validation failed:')
       for issue in issues:
           print(f'  - {issue}')
   "
   ```

2. **Generate changelog**:
   ```bash
   python -c "
   from src.csa_docs_tools.release_manager import ReleaseManager
   from pathlib import Path
   
   manager = ReleaseManager(repo_path=Path('.'))
   changelog = manager.generate_changelog('v1.0.0', 'v1.1.0')
   print(changelog)
   "
   ```

3. **Deploy the version**:
   ```bash
   mkdocs build
   mike deploy 1.1.0 "CSA Documentation v1.1.0" --update-aliases
   ```

## Version Management Commands

### List All Versions
```bash
# Using Mike
mike list

# Using our tools for detailed info
python -c "
from src.csa_docs_tools.mike_manager import MikeVersionManager
from pathlib import Path

manager = MikeVersionManager(Path('.'))
versions = manager.list_versions()
for v in versions:
    print(f'{v.version} - {v.title} (Default: {v.is_default})')
"
```

### Set Default Version
```bash
mike set-default 1.1.0
```

### Delete Old Version
```bash
mike delete 0.9.0
```

### Generate Migration Guide
```bash
python -c "
from src.csa_docs_tools.migration_manager import MigrationManager
from pathlib import Path

manager = MigrationManager(Path('.'))
guide = manager.create_migration_guide('1.0.0', '1.1.0')
print(f'Migration guide: {guide.title}')
print(f'Effort level: {guide.estimated_effort}')
for step in guide.migration_steps:
    print(f'- {step}')
"
```

## Quality Gates

Run quality validation before releases:

```bash
python -c "
import asyncio
from src.csa_docs_tools.version_validator import VersionValidator
from pathlib import Path

async def validate():
    validator = VersionValidator(Path('.'))
    all_passed, results = await validator.validate_version('1.1.0')
    
    print(f'Overall result: {"PASSED" if all_passed else "FAILED"}')
    for result in results:
        status = "✓" if result.passed else "✗"
        print(f'{status} {result.gate_name}: {result.message}')

asyncio.run(validate())
"
```

## Working with Branches

### Release Branch Workflow

1. **Create release branch**:
   ```bash
   python -c "
   from src.csa_docs_tools.release_manager import ReleaseManager
   from pathlib import Path
   
   manager = ReleaseManager(repo_path=Path('.'))
   branch = manager.create_release_branch('1.1.0')
   print(f'Created release branch: {branch}')
   "
   ```

2. **Make changes and finalize**:
   ```bash
   # Make your documentation changes
   # ...
   
   # Finalize the release
   python -c "
   from src.csa_docs_tools.release_manager import ReleaseManager
   from pathlib import Path
   
   manager = ReleaseManager(repo_path=Path('.'))
   result = manager.finalize_release('1.1.0')
   print(f'Release {result["version"]} finalized')
   print(f'Tag: {result["tag"]}')
   print(f'Commit: {result["commit"]}')
   "
   ```

### Hotfix Workflow

1. **Create hotfix branch from tag**:
   ```bash
   python -c "
   from src.csa_docs_tools.release_manager import ReleaseManager
   from pathlib import Path
   
   manager = ReleaseManager(repo_path=Path('.'))
   branch = manager.create_hotfix_branch('1.0.1', 'v1.0.0')
   print(f'Created hotfix branch: {branch}')
   "
   ```

2. **Fix issues and release**:
   ```bash
   # Make your fixes
   # ...
   
   # Deploy hotfix
   mkdocs build
   mike deploy 1.0.1 "CSA Documentation v1.0.1 (Hotfix)"
   ```

## Configuration

### Custom Quality Gates

Create custom validation rules:

```python
# custom_validation.py
from src.csa_docs_tools.version_validator import QualityGate, VersionValidator
from pathlib import Path

custom_gates = [
    QualityGate(
        name="custom_content_check",
        description="Check for required content sections",
        validator_class="ContentValidator",
        required=True,
        failure_threshold=0.1
    )
]

validator = VersionValidator(Path('.'), quality_gates=custom_gates)
```

### Migration Rules

Define content migration rules:

```python
# migration_rules.py
from src.csa_docs_tools.migration_manager import MigrationRule, MigrationManager

rule = MigrationRule(
    rule_id="move_legacy_content",
    name="Move legacy content to archive",
    description="Move deprecated content to legacy section",
    from_version="1.0.0",
    to_version="2.0.0",
    rule_type="content",
    action="move",
    source_path="docs/old-section/",
    target_path="docs/legacy/old-section/"
)

manager = MigrationManager()
manager.add_migration_rule(rule)
```

## Troubleshooting

### Common Issues

1. **Build failures**:
   ```bash
   # Check build logs
   mkdocs build --verbose
   
   # Validate navigation
   python -c "
   from src.csa_docs_tools.navigation_validator import NavigationValidator
   from pathlib import Path
   
   validator = NavigationValidator(Path('.'))
   is_valid, issues = validator.validate_structure()
   if not is_valid:
       for issue in issues:
           print(f'- {issue}')
   "
   ```

2. **Version conflicts**:
   ```bash
   # Check existing versions
   mike list
   
   # Remove conflicting version
   mike delete problematic-version
   ```

3. **Permission errors**:
   - Ensure GitHub token has required permissions
   - Check repository settings for Pages deployment
   - Verify workflow permissions in `.github/workflows/`

### Getting Help

1. **Check workflow logs** in GitHub Actions tab
2. **Review validation reports** in `validation_reports/`
3. **Consult integration test results** in `docs/versioning/INTEGRATION_TEST_RESULTS.md`

## Best Practices

### Version Numbering
- Use semantic versioning: `MAJOR.MINOR.PATCH`
- Major: Breaking changes to documentation structure
- Minor: New sections or significant content additions
- Patch: Bug fixes, typos, minor updates

### Release Planning
- Plan major releases with migration guides
- Use prerelease versions for testing: `2.0.0-beta.1`
- Keep stable versions for at least 6 months
- Archive prerelease versions regularly

### Quality Assurance
- Always run quality gates before releases
- Test navigation changes thoroughly
- Validate all links, especially external ones
- Review performance impact of large changes

### User Communication
- Include clear release notes
- Provide migration guides for breaking changes
- Use deprecation notices for content removal
- Maintain compatibility matrices

---

**Next Steps**: Once comfortable with basics, explore advanced features like custom quality gates, migration rules, and performance optimization.
