# 🤝 Contributing to CSA Multimedia

> **🏠 [Home](../../README.md)** | **📖 [Documentation](../README.md)** | **🎬 [Multimedia](./ README.md)** | **🤝 Contributing**

![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)
![Contributors: Welcome](https://img.shields.io/badge/Contributors-Welcome-blue)
![Review: Required](https://img.shields.io/badge/Review-Required-orange)

## 📋 Overview

Thank you for your interest in contributing to Cloud Scale Analytics multimedia content! This guide will help you understand how to contribute videos, diagrams, interactive demos, and other multimedia assets effectively.

## 🎯 Contribution Types

### 1. Video Content

Contribute tutorial videos, demos, or walkthroughs:

**What We Need:**
- Azure Synapse tutorials
- Data engineering demos
- Best practices videos
- Quick tips (< 3 minutes)

**Requirements:**
- 1080p minimum resolution
- Clear audio (no background noise)
- Follow brand guidelines
- Include captions/transcripts
- Maximum 15 minutes duration

### 2. Diagrams & Graphics

Create or improve architecture diagrams and illustrations:

**What We Need:**
- Architecture diagrams
- Data flow visualizations
- Process flowcharts
- Infographics

**Requirements:**
- Use official Azure icons
- Follow color palette
- SVG format preferred
- Editable source files

### 3. Interactive Demos

Build hands-on demonstrations:

**What We Need:**
- Code playgrounds
- Configuration wizards
- Interactive tutorials
- Query builders

**Requirements:**
- TypeScript/JavaScript
- React components preferred
- Responsive design
- Accessibility compliant

### 4. Audio Content

Provide narration, voiceovers, or audio guides:

**What We Need:**
- Video narration
- Podcast content
- Audio tutorials

**Requirements:**
- Professional audio quality
- Clear pronunciation
- Follow script guidelines
- Include written transcript

## 🚀 Getting Started

### Step 1: Choose Your Contribution

1. Browse [open content requests](https://github.com/csa-inabox/csa-inabox-docs/issues?q=is%3Aissue+is%3Aopen+label%3Amultimedia)
2. Check [multimedia roadmap](https://github.com/csa-inabox/csa-inabox-docs/projects/multimedia-roadmap)
3. Or propose new content via [content request](../requests/README.md)

### Step 2: Set Up Environment

```bash
# Clone repository
git clone https://github.com/csa-inabox/csa-inabox-docs.git
cd csa-inabox-docs

# Create feature branch
git checkout -b multimedia/your-contribution-name

# Install dependencies
npm install

# Install multimedia tools
npm install -g @csa/media-toolkit
```

### Step 3: Review Guidelines

Required reading before contributing:
- [Brand Guidelines](production-guide/brand-guidelines.md)
- [Quality Standards](production-guide/quality-assurance.md)
- [Markdown Style Guide](../guides/MARKDOWN_STYLE_GUIDE.md)
- [Accessibility Standards](tools/accessibility/README.md)

## 📝 Contribution Workflow

### 1. Create Content

Follow the appropriate guide:
- **Videos:** [Video Production Guide](production-guide/video-production-workflow.md)
- **Diagrams:** [Graphics Production Guide](production-guide/graphics-production.md)
- **Demos:** [Interactive Demo Guide](interactive-demos/README.md)
- **Audio:** [Audio Production Guide](production-guide/audio-production-workflow.md)

### 2. Add Metadata

Create metadata file alongside your content:

```yaml
# video-metadata.yaml
title: "Azure Synapse Spark Pool Setup"
description: "Step-by-step tutorial for configuring Apache Spark pools in Azure Synapse Analytics"
duration: "8:45"
format: "mp4"
resolution: "1920x1080"
file_size: "125 MB"
captions: true
transcript: "video-transcript.txt"
created_by: "Your Name"
created_date: "2025-01-15"
tags:
  - azure-synapse
  - spark-pools
  - tutorial
  - setup
license: "MIT"
attribution_required: false
```

### 3. Optimize Assets

Use CSA media tools to optimize:

```bash
# Optimize video
csa-video-optimize input.mp4 --preset web --output optimized.mp4

# Optimize images
csa-image-optimize ./images --format webp --quality 85

# Generate captions
csa-caption-generate video.mp4 --language en-US --output captions.srt

# Validate accessibility
csa-accessibility-check ./content --standard wcag21-aa
```

### 4. Test Locally

```bash
# Build documentation site
mkdocs serve

# View at http://localhost:8000

# Run tests
npm test

# Lint markdown
markdownlint docs/**/*.md

# Validate links
markdown-link-check docs/**/*.md
```

### 5. Submit Pull Request

```bash
# Add files
git add docs/multimedia/

# Commit with descriptive message
git commit -m "feat(multimedia): add Spark pool setup tutorial video

- 1080p video with captions
- Includes transcript and metadata
- Optimized for web delivery
- Duration: 8:45"

# Push to your fork
git push origin multimedia/your-contribution-name

# Create pull request on GitHub
gh pr create --title "Add Spark pool setup tutorial" --body "Description of changes"
```

## 📋 Pull Request Checklist

Before submitting, ensure:

### Content Quality
- [ ] Follows brand guidelines
- [ ] Professional quality (video/audio/design)
- [ ] Free of errors and typos
- [ ] Tested and verified

### Accessibility
- [ ] Captions provided (videos)
- [ ] Transcripts included (audio/video)
- [ ] Alt text for images
- [ ] Color contrast meets WCAG AA
- [ ] Keyboard navigation works (interactive demos)

### Technical Requirements
- [ ] Optimized file sizes
- [ ] Proper formats (MP4, WebP, SVG, etc.)
- [ ] Metadata files included
- [ ] Source files provided (if applicable)

### Documentation
- [ ] README.md updated (if needed)
- [ ] Usage examples provided
- [ ] Related documentation linked

### Legal
- [ ] You own rights to content
- [ ] No copyrighted material (unless licensed)
- [ ] Proper attribution for stock assets
- [ ] License specified

## 🔍 Review Process

### Automated Checks

Your PR will be automatically checked for:
- Markdown linting
- Link validation
- Image optimization
- Accessibility compliance
- File size limits

### Human Review

Multimedia team will review:
- Content quality and accuracy
- Brand guideline adherence
- Technical correctness
- Accessibility standards
- User experience

### Review Timeline

| Priority | Initial Review | Full Review | Merge |
|----------|----------------|-------------|-------|
| Critical | Same day | 1-2 days | 2-3 days |
| High | 1 day | 2-3 days | 3-5 days |
| Medium | 2-3 days | 3-5 days | 5-7 days |
| Low | 3-5 days | 5-7 days | 7-14 days |

## 🎨 Style Guidelines

### Video Style

```markdown
## Technical Requirements
- Resolution: 1920x1080 (minimum)
- Frame Rate: 30 fps
- Format: MP4 (H.264)
- Audio: AAC, 128 kbps minimum
- Bitrate: 5 Mbps recommended

## Content Guidelines
- Clear narration (no background noise)
- Consistent pacing
- Professional tone
- Visual clarity
- Logical structure
- Call-to-action at end
```

### Design Style

```markdown
## Visual Standards
- Use CSA color palette
- Official Azure icons only
- Segoe UI font family
- Consistent spacing (16px grid)
- Professional, clean design
- Accessible color contrast

## Diagram Guidelines
- Clear labels
- Logical flow (left-to-right, top-to-bottom)
- Consistent icon sizing
- Descriptive annotations
- Export as SVG
```

### Code Style

```markdown
## Interactive Demo Code
- TypeScript preferred
- ESLint compliant
- Prettier formatted
- Well-commented
- Modular components
- Accessibility attributes
- Responsive design
```

## 🧪 Testing Requirements

### Video Testing

```bash
# Validate video format
ffprobe video.mp4

# Check accessibility
csa-caption-validate captions.srt --video video.mp4

# Test across browsers
npm run test:video
```

### Interactive Demo Testing

```bash
# Unit tests
npm test

# E2E tests
npm run test:e2e

# Accessibility tests
npm run test:a11y

# Cross-browser tests
npm run test:browsers
```

## 💬 Communication

### Getting Help

- **Questions:** [GitHub Discussions](https://github.com/csa-inabox/csa-inabox-docs/discussions)
- **Issues:** [GitHub Issues](https://github.com/csa-inabox/csa-inabox-docs/issues)
- **Teams:** CSA Multimedia Channel
- **Email:** multimedia@csa.azure.com

### Office Hours

Join weekly office hours:
- **When:** Wednesdays 2-3 PM EST
- **Where:** Microsoft Teams
- **Topics:** Content review, Q&A, collaboration

## 🏆 Recognition

### Contributors

All contributors are recognized:
- Listed in [CONTRIBUTORS.md](../../CONTRIBUTORS.md)
- Featured in release notes
- Acknowledged in content credits

### Rewards

Significant contributions may receive:
- Azure credits
- Conference passes
- Swag and merchandise
- LinkedIn recommendations
- Public recognition

## 📚 Resources

### Templates

- [Video Script Template](templates/video-script-template.md)
- [Diagram Template](templates/diagram-template.fig)
- [Demo Component Template](templates/demo-component-template.tsx)

### Tools

- [CSA Media Toolkit](tools/README.md)
- [Image Optimizer](tools/image-optimization.md)
- [Caption Generator](tools/accessibility/README.md)

### Learning Resources

- [Azure Documentation](https://docs.microsoft.com/azure/)
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- [React Documentation](https://react.dev/)
- [Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

## 🤔 FAQ

### Can I contribute if I'm not a developer?

Yes! We welcome contributions from:
- Content creators
- Technical writers
- Designers
- Video editors
- Audio engineers
- Translators

### What if my contribution is rejected?

We'll provide detailed feedback on why and suggestions for improvement. You're welcome to revise and resubmit.

### How long does review take?

Typically 3-7 days depending on complexity and priority. Critical fixes are reviewed within 24 hours.

### Can I work on multiple contributions?

Yes, but please submit separate PRs for each contribution for easier review.

### Do I need special software?

Recommended tools:
- Video: Adobe Premiere Pro, DaVinci Resolve (free)
- Graphics: Figma (free), Adobe Illustrator
- Audio: Audacity (free), Adobe Audition
- Code: VS Code (free)

### How do I get Azure access for demos?

Contact the team at multimedia@csa.azure.com for sandbox environment access.

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## 🙏 Thank You

Thank you for contributing to Cloud Scale Analytics! Your efforts help thousands of developers and data engineers learn and succeed with Azure.

---

*Last Updated: January 2025 | Version: 1.0.0*

**Questions? Contact:** multimedia@csa.azure.com
