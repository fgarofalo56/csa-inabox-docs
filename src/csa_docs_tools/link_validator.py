"""Link validation utilities for documentation.

Architecture:
  - Module-level pure functions: categorize_link(), validate_url_scheme(),
    resolve_relative_link(), generate_link_report()  — no I/O, fully unit-testable.
  - LinkValidator class: orchestrates I/O (file reads, DNS, HTTP) and
    delegates to the pure functions above.
"""

import asyncio
import socket
import ipaddress
import aiohttp
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from urllib.parse import urlparse
import logging
from dataclasses import dataclass

from .markdown_parser import MarkdownParser

logger = logging.getLogger(__name__)

# URI schemes that should be skipped (not validated as files or external links)
SKIP_SCHEMES = frozenset({'mailto', 'tel', 'ftp', 'ftps', 'javascript', 'data', 'blob'})

# Allowed schemes for external link validation
ALLOWED_EXTERNAL_SCHEMES = frozenset({'http', 'https'})


@dataclass
class LinkResult:
    """Result of link validation."""
    url: str
    status_code: Optional[int]
    is_valid: bool
    error_message: Optional[str]
    source_file: str
    line_number: int


# ---------------------------------------------------------------------------
# Pure functions (no I/O, no side effects — fully unit-testable)
# ---------------------------------------------------------------------------

def categorize_link(url: str) -> str:
    """Categorize a link by type.

    Pure function — no I/O.

    Args:
        url: URL to categorize

    Returns:
        Link category: 'external', 'internal', 'anchor', 'relative', 'skip'
    """
    if url.startswith('#'):
        return 'anchor'

    parsed = urlparse(url)
    scheme = parsed.scheme.lower()

    if scheme in SKIP_SCHEMES:
        return 'skip'
    elif scheme in ALLOWED_EXTERNAL_SCHEMES:
        return 'external'
    elif scheme:
        return 'skip'
    elif url.startswith('/'):
        return 'internal'
    else:
        return 'relative'


def validate_url_scheme(url: str) -> Optional[str]:
    """Validate the scheme and hostname of a URL.

    Pure function — checks URL structure without DNS/network I/O.

    Args:
        url: URL to validate

    Returns:
        Error message if URL is structurally unsafe, None if OK
    """
    parsed = urlparse(url)

    if parsed.scheme.lower() not in ALLOWED_EXTERNAL_SCHEMES:
        return f"Disallowed URL scheme: {parsed.scheme}"

    if not parsed.hostname:
        return "URL has no hostname"

    return None


def resolve_relative_link(link: str, source_dir: Path, docs_root: Path) -> Path:
    """Resolve a relative link to an absolute file path.

    Pure path computation — no filesystem access.

    Args:
        link: Relative link string
        source_dir: Directory containing the source file
        docs_root: Documentation root directory

    Returns:
        Resolved absolute path
    """
    link_path = link.split('#')[0]
    if not link_path:
        return source_dir

    if link_path.startswith('/'):
        return (docs_root / link_path.lstrip('/')).resolve(strict=False)
    else:
        return (source_dir / link_path).resolve(strict=False)


def generate_link_report(results: List[LinkResult]) -> Dict:
    """Generate a summary report of link validation.

    Pure function — no I/O.

    Args:
        results: List of LinkResult objects

    Returns:
        Dictionary with validation statistics
    """
    total_links = len(results)
    broken = [r for r in results if not r.is_valid]
    valid_links = total_links - len(broken)

    status_counts: Dict = {}
    for result in results:
        status = result.status_code or 'unknown'
        status_counts[status] = status_counts.get(status, 0) + 1

    link_types: Dict = {}
    for result in results:
        lt = categorize_link(result.url)
        link_types[lt] = link_types.get(lt, 0) + 1

    return {
        'total_links': total_links,
        'valid_links': valid_links,
        'broken_links': len(broken),
        'success_rate': (valid_links / total_links * 100) if total_links > 0 else 0,
        'status_codes': status_counts,
        'link_types': link_types,
        'broken_link_details': [
            {
                'url': r.url,
                'file': r.source_file,
                'line': r.line_number,
                'error': r.error_message
            }
            for r in broken
        ]
    }


# ---------------------------------------------------------------------------
# Validator class (I/O boundary — file reads, DNS, HTTP)
# ---------------------------------------------------------------------------

class LinkValidator:
    """Validate links in markdown documentation.

    Orchestrates I/O (file reading, HTTP requests) and delegates to
    pure functions for link categorisation, path resolution, and reporting.
    """

    def __init__(
        self,
        docs_root: Path,
        base_url: str = "",
        timeout: int = 30,
        connect_timeout: int = 10,
        max_connections: int = 50,
        max_connections_per_host: int = 10,
        batch_size: int = 20,
        block_private_ips: bool = True,
    ):
        self.docs_root = Path(docs_root)
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.timeout = timeout
        self.connect_timeout = connect_timeout
        self.max_connections = max_connections
        self.max_connections_per_host = max_connections_per_host
        self.batch_size = batch_size
        self.block_private_ips = block_private_ips
        self._parser = MarkdownParser()
        self.markdown_extensions = {'.md', '.markdown'}

    # -- Delegate pure helpers so existing call-sites still work -------

    def categorize_link(self, url: str) -> str:  # noqa: D102
        return categorize_link(url)

    def resolve_relative_link(self, link: str, source_file: Path) -> Path:  # noqa: D102
        link_path = link.split('#')[0]
        if not link_path:
            return source_file  # Anchor-only: return the source file itself
        return resolve_relative_link(link, source_file.parent, self.docs_root)

    def get_broken_links(self, results: List[LinkResult]) -> List[LinkResult]:  # noqa: D102
        return [r for r in results if not r.is_valid]

    def generate_report(self, results: List[LinkResult]) -> Dict:  # noqa: D102
        return generate_link_report(results)

    # -- Context manager for HTTP session ------------------------------

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=self.timeout, connect=self.connect_timeout)
        connector = aiohttp.TCPConnector(
            limit=self.max_connections,
            limit_per_host=self.max_connections_per_host,
        )
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={'User-Agent': 'CSA-Docs-Link-Checker/1.0'}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    # -- I/O methods ---------------------------------------------------

    def find_all_links(self, file_path: Path) -> List[Tuple[str, int, str]]:
        """Find all links in a markdown file using AST parser (file I/O)."""
        links = []
        try:
            doc = self._parser.parse_file(file_path)
            for link in doc.links:
                links.append((link.url, link.line_number, link.link_type))
            for image in doc.images:
                links.append((image.src, image.line_number, 'image'))
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
        return links

    def _is_private_ip(self, hostname: str) -> bool:
        """Check if hostname resolves to a private IP (DNS I/O)."""
        try:
            for info in socket.getaddrinfo(hostname, None):
                ip_str = info[4][0]
                ip = ipaddress.ip_address(ip_str)
                if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local:
                    return True
        except (socket.gaierror, ValueError):
            pass
        return False

    def _validate_url_safety(self, url: str) -> Optional[str]:
        """Validate URL safety (pure scheme check + DNS-based SSRF check)."""
        scheme_error = validate_url_scheme(url)
        if scheme_error:
            return scheme_error

        parsed = urlparse(url)
        if self.block_private_ips and self._is_private_ip(parsed.hostname):
            return f"Blocked request to private/internal IP: {parsed.hostname}"

        return None

    def _extract_anchors(self, file_path: Path) -> Set[str]:
        """Extract anchor targets from a markdown file (file I/O)."""
        anchors: Set[str] = set()
        try:
            doc = self._parser.parse_file(file_path)
            for heading in doc.headings:
                if heading.slug:
                    anchors.add(heading.slug)
            for html_id in doc.html_ids:
                anchors.add(html_id)
        except Exception as e:
            logger.debug(f"Could not extract anchors from {file_path}: {e}")
        return anchors

    def validate_internal_link(self, link: str, source_file: Path) -> LinkResult:
        """Validate an internal/relative link (filesystem I/O)."""
        try:
            anchor = None
            if '#' in link:
                parts = link.split('#', 1)
                link_path_part = parts[0]
                anchor = parts[1] if len(parts) > 1 else None
            else:
                link_path_part = link

            if not link_path_part:
                if anchor:
                    file_anchors = self._extract_anchors(source_file)
                    if anchor.lower() not in {a.lower() for a in file_anchors}:
                        return LinkResult(
                            url=link, status_code=None, is_valid=False,
                            error_message=f"Anchor '#{anchor}' not found in {source_file.name}",
                            source_file=str(source_file), line_number=0
                        )
                return LinkResult(
                    url=link, status_code=None, is_valid=True,
                    error_message=None, source_file=str(source_file), line_number=0
                )

            resolved_path = self.resolve_relative_link(link, source_file)

            if not resolved_path.exists():
                return LinkResult(
                    url=link, status_code=404, is_valid=False,
                    error_message=f"File not found: {resolved_path}",
                    source_file=str(source_file), line_number=0
                )

            if anchor:
                file_anchors = self._extract_anchors(resolved_path)
                if anchor.lower() not in {a.lower() for a in file_anchors}:
                    return LinkResult(
                        url=link, status_code=None, is_valid=False,
                        error_message=f"Anchor '#{anchor}' not found in {resolved_path.name}",
                        source_file=str(source_file), line_number=0
                    )

            return LinkResult(
                url=link, status_code=200, is_valid=True,
                error_message=None, source_file=str(source_file), line_number=0
            )

        except Exception as e:
            return LinkResult(
                url=link, status_code=None, is_valid=False,
                error_message=str(e), source_file=str(source_file), line_number=0
            )

    async def validate_external_link(self, url: str, source_file: str, line_num: int) -> LinkResult:
        """Validate an external HTTP/HTTPS link (network I/O)."""
        if not self.session:
            return LinkResult(
                url=url, status_code=None, is_valid=False,
                error_message="No HTTP session available",
                source_file=source_file, line_number=line_num
            )

        safety_error = self._validate_url_safety(url)
        if safety_error:
            return LinkResult(
                url=url, status_code=None, is_valid=False,
                error_message=f"Security: {safety_error}",
                source_file=source_file, line_number=line_num
            )

        try:
            async with self.session.head(url, allow_redirects=True) as response:
                if response.status in (405, 501):
                    async with self.session.get(url, allow_redirects=True) as get_response:
                        is_valid = get_response.status < 400
                        return LinkResult(
                            url=url, status_code=get_response.status, is_valid=is_valid,
                            error_message=None if is_valid else f"HTTP {get_response.status}",
                            source_file=source_file, line_number=line_num
                        )
                is_valid = response.status < 400
                return LinkResult(
                    url=url, status_code=response.status, is_valid=is_valid,
                    error_message=None if is_valid else f"HTTP {response.status}",
                    source_file=source_file, line_number=line_num
                )
        except asyncio.TimeoutError:
            return LinkResult(
                url=url, status_code=None, is_valid=False,
                error_message="Request timeout",
                source_file=source_file, line_number=line_num
            )
        except aiohttp.ClientError as e:
            return LinkResult(
                url=url, status_code=None, is_valid=False,
                error_message=f"Client error: {e}",
                source_file=source_file, line_number=line_num
            )
        except Exception as e:
            return LinkResult(
                url=url, status_code=None, is_valid=False,
                error_message=f"Unexpected error: {e}",
                source_file=source_file, line_number=line_num
            )

    async def validate_all_links(self, check_external: bool = True) -> List[LinkResult]:
        """Validate all links in the documentation (orchestration)."""
        results = []
        external_tasks = []

        markdown_files = []
        for ext in self.markdown_extensions:
            markdown_files.extend(self.docs_root.glob(f"**/*{ext}"))

        for file_path in markdown_files:
            links = self.find_all_links(file_path)

            for link_url, line_num, link_type in links:
                category = categorize_link(link_url)

                if category == 'skip':
                    continue
                elif category in ['relative', 'internal', 'anchor']:
                    result = self.validate_internal_link(link_url, file_path)
                    result.line_number = line_num
                    results.append(result)
                elif category == 'external' and check_external:
                    external_tasks.append(
                        self.validate_external_link(link_url, str(file_path), line_num)
                    )

        if external_tasks:
            for i in range(0, len(external_tasks), self.batch_size):
                batch = external_tasks[i:i + self.batch_size]
                batch_results = await asyncio.gather(*batch, return_exceptions=True)
                for result in batch_results:
                    if isinstance(result, Exception):
                        results.append(LinkResult(
                            url="unknown", status_code=None, is_valid=False,
                            error_message=str(result),
                            source_file="unknown", line_number=0
                        ))
                    else:
                        results.append(result)

        return results
