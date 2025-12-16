# CSS Animation Library

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎨 [Animations](README.md)** | **💅 CSS Animations**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: CSS3](https://img.shields.io/badge/Type-CSS3-blue)
![Performance: Optimized](https://img.shields.io/badge/Performance-Optimized-green)

## Overview

CSS animations provide performant, hardware-accelerated animations using CSS keyframes and transitions. This library includes reusable animation classes for common UI patterns.

## Utility Classes

### Fade Animations

```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

.fade-in {
  animation: fadeIn 400ms ease-in;
}

.fade-out {
  animation: fadeOut 400ms ease-out;
}
```

### Slide Animations

```css
@keyframes slideInUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

@keyframes slideInDown {
  from { transform: translateY(-100%); }
  to { transform: translateY(0); }
}

@keyframes slideInLeft {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}

@keyframes slideInRight {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

.slide-in-up { animation: slideInUp 500ms ease-out; }
.slide-in-down { animation: slideInDown 500ms ease-out; }
.slide-in-left { animation: slideInLeft 500ms ease-out; }
.slide-in-right { animation: slideInRight 500ms ease-out; }
```

### Bounce Animation

```css
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-30px);
  }
  60% {
    transform: translateY(-15px);
  }
}

.bounce {
  animation: bounce 1s ease-in-out;
}
```

### Shake Animation

```css
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
  20%, 40%, 60%, 80% { transform: translateX(10px); }
}

.shake {
  animation: shake 500ms ease-in-out;
}
```

### Pulse Animation

```css
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.pulse {
  animation: pulse 1s ease-in-out infinite;
}
```

### Rotate Animation

```css
@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.rotate {
  animation: rotate 2s linear infinite;
}
```

## Timing Functions

```css
:root {
  --ease-in-quad: cubic-bezier(0.55, 0.085, 0.68, 0.53);
  --ease-out-quad: cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --ease-in-out-quad: cubic-bezier(0.455, 0.03, 0.515, 0.955);
  --ease-in-cubic: cubic-bezier(0.55, 0.055, 0.675, 0.19);
  --ease-out-cubic: cubic-bezier(0.215, 0.61, 0.355, 1);
  --ease-in-out-cubic: cubic-bezier(0.645, 0.045, 0.355, 1);
}
```

## Performance Tips

1. Prefer `transform` and `opacity` for animations
2. Use `will-change` sparingly
3. Avoid animating `width`, `height`, `top`, `left`
4. Use GPU-accelerated properties
5. Limit simultaneous animations

## Resources

- [MDN CSS Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations)
- [Performance Optimization](performance-optimization.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
