# ETL Pipeline Animation Storyboard

> **🏠 [Home](../../../../README.md)** | **📖 [Documentation](../../../README.md)** | **🎬 [Multimedia](../../README.md)** | **🎨 [Animations](../README.md)** | **Storyboards** | **ETL Pipeline**

![Status: Planning](https://img.shields.io/badge/Status-Planning-blue)
![Type: Animation](https://img.shields.io/badge/Type-Animation-purple)
![Duration: 15 seconds](https://img.shields.io/badge/Duration-15s-blue)

## Overview

Animated visualization of an ETL (Extract, Transform, Load) pipeline in Azure Synapse Analytics, showing data flow from sources through transformation to destination.

## Animation Sequence

### Frame 1: Extract (0s - 5s)

**Visual Elements**:
```
Data Sources                    Ingestion
┌─────────────┐                ┌──────────┐
│   SAP ERP   │────────────────▶│          │
├─────────────┤                │          │
│ Salesforce  │────────────────▶│ Synapse  │
├─────────────┤                │ Pipeline │
│  IoT Hub    │────────────────▶│          │
└─────────────┘                └──────────┘
```

**Animation**:
- Data icons pulse at sources
- Animated particles flow from sources
- Converge into pipeline (funnel effect)
- Color: Blue (#0078D4)
- Duration: 5 seconds
- Easing: ease-in

**Key Frames**:
- 0s: Sources visible, static
- 1s: Data pulse begins
- 2s: First particles flow
- 3s: Multiple streams flowing
- 5s: All data entering pipeline

### Frame 2: Transform (5s - 10s)

**Visual Elements**:
```
Pipeline Processing
┌────────────────────────┐
│  Cleanse  │  Validate  │
├───────────┼────────────┤
│ Transform │ Aggregate  │
└────────────────────────┘
```

**Animation**:
- Data enters transformation zone
- Icons for each operation light up
- Particles change color as processed
  - Raw: Gray (#808080)
  - Cleansed: Green (#28a745)
  - Transformed: Blue (#0078D4)
- Gears rotating in background
- Duration: 5 seconds
- Easing: linear

**Key Frames**:
- 5s: Data enters transform stage
- 6s: Cleanse operation activates (green glow)
- 7s: Validate operation activates (checkmark)
- 8s: Transform operation activates (gear spin)
- 9s: Aggregate operation activates (merge effect)
- 10s: Processed data ready

### Frame 3: Load (10s - 15s)

**Visual Elements**:
```
Transformation              Destinations
┌──────────┐               ┌─────────────┐
│          │──────────────▶│ Data Lake   │
│ Pipeline │               ├─────────────┤
│          │──────────────▶│  SQL Pool   │
└──────────┘               ├─────────────┤
                           │  Power BI   │
                           └─────────────┘
```

**Animation**:
- Processed data flows to destinations
- Split stream to multiple targets
- Destination icons glow as data arrives
- Success checkmarks appear
- Duration: 5 seconds
- Easing: ease-out

**Key Frames**:
- 10s: Data exits transformation
- 11s: Stream splits to destinations
- 12s: Data Lake receives (storage icon fills)
- 13s: SQL Pool receives (database icon fills)
- 14s: Power BI receives (chart animates)
- 15s: All destinations show success ✓

## Visual Style

### Color Palette
- **Primary**: Azure Blue (#0078D4)
- **Success**: Green (#28a745)
- **Processing**: Yellow (#ffc107)
- **Data**: Gradient (#0078D4 → #50E6FF)
- **Background**: Dark (#1E1E1E) or White (#FFFFFF)

### Typography
- **Labels**: Segoe UI, 16px, Bold
- **Details**: Segoe UI, 12px, Regular
- **Monospaced**: Consolas, 14px (for data values)

### Icons
- Source systems: 64x64px
- Pipeline operations: 48x48px
- Destinations: 64x64px
- All icons: Line style, 2px stroke

## Technical Specifications

### Animation Properties
```css
/* Data flow particles */
.data-particle {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: flow 5s ease-in-out infinite;
}

@keyframes flow {
  0% {
    transform: translateX(0) scale(1);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateX(500px) scale(0.8);
    opacity: 0;
  }
}

/* Glow effect on active operations */
.operation-active {
  animation: glow 1s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    box-shadow: 0 0 5px #0078D4;
  }
  to {
    box-shadow: 0 0 20px #0078D4;
  }
}

/* Success checkmark */
.checkmark {
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  animation: draw 0.5s ease-out forwards;
}

@keyframes draw {
  to {
    stroke-dashoffset: 0;
  }
}
```

### File Formats
- **Source**: Adobe After Effects or Lottie JSON
- **Export**: MP4 (H.264), WebM, GIF
- **Resolution**: 1920x1080 @ 30fps
- **File Size**: < 5MB

## Usage Context

### Where to Use
- Tutorial videos (ETL concept introduction)
- Documentation headers
- Presentation slides
- Website hero animations
- Training materials

### Accessibility
- Provide text alternative describing the ETL process
- Ensure color contrast meets WCAG 2.1 AA
- Support reduced motion preference
- Include pause/play controls

## Production Notes

### Required Assets
- [ ] Source system icons (SAP, Salesforce, IoT)
- [ ] Pipeline component icons
- [ ] Destination icons (Data Lake, SQL, Power BI)
- [ ] Particle sprites
- [ ] Glow effect overlays
- [ ] Success checkmark SVG

### Animation Software
- **Primary**: Adobe After Effects
- **Alternative**: Lottie (JSON-based)
- **Web**: CSS animations + SVG
- **Runtime**: Lottie-web player

### Performance Optimization
- Use vector graphics (SVG)
- Minimize particle count (< 100)
- Limit concurrent animations
- Hardware acceleration enabled
- Compressed output format

## Related Animations

- [Stream Processing Animation](stream-processing.md)
- [Data Flow Animations](../data-flow-animations.md)
- [Process Animations](../process-animations.md)

---

*Last Updated: January 2025*
