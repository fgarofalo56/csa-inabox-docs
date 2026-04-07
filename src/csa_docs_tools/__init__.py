"""CSA Docs Tools - Testing and validation utilities for CSA-in-a-Box documentation."""

__version__ = "1.0.0"
__author__ = "CSA Documentation Team"
__description__ = "Testing infrastructure for Azure Synapse Analytics documentation"

# Main modules
from .build_tester import DocumentationBuildTester
from .link_validator import LinkValidator
from .markdown_quality import MarkdownQualityChecker
from .image_validator import ImageReferenceValidator
from .navigation_validator import NavigationStructureValidator
from .version_manager import SemanticVersionManager, VersionInfo, VersionType
from .release_manager import ReleaseManager
from .mike_manager import MikeVersionManager
from .markdown_parser import MarkdownParser, ParsedDocument
from .mermaid_renderer import MermaidRenderer as MermaidDiagramRenderer

__all__ = [
    "DocumentationBuildTester",
    "LinkValidator",
    "MarkdownQualityChecker",
    "ImageReferenceValidator",
    "NavigationStructureValidator",
    "SemanticVersionManager",
    "VersionInfo",
    "VersionType",
    "ReleaseManager",
    "MikeVersionManager",
    "MarkdownParser",
    "ParsedDocument",
    "MermaidDiagramRenderer",
]