#!/usr/bin/env python
# Updated Link Checker for Azure Synapse Analytics Documentation
# Checks for broken links in markdown files

import os
import re
import logging
import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class LinkChecker:
    def __init__(self, root_dir, exclusions=None):
        self.root_dir = root_dir
        self.broken_links = []
        self.all_links = []
        self.md_files = []
        self.exclusions = exclusions or []
    
    def find_md_files(self):
        for root, dirs, files in os.walk(self.root_dir):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.exclusions and not d.startswith('.')]
            
            for file in files:
                if file.endswith('.md'):
                    self.md_files.append(os.path.join(root, file))
        
        logging.info(f"Found {len(self.md_files)} Markdown files for analysis")
        return self.md_files
    
    def extract_links(self, content):
        """Extract both markdown links and HTML links"""
        # Extract markdown links [text](url)
        md_links = re.findall(r'\[.*?\]\((.*?)\)', content)
        
        # Extract HTML links <a href="url">
        html_links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', content)
        
        # Extract image links ![alt](url)
        img_links = re.findall(r'!\[.*?\]\((.*?)\)', content)
        
        return md_links + html_links + img_links
    
    def is_broken_link(self, link, file_path):
        """Check if a link is broken"""
        # Skip anchor links within the same page
        if link.startswith('#'):
            return False
            
        # Skip external links for this checker
        if link.startswith('http://') or link.startswith('https://'):
            return False
        
        # Skip mailto links
        if link.startswith('mailto:'):
            return False
            
        # Handle relative links
        if not link.startswith('/'):
            # Get directory of the current markdown file
            base_dir = os.path.dirname(file_path)
            # Resolve the relative link
            target_path = os.path.normpath(os.path.join(base_dir, link))
        else:
            # Handle root-relative links
            target_path = os.path.normpath(os.path.join(self.root_dir, link.lstrip('/')))
        
        # Remove anchor part if present
        target_path = target_path.split('#')[0]
        
        # Handle links to directories (assuming README.md)
        if os.path.isdir(target_path):
            return not (os.path.exists(os.path.join(target_path, 'README.md')))
        
        # Check if the file exists
        exists = os.path.exists(target_path)
        
        if not exists and not target_path.endswith('.md'):
            # Try adding .md extension for doc links that omit the extension
            exists = os.path.exists(f"{target_path}.md")
        
        return not exists
    
    def check_links(self):
        """Check all links in markdown files"""
        for file_path in self.md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                relative_path = os.path.relpath(file_path, self.root_dir)
                links = self.extract_links(content)
                
                for link in links:
                    self.all_links.append((relative_path, link))
                    
                    if self.is_broken_link(link, file_path):
                        self.broken_links.append((relative_path, link))
                        logging.warning(f"Broken link in {relative_path}: {link}")
            except Exception as e:
                logging.error(f"Error processing {file_path}: {e}")
        
        logging.info(f"Checked {len(self.all_links)} links, found {len(self.broken_links)} broken links")
        return self.broken_links
    
    def generate_report(self):
        """Generate a markdown report of broken links"""
        if not self.broken_links:
            self.check_links()
        
        report_path = os.path.join(self.root_dir, "project-planning", "updated_link_check_report.md")
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Broken Link Report\n\n")
            f.write(f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if not self.broken_links:
                f.write("✅ No broken links found! All links are valid.\n")
            else:
                f.write(f"Found {len(self.broken_links)} broken links:\n\n")
                f.write("| File | Broken Link |\n")
                f.write("|------|------------|\n")
                
                for file_path, link in self.broken_links:
                    f.write(f"| {file_path} | {link} |\n")
            
            f.write("\n## Summary\n\n")
            f.write(f"- Total markdown files checked: {len(self.md_files)}\n")
            f.write(f"- Total links checked: {len(self.all_links)}\n")
            f.write(f"- Total broken links: {len(self.broken_links)}\n")
        
        logging.info(f"Report generated at {report_path}")
        return report_path

if __name__ == "__main__":
    # Set up the link checker with the project root directory
    project_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    # Directories to exclude from check
    exclusions = ['.git', '.github', '__pycache__', 'site', 'venv', 'env']
    
    checker = LinkChecker(project_root, exclusions)
    checker.find_md_files()
    broken_links = checker.check_links()
    report_path = checker.generate_report()
    
    if broken_links:
        print(f"❌ Found {len(broken_links)} broken links. See {report_path} for details.")
        exit(1)
    else:
        print(f"✅ No broken links found! Report saved to {report_path}")
        exit(0)
