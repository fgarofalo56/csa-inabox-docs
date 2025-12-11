#!/usr/bin/env python3
"""
Generate multimedia presentation and template documentation files
for CSA-in-a-Box project
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
PRESENTATIONS_DIR = BASE_DIR / "docs" / "multimedia" / "presentations"
TEMPLATES_DIR = BASE_DIR / "docs" / "multimedia" / "templates"

# Presentation files to create
PRESENTATIONS = {
    "best-practices-deck.md": {
        "title": "Best Practices Deck",
        "type": "Technical",
        "duration": "45 min",
        "audience": "Practitioners",
        "description": "Comprehensive deck covering Azure Synapse Analytics best practices, optimization techniques, and implementation patterns."
    },
    "conference-talks.md": {
        "title": "Conference Talks",
        "type": "Public",
        "duration": "30-45 min",
        "audience": "General",
        "description": "Public-facing presentations for conferences and community events showcasing CSA capabilities."
    },
    "cost-benefit-analysis.md": {
        "title": "Cost-Benefit Analysis",
        "type": "Financial",
        "duration": "30 min",
        "audience": "Finance, Leadership",
        "description": "Detailed cost-benefit analysis presentation with ROI calculations and financial justifications."
    },
    "customer-success.md": {
        "title": "Customer Success Stories",
        "type": "Sales",
        "duration": "15-20 min",
        "audience": "Prospects, Customers",
        "description": "Real-world customer success stories, case studies, and testimonials demonstrating CSA value."
    },
    "industry-solutions.md": {
        "title": "Industry Solutions",
        "type": "Vertical",
        "duration": "30 min",
        "audience": "Vertical Markets",
        "description": "Industry-specific solutions for healthcare, financial services, retail, and manufacturing."
    },
    "migration-planning.md": {
        "title": "Migration Planning",
        "type": "Technical",
        "duration": "60 min",
        "audience": "Technical Teams",
        "description": "Comprehensive migration planning guide from legacy systems to Azure Synapse Analytics."
    },
    "partner-enablement.md": {
        "title": "Partner Enablement",
        "type": "Training",
        "duration": "60 min",
        "audience": "Partners",
        "description": "Partner enablement materials for system integrators and solution partners."
    },
    "roadmap-presentation.md": {
        "title": "Roadmap Presentation",
        "type": "Strategic",
        "duration": "30 min",
        "audience": "All Stakeholders",
        "description": "Product roadmap, future capabilities, and strategic direction for CSA platform."
    },
    "sales-enablement.md": {
        "title": "Sales Enablement",
        "type": "Sales",
        "duration": "20-30 min",
        "audience": "Sales Teams",
        "description": "Sales enablement deck with positioning, competitive intelligence, and demo scripts."
    },
    "security-compliance.md": {
        "title": "Security & Compliance",
        "type": "Security",
        "duration": "45 min",
        "audience": "Security Teams",
        "description": "Comprehensive security architecture, compliance frameworks, and governance model."
    },
    "training-decks.md": {
        "title": "Training Decks",
        "type": "Training",
        "duration": "Variable",
        "audience": "All Levels",
        "description": "Modular training materials for different roles and skill levels."
    },
    "workshop-materials.md": {
        "title": "Workshop Materials",
        "type": "Workshop",
        "duration": "4-8 hours",
        "audience": "Practitioners",
        "description": "Hands-on workshop materials with exercises, labs, and practical implementations."
    }
}

# Resource README directories
RESOURCE_DIRS = {
    "resources/animations/charts": "Chart animation resources and templates",
    "resources/animations/objects": "Object animation resources and effects",
    "resources/animations/text": "Text animation resources and transitions",
    "resources/animations/transitions": "Slide transition resources and effects",
    "resources/backgrounds": "Background images and templates",
    "resources/charts": "Chart templates and styles",
    "resources/diagrams": "Architecture diagram templates",
    "resources/icons": "Icon libraries and assets",
    "resources/layouts": "Slide layout templates"
}

# Template README directories
TEMPLATE_DIRS = {
    "executive": "Executive presentation templates",
    "sales": "Sales and marketing presentation templates",
    "technical": "Technical presentation templates",
    "training": "Training and workshop templates"
}

def create_presentation_file(filename, metadata):
    """Create a presentation markdown file"""
    filepath = PRESENTATIONS_DIR / filename

    content = f"""# 📊 {metadata['title']} - CSA-in-a-Box

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **📊 [Presentations](README.md)** | **👤 {metadata['title']}**

![Type: {metadata['type']}](https://img.shields.io/badge/Type-{metadata['type'].replace(' ', '%20')}-blue)
![Duration: {metadata['duration']}](https://img.shields.io/badge/Duration-{metadata['duration'].replace(' ', '%20')}-green)
![Audience: {metadata['audience']}](https://img.shields.io/badge/Audience-{metadata['audience'].replace(' ', '%20').replace(',', '%2C')}-purple)

## 📋 Overview

{metadata['description']}

## 🎯 Presentation Objectives

- Deliver comprehensive {metadata['title'].lower()} content
- Engage {metadata['audience'].lower()} effectively
- Demonstrate value and capabilities
- Enable decision-making and action

## 🎬 Slide Deck Outline

### Opening (Slides 1-3)

#### Slide 1: Title Slide

**Content**:
- {metadata['title']}
- Cloud Scale Analytics in-a-Box
- [Presenter Name], [Title]
- [Date]

**Speaker Notes**: Set context and objectives for this presentation.

---

#### Slide 2: Agenda

**Content**:
1. 🎯 Overview
2. 💡 Key Capabilities
3. 📊 Value Proposition
4. 🚀 Next Steps

**Speaker Notes**: Brief overview of presentation structure.

---

#### Slide 3: Executive Summary

**Content**:
- Overview of {metadata['title'].lower()}
- Key benefits and outcomes
- Success metrics

**Speaker Notes**: High-level summary of key messages.

---

## 📚 Content Sections

### Main Content

This presentation covers:

1. **Introduction**: Background and context
2. **Core Content**: Detailed information and examples
3. **Value Demonstration**: ROI and benefits
4. **Implementation**: Practical steps and guidance
5. **Q&A**: Interactive discussion

### Key Messages

- Message 1: [Customize based on audience]
- Message 2: [Customize based on use case]
- Message 3: [Customize based on objectives]

## 🎯 Delivery Guidelines

### Audience Considerations

**{metadata['audience']}**:
- Tailor technical depth appropriately
- Use relevant examples and case studies
- Address specific concerns and interests
- Allow time for questions and discussion

### Timing

**Duration: {metadata['duration']}**:
- Introduction: 10%
- Main content: 70%
- Q&A and wrap-up: 20%

## 📋 Customization Notes

### Required Updates

- [ ] Add company-specific data and metrics
- [ ] Include relevant case studies
- [ ] Customize examples for industry
- [ ] Update logos and branding
- [ ] Verify all links and references

### Optional Enhancements

- Add customer testimonials
- Include live demonstrations
- Incorporate industry statistics
- Add interactive polls or surveys

## 📖 Related Resources

### Documentation
- [Executive Overview](executive-overview.md)
- [Technical Deep Dive](technical-deep-dive.md)
- [Presentation Guides](guides/README.md)

### Templates
- PowerPoint template: [Download](../templates/)
- PDF handout template: [Download](../templates/)
- Speaker notes template: [Download](../templates/)

## 💬 Feedback

Help us improve this presentation:

- Was the content appropriate for the audience?
- What additional topics should be covered?
- How can we improve delivery effectiveness?

[Provide Feedback](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?title=[Feedback]+{metadata['title'].replace(' ', '-')})

---

*Last Updated: January 2025 | Version: 1.0.0*

**Note**: This presentation outline should be customized with specific content, data, and examples relevant to your organization and audience.
"""

    filepath.write_text(content, encoding='utf-8')
    print(f"Created: {filepath}")

def create_resource_readme(subdir, description):
    """Create README for resource directories"""
    filepath = PRESENTATIONS_DIR / subdir / "README.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)

    dir_name = subdir.split('/')[-1].replace('-', ' ').title()
    category = '/'.join(subdir.split('/')[1:-1]).title()

    content = f"""# 📚 {dir_name} Resources - CSA-in-a-Box

> **🏠 [Home](../../../../../README.md)** | **📖 [Documentation](../../../../README.md)** | **🎬 [Multimedia](../../../README.md)** | **📊 [Presentations](../../README.md)** | **📦 Resources** | **👤 {dir_name}**

![Type: Resources](https://img.shields.io/badge/Type-Resources-blue)
![Category: {category}](https://img.shields.io/badge/Category-{category.replace(' ', '%20')}-green)

## 📋 Overview

{description} for Cloud Scale Analytics presentations.

## 📦 Available Resources

### Asset Types

This directory contains:

- Templates and examples
- Reusable components
- Best practice implementations
- Azure-branded assets

### Usage Guidelines

**Access**:
- Browse available assets
- Download needed resources
- Follow brand guidelines
- Maintain attribution

**Customization**:
- Adapt to your needs
- Follow accessibility standards
- Test thoroughly
- Document modifications

## 🎨 Asset Standards

### Quality Requirements

**All assets must meet**:
- [ ] High resolution (150 DPI minimum)
- [ ] Proper format (PNG/SVG for graphics)
- [ ] Brand compliance
- [ ] Accessibility standards
- [ ] License compliance

### File Organization

```text
{subdir}/
├── templates/          # Reusable templates
├── examples/          # Example implementations
├── azure/             # Azure-branded assets
└── custom/            # Custom/specialized assets
```

## 📚 Documentation

### Guidelines

- [Brand Guidelines](../../guides/brand-guidelines.md)
- [Accessibility Guide](../../guides/accessibility.md)
- [Best Practices](../../guides/best-practices.md)

### Related Resources

- [Other Resource Categories](../README.md)
- [Presentation Templates](../../../templates/README.md)
- [Multimedia Index](../../../MULTIMEDIA_INDEX.md)

## 💡 Tips and Best Practices

### Effective Usage

1. **Review brand guidelines** before using assets
2. **Test accessibility** of all visual elements
3. **Optimize file sizes** for performance
4. **Document customizations** for future reference
5. **Share improvements** with the community

### Common Pitfalls

- ❌ Using low-resolution assets
- ❌ Ignoring brand guidelines
- ❌ Skipping accessibility checks
- ❌ Overusing animations or effects
- ❌ Not testing on target platform

## 🔄 Contributing

### Adding New Resources

Have resources to contribute?

1. Follow quality standards
2. Include documentation
3. Verify licensing
4. Submit for review

[Contribute Resources](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?title=[Resource]+{dir_name.replace(' ', '-')})

## 💬 Feedback

Help us improve this resource library:

- Are the resources helpful and high-quality?
- What additional assets would be valuable?
- Have suggestions for better organization?

[Provide Feedback](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?title=[Feedback]+{dir_name.replace(' ', '-')}-Resources)

---

*Last Updated: January 2025 | Version: 1.0.0*

**Note**: New resources are added regularly. Check back for updates or star the repository for notifications.
"""

    filepath.write_text(content, encoding='utf-8')
    print(f"Created: {filepath}")

def create_template_readme(subdir, description):
    """Create README for template directories"""
    filepath = TEMPLATES_DIR / subdir / "README.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)

    dir_name = subdir.replace('-', ' ').title()

    content = f"""# 📑 {dir_name} Templates - CSA-in-a-Box

> **🏠 [Home](../../../../README.md)** | **📖 [Documentation](../../../README.md)** | **🎬 [Multimedia](../../README.md)** | **📋 [Templates](../README.md)** | **👤 {dir_name}**

![Type: Templates](https://img.shields.io/badge/Type-Templates-blue)
![Category: {dir_name}](https://img.shields.io/badge/Category-{dir_name.replace(' ', '%20')}-purple)

## 📋 Overview

{description} for Cloud Scale Analytics presentations and documentation.

## 📦 Available Templates

### Template Types

**PowerPoint Templates**:
- Master slide templates
- Pre-designed layouts
- Branded color schemes
- Standard fonts embedded

**Supporting Materials**:
- Speaker notes templates
- Handout layouts
- PDF export templates
- Video recording templates

## 🎯 Template Usage

### Getting Started

**Quick Start**:
1. Download template file
2. Save as new presentation
3. Replace placeholder content
4. Customize as needed
5. Follow brand guidelines

**Customization**:
- Update company information
- Add specific data and metrics
- Include relevant case studies
- Adjust timing and flow
- Test accessibility

### Target Audience

**{dir_name} presentations** are designed for:
- Specific audience needs
- Appropriate technical depth
- Relevant messaging and positioning
- Expected duration and format

## 🎨 Design Standards

### Brand Compliance

**All templates follow**:
- Azure color palette
- Microsoft branding guidelines
- Segoe UI typography
- 16:9 aspect ratio
- Accessibility standards (WCAG 2.1 AA)

### Layout Structure

```text
Slide Layouts Included:
├── Title Slide
├── Agenda
├── Section Header
├── Content (1 column)
├── Content (2 columns)
├── Chart/Graph
├── Diagram
├── Quote/Testimonial
├── Q&A
└── Closing/Contact
```

## 📚 Documentation

### Guides

- [Customization Guide](../../presentations/guides/customization.md)
- [Brand Guidelines](../../presentations/guides/brand-guidelines.md)
- [Accessibility Guide](../../presentations/guides/accessibility.md)
- [Export Settings](../../presentations/guides/export-settings.md)

### Examples

- [Executive Overview](../../presentations/executive-overview.md)
- [Technical Deep Dive](../../presentations/technical-deep-dive.md)

## 💡 Best Practices

### Template Usage

**Do**:
- ✅ Use built-in layouts
- ✅ Maintain consistent branding
- ✅ Test all animations
- ✅ Verify accessibility
- ✅ Embed fonts for distribution

**Don't**:
- ❌ Override master slides
- ❌ Use off-brand colors
- ❌ Exceed recommended slide count
- ❌ Skip accessibility checks
- ❌ Forget to customize placeholders

### Quality Checklist

Before using template:
- [ ] Reviewed target audience needs
- [ ] Understood presentation objectives
- [ ] Checked duration requirements
- [ ] Verified technical setup
- [ ] Planned customization approach

## 🔄 Template Updates

### Versioning

Templates are versioned for tracking:
- Major versions: Significant redesigns
- Minor versions: Small improvements
- Check for latest version regularly

### Update Notifications

- Watch repository for updates
- Subscribe to release notes
- Join community discussions

## 📞 Support

### Getting Help

**Questions?**
- [Template FAQ](../README.md#faq)
- [Community Discussions](https://github.com/fgarofalo56/csa-inabox-docs/discussions)
- [Issue Tracker](https://github.com/fgarofalo56/csa-inabox-docs/issues)

**Custom Requirements?**
- Request custom templates
- Propose enhancements
- Share feedback

## 💬 Feedback

Help us improve these templates:

- Are the templates meeting your needs?
- What additional templates would be valuable?
- How can we improve usability?

[Provide Feedback](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?title=[Feedback]+{dir_name.replace(' ', '-')}-Templates)

---

*Last Updated: January 2025 | Version: 1.0.0*

**Note**: Templates are updated regularly based on user feedback and evolving best practices.
"""

    filepath.write_text(content, encoding='utf-8')
    print(f"Created: {filepath}")

def main():
    """Generate all multimedia documentation files"""
    print("Generating multimedia documentation files...\n")

    # Create presentation files
    print("Creating presentation files...")
    for filename, metadata in PRESENTATIONS.items():
        create_presentation_file(filename, metadata)

    # Create resource README files
    print("\nCreating resource README files...")
    for subdir, description in RESOURCE_DIRS.items():
        create_resource_readme(subdir, description)

    # Create template README files
    print("\nCreating template README files...")
    for subdir, description in TEMPLATE_DIRS.items():
        create_template_readme(subdir, description)

    print("\n✅ All multimedia documentation files created successfully!")
    print(f"\nTotal files created:")
    print(f"  - Presentations: {len(PRESENTATIONS)}")
    print(f"  - Resource READMEs: {len(RESOURCE_DIRS)}")
    print(f"  - Template READMEs: {len(TEMPLATE_DIRS)}")
    print(f"  - Total: {len(PRESENTATIONS) + len(RESOURCE_DIRS) + len(TEMPLATE_DIRS)}")

if __name__ == "__main__":
    main()
