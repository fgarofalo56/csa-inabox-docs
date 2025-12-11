# Micro-Interaction Specifications

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎨 [Animations](README.md)** | **✨ Micro-interactions**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: CSS/JavaScript](https://img.shields.io/badge/Type-CSS%2FJavaScript-blue)
![Duration: 100-400ms](https://img.shields.io/badge/Duration-100--400ms-purple)

## Overview

Micro-interactions are small, functional animations that provide feedback, guide users, and enhance the overall user experience through subtle, purposeful motion.

## Button Click Feedback

### Ripple Effect

```javascript
class RippleEffect {
  constructor(button) {
    this.button = button;
    this.button.addEventListener('click', (e) => this.createRipple(e));
  }

  createRipple(event) {
    const button = event.currentTarget;
    const ripple = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    ripple.style.width = ripple.style.height = `${diameter}px`;
    ripple.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    ripple.style.top = `${event.clientY - button.offsetTop - radius}px`;
    ripple.classList.add('ripple');

    button.appendChild(ripple);

    setTimeout(() => ripple.remove(), 600);
  }
}

// CSS
.button {
  position: relative;
  overflow: hidden;
}

.ripple {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  transform: scale(0);
  animation: ripple-animation 600ms ease-out;
}

@keyframes ripple-animation {
  to {
    transform: scale(4);
    opacity: 0;
  }
}
```

## Toggle Switch

```css
.toggle-switch {
  position: relative;
  width: 60px;
  height: 30px;
  background: #ccc;
  border-radius: 15px;
  transition: background 300ms ease;
  cursor: pointer;
}

.toggle-switch::after {
  content: '';
  position: absolute;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: white;
  top: 2px;
  left: 2px;
  transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.toggle-switch.active {
  background: #0078D4;
}

.toggle-switch.active::after {
  transform: translateX(30px);
}
```

## Checkbox Animation

```css
.checkbox {
  position: relative;
  width: 24px;
  height: 24px;
  border: 2px solid #0078D4;
  border-radius: 4px;
  transition: all 200ms ease;
}

.checkbox::after {
  content: '';
  position: absolute;
  width: 6px;
  height: 12px;
  border: solid white;
  border-width: 0 2px 2px 0;
  top: 2px;
  left: 7px;
  transform: rotate(45deg) scale(0);
  transition: transform 200ms ease;
}

.checkbox.checked {
  background: #0078D4;
}

.checkbox.checked::after {
  transform: rotate(45deg) scale(1);
}
```

## Input Focus Animation

```css
.input-field {
  border: 2px solid #E0E0E0;
  padding: 12px;
  transition: all 300ms ease;
  position: relative;
}

.input-field::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: #0078D4;
  transition: all 300ms ease;
}

.input-field:focus::after {
  left: 0;
  width: 100%;
}

.input-field:focus {
  border-color: #0078D4;
  box-shadow: 0 0 0 3px rgba(0, 120, 212, 0.1);
}
```

## Success/Error Notifications

```css
.notification {
  padding: 16px;
  border-radius: 8px;
  animation: slide-in 400ms ease-out, pulse 200ms 400ms ease-in-out;
}

.notification.success {
  background: #E6F4EA;
  border-left: 4px solid #107C10;
}

.notification.error {
  background: #FCE8E6;
  border-left: 4px solid #D13438;
}

@keyframes slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}
```

## Loading Dots

```css
.loading-dots {
  display: flex;
  gap: 8px;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #0078D4;
  animation: bounce-dot 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce-dot {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}
```

## Resources

- [Hover Effects](hover-effects.md)
- [Transition Animations](transition-animations.md)
- [CSS Animations](css-animations.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
