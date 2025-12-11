# Localization Guide

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **📎 [Production Guide](README.md)** | **🌐 Localization**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: Process](https://img.shields.io/badge/Type-Process-blue)

## Overview

Guidelines for localizing multimedia content into multiple languages and regions while maintaining quality, accuracy, and cultural appropriateness.

## Localization Workflow

### Language Priority

```yaml
supported_languages:
  tier_1:  # Full localization
    - en-US: "English (United States)"
    - es-ES: "Spanish (Spain)"
    - fr-FR: "French (France)"
    - de-DE: "German (Germany)"
    - ja-JP: "Japanese (Japan)"
    - zh-CN: "Chinese (Simplified)"

  tier_2:  # Subtitle localization only
    - pt-BR: "Portuguese (Brazil)"
    - it-IT: "Italian (Italy)"
    - ko-KR: "Korean (South Korea)"
    - nl-NL: "Dutch (Netherlands)"

  tier_3:  # On-demand
    - ar-SA: "Arabic (Saudi Arabia)"
    - hi-IN: "Hindi (India)"
    - ru-RU: "Russian (Russia)"
```

### Translation Process

```markdown
## Translation Workflow

### 1. Prepare Source Material
- [ ] Finalize English version
- [ ] Extract all text for translation
- [ ] Prepare translation glossary
- [ ] Identify cultural references needing adaptation

### 2. Translation
- [ ] Send to professional translator
- [ ] Provide context and reference materials
- [ ] Use translation memory for consistency
- [ ] Review technical term translations

### 3. Review & QA
- [ ] Native speaker review
- [ ] Technical accuracy check
- [ ] Cultural appropriateness review
- [ ] Test in-context (captions, UI, graphics)

### 4. Implementation
- [ ] Integrate translations
- [ ] Update metadata
- [ ] Test playback and display
- [ ] Verify character encoding

### 5. Publishing
- [ ] Deploy localized versions
- [ ] Update language selector
- [ ] Test region-specific access
- [ ] Monitor usage and feedback
```

## Caption Localization

### Subtitle Best Practices

```yaml
subtitle_guidelines:
  timing:
    minimum_duration: "1 second"
    maximum_duration: "7 seconds"
    reading_speed: "160-180 words per minute"
    gap_between: "0.1-0.3 seconds"

  formatting:
    max_lines: 2
    max_characters_per_line: 42
    line_break: "Natural phrase boundaries"
    positioning: "Bottom center (unless conflicts with on-screen text)"

  style:
    font: "Sans-serif (Arial, Helvetica)"
    size: "Proportional to video"
    color: "White with black outline or semi-transparent background"
    alignment: "Center"
```

### Multi-Language Caption Files

```vtt
WEBVTT - English

00:00:00.000 --> 00:00:03.500
Welcome to Cloud Scale Analytics.

00:00:03.500 --> 00:00:07.000
Today we'll explore Azure Synapse.
```

```vtt
WEBVTT - Spanish

00:00:00.000 --> 00:00:03.500
Bienvenido a Cloud Scale Analytics.

00:00:03.500 --> 00:00:07.000
Hoy exploraremos Azure Synapse.
```

## Voiceover Localization

### Recording Localized Audio

```markdown
## Localized Voiceover Process

### Voice Talent Selection
- **Native speakers** for target language
- **Professional experience** in technical content
- **Voice matching** to original tone and energy
- **Consistent talent** across video series

### Script Adaptation
- **Translate** while maintaining meaning
- **Adjust** for natural speech patterns in target language
- **Time sync** to match video length
- **Technical terms** - decide whether to translate or keep English

### Recording Specifications
- **Same audio standards** as English version
- **48kHz/24-bit** master files
- **-16 LUFS** loudness target
- **Separate tracks** for easy updates

### Implementation
- **Replace audio track** or provide as alternate
- **Update captions** to match new narration
- **Metadata** in target language
- **File naming:** `video-title_[language-code].mp4`
```

## Graphics Localization

### Text in Graphics

```yaml
graphics_localization:
  preparation:
    - "Design with localization in mind"
    - "Leave 30% extra space for text expansion"
    - "Use text layers, not rasterized text"
    - "Separate text from graphics when possible"

  translation:
    - "Translate all visible text"
    - "Maintain visual hierarchy"
    - "Adjust layout for different text lengths"
    - "Preserve brand colors and style"

  fonts:
    - "Ensure font supports target language characters"
    - "Use Unicode-compatible fonts"
    - "Test with actual translated text"
    - "Provide font files to translators if needed"

  cultural_adaptation:
    - "Review images for cultural appropriateness"
    - "Adapt examples to local context"
    - "Use region-appropriate icons and symbols"
    - "Adjust colors if cultural meanings differ"
```

## File Management

### Naming Conventions

```bash
# English (source)
azure-synapse-tutorial-2025-01.mp4
azure-synapse-tutorial-2025-01_en-US.vtt

# Spanish
azure-synapse-tutorial-2025-01_es-ES.mp4
azure-synapse-tutorial-2025-01_es-ES.vtt

# French
azure-synapse-tutorial-2025-01_fr-FR.mp4
azure-synapse-tutorial-2025-01_fr-FR.vtt

# Captions only (no voiceover localization)
azure-synapse-tutorial-2025-01.mp4  # Original English audio
azure-synapse-tutorial-2025-01_pt-BR.vtt  # Portuguese captions
```

### Metadata Localization

```json
{
  "video_id": "azure-synapse-tutorial-2025-01",
  "localizations": {
    "en-US": {
      "title": "Azure Synapse Analytics Tutorial",
      "description": "Learn how to create and configure Azure Synapse workspaces",
      "keywords": ["Azure", "Synapse", "Analytics", "Tutorial"],
      "captions": "azure-synapse-tutorial-2025-01_en-US.vtt"
    },
    "es-ES": {
      "title": "Tutorial de Azure Synapse Analytics",
      "description": "Aprende a crear y configurar espacios de trabajo de Azure Synapse",
      "keywords": ["Azure", "Synapse", "Análisis", "Tutorial"],
      "captions": "azure-synapse-tutorial-2025-01_es-ES.vtt",
      "audio": "azure-synapse-tutorial-2025-01_es-ES.mp4"
    }
  }
}
```

## Quality Assurance

### Localization QA Checklist

```markdown
## QA Checklist

### Translation Quality
- [ ] Accurate translation of all content
- [ ] Technical terms translated correctly
- [ ] Tone and style match original
- [ ] Grammar and spelling correct
- [ ] Natural-sounding in target language

### Technical Quality
- [ ] Caption sync accurate
- [ ] No character encoding issues
- [ ] Fonts display correctly
- [ ] Audio/video sync maintained
- [ ] File formats compatible

### Cultural Appropriateness
- [ ] No culturally inappropriate content
- [ ] Examples relevant to region
- [ ] Currency, dates, units localized
- [ ] Legal/regulatory compliance

### User Experience
- [ ] Language selector works
- [ ] Correct language displays
- [ ] Metadata in correct language
- [ ] Search/discovery functional
```

## Related Resources

- [Video Production Workflow](video-production-workflow.md)
- [Quality Assurance Guide](quality-assurance.md)
- [Accessibility Standards](accessibility-standards.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
