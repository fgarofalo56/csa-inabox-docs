# Analytics Setup Guide

![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)

This guide explains how to configure and manage analytics for the CSA-in-a-Box documentation site to understand usage patterns and improve user experience.

## Table of Contents

- [Overview](#overview)
- [Google Analytics 4 Configuration](#google-analytics-4-configuration)
- [Cookie Consent Configuration](#cookie-consent-configuration)
- [Privacy Considerations](#privacy-considerations)
- [GDPR Compliance](#gdpr-compliance)
- [Key Metrics to Track](#key-metrics-to-track)
- [Testing Analytics](#testing-analytics)
- [Troubleshooting](#troubleshooting)

## Overview

The CSA-in-a-Box documentation uses Google Analytics 4 (GA4) to collect anonymous usage data that helps us understand how users interact with the documentation and identify areas for improvement.

### Key Features

- Page view tracking
- User feedback collection
- Cookie consent management
- GDPR-compliant data collection
- Privacy-first approach

## Google Analytics 4 Configuration

### Prerequisites

- Google Analytics account
- Admin access to the documentation repository
- GA4 property created for the documentation site

### Step 1: Create GA4 Property

1. Sign in to [Google Analytics](https://analytics.google.com/)
2. Click Admin in the left navigation
3. In the Account column, select or create an account
4. In the Property column, click Create Property
5. Enter property details:
   - Property name: "CSA-in-a-Box Documentation"
   - Reporting time zone: Your timezone
   - Currency: Your currency
6. Click Next and complete the property setup

### Step 2: Get Measurement ID

1. In your GA4 property, navigate to Admin > Data Streams
2. Click on your web data stream or create a new one
3. Copy the Measurement ID (format: G-XXXXXXXXXX)

### Step 3: Configure MkDocs

Update the `mkdocs.yml` file with your Measurement ID:

```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX  # Replace with your actual Measurement ID
```

### Step 4: Deploy Changes

```bash
# Build the documentation
mkdocs build

# Deploy to GitHub Pages or your hosting platform
mkdocs gh-deploy
```

### Verification

1. Visit your documentation site
2. Open Google Analytics Real-Time reports
3. Navigate through documentation pages
4. Verify events appear in Real-Time view

## Cookie Consent Configuration

The documentation implements GDPR-compliant cookie consent using MkDocs Material's built-in consent feature.

### Configuration

The cookie consent banner is configured in `mkdocs.yml`:

```yaml
extra:
  consent:
    title: Cookie consent
    description: >-
      We use cookies to recognize your repeated visits and preferences, as well
      as to measure the effectiveness of our documentation and whether users
      find what they're searching for. With your consent, you're helping us to
      make our documentation better.
    actions:
      - accept    # Accept all cookies
      - manage    # Manage individual cookie preferences
      - reject    # Reject optional cookies
```

### User Experience

- Users see a consent banner on first visit
- Choice is stored in browser localStorage
- Users can change preferences anytime
- Analytics only load after consent

### Customization

To customize the consent message:

1. Edit the `description` field in `mkdocs.yml`
2. Modify available actions (accept/manage/reject)
3. Rebuild and deploy documentation

## Privacy Considerations

### Data Minimization

We collect only essential data:

- Page views and navigation paths
- Session duration and bounce rates
- Geographic region (country/city level)
- Device type and browser
- Search queries within documentation

### Data NOT Collected

- Personal identifiable information (PII)
- IP addresses (anonymized by GA4)
- User-specific tracking across sessions without consent
- Form inputs or sensitive data
- Cross-site tracking

### Data Retention

- Default retention: 14 months
- Can be adjusted in GA4 settings (Admin > Data Settings > Data Retention)
- Recommended: 14 months for documentation analytics

### User Rights

Users can:

- Opt-out via cookie consent banner
- Delete cookies from browser
- Use browser "Do Not Track" settings
- Request data deletion (GDPR right to erasure)

## GDPR Compliance

### Legal Basis

Analytics data collection operates under:

- Legitimate interest (improving documentation)
- Explicit consent (via cookie banner)

### Required Elements

#### Privacy Policy

Ensure your privacy policy includes:

- What data is collected
- Why it's collected
- How long it's retained
- User rights (access, deletion, portability)
- Contact information for privacy requests

#### Cookie Notice

The cookie consent banner must include:

- Clear description of cookie usage
- Ability to accept or reject
- Link to privacy policy
- Granular consent options

#### Data Processing Agreement

For enterprise use:

- Ensure Google Analytics DPA is signed
- Review data processing terms
- Understand data transfer mechanisms

### GDPR Checklist

- [x] Cookie consent banner implemented
- [x] Privacy policy updated
- [x] Data minimization applied
- [x] User opt-out mechanism available
- [x] Data retention policy defined
- [x] Analytics configured for IP anonymization
- [ ] Privacy policy link added to footer
- [ ] Data Processing Agreement signed with Google

## Key Metrics to Track

### Page Performance Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Page Views | Total number of page loads | Trending upward |
| Unique Page Views | Deduplicated page views per session | Monitor growth |
| Average Time on Page | How long users spend reading | > 2 minutes |
| Bounce Rate | Single-page sessions | < 50% |
| Exit Rate | Last page in session | Monitor top exits |

### User Engagement Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Sessions | Total visits to documentation | Monitor trends |
| Users | Unique visitors | Growing user base |
| New vs Returning | User retention indicator | 60/40 split ideal |
| Pages per Session | Average pages viewed | > 3 pages |
| Session Duration | Average session length | > 5 minutes |

### Content Metrics

| Metric | Description | Action |
|--------|-------------|--------|
| Top Pages | Most visited pages | Prioritize updates |
| Top Landing Pages | Entry points | Optimize for clarity |
| Top Exit Pages | Where users leave | Improve content flow |
| Search Queries | Internal searches | Identify content gaps |
| Feedback Ratings | Helpful/not helpful | Address low-rated pages |

### Technical Metrics

| Metric | Description | Action |
|--------|-------------|--------|
| Browser Distribution | Browser usage | Test compatibility |
| Device Categories | Desktop/mobile/tablet | Optimize responsive design |
| Operating Systems | OS distribution | Platform-specific testing |
| Screen Resolutions | Display sizes | Responsive design validation |

## Testing Analytics

### Local Testing

GA4 events won't fire on `localhost` by default. To test:

```bash
# Serve documentation with production settings
mkdocs serve --strict

# Or build and serve from site directory
mkdocs build
cd site
python -m http.server 8000
```

### Debug Mode

Enable GA4 debug mode:

1. Install [Google Analytics Debugger](https://chrome.google.com/webstore/detail/google-analytics-debugger) Chrome extension
2. Enable the extension
3. Open Chrome DevTools Console
4. Navigate documentation pages
5. View GA4 events in console

### Verification Checklist

- [ ] Page views tracked correctly
- [ ] Feedback widget displays on pages
- [ ] Feedback submissions recorded
- [ ] Cookie consent banner appears on first visit
- [ ] Consent choice persists across sessions
- [ ] Analytics disabled when consent rejected
- [ ] Events visible in GA4 Real-Time reports

## Troubleshooting

### Analytics Not Loading

__Problem:__ No data appears in Google Analytics

__Solutions:__

1. Verify Measurement ID is correct in `mkdocs.yml`
2. Check browser console for errors
3. Ensure ad blockers are disabled (for testing)
4. Confirm consent was given via cookie banner
5. Wait 24-48 hours for data to appear (not real-time)

### Cookie Consent Not Appearing

__Problem:__ Consent banner doesn't display

__Solutions:__

1. Clear browser localStorage and cookies
2. Verify `consent` configuration in `mkdocs.yml`
3. Check for conflicting CSS or JavaScript
4. Test in incognito/private browsing mode

### Feedback Widget Not Visible

__Problem:__ "Was this page helpful?" not showing

__Solutions:__

1. Verify `feedback` configuration in `mkdocs.yml`
2. Ensure Material theme version supports feedback (>= 9.0)
3. Check if feedback is hidden in theme customization
4. Review browser console for JavaScript errors

### High Bounce Rate

__Problem:__ Many single-page sessions

__Solutions:__

1. Improve page content and readability
2. Add clear navigation and next steps
3. Review top bounce pages for issues
4. Ensure fast page load times
5. Add related content links

### Low Feedback Response Rate

__Problem:__ Few users providing feedback

__Solutions:__

1. Make feedback widget more prominent
2. Reduce friction in feedback process
3. Add incentive messaging
4. Test different widget placements
5. A/B test feedback prompts

## Best Practices

### Regular Reviews

- Review analytics weekly
- Generate monthly reports
- Quarterly deep-dive analysis
- Annual comprehensive review

### Data-Driven Improvements

1. Identify low-performing content
2. Analyze user navigation patterns
3. Address common search queries
4. Update based on feedback
5. Test improvements and measure impact

### Privacy-First Approach

- Always respect user privacy
- Minimize data collection
- Be transparent about data use
- Honor opt-out requests
- Regularly audit data practices

### Documentation

- Document analytics configuration changes
- Record major metric shifts and causes
- Share insights with team
- Create action items from findings

## Additional Resources

### Google Analytics 4

- [GA4 Documentation](https://support.google.com/analytics/answer/10089681)
- [GA4 Setup Guide](https://support.google.com/analytics/answer/9304153)
- [GA4 Event Reference](https://support.google.com/analytics/answer/9267735)

### MkDocs Material

- [Analytics Integration](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-analytics/)
- [Cookie Consent](https://squidfunk.github.io/mkdocs-material/setup/ensuring-data-privacy/)
- [User Feedback](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-analytics/#was-this-page-helpful)

### Privacy & GDPR

- [GDPR Official Text](https://gdpr-info.eu/)
- [Google Analytics GDPR Guide](https://support.google.com/analytics/answer/9019185)
- [Cookie Consent Best Practices](https://www.cookiebot.com/en/gdpr-cookies/)

## Getting Help

- Check [MkDocs Material documentation](https://squidfunk.github.io/mkdocs-material/)
- Review [Google Analytics Help Center](https://support.google.com/analytics)
- Open an issue on [GitHub](https://github.com/fgarofalo56/csa-inabox-docs/issues)
- Contact documentation team for assistance

---

Last Updated: 2025-12-09
Version: 1.0.0
Maintainer: CSA Documentation Team
