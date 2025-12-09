"""Unit tests for LinkValidator."""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch
import aiohttp

from csa_docs_tools.link_validator import LinkValidator, LinkResult


class TestLinkValidator:
    """Test cases for LinkValidator class."""

    @pytest.mark.unit
    def test_init(self, temp_docs_root):
        """Test LinkValidator initialization."""
        validator = LinkValidator(temp_docs_root, "https://example.com")
        
        assert validator.docs_root == Path(temp_docs_root)
        assert validator.base_url == "https://example.com"
        assert validator.session is None

    @pytest.mark.unit
    def test_find_all_links_markdown(self, temp_docs_root):
        """Test finding markdown links in file."""
        validator = LinkValidator(temp_docs_root)
        
        # Test with the index.md file from temp fixture
        index_file = temp_docs_root / "docs" / "index.md"
        links = validator.find_all_links(index_file)
        
        assert len(links) > 0
        
        # Check that different link types are found
        link_urls = [link[0] for link in links]
        link_types = [link[2] for link in links]
        
        assert "architecture/overview.md" in link_urls
        assert "https://portal.azure.com" in link_urls
        assert "images/architecture.png" in link_urls
        
        assert "markdown" in link_types
        assert "image" in link_types

    @pytest.mark.unit
    def test_find_all_links_html(self, tmp_path):
        """Test finding HTML links in file."""
        validator = LinkValidator(tmp_path)
        
        html_content = """# Test
        
This has an HTML link: <a href="https://example.com">Example</a>
and an image: <img src="test.png" alt="Test">
"""
        
        test_file = tmp_path / "test.md"
        test_file.write_text(html_content)
        
        links = validator.find_all_links(test_file)
        
        assert len(links) == 2
        
        link_urls = [link[0] for link in links]
        assert "https://example.com" in link_urls
        assert "test.png" in link_urls

    @pytest.mark.unit
    def test_categorize_link(self, temp_docs_root):
        """Test link categorization."""
        validator = LinkValidator(temp_docs_root)
        
        assert validator.categorize_link("#section") == "anchor"
        assert validator.categorize_link("https://example.com") == "external"
        assert validator.categorize_link("http://example.com") == "external"
        assert validator.categorize_link("/docs/index.md") == "internal"
        assert validator.categorize_link("./relative.md") == "relative"
        assert validator.categorize_link("relative.md") == "relative"

    @pytest.mark.unit
    def test_resolve_relative_link(self, temp_docs_root):
        """Test resolving relative links."""
        validator = LinkValidator(temp_docs_root)
        
        source_file = temp_docs_root / "docs" / "architecture" / "overview.md"
        
        # Test relative link
        resolved = validator.resolve_relative_link("../index.md", source_file)
        expected = (temp_docs_root / "docs" / "index.md").resolve()
        assert resolved == expected
        
        # Test anchor-only link
        resolved = validator.resolve_relative_link("#section", source_file)
        assert resolved == source_file

    @pytest.mark.unit
    def test_validate_internal_link_exists(self, temp_docs_root):
        """Test validating internal link that exists."""
        validator = LinkValidator(temp_docs_root)
        
        source_file = temp_docs_root / "docs" / "index.md"
        result = validator.validate_internal_link("architecture/overview.md", source_file)
        
        assert result.is_valid
        assert result.status_code == 200
        assert result.error_message is None

    @pytest.mark.unit
    def test_validate_internal_link_missing(self, temp_docs_root):
        """Test validating internal link that doesn't exist."""
        validator = LinkValidator(temp_docs_root)
        
        source_file = temp_docs_root / "docs" / "index.md"
        result = validator.validate_internal_link("nonexistent.md", source_file)
        
        assert not result.is_valid
        assert result.status_code == 404
        assert "not found" in result.error_message.lower()

    @pytest.mark.unit
    def test_validate_internal_link_anchor(self, temp_docs_root):
        """Test validating anchor links."""
        validator = LinkValidator(temp_docs_root)
        
        source_file = temp_docs_root / "docs" / "index.md"
        result = validator.validate_internal_link("#section", source_file)
        
        assert result.is_valid  # Anchors assumed valid for now
        assert result.status_code is None

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_validate_external_link_success(self, temp_docs_root):
        """Test validating successful external link."""
        async with LinkValidator(temp_docs_root) as validator:
            # Mock the session response
            with patch.object(validator.session, 'head') as mock_head:
                mock_response = Mock()
                mock_response.status = 200
                mock_response.__aenter__ = AsyncMock(return_value=mock_response)
                mock_response.__aexit__ = AsyncMock(return_value=None)
                mock_head.return_value = mock_response
                
                result = await validator.validate_external_link(
                    "https://example.com", "test.md", 1
                )
                
                assert result.is_valid
                assert result.status_code == 200
                assert result.error_message is None

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_validate_external_link_failure(self, temp_docs_root):
        """Test validating failed external link."""
        async with LinkValidator(temp_docs_root) as validator:
            with patch.object(validator.session, 'head') as mock_head:
                mock_response = Mock()
                mock_response.status = 404
                mock_response.__aenter__ = AsyncMock(return_value=mock_response)
                mock_response.__aexit__ = AsyncMock(return_value=None)
                mock_head.return_value = mock_response
                
                result = await validator.validate_external_link(
                    "https://example.com/404", "test.md", 1
                )
                
                assert not result.is_valid
                assert result.status_code == 404
                assert "HTTP 404" in result.error_message

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_validate_external_link_timeout(self, temp_docs_root):
        """Test validating external link with timeout."""
        async with LinkValidator(temp_docs_root) as validator:
            with patch.object(validator.session, 'head') as mock_head:
                mock_head.side_effect = asyncio.TimeoutError()
                
                result = await validator.validate_external_link(
                    "https://slow.example.com", "test.md", 1
                )
                
                assert not result.is_valid
                assert result.status_code is None
                assert "timeout" in result.error_message.lower()

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_validate_external_link_client_error(self, temp_docs_root):
        """Test validating external link with client error."""
        async with LinkValidator(temp_docs_root) as validator:
            with patch.object(validator.session, 'head') as mock_head:
                mock_head.side_effect = aiohttp.ClientError("Connection failed")
                
                result = await validator.validate_external_link(
                    "https://error.example.com", "test.md", 1
                )
                
                assert not result.is_valid
                assert result.status_code is None
                assert "Client error" in result.error_message

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_validate_all_links(self, temp_docs_root):
        """Test validating all links in documentation."""
        async with LinkValidator(temp_docs_root) as validator:
            # Mock external link validation
            with patch.object(validator, 'validate_external_link') as mock_external:
                mock_external.return_value = LinkResult(
                    url="https://portal.azure.com",
                    status_code=200,
                    is_valid=True,
                    error_message=None,
                    source_file="docs/index.md",
                    line_number=1
                )
                
                results = await validator.validate_all_links(check_external=True)
                
                assert len(results) > 0
                
                # Check that we have both internal and external link results
                link_types = [validator.categorize_link(r.url) for r in results]
                assert any(t in ['relative', 'internal'] for t in link_types)
                assert any(t == 'external' for t in link_types)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_validate_all_links_no_external(self, temp_docs_root):
        """Test validating links without checking external links."""
        async with LinkValidator(temp_docs_root) as validator:
            results = await validator.validate_all_links(check_external=False)
            
            # Should only have internal/relative links
            external_results = [
                r for r in results 
                if validator.categorize_link(r.url) == 'external'
            ]
            assert len(external_results) == 0

    @pytest.mark.unit
    def test_get_broken_links(self, temp_docs_root):
        """Test filtering broken links."""
        validator = LinkValidator(temp_docs_root)
        
        results = [
            LinkResult("test1.md", 200, True, None, "source.md", 1),
            LinkResult("missing.md", 404, False, "Not found", "source.md", 2),
            LinkResult("test2.md", 200, True, None, "source.md", 3),
        ]
        
        broken = validator.get_broken_links(results)
        
        assert len(broken) == 1
        assert broken[0].url == "missing.md"
        assert not broken[0].is_valid

    @pytest.mark.unit
    def test_generate_report(self, temp_docs_root):
        """Test generating link validation report."""
        validator = LinkValidator(temp_docs_root)
        
        results = [
            LinkResult("test1.md", 200, True, None, "source.md", 1),
            LinkResult("https://example.com", 200, True, None, "source.md", 2),
            LinkResult("missing.md", 404, False, "Not found", "source.md", 3),
            LinkResult("#anchor", None, True, None, "source.md", 4),
        ]
        
        report = validator.generate_report(results)
        
        assert report['total_links'] == 4
        assert report['valid_links'] == 3
        assert report['broken_links'] == 1
        assert report['success_rate'] == 75.0
        
        assert 200 in report['status_codes']
        assert 404 in report['status_codes']
        
        assert 'external' in report['link_types']
        assert 'relative' in report['link_types']
        
        assert len(report['broken_link_details']) == 1

    @pytest.mark.unit
    def test_async_context_manager(self, temp_docs_root):
        """Test async context manager functionality."""
        validator = LinkValidator(temp_docs_root)
        
        # Test that session is None initially
        assert validator.session is None
        
        # Test context manager protocol
        assert hasattr(validator, '__aenter__')
        assert hasattr(validator, '__aexit__')

    @pytest.mark.unit
    def test_find_links_error_handling(self, tmp_path):
        """Test error handling when reading files."""
        validator = LinkValidator(tmp_path)
        
        # Test with non-existent file
        nonexistent = tmp_path / "nonexistent.md"
        links = validator.find_links_in_file(nonexistent)  # Should not raise
        
        # Exact behavior depends on implementation, but should handle gracefully
        assert isinstance(links, list)

    @pytest.mark.unit
    def test_resolve_link_edge_cases(self, temp_docs_root):
        """Test edge cases in link resolution."""
        validator = LinkValidator(temp_docs_root)
        source_file = temp_docs_root / "docs" / "index.md"
        
        # Test empty link
        resolved = validator.resolve_relative_link("", source_file)
        assert resolved == source_file
        
        # Test link with fragment
        resolved = validator.resolve_relative_link("other.md#section", source_file)
        expected = (temp_docs_root / "docs" / "other.md").resolve()
        assert resolved == expected

    @pytest.mark.unit
    def test_validate_internal_link_error_handling(self, temp_docs_root):
        """Test error handling in internal link validation."""
        validator = LinkValidator(temp_docs_root)
        
        # Test with problematic path (should handle gracefully)
        source_file = temp_docs_root / "docs" / "index.md"
        
        # This should not raise an exception
        result = validator.validate_internal_link("../../../etc/passwd", source_file)
        assert isinstance(result, LinkResult)
        assert isinstance(result.is_valid, bool)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_no_session_external_validation(self, temp_docs_root):
        """Test external link validation without session."""
        validator = LinkValidator(temp_docs_root)
        # Don't use async context manager
        
        result = await validator.validate_external_link(
            "https://example.com", "test.md", 1
        )
        
        assert not result.is_valid
        assert "No HTTP session" in result.error_message