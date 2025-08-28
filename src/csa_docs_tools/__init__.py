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

__all__ = [
    "DocumentationBuildTester",
    "LinkValidator", 
    "MarkdownQualityChecker",
    "ImageReferenceValidator",
    "NavigationStructureValidator"
]