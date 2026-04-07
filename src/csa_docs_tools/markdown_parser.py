"""Shared Markdown AST parser using markdown-it-py.

Provides structured extraction of links, images, headings, code blocks,
and other elements from Markdown files. Replaces fragile regex-based
parsing across validators with a proper AST walk.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from markdown_it import MarkdownIt

__all__ = [
    "MarkdownParser",
    "ParsedLink",
    "ParsedImage",
    "ParsedHeading",
    "ParsedCodeBlock",
    "ParsedDocument",
]


@dataclass
class ParsedLink:
    """A link extracted from the AST."""

    url: str
    text: str
    line_number: int
    link_type: str = "markdown"  # "markdown" | "html" | "autolink"


@dataclass
class ParsedImage:
    """An image reference extracted from the AST."""

    src: str
    alt_text: str
    line_number: int
    ref_type: str = "markdown"  # "markdown" | "html"


@dataclass
class ParsedHeading:
    """A heading extracted from the AST."""

    level: int
    text: str
    slug: str
    line_number: int


@dataclass
class ParsedCodeBlock:
    """A fenced code block extracted from the AST."""

    language: str
    content: str
    line_number: int


@dataclass
class ParsedDocument:
    """Complete parsed representation of a Markdown file."""

    links: List[ParsedLink] = field(default_factory=list)
    images: List[ParsedImage] = field(default_factory=list)
    headings: List[ParsedHeading] = field(default_factory=list)
    code_blocks: List[ParsedCodeBlock] = field(default_factory=list)
    has_front_matter: bool = False
    front_matter_closed: bool = True
    html_ids: List[str] = field(default_factory=list)


# Regex for extracting HTML <a> and <img> from inline HTML tokens
_HTML_LINK_RE = re.compile(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
_HTML_IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
_HTML_ID_RE = re.compile(r'id=["\']([^"\']+)["\']', re.IGNORECASE)

# Slugify helpers matching MkDocs/Material heading-slug rules
_SLUG_STRIP_RE = re.compile(r'[^\w\s-]')
_SLUG_WS_RE = re.compile(r'[\s]+')
_SLUG_DASH_RE = re.compile(r'-+')


def _slugify(text: str) -> str:
    """Convert heading text to a slug using MkDocs conventions."""
    slug = _SLUG_STRIP_RE.sub('', text.lower())
    slug = _SLUG_WS_RE.sub('-', slug.strip())
    slug = _SLUG_DASH_RE.sub('-', slug).strip('-')
    return slug


def _collect_inline_text(token) -> str:  # noqa: ANN001
    """Recursively collect plain text from inline children."""
    if not token.children:
        return token.content or ""
    parts: list[str] = []
    for child in token.children:
        if child.type in ("text", "code_inline"):
            parts.append(child.content)
        elif child.type == "softbreak":
            parts.append(" ")
        elif child.children:
            parts.append(_collect_inline_text(child))
    return "".join(parts)


class MarkdownParser:
    """Parse Markdown files into structured data using markdown-it-py."""

    def __init__(self) -> None:
        self._md = MarkdownIt("commonmark", {"html": True}).enable("table")

    def parse_text(self, text: str) -> ParsedDocument:
        """Parse Markdown text into a ParsedDocument.

        Args:
            text: Raw Markdown content.

        Returns:
            ParsedDocument with extracted elements.
        """
        doc = ParsedDocument()

        # Detect front matter
        if text.startswith('---'):
            doc.has_front_matter = True
            # Find closing ---
            lines = text.split('\n')
            found_close = False
            for line in lines[1:]:
                if line.strip() == '---':
                    found_close = True
                    break
            doc.front_matter_closed = found_close

        tokens = self._md.parse(text)
        self._walk(tokens, doc)
        return doc

    def parse_file(self, file_path: Path) -> ParsedDocument:
        """Parse a Markdown file into a ParsedDocument.

        Args:
            file_path: Path to the .md file.

        Returns:
            ParsedDocument with extracted elements.
        """
        content = file_path.read_text(encoding="utf-8")
        return self.parse_text(content)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _walk(self, tokens: list, doc: ParsedDocument) -> None:  # noqa: ANN001
        """Walk the token stream and populate *doc*."""
        i = 0
        while i < len(tokens):
            tok = tokens[i]

            # Headings ------------------------------------------------
            if tok.type == "heading_open":
                level = int(tok.tag[1])  # h1..h6
                line = (tok.map[0] + 1) if tok.map else 0
                # Next token is the inline content
                if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                    text = _collect_inline_text(tokens[i + 1])
                else:
                    text = ""
                doc.headings.append(ParsedHeading(
                    level=level,
                    text=text,
                    slug=_slugify(text),
                    line_number=line,
                ))

            # Fenced code blocks ---------------------------------------
            elif tok.type == "fence":
                line = (tok.map[0] + 1) if tok.map else 0
                doc.code_blocks.append(ParsedCodeBlock(
                    language=tok.info.strip() if tok.info else "",
                    content=tok.content,
                    line_number=line,
                ))

            # Inline tokens: links, images, HTML -----------------------
            elif tok.type == "inline":
                line = (tok.map[0] + 1) if tok.map else 0
                self._walk_inline(tok.children or [], doc, line)

            # Block-level HTML (may contain <a>, <img>, id attrs) ------
            elif tok.type == "html_block":
                line = (tok.map[0] + 1) if tok.map else 0
                self._extract_html(tok.content, doc, line)

            i += 1

    def _walk_inline(self, children: list, doc: ParsedDocument, base_line: int) -> None:  # noqa: ANN001
        """Walk inline children to extract links, images, and inline HTML."""
        j = 0
        while j < len(children):
            child = children[j]

            if child.type == "link_open":
                url = child.attrGet("href") or ""
                # Collect text until link_close
                text_parts: list[str] = []
                j += 1
                while j < len(children) and children[j].type != "link_close":
                    text_parts.append(children[j].content or "")
                    j += 1
                doc.links.append(ParsedLink(
                    url=url,
                    text="".join(text_parts),
                    line_number=base_line,
                    link_type="markdown",
                ))

            elif child.type == "image":
                src = child.attrGet("src") or ""
                alt = child.content or ""
                if not alt and child.children:
                    alt = _collect_inline_text(child)
                doc.images.append(ParsedImage(
                    src=src,
                    alt_text=alt,
                    line_number=base_line,
                    ref_type="markdown",
                ))

            elif child.type == "html_inline":
                self._extract_html(child.content, doc, base_line)

            j += 1

    def _extract_html(self, html: str, doc: ParsedDocument, line: int) -> None:
        """Extract links, images, and id attributes from raw HTML."""
        for m in _HTML_LINK_RE.finditer(html):
            doc.links.append(ParsedLink(
                url=m.group(1),
                text="",
                line_number=line,
                link_type="html",
            ))

        for m in _HTML_IMG_RE.finditer(html):
            doc.images.append(ParsedImage(
                src=m.group(1),
                alt_text="",
                line_number=line,
                ref_type="html",
            ))

        for m in _HTML_ID_RE.finditer(html):
            doc.html_ids.append(m.group(1))
