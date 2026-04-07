"""Mermaid diagram rendering via mmdc CLI.

Provides a Python wrapper around the Mermaid CLI (mmdc) for converting
.mmd/.mermaid files to PNG/SVG/PDF. This replaces the need for the
Node.js MermaidRenderer infrastructure in tools/src/.

The mmdc binary must be installed separately:
    npm install -g @mermaid-js/mermaid-cli
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import logging

logger = logging.getLogger(__name__)


@dataclass
class RenderResult:
    """Result of rendering a single diagram."""
    source_path: str
    output_path: str
    success: bool
    error: Optional[str] = None


@dataclass
class RenderReport:
    """Summary of a batch rendering run."""
    total: int = 0
    succeeded: int = 0
    failed: int = 0
    results: List[RenderResult] = field(default_factory=list)


class MermaidRenderer:
    """Render Mermaid diagrams to images via the mmdc CLI."""

    def __init__(
        self,
        background: str = "transparent",
        theme: str = "default",
        width: int = 1920,
        height: int = 1080,
        output_format: str = "png",
    ) -> None:
        self.background = background
        self.theme = theme
        self.width = width
        self.height = height
        self.output_format = output_format

    def is_available(self) -> bool:
        """Check if mmdc CLI is installed and callable."""
        try:
            result = subprocess.run(
                ["mmdc", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def render_file(
        self,
        source: Path,
        output: Optional[Path] = None,
    ) -> RenderResult:
        """Render a single Mermaid file to an image.

        Args:
            source: Path to .mmd or .mermaid source file.
            output: Path for the output image. Defaults to same
                    name with the configured format extension.

        Returns:
            RenderResult indicating success or failure.
        """
        source = Path(source)
        if output is None:
            output = source.with_suffix(f".{self.output_format}")
        else:
            output = Path(output)

        cmd = [
            "mmdc",
            "-i", str(source),
            "-o", str(output),
            "-b", self.background,
            "-t", self.theme,
            "-w", str(self.width),
            "-H", str(self.height),
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                return RenderResult(
                    source_path=str(source),
                    output_path=str(output),
                    success=True,
                )
            else:
                error_msg = result.stderr.strip() or result.stdout.strip() or "Unknown error"
                return RenderResult(
                    source_path=str(source),
                    output_path=str(output),
                    success=False,
                    error=error_msg,
                )
        except FileNotFoundError:
            return RenderResult(
                source_path=str(source),
                output_path=str(output),
                success=False,
                error="mmdc not found. Install with: npm install -g @mermaid-js/mermaid-cli",
            )
        except subprocess.TimeoutExpired:
            return RenderResult(
                source_path=str(source),
                output_path=str(output),
                success=False,
                error="Rendering timed out (60s limit)",
            )

    def render_text(
        self,
        mermaid_text: str,
        output: Path,
    ) -> RenderResult:
        """Render Mermaid text directly to an image.

        Writes the text to a temporary file and renders it.

        Args:
            mermaid_text: Raw Mermaid diagram source.
            output: Path for the output image.

        Returns:
            RenderResult indicating success or failure.
        """
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".mmd",
            delete=False,
            encoding="utf-8",
        ) as f:
            f.write(mermaid_text)
            temp_path = Path(f.name)

        try:
            return self.render_file(temp_path, output)
        finally:
            temp_path.unlink(missing_ok=True)

    def render_directory(
        self,
        source_dir: Path,
        output_dir: Optional[Path] = None,
        extensions: Optional[List[str]] = None,
    ) -> RenderReport:
        """Render all Mermaid files in a directory.

        Args:
            source_dir: Directory containing .mmd/.mermaid files.
            output_dir: Output directory. Defaults to source_dir.
            extensions: File extensions to look for.
                        Defaults to ['.mmd', '.mermaid'].

        Returns:
            RenderReport with aggregated results.
        """
        source_dir = Path(source_dir)
        output_dir = Path(output_dir) if output_dir else source_dir
        extensions = extensions or ['.mmd', '.mermaid']

        output_dir.mkdir(parents=True, exist_ok=True)

        report = RenderReport()
        files = []
        for ext in extensions:
            files.extend(source_dir.rglob(f"*{ext}"))

        for source_file in sorted(files):
            relative = source_file.relative_to(source_dir)
            output_file = output_dir / relative.with_suffix(f".{self.output_format}")
            output_file.parent.mkdir(parents=True, exist_ok=True)

            result = self.render_file(source_file, output_file)
            report.results.append(result)
            report.total += 1
            if result.success:
                report.succeeded += 1
            else:
                report.failed += 1
                logger.warning(f"Failed to render {source_file}: {result.error}")

        return report
