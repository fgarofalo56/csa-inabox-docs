#!/usr/bin/env python3
"""
Link Checker for Azure Synapse Analytics Documentation
=============================================================

This script scans all markdown files in the documentation project,
extracts links, and verifies that they are working properly.
It checks both internal relative links and external URLs.

Usage:
    python link_checker.py [project_root_directory]

Example:
    python link_checker.py ../..
"""

import re
import sys
import logging
import requests
import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Set, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('link_checker')

# Regular expression to find markdown links
# This matches both [text](url) format and reference-style links
MARKDOWN_LINK_PATTERN = re.compile(r'\[(?P<text>[^\]]+)\]\((?P<url>[^)]+)\)')
REFERENCE_LINK_PATTERN = re.compile(r'\[(?P<text>[^\]]+)\]\[(?P<ref>[^\]]*)\]')
REFERENCE_DEF_PATTERN = re.compile(r'^\[(?P<key>[^\]]+)\]:\s*(?P<url>.*?)$', re.MULTILINE)

# Skip binary and certain text files
SKIP_EXTENSIONS = {
    '.exe', '.bin', '.dll', '.so', '.dylib',
    '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
    '.pdf', '.zip', '.tar', '.gz', '.rar'
}

# Skip certain directories
SKIP_DIRS = {'.git', '.github', 'node_modules', 'venv', '__pycache__'}

# Headers for HTTP requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

class LinkChecker:
    """Main link checker class that handles finding and validating links."""
    
    def __init__(self, root_dir: str):
        """Initialize the link checker with the root directory of the project."""
        self.root_dir = Path(root_dir).resolve()
        logger.info(f"Starting link checker for: {self.root_dir}")
        
        # Track processed and broken links
        self.internal_links_checked: Set[str] = set()
        self.external_links_checked: Dict[str, bool] = {}
        self.broken_links: Dict[str, List[Tuple[str, str]]] = {
            "internal": [],  # (file_path, link)
            "external": []   # (file_path, link)
        }
        
    def find_markdown_files(self) -> List[Path]:
        """Recursively find all markdown files in the project."""
        markdown_files = []
        
        for path in self.root_dir.rglob('*.md'):
            relative_path = path.relative_to(self.root_dir)
            parts = relative_path.parts
            
            # Skip files in directories we want to ignore
            if any(skip_dir in parts for skip_dir in SKIP_DIRS):
                continue
                
            markdown_files.append(path)
            
        logger.info(f"Found {len(markdown_files)} markdown files")
        return markdown_files
    
    def extract_links(self, file_path: Path) -> Dict[str, List[str]]:
        """Extract all links from a markdown file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract inline links
        inline_links = MARKDOWN_LINK_PATTERN.findall(content)
        
        # Process reference links
        ref_links = REFERENCE_LINK_PATTERN.findall(content)
        ref_defs = dict(REFERENCE_DEF_PATTERN.findall(content))
        
        # Organize links by type (internal vs external)
        links = {
            "internal": [],
            "external": []
        }
        
        # Process inline links
        for text, url in inline_links:
            url = url.split(' ')[0]  # Remove title if present
            if self._is_external_link(url):
                links["external"].append(url)
            else:
                links["internal"].append(url)
                
        # Process reference links
        for text, ref in ref_links:
            ref_key = ref if ref else text
            if ref_key in ref_defs:
                url = ref_defs[ref_key]
                if self._is_external_link(url):
                    links["external"].append(url)
                else:
                    links["internal"].append(url)
        
        return links
    
    def _is_external_link(self, url: str) -> bool:
        """Check if a URL is external (starts with http:// or https://)."""
        return url.startswith(('http://', 'https://'))
    
    def verify_internal_link(self, file_path: Path, link: str) -> bool:
        """
        Verify if an internal link is valid.
        Returns True if link is valid, False otherwise.
        """
        if link in self.internal_links_checked:
            # We've already checked this link
            return True
            
        self.internal_links_checked.add(link)
        
        # Handle anchor links (links to sections within the same file)
        if link.startswith('#'):
            # We can't reliably check anchors without parsing the document structure
            # So we'll assume they're valid for now
            return True
            
        # Get the directory containing the current file
        base_dir = file_path.parent
        
        # Handle relative links
        target_path = None
        if link.startswith('/'):
            # Absolute path from project root
            target_path = self.root_dir / link[1:]
        else:
            # Relative path from current file
            target_path = (base_dir / link).resolve()
        
        # Extract any anchor or query parameter
        if '#' in link:
            target_path = Path(str(target_path).split('#')[0])
        if '?' in link:
            target_path = Path(str(target_path).split('?')[0])
            
        # Check if the target exists
        if target_path.exists():
            return True
            
        # Check if adding .md extension makes it exist
        if not target_path.suffix and (target_path.with_suffix('.md')).exists():
            return True
            
        # Check if it points to a directory with an index.md file
        if target_path.is_dir() and (target_path / 'index.md').exists():
            return True
            
        # Link is broken
        logger.warning(f"Broken internal link: {link} in {file_path}")
        self.broken_links["internal"].append((str(file_path), link))
        return False
    
    def verify_external_link(self, file_path: Path, url: str) -> bool:
        """
        Verify if an external URL is accessible.
        Returns True if URL is accessible, False otherwise.
        """
        if url in self.external_links_checked:
            # We've already checked this URL
            return self.external_links_checked[url]
            
        try:
            # Use HEAD request to check if URL exists
            response = requests.head(url, allow_redirects=True, timeout=10, headers=HEADERS)
            
            # If HEAD request fails, try GET request
            if response.status_code >= 400:
                response = requests.get(url, timeout=10, headers=HEADERS)
                
            is_valid = response.status_code < 400
            self.external_links_checked[url] = is_valid
            
            if not is_valid:
                logger.warning(f"Broken external link: {url} (Status: {response.status_code}) in {file_path}")
                self.broken_links["external"].append((str(file_path), url))
                
            return is_valid
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error checking URL {url}: {str(e)}")
            self.external_links_checked[url] = False
            self.broken_links["external"].append((str(file_path), url))
            return False
    
    def check_file(self, file_path: Path) -> None:
        """Check all links in a single markdown file."""
        logger.info(f"Checking links in: {file_path}")
        
        links = self.extract_links(file_path)
        
        # Verify internal links
        for link in links["internal"]:
            self.verify_internal_link(file_path, link)
            
        # Verify external links
        for url in links["external"]:
            self.verify_external_link(file_path, url)
    
    def check_all_files(self) -> None:
        """Check all markdown files in the project."""
        markdown_files = self.find_markdown_files()
        
        # Check files in parallel
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.check_file, markdown_files)
    
    def generate_report(self) -> None:
        """Generate and print a report of the broken links."""
        total_broken = len(self.broken_links["internal"]) + len(self.broken_links["external"])
        
        logger.info(f"\n=== Link Check Report ===")
        logger.info(f"Total broken links: {total_broken}")
        logger.info(f"Internal broken links: {len(self.broken_links['internal'])}")
        logger.info(f"External broken links: {len(self.broken_links['external'])}")
        
        if total_broken > 0:
            logger.info("\n=== Broken Internal Links ===")
            for file_path, link in self.broken_links["internal"]:
                logger.info(f"In {file_path}: {link}")
                
            logger.info("\n=== Broken External Links ===")
            for file_path, url in self.broken_links["external"]:
                logger.info(f"In {file_path}: {url}")
                
        # Save report to file
        report_path = self.root_dir / "project-planning" / "link_check_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Link Check Report\n\n")
            f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- Total broken links: {total_broken}\n")
            f.write(f"- Internal broken links: {len(self.broken_links['internal'])}\n")
            f.write(f"- External broken links: {len(self.broken_links['external'])}\n\n")
            
            if self.broken_links["internal"]:
                f.write("## Broken Internal Links\n\n")
                f.write("| File | Link |\n|------|------|\n")
                for file_path, link in self.broken_links["internal"]:
                    f.write(f"| {file_path} | {link} |\n")
                f.write("\n")
                
            if self.broken_links["external"]:
                f.write("## Broken External Links\n\n")
                f.write("| File | URL |\n|------|-----|\n")
                for file_path, url in self.broken_links["external"]:
                    f.write(f"| {file_path} | {url} |\n")
        
        logger.info(f"Report saved to: {report_path}")

if __name__ == "__main__":
    # Get project root directory from command-line argument or use default
    root_dir = sys.argv[1] if len(sys.argv) > 1 else ".."
    
    checker = LinkChecker(root_dir)
    checker.check_all_files()
    checker.generate_report()
    
    # Exit with error code if broken links were found
    if len(checker.broken_links["internal"]) + len(checker.broken_links["external"]) > 0:
        sys.exit(1)
