# Animation Best Practices

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎨 [Animations](README.md)** | **📋 Guidelines**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: Guidelines](https://img.shields.io/badge/Type-Guidelines-blue)

## Overview

Animation guidelines ensure consistent, accessible, and performant animations across all CSA-in-a-Box documentation and interfaces.

## Duration Guidelines

| Animation Type | Duration | Easing |
|:--------------|:---------|:-------|
| **Micro-interactions** | 100-200ms | ease-out |
| **Small elements** | 200-300ms | ease-in-out |
| **Medium elements** | 300-400ms | ease-in-out |
| **Large/complex** | 400-600ms | ease-out |
| **Page transitions** | 300-500ms | ease-in-out |

## Easing Functions

**Use Case Guidelines**:
- **ease-in**: Elements leaving the screen
- **ease-out**: Elements entering the screen
- **ease-in-out**: Elements moving within the screen
- **linear**: Continuous animations (loading spinners)

## Accessibility Requirements

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Focus Indicators

```css
:focus-visible {
  outline: 3px solid #0078D4;
  outline-offset: 2px;
  animation: pulse-outline 1s ease-in-out;
}

@keyframes pulse-outline {
  0%, 100% { outline-width: 3px; }
  50% { outline-width: 5px; }
}
```

## Performance Best Practices

1. **Use transform and opacity**
   - Hardware accelerated
   - Smooth 60fps performance

2. **Avoid layout triggers**
   - Don't animate width, height, padding, margin
   - Use transform: scale() instead

3. **Batch animations**
   - Group related animations
   - Use requestAnimationFrame

4. **Limit simultaneous animations**
   - Maximum 3-5 concurrent animations
   - Stagger complex sequences

5. **Test on low-end devices**
   - Ensure 30fps minimum
   - Provide fallbacks

## Browser Compatibility

Ensure animations work across:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Resources

- [Performance Optimization](performance-optimization.md)
- [CSS Animations](css-animations.md)
- [WCAG 2.1 Motion Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html)

---

*Last Updated: January 2025 | Version: 1.0.0*
