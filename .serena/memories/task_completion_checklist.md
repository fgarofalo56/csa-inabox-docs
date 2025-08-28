# Task Completion Checklist

When completing any documentation task, ensure:

## 1. Markdown Quality
- [ ] Run markdown linter: `npx markdownlint '**/*.md' -c .markdownlint.json --fix`
- [ ] Fix any remaining lint warnings manually
- [ ] Verify proper formatting (bold with underscores, lists with dashes)

## 2. Link Validation
- [ ] Run link checker: `python project_tracking/tools/link_checker.py`
- [ ] Fix any broken internal links
- [ ] Verify external links are accessible

## 3. Documentation Standards
- [ ] Follow MARKDOWN_STYLE_GUIDE.md guidelines
- [ ] Ensure proper directory structure per DIRECTORY_STRUCTURE_GUIDE.md
- [ ] Add README.md to any new directories
- [ ] Include breadcrumb navigation
- [ ] Add "related topics" sections

## 4. Visual Elements
- [ ] Convert Mermaid diagrams to PNG for GitHub compatibility
- [ ] Add alt text to all images
- [ ] Ensure images are in correct directory (`docs/images/`)

## 5. Testing
- [ ] Test documentation locally: `mkdocs serve`
- [ ] Verify navigation works correctly
- [ ] Check rendering of all visual elements

## 6. Git Operations
- [ ] Stage changes: `git add .`
- [ ] Commit with descriptive message
- [ ] Update TASK.md with completed items
- [ ] Update CHANGELOG.md if significant changes

## 7. Final Verification
- [ ] Build documentation: `mkdocs build`
- [ ] Check for build errors
- [ ] Verify all pages accessible via navigation
- [ ] Test in GitHub preview (if pushed to branch)