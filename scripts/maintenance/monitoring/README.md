# 📊 Monitoring and Health Check Scripts

> **🏠 [Home](../../../README.md)** | **📚 [Documentation](../../../docs/README.md)** | **📜 [Scripts](../../README.md)** | **🔧 [Maintenance](../README.md)**

---

## 📋 Overview

This directory contains scripts for monitoring the health and performance of the Cloud Scale Analytics (CSA) in-a-Box documentation project. These scripts perform health checks, validate content integrity, monitor system performance, and generate reports to ensure optimal operation and user experience.

## 🎯 Purpose

The monitoring and health check scripts are designed to:

- **Monitor documentation site availability** and response times
- **Validate content integrity** including links, images, and references  
- **Track performance metrics** for optimal user experience
- **Monitor system resources** and identify potential issues
- **Generate health reports** and alerting for proactive maintenance
- **Ensure compliance** with documentation standards and accessibility

## 📂 Current Scripts

### Available Scripts

Currently, no scripts exist in this directory. All scripts listed below are planned for implementation.

### Planned Scripts (To Be Created)

| Script | Purpose | Priority | Monitoring Scope |
|--------|---------|----------|------------------|
| `check-links.sh` | Validate all documentation links | **HIGH** | Content |
| `monitor-performance.sh` | Monitor site performance metrics | **HIGH** | Performance |
| `health-check-endpoints.sh` | Check all service endpoints | **MEDIUM** | Availability |
| `validate-accessibility.sh` | Check accessibility compliance | **MEDIUM** | Content |
| `monitor-ssl-certificates.sh` | Monitor SSL certificate status | **MEDIUM** | Security |
| `check-content-freshness.sh` | Monitor content update frequency | **LOW** | Content |
| `monitor-user-experience.sh` | Track user experience metrics | **LOW** | Performance |

## 🚀 Planned Script Details

### `check-links.sh` (Priority: HIGH)

**Purpose:** Comprehensive validation of all documentation links (internal and external)

**Features:**
- Scan all markdown files for links
- Validate internal links and anchors
- Check external links and handle timeouts
- Generate detailed link health report
- Auto-fix simple internal link issues
- Support for link exclusion lists

**Planned Usage:**
```bash
./check-links.sh [--fix-internal] [--exclude-external] [--output-format format] [--parallel threads]

# Examples
./check-links.sh --fix-internal  # Fix internal links automatically
./check-links.sh --exclude-external --output-format json
./check-links.sh --parallel 10 --timeout 30  # Use 10 threads, 30s timeout
```

**Link Validation Process:**
1. **Scan documentation files** - Find all markdown files and extract links
2. **Categorize links** - Separate internal, external, and anchor links
3. **Validate internal links** - Check file existence and anchor targets
4. **Check external links** - HTTP requests with timeout and retry logic
5. **Generate report** - Create detailed report with broken links
6. **Auto-fix issues** - Fix correctable internal link problems

### `monitor-performance.sh` (Priority: HIGH)

**Purpose:** Monitor website performance metrics and Core Web Vitals

**Features:**
- Measure page load times and Core Web Vitals
- Test from multiple geographic locations
- Monitor critical user journeys  
- Generate performance trend reports
- Alert on performance degradation
- Integration with monitoring dashboards

**Planned Usage:**
```bash
./monitor-performance.sh [--pages list] [--locations list] [--output-format format]

# Examples
./monitor-performance.sh --pages "index,architecture,guides"
./monitor-performance.sh --locations "us-east,eu-west,asia-south"
./monitor-performance.sh --output-format json --store-metrics
```

**Performance Metrics:**
- **Core Web Vitals:** LCP, FID, CLS, TTFB
- **Load Metrics:** Full page load time, first contentful paint
- **Resource Metrics:** JavaScript/CSS load times, image optimization
- **Network Metrics:** DNS resolution, connection time, SSL handshake
- **User Experience:** Time to interactive, cumulative layout shift

### `health-check-endpoints.sh` (Priority: MEDIUM)

**Purpose:** Monitor availability and health of all service endpoints

**Features:**
- Check documentation website availability
- Monitor monitoring API endpoints
- Validate SSL certificate status
- Test CDN and edge locations
- Generate uptime reports
- Send alerts for service outages

**Planned Usage:**
```bash
./health-check-endpoints.sh [--endpoints config] [--alert-email email] [--retry-count count]

# Examples
./health-check-endpoints.sh --endpoints config/endpoints.yml
./health-check-endpoints.sh --alert-email admin@contoso.com --retry-count 3
```

**Monitored Endpoints:**
```yaml
# config/endpoints.yml
endpoints:
  - name: "Main Documentation"
    url: "https://docs.contoso.com"
    method: "GET"
    expected_status: 200
    timeout: 30
    
  - name: "Monitoring API"
    url: "http://localhost:8056/api/health"
    method: "GET" 
    expected_status: 200
    timeout: 10
    
  - name: "Search API"
    url: "https://docs.contoso.com/search"
    method: "GET"
    expected_status: 200
    timeout: 15
```

### `validate-accessibility.sh` (Priority: MEDIUM)

**Purpose:** Validate documentation accessibility compliance

**Features:**
- Check WCAG 2.1 compliance
- Validate semantic HTML structure
- Test keyboard navigation
- Check color contrast ratios
- Validate alt text for images
- Generate accessibility reports

**Planned Usage:**
```bash
./validate-accessibility.sh [--standard wcag21] [--level aa] [--output-format format]

# Examples
./validate-accessibility.sh --standard wcag21 --level aa
./validate-accessibility.sh --output-format html --report-path reports/
```

## 📊 Monitoring Categories

### Content Health Monitoring

**Link Validation:**
- **Internal links** - Links within the documentation
- **External links** - Links to external websites and resources
- **Anchor links** - Links to specific sections within pages
- **Image links** - References to images and media files
- **Download links** - Links to downloadable resources

**Content Freshness:**
- **Last modified dates** - When content was last updated
- **Stale content detection** - Content not updated within threshold
- **Broken references** - References to moved or deleted content
- **Outdated screenshots** - Images that may be out of date

### Performance Monitoring

**Core Web Vitals:**
```javascript
// Metrics tracked by performance monitoring
const coreWebVitals = {
  LCP: 'Largest Contentful Paint',    // Should be < 2.5s
  FID: 'First Input Delay',           // Should be < 100ms  
  CLS: 'Cumulative Layout Shift',     // Should be < 0.1
  TTFB: 'Time to First Byte'          // Should be < 200ms
};
```

**Performance Thresholds:**
```yaml
performance_thresholds:
  excellent:
    lcp: 1.2          # seconds
    fid: 50           # milliseconds
    cls: 0.05         # score
    ttfb: 100         # milliseconds
    
  acceptable:
    lcp: 2.5          # seconds
    fid: 100          # milliseconds
    cls: 0.1          # score  
    ttfb: 200         # milliseconds
    
  poor:
    lcp: 4.0          # seconds
    fid: 300          # milliseconds
    cls: 0.25         # score
    ttfb: 500         # milliseconds
```

### System Health Monitoring  

**Service Availability:**
- **HTTP response codes** - 200, 404, 500 status monitoring
- **Response times** - Latency measurements
- **SSL certificate status** - Expiration and validity
- **DNS resolution** - Domain name resolution times
- **CDN health** - Content delivery network status

**Resource Utilization:**
- **CPU usage** - Server CPU utilization
- **Memory usage** - RAM consumption patterns
- **Disk space** - Storage utilization and growth
- **Network I/O** - Bandwidth and connection metrics
- **Database performance** - Query response times

## 🔧 Monitoring Configuration

### Health Check Configuration

**Configuration File:** `config/monitoring.yml`

```yaml
# Monitoring Configuration
monitoring:
  # Link checking
  link_checking:
    internal_timeout: 5        # seconds
    external_timeout: 30       # seconds
    parallel_threads: 5
    retry_count: 3
    retry_delay: 2             # seconds
    
    # Excluded patterns
    exclude_patterns:
      - "mailto:*"
      - "tel:*" 
      - "javascript:*"
      - "#temporary-*"
    
    # External domains to skip
    skip_external_domains:
      - "example.com"
      - "localhost"
  
  # Performance monitoring
  performance:
    # Test locations
    locations:
      - "us-east-1"
      - "eu-west-1" 
      - "ap-south-1"
    
    # Key pages to monitor
    critical_pages:
      - "/"
      - "/architecture/"
      - "/guides/"
      - "/search/"
    
    # Thresholds
    thresholds:
      warning_lcp: 2.5         # seconds
      critical_lcp: 4.0        # seconds
      warning_fid: 100         # milliseconds
      critical_fid: 300        # milliseconds
  
  # Health checks
  health_checks:
    check_interval: 300        # seconds (5 minutes)
    timeout: 30               # seconds
    retry_count: 3
    
    # Alert settings
    alerts:
      email: "admin@contoso.com"
      webhook: "https://hooks.slack.com/..."
      
    # Endpoints
    endpoints:
      - name: "Documentation Site"
        url: "https://docs.contoso.com"
        critical: true
        
      - name: "Monitoring API"
        url: "http://localhost:8056/api/health"
        critical: true
        
      - name: "Search Service"
        url: "https://docs.contoso.com/search"
        critical: false
```

### Alert Configuration

**Alert Rules:**
```yaml
# Alert rules configuration
alerts:
  # Critical alerts (immediate attention)
  critical:
    - condition: "site_down"
      description: "Documentation site is unreachable"
      threshold: "3 consecutive failures"
      
    - condition: "ssl_cert_expired"
      description: "SSL certificate has expired" 
      threshold: "immediate"
      
    - condition: "high_error_rate"
      description: "Error rate exceeds threshold"
      threshold: "> 5% in 5 minutes"
  
  # Warning alerts (should investigate)
  warning:
    - condition: "slow_response_time"
      description: "Response time is degraded"
      threshold: "> 5 seconds average for 10 minutes"
      
    - condition: "ssl_cert_expiring"
      description: "SSL certificate expires soon"
      threshold: "< 30 days"
      
    - condition: "broken_links"
      description: "Broken links detected"
      threshold: "> 10 broken links"
  
  # Info alerts (for awareness)
  info:
    - condition: "performance_degraded"
      description: "Performance metrics below optimal"
      threshold: "LCP > 2.5s for 30 minutes"
      
    - condition: "content_stale"
      description: "Content hasn't been updated recently"
      threshold: "> 90 days without update"
```

## 📈 Monitoring Reports

### Daily Health Report

**Daily Monitoring Summary:**
```
CSA Documentation Health Report - 2025-01-28

🟢 Overall Status: Healthy
📊 Uptime: 99.98% (24h)
⚡ Avg Response Time: 1.2s
🔗 Link Health: 99.8% (1,244/1,247 working)

Performance Metrics:
✅ Core Web Vitals: PASS
   - LCP: 1.8s (Good)
   - FID: 45ms (Good)  
   - CLS: 0.08 (Good)
   - TTFB: 150ms (Good)

Content Health:
✅ Link Validation: 3 issues found
   - 2 external links timeout (investigating)
   - 1 internal link fixed automatically

SSL Certificates:
✅ docs.contoso.com: Valid until 2025-04-15 (76 days)

Issues Requiring Attention:
⚠️ External link timeouts (non-critical)
   - https://example.com/old-resource (404)
   - https://partner-site.com/api (timeout)

Actions Taken:
- Fixed 1 internal broken link
- Updated link exclusion list
- Scheduled external link review

Next Check: 2025-01-29 06:00:00
```

### Performance Trend Report

**Weekly Performance Analysis:**
```bash
Performance Trend Analysis (Past 7 Days):

Core Web Vitals Trends:
- LCP: 1.6s → 1.8s (↑12% - investigate)
- FID: 42ms → 45ms (stable)
- CLS: 0.06 → 0.08 (↑33% - monitor)
- TTFB: 145ms → 150ms (stable)

Geographic Performance:
- US East: 1.5s avg (excellent)
- EU West: 1.9s avg (good)  
- Asia South: 2.3s avg (acceptable)

Critical Pages Performance:
- Homepage: 1.4s (good)
- Architecture: 2.1s (acceptable)
- Guides: 1.7s (good)
- Search: 1.6s (good)

Recommendations:
- Investigate LCP increase (possible new content)
- Optimize images on architecture pages
- Consider Asia CDN endpoint
```

## 🔍 Monitoring Tools Integration

### External Monitoring Services

**Supported Integrations:**
- **Uptime Robot** - External uptime monitoring
- **Pingdom** - Website performance monitoring
- **New Relic** - Application performance monitoring
- **Google PageSpeed Insights** - Core Web Vitals monitoring
- **GTmetrix** - Website speed testing

**Custom Monitoring Stack:**
```bash
# Local monitoring components
Prometheus     # Metrics collection
Grafana        # Visualization dashboards
AlertManager   # Alert routing and management
Node Exporter  # System metrics
Blackbox Exporter  # Endpoint probing
```

### Monitoring Dashboards

**Grafana Dashboard Panels:**
- **Site Availability** - Uptime percentage and incident timeline
- **Response Time Trends** - Historical response time charts
- **Core Web Vitals** - LCP, FID, CLS trend lines
- **Error Rate** - HTTP error code percentages
- **Link Health** - Working vs. broken link ratios
- **Content Freshness** - Last updated timestamps
- **SSL Certificate Status** - Certificate expiration timeline

## 🚨 Alerting and Notifications

### Notification Channels

**Supported Notification Methods:**
- **Email** - SMTP-based email notifications
- **Slack** - Webhook integration for team notifications
- **Microsoft Teams** - Webhook integration for enterprise teams
- **PagerDuty** - Incident management integration
- **Webhook** - Custom webhook endpoints

**Alert Routing:**
```yaml
# Alert routing configuration
routing:
  critical:
    channels: ["email", "slack", "pagerduty"]
    escalation: true
    
  warning:
    channels: ["email", "slack"]
    escalation: false
    
  info:
    channels: ["slack"]
    escalation: false
    
escalation_policy:
  - wait: 5m
    notify: ["team-lead"]
  - wait: 15m
    notify: ["manager", "on-call"]
  - wait: 30m
    notify: ["director"]
```

## 🔍 Troubleshooting

### Common Monitoring Issues

| Issue | Symptoms | Cause | Solution |
|-------|----------|--------|----------|
| **False positive alerts** | Alerts for working services | Network issues or strict thresholds | Adjust thresholds or add retry logic |
| **Missing alerts** | No alerts for actual issues | Monitoring service down or misconfigured | Check monitoring service status |
| **Slow link checking** | Link validation takes too long | Too many external links or slow sites | Increase timeouts or use parallel checking |
| **High false link failures** | Many links reported as broken | Network filtering or rate limiting | Add retry logic and check network path |
| **Performance inconsistency** | Metrics vary widely between checks | Network variability or server load | Use multiple measurements and averages |

### Debug Commands

```bash
# Test individual endpoints
curl -w "@curl-format.txt" -o /dev/null -s "https://docs.contoso.com"

# Check DNS resolution
dig docs.contoso.com
nslookup docs.contoso.com

# Test SSL certificate
openssl s_client -connect docs.contoso.com:443 -servername docs.contoso.com

# Check network path
traceroute docs.contoso.com
mtr docs.contoso.com

# Test from different locations  
curl -H "CF-IPCountry: US" https://docs.contoso.com
curl -H "CF-IPCountry: EU" https://docs.contoso.com
```

### Performance Optimization

**Monitoring Performance Tips:**
- **Use parallel processing** - Check multiple links/endpoints simultaneously
- **Implement caching** - Cache validation results to avoid repeated checks
- **Optimize frequency** - Balance thoroughness with resource usage
- **Use smart scheduling** - Schedule intensive checks during low traffic
- **Implement circuit breakers** - Skip unreliable external services temporarily

## 📚 Related Documentation

- [System Administration Guide](../../../docs/guides/SYSTEM_ADMIN_GUIDE.md) *(planned)*
- [Performance Optimization Guide](../../../docs/guides/PERFORMANCE_OPTIMIZATION.md) *(planned)*
- [Alerting and Monitoring Guide](../../../docs/guides/ALERTING_GUIDE.md) *(planned)*
- [Maintenance Scripts Overview](../README.md)
- [Database Maintenance Guide](../database/README.md)

## 🤝 Contributing

### Adding New Monitoring Scripts

1. **Identify monitoring need** - Determine what aspect needs monitoring
2. **Define success criteria** - Establish what "healthy" looks like
3. **Implement comprehensive checks** - Cover edge cases and failure modes
4. **Add proper error handling** - Handle network issues, timeouts gracefully
5. **Include detailed reporting** - Provide actionable information in reports
6. **Test with real failures** - Verify monitoring detects actual issues
7. **Update documentation** - Update this README with script details

### Script Requirements

- [ ] Supports configurable timeouts and retries
- [ ] Includes comprehensive error handling
- [ ] Generates detailed reports in multiple formats
- [ ] Has proper logging of all operations
- [ ] Supports parallel processing where beneficial
- [ ] Includes dry-run mode for testing
- [ ] Has configurable alert thresholds
- [ ] Is tested with various failure scenarios
- [ ] Integrates with existing monitoring infrastructure
- [ ] Is documented in this README file

## 📞 Support

For monitoring and health check issues:

- **GitHub Issues:** [Create Monitoring Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?labels=monitoring,maintenance)
- **Performance Issues:** Use performance testing tools and browser developer tools
- **Link Issues:** Check network connectivity and DNS resolution
- **SSL Issues:** Verify certificate status and expiration dates
- **Monitoring Logs:** Check monitoring logs in `/var/log/csa-docs/`
- **Team Contact:** CSA Documentation Team

---

**Last Updated:** January 28, 2025  
**Version:** 1.0.0  
**Maintainer:** CSA Documentation Team