"""Markdown quality checking utilities."""

import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class QualityIssue:
    """Represents a markdown quality issue."""
    file_path: str
    line_number: int
    column: Optional[int]
    rule_id: str
    rule_description: str
    severity: str
    message: str


class MarkdownQualityChecker:
    """Check markdown files for quality and style issues."""
    
    def __init__(self, docs_root: Path, config_file: Optional[Path] = None):
        """Initialize markdown quality checker.
        
        Args:
            docs_root: Path to documentation root
            config_file: Path to markdownlint configuration file
        """
        self.docs_root = Path(docs_root)
        self.config_file = config_file or self.docs_root / ".markdownlint.json"
        
        # Built-in quality rules
        self.quality_rules = {
            'heading_levels': self._check_heading_levels,
            'line_length': self._check_line_length,
            'trailing_whitespace': self._check_trailing_whitespace,
            'empty_lines': self._check_empty_lines,
            'link_formatting': self._check_link_formatting,
            'code_block_language': self._check_code_block_language,
            'table_formatting': self._check_table_formatting,
            'front_matter': self._check_front_matter,
        }
        
        # Default configuration
        self.default_config = {
            'line_length': 120,
            'max_heading_level': 6,
            'require_code_language': True,
            'allowed_html_tags': ['br', 'kbd', 'sub', 'sup'],
            'max_consecutive_empty_lines': 2
        }
    
    def load_config(self) -> Dict:
        """Load markdownlint configuration.
        
        Returns:
            Configuration dictionary
        """
        config = self.default_config.copy()
        
        if self.config_file and self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    config.update(file_config)
            except Exception as e:
                logger.warning(f"Could not load config from {self.config_file}: {e}")
                
        return config
    
    def run_markdownlint(self, file_path: Optional[Path] = None) -> List[QualityIssue]:
        """Run markdownlint CLI tool if available.
        
        Args:
            file_path: Specific file to check, or None for all files
            
        Returns:
            List of QualityIssue objects
        """
        issues = []
        
        try:
            cmd = ["markdownlint", "--json"]
            
            if self.config_file and self.config_file.exists():
                cmd.extend(["--config", str(self.config_file)])
            
            if file_path:
                cmd.append(str(file_path))
            else:
                cmd.extend([str(self.docs_root / "**/*.md")])
                cmd.append("--glob")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.docs_root
            )
            
            if result.stdout:
                lint_results = json.loads(result.stdout)
                
                for file_result in lint_results:
                    file_path_str = file_result.get('fileName', '')
                    for error in file_result.get('errors', []):
                        issues.append(QualityIssue(
                            file_path=file_path_str,
                            line_number=error.get('lineNumber', 0),
                            column=error.get('columnNumber'),
                            rule_id=error.get('ruleNames', [''])[0],
                            rule_description=error.get('ruleDescription', ''),
                            severity='error',
                            message=error.get('errorDetail', '')
                        ))
                        
        except FileNotFoundError:
            logger.info("markdownlint CLI not found, using built-in checks only")
        except Exception as e:
            logger.error(f"Error running markdownlint: {e}")
            
        return issues
    
    def check_file_quality(self, file_path: Path) -> List[QualityIssue]:
        """Check quality of a single markdown file.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            List of QualityIssue objects
        """
        issues = []
        
        if not file_path.exists():
            return issues
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
            
            config = self.load_config()
            
            # Run built-in quality checks
            for rule_name, rule_func in self.quality_rules.items():
                rule_issues = rule_func(file_path, content, lines, config)
                issues.extend(rule_issues)
                
        except Exception as e:
            logger.error(f"Error checking file quality for {file_path}: {e}")
            
        return issues
    
    def _check_heading_levels(self, file_path: Path, content: str, lines: List[str], config: Dict) -> List[QualityIssue]:
        """Check heading level consistency."""
        issues = []
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')
        previous_level = 0
        
        for line_num, line in enumerate(lines, 1):
            match = heading_pattern.match(line)
            if match:
                level = len(match.group(1))
                
                # Check if level jumps more than 1
                if level > previous_level + 1 and previous_level > 0:
                    issues.append(QualityIssue(
                        file_path=str(file_path),
                        line_number=line_num,
                        column=1,
                        rule_id='MD001',
                        rule_description='Heading levels should increment by one level at a time',
                        severity='warning',
                        message=f'Heading level {level} skips from {previous_level}'
                    ))
                
                # Check maximum heading level
                if level > config.get('max_heading_level', 6):
                    issues.append(QualityIssue(
                        file_path=str(file_path),
                        line_number=line_num,
                        column=1,
                        rule_id='MD002',
                        rule_description=f'Heading level exceeds maximum of {config.get("max_heading_level", 6)}',
                        severity='error',
                        message=f'Heading level {level} is too deep'
                    ))
                
                previous_level = level
                
        return issues
    
    def _check_line_length(self, file_path: Path, content: str, lines: List[str], config: Dict) -> List[QualityIssue]:
        """Check line length limits."""
        issues = []
        max_length = config.get('line_length', 120)
        
        for line_num, line in enumerate(lines, 1):
            # Skip lines that are mostly URLs or code
            if re.search(r'https?://\S+', line) or line.strip().startswith('```'):
                continue
                
            if len(line) > max_length:
                issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=line_num,
                    column=max_length + 1,
                    rule_id='MD013',
                    rule_description=f'Line length should not exceed {max_length} characters',
                    severity='warning',
                    message=f'Line length {len(line)} exceeds {max_length}'
                ))
                
        return issues
    
    def _check_trailing_whitespace(self, file_path: Path, content: str, lines: List[str], config: Dict) -> List[QualityIssue]:
        """Check for trailing whitespace."""
        issues = []
        
        for line_num, line in enumerate(lines, 1):
            if line.endswith(' ') or line.endswith('\t'):
                issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=line_num,
                    column=len(line.rstrip()) + 1,
                    rule_id='MD009',
                    rule_description='No trailing whitespace',
                    severity='error',
                    message='Line ends with whitespace'
                ))
                
        return issues
    
    def _check_empty_lines(self, file_path: Path, content: str, lines: List[str], config: Dict) -> List[QualityIssue]:
        """Check for excessive empty lines."""
        issues = []
        max_consecutive = config.get('max_consecutive_empty_lines', 2)
        consecutive_empty = 0
        
        for line_num, line in enumerate(lines, 1):
            if line.strip() == '':
                consecutive_empty += 1
                if consecutive_empty > max_consecutive:
                    issues.append(QualityIssue(
                        file_path=str(file_path),
                        line_number=line_num,
                        column=1,
                        rule_id='MD012',
                        rule_description=f'No more than {max_consecutive} consecutive empty lines',
                        severity='warning',
                        message=f'Too many consecutive empty lines: {consecutive_empty}'
                    ))
            else:
                consecutive_empty = 0
                
        return issues
    
    def _check_link_formatting(self, file_path: Path, content: str, lines: List[str], config: Dict) -> List[QualityIssue]:
        """Check link formatting issues."""
        issues = []
        
        # Check for malformed links
        malformed_link_pattern = re.compile(r'\[([^\]]*)\]\s*\(([^)]*)\)')
        
        for line_num, line in enumerate(lines, 1):
            matches = malformed_link_pattern.finditer(line)
            for match in matches:
                link_text = match.group(1)
                link_url = match.group(2)
                
                # Check for empty link text
                if not link_text.strip():
                    issues.append(QualityIssue(
                        file_path=str(file_path),
                        line_number=line_num,
                        column=match.start() + 1,
                        rule_id='MD042',
                        rule_description='No empty links',
                        severity='error',
                        message='Link has empty text'
                    ))
                
                # Check for missing URL
                if not link_url.strip():
                    issues.append(QualityIssue(
                        file_path=str(file_path),
                        line_number=line_num,
                        column=match.start() + 1,
                        rule_id='MD042',
                        rule_description='No empty links',
                        severity='error',
                        message='Link has empty URL'
                    ))
                    
        return issues
    
    def _check_code_block_language(self, file_path: Path, content: str, lines: List[str], config: Dict) -> List[QualityIssue]:
        """Check code block language specification."""
        issues = []
        
        if not config.get('require_code_language', True):
            return issues
        
        in_code_block = False
        code_block_start_pattern = re.compile(r'^```(\w*).*$')
        
        for line_num, line in enumerate(lines, 1):
            match = code_block_start_pattern.match(line.strip())
            if match and not in_code_block:
                in_code_block = True
                language = match.group(1)
                
                if not language:
                    issues.append(QualityIssue(
                        file_path=str(file_path),
                        line_number=line_num,
                        column=4,
                        rule_id='MD040',
                        rule_description='Fenced code blocks should have a language specified',
                        severity='warning',
                        message='Code block missing language specification'
                    ))
                    
            elif line.strip().startswith('```') and in_code_block:
                in_code_block = False
                
        return issues
    
    def _check_table_formatting(self, file_path: Path, content: str, lines: List[str], config: Dict) -> List[QualityIssue]:
        """Check table formatting."""
        issues = []
        table_row_pattern = re.compile(r'^\s*\|.*\|\s*$')
        
        for line_num, line in enumerate(lines, 1):
            if table_row_pattern.match(line):
                # Check if table row is properly formatted
                cells = line.split('|')[1:-1]  # Remove empty first and last elements
                
                # Check for consistent spacing (basic check)
                for cell in cells:
                    if cell and not (cell.startswith(' ') and cell.endswith(' ')):
                        issues.append(QualityIssue(
                            file_path=str(file_path),
                            line_number=line_num,
                            column=1,
                            rule_id='MD055',
                            rule_description='Table rows should have consistent formatting',
                            severity='style',
                            message='Table cell should have spaces around content'
                        ))
                        break
                        
        return issues
    
    def _check_front_matter(self, file_path: Path, content: str, lines: List[str], config: Dict) -> List[QualityIssue]:
        """Check YAML front matter formatting."""
        issues = []
        
        if not content.startswith('---'):
            return issues
        
        # Find end of front matter
        front_matter_end = -1
        for i, line in enumerate(lines[1:], 2):
            if line.strip() == '---':
                front_matter_end = i
                break
                
        if front_matter_end == -1:
            issues.append(QualityIssue(
                file_path=str(file_path),
                line_number=1,
                column=1,
                rule_id='MD058',
                rule_description='YAML front matter should be properly closed',
                severity='error',
                message='Front matter not properly closed with ---'
            ))
            
        return issues
    
    def check_all_files(self) -> Dict[str, List[QualityIssue]]:
        """Check quality of all markdown files.
        
        Returns:
            Dictionary mapping file paths to lists of issues
        """
        results = {}
        
        # First try markdownlint CLI
        cli_issues = self.run_markdownlint()
        for issue in cli_issues:
            if issue.file_path not in results:
                results[issue.file_path] = []
            results[issue.file_path].append(issue)
        
        # Then run built-in checks
        markdown_files = list(self.docs_root.glob("**/*.md"))
        
        for file_path in markdown_files:
            built_in_issues = self.check_file_quality(file_path)
            file_key = str(file_path)
            
            if file_key not in results:
                results[file_key] = []
            results[file_key].extend(built_in_issues)
        
        return results
    
    def generate_quality_report(self, results: Dict[str, List[QualityIssue]]) -> Dict:
        """Generate quality report summary.
        
        Args:
            results: Dictionary of file paths to issues
            
        Returns:
            Summary report dictionary
        """
        total_files = len(results)
        total_issues = sum(len(issues) for issues in results.values())
        files_with_issues = len([f for f, issues in results.items() if issues])
        
        # Group by severity
        severity_counts = {'error': 0, 'warning': 0, 'style': 0, 'info': 0}
        rule_counts = {}
        
        for issues in results.values():
            for issue in issues:
                severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
                rule_counts[issue.rule_id] = rule_counts.get(issue.rule_id, 0) + 1
        
        quality_score = max(0, 100 - (total_issues / total_files * 10)) if total_files > 0 else 100
        
        return {
            'total_files': total_files,
            'files_with_issues': files_with_issues,
            'total_issues': total_issues,
            'quality_score': round(quality_score, 2),
            'severity_breakdown': severity_counts,
            'top_rule_violations': dict(sorted(rule_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            'files_by_issue_count': [
                {'file': file_path, 'issue_count': len(issues)}
                for file_path, issues in sorted(results.items(), key=lambda x: len(x[1]), reverse=True)
            ][:10]
        }