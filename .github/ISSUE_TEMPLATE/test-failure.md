---
name: Test Failure Report
about: Report a failing test in the documentation testing infrastructure
title: "[TEST] Test failure in [component]"
labels: ["bug", "test", "priority-high"]
assignees: []
---

## Test Failure Details

**Test Suite:** (unit/integration/quality/etc.)
**Test File:** 
**Test Function:** 
**Component:** (build/link/quality/image/navigation)

## Failure Description

<!-- Provide a clear description of what test is failing -->

## Error Output

```
<!-- Paste the full error output/traceback here -->
```

## Environment

- **Python Version:** 
- **Operating System:** 
- **Dependencies:** (output of `pip freeze` if relevant)
- **Node.js Version:** (if using markdownlint)

## Reproduction Steps

1. 
2. 
3. 

## Expected Behavior

<!-- Describe what should happen when the test passes -->

## Actual Behavior  

<!-- Describe what is actually happening -->

## Additional Context

<!-- Add any other context about the problem -->

## Possible Solution

<!-- If you have ideas on how to fix this, include them here -->

## Impact

- [ ] Blocks development
- [ ] Breaks CI/CD pipeline
- [ ] Affects documentation quality
- [ ] Performance regression
- [ ] Other: _______________

## Checklist

- [ ] I have checked that this is not a duplicate issue
- [ ] I have provided all requested information
- [ ] I have tested with the latest version
- [ ] I have checked the troubleshooting guide