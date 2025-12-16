# Lottie Animation Assets

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎨 [Animations](README.md)** | **🎬 Lottie**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: Lottie JSON](https://img.shields.io/badge/Type-Lottie%20JSON-blue)
![File Size: < 500KB](https://img.shields.io/badge/File%20Size-<%20500KB-green)

## Overview

Lottie animations are vector-based, lightweight animations exported from After Effects that can be played across web, iOS, and Android platforms with perfect fidelity.

## Lottie Integration

### Web Implementation

```html
<div id="lottie-container" style="width: 400px; height: 400px;"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js"></script>
<script>
const animation = lottie.loadAnimation({
  container: document.getElementById('lottie-container'),
  renderer: 'svg',
  loop: true,
  autoplay: true,
  path: '/animations/data-flow.json'
});
</script>
```

### React Implementation

```jsx
import Lottie from 'lottie-react';
import animationData from './animations/data-flow.json';

function DataFlowAnimation() {
  return (
    <Lottie
      animationData={animationData}
      loop={true}
      autoplay={true}
      style={{ width: 400, height: 400 }}
    />
  );
}
```

## Export Settings

### After Effects to Lottie

**Recommended Settings**:
- Bodymovin plugin v5.9+
- Compression enabled
- Glyphs: Export as shapes
- Remove hidden layers
- Merge paths when possible

```json
{
  "exportSettings": {
    "bodymovin": {
      "version": "5.9.0",
      "compression": true,
      "glyphs": false,
      "fonts": {
        "list": [],
        "embed": false
      },
      "optimize": {
        "mergeShapes": true,
        "removeHidden": true,
        "simplifyPaths": true,
        "decimals": 2
      }
    }
  }
}
```

## Performance Optimization

**Optimization Techniques**:
- Limit layer count (< 50 layers recommended)
- Use shape layers instead of images
- Minimize effects (no complex blurs or glows)
- Reduce keyframe count
- Simplify paths

## Common Animations

### Data Processing Icon

```json
{
  "v": "5.9.0",
  "fr": 60,
  "ip": 0,
  "op": 180,
  "w": 400,
  "h": 400,
  "nm": "Data Processing",
  "ddd": 0,
  "assets": [],
  "layers": [
    {
      "ddd": 0,
      "ind": 1,
      "ty": 4,
      "nm": "Circle",
      "sr": 1,
      "ks": {
        "o": { "a": 0, "k": 100 },
        "r": {
          "a": 1,
          "k": [
            { "i": { "x": [0.833], "y": [0.833] }, "o": { "x": [0.167], "y": [0.167] }, "t": 0, "s": [0] },
            { "t": 180, "s": [360] }
          ]
        },
        "p": { "a": 0, "k": [200, 200, 0] },
        "a": { "a": 0, "k": [0, 0, 0] },
        "s": { "a": 0, "k": [100, 100, 100] }
      },
      "ao": 0,
      "shapes": [
        {
          "ty": "gr",
          "it": [
            {
              "d": 1,
              "ty": "el",
              "s": { "a": 0, "k": [150, 150] },
              "p": { "a": 0, "k": [0, 0] },
              "nm": "Ellipse Path 1"
            },
            {
              "ty": "st",
              "c": { "a": 0, "k": [0, 0.47, 0.83, 1] },
              "o": { "a": 0, "k": 100 },
              "w": { "a": 0, "k": 8 },
              "lc": 2,
              "lj": 2,
              "nm": "Stroke 1"
            }
          ],
          "nm": "Ellipse 1"
        }
      ],
      "ip": 0,
      "op": 180,
      "st": 0,
      "bm": 0
    }
  ]
}
```

## Resources

- [Lottie Documentation](https://airbnb.io/lottie/)
- [Animation Guidelines](animation-guidelines.md)
- [Performance Optimization](performance-optimization.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
