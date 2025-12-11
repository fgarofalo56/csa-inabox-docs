# Architecture Diagram Animations

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎨 [Animations](README.md)** | **🏗️ Architecture Animations**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: SVG/GSAP](https://img.shields.io/badge/Type-SVG%2FGSAP-blue)
![Duration: 60-90s](https://img.shields.io/badge/Duration-60--90s-purple)

## Overview

Architecture animations bring static diagrams to life, showing how components interact, scale, and evolve over time. These animations help stakeholders understand complex system architectures and design decisions.

## Synapse Architecture Evolution

### Specification

**Duration**: 90 seconds
**Format**: SVG + GSAP Timeline
**Frame Rate**: 60 fps
**Dimensions**: 1920x1080

### Animation Timeline

#### Phase 1: Basic Setup (0-20s)

**Components Introduced**:
- Single Synapse workspace
- Azure Data Lake Storage Gen2
- Basic SQL pool

**Animation Code**:

```javascript
const architectureTimeline = gsap.timeline({
  defaults: { ease: 'power2.out', duration: 1 }
});

// Phase 1: Foundation
architectureTimeline
  .from('#workspace', {
    scale: 0,
    opacity: 0,
    transformOrigin: 'center'
  })
  .from('#dataLake', {
    x: -200,
    opacity: 0
  }, '-=0.5')
  .from('#sqlPool', {
    y: 200,
    opacity: 0
  }, '-=0.5')
  .to('#connectionLines .foundation', {
    drawSVG: '0% 100%',
    duration: 1.5
  });
```

#### Phase 2: Adding Spark Pools (20-40s)

**New Components**:
- Apache Spark pools
- Notebook support
- Distributed processing

**Animation Code**:

```javascript
// Phase 2: Spark Integration
architectureTimeline
  .from('#sparkPools', {
    scale: 0,
    opacity: 0,
    stagger: 0.2
  })
  .to('#sparkPools .node', {
    scale: [1, 1.1, 1],
    duration: 0.5,
    stagger: 0.1,
    repeat: 2
  })
  .to('#connectionLines .spark', {
    drawSVG: '0% 100%',
    duration: 1
  });
```

#### Phase 3: Integration Layer (40-60s)

**New Components**:
- Azure Data Factory pipelines
- External data sources
- Integration runtime

**Animation Code**:

```javascript
// Phase 3: Integration
architectureTimeline
  .from('#dataFactory', {
    x: -300,
    opacity: 0
  })
  .from('#dataSources', {
    x: -400,
    opacity: 0,
    stagger: 0.15
  }, '-=0.5')
  .to('#dataFlow', {
    strokeDashoffset: 0,
    duration: 2,
    stagger: 0.2
  });
```

#### Phase 4: Analytics and BI (60-75s)

**New Components**:
- Power BI integration
- Serverless SQL pools
- External tables

**Animation Code**:

```javascript
// Phase 4: Analytics Layer
architectureTimeline
  .from('#serverlessSql', {
    y: -200,
    opacity: 0
  })
  .from('#powerBi', {
    x: 300,
    opacity: 0,
    rotation: -45
  }, '-=0.5')
  .to('#analyticsConnections', {
    drawSVG: '0% 100%',
    duration: 1.5
  });
```

#### Phase 5: Security and Governance (75-90s)

**New Components**:
- Azure AD integration
- Managed identities
- Network security groups
- Private endpoints

**Animation Code**:

```javascript
// Phase 5: Security Layer
architectureTimeline
  .from('#securityShield', {
    scale: 3,
    opacity: 0
  })
  .to('#securityShield', {
    opacity: 0.3,
    duration: 2
  })
  .from('.securityComponent', {
    scale: 0,
    opacity: 0,
    stagger: 0.2
  }, '-=1.5')
  .to('.lockIcon', {
    rotation: 360,
    duration: 1,
    ease: 'elastic.out(1, 0.5)'
  });
```

## Scaling Architecture Animation

### Specification

**Duration**: 60 seconds
**Format**: HTML/CSS/JavaScript
**Animation Library**: Anime.js

### HTML Structure

```html
<div class="architecture-container">
  <div class="stage stage-1">
    <div class="server single-server">Single Server</div>
  </div>

  <div class="stage stage-2">
    <div class="server-cluster">
      <div class="server">Server 1</div>
      <div class="server">Server 2</div>
      <div class="server">Server 3</div>
    </div>
    <div class="load-balancer">Load Balancer</div>
  </div>

  <div class="stage stage-3">
    <div class="server-cluster">
      <div class="server">Server 1</div>
      <div class="server">Server 2</div>
      <div class="server">Server 3</div>
    </div>
    <div class="load-balancer">Load Balancer</div>
    <div class="cache-layer">Redis Cache</div>
  </div>

  <div class="stage stage-4">
    <div class="region region-west">
      <div class="server-cluster">West US</div>
    </div>
    <div class="region region-east">
      <div class="server-cluster">East US</div>
    </div>
    <div class="traffic-manager">Traffic Manager</div>
  </div>
</div>
```

### CSS Styling

```css
.architecture-container {
  width: 1920px;
  height: 1080px;
  position: relative;
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
  overflow: hidden;
}

.stage {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 40px;
}

.server {
  width: 200px;
  height: 120px;
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-family: 'Segoe UI', sans-serif;
  font-size: 18px;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.server:hover {
  transform: translateY(-5px);
}

.server-cluster {
  display: flex;
  gap: 30px;
  flex-wrap: wrap;
  justify-content: center;
}

.load-balancer {
  width: 300px;
  height: 80px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.cache-layer {
  width: 250px;
  height: 80px;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.region {
  padding: 40px;
  border: 3px dashed rgba(255, 255, 255, 0.5);
  border-radius: 20px;
  margin: 20px;
}

.traffic-manager {
  width: 350px;
  height: 100px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 22px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}
```

### Animation Script

```javascript
class ScalingArchitectureAnimation {
  constructor() {
    this.currentStage = 0;
    this.stages = document.querySelectorAll('.stage');
    this.init();
  }

  init() {
    this.animateTimeline();
  }

  animateTimeline() {
    const timeline = anime.timeline({
      easing: 'easeOutExpo',
      duration: 1500
    });

    // Stage 1: Single Server (0-10s)
    timeline
      .add({
        targets: '.stage-1',
        opacity: [0, 1],
        duration: 1000
      })
      .add({
        targets: '.stage-1 .server',
        scale: [0, 1],
        rotate: [180, 0],
        duration: 1500,
        delay: 500
      })
      .add({
        targets: '.stage-1',
        opacity: [1, 0],
        duration: 1000,
        delay: 8000
      });

    // Stage 2: Load Balanced Cluster (10-25s)
    timeline
      .add({
        targets: '.stage-2',
        opacity: [0, 1],
        duration: 1000
      })
      .add({
        targets: '.stage-2 .load-balancer',
        translateY: [-100, 0],
        opacity: [0, 1],
        duration: 1500
      })
      .add({
        targets: '.stage-2 .server',
        scale: [0, 1],
        translateY: [100, 0],
        opacity: [0, 1],
        delay: anime.stagger(200),
        duration: 1000
      })
      .add({
        targets: '.stage-2',
        opacity: [1, 0],
        duration: 1000,
        delay: 12000
      });

    // Stage 3: With Caching Layer (25-45s)
    timeline
      .add({
        targets: '.stage-3',
        opacity: [0, 1],
        duration: 1000
      })
      .add({
        targets: '.stage-3 .load-balancer',
        translateY: [-100, 0],
        opacity: [0, 1],
        duration: 1000
      })
      .add({
        targets: '.stage-3 .server',
        scale: [0, 1],
        translateY: [100, 0],
        opacity: [0, 1],
        delay: anime.stagger(200),
        duration: 1000
      })
      .add({
        targets: '.stage-3 .cache-layer',
        scale: [0, 1],
        opacity: [0, 1],
        duration: 1500,
        delay: 500
      })
      .add({
        targets: '.stage-3',
        opacity: [1, 0],
        duration: 1000,
        delay: 17000
      });

    // Stage 4: Global Distribution (45-60s)
    timeline
      .add({
        targets: '.stage-4',
        opacity: [0, 1],
        duration: 1000
      })
      .add({
        targets: '.stage-4 .traffic-manager',
        scale: [0, 1],
        rotate: [0, 360],
        opacity: [0, 1],
        duration: 2000
      })
      .add({
        targets: '.stage-4 .region-west',
        translateX: [-300, 0],
        opacity: [0, 1],
        duration: 1500
      })
      .add({
        targets: '.stage-4 .region-east',
        translateX: [300, 0],
        opacity: [0, 1],
        duration: 1500,
        offset: '-=1500'
      })
      .add({
        targets: '.stage-4 .server-cluster',
        scale: [0, 1],
        opacity: [0, 1],
        delay: anime.stagger(300),
        duration: 1000
      });

    timeline.play();
  }
}

// Initialize when page loads
window.addEventListener('DOMContentLoaded', () => {
  new ScalingArchitectureAnimation();
});
```

## Hybrid Architecture Animation

### Specification

**Duration**: 75 seconds
**Format**: SVG with Three.js integration
**Complexity**: Advanced

### Storyboard

#### Scene 1: On-Premises Environment (0-15s)

- Traditional data center infrastructure
- Legacy databases and applications
- Physical servers and storage

#### Scene 2: Cloud Connection (15-30s)

- VPN gateway established
- ExpressRoute connection animated
- Hybrid connectivity highlighted

#### Scene 3: Cloud Services Integration (30-50s)

- Azure Synapse workspace activated
- Data synchronization flows
- Hybrid queries demonstrated

#### Scene 4: Complete Hybrid Solution (50-75s)

- Full architecture view
- Data flow visualization
- Security boundaries shown

## Microservices Architecture

### Specification

**Duration**: 60 seconds
**Format**: Canvas + WebGL
**Particle System**: Custom

### Implementation

```javascript
class MicroservicesArchitecture {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.width = 1920;
    this.height = 1080;
    this.services = [];
    this.connections = [];
    this.messages = [];

    this.initServices();
    this.animate();
  }

  initServices() {
    const serviceTypes = [
      { name: 'API Gateway', x: 960, y: 200, type: 'gateway' },
      { name: 'Auth Service', x: 600, y: 400, type: 'service' },
      { name: 'User Service', x: 960, y: 400, type: 'service' },
      { name: 'Data Service', x: 1320, y: 400, type: 'service' },
      { name: 'Analytics', x: 750, y: 650, type: 'service' },
      { name: 'Reporting', x: 1170, y: 650, type: 'service' },
      { name: 'Database', x: 480, y: 850, type: 'storage' },
      { name: 'Cache', x: 960, y: 850, type: 'storage' },
      { name: 'Queue', x: 1440, y: 850, type: 'storage' }
    ];

    serviceTypes.forEach(config => {
      this.services.push(new MicroserviceNode(config));
    });

    this.createConnections();
  }

  createConnections() {
    // Define service dependencies
    const dependencies = [
      [0, 1], [0, 2], [0, 3], // Gateway to services
      [1, 6], [2, 6], [3, 7], // Services to storage
      [2, 4], [3, 5], // Services to analytics
      [4, 8], [5, 8] // Analytics to queue
    ];

    dependencies.forEach(([from, to]) => {
      this.connections.push({
        from: this.services[from],
        to: this.services[to],
        active: false,
        particles: []
      });
    });
  }

  simulateTraffic() {
    // Randomly create messages between services
    if (Math.random() < 0.05) {
      const conn = this.connections[
        Math.floor(Math.random() * this.connections.length)
      ];
      this.messages.push(new ServiceMessage(conn.from, conn.to));
    }
  }

  drawConnection(conn) {
    this.ctx.save();
    this.ctx.strokeStyle = conn.active ? '#0078D4' : '#E0E0E0';
    this.ctx.lineWidth = conn.active ? 3 : 1;
    this.ctx.setLineDash(conn.active ? [] : [5, 5]);

    this.ctx.beginPath();
    this.ctx.moveTo(conn.from.x, conn.from.y);
    this.ctx.lineTo(conn.to.x, conn.to.y);
    this.ctx.stroke();

    this.ctx.restore();
  }

  animate() {
    this.ctx.clearRect(0, 0, this.width, this.height);

    // Draw connections
    this.connections.forEach(conn => this.drawConnection(conn));

    // Draw services
    this.services.forEach(service => {
      service.update();
      service.draw(this.ctx);
    });

    // Simulate and draw messages
    this.simulateTraffic();
    this.messages = this.messages.filter(msg => {
      msg.update();
      msg.draw(this.ctx);
      return !msg.completed;
    });

    requestAnimationFrame(() => this.animate());
  }
}

class MicroserviceNode {
  constructor({ name, x, y, type }) {
    this.name = name;
    this.x = x;
    this.y = y;
    this.type = type;
    this.radius = type === 'gateway' ? 60 : 50;
    this.color = this.getColorForType(type);
    this.pulsePhase = Math.random() * Math.PI * 2;
    this.load = 0;
  }

  getColorForType(type) {
    const colors = {
      gateway: '#0078D4',
      service: '#00BCF2',
      storage: '#107C10'
    };
    return colors[type] || '#666666';
  }

  update() {
    this.pulsePhase += 0.05;
    // Simulate varying load
    this.load = 0.3 + (Math.sin(this.pulsePhase) * 0.3);
  }

  draw(ctx) {
    ctx.save();

    // Outer glow (pulsing)
    const pulse = Math.sin(this.pulsePhase) * 8;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius + pulse, 0, Math.PI * 2);
    ctx.fillStyle = this.color + '33';
    ctx.fill();

    // Main circle
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.fill();
    ctx.strokeStyle = '#FFF';
    ctx.lineWidth = 3;
    ctx.stroke();

    // Load indicator (inner arc)
    ctx.beginPath();
    ctx.arc(
      this.x,
      this.y,
      this.radius - 10,
      -Math.PI / 2,
      -Math.PI / 2 + (Math.PI * 2 * this.load),
      false
    );
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
    ctx.lineWidth = 6;
    ctx.stroke();

    // Label
    ctx.fillStyle = '#FFF';
    ctx.font = 'bold 14px Segoe UI';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(this.name, this.x, this.y);

    ctx.restore();
  }
}

class ServiceMessage {
  constructor(from, to) {
    this.from = from;
    this.to = to;
    this.progress = 0;
    this.speed = 0.02;
    this.completed = false;
  }

  update() {
    this.progress += this.speed;
    if (this.progress >= 1) {
      this.completed = true;
    }
  }

  draw(ctx) {
    const x = this.from.x + (this.to.x - this.from.x) * this.progress;
    const y = this.from.y + (this.to.y - this.from.y) * this.progress;

    ctx.save();

    // Message packet
    ctx.beginPath();
    ctx.arc(x, y, 8, 0, Math.PI * 2);
    ctx.fillStyle = '#FFB900';
    ctx.fill();
    ctx.strokeStyle = '#FFF';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Trail
    ctx.beginPath();
    ctx.moveTo(this.from.x, this.from.y);
    ctx.lineTo(x, y);
    ctx.strokeStyle = 'rgba(255, 185, 0, 0.3)';
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.restore();
  }
}
```

## Performance Considerations

### Optimization Guidelines

**Canvas Rendering**:
- Use `requestAnimationFrame` for smooth animations
- Clear only necessary regions instead of full canvas
- Batch draw operations when possible
- Use off-screen canvases for complex elements

**SVG Animations**:
- Minimize DOM manipulations
- Use CSS transforms instead of SVG transforms
- Apply `will-change` for frequently animated properties
- Consider converting to canvas for complex animations

**Memory Management**:
- Remove completed animation objects
- Reuse particle/object pools
- Clean up event listeners
- Monitor memory usage in dev tools

## Testing Checklist

- [ ] Smooth playback at 60 fps
- [ ] Responsive on different screen sizes
- [ ] Works across all supported browsers
- [ ] Reduced motion alternative available
- [ ] Keyboard controls functional
- [ ] Screen reader announcements clear
- [ ] File size optimized
- [ ] Performance metrics within targets

## Resources

- [SVG Animation Guide](svg-animations.md)
- [CSS Animation Library](css-animations.md)
- [Performance Optimization](performance-optimization.md)
- [Animation Guidelines](animation-guidelines.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
