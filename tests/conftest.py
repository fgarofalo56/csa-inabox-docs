"""Pytest configuration and fixtures for CSA docs testing."""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import yaml
import asyncio
import aiohttp

# Import the classes we're testing
from src.csa_docs_tools import (
    DocumentationBuildTester,
    LinkValidator,
    MarkdownQualityChecker,
    ImageReferenceValidator,
    NavigationStructureValidator
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_docs_root():
    """Create a temporary documentation directory structure for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        docs_root = Path(temp_dir)
        
        # Create basic directory structure
        docs_dir = docs_root / "docs"
        docs_dir.mkdir()
        
        # Create sample markdown files
        (docs_dir / "index.md").write_text("""# Welcome to CSA Docs

This is the main documentation for Azure Synapse Analytics.

## Getting Started

Check out our [architecture guide](architecture/overview.md) to begin.

![Architecture Diagram](images/architecture.png "Azure Synapse Architecture")

## Code Example

```python
import azure.synapse as synapse

# Initialize connection
client = synapse.Client()
```

## Links

- [Azure Portal](https://portal.azure.com)
- [Internal Link](./tutorials/getting-started.md)
- [Broken Link](./nonexistent.md)
""")

        # Create architecture section
        arch_dir = docs_dir / "architecture"
        arch_dir.mkdir()
        (arch_dir / "overview.md").write_text("""# Architecture Overview

This section covers the overall architecture patterns.

## Delta Lakehouse

See [delta lakehouse details](../delta-lake/overview.md).

![Delta Architecture](../images/delta-architecture.svg)
""")

        # Create tutorials section
        tutorials_dir = docs_dir / "tutorials"
        tutorials_dir.mkdir()
        (tutorials_dir / "getting-started.md").write_text("""# Getting Started Tutorial

This tutorial will help you get started.

## Prerequisites

You need:
- Azure subscription
- Synapse workspace

![Prerequisites](../images/prerequisites.png)
""")

        # Create images directory and files
        images_dir = docs_dir / "images"
        images_dir.mkdir()
        
        # Create a simple PNG file (1x1 pixel)
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        (images_dir / "architecture.png").write_bytes(png_data)
        (images_dir / "prerequisites.png").write_bytes(png_data)
        
        # Create an SVG file
        (images_dir / "delta-architecture.svg").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="80" height="80" fill="blue"/>
  <text x="50" y="50" text-anchor="middle" fill="white">Delta</text>
</svg>""")

        # Create unused image
        (images_dir / "unused.png").write_bytes(png_data)
        
        # Create mkdocs.yml
        mkdocs_config = {
            'site_name': 'CSA Docs Test',
            'docs_dir': 'docs',
            'theme': {'name': 'material'},
            'nav': [
                {'Home': 'index.md'},
                {'Architecture': [
                    {'Overview': 'architecture/overview.md'}
                ]},
                {'Tutorials': [
                    {'Getting Started': 'tutorials/getting-started.md'}
                ]}
            ],
            'plugins': ['search']
        }
        
        with open(docs_root / "mkdocs.yml", 'w') as f:
            yaml.dump(mkdocs_config, f)
        
        # Create markdownlint config
        markdownlint_config = {
            "MD013": {"line_length": 120},
            "MD041": False,
            "MD033": False
        }
        
        with open(docs_root / ".markdownlint.json", 'w') as f:
            yaml.dump(markdownlint_config, f)
        
        yield docs_root


@pytest.fixture
def build_tester(temp_docs_root):
    """Create a DocumentationBuildTester instance."""
    return DocumentationBuildTester(temp_docs_root)


@pytest.fixture
async def link_validator(temp_docs_root):
    """Create a LinkValidator instance with async context."""
    async with LinkValidator(temp_docs_root) as validator:
        yield validator


@pytest.fixture
def markdown_quality_checker(temp_docs_root):
    """Create a MarkdownQualityChecker instance."""
    return MarkdownQualityChecker(temp_docs_root)


@pytest.fixture
def image_validator(temp_docs_root):
    """Create an ImageReferenceValidator instance."""
    return ImageReferenceValidator(temp_docs_root)


@pytest.fixture
def navigation_validator(temp_docs_root):
    """Create a NavigationStructureValidator instance."""
    return NavigationStructureValidator(temp_docs_root)


@pytest.fixture
def sample_markdown_content():
    """Sample markdown content for testing."""
    return """# Test Document

This is a test document with various elements.

## Section 2

Here's a paragraph with a [link](https://example.com) and ![image](test.png).

### Subsection

```python
def hello():
    print("Hello, world!")
```

| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |

## Issues

This line is too long and should trigger a line length warning in markdownlint if the limit is set properly and the line exceeds the configured maximum length.

This line has trailing spaces.   

There are too many empty lines below:




## End
"""


@pytest.fixture
def mock_http_session():
    """Mock aiohttp session for testing external links."""
    with patch('aiohttp.ClientSession') as mock_session:
        mock_response = Mock()
        mock_response.status = 200
        mock_response.__aenter__ = Mock(return_value=mock_response)
        mock_response.__aexit__ = Mock(return_value=None)
        
        mock_session.return_value.head.return_value = mock_response
        mock_session.return_value.close = Mock()
        mock_session.return_value.__aenter__ = Mock(return_value=mock_session.return_value)
        mock_session.return_value.__aexit__ = Mock(return_value=None)
        
        yield mock_session


@pytest.fixture
def temp_markdown_file(tmp_path, sample_markdown_content):
    """Create a temporary markdown file for testing."""
    md_file = tmp_path / "test.md"
    md_file.write_text(sample_markdown_content)
    return md_file


@pytest.fixture(scope="session")
def real_docs_root():
    """Use the actual documentation root for integration tests."""
    docs_root = Path(__file__).parent.parent
    if (docs_root / "mkdocs.yml").exists():
        return docs_root
    else:
        pytest.skip("Real documentation root not found - skipping integration test")


class MockSubprocessResult:
    """Mock subprocess result for testing."""
    
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


@pytest.fixture
def mock_subprocess_success():
    """Mock successful subprocess run."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MockSubprocessResult(
            returncode=0,
            stdout="Build completed successfully",
            stderr=""
        )
        yield mock_run


@pytest.fixture
def mock_subprocess_failure():
    """Mock failed subprocess run."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MockSubprocessResult(
            returncode=1,
            stdout="",
            stderr="Build failed with errors"
        )
        yield mock_run


@pytest.fixture
def broken_mkdocs_root(tmp_path):
    """Create a documentation root with broken mkdocs.yml."""
    docs_root = tmp_path / "broken_docs"
    docs_root.mkdir()
    
    # Create broken mkdocs.yml
    broken_config = "invalid: yaml: content: [unclosed"
    (docs_root / "mkdocs.yml").write_text(broken_config)
    
    return docs_root


@pytest.fixture
def no_config_docs_root(tmp_path):
    """Create a documentation root without mkdocs.yml."""
    docs_root = tmp_path / "no_config_docs"
    docs_root.mkdir()
    
    docs_dir = docs_root / "docs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Test")
    
    return docs_root


# Utility functions for test data generation
def create_test_markdown_file(path: Path, content: str):
    """Create a test markdown file with specified content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def create_test_image_file(path: Path, format='png'):
    """Create a test image file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if format == 'png':
        # 1x1 pixel PNG
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        path.write_bytes(png_data)
    elif format == 'svg':
        svg_content = '<?xml version="1.0"?><svg width="10" height="10" xmlns="http://www.w3.org/2000/svg"><rect width="10" height="10" fill="red"/></svg>'
        path.write_text(svg_content)


# Parametrize fixtures for different test scenarios
@pytest.fixture(params=['unit', 'integration'])
def test_mode(request):
    """Parametrize tests to run in both unit and integration modes."""
    return request.param