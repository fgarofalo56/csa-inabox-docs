"""Tests for the shared Markdown AST parser."""

import pytest
from pathlib import Path

from csa_docs_tools.markdown_parser import (
    MarkdownParser,
    ParsedDocument,
    ParsedLink,
    ParsedImage,
    ParsedHeading,
    ParsedCodeBlock,
)


@pytest.fixture
def parser():
    return MarkdownParser()


class TestMarkdownParserHeadings:
    """Test heading extraction."""

    def test_extract_headings(self, parser):
        text = "# Title\n\n## Section\n\n### Subsection\n"
        doc = parser.parse_text(text)
        assert len(doc.headings) == 3
        assert doc.headings[0].level == 1
        assert doc.headings[0].text == "Title"
        assert doc.headings[1].level == 2
        assert doc.headings[1].text == "Section"
        assert doc.headings[2].level == 3
        assert doc.headings[2].text == "Subsection"

    def test_heading_slugs(self, parser):
        text = "# Hello World\n\n## My API Endpoint\n"
        doc = parser.parse_text(text)
        assert doc.headings[0].slug == "hello-world"
        assert doc.headings[1].slug == "my-api-endpoint"

    def test_heading_slug_special_chars(self, parser):
        text = "# Hello (World) & Friends!\n"
        doc = parser.parse_text(text)
        # Slugify strips special chars and collapses consecutive hyphens
        assert doc.headings[0].slug == "hello-world-friends"

    def test_heading_line_numbers(self, parser):
        text = "# First\n\nSome text.\n\n## Second\n"
        doc = parser.parse_text(text)
        assert doc.headings[0].line_number == 1
        assert doc.headings[1].line_number == 5

    def test_no_headings(self, parser):
        text = "Just some text.\n\nMore text.\n"
        doc = parser.parse_text(text)
        assert doc.headings == []


class TestMarkdownParserLinks:
    """Test link extraction."""

    def test_extract_markdown_links(self, parser):
        text = "Click [here](https://example.com) to continue.\n"
        doc = parser.parse_text(text)
        assert len(doc.links) == 1
        assert doc.links[0].url == "https://example.com"
        assert doc.links[0].text == "here"
        assert doc.links[0].link_type == "markdown"

    def test_extract_multiple_links(self, parser):
        text = "See [A](a.md) and [B](b.md).\n"
        doc = parser.parse_text(text)
        assert len(doc.links) == 2
        assert doc.links[0].url == "a.md"
        assert doc.links[1].url == "b.md"

    def test_extract_link_with_title(self, parser):
        text = '[Click](page.md "A Title")\n'
        doc = parser.parse_text(text)
        assert len(doc.links) == 1
        assert doc.links[0].url == "page.md"

    def test_extract_html_links(self, parser):
        text = '<a href="https://example.com">Click</a>\n'
        doc = parser.parse_text(text)
        assert len(doc.links) == 1
        assert doc.links[0].url == "https://example.com"
        assert doc.links[0].link_type == "html"

    def test_extract_anchor_links(self, parser):
        text = "See [section](#my-section).\n"
        doc = parser.parse_text(text)
        assert len(doc.links) == 1
        assert doc.links[0].url == "#my-section"

    def test_no_links(self, parser):
        text = "No links here.\n"
        doc = parser.parse_text(text)
        assert doc.links == []

    def test_link_with_empty_text(self, parser):
        text = "[](empty.md)\n"
        doc = parser.parse_text(text)
        assert len(doc.links) == 1
        assert doc.links[0].text == ""


class TestMarkdownParserImages:
    """Test image extraction."""

    def test_extract_markdown_images(self, parser):
        text = "![Alt text](image.png)\n"
        doc = parser.parse_text(text)
        assert len(doc.images) == 1
        assert doc.images[0].src == "image.png"
        assert doc.images[0].alt_text == "Alt text"
        assert doc.images[0].ref_type == "markdown"

    def test_extract_html_images(self, parser):
        text = '<img src="photo.jpg" alt="Photo">\n'
        doc = parser.parse_text(text)
        assert len(doc.images) == 1
        assert doc.images[0].src == "photo.jpg"
        assert doc.images[0].ref_type == "html"

    def test_image_with_title(self, parser):
        text = '![Alt](image.png "Title")\n'
        doc = parser.parse_text(text)
        assert len(doc.images) == 1
        assert doc.images[0].src == "image.png"

    def test_no_images(self, parser):
        text = "No images here.\n"
        doc = parser.parse_text(text)
        assert doc.images == []


class TestMarkdownParserCodeBlocks:
    """Test code block extraction."""

    def test_extract_fenced_code_block(self, parser):
        text = "```python\nprint('hello')\n```\n"
        doc = parser.parse_text(text)
        assert len(doc.code_blocks) == 1
        assert doc.code_blocks[0].language == "python"
        assert "print('hello')" in doc.code_blocks[0].content

    def test_code_block_without_language(self, parser):
        text = "```\nsome code\n```\n"
        doc = parser.parse_text(text)
        assert len(doc.code_blocks) == 1
        assert doc.code_blocks[0].language == ""

    def test_multiple_code_blocks(self, parser):
        text = "```js\nvar x;\n```\n\n```python\nx = 1\n```\n"
        doc = parser.parse_text(text)
        assert len(doc.code_blocks) == 2
        assert doc.code_blocks[0].language == "js"
        assert doc.code_blocks[1].language == "python"

    def test_no_code_blocks(self, parser):
        text = "No code here.\n"
        doc = parser.parse_text(text)
        assert doc.code_blocks == []


class TestMarkdownParserFrontMatter:
    """Test front matter detection."""

    def test_detect_front_matter(self, parser):
        text = "---\ntitle: Test\n---\n\n# Hello\n"
        doc = parser.parse_text(text)
        assert doc.has_front_matter is True
        assert doc.front_matter_closed is True

    def test_unclosed_front_matter(self, parser):
        text = "---\ntitle: Test\nno closing\n"
        doc = parser.parse_text(text)
        assert doc.has_front_matter is True
        assert doc.front_matter_closed is False

    def test_no_front_matter(self, parser):
        text = "# Just a heading\n\nSome content.\n"
        doc = parser.parse_text(text)
        assert doc.has_front_matter is False
        assert doc.front_matter_closed is True


class TestMarkdownParserHtmlIds:
    """Test HTML id attribute extraction."""

    def test_extract_html_ids(self, parser):
        text = '<div id="my-section">Content</div>\n'
        doc = parser.parse_text(text)
        assert "my-section" in doc.html_ids

    def test_extract_inline_html_ids(self, parser):
        text = 'Text with <span id="marker">marker</span> inline.\n'
        doc = parser.parse_text(text)
        assert "marker" in doc.html_ids


class TestMarkdownParserFile:
    """Test file-based parsing."""

    def test_parse_file(self, parser, tmp_path):
        md_file = tmp_path / "test.md"
        md_file.write_text("# Title\n\n[Link](page.md)\n\n![Image](pic.png)\n", encoding="utf-8")

        doc = parser.parse_file(md_file)
        assert len(doc.headings) == 1
        assert len(doc.links) == 1
        assert len(doc.images) == 1

    def test_parse_file_empty(self, parser, tmp_path):
        md_file = tmp_path / "empty.md"
        md_file.write_text("", encoding="utf-8")

        doc = parser.parse_file(md_file)
        assert doc.headings == []
        assert doc.links == []
        assert doc.images == []


class TestMarkdownParserComplex:
    """Test complex document parsing."""

    def test_complex_document(self, parser):
        text = """# Main Title

Some intro text with a [link](./page.md) and an ![image](assets/img.png).

## Section A

```python
def hello():
    print("world")
```

### Sub Section

- Item with [ref](other.md#section)
- Item with <a href="https://ext.com">external link</a>

<div id="custom-anchor">Custom section</div>

## Section B

| Col A | Col B |
|-------|-------|
| 1     | 2     |

```
no language specified
```
"""
        doc = parser.parse_text(text)

        # Headings
        assert len(doc.headings) == 4
        assert doc.headings[0].text == "Main Title"
        assert doc.headings[3].text == "Section B"

        # Links (markdown + html)
        assert len(doc.links) >= 3  # ./page.md, other.md#section, https://ext.com

        # Images
        assert len(doc.images) == 1
        assert doc.images[0].src == "assets/img.png"

        # Code blocks
        assert len(doc.code_blocks) == 2
        assert doc.code_blocks[0].language == "python"
        assert doc.code_blocks[1].language == ""

        # Front matter (not in this test)
        assert doc.has_front_matter is False

        # HTML ids
        assert "custom-anchor" in doc.html_ids
