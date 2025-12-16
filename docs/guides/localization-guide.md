# Localization Guide

[Home](../../README.md) > [Guides](README.md) > Localization Guide

> Comprehensive guide for translating and localizing the CSA-in-a-Box documentation for international audiences. This guide covers translation workflows, terminology management, and contribution procedures.

---

## Table of Contents

- [Overview](#overview)
- [Translation Workflow](#translation-workflow)
- [Terminology Consistency](#terminology-consistency)
- [Translation Guidelines](#translation-guidelines)
- [File Organization](#file-organization)
- [Contributing Translations](#contributing-translations)
- [Quality Assurance](#quality-assurance)
- [Tools and Resources](#tools-and-resources)

---

## Overview

### Localization Strategy

The CSA-in-a-Box documentation follows a structured approach to localization:

- __Primary Language__: English (en-US)
- __Translation Approach__: Community-driven with professional review
- __Supported Languages__: Determined by community interest and Azure market presence
- __Update Cadence__: Translations updated quarterly or after major releases

### Target Languages

Priority languages based on Azure Synapse Analytics usage:

| Language | Code | Priority | Status | Maintainer |
|----------|------|----------|--------|------------|
| English (US) | en-US | Primary | Complete | Core team |
| French | fr-FR | High | Planned | Community |
| German | de-DE | High | Planned | Community |
| Spanish | es-ES | High | Planned | Community |
| Portuguese (Brazil) | pt-BR | High | Planned | Community |
| Japanese | ja-JP | High | Planned | Community |
| Chinese (Simplified) | zh-CN | High | Planned | Community |
| Korean | ko-KR | Medium | Planned | Community |
| Italian | it-IT | Medium | Planned | Community |
| Dutch | nl-NL | Medium | Planned | Community |

---

## Translation Workflow

### Workflow Overview

```text
┌──────────────────────┐
│ 1. Source Updated    │
│    (English)         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ 2. Mark for          │
│    Translation       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ 3. Community         │
│    Translation       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ 4. Peer Review       │
│    (Native Speakers) │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ 5. Technical Review  │
│    (Subject Matter   │
│     Experts)         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ 6. Final Approval &  │
│    Publication       │
└──────────────────────┘
```

### Step-by-Step Process

#### 1. Identify Content for Translation

- [ ] New documentation added
- [ ] Existing documentation updated
- [ ] Priority content for target language
- [ ] Community request for translation

#### 2. Prepare Source Content

```bash
# Create translation tracking issue
gh issue create \
  --title "Translation Request: [Document Name] to [Language]" \
  --body "Document: docs/path/to/document.md
Target Language: fr-FR
Priority: High
Estimated Words: 2500" \
  --label "translation,help-wanted"
```

#### 3. Assign to Translator

- Community volunteer or professional translator
- Native speaker preferred
- Technical background in cloud/analytics helpful
- Familiar with Azure terminology

#### 4. Translation Execution

```bash
# Translator forks repository
git clone https://github.com/YOUR-USERNAME/csa-inabox-docs.git
cd csa-inabox-docs

# Create translation branch
git checkout -b translate-fr-architecture-overview

# Create language directory structure
mkdir -p docs/i18n/fr-FR/architecture

# Translate file
# docs/architecture/README.md -> docs/i18n/fr-FR/architecture/README.md
```

#### 5. Submit for Review

```bash
# Commit translation
git add docs/i18n/fr-FR/architecture/README.md
git commit -m "docs(i18n): add French translation for architecture overview"

# Push to fork
git push origin translate-fr-architecture-overview

# Create pull request
gh pr create \
  --title "French translation: Architecture Overview" \
  --body "Closes #123

## Translation Details
- **Language**: French (fr-FR)
- **Source**: docs/architecture/README.md
- **Word Count**: 2500
- **Translator**: @username

## Checklist
- [x] Technical terms verified against glossary
- [x] Code examples preserved unchanged
- [x] Links updated for localized content
- [x] Formatting maintained
- [x] Proofread by native speaker"
```

---

## Terminology Consistency

### Terminology Management

Maintaining consistent terminology across all translations is critical for quality.

### Translation Glossary

Create and maintain a translation glossary for each language:

#### Core Technical Terms (Do NOT Translate)

| English Term | Rationale |
|-------------|-----------|
| Azure Synapse Analytics | Product name |
| Spark Pool | Feature name |
| SQL Pool | Feature name |
| ADLS Gen2 | Product acronym |
| Delta Lake | Technology name |
| Apache Spark | Technology name |
| Parquet | File format name |
| JSON | File format name |

#### Translatable Terms

| English | French | German | Spanish | Japanese | Chinese |
|---------|--------|--------|---------|----------|---------|
| Workspace | Espace de travail | Arbeitsbereich | Espacio de trabajo | ワークスペース | 工作区 |
| Pipeline | Pipeline | Pipeline | Canalización | パイプライン | 管道 |
| Dataset | Jeu de données | Datensatz | Conjunto de datos | データセット | 数据集 |
| Query | Requête | Abfrage | Consulta | クエリ | 查询 |
| Performance | Performance | Leistung | Rendimiento | パフォーマンス | 性能 |
| Security | Sécurité | Sicherheit | Seguridad | セキュリティ | 安全 |
| Authentication | Authentification | Authentifizierung | Autenticación | 認証 | 身份验证 |
| Monitoring | Surveillance | Überwachung | Monitorización | 監視 | 监控 |

### Creating a Language-Specific Glossary

```markdown
<!-- docs/i18n/fr-FR/GLOSSARY.md -->
# Glossaire Technique - Azure Synapse Analytics

## Termes Préservés (Non Traduits)

- **Azure Synapse Analytics** : Nom du produit Microsoft
- **Spark Pool** : Nom de fonctionnalité
- **Delta Lake** : Nom de technologie

## Termes Traduits

### A
- **Authentication** : Authentification
- **Authorization** : Autorisation
- **Availability** : Disponibilité

### D
- **Dataset** : Jeu de données
- **Deployment** : Déploiement

### P
- **Performance** : Performance
- **Pipeline** : Pipeline (terme conservé en anglais)

### W
- **Workspace** : Espace de travail
- **Workload** : Charge de travail
```

### Azure-Specific Terminology

Always check the official Azure terminology for your target language:

- [Azure Terminology (English)](https://docs.microsoft.com/en-us/azure/azure-glossary)
- [Microsoft Language Portal](https://www.microsoft.com/en-us/language)
- [Azure Documentation (Localized)](https://docs.microsoft.com/)

---

## Translation Guidelines

### General Principles

1. __Preserve Technical Accuracy__
   - Maintain exact meaning
   - Don't simplify technical concepts
   - Verify with subject matter experts

2. __Maintain Natural Language Flow__
   - Write naturally in target language
   - Don't translate word-for-word
   - Adapt idioms and expressions

3. __Keep User Focus__
   - Address reader directly
   - Maintain instructional tone
   - Preserve call-to-action clarity

### Content-Specific Guidelines

#### Code Examples

__DO NOT TRANSLATE:__

- Variable names
- Function names
- Code comments (unless specifically noted)
- Console output
- API endpoints
- File paths

```python
# CORRECT - Code preserved, comments optionally translated
# French translation
def creer_espace_de_travail(nom: str, region: str):
    """
    Crée un nouvel espace de travail Azure Synapse.

    Args:
        nom: Nom de l'espace de travail
        region: Région Azure
    """
    return create_workspace(name=nom, region=region)

# INCORRECT - Do not translate code elements
def creerEspaceDeTravail(nom: str, région: str):
    retourner créer_espace_de_travail(nom=nom, région=région)
```

#### Command-Line Instructions

Preserve commands; translate descriptions:

```markdown
<!-- CORRECT -->
## Installation d'Azure CLI

Exécutez la commande suivante pour installer Azure CLI :

```bash
az --version
```

<!-- INCORRECT - Don't translate commands -->
## Installation d'Azure CLI

Exécutez la commande suivante :

```bash
az --version  # version en français
```

```text
```

### Links and References

- Update links to localized versions when available
- Keep English links if no translation exists
- Note language differences

```text
<!-- CORRECT -->
Pour plus d'informations, consultez la [documentation Azure](https://docs.microsoft.com/fr-fr/azure/).

Si la documentation n'est pas disponible en français, référez-vous à la [version anglaise](https://docs.microsoft.com/en-us/azure/).

<!-- Maintain internal links with language path -->
Voir le [guide d'architecture](../architecture/README.md) pour plus de détails.
```

### UI Elements and Menu Paths

Translate UI elements consistently with Azure Portal localization:

```markdown
<!-- English -->
Navigate to **Resource groups** > **Create** > **Synapse workspace**

<!-- French -->
Accédez à **Groupes de ressources** > **Créer** > **Espace de travail Synapse**

<!-- German -->
Navigieren Sie zu **Ressourcengruppen** > **Erstellen** > **Synapse-Arbeitsbereich**
```

#### Numbers and Units

Follow local conventions:

```markdown
<!-- English (US) -->
- Storage: 1,000 GB
- Cost: $1,234.56
- Date: 12/31/2025

<!-- French (FR) -->
- Stockage : 1 000 Go
- Coût : 1 234,56 $
- Date : 31/12/2025

<!-- German (DE) -->
- Speicher: 1.000 GB
- Kosten: 1.234,56 $
- Datum: 31.12.2025
```

### Style and Tone

#### Formal vs. Informal Address

Different languages have different conventions:

| Language | Address Style | Example |
|----------|--------------|---------|
| English | Informal (you) | "You can configure..." |
| French | Formal (vous) | "Vous pouvez configurer..." |
| German | Formal (Sie) | "Sie können konfigurieren..." |
| Spanish | Formal (usted) | "Puede configurar..." |
| Japanese | Polite (です/ます) | "設定できます" |

#### Active vs. Passive Voice

Maintain active voice where possible:

```markdown
<!-- GOOD -->
# English
Create a new workspace by clicking the Create button.

# French
Créez un nouvel espace de travail en cliquant sur le bouton Créer.

<!-- AVOID -->
# English
A new workspace can be created by clicking the Create button.

# French
Un nouvel espace de travail peut être créé en cliquant sur le bouton Créer.
```

---

## File Organization

### Directory Structure

```text
docs/
├── i18n/                           # All translations
│   ├── fr-FR/                      # French translations
│   │   ├── GLOSSARY.md             # French glossary
│   │   ├── architecture/
│   │   │   ├── README.md
│   │   │   └── delta-lakehouse/
│   │   ├── best-practices/
│   │   ├── tutorials/
│   │   └── reference/
│   ├── de-DE/                      # German translations
│   │   ├── GLOSSARY.md
│   │   └── ...
│   ├── ja-JP/                      # Japanese translations
│   │   ├── GLOSSARY.md
│   │   └── ...
│   └── TRANSLATION_STATUS.md       # Overall translation status
├── architecture/                   # English (source)
├── best-practices/
└── ...
```

### File Naming

- Maintain same file names as English version
- Use same directory structure
- Preserve README.md convention

```bash
# English source
docs/architecture/delta-lakehouse/README.md

# French translation
docs/i18n/fr-FR/architecture/delta-lakehouse/README.md

# German translation
docs/i18n/de-DE/architecture/delta-lakehouse/README.md
```

### Translation Metadata

Add metadata header to translated files:

```markdown
---
translation:
  language: fr-FR
  source: docs/architecture/README.md
  translated_by: "@username"
  reviewed_by: "@reviewer"
  translation_date: 2025-01-15
  source_version: abc123def
---

# Architecture Vue d'ensemble

[Translation content follows...]
```

---

## Contributing Translations

### Prerequisites

- Native or fluent speaker of target language
- Familiarity with Azure Synapse Analytics (preferred)
- GitHub account
- Basic Git knowledge

### Contribution Steps

#### 1. Check for Existing Work

```bash
# Search for existing translation issues
gh issue list --label "translation" --label "fr-FR"

# Check translation status
cat docs/i18n/TRANSLATION_STATUS.md
```

#### 2. Claim a Document

```bash
# Comment on existing issue or create new one
gh issue comment 123 --body "I'd like to work on this translation"
```

#### 3. Set Up Development Environment

```bash
# Fork and clone repository
gh repo fork fgarofalo56/csa-inabox-docs --clone

# Create translation branch
git checkout -b translate/fr-FR/architecture-overview

# Set up translation directory
mkdir -p docs/i18n/fr-FR/architecture
```

#### 4. Translate Content

- Use glossary for terminology
- Preserve formatting and structure
- Keep code examples unchanged
- Update links appropriately

#### 5. Self-Review Checklist

Before submitting:

- [ ] All technical terms verified against glossary
- [ ] Code examples preserved exactly
- [ ] Links updated for localized content where available
- [ ] Formatting matches source (headings, lists, tables)
- [ ] Metadata header added
- [ ] Proofread for grammar and spelling
- [ ] Natural language flow (not word-for-word)
- [ ] Consistent tone and style

#### 6. Submit Pull Request

```bash
# Commit translation
git add docs/i18n/fr-FR/architecture/README.md
git commit -m "docs(i18n): add French translation for architecture overview"

# Push to fork
git push origin translate/fr-FR/architecture-overview

# Create pull request with template
gh pr create --template translation.md
```

### Pull Request Template

```markdown
## Translation Submission

### Translation Details
- **Language**: French (fr-FR)
- **Source Document**: docs/architecture/README.md
- **Source Version**: abc123def
- **Word Count**: ~2,500 words
- **Translator**: @username

### Verification Checklist
- [ ] Native speaker review completed
- [ ] Technical terms verified against glossary
- [ ] Code examples preserved unchanged
- [ ] Links updated appropriately
- [ ] Formatting maintained
- [ ] Metadata header added
- [ ] No machine translation used without review

### Glossary Updates
- [ ] No new terms
- [ ] New terms added to glossary (list below)

### Additional Notes
[Any context or questions for reviewers]
```

---

## Quality Assurance

### Review Process

#### Peer Review (Native Speakers)

Focus on:

- Natural language flow
- Grammar and spelling
- Cultural appropriateness
- Consistency with existing translations

#### Technical Review (Subject Matter Experts)

Focus on:

- Technical accuracy
- Terminology consistency
- Code preservation
- Completeness

### Translation Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Technical Accuracy | 100% | Expert review |
| Terminology Consistency | 95%+ | Glossary compliance |
| Completeness | 100% | All sections translated |
| Natural Flow | Good-Excellent | Peer review rating |
| Update Lag | <30 days | Time from source update |

### Common Translation Issues

#### Issue 1: Over-Literal Translation

__Problem__: Word-for-word translation sounds unnatural

__Solution__: Translate meaning, not words

```markdown
<!-- English -->
Let's dive deep into the architecture.

<!-- AVOID - Too literal French -->
Plongeons profondément dans l'architecture.

<!-- BETTER - Natural French -->
Examinons en détail l'architecture.
```

#### Issue 2: Inconsistent Terminology

__Problem__: Same term translated differently

__Solution__: Use glossary consistently

```markdown
<!-- INCONSISTENT -->
Page 1: "Espace de travail"
Page 2: "Zone de travail"
Page 3: "Workspace"

<!-- CONSISTENT -->
All pages: "Espace de travail" (per glossary)
```

#### Issue 3: Broken Internal Links

__Problem__: Links point to English version

__Solution__: Update to localized paths

```markdown
<!-- INCORRECT -->
[Architecture Guide](../../architecture/README.md)

<!-- CORRECT -->
[Guide d'Architecture](../../architecture/README.md)
<!-- Or if translated: -->
[Guide d'Architecture](../architecture/README.md)
```

---

## Tools and Resources

### Recommended Translation Tools

#### Computer-Assisted Translation (CAT) Tools

- __OmegaT__ (Free, Open Source)
  - Translation memory
  - Glossary management
  - Markdown support

- __Weblate__ (Hosted solution)
  - Web-based translation
  - Collaboration features
  - Git integration

#### Quality Assurance Tools

- __LanguageTool__ - Grammar and spelling check
- __Vale__ - Style linter for documentation
- __markdownlint__ - Markdown formatting validation

### Glossary Resources

- [Microsoft Language Portal](https://www.microsoft.com/en-us/language)
- [Azure Terminology](https://docs.microsoft.com/en-us/azure/azure-glossary)
- [Azure Product Names](https://docs.microsoft.com/en-us/azure/azure-glossary-cloud-terminology)

### Validation Scripts

```bash
# validate_translation.sh
#!/bin/bash

LANG_CODE=$1
SOURCE_FILE=$2
TRANS_FILE=$3

echo "Validating translation: $TRANS_FILE"

# Check metadata exists
if ! grep -q "^---$" "$TRANS_FILE"; then
    echo "ERROR: Missing metadata header"
    exit 1
fi

# Check code blocks match
SOURCE_CODE_BLOCKS=$(grep -c '```' "$SOURCE_FILE")
TRANS_CODE_BLOCKS=$(grep -c '```' "$TRANS_FILE")

if [ "$SOURCE_CODE_BLOCKS" != "$TRANS_CODE_BLOCKS" ]; then
    echo "WARNING: Code block count mismatch"
    echo "Source: $SOURCE_CODE_BLOCKS, Translation: $TRANS_CODE_BLOCKS"
fi

# Run markdownlint
markdownlint "$TRANS_FILE"

echo "Validation complete"
```

### Translation Memory

Maintain translation memory to ensure consistency:

```json
// translation-memory.json
{
  "source_lang": "en-US",
  "target_lang": "fr-FR",
  "segments": [
    {
      "source": "Create a new workspace",
      "target": "Créer un nouvel espace de travail",
      "context": "button_label"
    },
    {
      "source": "Azure Synapse Analytics provides...",
      "target": "Azure Synapse Analytics fournit...",
      "context": "introduction"
    }
  ]
}
```

---

## Communication Channels

### Translation Coordination

- __GitHub Issues__: Track translation requests and progress
- __GitHub Discussions__: Terminology discussions and questions
- __Pull Requests__: Submit and review translations

### Language-Specific Channels

Create dedicated discussion threads for each language:

```markdown
# GitHub Discussion: French (fr-FR) Translation

## Purpose
Coordinate French translation efforts, discuss terminology, and share resources.

## Current Translators
- @translator1
- @translator2

## Terminology Questions
[Discussion threads...]

## Resources
- [French Glossary](docs/i18n/fr-FR/GLOSSARY.md)
- [Azure French Documentation](https://docs.microsoft.com/fr-fr/azure/)
```

---

## Translation Status Tracking

### Status Document

```markdown
<!-- docs/i18n/TRANSLATION_STATUS.md -->
# Translation Status

Last Updated: 2025-01-15

## Overview

| Language | Progress | Pages Translated | Maintainer |
|----------|----------|-----------------|------------|
| fr-FR | 15% | 12/80 | @translator |
| de-DE | 5% | 4/80 | @translator2 |
| ja-JP | 0% | 0/80 | Needed |

## French (fr-FR) - 15% Complete

| Section | Status | Translator | Reviewer | Last Updated |
|---------|--------|-----------|----------|--------------|
| Architecture | ✅ Complete | @user1 | @user2 | 2025-01-10 |
| Best Practices | 🔄 In Progress | @user3 | - | 2025-01-12 |
| Tutorials | ⏳ Pending | - | - | - |
| Reference | ⏳ Pending | - | - | - |

## German (de-DE) - 5% Complete

[Similar breakdown...]
```

---

## Recognition

### Contributor Recognition

Translators will be recognized:

1. __In Translation File__ - Metadata header
2. __In Contributors File__ - docs/CONTRIBUTORS.md
3. __In Release Notes__ - Mentioned in changelog
4. __GitHub Profile__ - Contribution graph

### Translation Credits

```markdown
<!-- docs/i18n/fr-FR/CONTRIBUTORS.md -->
# Contributeurs Français

Merci à tous ceux qui ont contribué aux traductions françaises !

## Traducteurs Principaux

- **@translator1** - Architecture, Best Practices
- **@translator2** - Tutorials, Reference

## Réviseurs

- **@reviewer1** - Technical review
- **@reviewer2** - Language review
```

---

## Best Practices Summary

### Do's

✅ Use official Azure terminology
✅ Maintain consistent glossary usage
✅ Preserve code examples exactly
✅ Write naturally in target language
✅ Update links to localized content
✅ Add translation metadata
✅ Request peer review
✅ Keep translations synchronized with source

### Don'ts

❌ Don't rely solely on machine translation
❌ Don't translate product names
❌ Don't modify code examples
❌ Don't skip technical review
❌ Don't break internal links
❌ Don't ignore style guidelines
❌ Don't forget metadata headers

---

## Related Resources

- [Contributing Guide](CONTRIBUTING_GUIDE.md)
- [Markdown Style Guide](MARKDOWN_STYLE_GUIDE.md)
- [Regional Compliance](../reference/regional-compliance.md)
- [Azure Regions Reference](../reference/azure-regions.md)
- [Microsoft Language Portal](https://www.microsoft.com/en-us/language)
- [Azure Documentation Localization](https://docs.microsoft.com/en-us/contribute/localization)

---

> __Get Started__: Ready to contribute a translation? Check the [translation status](../i18n/TRANSLATION_STATUS.md) and claim a document in our [GitHub Issues](https://github.com/fgarofalo56/csa-inabox-docs/issues?q=is%3Aissue+is%3Aopen+label%3Atranslation).
