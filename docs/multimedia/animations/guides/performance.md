# Animation Performance Optimization Guide

> **🏠 [Home](../../../../README.md)** | **📖 [Documentation](../../../README.md)** | **🎬 [Multimedia](../../README.md)** | **🎨 [Animations](../README.md)** | **⚡ Performance**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: Performance](https://img.shields.io/badge/Type-Performance-blue)
![Impact: Critical](https://img.shields.io/badge/Impact-Critical-red)

## Overview

Animation performance is critical for user experience in the CSA-in-a-Box documentation. This guide provides comprehensive strategies for optimizing animations to achieve smooth 60fps performance across all devices, minimize resource usage, and ensure fast load times for global audiences accessing Azure analytics content.

## Table of Contents

- [Performance Targets](#performance-targets)
- [GPU Acceleration](#gpu-acceleration)
- [Rendering Optimization](#rendering-optimization)
- [Memory Management](#memory-management)
- [Loading Strategies](#loading-strategies)
- [Performance Monitoring](#performance-monitoring)
- [Mobile Optimization](#mobile-optimization)
- [Debugging Tools](#debugging-tools)

## Performance Targets

### Frame Rate Standards

| Target | Frame Rate | Use Case | User Experience |
|:-------|:-----------|:---------|:----------------|
| **Optimal** | 60 fps | Modern devices, smooth animations | Buttery smooth |
| **Good** | 45-59 fps | Mid-range devices | Smooth with minor drops |
| **Acceptable** | 30-44 fps | Older devices, complex animations | Usable |
| **Poor** | <30 fps | Needs optimization | Janky, noticeable lag |

### Performance Budgets

```javascript
const performanceBudgets = {
  // File size limits
  fileSizes: {
    svg: 50,        // KB
    lottie: 200,    // KB
    video: 5000,    // KB (5MB)
    total: 10000    // KB (10MB) per page
  },

  // Runtime performance
  runtime: {
    fps: 60,               // Target frame rate
    frameTime: 16.67,      // ms (1000/60)
    paintTime: 10,         // ms max paint time
    scriptTime: 5,         // ms max script execution
    memoryUsage: 100       // MB max memory for animations
  },

  // Loading performance
  loading: {
    firstPaint: 1000,      // ms
    interactive: 2000,     // ms
    totalLoad: 3000        // ms
  }
};
```

### Key Metrics to Track

```javascript
// Performance monitoring class
class AnimationPerformanceTracker {
  constructor() {
    this.metrics = {
      fps: [],
      frameTime: [],
      memoryUsage: [],
      loadTime: 0,
      totalFrames: 0,
      droppedFrames: 0
    };

    this.lastFrameTime = performance.now();
    this.startTime = performance.now();
  }

  measureFrame() {
    const now = performance.now();
    const delta = now - this.lastFrameTime;

    // Calculate FPS
    const fps = 1000 / delta;
    this.metrics.fps.push(fps);
    this.metrics.frameTime.push(delta);
    this.metrics.totalFrames++;

    // Detect dropped frames (>16.67ms)
    if (delta > 16.67) {
      this.metrics.droppedFrames++;
    }

    this.lastFrameTime = now;

    // Log warnings
    if (fps < 30) {
      console.warn(`Low FPS detected: ${fps.toFixed(2)}`);
    }
  }

  getAverageFPS() {
    return this.metrics.fps.reduce((a, b) => a + b, 0) / this.metrics.fps.length;
  }

  getDroppedFramePercentage() {
    return (this.metrics.droppedFrames / this.metrics.totalFrames) * 100;
  }

  getReport() {
    return {
      averageFPS: this.getAverageFPS().toFixed(2),
      minFPS: Math.min(...this.metrics.fps).toFixed(2),
      maxFPS: Math.max(...this.metrics.fps).toFixed(2),
      droppedFrames: this.metrics.droppedFrames,
      droppedPercentage: this.getDroppedFramePercentage().toFixed(2) + '%',
      totalRuntime: (performance.now() - this.startTime).toFixed(2) + 'ms'
    };
  }
}
```

## GPU Acceleration

### Hardware Acceleration Triggers

**Properties that trigger GPU acceleration:**
- `transform: translate3d(0, 0, 0)`
- `transform: translateZ(0)`
- `will-change: transform, opacity`
- `backface-visibility: hidden`
- `perspective: 1000px`

### CSS GPU Optimization

```css
/* Force GPU acceleration for smooth animations */
.gpu-accelerated {
  /* Promote to composite layer */
  transform: translateZ(0);
  /* Or use translate3d */
  transform: translate3d(0, 0, 0);

  /* Tell browser what will change */
  will-change: transform, opacity;

  /* Prevent flickering */
  backface-visibility: hidden;
  -webkit-font-smoothing: antialiased;
}

/* Data flow animation optimized for GPU */
.data-particle {
  will-change: transform;
  transform: translate3d(0, 0, 0);
}

@keyframes particleFlow {
  0% { transform: translate3d(0, 0, 0); }
  100% { transform: translate3d(100%, 0, 0); }
}

.data-particle {
  animation: particleFlow 2s linear infinite;
}
```

### Composite Layer Management

```css
/* Good - Promotes to own layer */
.service-node {
  will-change: transform;
  transform: translateZ(0);
}

/* Bad - Creates too many layers, hurts performance */
.animated-element * {
  will-change: transform, opacity, filter;
  transform: translateZ(0);
}

/* Optimal - Strategic layer promotion */
.critical-animation {
  will-change: transform;
}

.critical-animation.animating {
  transform: translateZ(0);
}

/* Clean up after animation */
.critical-animation.complete {
  will-change: auto;
  transform: none;
}
```

### will-change Best Practices

```javascript
// Dynamic will-change management
class WillChangeManager {
  constructor(element) {
    this.element = element;
  }

  // Add will-change before animation
  prepare(properties = ['transform', 'opacity']) {
    this.element.style.willChange = properties.join(', ');
  }

  // Start animation after browser optimizes
  startAnimation(delay = 0) {
    setTimeout(() => {
      this.element.classList.add('animating');
    }, delay);
  }

  // Remove will-change after animation
  cleanup() {
    this.element.addEventListener('animationend', () => {
      this.element.style.willChange = 'auto';
    }, { once: true });
  }

  // Full lifecycle
  animate() {
    this.prepare();
    requestAnimationFrame(() => {
      this.startAnimation();
      this.cleanup();
    });
  }
}

// Usage
const animator = new WillChangeManager(document.querySelector('.data-flow'));
animator.animate();
```

## Rendering Optimization

### Minimize Layout Thrashing

```javascript
// Bad - Causes layout thrashing
function badAnimation(elements) {
  elements.forEach(el => {
    const height = el.offsetHeight; // Read
    el.style.height = height + 10 + 'px'; // Write
    const width = el.offsetWidth; // Read
    el.style.width = width + 10 + 'px'; // Write
  });
}

// Good - Batch reads and writes
function goodAnimation(elements) {
  // Batch all reads
  const dimensions = elements.map(el => ({
    element: el,
    height: el.offsetHeight,
    width: el.offsetWidth
  }));

  // Batch all writes
  requestAnimationFrame(() => {
    dimensions.forEach(({ element, height, width }) => {
      element.style.height = height + 10 + 'px';
      element.style.width = width + 10 + 'px';
    });
  });
}

// Best - Use transform instead
function bestAnimation(elements) {
  elements.forEach(el => {
    el.style.transform = 'scale(1.1)';
  });
}
```

### Use Transform Instead of Position

```css
/* Bad - Triggers layout recalculation */
.moving-element-bad {
  position: absolute;
  animation: moveBad 1s ease;
}

@keyframes moveBad {
  0% { left: 0; top: 0; }
  100% { left: 100px; top: 100px; }
}

/* Good - GPU accelerated */
.moving-element-good {
  animation: moveGood 1s ease;
}

@keyframes moveGood {
  0% { transform: translate(0, 0); }
  100% { transform: translate(100px, 100px); }
}

/* Best - 3D transform for hardware acceleration */
.moving-element-best {
  animation: moveBest 1s ease;
}

@keyframes moveBest {
  0% { transform: translate3d(0, 0, 0); }
  100% { transform: translate3d(100px, 100px, 0); }
}
```

### Optimize Paint Areas

```css
/* Isolate animations to minimize paint areas */
.isolated-animation {
  /* Create stacking context */
  position: relative;
  z-index: 1;

  /* Contain paint to this element */
  contain: layout paint;

  /* Promote to composite layer */
  will-change: transform;
}

/* CSS Containment for better performance */
.animation-container {
  /* Layout containment */
  contain: layout;
}

.animation-content {
  /* Paint containment */
  contain: paint;
}

.complex-animation {
  /* Full containment */
  contain: strict;
}
```

## Memory Management

### Object Pooling for Animations

```javascript
// Object pool for frequently created/destroyed animated objects
class AnimationObjectPool {
  constructor(factory, initialSize = 10) {
    this.factory = factory;
    this.available = [];
    this.inUse = new Set();

    // Pre-create objects
    for (let i = 0; i < initialSize; i++) {
      this.available.push(this.factory());
    }
  }

  acquire() {
    let obj;

    if (this.available.length > 0) {
      obj = this.available.pop();
    } else {
      obj = this.factory();
      console.log('Pool exhausted, creating new object');
    }

    this.inUse.add(obj);
    return obj;
  }

  release(obj) {
    if (this.inUse.has(obj)) {
      this.inUse.delete(obj);
      obj.reset(); // Reset object state
      this.available.push(obj);
    }
  }

  clear() {
    this.available = [];
    this.inUse.clear();
  }
}

// Particle class with reset method
class Particle {
  constructor() {
    this.x = 0;
    this.y = 0;
    this.vx = 0;
    this.vy = 0;
    this.active = false;
  }

  reset() {
    this.x = 0;
    this.y = 0;
    this.vx = 0;
    this.vy = 0;
    this.active = false;
  }
}

// Usage
const particlePool = new AnimationObjectPool(() => new Particle(), 100);

function createDataFlowParticle() {
  const particle = particlePool.acquire();
  particle.x = Math.random() * 800;
  particle.y = 0;
  particle.vy = 2;
  particle.active = true;
  return particle;
}

function removeParticle(particle) {
  particlePool.release(particle);
}
```

### Memory Leak Prevention

```javascript
// Animation lifecycle manager to prevent leaks
class AnimationLifecycleManager {
  constructor() {
    this.animations = new Map();
    this.timers = new Map();
    this.listeners = new Map();
  }

  registerAnimation(id, animation) {
    // Clean up existing animation with same ID
    this.cleanup(id);

    this.animations.set(id, animation);

    // Auto-cleanup on completion
    animation.addEventListener('finish', () => {
      this.cleanup(id);
    });
  }

  registerTimer(id, timerId) {
    this.timers.set(id, timerId);
  }

  registerListener(id, element, event, handler) {
    if (!this.listeners.has(id)) {
      this.listeners.set(id, []);
    }

    this.listeners.get(id).push({ element, event, handler });
    element.addEventListener(event, handler);
  }

  cleanup(id) {
    // Stop animation
    const animation = this.animations.get(id);
    if (animation) {
      animation.cancel();
      this.animations.delete(id);
    }

    // Clear timers
    const timer = this.timers.get(id);
    if (timer) {
      clearTimeout(timer);
      clearInterval(timer);
      this.timers.delete(id);
    }

    // Remove event listeners
    const listeners = this.listeners.get(id);
    if (listeners) {
      listeners.forEach(({ element, event, handler }) => {
        element.removeEventListener(event, handler);
      });
      this.listeners.delete(id);
    }
  }

  cleanupAll() {
    this.animations.forEach((_, id) => this.cleanup(id));
    this.timers.forEach((_, id) => this.cleanup(id));
    this.listeners.forEach((_, id) => this.cleanup(id));
  }
}

// Usage
const lifecycleManager = new AnimationLifecycleManager();

// Register animation
const animation = element.animate(keyframes, options);
lifecycleManager.registerAnimation('data-flow-1', animation);

// Clean up when component unmounts
window.addEventListener('beforeunload', () => {
  lifecycleManager.cleanupAll();
});
```

## Loading Strategies

### Lazy Loading Animations

```javascript
// Intersection Observer for lazy loading
class LazyAnimationLoader {
  constructor(options = {}) {
    this.options = {
      rootMargin: '50px',
      threshold: 0.1,
      ...options
    };

    this.observer = new IntersectionObserver(
      this.handleIntersection.bind(this),
      this.options
    );

    this.loadedAnimations = new Set();
  }

  observe(element) {
    this.observer.observe(element);
  }

  handleIntersection(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting && !this.loadedAnimations.has(entry.target)) {
        this.loadAnimation(entry.target);
        this.loadedAnimations.add(entry.target);
        this.observer.unobserve(entry.target);
      }
    });
  }

  async loadAnimation(element) {
    const animationSrc = element.dataset.animationSrc;
    const animationType = element.dataset.animationType;

    try {
      element.classList.add('loading');

      switch (animationType) {
        case 'lottie':
          await this.loadLottie(element, animationSrc);
          break;
        case 'video':
          await this.loadVideo(element, animationSrc);
          break;
        default:
          element.src = animationSrc;
      }

      element.classList.remove('loading');
      element.classList.add('loaded');
    } catch (error) {
      console.error('Failed to load animation:', error);
      element.classList.add('error');
    }
  }

  async loadLottie(element, src) {
    const animation = lottie.loadAnimation({
      container: element,
      path: src,
      renderer: 'svg',
      loop: element.dataset.loop === 'true',
      autoplay: element.dataset.autoplay === 'true'
    });

    return new Promise((resolve) => {
      animation.addEventListener('DOMLoaded', resolve);
    });
  }

  async loadVideo(element, src) {
    const video = document.createElement('video');
    video.src = src;
    video.preload = 'metadata';

    return new Promise((resolve, reject) => {
      video.addEventListener('loadedmetadata', () => {
        element.appendChild(video);
        resolve();
      });
      video.addEventListener('error', reject);
    });
  }
}

// Initialize
const lazyLoader = new LazyAnimationLoader();

document.querySelectorAll('[data-lazy-animation]').forEach(el => {
  lazyLoader.observe(el);
});
```

### Progressive Loading

```javascript
// Progressive animation loading strategy
class ProgressiveAnimationLoader {
  async loadAnimation(priority = 'low') {
    const strategies = {
      critical: this.loadImmediately.bind(this),
      high: this.loadAfterPaint.bind(this),
      medium: this.loadOnIdle.bind(this),
      low: this.loadOnInteraction.bind(this)
    };

    return strategies[priority]();
  }

  loadImmediately(animationSrc) {
    return this.load(animationSrc);
  }

  async loadAfterPaint(animationSrc) {
    // Wait for first paint
    await new Promise(resolve => {
      if (document.readyState === 'complete') {
        resolve();
      } else {
        window.addEventListener('load', resolve, { once: true });
      }
    });

    return this.load(animationSrc);
  }

  async loadOnIdle(animationSrc) {
    // Use requestIdleCallback when available
    if ('requestIdleCallback' in window) {
      return new Promise(resolve => {
        requestIdleCallback(() => {
          this.load(animationSrc).then(resolve);
        }, { timeout: 2000 });
      });
    } else {
      // Fallback to setTimeout
      return new Promise(resolve => {
        setTimeout(() => {
          this.load(animationSrc).then(resolve);
        }, 1000);
      });
    }
  }

  async loadOnInteraction(animationSrc) {
    return new Promise(resolve => {
      const events = ['scroll', 'mousemove', 'touchstart', 'click'];
      const handler = () => {
        events.forEach(event => {
          window.removeEventListener(event, handler);
        });
        this.load(animationSrc).then(resolve);
      };

      events.forEach(event => {
        window.addEventListener(event, handler, { once: true, passive: true });
      });
    });
  }

  async load(src) {
    // Actual loading logic
    const response = await fetch(src);
    return response.json();
  }
}
```

## Performance Monitoring

### Real-time FPS Monitor

```javascript
// Visual FPS counter for development
class FPSMonitor {
  constructor(container) {
    this.container = container || document.body;
    this.display = this.createDisplay();
    this.frames = [];
    this.lastTime = performance.now();
    this.start();
  }

  createDisplay() {
    const div = document.createElement('div');
    div.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      background: rgba(0, 0, 0, 0.8);
      color: #0f0;
      padding: 10px;
      font-family: monospace;
      font-size: 14px;
      z-index: 99999;
      border-radius: 4px;
    `;
    this.container.appendChild(div);
    return div;
  }

  update() {
    const now = performance.now();
    const delta = now - this.lastTime;

    this.frames.push(1000 / delta);

    // Keep last 60 frames
    if (this.frames.length > 60) {
      this.frames.shift();
    }

    const avg = this.frames.reduce((a, b) => a + b) / this.frames.length;
    const min = Math.min(...this.frames);
    const max = Math.max(...this.frames);

    // Color code based on performance
    const color = avg >= 55 ? '#0f0' : avg >= 30 ? '#ff0' : '#f00';

    this.display.style.color = color;
    this.display.innerHTML = `
      FPS: ${avg.toFixed(1)}<br>
      Min: ${min.toFixed(1)}<br>
      Max: ${max.toFixed(1)}<br>
      Frame: ${delta.toFixed(2)}ms
    `;

    this.lastTime = now;
  }

  start() {
    const loop = () => {
      this.update();
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }
}

// Enable in development
if (process.env.NODE_ENV === 'development') {
  new FPSMonitor();
}
```

### Performance API Integration

```javascript
// Comprehensive performance measurement
class AnimationPerformanceAnalyzer {
  constructor(animationName) {
    this.animationName = animationName;
    this.marks = new Map();
  }

  start() {
    performance.mark(`${this.animationName}-start`);
  }

  mark(label) {
    performance.mark(`${this.animationName}-${label}`);
  }

  end() {
    performance.mark(`${this.animationName}-end`);
    this.measure();
  }

  measure() {
    performance.measure(
      this.animationName,
      `${this.animationName}-start`,
      `${this.animationName}-end`
    );
  }

  getMetrics() {
    const measures = performance.getEntriesByType('measure')
      .filter(m => m.name === this.animationName);

    if (measures.length === 0) return null;

    const latest = measures[measures.length - 1];

    return {
      name: latest.name,
      duration: latest.duration.toFixed(2),
      startTime: latest.startTime.toFixed(2)
    };
  }

  report() {
    const metrics = this.getMetrics();
    if (metrics) {
      console.table([metrics]);
    }
  }

  clear() {
    performance.clearMarks();
    performance.clearMeasures(this.animationName);
  }
}

// Usage
const analyzer = new AnimationPerformanceAnalyzer('data-flow-animation');
analyzer.start();
// ... run animation ...
analyzer.mark('midpoint');
// ... continue animation ...
analyzer.end();
analyzer.report();
```

## Mobile Optimization

### Device Detection and Adaptation

```javascript
// Adaptive animation quality based on device
class AdaptiveAnimationController {
  constructor() {
    this.deviceCapabilities = this.detectCapabilities();
    this.qualityLevel = this.determineQuality();
  }

  detectCapabilities() {
    return {
      // Device type
      isMobile: /Android|iPhone|iPad|iPod/i.test(navigator.userAgent),
      isLowEnd: this.isLowEndDevice(),

      // Hardware
      cores: navigator.hardwareConcurrency || 2,
      memory: navigator.deviceMemory || 4, // GB
      connection: this.getConnectionSpeed(),

      // Display
      pixelRatio: window.devicePixelRatio || 1,
      screenSize: window.screen.width * window.screen.height
    };
  }

  isLowEndDevice() {
    // Heuristics for low-end device detection
    const cores = navigator.hardwareConcurrency || 2;
    const memory = navigator.deviceMemory || 4;

    return cores <= 2 || memory <= 2;
  }

  getConnectionSpeed() {
    if ('connection' in navigator) {
      const conn = navigator.connection;
      return {
        effectiveType: conn.effectiveType, // '4g', '3g', '2g', 'slow-2g'
        downlink: conn.downlink, // Mbps
        saveData: conn.saveData
      };
    }
    return { effectiveType: '4g', downlink: 10, saveData: false };
  }

  determineQuality() {
    const { isMobile, isLowEnd, memory, connection } = this.deviceCapabilities;

    // Save Data mode
    if (connection.saveData) {
      return 'minimal';
    }

    // Low-end device
    if (isLowEnd || memory <= 2) {
      return 'low';
    }

    // Mobile device with slow connection
    if (isMobile && (connection.effectiveType === '3g' || connection.effectiveType === '2g')) {
      return 'medium';
    }

    // Mobile device with good connection
    if (isMobile) {
      return 'medium';
    }

    // Desktop/high-end
    return 'high';
  }

  getAnimationConfig() {
    const configs = {
      minimal: {
        enabled: false,
        staticFallback: true,
        message: 'Animations disabled to save data'
      },
      low: {
        enabled: true,
        fps: 24,
        particleCount: 10,
        effects: 'none',
        quality: 0.5
      },
      medium: {
        enabled: true,
        fps: 30,
        particleCount: 50,
        effects: 'basic',
        quality: 0.75
      },
      high: {
        enabled: true,
        fps: 60,
        particleCount: 200,
        effects: 'full',
        quality: 1.0
      }
    };

    return configs[this.qualityLevel];
  }
}

// Apply adaptive settings
const adaptiveController = new AdaptiveAnimationController();
const config = adaptiveController.getAnimationConfig();

console.log('Animation quality level:', adaptiveController.qualityLevel);
console.log('Configuration:', config);
```

### Touch Interaction Optimization

```javascript
// Optimized touch handling for mobile animations
class TouchOptimizedAnimation {
  constructor(element) {
    this.element = element;
    this.setupTouchHandlers();
  }

  setupTouchHandlers() {
    let touchStartTime;

    // Use passive listeners for better scroll performance
    this.element.addEventListener('touchstart', (e) => {
      touchStartTime = performance.now();
      this.onTouchStart(e);
    }, { passive: true });

    this.element.addEventListener('touchmove', (e) => {
      // Throttle touch move events
      requestAnimationFrame(() => this.onTouchMove(e));
    }, { passive: true });

    this.element.addEventListener('touchend', (e) => {
      const touchDuration = performance.now() - touchStartTime;
      this.onTouchEnd(e, touchDuration);
    }, { passive: true });
  }

  onTouchStart(e) {
    // Pause animation on touch
    this.element.classList.add('paused');
  }

  onTouchMove(e) {
    // Update animation based on touch position
  }

  onTouchEnd(e, duration) {
    // Resume animation
    this.element.classList.remove('paused');

    // Quick tap = toggle, long press = stop
    if (duration < 200) {
      this.toggle();
    } else if (duration > 1000) {
      this.stop();
    }
  }

  toggle() {
    // Toggle play/pause
  }

  stop() {
    // Stop animation
  }
}
```

## Debugging Tools

### Chrome DevTools Performance Profiling

```javascript
// Programmatic performance profiling
class PerformanceProfiler {
  startProfiling(label = 'Animation Profile') {
    console.profile(label);
    performance.mark('profile-start');
  }

  stopProfiling() {
    performance.mark('profile-end');
    performance.measure('profile-duration', 'profile-start', 'profile-end');

    const measure = performance.getEntriesByName('profile-duration')[0];
    console.log(`Profile duration: ${measure.duration.toFixed(2)}ms`);

    console.profileEnd();

    // Clean up marks
    performance.clearMarks();
    performance.clearMeasures();
  }

  captureTrace() {
    // Capture performance trace data
    const perfEntries = performance.getEntries();

    const trace = {
      marks: perfEntries.filter(e => e.entryType === 'mark'),
      measures: perfEntries.filter(e => e.entryType === 'measure'),
      resources: perfEntries.filter(e => e.entryType === 'resource'),
      navigation: perfEntries.filter(e => e.entryType === 'navigation')
    };

    return trace;
  }
}

// Usage
const profiler = new PerformanceProfiler();
profiler.startProfiling('Data Flow Animation');
// ... run animation ...
profiler.stopProfiling();
const trace = profiler.captureTrace();
console.log('Performance trace:', trace);
```

### Visual Performance Overlay

```html
<!-- Performance debugging overlay -->
<div id="perf-overlay" style="
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0,0,0,0.9);
  color: #fff;
  padding: 10px;
  font-family: monospace;
  font-size: 12px;
  display: none;
  z-index: 99999;
">
  <div id="perf-metrics"></div>
  <canvas id="perf-graph" width="800" height="100"></canvas>
</div>

<script>
class PerformanceOverlay {
  constructor() {
    this.overlay = document.getElementById('perf-overlay');
    this.metrics = document.getElementById('perf-metrics');
    this.canvas = document.getElementById('perf-graph');
    this.ctx = this.canvas.getContext('2d');
    this.fpsHistory = [];
    this.maxHistory = 200;
  }

  show() {
    this.overlay.style.display = 'block';
    this.startMonitoring();
  }

  hide() {
    this.overlay.style.display = 'none';
  }

  startMonitoring() {
    let lastTime = performance.now();

    const monitor = () => {
      const now = performance.now();
      const delta = now - lastTime;
      const fps = 1000 / delta;

      this.fpsHistory.push(fps);
      if (this.fpsHistory.length > this.maxHistory) {
        this.fpsHistory.shift();
      }

      this.updateMetrics(fps, delta);
      this.drawGraph();

      lastTime = now;
      requestAnimationFrame(monitor);
    };

    monitor();
  }

  updateMetrics(fps, delta) {
    const memory = performance.memory ?
      (performance.memory.usedJSHeapSize / 1048576).toFixed(2) : 'N/A';

    this.metrics.innerHTML = `
      FPS: ${fps.toFixed(1)} |
      Frame: ${delta.toFixed(2)}ms |
      Memory: ${memory}MB
    `;
  }

  drawGraph() {
    const { width, height } = this.canvas;
    this.ctx.clearRect(0, 0, width, height);

    // Draw grid
    this.ctx.strokeStyle = '#333';
    this.ctx.beginPath();
    this.ctx.moveTo(0, height / 2);
    this.ctx.lineTo(width, height / 2);
    this.ctx.stroke();

    // Draw FPS line
    this.ctx.strokeStyle = '#0f0';
    this.ctx.beginPath();

    this.fpsHistory.forEach((fps, i) => {
      const x = (i / this.maxHistory) * width;
      const y = height - (fps / 60) * height;
      if (i === 0) {
        this.ctx.moveTo(x, y);
      } else {
        this.ctx.lineTo(x, y);
      }
    });

    this.ctx.stroke();
  }
}

// Toggle with Ctrl+Shift+P
const perfOverlay = new PerformanceOverlay();
document.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.shiftKey && e.key === 'P') {
    perfOverlay.show();
  }
});
</script>
```

## Best Practices Summary

**DO:**
- Target 60fps on modern devices, minimum 30fps on older hardware
- Use `transform` and `opacity` for animations
- Leverage GPU acceleration with `will-change` and `translate3d`
- Implement lazy loading for off-screen animations
- Monitor performance metrics in production
- Optimize for mobile devices and slow connections
- Clean up animations and event listeners properly

**DON'T:**
- Animate layout properties (width, height, margin, padding)
- Create excessive composite layers
- Leave `will-change` on permanently
- Ignore memory leaks from abandoned animations
- Load all animations upfront
- Use high-quality settings on low-end devices
- Forget to test on real mobile devices

## Resources

- [Animation Guidelines](animation-guidelines.md)
- [Accessibility Guidelines](accessibility.md)
- [Export Settings](export-settings.md)
- [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/)
- [Web Performance Working Group](https://www.w3.org/webperf/)
- [CSS Triggers](https://csstriggers.com/)

---

*Last Updated: January 2025 | Version: 1.0.0*
