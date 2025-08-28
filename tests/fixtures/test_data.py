"""Test data and fixtures for CSA docs testing."""

from pathlib import Path
import tempfile
import shutil

# Sample markdown content with various issues for testing
SAMPLE_MARKDOWN_WITH_ISSUES = """---
title: Test Document
author: Test Author
date: 2024-01-01
---

# Test Document

This is a test document with various markdown quality issues.

## Section with Problems

This line is way too long and exceeds any reasonable line length limit that might be set for markdown linting purposes and should definitely trigger warnings about line length violations.

This line has trailing spaces.   

There are too many empty lines below:




### Inconsistent Heading (skipping H3)

Here's a [broken link](nonexistent.md) and ![missing image](missing.png).

```
Code block without language specification
```

| Bad | Table |
|-----|
| Missing cell |

####### Too many heading levels

The image below has no alt text:
![](../images/test.png)

This has redundant alt text:
![Image of a diagram showing the architecture](diagram.png)
"""

SAMPLE_GOOD_MARKDOWN = """# Good Document

This is a well-formatted document that follows best practices.

## Proper Section

Here's a [valid link](./other.md) and ![good image](../images/chart.png "Chart showing data").

### Code Example

```python
def example():
    return "Hello, world!"
```

### Table

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |

## Conclusion

This document demonstrates proper formatting and structure.
"""

# MkDocs configuration templates
GOOD_MKDOCS_CONFIG = {
    'site_name': 'Test Documentation',
    'docs_dir': 'docs',
    'site_dir': 'site',
    'theme': {
        'name': 'material',
        'features': ['navigation.tabs']
    },
    'nav': [
        {'Home': 'index.md'},
        {'Guide': [
            {'Getting Started': 'guide/getting-started.md'},
            {'Advanced': 'guide/advanced.md'}
        ]},
        {'Reference': 'reference.md'}
    ],
    'plugins': ['search'],
    'markdown_extensions': [
        'pymdownx.highlight',
        'pymdownx.superfences'
    ]
}

BAD_MKDOCS_CONFIG = {
    # Missing required fields
    'theme': 'material',
    'nav': [
        {'Home': 'nonexistent.md'},  # Missing file
        {'Section': [
            {'Bad': 'also-missing.md'}
        ]}
    ]
}

# Sample HTML with various link types
HTML_WITH_LINKS = """<!DOCTYPE html>
<html>
<head>
    <title>Test HTML</title>
</head>
<body>
    <h1>Link Test Page</h1>
    
    <p>Here are various types of links:</p>
    <ul>
        <li><a href="https://example.com">External link</a></li>
        <li><a href="./relative.html">Relative link</a></li>
        <li><a href="/absolute.html">Absolute link</a></li>
        <li><a href="#anchor">Anchor link</a></li>
        <li><a href="mailto:test@example.com">Email link</a></li>
        <li><a href="broken-link.html">Broken link</a></li>
    </ul>
    
    <p>Images:</p>
    <img src="existing-image.png" alt="Existing image">
    <img src="missing-image.png" alt="Missing image">
    <img src="https://example.com/external.jpg" alt="External image">
    
    <h2 id="anchor">Anchor Section</h2>
    <p>This is the anchor target.</p>
</body>
</html>
"""

def create_test_documentation_structure(root_dir: Path):
    """Create a comprehensive test documentation structure."""
    docs_dir = root_dir / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    # Create main index
    (docs_dir / "index.md").write_text(SAMPLE_GOOD_MARKDOWN)
    
    # Create problematic document
    (docs_dir / "problematic.md").write_text(SAMPLE_MARKDOWN_WITH_ISSUES)
    
    # Create guide section
    guide_dir = docs_dir / "guide"
    guide_dir.mkdir(exist_ok=True)
    
    (guide_dir / "getting-started.md").write_text("""# Getting Started

Welcome to the getting started guide.

## Prerequisites

You'll need:
- Python 3.9+
- pip
- Git

## Installation

```bash
pip install -r requirements.txt
```

See the [advanced guide](./advanced.md) for more details.

![Setup diagram](../images/setup.png "Setup process diagram")
""")
    
    (guide_dir / "advanced.md").write_text("""# Advanced Guide

This covers advanced topics.

## Configuration

Edit the configuration file:

```yaml
# config.yml
debug: true
port: 8000
```

## Troubleshooting

Check the [FAQ](../faq.md) for common issues.

![Troubleshooting flowchart](../images/troubleshooting.svg "Troubleshooting process")
""")
    
    # Create reference
    (docs_dir / "reference.md").write_text("""# Reference

## API Documentation

### Functions

#### `process_data(data: list) -> dict`

Processes input data and returns results.

**Parameters:**
- `data`: List of items to process

**Returns:**
- Dictionary with processed results

**Example:**
```python
result = process_data([1, 2, 3, 4])
print(result)  # {'count': 4, 'sum': 10}
```
""")
    
    # Create FAQ (orphaned file not in navigation)
    (docs_dir / "faq.md").write_text("""# Frequently Asked Questions

## General Questions

### Q: How do I get help?

A: Check the documentation or file an issue.

### Q: What versions are supported?

A: Python 3.9+ is required.
""")
    
    # Create images directory
    images_dir = docs_dir / "images"
    images_dir.mkdir(exist_ok=True)
    
    # Create sample PNG (1x1 pixel)
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    (images_dir / "setup.png").write_bytes(png_data)
    (images_dir / "chart.png").write_bytes(png_data)
    (images_dir / "unused-image.png").write_bytes(png_data)  # Unused image
    
    # Create sample SVG
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="200" height="100" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="180" height="80" fill="lightblue" stroke="blue" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial" font-size="16">Troubleshooting</text>
</svg>'''
    (images_dir / "troubleshooting.svg").write_text(svg_content)
    
    # Create assets directory with non-image files
    assets_dir = docs_dir / "assets"
    assets_dir.mkdir(exist_ok=True)
    (assets_dir / "style.css").write_text("/* Custom styles */\n.highlight { background: yellow; }")
    (assets_dir / "script.js").write_text("// Custom JavaScript\nconsole.log('Loaded');")
    
    return docs_dir


def create_test_mkdocs_config(root_dir: Path, config_data: dict):
    """Create mkdocs.yml configuration file."""
    import yaml
    
    config_file = root_dir / "mkdocs.yml"
    with open(config_file, 'w') as f:
        yaml.dump(config_data, f, default_flow_style=False)
    
    return config_file


def create_markdownlint_config(root_dir: Path):
    """Create .markdownlint.json configuration."""
    import json
    
    config = {
        "MD013": {"line_length": 120},  # Line length
        "MD033": False,  # Allow HTML
        "MD041": False,  # First line in file should be top level header
        "MD025": False,  # Multiple top level headers
        "MD024": {"allow_different_nesting": True}  # Multiple headers with same content
    }
    
    config_file = root_dir / ".markdownlint.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config_file


class TemporaryDocumentationSite:
    """Context manager for creating temporary documentation sites for testing."""
    
    def __init__(self, config_type="good"):
        self.config_type = config_type
        self.temp_dir = None
        self.docs_dir = None
        
    def __enter__(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Create documentation structure
        self.docs_dir = create_test_documentation_structure(self.temp_dir)
        
        # Create mkdocs config
        if self.config_type == "good":
            create_test_mkdocs_config(self.temp_dir, GOOD_MKDOCS_CONFIG)
        elif self.config_type == "bad":
            create_test_mkdocs_config(self.temp_dir, BAD_MKDOCS_CONFIG)
        
        # Create markdownlint config
        create_markdownlint_config(self.temp_dir)
        
        return self.temp_dir
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)


# Test scenarios for different validation types
TEST_SCENARIOS = {
    "perfect_docs": {
        "description": "Perfect documentation with no issues",
        "expected_quality_score": 100.0,
        "expected_image_health": 100.0,
        "expected_nav_health": 100.0,
        "expected_broken_links": 0
    },
    "problematic_docs": {
        "description": "Documentation with various quality issues",
        "expected_quality_score": 60.0,  # Lower due to issues
        "expected_image_health": 80.0,   # Some image issues
        "expected_nav_health": 90.0,     # Minor navigation issues
        "expected_broken_links": 2       # Some broken links
    },
    "broken_build": {
        "description": "Documentation that fails to build",
        "build_should_fail": True,
        "config_valid": False
    }
}


# Performance test data
def generate_large_markdown_content(sections: int = 50) -> str:
    """Generate large markdown content for performance testing."""
    content = ["# Large Test Document\n", "This document is used for performance testing.\n"]
    
    for i in range(sections):
        content.extend([
            f"\n## Section {i+1}\n",
            f"This is section {i+1} with some content.\n",
            f"It includes various markdown elements.\n\n",
            f"### Subsection {i+1}.1\n",
            f"Here's a [link to section {i}](#{i}) and ![image](../images/test_{i}.png).\n\n",
            f"```python\n",
            f"def section_{i+1}_function():\n",
            f'    return "Section {i+1} result"\n',
            f"```\n\n",
            f"| Column 1 | Column 2 | Column 3 |\n",
            f"|----------|----------|----------|\n",
            f"| Value {i*3+1} | Value {i*3+2} | Value {i*3+3} |\n\n"
        ])
    
    return "".join(content)


# Utility functions for test setup
def create_broken_image_file(path: Path):
    """Create a broken/corrupted image file."""
    path.write_bytes(b"This is not a valid image file")


def create_large_image_file(path: Path, size_mb: int = 10):
    """Create a large image file for testing."""
    # Create a basic PNG header then pad with data
    png_header = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
    padding = b'\x00' * (size_mb * 1024 * 1024 - len(png_header))
    png_end = b'\x00\x00\x00\x00IEND\xaeB`\x82'
    
    path.write_bytes(png_header + padding + png_end)


def create_invalid_yaml_config(path: Path):
    """Create an invalid YAML configuration file."""
    path.write_text("""
site_name: Test Site
invalid_yaml_structure:
  - item1
  - item2
    - nested_item  # Invalid indentation
theme:
  name: material
  features: [
    navigation.tabs
    # Missing comma
    navigation.sections
  ]
nav:
  - Home: index.md
  - Section:
    - Page 1: page1.md
    - Page 2: page2.md
    - Page 3: page3.md
""")


# Error simulation utilities
class SimulatedError:
    """Utility for simulating various error conditions in tests."""
    
    @staticmethod
    def network_timeout():
        """Simulate network timeout for link validation."""
        import asyncio
        raise asyncio.TimeoutError("Simulated network timeout")
    
    @staticmethod
    def file_permission_error():
        """Simulate file permission error."""
        raise PermissionError("Simulated permission denied")
    
    @staticmethod
    def invalid_image_error():
        """Simulate invalid image file error."""
        from PIL import Image
        raise Image.UnidentifiedImageError("Simulated invalid image")
    
    @staticmethod
    def yaml_parsing_error():
        """Simulate YAML parsing error."""
        import yaml
        raise yaml.YAMLError("Simulated YAML parsing error")


# Benchmark data for performance testing
PERFORMANCE_BENCHMARKS = {
    "small_site": {
        "files": 10,
        "images": 5,
        "max_build_time": 5.0,
        "max_quality_check_time": 2.0,
        "max_link_check_time": 3.0
    },
    "medium_site": {
        "files": 100,
        "images": 50,
        "max_build_time": 15.0,
        "max_quality_check_time": 10.0,
        "max_link_check_time": 20.0
    },
    "large_site": {
        "files": 500,
        "images": 200,
        "max_build_time": 60.0,
        "max_quality_check_time": 30.0,
        "max_link_check_time": 120.0
    }
}