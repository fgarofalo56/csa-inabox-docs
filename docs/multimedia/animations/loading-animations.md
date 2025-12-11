# Loading and Progress Animations

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎨 [Animations](README.md)** | **⏳ Loading Animations**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: CSS/SVG](https://img.shields.io/badge/Type-CSS%2FSVG-blue)
![Duration: Loop](https://img.shields.io/badge/Duration-Loop-purple)

## Overview

Loading animations provide visual feedback during data processing, query execution, and system operations. Well-designed loading animations improve user experience by managing expectations and reducing perceived wait time.

## Spinner Animations

### Azure Synapse Spinner

```css
.synapse-spinner {
  width: 60px;
  height: 60px;
  position: relative;
  animation: rotate 2s linear infinite;
}

.synapse-spinner::before,
.synapse-spinner::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 4px solid transparent;
}

.synapse-spinner::before {
  border-top-color: #0078D4;
  border-right-color: #0078D4;
  animation: spin 1.5s ease-in-out infinite;
}

.synapse-spinner::after {
  border-bottom-color: #00BCF2;
  border-left-color: #00BCF2;
  animation: spin 1.5s ease-in-out infinite reverse;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  50% { transform: rotate(180deg); }
  100% { transform: rotate(360deg); }
}
```

### Data Processing Spinner

```html
<svg class="data-processing-spinner" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40" stroke="#E0E0E0" stroke-width="8" fill="none"/>
  <circle cx="50" cy="50" r="40" stroke="#0078D4" stroke-width="8" fill="none"
          stroke-dasharray="251.2" stroke-dashoffset="0"
          transform="rotate(-90 50 50)">
    <animate attributeName="stroke-dashoffset"
             values="251.2;0;251.2"
             dur="2s"
             repeatCount="indefinite"/>
  </circle>
  <text x="50" y="55" text-anchor="middle" font-size="16" fill="#0078D4">
    <tspan id="percentage">0</tspan>%
  </text>
</svg>
```

## Progress Bars

### Linear Progress Bar

```css
.progress-bar {
  width: 100%;
  height: 8px;
  background: #E0E0E0;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #0078D4 0%, #00BCF2 100%);
  border-radius: 4px;
  transition: width 0.3s ease-in-out;
  position: relative;
  overflow: hidden;
}

.progress-bar-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.3) 50%,
    transparent 100%
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
```

### Indeterminate Progress

```css
.indeterminate-progress {
  width: 100%;
  height: 4px;
  background: #E0E0E0;
  position: relative;
  overflow: hidden;
}

.indeterminate-progress::before {
  content: '';
  position: absolute;
  height: 100%;
  width: 40%;
  background: linear-gradient(90deg, #0078D4, #00BCF2);
  animation: indeterminate 1.5s ease-in-out infinite;
}

@keyframes indeterminate {
  0% {
    left: -40%;
  }
  100% {
    left: 100%;
  }
}
```

## Skeleton Screens

### Table Skeleton

```html
<div class="skeleton-table">
  <div class="skeleton-row skeleton-header">
    <div class="skeleton-cell"></div>
    <div class="skeleton-cell"></div>
    <div class="skeleton-cell"></div>
  </div>
  <div class="skeleton-row">
    <div class="skeleton-cell"></div>
    <div class="skeleton-cell"></div>
    <div class="skeleton-cell"></div>
  </div>
  <div class="skeleton-row">
    <div class="skeleton-cell"></div>
    <div class="skeleton-cell"></div>
    <div class="skeleton-cell"></div>
  </div>
</div>

<style>
.skeleton-cell {
  height: 40px;
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: 4px;
  margin: 8px;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
```

## Pulse Animations

### Data Sync Pulse

```css
.sync-pulse {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #0078D4;
  position: relative;
  animation: pulse 2s infinite;
}

.sync-pulse::before,
.sync-pulse::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: rgba(0, 120, 212, 0.4);
  top: 0;
  left: 0;
  animation: pulse-ring 2s infinite;
}

.sync-pulse::after {
  animation-delay: 1s;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

@keyframes pulse-ring {
  0% {
    transform: scale(1);
    opacity: 0.5;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}
```

## Resources

- [Animation Guidelines](animation-guidelines.md)
- [CSS Animations](css-animations.md)
- [Performance Optimization](performance-optimization.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
