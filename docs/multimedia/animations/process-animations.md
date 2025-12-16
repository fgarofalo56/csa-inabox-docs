# Process Flow Animations

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎨 [Animations](README.md)** | **🔄 Process Animations**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: Lottie/SVG](https://img.shields.io/badge/Type-Lottie%2FSVG-blue)
![Duration: 30-50s](https://img.shields.io/badge/Duration-30--50s-purple)

## Overview

Process flow animations demonstrate step-by-step workflows, decision trees, and operational procedures within Azure Synapse Analytics. These animations help users understand complex processes and best practices.

## Data Ingestion Workflow

### Specification

**Duration**: 40 seconds
**Format**: Lottie JSON
**Complexity**: Intermediate

### Workflow Steps

#### Step 1: Source Connection (0-8s)

```json
{
  "step": "source_connection",
  "duration": 8,
  "elements": [
    {
      "type": "database_icon",
      "animation": "appear_with_bounce",
      "position": { "x": 100, "y": 400 }
    },
    {
      "type": "connection_line",
      "animation": "draw_from_left",
      "style": "dashed",
      "color": "#0078D4"
    }
  ]
}
```

#### Step 2: Data Extraction (8-16s)

```json
{
  "step": "extraction",
  "duration": 8,
  "elements": [
    {
      "type": "data_packet",
      "animation": "pulse_and_move",
      "count": 10,
      "speed": "variable"
    },
    {
      "type": "progress_bar",
      "animation": "fill_horizontal",
      "color": "#107C10"
    }
  ]
}
```

#### Step 3: Validation (16-24s)

```json
{
  "step": "validation",
  "duration": 8,
  "elements": [
    {
      "type": "checkpoint",
      "icon": "shield_check",
      "animation": "validate_items",
      "success_rate": 0.95
    },
    {
      "type": "error_notification",
      "animation": "shake_if_error",
      "color": "#D13438"
    }
  ]
}
```

#### Step 4: Transformation (24-32s)

```json
{
  "step": "transformation",
  "duration": 8,
  "elements": [
    {
      "type": "transform_box",
      "icon": "settings_gear",
      "animation": "rotate_and_process",
      "operations": ["clean", "enrich", "format"]
    }
  ]
}
```

#### Step 5: Loading (32-36s)

```json
{
  "step": "loading",
  "duration": 4,
  "elements": [
    {
      "type": "data_lake",
      "animation": "fill_with_data",
      "final_state": "complete"
    }
  ]
}
```

#### Step 6: Verification (36-40s)

```json
{
  "step": "verification",
  "duration": 4,
  "elements": [
    {
      "type": "checkmark",
      "animation": "draw_checkmark",
      "color": "#107C10",
      "size": "large"
    },
    {
      "type": "completion_message",
      "text": "Ingestion Complete",
      "animation": "fade_in"
    }
  ]
}
```

## Pipeline Execution Flow

### Specification

**Duration**: 50 seconds
**Format**: SVG Animation
**Frame Rate**: 60 fps

### Implementation

```javascript
class PipelineExecutionAnimation {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.stages = [
      { name: 'Trigger', duration: 5, color: '#0078D4' },
      { name: 'Copy Data', duration: 15, color: '#00BCF2' },
      { name: 'Transform', duration: 12, color: '#50E6FF' },
      { name: 'Load', duration: 10, color: '#107C10' },
      { name: 'Validate', duration: 8, color: '#10893E' }
    ];
    this.currentStage = 0;
    this.stageProgress = 0;
    this.init();
  }

  init() {
    this.renderPipeline();
    this.animate();
  }

  renderPipeline() {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 1200 600');
    svg.setAttribute('width', '100%');
    svg.setAttribute('height', '100%');

    this.stages.forEach((stage, index) => {
      const g = this.createStageElement(stage, index);
      svg.appendChild(g);

      if (index < this.stages.length - 1) {
        const connector = this.createConnector(index);
        svg.appendChild(connector);
      }
    });

    this.container.appendChild(svg);
  }

  createStageElement(stage, index) {
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    const x = 100 + (index * 220);
    const y = 250;

    // Stage box
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', x);
    rect.setAttribute('y', y);
    rect.setAttribute('width', '150');
    rect.setAttribute('height', '100');
    rect.setAttribute('rx', '10');
    rect.setAttribute('fill', '#F0F0F0');
    rect.setAttribute('stroke', stage.color);
    rect.setAttribute('stroke-width', '3');
    rect.setAttribute('class', `stage-${index}`);
    g.appendChild(rect);

    // Stage label
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', x + 75);
    text.setAttribute('y', y + 40);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('font-family', 'Segoe UI');
    text.setAttribute('font-size', '16');
    text.setAttribute('font-weight', 'bold');
    text.textContent = stage.name;
    g.appendChild(text);

    // Progress bar
    const progressBg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    progressBg.setAttribute('x', x + 10);
    progressBg.setAttribute('y', y + 70);
    progressBg.setAttribute('width', '130');
    progressBg.setAttribute('height', '10');
    progressBg.setAttribute('rx', '5');
    progressBg.setAttribute('fill', '#E0E0E0');
    g.appendChild(progressBg);

    const progress = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    progress.setAttribute('x', x + 10);
    progress.setAttribute('y', y + 70);
    progress.setAttribute('width', '0');
    progress.setAttribute('height', '10');
    progress.setAttribute('rx', '5');
    progress.setAttribute('fill', stage.color);
    progress.setAttribute('class', `progress-${index}`);
    g.appendChild(progress);

    return g;
  }

  createConnector(index) {
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    const x1 = 250 + (index * 220);
    const x2 = 320 + (index * 220);
    line.setAttribute('x1', x1);
    line.setAttribute('y1', '300');
    line.setAttribute('x2', x2);
    line.setAttribute('y2', '300');
    line.setAttribute('stroke', '#C0C0C0');
    line.setAttribute('stroke-width', '2');
    line.setAttribute('stroke-dasharray', '5,5');
    line.setAttribute('class', `connector-${index}`);
    return line;
  }

  animate() {
    const updateInterval = 50; // ms
    const progressPerUpdate = updateInterval / (this.stages[this.currentStage].duration * 1000);

    const interval = setInterval(() => {
      this.stageProgress += progressPerUpdate;

      // Update progress bar
      const progressBar = document.querySelector(`.progress-${this.currentStage}`);
      if (progressBar) {
        progressBar.setAttribute('width', Math.min(this.stageProgress * 130, 130));
      }

      // Highlight active stage
      const stageBox = document.querySelector(`.stage-${this.currentStage}`);
      if (stageBox) {
        stageBox.setAttribute('fill', this.stages[this.currentStage].color + '33');
      }

      if (this.stageProgress >= 1) {
        // Complete current stage
        this.completeStage(this.currentStage);

        // Move to next stage
        this.currentStage++;
        this.stageProgress = 0;

        if (this.currentStage >= this.stages.length) {
          clearInterval(interval);
          this.onComplete();
        }
      }
    }, updateInterval);
  }

  completeStage(index) {
    const stageBox = document.querySelector(`.stage-${index}`);
    if (stageBox) {
      stageBox.setAttribute('fill', this.stages[index].color + '66');
    }

    // Animate connector
    const connector = document.querySelector(`.connector-${index}`);
    if (connector) {
      connector.setAttribute('stroke', this.stages[index].color);
      connector.setAttribute('stroke-width', '4');
      connector.setAttribute('stroke-dasharray', '0');
    }
  }

  onComplete() {
    // Show completion message
    const svg = this.container.querySelector('svg');
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', '600');
    text.setAttribute('y', '500');
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('font-family', 'Segoe UI');
    text.setAttribute('font-size', '24');
    text.setAttribute('font-weight', 'bold');
    text.setAttribute('fill', '#107C10');
    text.textContent = 'Pipeline Execution Complete ✓';
    svg.appendChild(text);
  }
}
```

## Deployment Workflow

### Specification

**Duration**: 45 seconds
**Format**: HTML/CSS Animation

### Workflow Stages

**Stage 1: Build (0-12s)**
- Code compilation
- Dependency resolution
- Unit tests execution
- Artifact packaging

**Stage 2: Test (12-24s)**
- Integration tests
- Performance tests
- Security scanning
- Quality gates

**Stage 3: Deploy (24-36s)**
- Infrastructure provisioning
- Application deployment
- Configuration updates
- Health checks

**Stage 4: Verify (36-45s)**
- Smoke tests
- Monitoring setup
- Rollback readiness
- Success notification

## Decision Tree Animation

### Specification

**Duration**: 35 seconds
**Format**: SVG with JavaScript

### Implementation

```javascript
class DecisionTreeAnimation {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.nodes = [
      { id: 0, label: 'Start', x: 600, y: 50, type: 'start' },
      { id: 1, label: 'Data Available?', x: 600, y: 150, type: 'decision' },
      { id: 2, label: 'Validate Schema', x: 400, y: 300, type: 'process' },
      { id: 3, label: 'Wait for Data', x: 800, y: 300, type: 'process' },
      { id: 4, label: 'Schema Valid?', x: 400, y: 450, type: 'decision' },
      { id: 5, label: 'Transform', x: 250, y: 600, type: 'process' },
      { id: 6, label: 'Log Error', x: 550, y: 600, type: 'process' },
      { id: 7, label: 'Load to Lake', x: 250, y: 750, type: 'process' },
      { id: 8, label: 'Complete', x: 250, y: 900, type: 'end' }
    ];

    this.edges = [
      { from: 0, to: 1, label: '' },
      { from: 1, to: 2, label: 'Yes' },
      { from: 1, to: 3, label: 'No' },
      { from: 2, to: 4, label: '' },
      { from: 4, to: 5, label: 'Yes' },
      { from: 4, to: 6, label: 'No' },
      { from: 5, to: 7, label: '' },
      { from: 7, to: 8, label: '' }
    ];

    this.currentStep = 0;
    this.init();
  }

  init() {
    this.render();
    this.animate();
  }

  render() {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 1200 1000');
    svg.setAttribute('width', '100%');
    svg.setAttribute('height', '100%');

    // Render edges
    this.edges.forEach((edge, index) => {
      const g = this.createEdge(edge, index);
      svg.appendChild(g);
    });

    // Render nodes
    this.nodes.forEach((node, index) => {
      const g = this.createNode(node, index);
      svg.appendChild(g);
    });

    this.container.appendChild(svg);
  }

  createNode(node, index) {
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('class', `node-${index}`);
    g.setAttribute('opacity', '0.3');

    let shape;
    if (node.type === 'start' || node.type === 'end') {
      shape = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      shape.setAttribute('cx', node.x);
      shape.setAttribute('cy', node.y);
      shape.setAttribute('r', '40');
    } else if (node.type === 'decision') {
      shape = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
      const points = `${node.x},${node.y - 50} ${node.x + 50},${node.y} ${node.x},${node.y + 50} ${node.x - 50},${node.y}`;
      shape.setAttribute('points', points);
    } else {
      shape = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      shape.setAttribute('x', node.x - 60);
      shape.setAttribute('y', node.y - 30);
      shape.setAttribute('width', '120');
      shape.setAttribute('height', '60');
      shape.setAttribute('rx', '8');
    }

    shape.setAttribute('fill', '#E8F4FD');
    shape.setAttribute('stroke', '#0078D4');
    shape.setAttribute('stroke-width', '3');
    g.appendChild(shape);

    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', node.x);
    text.setAttribute('y', node.y + 5);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('font-family', 'Segoe UI');
    text.setAttribute('font-size', '14');
    text.setAttribute('font-weight', 'bold');
    text.textContent = node.label;
    g.appendChild(text);

    return g;
  }

  createEdge(edge, index) {
    const fromNode = this.nodes[edge.from];
    const toNode = this.nodes[edge.to];

    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('class', `edge-${index}`);
    g.setAttribute('opacity', '0.3');

    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', fromNode.x);
    line.setAttribute('y1', fromNode.y + 50);
    line.setAttribute('x2', toNode.x);
    line.setAttribute('y2', toNode.y - 50);
    line.setAttribute('stroke', '#0078D4');
    line.setAttribute('stroke-width', '2');
    line.setAttribute('marker-end', 'url(#arrowhead)');
    g.appendChild(line);

    if (edge.label) {
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', (fromNode.x + toNode.x) / 2);
      text.setAttribute('y', (fromNode.y + toNode.y) / 2);
      text.setAttribute('text-anchor', 'middle');
      text.setAttribute('font-family', 'Segoe UI');
      text.setAttribute('font-size', '12');
      text.setAttribute('fill', '#666');
      text.textContent = edge.label;
      g.appendChild(text);
    }

    return g;
  }

  animate() {
    const path = [0, 1, 2, 4, 5, 7, 8]; // Successful path
    let stepIndex = 0;

    const stepInterval = setInterval(() => {
      if (stepIndex >= path.length) {
        clearInterval(stepInterval);
        return;
      }

      const nodeIndex = path[stepIndex];
      const node = document.querySelector(`.node-${nodeIndex}`);
      if (node) {
        node.setAttribute('opacity', '1');
      }

      // Highlight connecting edge
      if (stepIndex > 0) {
        const edgeIndex = this.edges.findIndex(
          e => e.from === path[stepIndex - 1] && e.to === nodeIndex
        );
        const edge = document.querySelector(`.edge-${edgeIndex}`);
        if (edge) {
          edge.setAttribute('opacity', '1');
        }
      }

      stepIndex++;
    }, 3000);
  }
}
```

## Performance Monitoring

All process animations include:
- Step completion indicators
- Progress bars
- Time elapsed counters
- Error state handling
- Success/failure outcomes

## Accessibility Features

- Keyboard navigation through steps
- Screen reader announcements for each stage
- Reduced motion alternatives
- High contrast mode support
- Focus indicators

## Resources

- [Animation Guidelines](animation-guidelines.md)
- [Interactive Diagrams](interactive-diagrams.md)
- [Loading Animations](loading-animations.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
