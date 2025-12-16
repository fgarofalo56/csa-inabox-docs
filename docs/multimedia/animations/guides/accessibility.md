# Animation Accessibility Guidelines

> **🏠 [Home](../../../../README.md)** | **📖 [Documentation](../../../README.md)** | **🎬 [Multimedia](../../README.md)** | **🎨 [Animations](../README.md)** | **♿ Accessibility**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: Accessibility](https://img.shields.io/badge/Type-Accessibility-blue)
![WCAG: 2.1 AA](https://img.shields.io/badge/WCAG-2.1%20AA-success)

## Overview

Animation accessibility ensures that all users, regardless of their abilities or preferences, can effectively engage with CSA-in-a-Box documentation. This guide covers motion sensitivity, cognitive accessibility, screen reader compatibility, and inclusive design practices for data analytics visualizations.

## Table of Contents

- [WCAG Compliance](#wcag-compliance)
- [Reduced Motion Support](#reduced-motion-support)
- [Cognitive Accessibility](#cognitive-accessibility)
- [Screen Reader Support](#screen-reader-support)
- [Keyboard Navigation](#keyboard-navigation)
- [Visual Accessibility](#visual-accessibility)
- [Testing Procedures](#testing-procedures)

## WCAG Compliance

### Relevant WCAG 2.1 Success Criteria

**Level A Requirements**

**2.2.2 Pause, Stop, Hide (Level A)**
- Provide controls to pause, stop, or hide animations that auto-start
- Essential for carousel animations and auto-playing data visualizations

```html
<!-- Animation with user controls -->
<div class="animation-container">
  <div class="animation-player" id="data-flow-animation">
    <!-- Animation content -->
  </div>

  <div class="animation-controls" role="group" aria-label="Animation controls">
    <button id="play-pause" aria-label="Play or pause animation">
      <span class="play-icon" aria-hidden="true">▶</span>
      <span class="pause-icon hidden" aria-hidden="true">⏸</span>
    </button>
    <button id="stop" aria-label="Stop animation">
      <span aria-hidden="true">⏹</span>
    </button>
    <button id="restart" aria-label="Restart animation">
      <span aria-hidden="true">⟲</span>
    </button>
  </div>
</div>
```

**Level AA Requirements**

**2.3.1 Three Flashes or Below Threshold (Level A)**
- No content flashes more than 3 times per second
- Critical for data streaming visualizations

**2.3.3 Animation from Interactions (Level AAA, recommended)**
- Disable motion animations triggered by user interaction when requested
- Implement system-wide reduced motion preferences

### Implementation Standards

```css
/* Compliance with WCAG 2.3.1 - No rapid flashing */
@keyframes safe-pulse {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 1.0; }
}

.status-indicator {
  /* Pulse duration > 333ms to stay under 3 flashes/second */
  animation: safe-pulse 1s ease-in-out infinite;
}
```

## Reduced Motion Support

### Media Query Implementation

**Standard Reduced Motion Query**
```css
/* Default: Full animations */
.animated-element {
  transition: transform 400ms ease-out, opacity 400ms ease-out;
}

.animated-element.active {
  transform: translateY(0) scale(1);
  opacity: 1;
}

/* Reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  .animated-element {
    /* Reduce to essential transitions only */
    transition: opacity 50ms linear;
  }

  .animated-element.active {
    /* Remove transform animations */
    transform: none;
    opacity: 1;
  }

  /* Disable all complex animations */
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### JavaScript Detection

```javascript
// Detect and respond to motion preferences
class MotionPreferenceManager {
  constructor() {
    this.mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    this.prefersReducedMotion = this.mediaQuery.matches;
    this.init();
  }

  init() {
    // Initial check
    this.updateMotionPreference();

    // Listen for changes
    this.mediaQuery.addEventListener('change', () => {
      this.updateMotionPreference();
    });
  }

  updateMotionPreference() {
    this.prefersReducedMotion = this.mediaQuery.matches;

    if (this.prefersReducedMotion) {
      document.documentElement.classList.add('reduce-motion');
      this.disableComplexAnimations();
    } else {
      document.documentElement.classList.remove('reduce-motion');
      this.enableComplexAnimations();
    }

    // Dispatch custom event for components to listen to
    window.dispatchEvent(new CustomEvent('motionPreferenceChanged', {
      detail: { reducedMotion: this.prefersReducedMotion }
    }));
  }

  disableComplexAnimations() {
    // Pause all Lottie animations
    document.querySelectorAll('.lottie-animation').forEach(el => {
      if (el.lottieInstance) {
        el.lottieInstance.pause();
        el.lottieInstance.goToAndStop(0, true);
      }
    });

    // Show static alternatives
    document.querySelectorAll('[data-static-alternative]').forEach(el => {
      const staticSrc = el.dataset.staticAlternative;
      if (staticSrc) {
        el.src = staticSrc;
      }
    });
  }

  enableComplexAnimations() {
    // Resume animations
    document.querySelectorAll('.lottie-animation').forEach(el => {
      if (el.lottieInstance && el.dataset.autoplay === 'true') {
        el.lottieInstance.play();
      }
    });
  }

  shouldAnimate(animationType = 'standard') {
    if (this.prefersReducedMotion) {
      // Only allow essential animations even with reduced motion
      return animationType === 'essential';
    }
    return true;
  }
}

// Initialize globally
const motionManager = new MotionPreferenceManager();
```

### Static Alternatives

**Provide Non-Animated Equivalents**
```html
<!-- Animation with static fallback -->
<picture>
  <source
    srcset="/images/architecture-animation.mp4"
    type="video/mp4"
    media="(prefers-reduced-motion: no-preference)"
  >
  <img
    src="/images/architecture-static.svg"
    alt="Azure Synapse architecture diagram showing data flow from Event Hub through Stream Analytics to Data Lake and Power BI"
  >
</picture>
```

## Cognitive Accessibility

### Simplification Strategies

**Reduce Complexity for Cognitive Load**
```javascript
class CognitiveAccessibilityManager {
  constructor() {
    this.simplifiedMode = false;
    this.userPreferences = this.loadPreferences();
  }

  enableSimplifiedMode() {
    this.simplifiedMode = true;

    // Reduce animation speed
    document.documentElement.style.setProperty('--animation-speed-multiplier', '0.5');

    // Show fewer simultaneous animations
    this.limitSimultaneousAnimations(2);

    // Increase pause durations
    document.documentElement.style.setProperty('--pause-duration', '2s');

    // Add visual indicators for transitions
    this.addTransitionIndicators();
  }

  limitSimultaneousAnimations(maxCount) {
    const animationQueue = [];
    let activeCount = 0;

    const processQueue = () => {
      while (activeCount < maxCount && animationQueue.length > 0) {
        const animation = animationQueue.shift();
        activeCount++;
        animation.play().then(() => {
          activeCount--;
          processQueue();
        });
      }
    };

    // Override animation play method
    window.queueAnimation = (animation) => {
      animationQueue.push(animation);
      processQueue();
    };
  }

  addTransitionIndicators() {
    // Add visual cues before major transitions
    document.querySelectorAll('[data-major-transition]').forEach(el => {
      const indicator = document.createElement('div');
      indicator.className = 'transition-indicator';
      indicator.textContent = 'Scene changing...';
      indicator.setAttribute('role', 'status');
      indicator.setAttribute('aria-live', 'polite');
      el.prepend(indicator);
    });
  }
}
```

### User Control Options

```html
<!-- Accessibility control panel -->
<div class="accessibility-controls" role="region" aria-label="Animation accessibility settings">
  <h3>Animation Settings</h3>

  <div class="control-group">
    <input
      type="checkbox"
      id="reduce-motion-toggle"
      name="reduce-motion"
      aria-describedby="reduce-motion-desc"
    >
    <label for="reduce-motion-toggle">Reduce motion</label>
    <p id="reduce-motion-desc" class="description">
      Minimizes animations and transitions
    </p>
  </div>

  <div class="control-group">
    <label for="animation-speed">Animation speed</label>
    <input
      type="range"
      id="animation-speed"
      name="animation-speed"
      min="0.5"
      max="2"
      step="0.1"
      value="1"
      aria-valuetext="Normal speed"
    >
    <output for="animation-speed">1x</output>
  </div>

  <div class="control-group">
    <input
      type="checkbox"
      id="pause-on-hover"
      name="pause-on-hover"
    >
    <label for="pause-on-hover">Pause animations on hover</label>
  </div>

  <div class="control-group">
    <input
      type="checkbox"
      id="show-descriptions"
      name="show-descriptions"
      checked
    >
    <label for="show-descriptions">Show text descriptions</label>
  </div>
</div>
```

## Screen Reader Support

### ARIA Labels for Animations

```html
<!-- Animated data visualization with screen reader support -->
<div
  class="data-visualization"
  role="img"
  aria-label="Real-time data flow showing 1,000 events per second streaming from IoT devices through Event Hub to Stream Analytics"
  aria-describedby="viz-description"
>
  <!-- Animation content -->
  <svg class="animated-diagram">
    <!-- SVG animation elements -->
  </svg>

  <!-- Hidden description for screen readers -->
  <div id="viz-description" class="sr-only">
    This animation demonstrates a real-time data pipeline. Events are generated
    by IoT devices at a rate of 1,000 per second. They flow into Azure Event Hub,
    which partitions and buffers the data. Stream Analytics then processes the
    events using windowing functions, aggregating them every 5 seconds. Finally,
    processed results are sent to Azure Data Lake for storage and Power BI for
    real-time visualization.
  </div>
</div>

<!-- CSS for screen reader only content -->
<style>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>
```

### Live Regions for Animation Updates

```html
<!-- Animation with live status updates -->
<div class="animation-container">
  <div class="animation-player" id="etl-pipeline">
    <!-- Animation -->
  </div>

  <!-- Live region for screen reader announcements -->
  <div
    id="animation-status"
    role="status"
    aria-live="polite"
    aria-atomic="true"
    class="sr-only"
  >
    <!-- Dynamically updated status -->
  </div>
</div>

<script>
// Update screen reader announcements during animation
class AnimationNarrator {
  constructor(animationId, statusId) {
    this.animation = document.getElementById(animationId);
    this.status = document.getElementById(statusId);
    this.stages = [
      { time: 0, message: 'Animation started: Data extraction phase' },
      { time: 2000, message: 'Data transformation in progress' },
      { time: 4000, message: 'Loading data into destination' },
      { time: 6000, message: 'Animation complete: Pipeline execution finished' }
    ];
  }

  start() {
    this.stages.forEach(stage => {
      setTimeout(() => {
        this.announce(stage.message);
      }, stage.time);
    });
  }

  announce(message) {
    this.status.textContent = message;
  }
}
</script>
```

## Keyboard Navigation

### Focus Management

```javascript
// Keyboard-accessible animation controls
class KeyboardAnimationController {
  constructor(containerSelector) {
    this.container = document.querySelector(containerSelector);
    this.focusableElements = this.container.querySelectorAll(
      'button, [tabindex]:not([tabindex="-1"])'
    );
    this.setupKeyboardHandlers();
  }

  setupKeyboardHandlers() {
    // Space/Enter to toggle play/pause
    this.container.addEventListener('keydown', (e) => {
      if (e.key === ' ' || e.key === 'Spacebar' || e.key === 'Enter') {
        if (e.target.classList.contains('animation-player')) {
          e.preventDefault();
          this.togglePlayPause();
        }
      }

      // Arrow keys for frame-by-frame navigation
      if (e.key === 'ArrowRight') {
        this.nextFrame();
      }
      if (e.key === 'ArrowLeft') {
        this.previousFrame();
      }

      // Escape to stop animation
      if (e.key === 'Escape') {
        this.stopAnimation();
      }
    });
  }

  togglePlayPause() {
    // Implementation
  }

  nextFrame() {
    // Skip forward 1 frame
  }

  previousFrame() {
    // Skip backward 1 frame
  }

  stopAnimation() {
    // Stop and reset
  }
}
```

### Tab Order Management

```html
<!-- Proper tab order for animation interface -->
<div class="animation-interface">
  <div class="animation-display" tabindex="0" role="img" aria-label="Architecture animation">
    <!-- Animation content -->
  </div>

  <div class="controls" role="toolbar" aria-label="Animation controls">
    <button tabindex="0" aria-label="Play animation">Play</button>
    <button tabindex="0" aria-label="Pause animation">Pause</button>
    <button tabindex="0" aria-label="Stop animation">Stop</button>
    <button tabindex="0" aria-label="Restart animation">Restart</button>
  </div>

  <div class="timeline" role="slider" aria-label="Animation timeline"
       aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" tabindex="0">
    <!-- Timeline scrubber -->
  </div>
</div>
```

## Visual Accessibility

### Color Contrast

```css
/* Ensure animations maintain WCAG AA contrast ratios */
.data-flow-line {
  /* Light background: use darker colors */
  stroke: #005A9E; /* Contrast ratio 4.5:1 on white */
  stroke-width: 2px;
}

@media (prefers-color-scheme: dark) {
  .data-flow-line {
    /* Dark background: use lighter colors */
    stroke: #50E6FF; /* Contrast ratio 4.5:1 on dark gray */
  }
}

/* Animated focus indicators */
:focus-visible {
  outline: 3px solid #0078D4;
  outline-offset: 2px;
  animation: focus-pulse 1s ease-in-out;
}

@keyframes focus-pulse {
  0%, 100% { outline-width: 3px; }
  50% { outline-width: 5px; }
}
```

### Text Alternatives

```html
<!-- Complex animation with text alternative -->
<figure class="animation-figure">
  <div class="animation-wrapper">
    <!-- Animated SVG -->
  </div>

  <figcaption>
    <details>
      <summary>Animation description (expand for text alternative)</summary>
      <p>
        This animation illustrates a Lambda architecture pattern implemented
        in Azure. Real-time data flows through the speed layer via Event Hub
        and Stream Analytics, providing low-latency results. Simultaneously,
        the same data flows through the batch layer via Data Factory and
        Synapse Spark, providing comprehensive historical analysis. Both
        layers converge in the serving layer, implemented with Azure Synapse
        SQL, enabling both real-time and batch query capabilities.
      </p>
    </details>
  </figcaption>
</figure>
```

## Testing Procedures

### Automated Testing

```javascript
// Accessibility testing suite for animations
describe('Animation Accessibility Tests', () => {

  test('Respects prefers-reduced-motion', () => {
    // Simulate reduced motion preference
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: jest.fn().mockImplementation(query => ({
        matches: query === '(prefers-reduced-motion: reduce)',
        media: query,
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
      })),
    });

    const animation = new DataFlowAnimation();
    expect(animation.isReduced).toBe(true);
  });

  test('Provides keyboard controls', () => {
    const controller = new AnimationController('#test-animation');
    const playButton = document.querySelector('[aria-label="Play animation"]');

    expect(playButton).toHaveFocus();
    expect(playButton).toHaveAttribute('tabindex', '0');
  });

  test('Announces status changes', async () => {
    const liveRegion = document.querySelector('[role="status"]');
    const animation = new AnimationWithNarration();

    animation.start();
    await waitFor(() => {
      expect(liveRegion.textContent).toContain('Animation started');
    });
  });

  test('Maintains WCAG AA contrast ratio', () => {
    const element = document.querySelector('.animated-element');
    const contrast = getContrastRatio(element);

    expect(contrast).toBeGreaterThanOrEqual(4.5);
  });
});
```

### Manual Testing Checklist

- [ ] **Motion Sensitivity**
  - [ ] Reduced motion preference disables complex animations
  - [ ] Static alternatives are available
  - [ ] No flashing content >3 times per second

- [ ] **Screen Reader Compatibility**
  - [ ] ARIA labels describe animations accurately
  - [ ] Status updates announced appropriately
  - [ ] Text alternatives provided for complex visualizations

- [ ] **Keyboard Navigation**
  - [ ] All controls are keyboard accessible
  - [ ] Focus indicators visible during animations
  - [ ] Tab order is logical

- [ ] **Visual Accessibility**
  - [ ] Contrast ratios meet WCAG AA (4.5:1)
  - [ ] Animations work in high contrast mode
  - [ ] Color is not the only means of conveying information

- [ ] **User Control**
  - [ ] Play/pause controls available
  - [ ] Animation can be stopped
  - [ ] Speed adjustments available (if applicable)

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Animation Guidelines](animation-guidelines.md)
- [Performance Optimization](performance.md)
- [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
- [WebAIM: Accessible Animations](https://webaim.org/articles/keyboard/)

---

*Last Updated: January 2025 | Version: 1.0.0*
