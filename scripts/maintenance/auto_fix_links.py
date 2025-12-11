#!/usr/bin/env python3
"""
Automatically fix broken relative links in markdown files.
Focus on fixing the most common and critical broken links.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Root directory of the project
ROOT_DIR = Path(__file__).parent.parent.parent
DOCS_DIR = ROOT_DIR / "docs"


def check_link_exists(file_path: Path, link: str) -> bool:
    """Check if a relative link target exists."""
    file_dir = file_path.parent

    # Split anchor from path
    link_path = link.split('#')[0] if '#' in link else link
    if not link_path:  # Just an anchor
        return True

    target_path = (file_dir / link_path).resolve()
    return target_path.exists()


def get_relative_depth(file_path: Path) -> int:
    """Get the depth of a file relative to docs directory."""
    try:
        rel_to_docs = file_path.relative_to(DOCS_DIR)
        return len(rel_to_docs.parts) - 1  # -1 because we don't count the file itself
    except ValueError:
        return 0


def fix_root_readme_links(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix links pointing to ../../README.md from docs folder."""
    depth = get_relative_depth(file_path)

    # Pattern for links to root README
    patterns = [
        (r'\]\((\.\./\.\./README\.md)\)',  # From 2 levels deep
         f"]({'../' * (depth + 1)}README.md)"),
        (r'\]\((\.\./\.\./README\.md#[^)]+)\)',  # With anchor
         lambda m: f"]({'../' * (depth + 1)}README.md{m.group(1).split('README.md')[1]})"),
    ]

    fixes = 0
    for pattern, replacement in patterns:
        if callable(replacement):
            def repl_fn(match):
                nonlocal fixes
                if not check_link_exists(file_path, match.group(1)):
                    fixes += 1
                    return replacement(match)
                return match.group(0)
            content = re.sub(pattern, repl_fn, content)
        else:
            # Check if the link is actually broken before fixing
            for match in re.finditer(pattern, content):
                if not check_link_exists(file_path, match.group(1)):
                    content = content.replace(match.group(0), replacement)
                    fixes += 1
                    break  # Only fix one at a time

    return content, fixes


def fix_common_navigation_links(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix common navigation links to main sections."""
    fixes = 0
    depth = get_relative_depth(file_path)
    base_path = '../' * depth

    # Common broken patterns and their fixes
    fixes_map = {
        # Architecture links
        r'\]\(\.\./architecture/integration/README\.md\)': f']({base_path}architecture/README.md)',
        r'\]\(\.\./\.\./architecture/integration/README\.md\)': f']({base_path}architecture/README.md)',

        # Service catalog links for non-existent services
        r'\]\(\.\./02-services/streaming-services/azure-stream-analytics/README\.md\)': f']({base_path}02-services/streaming-services/README.md)',
        r'\]\(\.\./\.\./02-services/streaming-services/azure-stream-analytics/README\.md\)': f']({base_path}02-services/streaming-services/README.md)',
        r'\]\(\.\./02-services/streaming-services/azure-event-grid/README\.md\)': f']({base_path}02-services/streaming-services/README.md)',
        r'\]\(\.\./02-services/storage-services/azure-cosmos-db/README\.md\)': f']({base_path}02-services/storage-services/README.md)',
        r'\]\(\.\./02-services/storage-services/azure-sql-database/README\.md\)': f']({base_path}02-services/storage-services/README.md)',
        r'\]\(\.\./02-services/orchestration-services/azure-logic-apps/README\.md\)': f']({base_path}02-services/orchestration-services/README.md)',

        # Reference architecture links
        r'\]\(\.\./03-architecture-patterns/reference-architectures/README\.md\)': f']({base_path}03-architecture-patterns/README.md)',
        r'\]\(\.\./\.\./03-architecture-patterns/reference-architectures/README\.md\)': f']({base_path}03-architecture-patterns/README.md)',
    }

    for pattern, replacement in fixes_map.items():
        count = len(re.findall(pattern, content))
        if count > 0:
            content = re.sub(pattern, replacement, content)
            fixes += count

    return content, fixes


def fix_sibling_links(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix links to sibling directories that are one level up."""
    fixes = 0

    # Pattern: ../something/file.md when it should be ../../something/file.md
    pattern = r'\]\((\.\./([^/]+)/([^)]+))\)'

    for match in re.finditer(pattern, content):
        full_link = match.group(1)
        if not check_link_exists(file_path, full_link):
            # Try adding another ../
            corrected_link = '../' + full_link
            if check_link_exists(file_path, corrected_link):
                content = content.replace(f']({full_link})', f']({corrected_link})')
                fixes += 1

    return content, fixes


def remove_anchor_only_broken_links(content: str, file_path: Path) -> Tuple[str, int]:
    """Remove anchor references from links if the anchor doesn't exist."""
    fixes = 0

    # Pattern for links with anchors to root README
    pattern = r'\]\((.*?README\.md#[^)]+)\)'

    for match in re.finditer(pattern, content):
        full_link = match.group(1)
        if not check_link_exists(file_path, full_link):
            # Remove the anchor part
            base_link = full_link.split('#')[0]
            if check_link_exists(file_path, base_link):
                content = content.replace(f']({full_link})', f']({base_link})')
                fixes += 1

    return content, fixes


def process_file(file_path: Path, dry_run: bool = True) -> Dict:
    """Process a single file and fix broken links."""
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    content = original_content
    total_fixes = 0

    # Apply fixes in order
    content, fixes = fix_root_readme_links(content, file_path)
    total_fixes += fixes

    content, fixes = fix_common_navigation_links(content, file_path)
    total_fixes += fixes

    content, fixes = fix_sibling_links(content, file_path)
    total_fixes += fixes

    content, fixes = remove_anchor_only_broken_links(content, file_path)
    total_fixes += fixes

    # Write back if changed and not dry run
    if total_fixes > 0 and not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    return {
        'file': file_path,
        'fixes': total_fixes,
        'changed': content != original_content
    }


def main():
    """Main execution function."""
    import sys

    dry_run = '--apply' not in sys.argv

    print("=" * 80)
    print("CSA Documentation - Broken Link Auto-Fix")
    print("=" * 80)
    print(f"Mode: {'DRY RUN (use --apply to make changes)' if dry_run else 'APPLYING FIXES'}")
    print(f"Root directory: {ROOT_DIR}")
    print(f"Docs directory: {DOCS_DIR}\n")

    # Find all markdown files
    md_files = list(DOCS_DIR.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files\n")

    # Process each file
    results = []
    for md_file in md_files:
        result = process_file(md_file, dry_run=dry_run)
        results.append(result)

        if result['fixes'] > 0:
            rel_path = md_file.relative_to(ROOT_DIR)
            status = "[WOULD FIX]" if dry_run else "[FIXED]"
            print(f"{status} {rel_path}: {result['fixes']} links")

    # Summary
    total_files_fixed = sum(1 for r in results if r['fixes'] > 0)
    total_fixes = sum(r['fixes'] for r in results)

    print("\n" + "=" * 80)
    print(f"Summary:")
    print(f"  Files processed: {len(md_files)}")
    print(f"  Files with fixes: {total_files_fixed}")
    print(f"  Total link fixes: {total_fixes}")

    if dry_run:
        print("\nTo apply these fixes, run: python scripts/maintenance/auto_fix_links.py --apply")
    else:
        print("\nFixes have been applied!")
    print("=" * 80)


if __name__ == "__main__":
    main()
