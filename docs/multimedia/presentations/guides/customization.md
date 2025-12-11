# 🔧 Presentation Customization Guide - CSA-in-a-Box

> **🏠 [Home](../../../../README.md)** | **📖 [Documentation](../../../README.md)** | **🎬 [Multimedia](../../README.md)** | **📊 [Presentations](../README.md)** | **📋 [Guides](README.md)** | **👤 Customization**

![Type: Guide](https://img.shields.io/badge/Type-Guide-blue)
![Audience: Content Creators](https://img.shields.io/badge/Audience-Content%20Creators-orange)

## 📋 Overview

Guide to customizing CSA-in-a-Box presentation templates for your organization while maintaining brand consistency and accessibility.

## 🎨 Template Customization

### PowerPoint Master Slides

**Accessing Master View**:
```text
View → Master Views → Slide Master
```

**Master Slide Hierarchy**:
```markdown
Slide Master (Top Level)
├── Title Slide Layout
├── Title and Content Layout
├── Section Header Layout
├── Two Content Layout
├── Comparison Layout
├── Blank Layout
└── Custom Layouts
```

**Best Practices**:
- Edit master slides, not individual slides
- Changes cascade to all related slides
- Create custom layouts for special needs
- Test changes across all slide types
- Save custom template (.potx)

### Corporate Branding

**Adding Your Logo**:

```text
Steps:
1. Enter Slide Master view
2. Insert → Pictures → Select logo file
3. Position in standard location (top-left recommended)
4. Resize maintaining aspect ratio
5. Add to all relevant master layouts
6. Return to Normal view
```

**Logo Specifications**:
- Format: PNG with transparency (preferred) or SVG
- Resolution: 150 DPI minimum
- Size: 1-2 inches width
- Clear space: Logo height × 0.5
- Position: Consistent across all slides

**Color Scheme Customization**:

```text
Design → Variants → Colors → Customize Colors

Replace Azure colors with corporate colors:
- Primary (Azure Blue) → Corporate Primary
- Accent (Cloud Blue) → Corporate Accent
- Text (Dark Gray) → Corporate Text
- Background (White) → Corporate Background

Save as "[Company Name] Colors"
```

**Corporate Color Palette Example**:

```markdown
Acme Corporation Palette:

Primary: #FF6B35 (Acme Orange)
Secondary: #004E89 (Acme Navy)
Accent: #F7B801 (Acme Gold)
Text: #2D3142 (Dark Gray)
Background: #FFFFFF (White)
Light: #EDF2F4 (Light Gray)
```

### Typography Customization

**Corporate Font Implementation**:

```text
Home → Replace → Replace Fonts

Replace:
- Segoe UI → [Corporate Font Name]
- Arial → [Corporate Sans-Serif]
- Calibri → [Corporate Alternative]

Important: Embed fonts for portability
File → Options → Save → Embed fonts in the file
```

**Font Pairing Guidelines**:

```markdown
Recommended Pairings:

Professional:
- Headings: Helvetica Bold
- Body: Open Sans Regular

Modern:
- Headings: Montserrat Bold
- Body: Lato Regular

Classic:
- Headings: Georgia Bold
- Body: Arial Regular

Tech:
- Headings: Roboto Bold
- Body: Source Sans Pro Regular
```

## 📝 Content Customization

### Replacing Placeholder Content

**Systematic Replacement Checklist**:

```markdown
Find and Replace:
- [ ] [COMPANY NAME] → Your Company Name
- [ ] [PROJECT NAME] → Your Project Name
- [ ] [DATE] → Current Date
- [ ] [PRESENTER] → Your Name
- [ ] [DEPARTMENT] → Your Department
- [ ] [PHONE/EMAIL] → Your Contact Info
- [ ] [WEBSITE] → Your Website
- [ ] [LOGO] → Your Logo Image
```

**PowerPoint Find & Replace**:
```text
Home → Replace (Ctrl+H)
- Find what: [COMPANY NAME]
- Replace with: Acme Corporation
- Replace All
```

### Industry-Specific Customization

**Vertical Market Examples**:

**Healthcare**:
```markdown
Replace Generic Terms:
- "Customer" → "Patient" or "Provider"
- "User" → "Clinician" or "Care Team"
- "Sales" → "Patient Care" or "Clinical Services"
- Add HIPAA compliance references
- Include healthcare-specific use cases
```

**Financial Services**:
```markdown
Replace Generic Terms:
- "Customer" → "Client" or "Account Holder"
- "Product" → "Financial Product" or "Service"
- Add compliance references (SOX, PCI-DSS)
- Include financial use cases
- Emphasize security and compliance
```

**Retail**:
```markdown
Replace Generic Terms:
- "User" → "Shopper" or "Customer"
- "Analytics" → "Customer Insights"
- Add retail-specific metrics (foot traffic, conversion)
- Include omnichannel examples
- Emphasize personalization
```

### Data and Metrics Customization

**Replacing Sample Data**:

**Charts and Graphs**:
```text
1. Select chart
2. Right-click → Edit Data
3. Replace sample data with actual data
4. Update chart title and labels
5. Adjust scale and formatting
6. Verify data accuracy
```

**Tables**:
```markdown
Best Practices:
- Use actual company metrics
- Include source citations
- Update timestamps
- Verify calculations
- Format consistently ($ vs %, etc.)
```

**Example Metrics Replacement**:

```markdown
Before:
"40% cost reduction"
"60% faster time-to-insight"
"99.9% uptime"

After (customize with your data):
"23% operational cost reduction in Q1 2024"
"2 hours vs. 2 weeks for standard reports"
"99.97% uptime over 12-month period"
```

## 🖼️ Visual Asset Customization

### Image Replacement

**Corporate Photography**:

```text
Replace generic images:
1. Delete placeholder image
2. Insert → Pictures → Select corporate photo
3. Crop to appropriate aspect ratio
4. Apply consistent style (filter/overlay if needed)
5. Compress for file size optimization
```

**Image Style Consistency**:
```markdown
Maintain Consistency:
- Color treatment: Apply corporate color overlay
- Aspect ratios: Maintain standard ratios (16:9, 4:3, 1:1)
- Resolution: 150 DPI minimum
- File format: PNG for logos, JPEG for photos
- Compression: Optimize but maintain quality
```

### Diagram Customization

**Architecture Diagrams**:

```text
Customization Steps:
1. Ungroup diagram elements
2. Replace generic labels with actual system names
3. Update colors to match corporate palette
4. Adjust component names and descriptions
5. Regroup elements
6. Test accessibility (color contrast)
```

**Icon Replacement**:
```markdown
Options:
- Use corporate icon library
- Download from approved sources (Fluent, Heroicons)
- Maintain consistent style throughout
- Ensure license compliance
- Resize to standard dimensions
```

## 📊 Chart and Data Visualization Customization

### Chart Templates

**Creating Reusable Chart Templates**:

```text
1. Format chart with corporate colors and fonts
2. Right-click chart → Save as Template
3. Save to Templates folder
4. Apply to future charts:
   - Right-click chart → Change Chart Type
   - Templates → [Your Template Name]
```

**Corporate Chart Style**:

```markdown
Chart Elements Checklist:
- [ ] Colors match corporate palette
- [ ] Font matches corporate font
- [ ] Data labels readable (18pt minimum)
- [ ] Legend positioned consistently
- [ ] Grid lines subtle (light gray)
- [ ] Chart title descriptive
- [ ] Axis labels clear with units
- [ ] High contrast for accessibility
```

### Data Table Styling

**Corporate Table Format**:

```text
Table Design:
- Header row: Corporate primary color
- Header text: White, bold
- Alternating rows: Light gray and white
- Border: 1pt solid corporate primary
- Font: Corporate font, 20-22pt
- Alignment: Left for text, right for numbers
```

## 🎬 Animation and Transition Customization

### Corporate Animation Style

**Animation Templates**:

```markdown
Conservative (Finance, Legal):
- Transitions: Fade only
- Animations: Appear, minimal use
- Duration: 0.5 seconds
- Trigger: On Click

Modern (Tech, Startup):
- Transitions: Fade, Morph
- Animations: Wipe, Zoom
- Duration: 0.75 seconds
- Trigger: Mix of On Click and Auto

Dynamic (Sales, Marketing):
- Transitions: Push, Fade, Morph
- Animations: Fly In, Grow, Emphasis
- Duration: 0.5-1.0 seconds
- Trigger: Mostly On Click
```

### Timing Customization

**Presentation Pacing**:

```markdown
Adjust for Different Scenarios:

Executive Brief (15 min):
- Slides: 10-12 maximum
- Pace: 75-90 seconds per slide
- Q&A: Reserve 5 minutes

Technical Deep Dive (60 min):
- Slides: 30-40
- Pace: 90-120 seconds per slide
- Demos: 15-20 minutes
- Q&A: 10-15 minutes

Workshop (4 hours):
- Slides: 60-80
- Pace: Variable (2-5 min per slide)
- Activities: 50% of time
- Breaks: Every 60-90 minutes
```

## 🔗 Link and Navigation Customization

### Custom Navigation

**Agenda Slide with Hyperlinks**:

```text
Create Interactive Agenda:
1. Create agenda slide
2. Select text for each section
3. Insert → Link → Place in This Document
4. Select target slide
5. Test all links
6. Add "Return to Agenda" buttons on section slides
```

**Footer Customization**:

```text
Insert → Header & Footer:
- Slide number: ✅ Enabled
- Footer text: [Company Name] - Confidential
- Date: Auto-update or fixed date
- Apply to all or exclude title slide
```

## 📱 Format-Specific Customization

### PDF Handouts

**Creating Custom PDF Handouts**:

```text
1. File → Export → Create Handouts
2. Layout options:
   - Notes Pages (1 slide + notes per page)
   - Outline View (text only)
   - Handouts (2, 3, 4, 6, or 9 slides per page)
3. Add header/footer
4. Export as PDF
```

**PDF Customization**:
```markdown
Settings:
- Include: Notes, hidden slides (optional)
- Quality: High (300 DPI)
- Fonts: Embedded
- Bookmarks: From slide titles
- Properties: Add metadata (title, author, keywords)
```

### Video Export Customization

**Recording Settings**:

```text
Slide Show → Record Slide Show

Options:
- Narrations: ✅ Record voiceover
- Timings: ✅ Record slide timings
- Ink & Laser: ✅ Include annotations
- Camera: ⬜ (Optional)

Export:
- File → Export → Create Video
- Quality: Full HD (1920×1080)
- Timing: Use recorded timings
```

## 🧪 Testing Customized Presentations

### Quality Assurance Checklist

**Visual Review**:
- [ ] All placeholders replaced
- [ ] Colors consistent throughout
- [ ] Fonts render correctly
- [ ] Images high quality and relevant
- [ ] Logo positioned correctly
- [ ] Contact information accurate

**Content Review**:
- [ ] Data and metrics accurate
- [ ] Terminology consistent
- [ ] No typos or grammar errors
- [ ] Links functional
- [ ] Slide numbers sequential

**Technical Review**:
- [ ] File size optimized
- [ ] Fonts embedded
- [ ] Animations tested
- [ ] Transitions appropriate
- [ ] Accessibility checker passed
- [ ] Tested on target platform

**Cross-Platform Testing**:
```markdown
Test On:
- Windows PowerPoint 2016+
- macOS PowerPoint
- PowerPoint Online
- PDF reader
- Target presentation display
```

## 💾 Saving Custom Templates

### Creating Organization Templates

**Save as Template**:

```text
1. Customize presentation fully
2. Delete content slides (keep masters)
3. File → Save As
4. File type: PowerPoint Template (.potx)
5. Location: Organization template folder
6. Name: [Company]-[Type]-Template-v1.0.potx
```

**Template Distribution**:

```markdown
Distribution Methods:
- SharePoint template library
- OneDrive shared folder
- Corporate intranet
- Email to team members
- Add to PowerPoint template gallery
```

### Version Control

**Template Versioning**:

```text
Naming Convention:
[Company]-[Type]-Template-v[Major].[Minor].potx

Examples:
Acme-Executive-Template-v1.0.potx
Acme-Technical-Template-v1.1.potx
Acme-Sales-Template-v2.0.potx

Version Log:
v1.0 - Initial release
v1.1 - Updated color palette
v2.0 - Major redesign with new branding
```

## 📋 Customization Checklist

### Complete Customization Checklist

**Branding**:
- [ ] Corporate logo added
- [ ] Color scheme updated
- [ ] Fonts customized
- [ ] Footer/header customized

**Content**:
- [ ] All placeholders replaced
- [ ] Industry-specific terminology
- [ ] Actual data and metrics
- [ ] Corporate examples

**Visuals**:
- [ ] Images replaced
- [ ] Diagrams customized
- [ ] Icons updated
- [ ] Charts styled

**Technical**:
- [ ] Fonts embedded
- [ ] File optimized
- [ ] Accessibility verified
- [ ] Cross-platform tested

**Distribution**:
- [ ] Template saved
- [ ] Version documented
- [ ] Shared with team
- [ ] Usage guide created

## 💬 Feedback

Questions about customization?

[Get Help](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?title=[Help]+Customization)

## 📖 Related Documentation

- [Brand Guidelines](brand-guidelines.md)
- [Best Practices](best-practices.md)
- [Accessibility Guide](accessibility.md)
- [Export Settings](export-settings.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
