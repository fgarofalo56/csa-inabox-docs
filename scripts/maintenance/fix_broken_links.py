#!/usr/bin/env python3
"""
Fix broken relative links in markdown files.
Identifies and corrects broken '../' relative paths.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Dict

# Root directory of the project
ROOT_DIR = Path(__file__).parent.parent.parent
DOCS_DIR = ROOT_DIR / "docs"


def find_markdown_files(directory: Path) -> List[Path]:
    """Find all markdown files in the directory."""
    return list(directory.rglob("*.md"))


def extract_relative_links(content: str) -> List[Tuple[str, str]]:
    """Extract all relative links from markdown content.

    Returns list of (full_match, link_path) tuples.
    """
    # Pattern to match markdown links with relative paths
    pattern = r'\[([^\]]+)\]\((\.\./[^)]+)\)'
    matches = re.findall(pattern, content)
    return [(match[1], match[1]) for match in matches]


def check_link_exists(file_path: Path, link: str) -> bool:
    """Check if a relative link target exists."""
    # Resolve the link relative to the file's directory
    file_dir = file_path.parent
    target_path = (file_dir / link).resolve()

    return target_path.exists()


def find_correct_path(file_path: Path, broken_link: str) -> str:
    """Try to find the correct path for a broken link."""
    # Extract the target filename
    target = Path(broken_link).name
    file_dir = file_path.parent

    # Common patterns to try
    # 1. Check if it's pointing to root README
    if target == "README.md" and "../" in broken_link:
        # Count the number of ../ to determine depth
        depth = broken_link.count("../")

        # Calculate actual depth from docs root
        try:
            rel_to_docs = file_path.relative_to(DOCS_DIR)
            actual_depth = len(rel_to_docs.parts) - 1  # -1 because we don't count the file itself

            # Check if trying to go to project root
            if depth == actual_depth + 1:
                return "../" * (actual_depth + 1) + "README.md"
            # Check if trying to go to docs root
            elif depth == actual_depth:
                return "../" * actual_depth + "README.md"
        except ValueError:
            pass

    # 2. Try to find the file in common locations
    if target != "README.md":
        # Extract directory from broken link
        link_parts = Path(broken_link).parts
        if len(link_parts) > 1:
            target_dir = link_parts[-2]

            # Search for the target file
            for root, dirs, files in os.walk(DOCS_DIR):
                if target in files and target_dir in Path(root).parts:
                    found_path = Path(root) / target
                    try:
                        # Calculate relative path from current file to found file
                        rel_path = os.path.relpath(found_path, file_dir)
                        # Convert to forward slashes for consistency
                        rel_path = rel_path.replace("\\", "/")
                        return rel_path
                    except ValueError:
                        pass

    return None


def analyze_file(file_path: Path) -> Dict:
    """Analyze a single markdown file for broken links."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    links = extract_relative_links(content)
    broken_links = []

    for full_match, link in links:
        if not check_link_exists(file_path, link):
            correct_path = find_correct_path(file_path, link)
            broken_links.append({
                'original': link,
                'suggested': correct_path,
                'full_match': full_match
            })

    return {
        'file': file_path,
        'broken_links': broken_links,
        'content': content
    }


def generate_report(results: List[Dict]) -> str:
    """Generate a report of broken links."""
    report_lines = []
    report_lines.append("# Broken Link Analysis Report\n")
    report_lines.append(f"Total files analyzed: {len(results)}\n")

    files_with_issues = [r for r in results if r['broken_links']]
    report_lines.append(f"Files with broken links: {len(files_with_issues)}\n\n")

    for result in files_with_issues:
        rel_path = result['file'].relative_to(ROOT_DIR)
        report_lines.append(f"\n## {rel_path}\n")

        for broken in result['broken_links']:
            report_lines.append(f"- **Broken**: `{broken['original']}`")
            if broken['suggested']:
                report_lines.append(f"  → **Suggested**: `{broken['suggested']}`\n")
            else:
                report_lines.append(f"  → **Status**: Target not found\n")

    return "\n".join(report_lines)


def main():
    """Main execution function."""
    print("Analyzing markdown files for broken relative links...")
    print(f"Root directory: {ROOT_DIR}")
    print(f"Docs directory: {DOCS_DIR}\n")

    # Find all markdown files
    md_files = find_markdown_files(DOCS_DIR)
    print(f"Found {len(md_files)} markdown files\n")

    # Analyze each file
    results = []
    for md_file in md_files:
        result = analyze_file(md_file)
        results.append(result)

        if result['broken_links']:
            rel_path = md_file.relative_to(ROOT_DIR)
            print(f"[X] {rel_path}: {len(result['broken_links'])} broken links")

    # Generate report
    report = generate_report(results)
    report_path = ROOT_DIR / "broken_links_report.md"

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n\nReport saved to: {report_path}")

    # Summary
    total_broken = sum(len(r['broken_links']) for r in results)
    print(f"\nTotal broken links found: {total_broken}")


if __name__ == "__main__":
    main()
