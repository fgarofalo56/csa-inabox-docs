# Asset Management Guide

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **📎 [Production Guide](README.md)** | **📦 Asset Management**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)

## Overview

Digital asset management (DAM) guidelines for organizing, storing, and managing multimedia production assets efficiently and securely.

## File Organization

### Directory Structure

```
assets/
├── video/
│   ├── source/          # Raw footage, project files
│   ├── edited/          # Final edited videos
│   ├── exports/         # Multiple format exports
│   └── archive/         # Completed projects
├── audio/
│   ├── voiceover/       # Narration recordings
│   ├── music/           # Background music
│   ├── sfx/             # Sound effects
│   └── stems/           # Individual audio tracks
├── graphics/
│   ├── source/          # AI, PSD, FIG files
│   ├── exports/         # PNG, SVG, JPEG
│   ├── templates/       # Reusable templates
│   └── brand/           # Logos, brand assets
├── stock/
│   ├── video/           # Stock video clips
│   ├── photos/          # Stock photos
│   ├── music/           # Licensed music
│   └── icons/           # Icon libraries
└── projects/
    └── [project-name]/
        ├── planning/    # Scripts, storyboards
        ├── production/  # Raw assets
        └── delivery/    # Final deliverables
```

### Naming Conventions

```yaml
file_naming:
  format: "[project]-[type]-[version]-[language].[ext]"

  examples:
    video: "azure-synapse-tutorial-final-v2-en.mp4"
    audio: "corporate-intro-music-final.mp3"
    graphic: "architecture-diagram-v3.svg"
    project: "azure-tutorial-2025-01-aep.zip"

  version_control:
    draft: "v0.1, v0.2, v0.3"
    review: "v1.0, v1.1, v1.2"
    final: "final, final-v2 (if revisions needed)"

  language_codes:
    format: "ISO 639-1 + ISO 3166-1"
    examples: "en-US, es-ES, fr-FR, ja-JP"
```

## Storage Solutions

### Azure Blob Storage Structure

```yaml
storage_account: "csaassets"

containers:
  production:
    name: "production-assets"
    access: "Private"
    lifecycle: "Hot tier, no auto-deletion"
    backup: "Geo-redundant (GRS)"

  published:
    name: "published-content"
    access: "Public (CDN)"
    lifecycle: "Cool tier after 90 days"
    cdn: "Enabled"

  archive:
    name: "archived-projects"
    access: "Private"
    lifecycle: "Archive tier after 1 year"
    backup: "Geo-redundant (GRS)"

  temp:
    name: "temporary-files"
    access: "Private"
    lifecycle: "Auto-delete after 30 days"
```

### Local Storage

```markdown
## Local Working Storage

### Production Workstation
- **Location:** `D:\Production\Active\`
- **Capacity:** 2TB NVMe SSD minimum
- **Backup:** Daily incremental to NAS
- **Retention:** Keep until project published + 30 days

### Network Attached Storage (NAS)
- **Location:** `\nas\multimedia\`
- **Capacity:** 20TB+ RAID 6
- **Backup:** Weekly to cloud (Azure Blob Archive)
- **Retention:** 2 years for source files, permanent for masters

### Backup Strategy
1. **3-2-1 Rule:** 3 copies, 2 different media, 1 offsite
2. **Working files:** Local SSD + NAS (daily)
3. **Project archives:** NAS + Azure Blob (weekly)
4. **Masters:** NAS + Azure Blob Archive (permanent)
```

## Asset Metadata

### Metadata Standards

```json
{
  "asset_id": "az-syn-001",
  "title": "Azure Synapse Analytics Tutorial",
  "type": "video",
  "format": "mp4",
  "resolution": "1920x1080",
  "duration": "15:30",
  "file_size": "450MB",
  "created_date": "2025-01-15",
  "creator": "Sarah Johnson",
  "project": "Azure Tutorials 2025",
  "status": "published",
  "tags": ["azure", "synapse", "analytics", "tutorial"],
  "keywords": "Azure, Data Warehouse, Big Data",
  "language": "en-US",
  "license": "CC BY-NC 4.0",
  "accessibility": {
    "captions": true,
    "transcript": true,
    "audio_description": false
  },
  "versions": {
    "master": "az-syn-001-master.mov",
    "web": "az-syn-001-web.mp4",
    "mobile": "az-syn-001-mobile.mp4"
  },
  "related_assets": [
    "az-syn-001-captions-en.vtt",
    "az-syn-001-transcript.pdf",
    "az-syn-001-thumbnail.jpg"
  ]
}
```

## Version Control

### Git LFS for Large Files

```bash
# Initialize Git LFS
git lfs install

# Track large file types
git lfs track "*.psd"
git lfs track "*.ai"
git lfs track "*.aep"
git lfs track "*.prproj"
git lfs track "*.mp4"
git lfs track "*.mov"

# Commit .gitattributes
git add .gitattributes
git commit -m "Configure Git LFS for media files"

# Add and commit large files
git add assets/graphics/hero-image.psd
git commit -m "Add hero image source file"
git push
```

### Project Archival

```markdown
## Archive Procedure

### Before Archiving
- [ ] Collect all project files
- [ ] Organize into standard structure
- [ ] Remove temporary/cache files
- [ ] Generate project documentation
- [ ] Export final deliverables

### Archive Package Contents
```
project-archive/
├── README.md              # Project overview
├── metadata.json          # Asset metadata
├── source/                # Original project files
├── assets/                # Media assets
├── deliverables/          # Final outputs
│   ├── video/
│   ├── audio/
│   └── graphics/
└── documentation/
    ├── scripts/
    ├── storyboards/
    └── approval-emails/
```

### Archive Storage
- **Compress:** ZIP or 7Z with compression
- **Name:** `[project-name]-archive-[YYYY-MM].zip`
- **Upload:** Azure Blob Archive tier
- **Catalog:** Add to asset database
- **Verify:** Checksum validation
```

## Rights & Licensing

### License Tracking

```yaml
asset_licenses:
  music:
    - title: "Corporate Innovation"
      source: "Epidemic Sound"
      license_type: "Commercial Subscription"
      expiration: "2026-12-31"
      usage_rights: "Unlimited commercial use"
      attribution: "Not required"

  stock_footage:
    - title: "City Skyline Timelapse"
      source: "Pexels"
      license_type: "Pexels License"
      usage_rights: "Free commercial use"
      attribution: "Optional but appreciated"

  icons:
    - title: "Azure Architecture Icons"
      source: "Microsoft"
      license_type: "Microsoft License"
      usage_rights: "Use in Microsoft-related content"
      attribution: "Required"

  fonts:
    - title: "Segoe UI"
      source: "Microsoft"
      license_type: "Microsoft EULA"
      usage_rights: "Windows/Office projects"
```

## Related Resources

- [Video Production Workflow](video-production-workflow.md)
- [Quality Assurance Guide](quality-assurance.md)
- [Publishing Workflow](publishing-workflow.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
