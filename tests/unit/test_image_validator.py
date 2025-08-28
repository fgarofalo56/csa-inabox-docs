"""Unit tests for ImageReferenceValidator."""

import pytest
from pathlib import Path
from unittest.mock import patch, Mock
from PIL import Image

from src.csa_docs_tools.image_validator import ImageReferenceValidator, ImageIssue


class TestImageReferenceValidator:
    """Test cases for ImageReferenceValidator class."""

    @pytest.mark.unit
    def test_init(self, temp_docs_root):
        """Test ImageReferenceValidator initialization."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        assert validator.docs_root == Path(temp_docs_root)
        assert '.png' in validator.supported_formats
        assert '.jpg' in validator.supported_formats
        assert '.svg' in validator.supported_formats

    @pytest.mark.unit
    def test_find_image_references_markdown(self, temp_docs_root):
        """Test finding markdown image references."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        # Test with index.md from fixture
        index_file = temp_docs_root / "docs" / "index.md"
        references = validator.find_image_references(index_file)
        
        assert len(references) > 0
        
        # Check that we found the architecture diagram
        image_paths = [ref[0] for ref in references]
        alt_texts = [ref[2] for ref in references]
        
        assert "images/architecture.png" in image_paths
        assert "Architecture Diagram" in alt_texts

    @pytest.mark.unit
    def test_find_image_references_html(self, tmp_path):
        """Test finding HTML image references."""
        validator = ImageReferenceValidator(tmp_path)
        
        content = """# Test Document

Here's an HTML image: <img src="test.png" alt="Test Image">

And another: <img src="diagrams/flow.svg" alt="">
"""
        
        test_file = tmp_path / "test.md"
        test_file.write_text(content)
        
        references = validator.find_image_references(test_file)
        
        assert len(references) == 2
        
        paths = [ref[0] for ref in references]
        assert "test.png" in paths
        assert "diagrams/flow.svg" in paths

    @pytest.mark.unit
    def test_find_image_references_error_handling(self, tmp_path):
        """Test error handling when file cannot be read."""
        validator = ImageReferenceValidator(tmp_path)
        
        # Test with non-existent file
        nonexistent = tmp_path / "nonexistent.md"
        references = validator.find_image_references(nonexistent)
        
        assert isinstance(references, list)
        assert len(references) == 0

    @pytest.mark.unit
    def test_validate_image_exists_relative_path(self, temp_docs_root):
        """Test image existence validation with relative paths."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        source_file = temp_docs_root / "docs" / "index.md"
        
        # Test existing image
        exists, resolved = validator.validate_image_exists("images/architecture.png", source_file)
        assert exists
        assert "architecture.png" in resolved
        
        # Test non-existing image
        exists, resolved = validator.validate_image_exists("images/nonexistent.png", source_file)
        assert not exists

    @pytest.mark.unit
    def test_validate_image_exists_absolute_path(self, temp_docs_root):
        """Test image existence validation with absolute paths."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        source_file = temp_docs_root / "docs" / "index.md"
        
        # Test absolute path (from docs root)
        exists, resolved = validator.validate_image_exists("/images/architecture.png", source_file)
        assert exists

    @pytest.mark.unit
    def test_validate_image_exists_external_url(self, temp_docs_root):
        """Test image existence validation with external URLs."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        source_file = temp_docs_root / "docs" / "index.md"
        
        # External URLs are assumed to exist
        exists, resolved = validator.validate_image_exists("https://example.com/image.png", source_file)
        assert exists
        assert resolved == "https://example.com/image.png"

    @pytest.mark.unit
    def test_validate_image_format_valid_png(self, temp_docs_root):
        """Test image format validation with valid PNG."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        # Test with existing PNG from fixture
        png_file = temp_docs_root / "docs" / "images" / "architecture.png"
        
        is_valid, error = validator.validate_image_format(png_file)
        assert is_valid
        assert error == ""

    @pytest.mark.unit
    def test_validate_image_format_valid_svg(self, temp_docs_root):
        """Test image format validation with valid SVG."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        # Test with existing SVG from fixture
        svg_file = temp_docs_root / "docs" / "images" / "delta-architecture.svg"
        
        is_valid, error = validator.validate_image_format(svg_file)
        assert is_valid
        assert error == ""

    @pytest.mark.unit
    def test_validate_image_format_nonexistent(self, temp_docs_root):
        """Test image format validation with non-existent file."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        nonexistent = temp_docs_root / "nonexistent.png"
        
        is_valid, error = validator.validate_image_format(nonexistent)
        assert not is_valid
        assert "does not exist" in error

    @pytest.mark.unit
    def test_validate_image_format_unsupported_extension(self, tmp_path):
        """Test image format validation with unsupported extension."""
        validator = ImageReferenceValidator(tmp_path)
        
        # Create file with unsupported extension
        unsupported = tmp_path / "test.xyz"
        unsupported.write_text("fake image")
        
        is_valid, error = validator.validate_image_format(unsupported)
        assert not is_valid
        assert "Unsupported image format" in error

    @pytest.mark.unit
    def test_validate_image_format_corrupted_image(self, tmp_path):
        """Test image format validation with corrupted image file."""
        validator = ImageReferenceValidator(tmp_path)
        
        # Create fake PNG file with invalid content
        fake_png = tmp_path / "fake.png"
        fake_png.write_bytes(b"not a real png file")
        
        is_valid, error = validator.validate_image_format(fake_png)
        assert not is_valid
        assert "Invalid image file" in error

    @pytest.mark.unit
    def test_validate_image_format_invalid_svg(self, tmp_path):
        """Test image format validation with invalid SVG."""
        validator = ImageReferenceValidator(tmp_path)
        
        # Create invalid SVG file
        invalid_svg = tmp_path / "invalid.svg"
        invalid_svg.write_text("not valid svg content")
        
        is_valid, error = validator.validate_image_format(invalid_svg)
        assert not is_valid
        assert "Invalid SVG file format" in error

    @pytest.mark.unit
    def test_check_image_properties_valid_image(self, temp_docs_root):
        """Test checking properties of valid image."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        # Test with PNG from fixture
        png_file = temp_docs_root / "docs" / "images" / "architecture.png"
        properties = validator.check_image_properties(png_file)
        
        assert 'width' in properties
        assert 'height' in properties
        assert 'file_size' in properties
        assert 'format' in properties
        assert 'issues' in properties
        
        assert isinstance(properties['width'], int)
        assert isinstance(properties['height'], int)
        assert isinstance(properties['file_size'], int)

    @pytest.mark.unit
    def test_check_image_properties_large_file(self, tmp_path):
        """Test checking properties with large file size."""
        validator = ImageReferenceValidator(tmp_path)
        
        # Create a "large" file (simulate with metadata)
        large_file = tmp_path / "large.png"
        # Create minimal PNG and patch file size
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        large_file.write_bytes(png_data)
        
        with patch.object(Path, 'stat') as mock_stat:
            mock_stat.return_value.st_size = 6 * 1024 * 1024  # 6MB
            
            properties = validator.check_image_properties(large_file)
            
            assert any("Large file size" in issue for issue in properties['issues'])

    @pytest.mark.unit
    def test_check_image_properties_large_dimensions(self, tmp_path):
        """Test checking properties with large dimensions."""
        validator = ImageReferenceValidator(tmp_path)
        
        # Mock PIL Image to return large dimensions
        with patch('PIL.Image.open') as mock_open:
            mock_img = Mock()
            mock_img.width = 3000
            mock_img.height = 2500
            mock_img.format = "PNG"
            mock_open.return_value.__enter__.return_value = mock_img
            
            test_file = tmp_path / "large_image.png"
            test_file.write_bytes(b"fake png data")
            
            properties = validator.check_image_properties(test_file)
            
            assert any("Large dimensions" in issue for issue in properties['issues'])

    @pytest.mark.unit
    def test_check_image_properties_small_dimensions(self, tmp_path):
        """Test checking properties with small dimensions."""
        validator = ImageReferenceValidator(tmp_path)
        
        with patch('PIL.Image.open') as mock_open:
            mock_img = Mock()
            mock_img.width = 50
            mock_img.height = 30
            mock_img.format = "PNG"
            mock_open.return_value.__enter__.return_value = mock_img
            
            test_file = tmp_path / "small_image.png"
            test_file.write_bytes(b"fake png data")
            
            properties = validator.check_image_properties(test_file)
            
            assert any("Small dimensions" in issue for issue in properties['issues'])

    @pytest.mark.unit
    def test_check_image_properties_svg(self, temp_docs_root):
        """Test checking properties of SVG file."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        svg_file = temp_docs_root / "docs" / "images" / "delta-architecture.svg"
        properties = validator.check_image_properties(svg_file)
        
        assert properties['format'] == 'SVG'
        assert properties['width'] is None  # SVG dimensions not analyzed
        assert properties['height'] is None

    @pytest.mark.unit
    def test_validate_alt_text_valid(self, temp_docs_root):
        """Test alt text validation with valid text."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        issues = validator.validate_alt_text("Azure Synapse Analytics architecture diagram", "architecture.png")
        
        assert len(issues) == 0

    @pytest.mark.unit
    def test_validate_alt_text_missing(self, temp_docs_root):
        """Test alt text validation with missing text."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        issues = validator.validate_alt_text("", "architecture.png")
        
        assert len(issues) == 1
        assert "Missing alt text" in issues[0]

    @pytest.mark.unit
    def test_validate_alt_text_too_long(self, temp_docs_root):
        """Test alt text validation with text that's too long."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        long_text = "This is an extremely long alt text that goes on and on and on and exceeds the recommended character limit for accessibility"
        issues = validator.validate_alt_text(long_text, "architecture.png")
        
        assert len(issues) >= 1
        assert any("too long" in issue for issue in issues)

    @pytest.mark.unit
    def test_validate_alt_text_too_short(self, temp_docs_root):
        """Test alt text validation with text that's too short."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        issues = validator.validate_alt_text("Chart", "architecture.png")
        
        assert len(issues) >= 1
        assert any("too short" in issue for issue in issues)

    @pytest.mark.unit
    def test_validate_alt_text_redundant_phrases(self, temp_docs_root):
        """Test alt text validation with redundant phrases."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        issues = validator.validate_alt_text("Image of Azure architecture diagram", "architecture.png")
        
        assert len(issues) >= 1
        assert any("Redundant phrase" in issue for issue in issues)

    @pytest.mark.unit
    def test_validate_alt_text_contains_filename(self, temp_docs_root):
        """Test alt text validation when it contains filename."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        issues = validator.validate_alt_text("Architecture diagram from architecture.png file", "architecture.png")
        
        assert len(issues) >= 1
        assert any("filename" in issue for issue in issues)

    @pytest.mark.unit
    def test_find_unused_images(self, temp_docs_root):
        """Test finding unused image files."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        unused = validator.find_unused_images()
        
        # Should find the unused.png from fixture
        unused_names = [img.name for img in unused]
        assert "unused.png" in unused_names

    @pytest.mark.unit
    def test_validate_all_images(self, temp_docs_root):
        """Test comprehensive image validation."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        results = validator.validate_all_images()
        
        assert isinstance(results, dict)
        
        # Should have some validation results
        assert len(results) > 0
        
        # Check structure of results
        for file_path, issues in results.items():
            assert isinstance(file_path, str)
            assert file_path.endswith('.md')
            assert isinstance(issues, list)
            
            for issue in issues:
                assert isinstance(issue, ImageIssue)
                assert hasattr(issue, 'file_path')
                assert hasattr(issue, 'image_path')
                assert hasattr(issue, 'issue_type')
                assert hasattr(issue, 'severity')
                assert hasattr(issue, 'message')

    @pytest.mark.unit
    def test_generate_image_report(self, temp_docs_root):
        """Test generating image validation report."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        # Create sample validation results
        sample_issues = [
            ImageIssue("docs/index.md", 1, "missing.png", "missing_file", "error", "File not found"),
            ImageIssue("docs/index.md", 2, "large.png", "image_property", "warning", "Large file size"),
            ImageIssue("docs/guide.md", 5, "chart.png", "alt_text", "warning", "Missing alt text"),
        ]
        
        validation_results = {
            "docs/index.md": [sample_issues[0], sample_issues[1]],
            "docs/guide.md": [sample_issues[2]]
        }
        
        report = validator.generate_image_report(validation_results)
        
        assert 'total_markdown_files' in report
        assert 'files_with_image_issues' in report
        assert 'total_image_issues' in report
        assert 'total_images' in report
        assert 'unused_images' in report
        assert 'issue_type_breakdown' in report
        assert 'severity_breakdown' in report
        assert 'image_health_score' in report
        assert 'recommendations' in report
        
        assert report['files_with_image_issues'] == 2
        assert report['total_image_issues'] == 3
        
        assert 'missing_file' in report['issue_type_breakdown']
        assert 'error' in report['severity_breakdown']
        assert 'warning' in report['severity_breakdown']

    @pytest.mark.unit
    def test_generate_recommendations(self, temp_docs_root):
        """Test recommendation generation."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        # Test with various issue types
        validation_results = {
            "file1.md": [
                ImageIssue("file1.md", 1, "img1.png", "alt_text", "warning", "Missing alt text"),
                ImageIssue("file1.md", 2, "img2.png", "alt_text", "warning", "Alt text too short"),
                ImageIssue("file1.md", 3, "img3.png", "alt_text", "warning", "Missing alt text"),
                ImageIssue("file1.md", 4, "img4.png", "alt_text", "warning", "Missing alt text"),
                ImageIssue("file1.md", 5, "img5.png", "alt_text", "warning", "Missing alt text"),
                ImageIssue("file1.md", 6, "img6.png", "alt_text", "warning", "Missing alt text"),
            ],
            "file2.md": [
                ImageIssue("file2.md", 1, "large1.png", "image_property", "warning", "Large file size: 6.0MB"),
                ImageIssue("file2.md", 2, "large2.png", "image_property", "warning", "Large file size: 8.0MB"),
                ImageIssue("file2.md", 3, "large3.png", "image_property", "warning", "Large file size: 10.0MB"),
                ImageIssue("file2.md", 4, "large4.png", "image_property", "warning", "Large file size: 12.0MB"),
            ]
        }
        
        unused_images = [Path("unused1.png"), Path("unused2.png"), Path("unused3.png")]
        
        recommendations = validator._generate_recommendations(validation_results, unused_images)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Check for specific recommendations based on the issues
        recommendation_text = " ".join(recommendations).lower()
        assert "alt text" in recommendation_text  # Should recommend alt text improvements
        assert "optimize" in recommendation_text or "large" in recommendation_text  # Should recommend optimization
        assert "unused" in recommendation_text  # Should recommend removing unused images

    @pytest.mark.unit
    def test_image_health_score_calculation(self, temp_docs_root):
        """Test image health score calculation."""
        validator = ImageReferenceValidator(temp_docs_root)
        
        # Test with no issues
        validation_results = {}
        report = validator.generate_image_report(validation_results)
        assert report['image_health_score'] == 100.0
        
        # Test with some issues
        validation_results = {
            "file1.md": [
                ImageIssue("file1.md", 1, "img1.png", "missing_file", "error", "Not found"),
                ImageIssue("file1.md", 2, "img2.png", "alt_text", "warning", "Missing alt text"),
            ]
        }
        
        report = validator.generate_image_report(validation_results)
        assert report['image_health_score'] < 100.0

    @pytest.mark.unit
    def test_error_handling_image_analysis(self, tmp_path):
        """Test error handling during image analysis."""
        validator = ImageReferenceValidator(tmp_path)
        
        # Test with file that can't be analyzed
        test_file = tmp_path / "problematic.png"
        test_file.write_bytes(b"not a valid image")
        
        properties = validator.check_image_properties(test_file)
        
        # Should handle error gracefully
        assert 'issues' in properties
        assert len(properties['issues']) > 0