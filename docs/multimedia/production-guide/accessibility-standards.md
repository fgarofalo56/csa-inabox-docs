# Accessibility Standards

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **📎 [Production Guide](README.md)** | **♿ Accessibility**

![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)
![WCAG: 2.1 AA](https://img.shields.io/badge/WCAG-2.1%20AA-blue)

## Overview

Accessibility standards ensure Cloud Scale Analytics multimedia content is usable by everyone, including people with disabilities. All content must meet WCAG 2.1 Level AA compliance.

## WCAG 2.1 Level AA Requirements

### Video Accessibility

#### Captions (1.2.2)

**Requirements:**
- Accurate synchronized captions for all pre-recorded video
- 99%+ accuracy minimum
- Speaker identification when multiple speakers
- Sound effect descriptions
- Synchronized within 0.5 seconds

**Caption Format (WebVTT):**

```vtt
WEBVTT

00:00:00.000 --> 00:00:03.500
Welcome to Cloud Scale Analytics.

00:00:03.500 --> 00:00:07.000
Today we'll explore Azure Synapse Analytics.

00:00:07.000 --> 00:00:10.500
[soft background music playing]

00:00:10.500 --> 00:00:14.000
<v Instructor>Let's start with the Azure Portal.

00:00:14.500 --> 00:00:18.000
<v Instructor>Navigate to Azure Synapse Analytics.

00:00:18.500 --> 00:00:22.000
[mouse clicking sound]
```

**Implementation:**

```html
<video controls>
  <source src="tutorial.mp4" type="video/mp4">
  <track kind="captions" src="captions-en.vtt" srclang="en" label="English" default>
  <track kind="captions" src="captions-es.vtt" srclang="es" label="Español">
  Your browser does not support the video tag.
</video>
```

#### Audio Description (1.2.5)

**Requirements:**
- Describe important visual information not conveyed in audio
- Delivered during natural pauses in dialogue
- Extended audio description if pauses insufficient

**Audio Description Script:**

```markdown
## Video: Azure Synapse Workspace Setup

### Scene 1 (0:30-1:00)
**Visual:** Azure Portal dashboard with Synapse workspace tile highlighted
**Description:** "The Azure Portal shows a dashboard view. A blue tile labeled 'Azure Synapse Analytics' is highlighted in the center."

### Scene 2 (1:15-1:45)
**Visual:** Configuration panel with multiple dropdown menus and text fields
**Description:** "A configuration panel appears with fields for workspace name, subscription, and resource group. Required fields are marked with red asterisks."

### Scene 3 (2:30-3:00)
**Visual:** Progress indicator showing deployment status
**Description:** "A progress bar displays deployment status at 75%, with green checkmarks indicating completed steps."
```

#### Transcripts (1.2.8)

**Full Text Transcript:**

```markdown
# Transcript: Azure Synapse Analytics Tutorial

## Speaker: Cloud Architect

[00:00] Welcome to Cloud Scale Analytics. I'm Sarah, and today we'll explore Azure Synapse Analytics.

[00:03] [Soft background music begins]

[00:05] Azure Synapse is a powerful analytics service that brings together data integration, enterprise data warehousing, and big data analytics.

[00:15] Let's start by creating a new workspace in the Azure Portal.

[00:18] [Mouse clicking sound]

[00:20] Navigate to "Create a resource" and search for "Synapse Analytics"...

---

## Resources Mentioned
- Azure Portal: portal.azure.com
- Documentation: docs.microsoft.com/azure/synapse-analytics
- GitHub Repository: github.com/csa-inabox

## Transcript Information
- Duration: 15:30
- Created: January 2025
- Language: English
- Format: Text, PDF, HTML
```

### Interactive Content Accessibility

#### Keyboard Navigation (2.1.1)

**Requirements:**
- All functionality available via keyboard
- Tab order logical
- Focus visible (2.4.7)
- No keyboard traps (2.1.2)

**Implementation Example:**

```html
<div class="interactive-demo" role="application" aria-label="Azure Pipeline Builder">
  <!-- Keyboard accessible controls -->
  <button
    id="add-step"
    aria-label="Add pipeline step"
    aria-describedby="add-step-help"
    tabindex="0">
    Add Step
  </button>
  <div id="add-step-help" class="sr-only">
    Press Enter to add a new step to the pipeline
  </div>

  <!-- Keyboard shortcuts -->
  <div role="region" aria-label="Keyboard shortcuts">
    <h3>Keyboard Shortcuts</h3>
    <ul>
      <li><kbd>Tab</kbd> - Navigate between elements</li>
      <li><kbd>Enter</kbd> - Activate button or link</li>
      <li><kbd>Esc</kbd> - Close dialog or cancel action</li>
      <li><kbd>Arrow keys</kbd> - Navigate within component</li>
    </ul>
  </div>
</div>

<script>
// Implement keyboard navigation
document.getElementById('add-step').addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    addPipelineStep();
  }
});

// Ensure focus visible
document.querySelectorAll('button, a, input').forEach(el => {
  el.classList.add('focus-visible-support');
});
</script>

<style>
/* Focus indicators */
button:focus-visible,
a:focus-visible,
input:focus-visible {
  outline: 3px solid #0078D4;
  outline-offset: 2px;
}

/* Screen reader only content */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>
```

#### ARIA Labels and Roles (4.1.2)

```html
<!-- Properly labeled interactive elements -->
<div role="region" aria-labelledby="demo-title" aria-describedby="demo-desc">
  <h2 id="demo-title">Pipeline Configuration Demo</h2>
  <p id="demo-desc">Configure your Azure Synapse pipeline using this interactive builder</p>

  <!-- Form with proper labels -->
  <form role="form" aria-label="Pipeline configuration form">
    <label for="pipeline-name">Pipeline Name:</label>
    <input
      id="pipeline-name"
      type="text"
      aria-required="true"
      aria-invalid="false"
      aria-describedby="name-error">
    <span id="name-error" role="alert" aria-live="polite"></span>

    <!-- Select with grouped options -->
    <label for="trigger-type">Trigger Type:</label>
    <select id="trigger-type" aria-label="Select pipeline trigger type">
      <optgroup label="Time-based triggers">
        <option value="schedule">Schedule</option>
        <option value="tumbling">Tumbling Window</option>
      </optgroup>
      <optgroup label="Event-based triggers">
        <option value="storage">Storage Event</option>
        <option value="custom">Custom Event</option>
      </optgroup>
    </select>

    <!-- Status updates -->
    <div role="status" aria-live="polite" aria-atomic="true">
      <span class="sr-only">Pipeline validation in progress</span>
    </div>
  </form>
</div>
```

### Graphics and Images Accessibility

#### Alternative Text (1.1.1)

**Guidelines:**

```markdown
## Alt Text Best Practices

### Informative Images
**Good:** "Architecture diagram showing data flow from Azure Data Lake through Synapse to Power BI"
**Bad:** "Diagram" or "Architecture"

### Functional Images (buttons, icons)
**Good:** "Search" (for search icon button)
**Bad:** "Magnifying glass icon"

### Complex Images (charts, diagrams)
- **Alt text:** Brief description
- **Long description:** Detailed explanation in adjacent text or linked page

### Decorative Images
- **Alt text:** Empty (alt="")
- **ARIA:** aria-hidden="true"
```

**Implementation:**

```html
<!-- Informative image -->
<img
  src="synapse-architecture.png"
  alt="Azure Synapse Analytics architecture showing data ingestion, processing, and visualization layers">

<!-- Complex diagram with long description -->
<figure>
  <img
    src="data-flow-diagram.svg"
    alt="Data flow diagram from source to analytics"
    aria-describedby="diagram-desc">
  <figcaption id="diagram-desc">
    <details>
      <summary>Detailed diagram description</summary>
      <p>The diagram illustrates a three-tier data architecture:</p>
      <ol>
        <li><strong>Ingestion Layer:</strong> Data flows from multiple sources including Azure Event Hub, Azure IoT Hub, and Azure Data Lake Storage Gen2.</li>
        <li><strong>Processing Layer:</strong> Azure Synapse Analytics processes the data using both Spark pools for big data processing and dedicated SQL pools for structured queries.</li>
        <li><strong>Analytics Layer:</strong> Processed data is consumed by Power BI for visualization and Azure Machine Learning for predictive analytics.</li>
      </ol>
    </details>
  </figcaption>
</figure>

<!-- Decorative image -->
<img src="decorative-gradient.png" alt="" aria-hidden="true">
```

### Color and Contrast (1.4.3, 1.4.11)

**Contrast Requirements:**

```yaml
contrast_ratios:
  normal_text:
    minimum: "4.5:1"
    enhanced: "7:1 (AAA)"
    applies: "< 18pt or < 14pt bold"

  large_text:
    minimum: "3:1"
    enhanced: "4.5:1 (AAA)"
    applies: ">= 18pt or >= 14pt bold"

  ui_components:
    minimum: "3:1"
    applies: "Buttons, form fields, icons"

  graphical_objects:
    minimum: "3:1"
    applies: "Charts, diagrams, meaningful graphics"

examples:
  compliant:
    - background: "#FFFFFF"
      text: "#323130"
      ratio: "13.4:1"
      status: "Pass"

    - background: "#0078D4"
      text: "#FFFFFF"
      ratio: "4.59:1"
      status: "Pass"

  non_compliant:
    - background: "#FFFFFF"
      text: "#808080"
      ratio: "3.95:1"
      status: "Fail (normal text)"
```

**Testing Tools:**

```javascript
// Contrast checker function
function checkContrast(foreground, background) {
  const getLuminance = (color) => {
    const rgb = color.match(/\d+/g).map(Number);
    const [r, g, b] = rgb.map(val => {
      val = val / 255;
      return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };

  const l1 = getLuminance(foreground);
  const l2 = getLuminance(background);
  const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);

  return {
    ratio: ratio.toFixed(2),
    aaLargeText: ratio >= 3,
    aaNormalText: ratio >= 4.5,
    aaaLargeText: ratio >= 4.5,
    aaaNormalText: ratio >= 7
  };
}

// Example usage
const result = checkContrast('rgb(50, 49, 48)', 'rgb(255, 255, 255)');
console.log(`Contrast ratio: ${result.ratio}:1`);
console.log(`AA Normal Text: ${result.aaNormalText ? 'Pass' : 'Fail'}`);
```

### Motion and Animation (2.2.2, 2.3.1)

**Guidelines:**

```yaml
motion_guidelines:
  pause_stop_hide:
    requirement: "User can pause, stop, or hide moving content"
    applies: "Auto-playing content > 5 seconds"
    implementation: "Provide playback controls"

  prefers_reduced_motion:
    requirement: "Respect user's motion preferences"
    implementation: "CSS media query"
    fallback: "Static or simplified animation"

  three_flashes:
    requirement: "No content flashes > 3 times per second"
    applies: "All visual content"
    testing: "PEAT (Photosensitive Epilepsy Analysis Tool)"

examples:
  css_implementation: |
    /* Default animation */
    .animated-element {
      animation: slide-in 0.5s ease-out;
    }

    /* Reduced motion alternative */
    @media (prefers-reduced-motion: reduce) {
      .animated-element {
        animation: none;
        opacity: 1;
      }
    }

  javascript_implementation: |
    // Check user preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotion) {
      // Use simpler, instant transitions
      element.style.transition = 'none';
    } else {
      // Use full animation
      element.style.transition = 'all 0.5s ease-out';
    }
```

## Testing and Validation

### Automated Testing Tools

```yaml
testing_tools:
  browser_extensions:
    wave:
      name: "WAVE Web Accessibility Evaluation Tool"
      url: "https://wave.webaim.org/extension/"
      tests: "WCAG compliance, errors, alerts, features"

    axe:
      name: "axe DevTools"
      url: "https://www.deque.com/axe/devtools/"
      tests: "Automated accessibility scans"

    lighthouse:
      name: "Google Lighthouse"
      url: "Built into Chrome DevTools"
      tests: "Accessibility audit, performance, SEO"

  command_line:
    pa11y:
      install: "npm install -g pa11y"
      usage: "pa11y https://your-site.com"
      output: "JSON, CSV, HTML reports"

    axe_cli:
      install: "npm install -g @axe-core/cli"
      usage: "axe https://your-site.com"
      output: "Detailed violation reports"

  continuous_integration:
    axe_core:
      integration: "Jest, Mocha, Cypress"
      automation: "CI/CD pipeline testing"
```

### Manual Testing Procedures

```markdown
## Manual Accessibility Testing

### Screen Reader Testing

#### NVDA (Windows, Free)
1. Download from https://www.nvaccess.org/
2. Start NVDA (Ctrl + Alt + N)
3. Navigate content (arrow keys, H for headings, Tab for links)
4. Verify:
   - All content announced correctly
   - Heading structure logical
   - Links descriptive
   - Images have alt text
   - Forms properly labeled

#### JAWS (Windows, Paid)
- Similar to NVDA, industry standard
- Test if budget allows

#### VoiceOver (macOS/iOS, Built-in)
- Start: Cmd + F5 (macOS) or Settings > Accessibility (iOS)
- Navigate with VoiceOver commands
- Test on both desktop and mobile

### Keyboard Navigation Testing

1. **Tab Through Page**
   - All interactive elements reachable
   - Focus order logical
   - Focus clearly visible
   - No keyboard traps

2. **Test Functionality**
   - Forms submittable with Enter
   - Dropdowns operable with arrow keys
   - Dialogs closeable with Escape
   - Custom controls have keyboard support

3. **Skip Links**
   - "Skip to main content" link present
   - Works when activated
   - Other skip links as needed

### Visual Testing

1. **Zoom to 200%**
   - Content remains visible
   - No horizontal scrolling (ideally)
   - Text reflows appropriately
   - UI controls still functional

2. **Color Blind Simulation**
   - Use browser extensions (e.g., ColorOracle)
   - Verify information not conveyed by color alone
   - Test with various types of color blindness

3. **High Contrast Mode**
   - Windows High Contrast
   - macOS Increase Contrast
   - Verify content still visible and usable
```

## Accessibility Documentation

### Content Accessibility Report

```markdown
# Accessibility Conformance Report

## Product Information
- **Product:** [Video/Interactive Demo Name]
- **Version:** [Version Number]
- **Date:** [YYYY-MM-DD]
- **Report Based On:** WCAG 2.1 Level AA

## Summary
This [video/interactive content] has been evaluated for accessibility and conforms to WCAG 2.1 Level AA.

## Conformance Level
- **Level A:** [Conformant / Partially Conformant / Non-Conformant]
- **Level AA:** [Conformant / Partially Conformant / Non-Conformant]
- **Level AAA:** [Not Evaluated / Partially Conformant / Non-Conformant]

## Success Criteria

### Level A

#### 1.1.1 Non-text Content (A)
- **Status:** Conformant
- **Details:** All images have appropriate alt text. Decorative images marked as such.

#### 1.2.1 Audio-only and Video-only (A)
- **Status:** Conformant
- **Details:** Transcript provided for all audio/video content.

#### 1.2.2 Captions (Prerecorded) (A)
- **Status:** Conformant
- **Details:** Synchronized captions with 99.5% accuracy.

[Continue for all applicable criteria...]

### Level AA

#### 1.2.5 Audio Description (AA)
- **Status:** Conformant
- **Details:** Extended audio description provided for visual content.

#### 1.4.3 Contrast (Minimum) (AA)
- **Status:** Conformant
- **Details:** All text meets 4.5:1 contrast ratio. UI elements meet 3:1.

[Continue for all applicable criteria...]

## Known Issues
- [List any known accessibility issues and planned remediation]

## Testing Methods
- Automated: WAVE, axe DevTools, Lighthouse
- Manual: Keyboard navigation, screen reader (NVDA)
- User Testing: [If conducted]

## Contact
For accessibility questions or issues:
- Email: accessibility@cloudscaleanalytics.com
- Issue Tracker: [URL]
```

## Related Resources

- [Quality Assurance Guide](quality-assurance.md)
- [Video Production Workflow](video-production-workflow.md)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Resources](https://webaim.org/resources/)

---

*Last Updated: January 2025 | Version: 1.0.0*
