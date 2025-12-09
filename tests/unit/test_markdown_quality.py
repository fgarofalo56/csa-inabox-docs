"""Unit tests for MarkdownQualityChecker."""

import pytest
import json
import subprocess
from pathlib import Path
from unittest.mock import patch, Mock

from csa_docs_tools.markdown_quality import MarkdownQualityChecker, QualityIssue


class TestMarkdownQualityChecker:
    """Test cases for MarkdownQualityChecker class."""

    @pytest.mark.unit
    def test_init(self, temp_docs_root):
        """Test MarkdownQualityChecker initialization."""
        checker = MarkdownQualityChecker(temp_docs_root)
        
        assert checker.docs_root == Path(temp_docs_root)
        assert checker.config_file == Path(temp_docs_root) / ".markdownlint.json"
        assert 'heading_levels' in checker.quality_rules
        assert 'line_length' in checker.default_config

    @pytest.mark.unit
    def test_load_config_default(self, tmp_path):
        """Test loading default configuration."""
        checker = MarkdownQualityChecker(tmp_path)
        config = checker.load_config()
        
        assert isinstance(config, dict)
        assert 'line_length' in config
        assert 'max_heading_level' in config
        assert config['line_length'] == 120  # Default value

    @pytest.mark.unit
    def test_load_config_from_file(self, temp_docs_root):
        """Test loading configuration from file."""
        checker = MarkdownQualityChecker(temp_docs_root)
        config = checker.load_config()
        
        assert isinstance(config, dict)
        # Should merge default with file config
        assert 'line_length' in config
        assert 'max_heading_level' in config

    @pytest.mark.unit
    def test_load_config_invalid_json(self, tmp_path):
        """Test loading invalid JSON config file."""
        config_file = tmp_path / ".markdownlint.json"
        config_file.write_text("invalid json content")
        
        checker = MarkdownQualityChecker(tmp_path, config_file)
        config = checker.load_config()
        
        # Should fall back to default config
        assert config == checker.default_config

    @pytest.mark.unit
    def test_run_markdownlint_success(self, temp_docs_root):
        """Test successful markdownlint execution."""
        checker = MarkdownQualityChecker(temp_docs_root)
        
        # Mock successful markdownlint output
        mock_output = [
            {
                "fileName": "docs/index.md",
                "errors": [
                    {
                        "lineNumber": 10,
                        "columnNumber": 5,
                        "ruleNames": ["MD013"],
                        "ruleDescription": "Line length",
                        "errorDetail": "Line too long (125 > 120 characters)"
                    }
                ]
            }
        ]
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                stdout=json.dumps(mock_output),
                stderr="",
                returncode=0
            )
            
            issues = checker.run_markdownlint()
            
            assert len(issues) == 1
            issue = issues[0]
            assert issue.file_path == "docs/index.md"
            assert issue.line_number == 10
            assert issue.rule_id == "MD013"
            assert issue.severity == "error"

    @pytest.mark.unit
    def test_run_markdownlint_not_found(self, temp_docs_root):
        """Test markdownlint CLI not found."""
        checker = MarkdownQualityChecker(temp_docs_root)
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = FileNotFoundError("markdownlint not found")
            
            issues = checker.run_markdownlint()
            
            assert len(issues) == 0  # Should handle gracefully

    @pytest.mark.unit
    def test_run_markdownlint_error(self, temp_docs_root):
        """Test markdownlint execution error."""
        checker = MarkdownQualityChecker(temp_docs_root)
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "markdownlint")
            
            issues = checker.run_markdownlint()
            
            assert isinstance(issues, list)  # Should handle gracefully

    @pytest.mark.unit
    def test_check_heading_levels_valid(self, tmp_path):
        """Test heading level checking with valid headings."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Main Title
        
## Section 1

### Subsection 1.1

## Section 2

### Subsection 2.1

#### Deep section
"""
        
        lines = content.splitlines()
        config = checker.load_config()
        
        issues = checker._check_heading_levels(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) == 0

    @pytest.mark.unit
    def test_check_heading_levels_skip_level(self, tmp_path):
        """Test heading level checking with skipped levels."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Main Title
        
#### Deep section (skipping levels)
"""
        
        lines = content.splitlines()
        config = checker.load_config()
        
        issues = checker._check_heading_levels(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) == 1
        assert issues[0].rule_id == "MD001"
        assert "skips from" in issues[0].message

    @pytest.mark.unit
    def test_check_heading_levels_too_deep(self, tmp_path):
        """Test heading level checking with too deep headings."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Main Title
        
####### Too deep heading
"""
        
        lines = content.splitlines()
        config = {"max_heading_level": 6}
        
        issues = checker._check_heading_levels(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) == 1
        assert issues[0].rule_id == "MD002"
        assert "too deep" in issues[0].message

    @pytest.mark.unit
    def test_check_line_length_valid(self, tmp_path):
        """Test line length checking with valid lines."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Short title

This is a normal line that is well within the length limit.

Another normal line.
"""
        
        lines = content.splitlines()
        config = {"line_length": 120}
        
        issues = checker._check_line_length(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) == 0

    @pytest.mark.unit
    def test_check_line_length_too_long(self, tmp_path):
        """Test line length checking with too long lines."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = f"""# Title

{'This is a very long line that exceeds the maximum length limit and should trigger a warning from the line length checker.' * 2}

Normal line.
"""
        
        lines = content.splitlines()
        config = {"line_length": 80}
        
        issues = checker._check_line_length(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) > 0
        assert all(issue.rule_id == "MD013" for issue in issues)

    @pytest.mark.unit
    def test_check_line_length_skip_urls(self, tmp_path):
        """Test that lines with URLs are skipped from length checking."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Title

Check out this long URL: https://example.com/very/long/path/that/would/normally/exceed/the/line/length/limit/but/should/be/ignored

Normal line.
"""
        
        lines = content.splitlines()
        config = {"line_length": 50}
        
        issues = checker._check_line_length(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) == 0  # URL line should be skipped

    @pytest.mark.unit
    def test_check_trailing_whitespace(self, tmp_path):
        """Test trailing whitespace detection."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Title

Normal line
Line with trailing spaces   
Line with tab	
Another normal line
"""
        
        lines = content.splitlines()
        config = {}
        
        issues = checker._check_trailing_whitespace(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) == 2  # Two lines with trailing whitespace
        assert all(issue.rule_id == "MD009" for issue in issues)

    @pytest.mark.unit
    def test_check_empty_lines(self, tmp_path):
        """Test excessive empty lines detection."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Title

Normal paragraph.



Too many empty lines above.
"""
        
        lines = content.splitlines()
        config = {"max_consecutive_empty_lines": 2}
        
        issues = checker._check_empty_lines(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) > 0
        assert all(issue.rule_id == "MD012" for issue in issues)

    @pytest.mark.unit
    def test_check_link_formatting_valid(self, tmp_path):
        """Test valid link formatting."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Title

Check out [this link](https://example.com) for more info.

Also see [another page](./other.md).
"""
        
        lines = content.splitlines()
        config = {}
        
        issues = checker._check_link_formatting(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) == 0

    @pytest.mark.unit
    def test_check_link_formatting_empty_text(self, tmp_path):
        """Test empty link text detection."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Title

Check out [](https://example.com) for more info.

Also see [another page]().
"""
        
        lines = content.splitlines()
        config = {}
        
        issues = checker._check_link_formatting(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) == 2
        assert all(issue.rule_id == "MD042" for issue in issues)

    @pytest.mark.unit
    def test_check_code_block_language_valid(self, tmp_path):
        """Test code block language specification - valid case."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Title

```python
def hello():
    print("Hello")
```

```bash
echo "Hello"
```
"""
        
        lines = content.splitlines()
        config = {"require_code_language": True}
        
        issues = checker._check_code_block_language(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) == 0

    @pytest.mark.unit
    def test_check_code_block_language_missing(self, tmp_path):
        """Test code block language specification - missing language."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Title

```
def hello():
    print("Hello")
```
"""
        
        lines = content.splitlines()
        config = {"require_code_language": True}
        
        issues = checker._check_code_block_language(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) == 1
        assert issues[0].rule_id == "MD040"

    @pytest.mark.unit
    def test_check_code_block_language_disabled(self, tmp_path):
        """Test code block language checking when disabled."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Title

```
def hello():
    print("Hello")
```
"""
        
        lines = content.splitlines()
        config = {"require_code_language": False}
        
        issues = checker._check_code_block_language(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) == 0

    @pytest.mark.unit
    def test_check_table_formatting_valid(self, tmp_path):
        """Test valid table formatting."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Title

| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |
| Value 3  | Value 4  |
"""
        
        lines = content.splitlines()
        config = {}
        
        issues = checker._check_table_formatting(
            tmp_path / "test.md", content, lines, config
        )
        
        # Should have minimal or no issues for properly formatted table
        assert isinstance(issues, list)

    @pytest.mark.unit
    def test_check_table_formatting_bad_spacing(self, tmp_path):
        """Test table formatting with bad spacing."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Title

|Column 1|Column 2|
|--------|--------|
|Value 1|Value 2|
"""
        
        lines = content.splitlines()
        config = {}
        
        issues = checker._check_table_formatting(
            tmp_path / "test.md", content, lines, config
        )
        
        # Should detect spacing issues
        assert len(issues) > 0

    @pytest.mark.unit
    def test_check_front_matter_valid(self, tmp_path):
        """Test valid YAML front matter."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """---
title: Test Document
author: Test Author
---

# Content starts here
"""
        
        lines = content.splitlines()
        config = {}
        
        issues = checker._check_front_matter(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) == 0

    @pytest.mark.unit
    def test_check_front_matter_unclosed(self, tmp_path):
        """Test unclosed YAML front matter."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """---
title: Test Document
author: Test Author

# Content starts here (front matter not closed)
"""
        
        lines = content.splitlines()
        config = {}
        
        issues = checker._check_front_matter(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) == 1
        assert issues[0].rule_id == "MD058"

    @pytest.mark.unit
    def test_check_front_matter_no_front_matter(self, tmp_path):
        """Test content without front matter."""
        checker = MarkdownQualityChecker(tmp_path)
        
        content = """# Regular content

No front matter here.
"""
        
        lines = content.splitlines()
        config = {}
        
        issues = checker._check_front_matter(
            tmp_path / "test.md", content, lines, config
        )
        
        assert len(issues) == 0  # No front matter is fine

    @pytest.mark.unit
    def test_check_file_quality_comprehensive(self, temp_docs_root):
        """Test comprehensive file quality checking."""
        checker = MarkdownQualityChecker(temp_docs_root)
        
        # Test with existing file from fixture
        index_file = temp_docs_root / "docs" / "index.md"
        issues = checker.check_file_quality(index_file)
        
        assert isinstance(issues, list)
        # Should find some issues in the test content
        # (exact number depends on the test content)

    @pytest.mark.unit
    def test_check_file_quality_nonexistent(self, temp_docs_root):
        """Test quality checking with non-existent file."""
        checker = MarkdownQualityChecker(temp_docs_root)
        
        nonexistent = temp_docs_root / "nonexistent.md"
        issues = checker.check_file_quality(nonexistent)
        
        assert len(issues) == 0

    @pytest.mark.unit
    def test_check_all_files(self, temp_docs_root):
        """Test checking all markdown files."""
        checker = MarkdownQualityChecker(temp_docs_root)
        
        with patch.object(checker, 'run_markdownlint', return_value=[]):
            results = checker.check_all_files()
            
            assert isinstance(results, dict)
            assert len(results) > 0  # Should find markdown files
            
            # Check that file paths are keys
            for file_path in results.keys():
                assert isinstance(file_path, str)
                assert file_path.endswith('.md')

    @pytest.mark.unit
    def test_generate_quality_report(self, temp_docs_root):
        """Test quality report generation."""
        checker = MarkdownQualityChecker(temp_docs_root)
        
        # Create sample results
        sample_issues = [
            QualityIssue("file1.md", 1, 1, "MD013", "Line length", "error", "Too long"),
            QualityIssue("file2.md", 5, 1, "MD009", "Trailing space", "warning", "Trailing whitespace"),
        ]
        
        results = {
            "file1.md": [sample_issues[0]],
            "file2.md": [sample_issues[1]]
        }
        
        report = checker.generate_quality_report(results)
        
        assert report['total_files'] == 2
        assert report['files_with_issues'] == 2
        assert report['total_issues'] == 2
        assert 'quality_score' in report
        assert 'severity_breakdown' in report
        assert 'top_rule_violations' in report

    @pytest.mark.unit
    def test_quality_score_calculation(self, temp_docs_root):
        """Test quality score calculation logic."""
        checker = MarkdownQualityChecker(temp_docs_root)
        
        # Test with no issues
        results = {"file1.md": [], "file2.md": []}
        report = checker.generate_quality_report(results)
        assert report['quality_score'] == 100.0
        
        # Test with many issues
        issues = [QualityIssue("file1.md", i, 1, "MD013", "Test", "error", "Test") for i in range(20)]
        results = {"file1.md": issues}
        report = checker.generate_quality_report(results)
        assert report['quality_score'] < 100.0

    @pytest.mark.unit
    def test_error_handling_file_read(self, tmp_path):
        """Test error handling when file cannot be read."""
        checker = MarkdownQualityChecker(tmp_path)
        
        # Create a file and then make it unreadable (simulation)
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test")
        
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            issues = checker.check_file_quality(test_file)
            
            # Should handle error gracefully
            assert isinstance(issues, list)