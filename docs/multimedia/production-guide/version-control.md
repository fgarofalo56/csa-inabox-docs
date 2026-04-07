# 🔄 Version Control Guide

> **🏠 [Home](../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **📎 [Production Guide](README.md)**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Version: 1.0](https://img.shields.io/badge/Version-1.0-blue)

## 📋 Overview

Version control strategies and best practices for managing multimedia assets throughout the
production lifecycle for CSA documentation.

## 📁 File Naming Convention

### Standard Format

```
[Project]_[Type]_v[Version]_[Date].[ext]

Examples:
AzureSynapse_Tutorial_v1.0_20250115.mp4
StreamAnalytics_Thumbnail_v2.1_20250116.png
```

### Version Numbering

- **Major (v1.0 → v2.0)**: Complete rebuild or new approach
- **Minor (v1.0 → v1.1)**: Significant changes or additions
- **Patch (v1.1 → v1.1.1)**: Small fixes and corrections

## 🎥 Video Asset Versioning

### Project Structure

```
project-folder/
├── 01-raw-footage/
├── 02-project-files/
├── 03-exports/
├── 04-graphics/
└── 05-documentation/
```

### Version Log

Maintain a changelog documenting all versions, changes, and approvals.

## 💻 Code Versioning

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-demo

# Commit with semantic message
git commit -m "feat: add cost calculator demo"

# Tag releases
git tag v1.0.0
git push --tags
```

### Commit Message Format

```
type(scope): subject

Types: feat, fix, docs, style, refactor, test, chore
```

## 🗂️ Archive Strategy

### Lifecycle

- **Active**: During production + 30 days (hot tier)
- **Recent**: 30-180 days after publish (cool tier)
- **Archive**: 180+ days (archive tier)
- **Permanent**: Final published versions (CDN)

## 📊 Version Tracking

Track which versions are in production, review, and archive stages using asset management
systems and metadata.

## 🔐 Access Control

- Drafts: Creator and editors only
- Review: Team and stakeholders
- Final: Team read, admin write
- Published: Public read, admin write

## 📚 Additional Resources

- [Asset Management](./asset-management.md)
- [Publishing Workflow](./publishing-workflow.md)
- [Quality Assurance](./quality-assurance.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
