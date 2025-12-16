# Animation Storyboard Templates

> **🏠 [Home](../../../../../README.md)** | **📖 [Documentation](../../../../README.md)** | **🎬 [Multimedia](../../../README.md)** | **🎨 [Animations](../../README.md)** | **Templates** | **Storyboards**

![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)
![Type: Templates](https://img.shields.io/badge/Type-Templates-blue)

## Overview

This directory contains templates and guidelines for creating animation storyboards for CSA-in-a-Box documentation and multimedia content.

## Available Templates

### 1. Standard Animation Storyboard

Use this template for general-purpose animations including:
- Data flow visualizations
- Process diagrams
- Architecture overviews
- Concept explanations

**Template Structure**:
```markdown
# [Animation Name] Storyboard

## Overview
- Purpose
- Duration
- Target audience
- Usage context

## Animation Sequence
- Frame-by-frame breakdown
- Timing details
- Visual elements
- Transitions

## Visual Style
- Color palette
- Typography
- Icon style
- Motion design

## Technical Specifications
- Resolution
- Frame rate
- File formats
- Performance targets

## Production Assets
- Required graphics
- Asset dimensions
- Export formats
```

### 2. Technical Process Animation

Specialized template for technical process animations:
- ETL pipelines
- CI/CD workflows
- Data processing flows
- System interactions

**Additional Sections**:
- State diagrams
- Code examples
- System architecture
- Error states

### 3. Interactive Animation

Template for animations with user interaction:
- Clickable diagrams
- Hover effects
- Progress indicators
- Tutorial walkthroughs

**Interactive Elements**:
- Trigger events
- State management
- User feedback
- Accessibility controls

## Storyboard Elements

### Frame Specification

Each frame should include:

```markdown
### Frame [Number]: [Title] ([Start Time] - [End Time])

**Visual Elements**:
- [Element 1]: Description
- [Element 2]: Description
- [Element 3]: Description

**Animation**:
- Start state
- End state
- Transition type
- Duration
- Easing function

**Key Frames**:
- [Time]: Description of state
- [Time]: Description of state
```

### Visual Style Guidelines

**Color Palette**:
```css
:root {
  --azure-blue: #0078D4;
  --azure-light-blue: #50E6FF;
  --success-green: #28a745;
  --warning-yellow: #ffc107;
  --error-red: #dc3545;
  --bg-dark: #1E1E1E;
  --bg-light: #FFFFFF;
  --text-primary: #323130;
  --text-secondary: #605E5C;
}
```

**Typography**:
- **Headings**: Segoe UI Bold
- **Body**: Segoe UI Regular
- **Code**: Consolas, Cascadia Code
- **Sizes**: 12px, 14px, 16px, 20px, 24px, 36px, 48px

**Motion Design**:
```css
/* Standard easing functions */
--ease-in: cubic-bezier(0.42, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.58, 1);
--ease-in-out: cubic-bezier(0.42, 0, 0.58, 1);

/* Standard durations */
--duration-quick: 150ms;
--duration-base: 300ms;
--duration-slow: 500ms;
--duration-slower: 800ms;
```

## Animation Principles

### 1. Clarity
- One idea per animation
- Clear visual hierarchy
- Obvious start and end states
- Purposeful motion

### 2. Performance
- Optimize for 60fps
- Use GPU-accelerated properties
- Minimize repaints/reflows
- Test on target devices

### 3. Accessibility
- Support reduced motion
- Provide text alternatives
- Ensure color contrast
- Include controls (play/pause)

### 4. Consistency
- Match brand guidelines
- Reuse motion patterns
- Maintain visual style
- Standardize timing

## Technical Specifications

### Output Formats

| Format | Use Case | Pros | Cons |
|--------|----------|------|------|
| **Lottie** | Web, mobile | Small size, scalable, interactive | Limited effects |
| **MP4** | Video embed | Universal support, high quality | Large file size |
| **GIF** | Email, legacy | Universal support | Limited colors, large size |
| **WebM** | Modern web | Small size, quality | Browser support |
| **SVG+CSS** | Simple animations | Crisp, editable | Limited complexity |

### Resolution Guidelines

| Target | Resolution | Frame Rate | Bitrate |
|--------|-----------|------------|---------|
| **Web (Desktop)** | 1920x1080 | 30fps | 5-8 Mbps |
| **Web (Mobile)** | 1280x720 | 30fps | 3-5 Mbps |
| **Social Media** | 1080x1080 | 30fps | 8-10 Mbps |
| **Email** | 800x600 | 15fps | 2-3 Mbps |
| **Docs (Hero)** | 1920x1080 | 30fps | 5-8 Mbps |

### File Size Targets

- **Lottie JSON**: < 500KB
- **MP4 (short)**: < 3MB
- **MP4 (long)**: < 10MB
- **GIF**: < 5MB
- **WebM**: < 2MB

## Production Workflow

### 1. Planning (25%)
- Define objectives
- Create storyboard
- Review with stakeholders
- Gather assets

### 2. Production (50%)
- Create assets
- Build animation
- Add interactions
- Test performance

### 3. Review (15%)
- Technical review
- Stakeholder approval
- Accessibility check
- Performance test

### 4. Delivery (10%)
- Export formats
- Optimize files
- Document usage
- Archive sources

## Tools & Software

### Design
- **Adobe Illustrator**: Vector graphics
- **Figma**: Design and prototyping
- **Sketch**: UI design

### Animation
- **Adobe After Effects**: Complex animations
- **LottieFiles**: Lottie creation/editing
- **Principle**: Interaction design

### Web
- **CSS animations**: Simple web animations
- **GSAP**: Advanced web animations
- **Anime.js**: Lightweight animation library

### Video
- **Adobe Premiere**: Video editing
- **Final Cut Pro**: Mac video editing
- **DaVinci Resolve**: Free alternative

## Example Storyboards

Refer to these examples for inspiration:
- [ETL Pipeline Animation](../../storyboards/etl-pipeline.md)
- [Stream Processing Animation](../../storyboards/stream-processing.md)
- [Architecture Foundation](../../../video-tutorials/storyboards/architecture/01-foundation.md)

## Best Practices

### DO ✅
- Plan thoroughly before production
- Use consistent motion patterns
- Optimize for performance
- Support accessibility
- Test on target devices
- Document technical specs
- Archive source files

### DON'T ❌
- Start without a storyboard
- Use random easing/timing
- Ignore performance impact
- Forget accessibility
- Assume all devices are fast
- Skip documentation
- Delete source files

## Resources

### Learning
- [Animation Principles (Disney)](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation)
- [Material Design Motion](https://material.io/design/motion)
- [LottieFiles Learn](https://lottiefiles.com/learn)

### Assets
- [Azure Icons](https://docs.microsoft.com/en-us/azure/architecture/icons/)
- [Noun Project](https://thenounproject.com/)
- [Flaticon](https://www.flaticon.com/)

### Tools
- [LottieFiles](https://lottiefiles.com/)
- [CodePen](https://codepen.io/) (for testing)
- [Can I Use](https://caniuse.com/) (browser support)

---

*Last Updated: January 2025*
