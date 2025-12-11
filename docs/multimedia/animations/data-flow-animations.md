# Data Flow Animation Specifications

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎨 [Animations](README.md)** | **📊 Data Flow Animations**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: Lottie/SVG](https://img.shields.io/badge/Type-Lottie%2FSVG-blue)
![Duration: 30-60s](https://img.shields.io/badge/Duration-30--60s-purple)

## Overview

Data flow animations visualize how data moves through Azure Synapse Analytics pipelines, from ingestion to transformation and consumption. These animations help users understand complex data movement patterns and processing workflows.

## Real-Time Stream Processing Animation

### Specification

**Duration**: 30 seconds
**Format**: Lottie JSON
**Frame Rate**: 60 fps
**Dimensions**: 1920x1080
**File Size Target**: < 2MB

### Scene Breakdown

#### Scene 1: Data Sources (0-5s)

**Visual Elements**:
- IoT devices emitting data points
- Application servers sending events
- Sensor networks transmitting readings

**Animation**:

```json
{
  "time": "0-5s",
  "elements": [
    {
      "type": "IoT_Device",
      "animation": "pulse",
      "frequency": "2Hz",
      "color": "#0078D4"
    },
    {
      "type": "Data_Particle",
      "animation": "emit",
      "count": 5,
      "speed": "fast"
    }
  ],
  "transition": "fade-in"
}
```

#### Scene 2: Event Hub Ingestion (5-15s)

**Visual Elements**:
- Event streams flowing to Event Hub
- Partition distribution
- Message buffering

**Animation**:

```json
{
  "time": "5-15s",
  "elements": [
    {
      "type": "Event_Stream",
      "path": "curved",
      "particles": 20,
      "color_gradient": ["#0078D4", "#00BCF2"]
    },
    {
      "type": "Event_Hub",
      "animation": "rotate_partitions",
      "partitions": 4,
      "fill_animation": "progressive"
    }
  ],
  "transition": "flow"
}
```

#### Scene 3: Stream Analytics Processing (15-25s)

**Visual Elements**:
- Windowing operations
- Aggregation functions
- Filtering logic

**Animation**:

```json
{
  "time": "15-25s",
  "elements": [
    {
      "type": "Processing_Window",
      "animation": "sliding_window",
      "window_size": "5s",
      "slide": "1s"
    },
    {
      "type": "Transform",
      "icon": "gear",
      "animation": "rotate",
      "speed": "medium"
    }
  ],
  "transition": "transform"
}
```

#### Scene 4: Output Destinations (25-30s)

**Visual Elements**:
- Data Lake storage
- Power BI dashboards
- Alert notifications

**Animation**:

```json
{
  "time": "25-30s",
  "elements": [
    {
      "type": "Destinations",
      "items": ["Data_Lake", "Power_BI", "Alerts"],
      "animation": "fan_out",
      "stagger": "0.5s"
    }
  ],
  "transition": "distribute"
}
```

## ETL Pipeline Visualization

### Specification

**Duration**: 45 seconds
**Format**: SVG Animation
**Frame Rate**: 30 fps
**Dimensions**: 1920x1080

### Animation Code

```svg
<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Define gradients for data flow -->
    <linearGradient id="dataFlowGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#0078D4;stop-opacity:1">
        <animate attributeName="offset"
                 values="0;1;0"
                 dur="3s"
                 repeatCount="indefinite" />
      </stop>
      <stop offset="100%" style="stop-color:#00BCF2;stop-opacity:1">
        <animate attributeName="offset"
                 values="0;1;0"
                 dur="3s"
                 repeatCount="indefinite" />
      </stop>
    </linearGradient>

    <!-- Data particle definition -->
    <circle id="dataParticle" r="6" fill="url(#dataFlowGradient)">
      <animate attributeName="r"
               values="4;7;4"
               dur="1.5s"
               repeatCount="indefinite" />
    </circle>

    <!-- Arrow marker for connections -->
    <marker id="arrowhead" markerWidth="10" markerHeight="10"
            refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#0078D4" />
    </marker>
  </defs>

  <!-- Extract Phase -->
  <g id="extractPhase" transform="translate(200, 400)">
    <rect width="250" height="120" rx="15"
          fill="#E8F4FD" stroke="#0078D4" stroke-width="3">
      <animate attributeName="stroke-width"
               values="3;5;3"
               dur="2s"
               repeatCount="indefinite" />
    </rect>
    <text x="125" y="60" text-anchor="middle"
          font-family="Segoe UI" font-size="24"
          font-weight="bold" fill="#0078D4">
      Extract
    </text>

    <!-- Source icons -->
    <g id="sources">
      <circle cx="50" cy="90" r="8" fill="#0078D4">
        <animate attributeName="opacity"
                 values="0.5;1;0.5"
                 dur="1s"
                 repeatCount="indefinite" />
      </circle>
      <circle cx="125" cy="90" r="8" fill="#0078D4">
        <animate attributeName="opacity"
                 values="0.5;1;0.5"
                 dur="1s"
                 begin="0.3s"
                 repeatCount="indefinite" />
      </circle>
      <circle cx="200" cy="90" r="8" fill="#0078D4">
        <animate attributeName="opacity"
                 values="0.5;1;0.5"
                 dur="1s"
                 begin="0.6s"
                 repeatCount="indefinite" />
      </circle>
    </g>
  </g>

  <!-- Connection: Extract to Transform -->
  <path d="M 450 460 L 650 460" stroke="#0078D4"
        stroke-width="4" fill="none"
        marker-end="url(#arrowhead)">
    <animate attributeName="stroke-dasharray"
             values="0,300;300,0"
             dur="2s"
             repeatCount="indefinite"/>
  </path>

  <!-- Animated data particles -->
  <g id="flowParticles">
    <use href="#dataParticle" x="450" y="460">
      <animateMotion path="M 0,0 L 200,0"
                     dur="2s"
                     repeatCount="indefinite" />
    </use>
    <use href="#dataParticle" x="450" y="460">
      <animateMotion path="M 0,0 L 200,0"
                     dur="2s"
                     begin="0.5s"
                     repeatCount="indefinite" />
    </use>
  </g>

  <!-- Transform Phase -->
  <g id="transformPhase" transform="translate(650, 400)">
    <rect width="250" height="120" rx="15"
          fill="#E8F4FD" stroke="#0078D4" stroke-width="3">
      <animate attributeName="stroke-width"
               values="3;5;3"
               dur="2s"
               begin="0.5s"
               repeatCount="indefinite" />
    </rect>
    <text x="125" y="60" text-anchor="middle"
          font-family="Segoe UI" font-size="24"
          font-weight="bold" fill="#0078D4">
      Transform
    </text>

    <!-- Transformation gear -->
    <g transform="translate(125, 80)">
      <path d="M -25,-8 L -20,-20 L -8,-20 L 0,-8 L 8,-20 L 20,-20
               L 25,-8 L 25,8 L 20,20 L 8,20 L 0,8 L -8,20 L -20,20
               L -25,8 Z"
            fill="#0078D4" opacity="0.4">
        <animateTransform attributeName="transform"
                         type="rotate"
                         from="0" to="360"
                         dur="6s"
                         repeatCount="indefinite"/>
      </path>
    </g>
  </g>

  <!-- Connection: Transform to Load -->
  <path d="M 900 460 L 1100 460" stroke="#0078D4"
        stroke-width="4" fill="none"
        marker-end="url(#arrowhead)">
    <animate attributeName="stroke-dasharray"
             values="0,300;300,0"
             dur="2s"
             begin="1s"
             repeatCount="indefinite"/>
  </path>

  <!-- Load Phase -->
  <g id="loadPhase" transform="translate(1100, 400)">
    <rect width="250" height="120" rx="15"
          fill="#E8F4FD" stroke="#0078D4" stroke-width="3">
      <animate attributeName="stroke-width"
               values="3;5;3"
               dur="2s"
               begin="1s"
               repeatCount="indefinite" />
    </rect>
    <text x="125" y="60" text-anchor="middle"
          font-family="Segoe UI" font-size="24"
          font-weight="bold" fill="#0078D4">
      Load
    </text>

    <!-- Progress bar -->
    <rect x="30" y="80" width="190" height="15"
          fill="#E0E0E0" rx="8"/>
    <rect x="30" y="80" width="0" height="15"
          fill="#107C10" rx="8">
      <animate attributeName="width"
               values="0;190;0"
               dur="4s"
               repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- Timeline indicator -->
  <g id="timeline" transform="translate(200, 900)">
    <line x1="0" y1="0" x2="1150" y2="0"
          stroke="#C0C0C0" stroke-width="2"/>
    <text x="0" y="30" font-family="Segoe UI"
          font-size="16" fill="#666">0s</text>
    <text x="380" y="30" font-family="Segoe UI"
          font-size="16" fill="#666">15s</text>
    <text x="760" y="30" font-family="Segoe UI"
          font-size="16" fill="#666">30s</text>
    <text x="1130" y="30" font-family="Segoe UI"
          font-size="16" fill="#666">45s</text>
  </g>
</svg>
```

## Batch Processing Flow

### Specification

**Duration**: 40 seconds
**Format**: Canvas Animation (HTML5)
**Frame Rate**: 60 fps

### JavaScript Implementation

```javascript
class BatchProcessingAnimation {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.width = 1920;
    this.height = 1080;
    this.canvas.width = this.width;
    this.canvas.height = this.height;

    this.batches = [];
    this.processors = [];
    this.initializeComponents();
    this.animate();
  }

  initializeComponents() {
    // Create batch queues
    for (let i = 0; i < 3; i++) {
      this.batches.push({
        x: 100,
        y: 200 + (i * 200),
        width: 150,
        height: 80,
        progress: 0,
        status: 'queued'
      });
    }

    // Create processing nodes
    for (let i = 0; i < 4; i++) {
      this.processors.push({
        x: 500 + (i * 250),
        y: 400,
        radius: 50,
        active: false,
        load: 0
      });
    }
  }

  drawBatch(batch) {
    this.ctx.save();

    // Batch container
    this.ctx.fillStyle = '#E8F4FD';
    this.ctx.strokeStyle = batch.status === 'processing'
      ? '#107C10' : '#0078D4';
    this.ctx.lineWidth = 3;
    this.ctx.fillRect(batch.x, batch.y, batch.width, batch.height);
    this.ctx.strokeRect(batch.x, batch.y, batch.width, batch.height);

    // Progress bar
    if (batch.progress > 0) {
      this.ctx.fillStyle = '#107C10';
      this.ctx.fillRect(
        batch.x + 10,
        batch.y + batch.height - 20,
        (batch.width - 20) * batch.progress,
        10
      );
    }

    // Batch label
    this.ctx.fillStyle = '#000';
    this.ctx.font = '18px Segoe UI';
    this.ctx.textAlign = 'center';
    this.ctx.fillText(
      `Batch ${this.batches.indexOf(batch) + 1}`,
      batch.x + batch.width / 2,
      batch.y + 30
    );

    this.ctx.restore();
  }

  drawProcessor(processor, index) {
    this.ctx.save();

    // Outer glow for active processors
    if (processor.active) {
      this.ctx.beginPath();
      this.ctx.arc(
        processor.x,
        processor.y,
        processor.radius + 5,
        0,
        Math.PI * 2
      );
      this.ctx.fillStyle = '#0078D444';
      this.ctx.fill();
    }

    // Main circle
    this.ctx.beginPath();
    this.ctx.arc(
      processor.x,
      processor.y,
      processor.radius,
      0,
      Math.PI * 2
    );
    this.ctx.fillStyle = processor.active ? '#0078D4' : '#E0E0E0';
    this.ctx.fill();
    this.ctx.strokeStyle = '#0078D4';
    this.ctx.lineWidth = 3;
    this.ctx.stroke();

    // Load indicator
    if (processor.load > 0) {
      this.ctx.beginPath();
      this.ctx.arc(
        processor.x,
        processor.y,
        processor.radius - 10,
        -Math.PI / 2,
        (-Math.PI / 2) + (Math.PI * 2 * processor.load),
        false
      );
      this.ctx.strokeStyle = '#107C10';
      this.ctx.lineWidth = 8;
      this.ctx.stroke();
    }

    // Label
    this.ctx.fillStyle = processor.active ? '#FFF' : '#666';
    this.ctx.font = '16px Segoe UI';
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'middle';
    this.ctx.fillText(`Node ${index + 1}`, processor.x, processor.y);

    this.ctx.restore();
  }

  updateBatches() {
    this.batches.forEach((batch, index) => {
      if (batch.status === 'processing') {
        batch.progress += 0.005;
        if (batch.progress >= 1) {
          batch.status = 'completed';
          batch.progress = 1;
        }
      } else if (batch.status === 'queued' && index === 0) {
        // Start processing first queued batch
        batch.status = 'processing';
      }
    });
  }

  updateProcessors() {
    this.processors.forEach((processor, index) => {
      // Simulate processor activity
      const activeBatch = this.batches.find(b => b.status === 'processing');
      processor.active = !!activeBatch;

      if (processor.active) {
        processor.load = activeBatch.progress;
      } else {
        processor.load = 0;
      }
    });
  }

  drawConnections() {
    // Draw connections from batches to processors
    this.batches.forEach(batch => {
      if (batch.status === 'processing') {
        this.processors.forEach(processor => {
          this.ctx.save();
          this.ctx.strokeStyle = '#0078D440';
          this.ctx.lineWidth = 2;
          this.ctx.setLineDash([5, 5]);
          this.ctx.beginPath();
          this.ctx.moveTo(batch.x + batch.width, batch.y + batch.height / 2);
          this.ctx.lineTo(processor.x - processor.radius, processor.y);
          this.ctx.stroke();
          this.ctx.restore();
        });
      }
    });
  }

  animate() {
    // Clear canvas
    this.ctx.clearRect(0, 0, this.width, this.height);

    // Update state
    this.updateBatches();
    this.updateProcessors();

    // Draw components
    this.drawConnections();
    this.batches.forEach(batch => this.drawBatch(batch));
    this.processors.forEach((processor, index) =>
      this.drawProcessor(processor, index)
    );

    // Continue animation
    requestAnimationFrame(() => this.animate());
  }
}

// Initialize animation when page loads
window.addEventListener('DOMContentLoaded', () => {
  new BatchProcessingAnimation('batchProcessingCanvas');
});
```

## Delta Lake Change Data Capture

### Specification

**Duration**: 35 seconds
**Format**: Lottie JSON
**Complexity**: Advanced

### Storyboard

#### Phase 1: Source Change Detection (0-10s)

- Source database shows INSERT, UPDATE, DELETE operations
- Change log captured in real-time
- Transaction markers displayed

#### Phase 2: CDC Processing (10-20s)

- Change events flow to processing layer
- Schema validation
- Conflict resolution

#### Phase 3: Delta Lake Write (20-30s)

- Changes written to Delta table
- Transaction log updated
- Version increment shown

#### Phase 4: Consumers Update (30-35s)

- Downstream systems receive updates
- Materialized views refresh
- Analytics queries reflect changes

## Performance Metrics

### Animation Performance Standards

| Metric | Target | Acceptable | Notes |
|:-------|:-------|:-----------|:------|
| **Frame Rate** | 60 fps | 30 fps | Smooth playback |
| **Load Time** | < 1s | < 2s | Initial render |
| **File Size** | < 2MB | < 5MB | Network efficiency |
| **CPU Usage** | < 30% | < 50% | During playback |
| **Memory** | < 100MB | < 200MB | Peak usage |

### Optimization Techniques

```javascript
// Throttle animation updates for performance
class OptimizedAnimation {
  constructor() {
    this.lastFrame = 0;
    this.targetFPS = 60;
    this.frameInterval = 1000 / this.targetFPS;
  }

  animate(timestamp) {
    const delta = timestamp - this.lastFrame;

    if (delta >= this.frameInterval) {
      this.lastFrame = timestamp - (delta % this.frameInterval);
      this.update();
      this.render();
    }

    requestAnimationFrame((t) => this.animate(t));
  }

  update() {
    // Update animation state
  }

  render() {
    // Render current frame
  }
}
```

## Accessibility Features

### Reduced Motion Support

```javascript
// Respect user motion preferences
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

if (prefersReducedMotion) {
  // Show static diagram instead
  showStaticVersion();
} else {
  // Show animated version
  startAnimation();
}
```

### Alternative Text Descriptions

All data flow animations include:

- Comprehensive alt text describing the flow
- Step-by-step text breakdown
- Interactive pause/play controls
- Keyboard navigation support

### Screen Reader Support

```html
<div role="img" aria-label="Data flow animation showing ETL process">
  <svg aria-hidden="true">
    <!-- Animation content -->
  </svg>
  <div class="sr-only">
    <p>Data flows from source systems through three phases:</p>
    <ol>
      <li>Extract: Data is extracted from multiple sources</li>
      <li>Transform: Data is cleaned and transformed</li>
      <li>Load: Data is loaded into the data warehouse</li>
    </ol>
  </div>
</div>
```

## Testing and Validation

### Animation Testing Checklist

- [ ] Plays smoothly at target frame rate
- [ ] Loops seamlessly (if applicable)
- [ ] File size within limits
- [ ] Works across browsers (Chrome, Firefox, Safari, Edge)
- [ ] Responsive on mobile devices
- [ ] Reduced motion alternative tested
- [ ] Keyboard controls functional
- [ ] Screen reader compatible

### Browser Compatibility

| Browser | Version | Status | Notes |
|:--------|:--------|:-------|:------|
| **Chrome** | 90+ | ✅ Full Support | Best performance |
| **Firefox** | 88+ | ✅ Full Support | Good performance |
| **Safari** | 14+ | ✅ Full Support | WebKit optimized |
| **Edge** | 90+ | ✅ Full Support | Chromium-based |
| **Mobile Safari** | 14+ | ✅ Full Support | Touch optimized |
| **Chrome Mobile** | 90+ | ✅ Full Support | Touch optimized |

## Resources

- [Lottie Animation Guidelines](lottie-animations.md)
- [SVG Animation Specifications](svg-animations.md)
- [Performance Optimization](performance-optimization.md)
- [Animation Best Practices](animation-guidelines.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
