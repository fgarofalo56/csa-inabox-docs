# Animation Export Settings Guide

> **🏠 [Home](../../../../README.md)** | **📖 [Documentation](../../../README.md)** | **🎬 [Multimedia](../../README.md)** | **🎨 [Animations](../README.md)** | **📦 Export Settings**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: Technical Guide](https://img.shields.io/badge/Type-Technical%20Guide-blue)
![Formats: Multiple](https://img.shields.io/badge/Formats-Multiple-purple)

## Overview

This guide provides comprehensive export settings and optimization strategies for animations in the CSA-in-a-Box documentation. Proper export configuration ensures animations are optimized for web delivery, maintain quality across devices, and load efficiently for global audiences accessing Azure analytics documentation.

## Table of Contents

- [Export Formats Overview](#export-formats-overview)
- [SVG Animations](#svg-animations)
- [Lottie JSON](#lottie-json)
- [GIF Animations](#gif-animations)
- [Video Formats](#video-formats)
- [Canvas/WebGL](#canvaswebgl)
- [Optimization Guidelines](#optimization-guidelines)
- [Quality Assurance](#quality-assurance)

## Export Formats Overview

### Format Selection Matrix

| Format | Use Case | File Size | Browser Support | Interactivity | Best For |
|:-------|:---------|:----------|:----------------|:--------------|:---------|
| **SVG** | Icons, diagrams, simple animations | 5-50KB | Excellent | Yes | Architecture diagrams, flow charts |
| **Lottie** | Complex animations, motion graphics | 10-200KB | Good (requires library) | Yes | Data flows, process animations |
| **GIF** | Simple loops, fallback animations | 50-500KB | Universal | No | Email, legacy support |
| **MP4/WebM** | High-quality, long animations | 100KB-5MB | Excellent | Limited | Video tutorials, demos |
| **Canvas** | Real-time, interactive visualizations | N/A (code) | Excellent | Yes | Live dashboards, simulations |
| **WebGL** | 3D, high-performance graphics | N/A (code) | Good | Yes | 3D architecture models |

### Decision Tree

```
Is the animation interactive?
├─ Yes
│  ├─ Simple interaction (hover, click)?
│  │  └─ Use SVG with CSS/JS
│  └─ Complex interaction (data-driven)?
│     └─ Use Canvas or WebGL
│
└─ No
   ├─ Simple shapes and motion?
   │  └─ Use SVG animation
   ├─ Complex motion graphics?
   │  └─ Use Lottie
   └─ Photographic/video content?
      └─ Use MP4/WebM
```

## SVG Animations

### Export Settings for Adobe Illustrator

**File > Export > Export As > SVG**

```
SVG Options:
├─ Styling: Presentation Attributes
├─ Font: Convert to Outlines
├─ Images: Embed
├─ Object IDs: Layer Names
├─ Decimal: 2
├─ Minify: ✓
├─ Responsive: ✓
└─ CSS Properties: Style Attributes
```

### After Effects to SVG (via Bodymovin)

```json
{
  "exportSettings": {
    "format": "svg",
    "path": "./exports/",
    "fileName": "data-flow-animation.svg",
    "options": {
      "inline": false,
      "minify": true,
      "precision": 2,
      "removeHiddenLayers": true,
      "convertShapesToPath": true,
      "exportImages": "embed"
    }
  }
}
```

### Optimized SVG Example

```xml
<!-- Exported and optimized SVG animation -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
  <defs>
    <!-- Reusable gradients -->
    <linearGradient id="azure-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#0078D4;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#00BCF2;stop-opacity:1" />
    </linearGradient>

    <!-- Animation definitions -->
    <style>
      @keyframes flow { from { stroke-dashoffset: 100; } to { stroke-dashoffset: 0; } }
      .data-line { animation: flow 2s linear infinite; }
    </style>
  </defs>

  <!-- Animated data flow -->
  <path d="M 100,300 Q 400,100 700,300"
        stroke="url(#azure-gradient)"
        stroke-width="3"
        fill="none"
        stroke-dasharray="10 5"
        class="data-line" />
</svg>
```

### SVG Optimization with SVGO

```json
{
  "plugins": [
    {
      "name": "preset-default",
      "params": {
        "overrides": {
          "removeViewBox": false,
          "cleanupIDs": {
            "minify": true,
            "preserve": ["azure-gradient", "flow-animation"]
          }
        }
      }
    },
    "removeDimensions",
    "sortAttrs",
    {
      "name": "addAttributesToSVGElement",
      "params": {
        "attributes": [
          { "aria-label": "Data flow visualization" },
          { "role": "img" }
        ]
      }
    }
  ]
}
```

## Lottie JSON

### After Effects Export (Bodymovin Plugin)

**Window > Extensions > Bodymovin**

```json
{
  "bodymovin": {
    "exportSettings": {
      "format": "json",
      "renderer": "svg",
      "glyphs": false,
      "compress": true,
      "splitText": false,
      "hiddenLayers": false,
      "extraComps": false,
      "includeMarkers": true,
      "exportAudio": false,
      "exportImages": "embed",
      "exportImageQuality": 85,
      "exportPaths": "relative",
      "exportIdleFrames": false,
      "skipDefaultProperties": true
    },
    "optimization": {
      "mergeShapes": true,
      "mergePaths": true,
      "removeHiddenLayers": true,
      "simplifyPaths": true,
      "pathPrecision": 2,
      "transformPrecision": 2
    }
  }
}
```

### Lottie Quality Settings

**High Quality (Presentations, Hero Animations)**
```json
{
  "name": "azure-architecture-hero",
  "v": "5.9.0",
  "fr": 60,
  "ip": 0,
  "op": 180,
  "w": 1920,
  "h": 1080,
  "assets": [],
  "layers": [],
  "meta": {
    "g": "Lottie for CSA-in-a-Box",
    "quality": "high",
    "targetSize": "< 500KB"
  }
}
```

**Standard Quality (Documentation Inline)**
```json
{
  "name": "data-pipeline-standard",
  "fr": 30,
  "w": 800,
  "h": 600,
  "meta": {
    "quality": "standard",
    "targetSize": "< 200KB"
  }
}
```

**Optimized (Mobile, Email)**
```json
{
  "name": "process-flow-mobile",
  "fr": 24,
  "w": 600,
  "h": 400,
  "meta": {
    "quality": "optimized",
    "targetSize": "< 100KB"
  }
}
```

### Lottie Player Configuration

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.9.6/lottie.min.js"></script>
<div id="lottie-container"></div>

<script>
const lottieConfig = {
  container: document.getElementById('lottie-container'),
  renderer: 'svg', // 'svg', 'canvas', 'html'
  loop: true,
  autoplay: true,
  path: '/animations/data-flow.json',
  rendererSettings: {
    context: null,
    preserveAspectRatio: 'xMidYMid meet',
    clearCanvas: false,
    progressiveLoad: true,
    hideOnTransparent: true,
    className: 'lottie-svg',
    // SVG-specific
    title: 'Data Flow Animation',
    description: 'Azure data pipeline visualization',
    // Canvas-specific (if using canvas renderer)
    imagePreserveAspectRatio: 'xMidYMid slice'
  }
};

const animation = lottie.loadAnimation(lottieConfig);
</script>
```

## GIF Animations

### Photoshop Export Settings

**File > Export > Save for Web (Legacy)**

```
GIF Settings:
├─ Lossy: 0-10 (depending on content)
├─ Colors: 128-256
├─ Dither: Diffusion
├─ Dither Amount: 75-100%
├─ Transparency: ✓ (if needed)
├─ Interlaced: ✓
├─ Web Snap: 0%
└─ Size: Optimize to target file size
```

### After Effects to GIF (via Media Encoder)

```
Adobe Media Encoder Settings:
├─ Format: Animated GIF
├─ Preset: Custom
├─ Basic Video Settings
│  ├─ Width: 800px
│  ├─ Height: 600px
│  ├─ Frame Rate: 24 fps
│  └─ Field Order: Progressive
├─ Advanced Settings
│  ├─ Quality: 90
│  ├─ Looping: Forever
│  └─ Color: Adaptive, 256 colors
└─ Target: < 2MB for web
```

### GIF Optimization Tools

**Using gifski (Command Line)**
```bash
# High-quality GIF from video
gifski --fps 24 --width 800 --quality 90 input.mp4 -o output.gif

# Optimize existing GIF
gifsicle --optimize=3 --colors 256 input.gif -o optimized.gif

# Reduce file size aggressively
gifsicle --optimize=3 --lossy=80 --colors 128 --scale 0.8 input.gif -o compressed.gif
```

## Video Formats

### MP4 Export (H.264)

**After Effects > Render Queue > Output Module**

```
Format: H.264
├─ Video Codec: H.264
├─ Profile: Main
├─ Level: 4.0
├─ Quality: VBR, 2 pass, Target 5 Mbps, Max 8 Mbps
├─ Frame Rate: 30 fps
├─ Resolution: 1920x1080 (Full HD) or 1280x720 (HD)
├─ Pixel Aspect Ratio: Square Pixels
├─ Field Order: Progressive
└─ Audio: AAC, 128 kbps, 48 kHz
```

### WebM Export (VP9)

**FFmpeg Command Line**
```bash
# High-quality WebM for modern browsers
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus output.webm

# Two-pass encoding for better quality
ffmpeg -i input.mp4 -c:v libvpx-vp9 -b:v 1M -pass 1 -an -f webm /dev/null
ffmpeg -i input.mp4 -c:v libvpx-vp9 -b:v 1M -pass 2 -c:a libopus -b:a 128k output.webm
```

### Responsive Video HTML

```html
<!-- Multiple formats for browser compatibility -->
<video
  width="800"
  height="600"
  controls
  preload="metadata"
  poster="/images/video-poster.jpg"
  aria-label="Azure Synapse workspace setup tutorial"
>
  <source src="/videos/synapse-setup.webm" type="video/webm">
  <source src="/videos/synapse-setup.mp4" type="video/mp4">

  <!-- Fallback for browsers without video support -->
  <p>
    Your browser doesn't support HTML video.
    <a href="/videos/synapse-setup.mp4">Download the video</a> instead.
  </p>
</video>
```

### Video Optimization Settings by Use Case

**Tutorial Videos (5-10 minutes)**
- Resolution: 1280x720 (720p)
- Bitrate: 2-3 Mbps
- Format: MP4 (H.264) + WebM (VP9)
- Target size: 50-150MB

**Demo Clips (30-60 seconds)**
- Resolution: 1920x1080 (1080p)
- Bitrate: 3-5 Mbps
- Format: MP4 (H.264) + WebM (VP9)
- Target size: 10-30MB

**Micro Animations (5-15 seconds)**
- Resolution: 800x600
- Bitrate: 1-2 Mbps
- Format: MP4 (H.264) or consider GIF/Lottie
- Target size: 1-5MB

## Canvas/WebGL

### Canvas Export Considerations

**Canvas animations are code-based, not exported files**

```javascript
// Optimized canvas rendering
class OptimizedCanvasAnimation {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d', {
      alpha: false, // Disable transparency if not needed
      desynchronized: true // Reduce latency
    });

    // Use device pixel ratio for sharp rendering
    this.dpr = window.devicePixelRatio || 1;
    this.setCanvasSize();
  }

  setCanvasSize() {
    const rect = this.canvas.getBoundingClientRect();

    // Set actual canvas pixel size
    this.canvas.width = rect.width * this.dpr;
    this.canvas.height = rect.height * this.dpr;

    // Scale context for high DPI displays
    this.ctx.scale(this.dpr, this.dpr);

    // Set CSS size
    this.canvas.style.width = rect.width + 'px';
    this.canvas.style.height = rect.height + 'px';
  }

  render() {
    // Clear previous frame
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Render animation frame
    // ... rendering code ...

    // Request next frame
    requestAnimationFrame(() => this.render());
  }
}
```

### WebGL Performance Settings

```javascript
// Optimized WebGL context
const canvas = document.getElementById('webgl-canvas');
const gl = canvas.getContext('webgl2', {
  alpha: false,
  antialias: true,
  depth: true,
  premultipliedAlpha: false,
  preserveDrawingBuffer: false,
  powerPreference: 'high-performance'
});

// Enable extensions for better performance
const ext = gl.getExtension('WEBGL_compressed_texture_s3tc');
```

## Optimization Guidelines

### File Size Targets

| Animation Type | Max File Size | Recommended Size | Notes |
|:--------------|:--------------|:-----------------|:------|
| **Icon animations** | 10KB | 5KB | SVG or Lottie |
| **Inline documentation** | 200KB | 100KB | Any format |
| **Hero animations** | 500KB | 300KB | Lottie or video |
| **Tutorial videos** | 10MB | 5MB | MP4 + WebM |
| **Full presentations** | 50MB | 25MB | Multiple videos |

### Image Optimization

**Embed Images in Animations**
```bash
# Convert images to WebP before embedding
cwebp -q 85 input.png -o output.webp

# Optimize PNG images
pngquant --quality=85-95 input.png -o output.png
optipng -o7 output.png

# Optimize JPEG images
jpegoptim --max=85 --strip-all input.jpg
```

### Compression Techniques

**Gzip Compression (Server-side)**
```nginx
# Nginx configuration
gzip on;
gzip_types application/json text/css text/javascript application/javascript;
gzip_min_length 1000;
gzip_comp_level 6;
```

**Brotli Compression (Better than Gzip)**
```nginx
# Nginx with Brotli module
brotli on;
brotli_types application/json text/css text/javascript application/javascript;
brotli_comp_level 6;
```

## Quality Assurance

### Pre-Export Checklist

- [ ] **File Preparation**
  - [ ] Remove unused layers and assets
  - [ ] Consolidate duplicate elements
  - [ ] Optimize paths and shapes
  - [ ] Check text has been converted to outlines (if needed)

- [ ] **Animation Review**
  - [ ] Verify all keyframes are necessary
  - [ ] Check for smooth easing
  - [ ] Confirm animation loops properly (if applicable)
  - [ ] Test at target frame rate

- [ ] **Accessibility**
  - [ ] Add ARIA labels and descriptions
  - [ ] Provide static alternative
  - [ ] Check contrast ratios
  - [ ] Verify reduced motion compatibility

### Post-Export Validation

```javascript
// Automated quality checks
class AnimationQualityChecker {
  async validateExport(filePath) {
    const results = {
      fileSize: await this.checkFileSize(filePath),
      format: await this.validateFormat(filePath),
      performance: await this.testPerformance(filePath),
      accessibility: await this.checkAccessibility(filePath)
    };

    return results;
  }

  async checkFileSize(filePath) {
    const stats = await fs.stat(filePath);
    const sizeKB = stats.size / 1024;
    const maxSize = this.getMaxSize(filePath);

    return {
      size: sizeKB,
      maxSize: maxSize,
      passed: sizeKB <= maxSize,
      warning: sizeKB > maxSize * 0.8
    };
  }

  async testPerformance(filePath) {
    // Load animation and measure FPS
    const animation = await this.loadAnimation(filePath);
    const fps = await this.measureFPS(animation);

    return {
      fps: fps,
      passed: fps >= 30,
      optimal: fps >= 60
    };
  }
}
```

### Cross-Browser Testing

**Test Matrix**
```javascript
const testBrowsers = [
  { name: 'Chrome', version: '90+', priority: 'high' },
  { name: 'Firefox', version: '88+', priority: 'high' },
  { name: 'Safari', version: '14+', priority: 'high' },
  { name: 'Edge', version: '90+', priority: 'medium' },
  { name: 'iOS Safari', version: '14+', priority: 'high' },
  { name: 'Chrome Mobile', version: '90+', priority: 'high' }
];

const testSizes = [
  { width: 1920, height: 1080, name: 'Desktop HD' },
  { width: 1366, height: 768, name: 'Laptop' },
  { width: 768, height: 1024, name: 'Tablet' },
  { width: 375, height: 667, name: 'Mobile' }
];
```

## Export Workflow Summary

```
1. Design & Animate
   ├─ Create in preferred tool
   ├─ Optimize during design
   └─ Review animation

2. Pre-Export
   ├─ Clean up project
   ├─ Run optimization
   └─ Check accessibility

3. Export
   ├─ Choose format
   ├─ Apply settings
   └─ Generate files

4. Post-Export
   ├─ Optimize files
   ├─ Test performance
   └─ Validate quality

5. Deploy
   ├─ Upload to CDN
   ├─ Configure compression
   └─ Monitor performance
```

## Resources

- [Animation Guidelines](animation-guidelines.md)
- [Performance Optimization](performance.md)
- [Accessibility Guidelines](accessibility.md)
- [SVGO Optimizer](https://github.com/svg/svgo)
- [Lottie Files](https://lottiefiles.com/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)

---

*Last Updated: January 2025 | Version: 1.0.0*
