"""Image reference validation utilities."""

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
import mimetypes
from PIL import Image
import logging

logger = logging.getLogger(__name__)


@dataclass
class ImageIssue:
    """Represents an image-related issue."""
    file_path: str
    line_number: int
    image_path: str
    issue_type: str
    severity: str
    message: str


class ImageReferenceValidator:
    """Validate image references in markdown documentation."""
    
    def __init__(self, docs_root: Path):
        """Initialize image reference validator.
        
        Args:
            docs_root: Path to documentation root
        """
        self.docs_root = Path(docs_root)
        
        # Supported image formats
        self.supported_formats = {
            '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.tiff'
        }
        
        # Image reference patterns
        self.markdown_image_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
        self.html_image_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>')
        
        # Recommended image sizes (width x height)
        self.size_recommendations = {
            'diagrams': (800, 600),
            'screenshots': (1200, 800),
            'icons': (64, 64),
            'thumbnails': (200, 150)
        }
    
    def find_image_references(self, file_path: Path) -> List[Tuple[str, int, str, str]]:
        """Find all image references in a markdown file.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            List of tuples (image_path, line_number, alt_text, reference_type)
        """
        references = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, 1):
                # Find markdown images
                for match in self.markdown_image_pattern.finditer(line):
                    alt_text = match.group(1)
                    image_path = match.group(2)
                    references.append((image_path, line_num, alt_text, 'markdown'))
                
                # Find HTML images
                for match in self.html_image_pattern.finditer(line):
                    image_path = match.group(1)
                    references.append((image_path, line_num, '', 'html'))
                    
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            
        return references
    
    def validate_image_exists(self, image_path: str, source_file: Path) -> Tuple[bool, str]:
        """Check if image file exists.
        
        Args:
            image_path: Relative or absolute image path
            source_file: Source markdown file
            
        Returns:
            Tuple of (exists, resolved_path)
        """
        # Handle external URLs
        if image_path.startswith(('http://', 'https://')):
            return True, image_path  # Assume external images exist
        
        # Handle absolute paths
        if image_path.startswith('/'):
            resolved_path = self.docs_root / image_path.lstrip('/')
        else:
            # Relative path from source file
            resolved_path = source_file.parent / image_path
            
        resolved_path = resolved_path.resolve()
        return resolved_path.exists(), str(resolved_path)
    
    def validate_image_format(self, image_path: Path) -> Tuple[bool, str]:
        """Validate image file format.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not image_path.exists():
            return False, "File does not exist"
        
        # Check file extension
        extension = image_path.suffix.lower()
        if extension not in self.supported_formats:
            return False, f"Unsupported image format: {extension}"
        
        # Try to open and validate the image
        try:
            if extension == '.svg':
                # SVG validation (basic check)
                with open(image_path, 'r', encoding='utf-8') as f:
                    content = f.read(1000)  # Read first 1KB
                    if not content.strip().startswith('<?xml') and not content.strip().startswith('<svg'):
                        return False, "Invalid SVG file format"
            else:
                # Use PIL for other formats
                with Image.open(image_path) as img:
                    img.verify()  # This will raise an exception if invalid
                    
            return True, ""
            
        except Exception as e:
            return False, f"Invalid image file: {e}"
    
    def check_image_properties(self, image_path: Path) -> Dict:
        """Get image properties and check for potential issues.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with image properties and potential issues
        """
        properties = {
            'width': None,
            'height': None,
            'file_size': None,
            'format': None,
            'issues': []
        }
        
        if not image_path.exists():
            properties['issues'].append("File does not exist")
            return properties
        
        try:
            # Get file size
            properties['file_size'] = image_path.stat().st_size
            
            # Check file size
            max_size = 5 * 1024 * 1024  # 5MB
            if properties['file_size'] > max_size:
                properties['issues'].append(f"Large file size: {properties['file_size'] / 1024 / 1024:.1f}MB")
            
            # Handle SVG separately
            if image_path.suffix.lower() == '.svg':
                properties['format'] = 'SVG'
                # SVG size analysis would require XML parsing
            else:
                with Image.open(image_path) as img:
                    properties['width'] = img.width
                    properties['height'] = img.height
                    properties['format'] = img.format
                    
                    # Check image dimensions
                    if img.width > 2000 or img.height > 2000:
                        properties['issues'].append(f"Large dimensions: {img.width}x{img.height}")
                    
                    if img.width < 100 or img.height < 100:
                        properties['issues'].append(f"Small dimensions: {img.width}x{img.height}")
                        
        except Exception as e:
            properties['issues'].append(f"Could not analyze image: {e}")
            
        return properties
    
    def validate_alt_text(self, alt_text: str, image_path: str) -> List[str]:
        """Validate image alt text.
        
        Args:
            alt_text: Alt text string
            image_path: Path to image
            
        Returns:
            List of validation issues
        """
        issues = []
        
        # Check for missing alt text
        if not alt_text.strip():
            issues.append("Missing alt text")
            return issues
        
        # Check alt text length
        if len(alt_text) > 125:
            issues.append(f"Alt text too long: {len(alt_text)} characters (recommended: <125)")
        
        if len(alt_text) < 10:
            issues.append(f"Alt text too short: {len(alt_text)} characters (recommended: >10)")
        
        # Check for redundant phrases
        redundant_phrases = [
            'image of', 'picture of', 'photo of', 'screenshot of',
            'diagram of', 'chart of', 'graph of'
        ]
        
        alt_lower = alt_text.lower()
        for phrase in redundant_phrases:
            if phrase in alt_lower:
                issues.append(f"Redundant phrase in alt text: '{phrase}'")
        
        # Check for filename in alt text
        image_name = Path(image_path).stem.lower()
        if image_name in alt_lower:
            issues.append("Alt text should not contain filename")
        
        return issues
    
    def find_unused_images(self) -> List[Path]:
        """Find image files that are not referenced in any markdown file.
        
        Returns:
            List of unused image file paths
        """
        # Find all image files
        all_images = set()
        for ext in self.supported_formats:
            all_images.update(self.docs_root.glob(f"**/*{ext}"))
        
        # Find all referenced images
        referenced_images = set()
        markdown_files = list(self.docs_root.glob("**/*.md"))
        
        for md_file in markdown_files:
            references = self.find_image_references(md_file)
            for image_path, _, _, _ in references:
                # Skip external URLs
                if image_path.startswith(('http://', 'https://')):
                    continue
                    
                # Resolve image path
                if image_path.startswith('/'):
                    resolved = self.docs_root / image_path.lstrip('/')
                else:
                    resolved = md_file.parent / image_path
                    
                resolved = resolved.resolve()
                if resolved.exists():
                    referenced_images.add(resolved)
        
        # Find unused images
        unused_images = all_images - referenced_images
        return sorted(unused_images)
    
    def validate_all_images(self) -> Dict[str, List[ImageIssue]]:
        """Validate all image references in documentation.
        
        Returns:
            Dictionary mapping markdown files to lists of image issues
        """
        results = {}
        markdown_files = list(self.docs_root.glob("**/*.md"))
        
        for md_file in markdown_files:
            file_issues = []
            references = self.find_image_references(md_file)
            
            for image_path, line_num, alt_text, ref_type in references:
                # Skip external URLs for existence check
                if image_path.startswith(('http://', 'https://')):
                    # Still validate alt text
                    alt_issues = self.validate_alt_text(alt_text, image_path)
                    for issue in alt_issues:
                        file_issues.append(ImageIssue(
                            file_path=str(md_file),
                            line_number=line_num,
                            image_path=image_path,
                            issue_type='alt_text',
                            severity='warning',
                            message=issue
                        ))
                    continue
                
                # Check if image exists
                exists, resolved_path = self.validate_image_exists(image_path, md_file)
                if not exists:
                    file_issues.append(ImageIssue(
                        file_path=str(md_file),
                        line_number=line_num,
                        image_path=image_path,
                        issue_type='missing_file',
                        severity='error',
                        message=f"Image file not found: {resolved_path}"
                    ))
                    continue
                
                # Validate image format
                resolved_image_path = Path(resolved_path)
                format_valid, format_error = self.validate_image_format(resolved_image_path)
                if not format_valid:
                    file_issues.append(ImageIssue(
                        file_path=str(md_file),
                        line_number=line_num,
                        image_path=image_path,
                        issue_type='invalid_format',
                        severity='error',
                        message=format_error
                    ))
                    continue
                
                # Check image properties
                properties = self.check_image_properties(resolved_image_path)
                for property_issue in properties['issues']:
                    file_issues.append(ImageIssue(
                        file_path=str(md_file),
                        line_number=line_num,
                        image_path=image_path,
                        issue_type='image_property',
                        severity='warning',
                        message=property_issue
                    ))
                
                # Validate alt text
                alt_issues = self.validate_alt_text(alt_text, image_path)
                for alt_issue in alt_issues:
                    file_issues.append(ImageIssue(
                        file_path=str(md_file),
                        line_number=line_num,
                        image_path=image_path,
                        issue_type='alt_text',
                        severity='warning',
                        message=alt_issue
                    ))
            
            if file_issues:
                results[str(md_file)] = file_issues
        
        return results
    
    def generate_image_report(self, validation_results: Dict[str, List[ImageIssue]]) -> Dict:
        """Generate comprehensive image validation report.
        
        Args:
            validation_results: Dictionary of validation results
            
        Returns:
            Summary report dictionary
        """
        total_files = len([f for f in self.docs_root.glob("**/*.md")])
        files_with_issues = len(validation_results)
        total_issues = sum(len(issues) for issues in validation_results.values())
        
        # Count issues by type
        issue_type_counts = {}
        severity_counts = {'error': 0, 'warning': 0, 'info': 0}
        
        for issues in validation_results.values():
            for issue in issues:
                issue_type_counts[issue.issue_type] = issue_type_counts.get(issue.issue_type, 0) + 1
                severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
        
        # Find unused images
        unused_images = self.find_unused_images()
        
        # Count total images
        total_images = len(list(self.docs_root.glob("**/*.{png,jpg,jpeg,gif,svg,webp,bmp,tiff}")))
        
        return {
            'total_markdown_files': total_files,
            'files_with_image_issues': files_with_issues,
            'total_image_issues': total_issues,
            'total_images': total_images,
            'unused_images': len(unused_images),
            'issue_type_breakdown': issue_type_counts,
            'severity_breakdown': severity_counts,
            'unused_image_paths': [str(path) for path in unused_images[:20]],  # Top 20
            'image_health_score': max(0, 100 - (total_issues / max(total_files, 1) * 5)),
            'recommendations': self._generate_recommendations(validation_results, unused_images)
        }
    
    def _generate_recommendations(self, validation_results: Dict, unused_images: List[Path]) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        total_issues = sum(len(issues) for issues in validation_results.values())
        
        if total_issues > 0:
            recommendations.append("Review and fix image validation issues")
        
        if unused_images:
            recommendations.append(f"Consider removing {len(unused_images)} unused image files to reduce repository size")
        
        # Count specific issue types
        missing_alt_count = 0
        large_file_count = 0
        
        for issues in validation_results.values():
            for issue in issues:
                if 'alt text' in issue.message.lower():
                    missing_alt_count += 1
                if 'large file size' in issue.message.lower():
                    large_file_count += 1
        
        if missing_alt_count > 5:
            recommendations.append("Focus on improving alt text quality for better accessibility")
        
        if large_file_count > 3:
            recommendations.append("Optimize large images to improve page load times")
        
        return recommendations