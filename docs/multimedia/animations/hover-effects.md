# Hover State Animations

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎨 [Animations](README.md)** | **👆 Hover Effects**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: CSS](https://img.shields.io/badge/Type-CSS-blue)
![Duration: 200-300ms](https://img.shields.io/badge/Duration-200--300ms-purple)

## Overview

Hover effects provide immediate visual feedback when users interact with elements. Well-designed hover states improve usability and create engaging interfaces.

## Button Hover Effects

### Lift Effect

```css
.button-lift {
  transition: all 250ms ease-out;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.button-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}
```

### Glow Effect

```css
.button-glow {
  transition: all 300ms ease;
  box-shadow: 0 0 0 0 rgba(0, 120, 212, 0);
}

.button-glow:hover {
  box-shadow: 0 0 20px 4px rgba(0, 120, 212, 0.4);
}
```

## Card Hover Effects

### Scale and Shadow

```css
.card {
  transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card:hover {
  transform: scale(1.03);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}
```

## Icon Hover Effects

### Rotation

```css
.icon-rotate {
  transition: transform 300ms ease-in-out;
}

.icon-rotate:hover {
  transform: rotate(90deg);
}
```

### Bounce

```css
.icon-bounce:hover {
  animation: bounce 600ms ease-in-out;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
```

## Resources

- [Micro-interactions](micro-interactions.md)
- [CSS Animations](css-animations.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
