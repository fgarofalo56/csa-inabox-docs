## 📋 Description

### Summary

<!-- Provide a brief summary of the changes -->

### Motivation and Context

<!-- Why is this change required? What problem does it solve? -->
<!-- If it fixes an open issue, please link to the issue here -->

Closes #(issue)

## 📝 Type of Change

Please select the relevant option(s):

- [ ] **New Documentation** - New documentation added
- [ ] **Documentation Update** - Existing documentation improved or updated
- [ ] **Bug Fix** - Correction of errors or broken links
- [ ] **Code Examples** - New or updated code samples
- [ ] **Architecture/Diagrams** - New or updated architecture documentation
- [ ] **Best Practices** - New or updated best practices
- [ ] **Tooling/Scripts** - Changes to build, test, or validation tools
- [ ] **Configuration** - Changes to project configuration
- [ ] **Other** - Please specify: _______________

## 📝 Changes Made

### Documentation Changes

<!-- List the specific documentation files changed and what was updated -->

- **File 1**: Description of changes
- **File 2**: Description of changes

### New Files Added

<!-- List any new files created -->

- `path/to/file1.md` - Description
- `path/to/file2.md` - Description

### Files Deleted

<!-- List any files removed -->

- `path/to/file.md` - Reason for deletion

## 📸 Screenshots (if applicable)
<!-- Add screenshots to show visual changes -->

## 📚 Documentation Standards Checklist

Please confirm that your changes meet our documentation standards:

### Content Quality

- [ ] Content is accurate and technically correct
- [ ] Information is clear and easy to understand
- [ ] Examples are realistic and working
- [ ] Terminology is consistent with project glossary
- [ ] No sensitive information (API keys, secrets, etc.) included

### Style Guidelines

- [ ] Follows [MARKDOWN_STYLE_GUIDE.md](docs/guides/MARKDOWN_STYLE_GUIDE.md)
- [ ] Uses consistent heading hierarchy (one H1, proper H2-H4 structure)
- [ ] Includes navigation breadcrumbs at top of document
- [ ] Uses appropriate icons and badges consistently
- [ ] Code blocks have language identifiers
- [ ] Lists have proper formatting and spacing

### Structure Guidelines

- [ ] Follows [DIRECTORY_STRUCTURE_GUIDE.md](docs/guides/DIRECTORY_STRUCTURE_GUIDE.md)
- [ ] Files are in appropriate directories
- [ ] README.md files exist in new directories
- [ ] Navigation is updated in `mkdocs.yml` if needed

### Technical Validation

- [ ] All links are valid and working
- [ ] All images have alt text and proper paths
- [ ] Code examples have been tested and work
- [ ] Cross-references to other docs are correct
- [ ] Markdown linting passes without errors

## 🧪 Testing Verification

### Local Testing Completed

- [ ] Documentation builds successfully with `mkdocs build --strict`
- [ ] Documentation renders correctly with `mkdocs serve`
- [ ] All links validated with link checker
- [ ] Markdown linting passed (`markdownlint **/*.md`)
- [ ] Spell check completed
- [ ] Tested on multiple screen sizes (if UI changes)

### Testing Evidence

<!-- Provide screenshots or evidence of testing if applicable -->

```bash
# Example: Include output from build/lint commands
$ mkdocs build --strict
INFO    -  Building documentation...
INFO    -  Documentation built in X.XX seconds

$ markdownlint '**/*.md' -c .markdownlint.json
# No errors
```

## 📊 Impact Assessment

### Areas Affected

<!-- Which parts of the documentation are affected? -->

- [ ] Getting Started / Onboarding
- [ ] Service Documentation
- [ ] Architecture Patterns
- [ ] Best Practices
- [ ] Code Examples
- [ ] Tutorials
- [ ] Reference Documentation
- [ ] Navigation/Structure
- [ ] Build/Deploy Configuration

### Breaking Changes

<!-- Are there any breaking changes? -->

- [ ] **No breaking changes**
- [ ] **Breaking changes** - Please describe:

### Dependencies

<!-- Does this PR depend on other PRs or changes? -->

- [ ] No dependencies
- [ ] Depends on: #(PR number)

## 📋 Additional Notes

### Related Issues/PRs

<!-- List related issues or pull requests -->

- Related to #(issue)
- Builds on #(PR)

### Reviewers

<!-- Tag specific reviewers if needed -->

@reviewer1 @reviewer2

### Questions/Concerns

<!-- Any questions or concerns for reviewers? -->

---

## 👀 Reviewer Checklist

<!-- For reviewers to complete -->

- [ ] Content accuracy verified
- [ ] Documentation standards met
- [ ] Links and images working
- [ ] Code examples tested
- [ ] Navigation updated appropriately
- [ ] No sensitive information exposed
- [ ] Approved for merge

---

**Thank you for contributing to CSA-in-a-Box Documentation!**

Your contributions help make Azure analytics more accessible to everyone.