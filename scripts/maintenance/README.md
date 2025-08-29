# 🔧 Maintenance Scripts

> **🏠 [Home](../../README.md)** | **📚 [Documentation](../../docs/README.md)** | **📜 [Scripts](../README.md)** | **📊 [Project Tracking](../../project_tracking/README.md)**

---

## 📋 Overview

This directory contains scripts for ongoing maintenance and monitoring of the Cloud Scale Analytics (CSA) in-a-Box documentation project. These scripts automate routine maintenance tasks, data cleanup, system monitoring, and health checks to ensure optimal performance and reliability.

## 🎯 Purpose

The maintenance scripts are designed to:

- **Monitor documentation health** and performance metrics
- **Validate content integrity** including links, images, and references
- **Clean up temporary and obsolete data** to optimize storage
- **Backup critical data** and configuration files
- **Maintain database performance** for analytics and monitoring systems
- **Generate maintenance reports** for system health analysis

## 📂 Directory Structure

```
maintenance/
├── 📄 README.md                    # This file
├── 📁 database/                    # Database maintenance scripts
│   ├── 📄 README.md                # Database maintenance documentation
│   └── (planned database scripts)
├── 📁 cleanup/                     # System cleanup scripts
│   ├── 📄 README.md                # Cleanup scripts documentation
│   └── (planned cleanup scripts)
└── 📁 monitoring/                  # Monitoring and health check scripts
    ├── 📄 README.md                # Monitoring scripts documentation
    └── (planned monitoring scripts)
```

## 📂 Current Scripts

### Available Scripts

Currently, no scripts exist in this directory. All scripts listed below are planned for implementation.

### Planned Scripts (To Be Created)

| Category | Script | Purpose | Priority |
|----------|--------|---------|----------|
| **General** | `health-check.sh` | Comprehensive system health check | **HIGH** |
| **General** | `validate-all.sh` | Validate all documentation content | **HIGH** |
| **Database** | `optimize-analytics-db.sh` | Optimize analytics database performance | **MEDIUM** |
| **Database** | `backup-databases.sh` | Backup all databases and data | **MEDIUM** |
| **Cleanup** | `cleanup-temp-files.sh` | Remove temporary files and caches | **HIGH** |
| **Cleanup** | `cleanup-old-logs.sh` | Archive and remove old log files | **MEDIUM** |
| **Monitoring** | `check-links.sh` | Validate all documentation links | **HIGH** |
| **Monitoring** | `monitor-performance.sh` | Monitor site performance metrics | **MEDIUM** |

## 🚀 Usage Examples

### Daily Maintenance

```bash
# Run daily health check
./scripts/maintenance/health-check.sh --report-email admin@contoso.com

# Clean temporary files
./scripts/maintenance/cleanup/cleanup-temp-files.sh

# Validate documentation links
./scripts/maintenance/monitoring/check-links.sh --fix-internal
```

### Weekly Maintenance

```bash
# Comprehensive validation
./scripts/maintenance/validate-all.sh --verbose

# Database optimization
./scripts/maintenance/database/optimize-analytics-db.sh

# Performance monitoring
./scripts/maintenance/monitoring/monitor-performance.sh --generate-report
```

### Monthly Maintenance

```bash
# Full system backup
./scripts/maintenance/database/backup-databases.sh --full-backup

# Clean old logs (keep last 90 days)
./scripts/maintenance/cleanup/cleanup-old-logs.sh --days 90

# Generate maintenance report
./scripts/maintenance/generate-maintenance-report.sh --month
```

## 📋 Planned Script Details

### `health-check.sh` (Priority: HIGH)

**Purpose:** Comprehensive system health monitoring and reporting

**Features:**
- Check all documentation sites and endpoints
- Validate SSL certificates and domain configuration
- Monitor resource usage (CPU, memory, disk)
- Test monitoring system functionality
- Generate health status report
- Send alerts for critical issues

**Planned Usage:**
```bash
./health-check.sh [--report-email email] [--alert-threshold level] [--output-format format]

# Examples
./health-check.sh --report-email admin@contoso.com
./health-check.sh --alert-threshold critical --output-format json
./health-check.sh --silent  # No console output, only logs
```

### `validate-all.sh` (Priority: HIGH)

**Purpose:** Comprehensive validation of all documentation content

**Features:**
- Validate markdown syntax and structure
- Check all internal and external links
- Verify image references and accessibility
- Validate code snippets and examples
- Check documentation completeness
- Generate validation report with metrics

**Planned Usage:**
```bash
./validate-all.sh [--fix-auto] [--report-format format] [--exclude-external]

# Examples
./validate-all.sh --fix-auto  # Fix issues automatically where possible
./validate-all.sh --report-format html --exclude-external
./validate-all.sh --verbose --output-dir reports/
```

## 🔧 Maintenance Categories

### Database Maintenance

See [Database maintenance documentation](./database/README.md) for detailed information about:
- Analytics database optimization
- Data backup and recovery procedures
- Database cleanup and archival
- Performance monitoring and tuning

### System Cleanup

See [Cleanup scripts documentation](./cleanup/README.md) for detailed information about:
- Temporary file cleanup procedures
- Log rotation and archival
- Cache management and optimization
- Storage space management

### Monitoring and Health Checks

See [Monitoring scripts documentation](./monitoring/README.md) for detailed information about:
- Link validation and health checks
- Performance monitoring and metrics
- Uptime and availability tracking
- Alert generation and notification

## 📊 Maintenance Scheduling

### Automated Maintenance Schedule

**Daily (Automated via Cron):**
```bash
# 02:00 - Health check and basic validation
0 2 * * * /path/to/scripts/maintenance/health-check.sh --quiet

# 03:00 - Clean temporary files  
0 3 * * * /path/to/scripts/maintenance/cleanup/cleanup-temp-files.sh

# 04:00 - Link validation
0 4 * * * /path/to/scripts/maintenance/monitoring/check-links.sh
```

**Weekly (Sundays):**
```bash
# 01:00 - Database optimization
0 1 * * 0 /path/to/scripts/maintenance/database/optimize-analytics-db.sh

# 02:00 - Comprehensive validation
0 2 * * 0 /path/to/scripts/maintenance/validate-all.sh --report-email admin@contoso.com
```

**Monthly (First Sunday):**
```bash
# 00:00 - Full backup
0 0 1-7 * 0 /path/to/scripts/maintenance/database/backup-databases.sh --full-backup

# 01:00 - Log cleanup (keep 90 days)
0 1 1-7 * 0 /path/to/scripts/maintenance/cleanup/cleanup-old-logs.sh --days 90
```

### Manual Maintenance Tasks

**Before Major Updates:**
- [ ] Run full validation suite
- [ ] Create full system backup
- [ ] Check resource utilization trends
- [ ] Review and update maintenance scripts
- [ ] Test rollback procedures

**After Major Updates:**
- [ ] Verify all functionality works
- [ ] Run comprehensive health check
- [ ] Monitor performance metrics
- [ ] Check for broken links or references
- [ ] Update maintenance documentation

## 🔧 Configuration

### Maintenance Configuration File

**File:** `config/maintenance.yml`

```yaml
# Maintenance Configuration
maintenance:
  # Health check settings
  health_check:
    endpoints:
      - name: "Main Documentation"
        url: "https://docs.contoso.com"
        timeout: 30
        expected_status: 200
      - name: "Monitoring API"
        url: "http://localhost:8056/api/health"
        timeout: 10
        expected_status: 200
    
    alerts:
      email: "admin@contoso.com"
      threshold: "warning"
      retry_count: 3
  
  # Validation settings
  validation:
    check_external_links: true
    external_link_timeout: 15
    check_images: true
    check_code_blocks: true
    fix_auto: false
  
  # Cleanup settings  
  cleanup:
    temp_file_retention: 7  # days
    log_retention: 90      # days
    cache_retention: 30    # days
    backup_retention: 365  # days
  
  # Database settings
  database:
    optimization_schedule: "weekly"
    backup_schedule: "daily"
    analytics_retention: 365  # days
    performance_retention: 90 # days
  
  # Monitoring settings
  monitoring:
    performance_threshold:
      page_load_time: 3.0  # seconds
      error_rate: 0.01     # 1%
      uptime: 99.9         # percent
    
    report_frequency: "daily"
    dashboard_refresh: 300  # seconds
```

### Environment Variables

```bash
# Maintenance configuration
MAINTENANCE_CONFIG=/path/to/config/maintenance.yml
MAINTENANCE_LOG_LEVEL=INFO
MAINTENANCE_EMAIL=admin@contoso.com

# Health check endpoints
HEALTH_CHECK_MAIN_URL=https://docs.contoso.com
HEALTH_CHECK_API_URL=http://localhost:8056

# Database configuration
ANALYTICS_DB_PATH=/path/to/analytics.db
BACKUP_STORAGE_PATH=/path/to/backups

# Notification settings
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
SMTP_USER=notifications@contoso.com
SMTP_PASSWORD=your-password

# Cleanup settings
TEMP_DIR=/tmp/csa-docs
LOG_DIR=/var/log/csa-docs
CACHE_DIR=/var/cache/csa-docs
```

## 📈 Monitoring and Metrics

### Key Performance Indicators (KPIs)

**Documentation Health:**
- **Link health rate:** % of working links
- **Content freshness:** Days since last update
- **Build success rate:** % of successful builds
- **Validation pass rate:** % of content passing validation

**System Performance:**
- **Page load time:** Average load time in seconds
- **Uptime:** % availability over time period
- **Error rate:** % of requests resulting in errors  
- **Resource utilization:** CPU, memory, disk usage

**User Experience:**
- **User engagement:** Page views, session duration
- **Feedback scores:** User ratings and comments
- **Search success:** % of successful searches
- **Mobile experience:** Mobile-specific metrics

### Maintenance Reports

**Daily Health Report:**
```
CSA Documentation Health Report - 2025-01-28

System Status: ✅ Healthy
Uptime: 99.95% (24h)
Average Response Time: 1.2s

Link Validation:
- Total Links: 1,247
- Working Links: 1,244 (99.76%)
- Broken Links: 3
- External Links: 423 (checked)

Performance Metrics:
- Page Load Time: 1.8s (avg)
- Core Web Vitals: Pass
- Error Rate: 0.02%

Issues Found:
- 2 broken internal links (auto-fixed)
- 1 external link timeout (monitoring)

Actions Taken:
- Cleaned 156MB temp files
- Optimized 3 database queries
- Updated 1 SSL certificate
```

## 🔍 Troubleshooting

### Common Maintenance Issues

| Issue | Cause | Solution |
|-------|--------|----------|
| **High disk usage** | Accumulation of logs/temp files | Run cleanup scripts more frequently |
| **Slow database queries** | Database needs optimization | Run database optimization script |
| **Broken links detected** | External sites changed/moved | Update links or mark as known issues |
| **SSL certificate expiring** | Automatic renewal failed | Check cert-manager or renew manually |
| **High memory usage** | Memory leak or large dataset | Restart services and monitor trends |
| **Backup failures** | Insufficient storage or permissions | Check storage space and permissions |

### Debug and Logging

**Log Locations:**
```bash
# Main maintenance log
/var/log/csa-docs/maintenance.log

# Script-specific logs
/var/log/csa-docs/health-check.log
/var/log/csa-docs/validation.log
/var/log/csa-docs/cleanup.log

# Database logs
/var/log/csa-docs/database.log

# Error logs
/var/log/csa-docs/errors.log
```

**Debug Commands:**
```bash
# Check system resources
df -h  # Disk usage
free -h  # Memory usage
top  # Process usage

# Check service status
systemctl status csa-docs-monitoring
systemctl status nginx

# Check logs
tail -f /var/log/csa-docs/maintenance.log
journalctl -u csa-docs-monitoring -f

# Manual health check
curl -s http://localhost:8056/api/health | jq '.'
```

## ⚡ Performance Optimization

### Database Performance

- **Regular optimization** - Run VACUUM and ANALYZE on SQLite databases
- **Index management** - Ensure proper indexes on frequently queried columns
- **Query optimization** - Monitor slow queries and optimize them
- **Data archival** - Archive old analytics data to keep databases lean

### System Performance

- **Resource monitoring** - Track CPU, memory, and disk usage trends
- **Cache management** - Implement and maintain proper caching strategies
- **Content optimization** - Compress images and optimize static assets
- **CDN utilization** - Use CDN for static content delivery

### Maintenance Efficiency

- **Parallel processing** - Run multiple maintenance tasks concurrently
- **Incremental checks** - Only check changed content when possible
- **Smart scheduling** - Schedule resource-intensive tasks during low usage
- **Result caching** - Cache validation results to avoid repeated checks

## 📚 Related Documentation

- [Database Maintenance Guide](./database/README.md)
- [Cleanup Procedures Guide](./cleanup/README.md)
- [Monitoring and Health Checks Guide](./monitoring/README.md)
- [System Administration Guide](../../docs/guides/SYSTEM_ADMIN_GUIDE.md) *(planned)*
- [Troubleshooting Guide](../../docs/guides/TROUBLESHOOTING.md) *(planned)*

## 🤝 Contributing

### Adding New Maintenance Scripts

1. **Identify maintenance need** - Determine what requires regular maintenance
2. **Choose appropriate category** - database, cleanup, or monitoring
3. **Follow scripting standards** - Use standard template and error handling
4. **Include comprehensive logging** - Log all operations and results
5. **Add configuration options** - Make scripts configurable via environment variables
6. **Test thoroughly** - Test in various scenarios and edge cases
7. **Update documentation** - Update this README and category-specific READMEs

### Script Requirements

- [ ] Follows naming conventions (`kebab-case.sh`)
- [ ] Includes proper header with metadata
- [ ] Has comprehensive error handling and logging
- [ ] Supports `--help`, `--dry-run`, and `--verbose` flags
- [ ] Is idempotent (safe to run multiple times)
- [ ] Has configurable parameters via environment variables
- [ ] Includes progress indicators for long-running operations
- [ ] Generates summary reports of actions taken
- [ ] Is documented in appropriate README files
- [ ] Has been tested with various input scenarios

## 📞 Support

For maintenance-related issues:

- **GitHub Issues:** [Create Maintenance Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?labels=maintenance)
- **Documentation:** Check script `--help` output and category-specific READMEs
- **Logs:** Check maintenance logs in `/var/log/csa-docs/`
- **System Status:** Use health check scripts for current status
- **Team Contact:** CSA Documentation Team

---

**Last Updated:** January 28, 2025  
**Version:** 1.0.0  
**Maintainer:** CSA Documentation Team