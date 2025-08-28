#!/usr/bin/env python
"""
Script to fix common markdown linting issues in documentation files.
This script:
1. Ensures proper blank lines around headings
2. Ensures proper blank lines around code blocks
3. Ensures proper blank lines around lists
4. Updates relative links to README.md to absolute path
"""

import os
import re
import sys
import subprocess
from pathlib import Path

# Files that need to be fixed
FILES_TO_FIX = [
    "docs/best-practices/data-governance.md",
    "docs/best-practices/performance-optimization.md",
    "docs/architecture/delta-lakehouse-overview.md", 
    "docs/reference/security.md",
    "docs/reference/security-checklist.md"
]

def fix_relative_links(content):
    """Fix relative links to README.md to use absolute paths."""
    # Replace [Home](/README.md) with [Home](/)
    content = re.sub(r'\[Home\]\(/README\.md\)', '[Home](/)', content)
    # Also fix other relative links to README.md if they exist
    content = re.sub(r'\[([^\]]+)\]\(\.\.\/\.\.\/README\.md\)', r'[\1](/)', content)
    return content

def fix_blank_lines_around_headings(content):
    """Ensure headings have blank lines before and after them."""
    # Add blank line before headings if not present
    content = re.sub(r'([^\n])\n(#+\s+)', r'\1\n\n\2', content)
    # Add blank line after headings if not present
    content = re.sub(r'(#+\s+[^\n]+)\n([^#\s][^\n]*)', r'\1\n\n\2', content)
    return content

def fix_blank_lines_around_code_blocks(content):
    """Ensure code blocks have blank lines before and after them."""
    # Add blank line before code blocks if not present
    content = re.sub(r'([^\n])\n```', r'\1\n\n```', content)
    # Add blank line after code blocks if not present
    content = re.sub(r'```\n([^`\s][^\n]*)', r'```\n\n\1', content)
    return content

def fix_blank_lines_around_lists(content):
    """Ensure lists have blank lines before and after them."""
    # Add blank line before lists if not present
    content = re.sub(r'([^\n])\n([-\*]\s+)', r'\1\n\n\2', content)
    # Add blank line after lists if not present (trickier)
    list_end_pattern = re.compile(r'(^[-\*]\s+[^\n]+\n)(?![-\*]\s+)([^-\*\s][^\n]*)', re.MULTILINE)
    content = list_end_pattern.sub(r'\1\n\2', content)
    return content

def fix_duplicate_headings(content):
    """Remove duplicate headings at the beginning of the file."""
    lines = content.split('\n')
    # Check for duplicate title
    title_lines = []
    for i, line in enumerate(lines):
        if re.match(r'^# ', line):
            title_lines.append(i)
    
    # If there are multiple title lines (# headings) close to each other, keep only the first one
    if len(title_lines) > 1 and title_lines[1] - title_lines[0] < 10:
        # Keep the first title and remove the second
        del lines[title_lines[1]]
    
    return '\n'.join(lines)

def fix_markdown_file(file_path):
    """Apply all fixes to a markdown file."""
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist.")
        return False
    
    print(f"Fixing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply all fixes
    content = fix_duplicate_headings(content)
    content = fix_relative_links(content)
    content = fix_blank_lines_around_headings(content)
    content = fix_blank_lines_around_code_blocks(content)
    content = fix_blank_lines_around_lists(content)
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Finally use mdformat to apply consistent formatting
    try:
        subprocess.run(['mdformat', str(file_path)], check=True)
        print(f"Successfully fixed {file_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running mdformat on {file_path}: {e}")
        return False

def main():
    """Fix all markdown files in the list."""
    repo_root = Path(__file__).parent.parent.parent
    success_count = 0
    
    for relative_path in FILES_TO_FIX:
        file_path = repo_root / relative_path
        if fix_markdown_file(file_path):
            success_count += 1
    
    print(f"Fixed {success_count}/{len(FILES_TO_FIX)} files.")
    return 0 if success_count == len(FILES_TO_FIX) else 1

if __name__ == '__main__':
    sys.exit(main())
