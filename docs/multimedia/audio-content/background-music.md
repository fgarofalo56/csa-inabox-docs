# 🎵 Background Music & Audio Assets

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎧 [Audio Content](README.md)** | **🎵 Background Music**

![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)
![Library Size: 100+ Tracks](https://img.shields.io/badge/Tracks-100+-blue)
![Licensed: Yes](https://img.shields.io/badge/Licensed-Yes-success)

## 📋 Overview

This document outlines the background music library, usage guidelines, and licensing requirements for Cloud Scale Analytics audio content. All music assets are properly licensed for commercial use.

## 🎼 Music Library Categories

### Brand Signature Music

```markdown
## Primary Brand Tracks

**CSA Main Theme** - "Cloud Ascent"
- **Duration**: 30 seconds (full), 15 seconds (short), 5 seconds (sting)
- **Tempo**: 120 BPM
- **Key**: C Major
- **Mood**: Uplifting, professional, tech-forward
- **Instruments**: Synth lead, piano, light drums, ambient pads
- **Usage**: Podcast intros/outros, video intros, brand moments
- **File**: `CSA-MainTheme-Full.wav`

**CSA Underscore** - "Data Flow"
- **Duration**: Variable (loopable 2-minute segments)
- **Tempo**: 90 BPM
- **Key**: A Minor
- **Mood**: Focused, ambient, non-distracting
- **Instruments**: Soft pads, subtle percussion, atmospheric
- **Usage**: Tutorial backgrounds, presentation underscoring
- **File**: `CSA-Underscore-DataFlow.wav`

**CSA Transition** - "Quick Shift"
- **Duration**: 3 seconds
- **Tempo**: Variable
- **Mood**: Smooth, professional
- **Usage**: Section transitions, topic changes
- **File**: `CSA-Transition-QuickShift.wav`
```

### Content Type Categories

#### Tutorial & Educational Content

```markdown
## Tutorial Music Collection

**Purpose**: Background music for instructional content
**Characteristics**:
- Low-profile, non-distracting
- Steady tempo (no dramatic changes)
- Minimal melodic complexity
- Long-form loopable segments

### Available Tracks

1. **"Focused Learning"**
   - Duration: 5 minutes (loopable)
   - Tempo: 85 BPM
   - Mood: Calm, focused
   - Volume recommendation: -32 dB under voice

2. **"Technical Clarity"**
   - Duration: 4 minutes (loopable)
   - Tempo: 95 BPM
   - Mood: Professional, clean
   - Volume recommendation: -30 dB under voice

3. **"Step by Step"**
   - Duration: 6 minutes (loopable)
   - Tempo: 80 BPM
   - Mood: Patient, methodical
   - Volume recommendation: -33 dB under voice
```

#### Podcast Content

```markdown
## Podcast Music Collection

**Purpose**: Intro, outro, and transition music for podcast episodes
**Characteristics**:
- Memorable, distinctive
- Energetic but professional
- Clear intro/outro points
- Brand recognition

### Available Tracks

1. **"Cloud Insights Theme"** (Primary)
   - Full: 30 seconds | Short: 15s | Sting: 5s
   - Tempo: 120 BPM
   - Energy: High
   - Usage: Standard podcast intro/outro

2. **"Tech Talk"** (Alternative)
   - Full: 25 seconds | Short: 12s
   - Tempo: 110 BPM
   - Energy: Medium-high
   - Usage: Interview episodes

3. **"Deep Dive"** (Specialized)
   - Full: 35 seconds | Short: 18s
   - Tempo: 95 BPM
   - Energy: Medium
   - Usage: Technical deep-dive episodes
```

#### Demo & Presentation Content

```markdown
## Presentation Music Collection

**Purpose**: Enhance demos, product showcases, presentations
**Characteristics**:
- Modern, tech-oriented
- Builds energy gradually
- Clear sections for content pacing
- Flexible usage

### Available Tracks

1. **"Product Showcase"**
   - Duration: 3 minutes
   - Sections: Intro (20s), Main (2:20), Outro (20s)
   - Tempo: 115 BPM
   - Energy: Building from medium to high

2. **"Feature Highlight"**
   - Duration: 2 minutes
   - Style: Upbeat, modern
   - Tempo: 125 BPM
   - Energy: Consistently high

3. **"Architecture Vision"**
   - Duration: 4 minutes
   - Style: Epic, expansive
   - Tempo: 85 BPM (building to 110 BPM)
   - Energy: Starts low, builds dramatically
```

## 📊 Music Usage Guidelines

### Volume Levels by Context

```markdown
## Recommended Volume Levels

### Music with Voice-Over
| Context | Music Level | Voice Level | Ratio |
|---------|-------------|-------------|-------|
| Tutorial narration | -32 dB | 0 dB (reference) | Barely audible |
| Podcast segments | -30 dB | 0 dB | Subtle presence |
| Dramatic moments | -25 dB | 0 dB | Noticeable support |
| Underscore emphasis | -20 dB | 0 dB | Strong presence |

### Music Without Voice
| Context | Music Level | Purpose |
|---------|-------------|---------|
| Intro/outro | -3 dB | Full presence |
| Transitions | -8 dB | Clear but brief |
| Background ambience | -15 dB | Subtle atmosphere |
| Hold music | -10 dB | Comfortable listening |
```

### Fade Techniques

```markdown
## Professional Fade Standards

**Standard Fade-In**:
- Duration: 2 seconds
- Curve: Logarithmic (gradual start, quick finish)
- Usage: Music beginning

**Standard Fade-Out**:
- Duration: 2-3 seconds
- Curve: Logarithmic
- Usage: Music ending

**Duck for Voice (Fade Down)**:
- Duration: 1-1.5 seconds
- Target: -30 dB to -35 dB below voice
- Curve: Quick exponential
- Usage: When voice begins over music

**Unduck (Fade Up)**:
- Duration: 1-2 seconds
- Return to: Original level or fade out
- Curve: Gradual exponential
- Usage: When voice ends

**Cross-Fade**:
- Duration: 3-5 seconds
- Overlap: 50% typical
- Curve: Equal power
- Usage: Transitioning between music tracks
```

## 🎚️ Audio Mixing Best Practices

### Layering Music & Voice

```markdown
## Multi-Layer Audio Setup

**Layer 1 - Voice** (Primary):
- Peak: -6 dBFS
- Average: -16 to -12 dBFS
- Processing: EQ, compression, de-essing
- Priority: Always most prominent

**Layer 2 - Music** (Support):
- Peak: -30 to -35 dB relative to voice
- Processing: EQ (cut frequencies competing with voice)
- Ducking: Automated or manual volume reduction
- Priority: Never competes with voice

**Layer 3 - Sound Effects** (Accent):
- Peak: -15 to -20 dB relative to voice
- Processing: Minimal, preserve character
- Usage: Brief, purposeful
- Priority: Complements but doesn't distract
```

### EQ Guidelines for Music Under Voice

```markdown
## Frequency Management

**Cut These Frequencies**:
- 200-400 Hz: Reduce to avoid muddiness with voice
- 1-3 kHz: Cut to prevent competition with voice clarity
- 4-6 kHz: Reduce to avoid masking voice presence

**Preserve These Frequencies**:
- Below 100 Hz: Keep low-end warmth (if not competing)
- Above 8 kHz: Maintain air and sparkle
- Mid-bass: Can support without competing (100-200 Hz)

**Practical EQ Settings**:
- High-pass filter: 80 Hz (remove subsonic)
- Mid-cut: -3 to -6 dB at 1-3 kHz (voice clarity region)
- Presence cut: -2 to -4 dB at 4-6 kHz (reduce mask)
- Air boost: +1 to +2 dB at 10+ kHz (optional sparkle)
```

## 📜 Licensing & Attribution

### Music Sources

```markdown
## Licensed Music Libraries

**Primary Source**: Epidemic Sound
- **License Type**: Commercial, broadcast, podcast
- **Coverage**: All Cloud Scale Analytics audio content
- **Attribution**: Not required, but good practice
- **Renewal**: Annual subscription
- **Account**: team@cloudscaleanalytics.com

**Secondary Source**: Artlist
- **License Type**: Perpetual commercial license
- **Coverage**: Video and multimedia productions
- **Attribution**: Not required
- **Renewal**: Annual subscription
- **Account**: production@cloudscaleanalytics.com

**Free Music Archive** (Limited Use):
- **License Type**: Various Creative Commons
- **Coverage**: Non-commercial, limited projects
- **Attribution**: REQUIRED (see specific license)
- **Restriction**: Check each track's license
- **Usage**: Internal training only
```

### Attribution Requirements

```markdown
## When Attribution is Required

**Creative Commons Music**:
```
Music: "Track Name" by Artist Name
License: CC BY 3.0
Source: Free Music Archive
URL: [Link to track]
```

**Custom Commissioned Music**:
```
Original Music: "Track Name"
Composer: Composer Name
Commissioned for Cloud Scale Analytics
© 2025 Cloud Scale Analytics
```

**Licensed Library Music** (Optional):
```
Music licensed from [Epidemic Sound/Artlist]
```
```

### License Restrictions

```markdown
## Usage Rights & Restrictions

**Allowed Uses**:
✅ Podcast episodes (public distribution)
✅ YouTube and video tutorials
✅ Internal training materials
✅ Promotional videos
✅ Conference presentations
✅ Webinars and live events
✅ Social media content

**Restricted Uses**:
❌ Reselling music separately
❌ Using in other company's content
❌ Distributing music files standalone
❌ Sublicensing to third parties
❌ Using after license expiration (Epidemic Sound)

**Special Considerations**:
- ⚠️ Check license for live streaming (usually allowed)
- ⚠️ Some tracks may have regional restrictions
- ⚠️ Update music library annually to stay within license
```

## 🎯 Music Selection Guide

### Matching Music to Content

```markdown
## Content-Mood Mapping

**Technical Tutorials**:
- Mood: Focused, professional, calm
- Energy: Low to medium (3-5/10)
- Tempo: Slow to moderate (70-90 BPM)
- Example tracks: "Focused Learning," "Technical Clarity"

**Product Demos**:
- Mood: Exciting, modern, confident
- Energy: Medium to high (6-8/10)
- Tempo: Moderate to fast (110-130 BPM)
- Example tracks: "Product Showcase," "Feature Highlight"

**Podcast Interviews**:
- Mood: Engaging, conversational, professional
- Energy: Medium (5-7/10)
- Tempo: Moderate (100-120 BPM)
- Example tracks: "Cloud Insights Theme," "Tech Talk"

**Architecture Discussions**:
- Mood: Thoughtful, expansive, visionary
- Energy: Medium, building (5-7/10, builds to 8/10)
- Tempo: Slow building (80-110 BPM)
- Example tracks: "Architecture Vision," "Deep Dive"

**Quick Tips / Short Form**:
- Mood: Upbeat, accessible, friendly
- Energy: High (7-9/10)
- Tempo: Fast (120-140 BPM)
- Example tracks: Brief stingers, upbeat loops
```

### Duration Considerations

```markdown
## Matching Music Length to Content

**Short Content** (Under 2 minutes):
- Use: Short form tracks or stingers
- Strategy: Single music piece, fade in/out
- Avoid: Multiple music changes (feels choppy)

**Medium Content** (2-10 minutes):
- Use: Loopable tracks or full pieces
- Strategy: Intro music, optional background, outro
- Transitions: Minimal, smooth

**Long Content** (10+ minutes):
- Use: Multiple loopable segments
- Strategy: Vary music slightly for different sections
- Transitions: Cross-fade between similar styles
- Avoid: Exact loop repetition (noticeable)
```

## 🛠️ Implementation Workflow

### Adding Music to Productions

```markdown
## Step-by-Step Workflow

### 1. Pre-Production Planning
- [ ] Identify content type and target mood
- [ ] Review music library for appropriate tracks
- [ ] Test music with voice-over sample
- [ ] Confirm licensing covers usage type

### 2. Music Integration
- [ ] Import music into editing software
- [ ] Place on separate audio track (below voice)
- [ ] Set initial volume level (-30 to -35 dB)
- [ ] Add fade in/out (2-3 seconds)

### 3. Mixing & Balancing
- [ ] Apply EQ to music (cut 1-3 kHz region)
- [ ] Set up ducking automation or sidechain
- [ ] Test balance (music should not mask voice)
- [ ] Adjust music volume based on voice energy

### 4. Quality Check
- [ ] Listen on multiple devices (headphones, speakers)
- [ ] Verify music doesn't distract from content
- [ ] Check for clipping or distortion
- [ ] Ensure smooth transitions

### 5. Final Delivery
- [ ] Export with proper levels (-16 LUFS for podcasts)
- [ ] Include music credits if required
- [ ] Archive project with music files referenced
- [ ] Document music choices for consistency
```

## 📚 Music Library Access

```markdown
## Accessing Music Files

**Internal Team Access**:
- Location: SharePoint > Content Production > Audio Assets > Music Library
- Organization: By category, tempo, and mood
- Previews: Available for all tracks
- Metadata: Includes BPM, key, duration, mood tags

**File Naming Convention**:
```
[Category]-[TrackName]-[Duration]-[BPM].wav

Examples:
Brand-CloudAscent-30sec-120BPM.wav
Tutorial-FocusedLearning-5min-85BPM.wav
Transition-QuickShift-3sec-VAR.wav
```

**Download & Usage**:
1. Browse by category or search by mood/tempo
2. Preview track before downloading
3. Download WAV (production) or MP3 (preview)
4. Import into project
5. Log usage in production notes (for tracking)
```

## 🔗 Related Resources

- [Sound Effects Library](./sound-effects.md)
- [Audio Editing Guidelines](./editing-guidelines.md)
- [Production Standards](../production-guide/README.md)
- [Audio Branding Guide](./audio-branding.md)

## 💬 Support & Requests

**Music Library Questions**: audio-library@cloudscaleanalytics.com
**License Issues**: licensing@cloudscaleanalytics.com
**Custom Music Requests**: music-production@cloudscaleanalytics.com

---

*Last Updated: January 2025 | Version: 1.0.0*
