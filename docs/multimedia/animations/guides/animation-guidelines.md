# Animation Guidelines for CSA-in-a-Box

> **🏠 [Home](../../../../README.md)** | **📖 [Documentation](../../../README.md)** | **🎬 [Multimedia](../../README.md)** | **🎨 [Animations](../README.md)** | **📋 Guidelines**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: Guidelines](https://img.shields.io/badge/Type-Guidelines-blue)
![Audience: Designers & Developers](https://img.shields.io/badge/Audience-Designers%20%26%20Developers-purple)

## Overview

This guide establishes comprehensive animation standards for the Cloud Scale Analytics (CSA) in-a-Box documentation platform. These guidelines ensure animations are consistent, accessible, performant, and enhance the learning experience for data engineers, architects, and analysts working with Azure analytics services.

## Table of Contents

- [Animation Principles](#animation-principles)
- [Duration Standards](#duration-standards)
- [Easing Functions](#easing-functions)
- [Motion Patterns](#motion-patterns)
- [Animation Types](#animation-types)
- [Azure Brand Alignment](#azure-brand-alignment)
- [Browser Compatibility](#browser-compatibility)
- [Testing Requirements](#testing-requirements)

## Animation Principles

### Core Principles for Data Analytics Context

**1. Purposeful Motion**
- Every animation must serve a clear purpose (explain, guide, engage)
- Avoid decorative animations that don't add value
- Focus on clarifying complex data flows and architecture patterns

**2. Hierarchy and Focus**
- Use motion to direct attention to key elements
- Animate primary content before secondary details
- Ensure data flow direction is clear and logical

**3. Consistency**
- Maintain uniform timing and easing across similar animations
- Use consistent motion patterns for recurring elements (data packets, service connections)
- Apply Azure design system principles

**4. Performance First**
- Target 60fps on modern devices, minimum 30fps on older hardware
- Keep file sizes optimized for global audiences
- Provide static alternatives for low-bandwidth scenarios

## Duration Standards

### Recommended Timing by Animation Type

| Animation Type | Duration | Use Case | Example |
|:--------------|:---------|:---------|:--------|
| **Micro-interactions** | 100-200ms | Button hover, toggle states | Service health indicator change |
| **UI Feedback** | 200-300ms | Form validation, status updates | Pipeline execution status |
| **Element Transitions** | 300-400ms | Card flips, panel expansions | Metric card expansion |
| **Data Visualizations** | 400-800ms | Chart animations, graph updates | Real-time analytics dashboard |
| **Process Flows** | 800-1500ms | Multi-step workflows | ETL pipeline visualization |
| **Architecture Diagrams** | 1500-3000ms | Complex system animations | Azure service mesh animation |
| **Tutorial Sequences** | 3000-10000ms | Step-by-step demonstrations | Synapse workspace setup |

### Duration Guidelines by Element Size

```css
/* Small UI elements (icons, badges) */
.small-element {
  transition-duration: 150ms;
}

/* Medium elements (cards, panels) */
.medium-element {
  transition-duration: 300ms;
}

/* Large elements (modals, full sections) */
.large-element {
  transition-duration: 450ms;
}

/* Complex animations (multi-stage) */
.complex-animation {
  animation-duration: 600ms;
}
```

## Easing Functions

### Standard Easing Patterns

**Ease-Out (Deceleration)**
- **Use for**: Elements entering the viewport, expanding panels
- **Purpose**: Creates natural, smooth entry
- **Azure Context**: Data flowing into storage, services initializing

```css
.entering-element {
  transition-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
  /* Material Design's "Decelerate" curve */
}
```

**Ease-In (Acceleration)**
- **Use for**: Elements leaving the viewport, closing dialogs
- **Purpose**: Quick, clean exits
- **Azure Context**: Data egress, service shutdown

```css
.exiting-element {
  transition-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
  /* Material Design's "Accelerate" curve */
}
```

**Ease-In-Out (Acceleration then Deceleration)**
- **Use for**: Elements moving within the viewport, state transitions
- **Purpose**: Balanced, smooth motion
- **Azure Context**: Data transformation, state changes

```css
.moving-element {
  transition-timing-function: cubic-bezier(0.4, 0.0, 0.2, 1);
  /* Material Design's "Standard" curve */
}
```

**Linear**
- **Use for**: Continuous processes, loading indicators
- **Purpose**: Constant speed for predictable motion
- **Azure Context**: Data streaming, continuous queries

```css
.continuous-process {
  transition-timing-function: linear;
}
```

### Custom Easing for Data Flows

```css
/* Azure data flow easing - gentle wave pattern */
@keyframes data-flow-wave {
  0% { transform: translateX(0) translateY(0); }
  25% { transform: translateX(25%) translateY(-5px); }
  50% { transform: translateX(50%) translateY(0); }
  75% { transform: translateX(75%) translateY(5px); }
  100% { transform: translateX(100%) translateY(0); }
}

.data-packet {
  animation: data-flow-wave 2s cubic-bezier(0.42, 0, 0.58, 1) infinite;
}
```

## Motion Patterns

### Data Flow Animations

**Streaming Data Pattern**
```css
/* Continuous data stream visualization */
.data-stream {
  position: relative;
  overflow: hidden;
}

.data-stream::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg,
    transparent 0%,
    #0078D4 50%,
    transparent 100%
  );
  animation: stream-flow 2s linear infinite;
}

@keyframes stream-flow {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
```

**Batch Processing Pattern**
```css
/* Discrete batch processing visualization */
.batch-process {
  animation: batch-pulse 3s ease-in-out infinite;
}

@keyframes batch-pulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
}
```

### Service Interaction Patterns

**Service-to-Service Communication**
```css
.service-connection {
  stroke-dasharray: 10 5;
  animation: service-pulse 1.5s linear infinite;
}

@keyframes service-pulse {
  0% { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: 15; }
}
```

**Load Balancing Visualization**
```css
.load-distribution {
  animation: distribute-load 2s ease-in-out infinite;
}

@keyframes distribute-load {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}
```

## Animation Types

### Entrance Animations

**Fade In and Scale**
```css
.fade-in-scale {
  animation: fadeInScale 400ms cubic-bezier(0.0, 0.0, 0.2, 1) forwards;
  opacity: 0;
}

@keyframes fadeInScale {
  0% {
    opacity: 0;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
```

**Slide In from Direction**
```css
.slide-in-right {
  animation: slideInRight 500ms cubic-bezier(0.0, 0.0, 0.2, 1) forwards;
}

@keyframes slideInRight {
  0% {
    opacity: 0;
    transform: translateX(30px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}
```

### Loading Animations

**Azure Service Loading Indicator**
```css
.azure-loader {
  display: inline-block;
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 120, 212, 0.1);
  border-left-color: #0078D4;
  border-radius: 50%;
  animation: azure-spin 1s linear infinite;
}

@keyframes azure-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

**Data Processing Progress**
```css
.processing-bar {
  width: 0%;
  height: 4px;
  background: linear-gradient(90deg, #0078D4, #00BCF2);
  animation: processing-progress 3s ease-in-out forwards;
}

@keyframes processing-progress {
  0% { width: 0%; }
  100% { width: 100%; }
}
```

## Azure Brand Alignment

### Color Animation Standards

**Primary Azure Blue**
- Use `#0078D4` for primary animations
- Use `#00BCF2` for secondary/complementary elements
- Maintain WCAG 2.1 AA contrast ratios during animations

**Color Transitions**
```css
/* Good - smooth color transition */
.service-status {
  transition: background-color 300ms ease-in-out;
}

.service-status.healthy { background-color: #107C10; } /* Success green */
.service-status.warning { background-color: #FFB900; } /* Warning amber */
.service-status.error { background-color: #D13438; } /* Error red */
```

### Typography Animation

```css
/* Animated typography for data metrics */
.metric-value {
  font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
  font-variant-numeric: tabular-nums;
  animation: metric-update 500ms ease-out;
}

@keyframes metric-update {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); color: #0078D4; }
}
```

## Browser Compatibility

### Supported Browsers

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- iOS Safari 14+
- Chrome Mobile 90+

### Fallback Strategy

```css
/* Progressive enhancement approach */
@supports (animation: name) {
  .enhanced-element {
    animation: complex-animation 1s ease-in-out;
  }
}

/* Fallback for older browsers */
.enhanced-element {
  /* Static or simplified alternative */
  transform: translateX(0);
}
```

### Vendor Prefixes

```css
/* Use autoprefixer in build process */
/* Manual prefixing when necessary */
.prefixed-animation {
  -webkit-animation: slide 1s ease;
  -moz-animation: slide 1s ease;
  animation: slide 1s ease;
}
```

## Testing Requirements

### Performance Testing

**Frame Rate Monitoring**
```javascript
// Monitor animation performance
class AnimationFPSMonitor {
  constructor() {
    this.fps = 0;
    this.frames = 0;
    this.lastTime = performance.now();
  }

  measure() {
    this.frames++;
    const currentTime = performance.now();

    if (currentTime >= this.lastTime + 1000) {
      this.fps = Math.round((this.frames * 1000) / (currentTime - this.lastTime));
      console.log(`Animation FPS: ${this.fps}`);

      if (this.fps < 30) {
        console.warn('Low FPS detected - consider optimization');
      }

      this.frames = 0;
      this.lastTime = currentTime;
    }
  }
}
```

### Cross-Browser Testing

**Test Checklist**
- [ ] Chrome (Windows, macOS, Linux)
- [ ] Firefox (Windows, macOS)
- [ ] Safari (macOS, iOS)
- [ ] Edge (Windows)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)
- [ ] Reduced motion preferences respected
- [ ] Touch device interactions work correctly

### Accessibility Testing

**Reduced Motion Testing**
```javascript
// Test reduced motion implementation
const testReducedMotion = () => {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  if (prefersReducedMotion.matches) {
    console.log('✓ Reduced motion alternative active');
  } else {
    console.log('✓ Full animation active');
  }

  // Listen for changes
  prefersReducedMotion.addEventListener('change', (e) => {
    console.log(`Motion preference changed: ${e.matches ? 'reduced' : 'full'}`);
  });
};
```

## Best Practices Summary

**DO:**
- Use transform and opacity for performant animations
- Provide reduced motion alternatives
- Test on low-end devices and slow connections
- Use meaningful animation that clarifies content
- Follow Azure design system guidelines
- Optimize file sizes for web delivery

**DON'T:**
- Animate layout properties (width, height, margin, padding)
- Create animations that distract from content
- Ignore accessibility requirements
- Use excessive simultaneous animations (max 3-5)
- Rely solely on animation to convey critical information
- Forget to test on mobile devices

## Related Resources

- [Accessibility Guidelines](accessibility.md)
- [Performance Optimization](performance.md)
- [Export Settings](export-settings.md)
- [Azure Design System](https://aka.ms/azure-design)
- [WCAG 2.1 Animation Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html)

---

*Last Updated: January 2025 | Version: 1.0.0*
