# Scroll-Triggered Animations

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🎨 [Animations](README.md)** | **📜 Scroll Animations**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![Type: JavaScript](https://img.shields.io/badge/Type-JavaScript-blue)
![Performance: Optimized](https://img.shields.io/badge/Performance-Optimized-green)

## Overview

Scroll animations trigger as users scroll through content, revealing elements progressively and creating engaging narrative experiences.

## Intersection Observer Implementation

```javascript
class ScrollAnimation {
  constructor() {
    this.observer = new IntersectionObserver(
      (entries) => this.handleIntersection(entries),
      {
        threshold: [0.1, 0.5, 0.9],
        rootMargin: '0px 0px -100px 0px'
      }
    );

    this.init();
  }

  init() {
    document.querySelectorAll('[data-animate-on-scroll]').forEach(el => {
      this.observer.observe(el);
    });
  }

  handleIntersection(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        if (entry.target.dataset.animateOnce) {
          this.observer.unobserve(entry.target);
        }
      } else {
        if (!entry.target.dataset.animateOnce) {
          entry.target.classList.remove('visible');
        }
      }
    });
  }
}
```

## Fade In On Scroll

```css
[data-animate-on-scroll] {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 600ms ease-out, transform 600ms ease-out;
}

[data-animate-on-scroll].visible {
  opacity: 1;
  transform: translateY(0);
}
```

## Parallax Scrolling

```javascript
class ParallaxScroll {
  constructor() {
    this.elements = document.querySelectorAll('[data-parallax]');
    this.handleScroll = this.handleScroll.bind(this);
    window.addEventListener('scroll', this.handleScroll);
  }

  handleScroll() {
    const scrolled = window.pageYOffset;

    this.elements.forEach(el => {
      const speed = el.dataset.parallaxSpeed || 0.5;
      const yPos = -(scrolled * speed);
      el.style.transform = `translateY(${yPos}px)`;
    });
  }
}
```

## Resources

- [Performance Optimization](performance-optimization.md)
- [Animation Guidelines](animation-guidelines.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
