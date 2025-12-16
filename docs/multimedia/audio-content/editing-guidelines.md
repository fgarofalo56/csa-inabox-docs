# ✂️ Audio Editing Guidelines

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎧 [Audio Content](README.md)** | **✂️ Editing Guidelines**

![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)
![Type: Technical Guide](https://img.shields.io/badge/Type-Technical-blue)

## 📋 Overview

Comprehensive guidelines for editing audio content to professional broadcast standards while maintaining natural, conversational quality.

## 🎯 Editing Philosophy

### Balance Between Polish and Authenticity

- **Remove**: Distracting errors, technical issues, excessive pauses
- **Keep**: Natural speech patterns, personality, authentic moments
- **Goal**: Clean, professional audio that sounds natural

## ✂️ Basic Editing Workflow

### 1. Organization & Import (15-30 min)

- Import all audio files
- Name tracks clearly (Host, Guest, Music, SFX)
- Create backup of original files
- Set project sample rate to 48kHz, 24-bit

### 2. Rough Edit (1-2 hours per hour of audio)

- Remove long pauses (over 3 seconds)
- Cut false starts and retakes
- Remove "ums," "uhs," and filler words (excessive only)
- Arrange segments in proper order
- Mark sections needing attention

### 3. Fine Edit (1-2 hours)

- Smooth transitions between cuts
- Adjust timing for natural flow
- Remove mouth clicks and breaths (excessive only)
- Add music and sound effects
- Create final structure

### 4. Audio Processing (30-60 min)

- Apply noise reduction
- EQ for clarity
- Compress for consistency
- De-ess harsh sibilance
- Limit to prevent peaks

### 5. Final Mix (30-60 min)

- Balance levels between speakers
- Adjust music volume
- Master to -16 LUFS (podcasts)
- Final listen-through
- Export in required formats

## 🎚️ Audio Processing Chain

### Standard Processing Order

```markdown
1. Noise Reduction (subtle, -10 to -15 dB reduction)
2. EQ (high-pass 80Hz, presence boost 2-4 kHz)
3. De-esser (4-8 kHz range, threshold -20 to -15 dB)
4. Compression (3:1 ratio, -18 dB threshold, 3ms attack, 50ms release)
5. Limiting (-3 dB ceiling for headroom)
```

### Level Standards

- **Peak Level**: -3 dBFS (leaves headroom)
- **Average Level**: -16 LUFS (podcasts), -18 LUFS (broadcast)
- **Noise Floor**: Below -60 dBFS
- **Music Under Voice**: -30 to -35 dB below voice

## 🔧 Common Editing Techniques

### Removing Breaths

- Remove only loud, distracting breaths
- Keep natural breathing rhythm
- Use automation to lower breath volume vs. removing entirely

### Cutting Filler Words

- "Um," "uh," "you know," "like" - remove when excessive
- Keep some for natural speech
- Don't create unnatural gaps

### Smoothing Edits

- Use 10-20ms crossfades at all edit points
- Align edits at zero-crossings to avoid clicks
- Maintain natural rhythm

### Speed Adjustments

- Use time-stretching to tighten slow sections (max 5-10%)
- Maintain pitch (algorithmic time-stretching)
- Sounds unnatural if pushed too far

## 🎵 Music & SFX Integration

### Adding Background Music

- Intro: Full volume, fade to -30dB when voice begins
- During speech: -30 to -35 dB below voice
- Transitions: Brief swell to -15dB between segments
- Outro: Fade up to full volume as voice ends

### Sound Effects

- Volume: -15 to -20 dB relative to voice
- Timing: Sync with visual/topic cues
- Transitions: Use for section changes
- Don't overuse - less is more

## ✅ Quality Checklist

### Before Export

- [ ] No clipping (peaks below -3 dBFS)
- [ ] Consistent levels throughout
- [ ] No background noise artifacts
- [ ] Smooth edits (no clicks or pops)
- [ ] Music balanced properly
- [ ] Final loudness: -16 LUFS (podcast)
- [ ] Listened on multiple playback systems
- [ ] Transcript prepared
- [ ] Metadata complete

## 🔗 Related Resources

- [Recording Setup](./recording-setup.md)
- [Narration Guidelines](./narration-guidelines.md)
- [Audio Transcripts](./audio-transcripts.md)

---

*Last Updated: January 2025*
