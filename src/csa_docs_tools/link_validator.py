"""Link validation utilities for documentation."""

import re
import asyncio
import aiohttp
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from urllib.parse import urljoin, urlparse
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LinkResult:
    """Result of link validation."""
    url: str
    status_code: Optional[int]
    is_valid: bool
    error_message: Optional[str]
    source_file: str
    line_number: int


class LinkValidator:
    """Validate links in markdown documentation."""
    
    def __init__(self, docs_root: Path, base_url: str = ""):
        """Initialize link validator.
        
        Args:
            docs_root: Path to documentation root
            base_url: Base URL for the documentation site
        """
        self.docs_root = Path(docs_root)
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Common patterns for links
        self.markdown_link_pattern = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
        self.html_link_pattern = re.compile(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>')
        self.image_link_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
        
        # File extensions to check
        self.markdown_extensions = {'.md', '.markdown'}
        
    async def __aenter__(self):
        """Async context manager entry."""
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        connector = aiohttp.TCPConnector(limit=50, limit_per_host=10)
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={'User-Agent': 'CSA-Docs-Link-Checker/1.0'}
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    def find_all_links(self, file_path: Path) -> List[Tuple[str, int, str]]:
        """Find all links in a markdown file.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            List of tuples (link_url, line_number, link_type)
        """
        links = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, 1):
                # Find markdown links
                for match in self.markdown_link_pattern.finditer(line):
                    links.append((match.group(2), line_num, 'markdown'))
                
                # Find HTML links
                for match in self.html_link_pattern.finditer(line):
                    links.append((match.group(1), line_num, 'html'))
                    
                # Find image links
                for match in self.image_link_pattern.finditer(line):
                    links.append((match.group(2), line_num, 'image'))
                    
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            
        return links
    
    def categorize_link(self, url: str) -> str:
        """Categorize a link by type.
        
        Args:
            url: URL to categorize
            
        Returns:
            Link category: 'external', 'internal', 'anchor', 'relative'
        """
        if url.startswith('#'):
            return 'anchor'
        elif url.startswith(('http://', 'https://')):
            return 'external'
        elif url.startswith('/'):
            return 'internal'
        else:
            return 'relative'
    
    def resolve_relative_link(self, link: str, source_file: Path) -> Path:
        """Resolve relative link to absolute file path.
        
        Args:
            link: Relative link
            source_file: Source file containing the link
            
        Returns:
            Resolved absolute path
        """
        # Remove anchor fragments
        link_path = link.split('#')[0]
        if not link_path:
            return source_file  # Anchor in same file
            
        # Resolve relative to source file directory
        source_dir = source_file.parent
        resolved = (source_dir / link_path).resolve()
        
        return resolved
    
    def validate_internal_link(self, link: str, source_file: Path) -> LinkResult:
        """Validate an internal/relative link.
        
        Args:
            link: Link URL
            source_file: Source file containing the link
            
        Returns:
            LinkResult with validation status
        """
        try:
            if link.startswith('#'):
                # Anchor link - would need to parse file content to validate
                return LinkResult(
                    url=link,
                    status_code=None,
                    is_valid=True,  # Assume valid for now
                    error_message=None,
                    source_file=str(source_file),
                    line_number=0
                )
            
            resolved_path = self.resolve_relative_link(link, source_file)
            
            # Check if file exists
            if resolved_path.exists():
                return LinkResult(
                    url=link,
                    status_code=200,
                    is_valid=True,
                    error_message=None,
                    source_file=str(source_file),
                    line_number=0
                )
            else:
                return LinkResult(
                    url=link,
                    status_code=404,
                    is_valid=False,
                    error_message=f"File not found: {resolved_path}",
                    source_file=str(source_file),
                    line_number=0
                )
                
        except Exception as e:
            return LinkResult(
                url=link,
                status_code=None,
                is_valid=False,
                error_message=str(e),
                source_file=str(source_file),
                line_number=0
            )
    
    async def validate_external_link(self, url: str, source_file: str, line_num: int) -> LinkResult:
        """Validate an external HTTP/HTTPS link.
        
        Args:
            url: External URL to validate
            source_file: Source file path
            line_num: Line number in source file
            
        Returns:
            LinkResult with validation status
        """
        if not self.session:
            return LinkResult(
                url=url,
                status_code=None,
                is_valid=False,
                error_message="No HTTP session available",
                source_file=source_file,
                line_number=line_num
            )
        
        try:
            async with self.session.head(url, allow_redirects=True) as response:
                is_valid = response.status < 400
                return LinkResult(
                    url=url,
                    status_code=response.status,
                    is_valid=is_valid,
                    error_message=None if is_valid else f"HTTP {response.status}",
                    source_file=source_file,
                    line_number=line_num
                )
                
        except asyncio.TimeoutError:
            return LinkResult(
                url=url,
                status_code=None,
                is_valid=False,
                error_message="Request timeout",
                source_file=source_file,
                line_number=line_num
            )
        except aiohttp.ClientError as e:
            return LinkResult(
                url=url,
                status_code=None,
                is_valid=False,
                error_message=f"Client error: {e}",
                source_file=source_file,
                line_number=line_num
            )
        except Exception as e:
            return LinkResult(
                url=url,
                status_code=None,
                is_valid=False,
                error_message=f"Unexpected error: {e}",
                source_file=source_file,
                line_number=line_num
            )
    
    async def validate_all_links(self, check_external: bool = True) -> List[LinkResult]:
        """Validate all links in the documentation.
        
        Args:
            check_external: Whether to validate external HTTP links
            
        Returns:
            List of LinkResult objects
        """
        results = []
        
        # Find all markdown files
        markdown_files = []
        for ext in self.markdown_extensions:
            markdown_files.extend(self.docs_root.glob(f"**/*{ext}"))
        
        for file_path in markdown_files:
            links = self.find_all_links(file_path)
            
            for link_url, line_num, link_type in links:
                category = self.categorize_link(link_url)
                
                if category in ['relative', 'internal', 'anchor']:
                    result = self.validate_internal_link(link_url, file_path)
                    result.line_number = line_num
                    results.append(result)
                    
                elif category == 'external' and check_external:
                    result = await self.validate_external_link(
                        link_url, str(file_path), line_num
                    )
                    results.append(result)
        
        return results
    
    def get_broken_links(self, results: List[LinkResult]) -> List[LinkResult]:
        """Filter results to only broken links.
        
        Args:
            results: List of LinkResult objects
            
        Returns:
            List of broken links only
        """
        return [result for result in results if not result.is_valid]
    
    def generate_report(self, results: List[LinkResult]) -> Dict:
        """Generate a summary report of link validation.
        
        Args:
            results: List of LinkResult objects
            
        Returns:
            Dictionary with validation statistics
        """
        total_links = len(results)
        broken_links = self.get_broken_links(results)
        valid_links = total_links - len(broken_links)
        
        # Group by status code
        status_counts = {}
        for result in results:
            status = result.status_code or 'unknown'
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Group by link type
        link_types = {}
        for result in results:
            link_type = self.categorize_link(result.url)
            link_types[link_type] = link_types.get(link_type, 0) + 1
        
        return {
            'total_links': total_links,
            'valid_links': valid_links,
            'broken_links': len(broken_links),
            'success_rate': (valid_links / total_links * 100) if total_links > 0 else 0,
            'status_codes': status_counts,
            'link_types': link_types,
            'broken_link_details': [
                {
                    'url': result.url,
                    'file': result.source_file,
                    'line': result.line_number,
                    'error': result.error_message
                }
                for result in broken_links
            ]
        }