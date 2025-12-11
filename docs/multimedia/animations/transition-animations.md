# UI Transition Specifications

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎨 [Animations](README.md)** | **🎭 Transitions**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: CSS](https://img.shields.io/badge/Type-CSS-blue)
![Duration: 200-500ms](https://img.shields.io/badge/Duration-200--500ms-purple)

## Overview

UI transition animations create smooth, professional interactions between different states and views. Properly designed transitions enhance usability and provide visual continuity.

## Page Transitions

### Fade Transition

```css
.page-fade-enter {
  opacity: 0;
}

.page-fade-enter-active {
  opacity: 1;
  transition: opacity 300ms ease-in;
}

.page-fade-exit {
  opacity: 1;
}

.page-fade-exit-active {
  opacity: 0;
  transition: opacity 300ms ease-out;
}
```

### Slide Transition

```css
.page-slide-enter {
  transform: translateX(100%);
}

.page-slide-enter-active {
  transform: translateX(0);
  transition: transform 400ms ease-out;
}

.page-slide-exit {
  transform: translateX(0);
}

.page-slide-exit-active {
  transform: translateX(-100%);
  transition: transform 400ms ease-in;
}
```

## Modal Transitions

### Scale and Fade

```css
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  transition: opacity 300ms ease-in-out;
}

.modal-backdrop.show {
  opacity: 1;
}

.modal-content {
  transform: scale(0.7);
  opacity: 0;
  transition: all 300ms ease-out;
}

.modal-content.show {
  transform: scale(1);
  opacity: 1;
}
```

## Accordion Transitions

```css
.accordion-panel {
  max-height: 0;
  overflow: hidden;
  transition: max-height 400ms ease-in-out;
}

.accordion-panel.open {
  max-height: 1000px;
}

.accordion-icon {
  transition: transform 300ms ease-in-out;
}

.accordion-icon.rotated {
  transform: rotate(180deg);
}
```

## Resources

- [Animation Guidelines](animation-guidelines.md)
- [Micro-interactions](micro-interactions.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
