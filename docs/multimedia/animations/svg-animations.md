# SVG Animation Specifications

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎨 [Animations](README.md)** | **📐 SVG Animations**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: SVG/SMIL](https://img.shields.io/badge/Type-SVG%2FSMIL-blue)
![Browser Support: Modern](https://img.shields.io/badge/Browser%20Support-Modern-green)

## Overview

SVG animations provide crisp, scalable vector animations that work across all screen sizes and resolutions. They're ideal for icons, diagrams, and technical illustrations.

## SMIL Animation

### Basic Animation

```svg
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="40" fill="#0078D4">
    <animate
      attributeName="r"
      values="40;45;40"
      dur="2s"
      repeatCount="indefinite"/>
  </circle>
</svg>
```

### Path Animation

```svg
<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
  <path id="dataPath" d="M 10,50 Q 50,10 100,50 T 190,50"
        stroke="#0078D4" stroke-width="2" fill="none"
        stroke-dasharray="1000" stroke-dashoffset="1000">
    <animate
      attributeName="stroke-dashoffset"
      from="1000"
      to="0"
      dur="3s"
      fill="freeze"/>
  </path>
</svg>
```

## CSS-Animated SVG

```svg
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <style>
    .rotating-gear {
      transform-origin: center;
      animation: rotate 4s linear infinite;
    }
    @keyframes rotate {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
  </style>
  <g class="rotating-gear">
    <circle cx="50" cy="50" r="30" fill="#0078D4"/>
  </g>
</svg>
```

## JavaScript-Controlled SVG

```javascript
class SVGAnimationController {
  constructor(svgElement) {
    this.svg = svgElement;
    this.elements = {};
    this.timeline = [];
    this.currentTime = 0;
  }

  animate(elementId, property, from, to, duration) {
    const element = this.svg.getElementById(elementId);
    const startTime = this.currentTime;

    this.timeline.push({
      element,
      property,
      from,
      to,
      startTime,
      duration,
      easing: this.easeInOutCubic
    });
  }

  play() {
    this.startTime = Date.now();
    requestAnimationFrame(() => this.update());
  }

  update() {
    const elapsed = (Date.now() - this.startTime) / 1000;

    this.timeline.forEach(anim => {
      const progress = Math.min((elapsed - anim.startTime) / anim.duration, 1);
      const easedProgress = anim.easing(progress);
      const value = anim.from + (anim.to - anim.from) * easedProgress;

      anim.element.setAttribute(anim.property, value);
    });

    if (elapsed < this.duration) {
      requestAnimationFrame(() => this.update());
    }
  }

  easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
  }
}
```

## Resources

- [SVG Animation Guide](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/animate)
- [Animation Guidelines](animation-guidelines.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
