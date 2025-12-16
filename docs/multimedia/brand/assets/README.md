# 📦 Brand Assets Collection

> **🏠 [Home](../../../../README.md)** | **📖 [Documentation](../../../README.md)** | **🎬 [Multimedia](../../README.md)** | **🎨 [Brand](../README.md)** | **📦 Assets**

![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)
![Type: Repository](https://img.shields.io/badge/Type-Repository-blue)
![Format: Multiple](https://img.shields.io/badge/Format-Multiple-purple)

## 📋 Overview

Complete collection of Cloud Scale Analytics brand assets including logos, icons, images, fonts, and templates. All assets are production-ready and optimized for various media formats.

## 📁 Directory Structure

```
assets/
├── logos/
│   ├── svg/                    # Vector logos (scalable)
│   ├── png/                    # Raster logos (various sizes)
│   ├── ico/                    # Favicon formats
│   └── social/                 # Social media profile images
│
├── icons/
│   ├── azure-services/         # Azure service icons
│   ├── ui-elements/            # UI component icons
│   └── custom/                 # Custom CSA icons
│
├── colors/
│   ├── swatches/               # Color palette files
│   ├── css/                    # CSS/SCSS variables
│   └── samples/                # Color usage examples
│
├── fonts/
│   ├── segoe-ui/               # Primary font family
│   ├── consolas/               # Monospace font
│   └── webfonts/               # Web-optimized fonts
│
├── images/
│   ├── hero/                   # Hero/banner images
│   ├── backgrounds/            # Background patterns
│   ├── screenshots/            # Product screenshots
│   └── stock/                  # Stock images (licensed)
│
├── video/
│   ├── intros/                 # Video intro slates
│   ├── outros/                 # Video outro slates
│   ├── lower-thirds/           # Lower third animations
│   └── transitions/            # Transition effects
│
├── audio/
│   ├── music/                  # Background music
│   ├── effects/                # Sound effects
│   └── voiceovers/             # Voice samples
│
└── templates/
    ├── powerpoint/             # Presentation templates
    ├── figma/                  # Figma design files
    ├── after-effects/          # Video templates
    └── illustrator/            # Graphic templates
```

## 🖼️ Logo Assets

### Vector Logos (SVG)

```markdown
## Primary Logo - Full Color
**File:** `logos/svg/csa-logo-primary.svg`
**Usage:** Main brand representation
**Background:** Light/white backgrounds
**Minimum Size:** 120px width

## Reversed Logo - White
**File:** `logos/svg/csa-logo-white.svg`
**Usage:** Dark backgrounds
**Background:** Dark colors, video overlays
**Minimum Size:** 120px width

## Icon Only - Square
**File:** `logos/svg/csa-icon-square.svg`
**Usage:** Favicons, small spaces, app icons
**Sizes Available:** 16x16 to 1024x1024
```

### Raster Logos (PNG)

Available in multiple resolutions:
- 64x64 (Tiny)
- 128x128 (Small)
- 256x256 (Medium)
- 512x512 (Large)
- 1024x1024 (Extra Large)
- 2048x2048 (Print Quality)

### Favicon Package

```markdown
**Package:** `logos/ico/favicon-package.zip`
**Contents:**
- favicon.ico (16x16, 32x32, 48x48)
- favicon-16x16.png
- favicon-32x32.png
- favicon-96x96.png
- apple-touch-icon.png (180x180)
- android-chrome-192x192.png
- android-chrome-512x512.png
- site.webmanifest
```

## 🎨 Color Assets

### Swatch Files

```markdown
## Adobe Swatch Exchange (.ase)
**File:** `colors/swatches/csa-colors.ase`
**Compatible:** Photoshop, Illustrator, InDesign

## Figma Palette (.fig)
**File:** `colors/swatches/csa-figma-palette.fig`
**Import:** Figma > Plugins > Import Palette

## Sketch Palette (.sketchpalette)
**File:** `colors/swatches/csa-sketch-palette.sketchpalette`
**Import:** Sketch > Document > Import Palette
```

### CSS/SCSS Variables

```css
/* File: colors/css/colors.css */
:root {
  /* Primary Colors */
  --azure-blue: #0078D4;
  --azure-light-blue: #50E6FF;
  --azure-dark-blue: #003D73;

  /* Secondary Colors */
  --azure-orange: #FF6B00;
  --azure-purple: #5E5BE5;
  --azure-green: #107C10;

  /* Neutral Colors */
  --gray-90: #323130;
  --gray-70: #605E5C;
  --gray-50: #A19F9D;
  --gray-30: #C8C6C4;
  --gray-10: #EDEBE9;

  /* Semantic Colors */
  --success: #107C10;
  --warning: #FFB900;
  --error: #D13438;
  --info: #0078D4;
}
```

## 🔤 Font Assets

### Web Fonts (WOFF2)

```markdown
## Segoe UI Family
**Files:** `fonts/webfonts/segoe-ui/`
- SegoeUI-Light.woff2 (300)
- SegoeUI-Regular.woff2 (400)
- SegoeUI-Semibold.woff2 (600)
- SegoeUI-Bold.woff2 (700)

## Consolas (Monospace)
**Files:** `fonts/webfonts/consolas/`
- Consolas-Regular.woff2 (400)
- Consolas-Bold.woff2 (700)
```

### Font CSS

```css
/* File: fonts/webfonts/fonts.css */
@font-face {
  font-family: 'Segoe UI';
  src: url('./segoe-ui/SegoeUI-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Segoe UI';
  src: url('./segoe-ui/SegoeUI-Bold.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Consolas';
  src: url('./consolas/Consolas-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

## 📸 Image Assets

### Hero Images

High-resolution hero images for landing pages and headers:
- **Resolution:** 2560x1440 (2K)
- **Format:** JPEG, WebP
- **Optimized:** Yes (< 500KB)
- **Location:** `images/hero/`

### Background Patterns

Subtle patterns for backgrounds:
- **Resolution:** Tileable 512x512
- **Format:** PNG with transparency
- **Usage:** Section backgrounds, cards
- **Location:** `images/backgrounds/`

### Screenshots

Product and interface screenshots:
- **Resolution:** Various (1920x1080 typical)
- **Format:** PNG, WebP
- **Annotations:** Available with/without
- **Location:** `images/screenshots/`

## 🎬 Video Assets

### Intro Slate (5 seconds)

```markdown
**File:** `video/intros/csa-intro-5s.mp4`
**Resolution:** 1920x1080 (Full HD)
**Codecs:** H.264 (MP4), VP9 (WebM)
**Audio:** Background music (fade in)
**File Size:** ~5 MB (MP4), ~3 MB (WebM)
```

### Outro Slate (5 seconds)

```markdown
**File:** `video/outros/csa-outro-5s.mp4`
**Resolution:** 1920x1080 (Full HD)
**Codecs:** H.264 (MP4), VP9 (WebM)
**Audio:** Background music (fade out)
**Includes:** Call-to-action, links, logo
```

### Lower Third Templates

```markdown
**Package:** `video/lower-thirds/lower-third-pack.zip`
**Contents:**
- After Effects project (.aep)
- Exported renders (MP4 with alpha)
- Customization guide
- Color variations
```

## 🎵 Audio Assets

### Background Music

```markdown
## Intro Theme (15 seconds)
**File:** `audio/music/intro-theme-15s.mp3`
**Style:** Corporate, uplifting
**Tempo:** 120 BPM
**License:** Royalty-free for CSA use

## Background Loop (3 minutes)
**File:** `audio/music/background-loop-180s.mp3`
**Style:** Ambient, subtle
**Usage:** Behind narration (-25dB)
**License:** Royalty-free for CSA use
```

### Sound Effects

```markdown
**Package:** `audio/effects/sound-effects-pack.zip`
**Contents:**
- Whoosh transitions (5 variations)
- UI clicks (10 variations)
- Success chimes (3 variations)
- Notification sounds (5 variations)
**Format:** WAV 48kHz/24-bit, MP3 320kbps
```

## 📐 Template Assets

### PowerPoint Templates

```markdown
**Package:** `templates/powerpoint/csa-ppt-templates.zip`
**Contents:**
- Standard Deck (16:9)
- Technical Deck (16:9)
- Executive Summary (16:9)
- Wide Screen (21:9)
**Features:**
- Master slides
- Color themes
- Font styles
- Diagram layouts
```

### Figma Design System

```markdown
**File:** `templates/figma/csa-design-system.fig`
**Components:**
- Buttons and controls
- Form elements
- Cards and containers
- Navigation components
- Icons and illustrations
**Plugins Recommended:**
- Auto Layout
- Content Reel
- Figmotion
```

### After Effects Templates

```markdown
**Package:** `templates/after-effects/csa-ae-templates.zip`
**Contents:**
- Intro slate template
- Outro slate template
- Lower third animations
- Title cards
- Transition effects
**Requirements:** After Effects CC 2020 or later
```

## 📥 Download Instructions

### Azure Blob Storage

```bash
# Install Azure CLI
az storage blob download-batch \
  --account-name csamediastorage \
  --source brand-assets \
  --destination ./csa-brand-assets \
  --pattern "*.{svg,png,css,mp4,mp3}"
```

### Azure CDN

```bash
# Download entire asset pack
curl -O https://cdn.csa.azure.com/brand/csa-brand-assets-complete.zip

# Download specific categories
curl -O https://cdn.csa.azure.com/brand/logos.zip
curl -O https://cdn.csa.azure.com/brand/colors.zip
curl -O https://cdn.csa.azure.com/brand/fonts.zip
curl -O https://cdn.csa.azure.com/brand/templates.zip
```

### GitHub Repository

```bash
# Clone repository
git clone https://github.com/csa-inabox/brand-assets.git

# Sparse checkout (specific folders only)
git sparse-checkout set assets/logos assets/colors
```

## 🔒 Usage Guidelines

### Permitted Uses

✅ Documentation and tutorials
✅ Presentations and training
✅ Marketing materials
✅ Social media posts
✅ Internal communications
✅ Partner presentations (with approval)

### Restricted Uses

❌ Logo modifications without approval
❌ Redistribution of assets
❌ Commercial use outside CSA
❌ Competitive products
❌ Misleading representations

## 📚 Related Resources

- [Brand Guidelines](../../production-guide/brand-guidelines.md)
- [Visual Style Guide](../../../VISUAL-STYLE-GUIDE.md)
- [Asset Management](../../production-guide/asset-management.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
