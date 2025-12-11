# 🎨 Brand Assets & Resources

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎨 Brand**

![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)
![Type: Assets](https://img.shields.io/badge/Type-Assets-blue)
![Access: Controlled](https://img.shields.io/badge/Access-Controlled-orange)

## 📋 Overview

Centralized repository for Cloud Scale Analytics brand assets, including logos, color palettes, typography, templates, and brand guidelines. All assets are optimized for web and aligned with Microsoft Azure design principles.

## 🎯 Quick Access

### Essential Assets

| Asset Type | Format | Download | Usage |
|------------|--------|----------|-------|
| Logo (Primary) | SVG, PNG | [Download](assets/logo-primary.svg) | Main brand representation |
| Logo (White) | SVG, PNG | [Download](assets/logo-white.svg) | Dark backgrounds |
| Logo (Icon Only) | SVG, PNG | [Download](assets/logo-icon.svg) | Favicons, small spaces |
| Color Palette | CSS, SCSS | [Download](assets/colors.css) | Web development |
| Typography | WOFF2, TTF | [Download](assets/fonts/) | All text content |
| Templates | Various | [Browse](../templates/README.md) | Video, presentations |

## 🎨 Brand Colors

### Primary Colors

```css
/* Azure Blue - Primary Brand Color */
--color-azure-blue: #0078D4;
--color-azure-blue-rgb: 0, 120, 212;

/* Azure Light Blue - Accents & Highlights */
--color-azure-light-blue: #50E6FF;
--color-azure-light-blue-rgb: 80, 230, 255;

/* Azure Dark Blue - Backgrounds & Depth */
--color-azure-dark-blue: #003D73;
--color-azure-dark-blue-rgb: 0, 61, 115;
```

### Secondary Colors

```css
/* Azure Orange - CTAs & Important Actions */
--color-azure-orange: #FF6B00;
--color-azure-orange-rgb: 255, 107, 0;

/* Azure Purple - Innovation & AI/ML */
--color-azure-purple: #5E5BE5;
--color-azure-purple-rgb: 94, 91, 229;

/* Azure Green - Success States */
--color-azure-green: #107C10;
--color-azure-green-rgb: 16, 124, 16;
```

### Neutral Colors

```css
/* Text Colors */
--color-text-primary: #323130;
--color-text-secondary: #605E5C;
--color-text-disabled: #A19F9D;

/* Background Colors */
--color-bg-primary: #FFFFFF;
--color-bg-secondary: #F5F5F5;
--color-bg-tertiary: #EDEBE9;

/* Border Colors */
--color-border: #EDEBE9;
--color-border-hover: #C8C6C4;
```

### Semantic Colors

```css
/* Status Colors */
--color-success: #107C10;
--color-warning: #FFB900;
--color-error: #D13438;
--color-info: #0078D4;
```

**Color Swatches:**

![Azure Blue](https://img.shields.io/badge/-0078D4-0078D4?style=for-the-badge)
![Azure Light Blue](https://img.shields.io/badge/-50E6FF-50E6FF?style=for-the-badge)
![Azure Orange](https://img.shields.io/badge/-FF6B00-FF6B00?style=for-the-badge)
![Azure Purple](https://img.shields.io/badge/-5E5BE5-5E5BE5?style=for-the-badge)

## 🔤 Typography

### Font Family

```css
/* Primary Font - Segoe UI */
--font-family-primary: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;

/* Monospace Font - For Code */
--font-family-mono: Consolas, "Courier New", monospace;

/* Variable Font - Modern Displays */
--font-family-variable: "Segoe UI Variable", "Segoe UI", sans-serif;
```

### Type Scale

```css
/* Headings */
--font-size-h1: 48px;  /* 3rem */
--font-size-h2: 32px;  /* 2rem */
--font-size-h3: 24px;  /* 1.5rem */
--font-size-h4: 20px;  /* 1.25rem */

/* Body Text */
--font-size-large: 18px;  /* 1.125rem */
--font-size-body: 16px;   /* 1rem */
--font-size-small: 14px;  /* 0.875rem */
--font-size-tiny: 12px;   /* 0.75rem */

/* Line Heights */
--line-height-heading: 1.2;
--line-height-body: 1.5;
--line-height-code: 1.6;
```

### Font Weights

```css
--font-weight-light: 300;
--font-weight-normal: 400;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

## 🖼️ Logo Usage

### Logo Variations

```markdown
## Primary Logo
- **Usage:** Main brand representation on light backgrounds
- **Formats:** SVG (vector), PNG (300dpi)
- **Minimum Size:** 120px width
- **Clear Space:** Equal to logo height on all sides

## Reversed Logo (White)
- **Usage:** Dark backgrounds, video overlays
- **Formats:** SVG, PNG with transparency
- **Minimum Size:** 120px width

## Icon Only
- **Usage:** Favicons, app icons, social media profile
- **Formats:** SVG, PNG, ICO
- **Sizes:** 16x16, 32x32, 64x64, 512x512
```

### Logo Don'ts

```markdown
❌ Don't stretch or distort the logo
❌ Don't change logo colors
❌ Don't add effects (shadows, glows, gradients)
❌ Don't rotate or angle the logo
❌ Don't place on busy backgrounds without contrast
❌ Don't use old logo versions
```

## 📦 Asset Downloads

### Logos

```bash
# Download all logo variations
curl -O https://cdn.csa.azure.com/brand/logos/csa-logo-pack.zip

# Individual downloads
curl -O https://cdn.csa.azure.com/brand/logos/csa-logo-primary.svg
curl -O https://cdn.csa.azure.com/brand/logos/csa-logo-white.svg
curl -O https://cdn.csa.azure.com/brand/logos/csa-logo-icon.svg
```

### Color Palettes

```bash
# CSS Variables
curl -O https://cdn.csa.azure.com/brand/colors/colors.css

# SCSS Variables
curl -O https://cdn.csa.azure.com/brand/colors/colors.scss

# Figma Palette
curl -O https://cdn.csa.azure.com/brand/colors/csa-colors.fig

# Adobe Swatches
curl -O https://cdn.csa.azure.com/brand/colors/csa-colors.ase
```

### Typography

```bash
# Web Fonts (WOFF2)
curl -O https://cdn.csa.azure.com/brand/fonts/segoe-ui-webfont.zip

# Font Specimens
curl -O https://cdn.csa.azure.com/brand/fonts/font-specimens.pdf
```

## 🎬 Video & Animation Assets

### Intro/Outro Slates

```markdown
## Video Intro Slate (5 seconds)
- **Resolution:** 1920x1080 (Full HD)
- **Format:** MP4 (H.264), WebM (VP9)
- **With Audio:** Background music fade-in
- **Download:** [intro-5s.mp4](assets/video/intro-5s.mp4)

## Video Outro Slate (5 seconds)
- **Resolution:** 1920x1080 (Full HD)
- **Format:** MP4, WebM
- **With Audio:** Background music fade-out
- **Download:** [outro-5s.mp4](assets/video/outro-5s.mp4)
```

### Lower Thirds

```markdown
## Animated Lower Third
- **Duration:** 8 seconds (fade in/out)
- **Format:** After Effects project, MP4 with alpha
- **Customizable:** Text fields, colors
- **Download:** [lower-third.aep](assets/video/lower-third.aep)
```

### Motion Graphics

```markdown
## Logo Animation
- **Duration:** 3 seconds
- **Format:** After Effects, Lottie JSON
- **Usage:** Loading screens, intros
- **Download:** [logo-animation.json](assets/motion/logo-animation.json)
```

## 🎵 Audio Assets

### Background Music

```markdown
## Corporate Intro Theme (15 seconds)
- **Style:** Uplifting, professional
- **Tempo:** 120 BPM
- **License:** Royalty-free for CSA use
- **Format:** MP3, WAV
- **Download:** [intro-music.mp3](assets/audio/intro-music.mp3)

## Background Bed (Loop)
- **Duration:** 3:00 (seamless loop)
- **Style:** Ambient, subtle technology
- **Usage:** Background during narration
- **Volume:** -25dB under voice
- **Download:** [background-loop.mp3](assets/audio/background-loop.mp3)
```

### Sound Effects

```markdown
## Transition Sounds
- **Whoosh:** Section transitions
- **Click:** UI interactions
- **Chime:** Success notifications
- **Download:** [sound-effects.zip](assets/audio/sound-effects.zip)
```

## 📐 Design Templates

### Presentation Templates

```markdown
## PowerPoint Templates
- **Standard Deck:** General presentations
- **Technical Deck:** Deep-dive technical content
- **Executive Deck:** Executive summaries
- **Download:** [powerpoint-templates.zip](assets/templates/powerpoint-templates.zip)

## Google Slides Templates
- **Same variations as PowerPoint**
- **Download:** [Google Slides Link](https://docs.google.com/presentation/...)
```

### Graphics Templates

```markdown
## Figma Design System
- **Components:** Buttons, cards, icons
- **Templates:** Social media, diagrams
- **Access:** [Figma File](https://figma.com/file/...)

## Adobe Illustrator Templates
- **Architecture Diagrams**
- **Infographics**
- **Data Visualizations**
- **Download:** [illustrator-templates.zip](assets/templates/illustrator-templates.zip)
```

## 🔐 Access & Licensing

### Internal Use

```markdown
All brand assets are available for internal use by CSA team members and contributors.

✅ Permitted Uses:
- Documentation and tutorials
- Presentations and training materials
- Marketing and promotional content
- Social media posts
- Internal communications

❌ Not Permitted:
- Redistribution of brand assets
- Commercial use outside CSA project
- Modification of logos without approval
- Use in competitive products
```

### External Use

```markdown
External parties wishing to use CSA brand assets must:
1. Request permission via email: brand@csa.azure.com
2. Provide usage context and examples
3. Receive written approval
4. Follow brand guidelines
5. Include proper attribution
```

### Attribution

```markdown
When using CSA brand assets, include:

"Cloud Scale Analytics" and associated logos are property of [Organization Name].
Used with permission under [License Type].
```

## 📚 Brand Guidelines

Full brand guidelines available at:
- [Brand Guidelines PDF](../production-guide/brand-guidelines.md)
- [Visual Style Guide](../../VISUAL-STYLE-GUIDE.md)
- [Markdown Style Guide](../../guides/MARKDOWN_STYLE_GUIDE.md)

## 🔗 Related Resources

- [Production Guide](../production-guide/README.md)
- [Templates Library](../templates/README.md)
- [Asset Management](../production-guide/asset-management.md)

## 📞 Contact

Questions about brand assets?
- Email: brand@csa.azure.com
- Teams: [CSA Brand Channel](https://teams.microsoft.com/...)
- GitHub: [Issue Tracker](https://github.com/csa-inabox/csa-inabox-docs/issues)

---

*Last Updated: January 2025 | Version: 1.0.0*
