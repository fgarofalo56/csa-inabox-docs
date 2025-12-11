# Brand Guidelines

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **📎 [Production Guide](README.md)** | **🎨 Brand Guidelines**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: Standards](https://img.shields.io/badge/Type-Standards-blue)

## Overview

Brand guidelines for Cloud Scale Analytics multimedia content ensure consistency, professionalism, and recognizability across all video, audio, and graphic productions.

## Visual Identity

### Color Palette

```yaml
primary_colors:
  azure_blue:
    hex: "#0078D4"
    rgb: "0, 120, 212"
    cmyk: "100, 43, 0, 17"
    usage: "Primary brand color, headings, CTAs, Azure branding"

  azure_light_blue:
    hex: "#50E6FF"
    rgb: "80, 230, 255"
    cmyk: "69, 0, 0, 0"
    usage: "Accents, highlights, data visualizations"

secondary_colors:
  azure_dark_blue:
    hex: "#003D73"
    rgb: "0, 61, 115"
    usage: "Backgrounds, gradients, dark themes"

  azure_orange:
    hex: "#FF6B00"
    rgb: "255, 107, 0"
    usage: "Warnings, important callouts, energy"

  azure_purple:
    hex: "#5E5BE5"
    rgb: "94, 91, 229"
    usage: "AI/ML topics, innovation themes"

neutral_colors:
  dark_gray:
    hex: "#323130"
    rgb: "50, 49, 48"
    usage: "Body text, primary text"

  medium_gray:
    hex: "#605E5C"
    rgb: "96, 94, 92"
    usage: "Secondary text, captions"

  light_gray:
    hex: "#EDEBE9"
    rgb: "237, 235, 233"
    usage: "Backgrounds, dividers"

  white:
    hex: "#FFFFFF"
    rgb: "255, 255, 255"
    usage: "Primary background, contrast"

semantic_colors:
  success:
    hex: "#107C10"
    usage: "Success states, confirmations"

  warning:
    hex: "#FFB900"
    usage: "Warnings, cautions"

  error:
    hex: "#D13438"
    usage: "Errors, critical alerts"

  info:
    hex: "#0078D4"
    usage: "Information, tips"
```

### Typography

```yaml
font_family:
  primary:
    name: "Segoe UI"
    fallback: "Tahoma, Geneva, Verdana, sans-serif"
    usage: "All UI text, headings, body copy"
    weights: [300, 400, 600, 700]

  monospace:
    name: "Consolas"
    fallback: "Courier New, monospace"
    usage: "Code snippets, technical data"
    weights: [400, 700]

  alternative:
    name: "Segoe UI Variable"
    usage: "Modern displays, variable font support"

type_scale:
  h1:
    size: "48px / 3rem"
    weight: 700
    line_height: "1.2"
    usage: "Main titles, video intros"

  h2:
    size: "32px / 2rem"
    weight: 600
    line_height: "1.3"
    usage: "Section headings"

  h3:
    size: "24px / 1.5rem"
    weight: 600
    line_height: "1.4"
    usage: "Subsection headings"

  body_large:
    size: "18px / 1.125rem"
    weight: 400
    line_height: "1.6"
    usage: "Intro text, emphasized content"

  body:
    size: "16px / 1rem"
    weight: 400
    line_height: "1.5"
    usage: "Main body text"

  small:
    size: "14px / 0.875rem"
    weight: 400
    line_height: "1.5"
    usage: "Captions, metadata"

  code:
    size: "14px / 0.875rem"
    weight: 400
    line_height: "1.6"
    family: "Consolas"
    usage: "Code snippets"
```

### Logo Usage

```markdown
## Logo Specifications

### Primary Logo
- **Format:** SVG (vector) or PNG (minimum 300dpi)
- **Minimum Size:** 120px width
- **Clear Space:** Minimum padding equal to logo height
- **Placement:** Top-left or center (intro/outro slates)

### Logo Variations
1. **Full Color:** Primary use on white/light backgrounds
2. **Reversed:** White logo on dark backgrounds
3. **Monochrome:** Single color when color not available

### Don'ts
- ❌ Don't stretch or distort the logo
- ❌ Don't change logo colors
- ❌ Don't add effects (shadows, glows, gradients)
- ❌ Don't place on busy backgrounds
- ❌ Don't rotate or angle the logo
```

## Video Branding Standards

### Intro Slate

```yaml
intro_slate:
  duration: "3-5 seconds"
  composition:
    background:
      type: "Gradient"
      colors: ["#0078D4", "#003D73"]
      direction: "135deg"

    logo:
      position: "Center"
      animation: "Fade in + slight scale"
      duration: "1 second"

    title:
      text: "[Video Title]"
      position: "Below logo"
      font: "Segoe UI Bold, 32px"
      color: "#FFFFFF"
      animation: "Fade in from bottom"

    music:
      file: "corporate_intro.mp3"
      duration: "Full 5 seconds"
      fade_out: "Last 1 second"

template_file: "templates/csa_intro_slate.aep"
```

### Lower Thirds

```yaml
lower_thirds:
  position:
    horizontal: "Left aligned, 60px from edge"
    vertical: "Bottom third, 100px from bottom"

  design:
    background:
      color: "rgba(0, 120, 212, 0.9)"  # Azure Blue 90% opacity
      height: "80px"
      width: "500px"
      border_radius: "4px"

    primary_text:
      content: "[Name / Topic]"
      font: "Segoe UI Bold, 24px"
      color: "#FFFFFF"
      position: "20px padding from left"

    secondary_text:
      content: "[Title / Description]"
      font: "Segoe UI Regular, 18px"
      color: "#50E6FF"  # Light blue
      position: "Below primary, 5px spacing"

  animation:
    entrance: "Slide from left, 0.5s ease-out"
    duration: "5-8 seconds on screen"
    exit: "Fade out, 0.3s"

  usage:
    - "Speaker introduction"
    - "Topic transitions"
    - "Key concepts highlight"
    - "Resource callouts"
```

### Outro Slate

```yaml
outro_slate:
  duration: "5-7 seconds"
  composition:
    background:
      type: "Solid color with subtle texture"
      color: "#FAFAFA"

    call_to_action:
      text: "Learn More"
      font: "Segoe UI Bold, 36px"
      color: "#323130"
      position: "Top center"

    resources:
      type: "List of links"
      items:
        - "Documentation: docs.cloudscaleanalytics.com"
        - "GitHub: github.com/csa-inabox"
        - "Contact: info@cloudscaleanalytics.com"
      font: "Segoe UI Regular, 20px"
      color: "#605E5C"
      position: "Center"

    logo:
      position: "Bottom center"
      size: "120px width"

    music:
      file: "corporate_outro.mp3"
      fade_in: "First 1 second"
      full_volume: "3 seconds"
      fade_out: "Last 1 second"
```

## Audio Branding

### Music Selection

```yaml
music_guidelines:
  style:
    - "Corporate"
    - "Ambient"
    - "Electronic (subtle)"
    - "Motivational (soft)"

  characteristics:
    tempo: "80-120 BPM"
    energy: "Low to medium"
    instrumentation: "Minimal vocals or instrumental only"
    mood: "Professional, confident, innovative"

  licensed_tracks:
    intro_theme:
      name: "Corporate Innovation"
      duration: "0:15"
      usage: "Video intros"
      license: "Royalty-free"

    background_bed:
      name: "Subtle Technology"
      duration: "3:00"
      usage: "Background during narration"
      level: "-25 dB under voice"

    outro_theme:
      name: "Forward Momentum"
      duration: "0:10"
      usage: "Video outros"
      license: "Royalty-free"

  sources:
    - "Epidemic Sound (subscription)"
    - "Artlist (subscription)"
    - "YouTube Audio Library (free, check attribution)"
```

### Sound Effects

```yaml
sound_effects:
  transitions:
    whoosh: "Between major sections"
    click: "UI interactions in demos"
    chime: "Success indicators"

  usage_rules:
    volume: "-10 to -15 dB (audible but not jarring)"
    frequency: "Sparingly (every 2-3 minutes max)"
    duration: "0.5-2 seconds"
    consistency: "Use same sound for same action type"

  library:
    source: "Zapsplat.com (free) or local library"
    format: "WAV 48kHz/24-bit"
    organization: "By category (transition, UI, ambient)"
```

## Graphics Standards

### Icon Set

```markdown
## Azure Architecture Icons

### Usage
- **Source:** [Official Azure Architecture Icons](https://docs.microsoft.com/azure/architecture/icons/)
- **Format:** SVG preferred, PNG fallback
- **Size:** 64x64px or 128x128px
- **Color:** Use official Azure service colors

### Consistency Rules
1. Always use official Azure icons for Azure services
2. Maintain aspect ratio
3. Use consistent sizing within same diagram
4. Add shadow only if entire set has shadows
5. Background: Transparent or white circle

### Custom Icons
- **Style:** Flat design, 2D
- **Line weight:** 2-3px consistent
- **Color:** From brand palette
- **Size:** Match Azure icon dimensions
```

### Diagram Styles

```yaml
diagram_standards:
  layout:
    canvas: "1920x1080 or 1600x900"
    grid: "16px base unit"
    margins: "60px all sides"
    spacing: "32-48px between elements"

  components:
    containers:
      stroke: "2px solid #323130"
      fill: "rgba(237, 235, 233, 0.5)"
      corner_radius: "8px"
      padding: "24px"

    connectors:
      width: "2px"
      color: "#0078D4"
      style: "Solid (direct flow), Dashed (conditional)"
      arrows: "Directional for one-way, none for bidirectional"

    labels:
      font: "Segoe UI Regular, 14-16px"
      color: "#323130"
      background: "White with subtle border"
      position: "Above or beside, never overlapping"

  data_flow:
    color_coding:
      ingestion: "#107C10"  # Green
      processing: "#0078D4"  # Blue
      storage: "#FFB900"    # Yellow
      output: "#5E5BE5"     # Purple
```

## Templates & Assets

### Available Templates

```markdown
## Template Library

### Video Templates (After Effects)
- `csa_intro_slate.aep` - Standard intro slate
- `csa_outro_slate.aep` - Standard outro slate
- `csa_lower_third.aep` - Animated lower third
- `csa_title_card.aep` - Section title card

### Graphics Templates (Figma/Illustrator)
- `architecture_diagram.fig` - Architecture diagram template
- `infographic_template.ai` - Infographic layouts
- `social_media_cards.fig` - Social sharing graphics

### Presentation Templates (PowerPoint)
- `csa_deck_standard.pptx` - Standard presentation
- `csa_deck_technical.pptx` - Technical deep-dive
- `csa_deck_executive.pptx` - Executive summary

### Usage
1. Download from: `\\assets\templates\`
2. Do not modify master templates
3. Save your version with descriptive name
4. Follow guidelines within template comments
```

## Brand Voice & Tone

### Writing Style

```markdown
## Content Voice

### Characteristics
- **Professional:** Expert knowledge, credible
- **Approachable:** Friendly, not stuffy
- **Clear:** Jargon-free when possible, explain when necessary
- **Helpful:** Solution-oriented, practical

### Tone Guidelines

#### Technical Content
✅ DO:
- Use active voice
- Explain concepts clearly
- Provide context and examples
- Acknowledge complexity when appropriate

❌ DON'T:
- Use unnecessary jargon
- Assume advanced knowledge
- Skip steps or prerequisites
- Be condescending

#### Marketing Content
✅ DO:
- Focus on benefits
- Use compelling language
- Include social proof
- Clear calls-to-action

❌ DON'T:
- Overpromise
- Use empty buzzwords
- Be pushy or aggressive
```

### Terminology

```yaml
approved_terms:
  azure_services:
    - "Azure Synapse Analytics" (not just "Synapse")
    - "Azure Data Lake Storage" (spell out, then ADLS)
    - "Dedicated SQL pool" (not "SQL DW")
    - "Serverless SQL pool" (not "on-demand")

  general_terms:
    - "Cloud Scale Analytics" (full name first mention)
    - "CSA" (after full name established)
    - "Big data" (not "bigdata")
    - "Real-time" (hyphenated adjective)

  avoid:
    - "Awesome" (overused)
    - "Revolutionary" (hyperbolic)
    - "Cutting-edge" (cliché)
    - "World-class" (vague)
```

## Quality Standards

### Brand Compliance Checklist

```markdown
## Pre-Publishing Brand Check

### Visual Elements
- [ ] Uses approved color palette
- [ ] Typography follows guidelines
- [ ] Logo usage correct (size, placement, version)
- [ ] Templates used appropriately
- [ ] Graphics style consistent

### Audio Elements
- [ ] Approved music tracks used
- [ ] Sound effects from approved library
- [ ] Audio branding present (intro/outro)
- [ ] Volume levels consistent

### Content
- [ ] Voice and tone appropriate
- [ ] Approved terminology used
- [ ] No prohibited terms or phrases
- [ ] Clear, professional writing
- [ ] Factually accurate

### Technical
- [ ] File naming convention followed
- [ ] Metadata tags complete
- [ ] Proper attribution/credits
- [ ] Copyright notices included
- [ ] Accessibility standards met
```

## Related Resources

- [Graphics Production Guide](graphics-production.md)
- [Video Production Workflow](video-production-workflow.md)
- [Quality Assurance Guide](quality-assurance.md)
- [Templates Library](../templates/README.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
