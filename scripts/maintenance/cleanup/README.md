# 🧹 System Cleanup Scripts

> **🏠 [Home](../../../README.md)** | **📚 [Documentation](../../../docs/README.md)** | **📜 [Scripts](../../README.md)** | **🔧 [Maintenance](../README.md)**

---

## 📋 Overview

This directory contains scripts for cleaning up temporary files, managing disk space, and maintaining optimal system performance for the Cloud Scale Analytics (CSA) in-a-Box documentation project. These scripts help prevent disk space issues and maintain system efficiency by removing obsolete data and optimizing storage usage.

## 🎯 Purpose

The cleanup scripts are designed to:

- **Remove temporary files and caches** to free up disk space
- **Manage log file rotation and archival** to prevent log files from consuming excessive space
- **Clean up build artifacts** from documentation generation processes
- **Optimize storage usage** by compressing and archiving old data
- **Maintain system performance** by preventing disk space issues
- **Generate cleanup reports** to track space reclamation and system health

## 📂 Current Scripts

### Available Scripts

Currently, no scripts exist in this directory. All scripts listed below are planned for implementation.

### Planned Scripts (To Be Created)

| Script | Purpose | Priority | Frequency |
|--------|---------|----------|-----------|
| `cleanup-temp-files.sh` | Remove temporary files and caches | **HIGH** | Daily |
| `cleanup-old-logs.sh` | Archive and rotate log files | **HIGH** | Daily |
| `cleanup-build-artifacts.sh` | Remove old build artifacts | **MEDIUM** | Weekly |
| `cleanup-monitoring-data.sh` | Clean old monitoring cache data | **MEDIUM** | Weekly |
| `compress-archives.sh` | Compress old archive files | **LOW** | Monthly |
| `disk-space-monitor.sh` | Monitor and alert on disk usage | **MEDIUM** | Daily |
| `storage-optimizer.sh` | Optimize storage configuration | **LOW** | Monthly |

## 🚀 Planned Script Details

### `cleanup-temp-files.sh` (Priority: HIGH)

**Purpose:** Remove temporary files, caches, and other transient data to free up disk space

**Features:**
- Clean system temporary directories
- Remove MkDocs build cache files
- Clean browser cache and temporary downloads
- Remove Python __pycache__ directories
- Clean Node.js node_modules caches
- Generate cleanup summary report

**Planned Usage:**
```bash
./cleanup-temp-files.sh [--dry-run] [--aggressive] [--older-than days]

# Examples
./cleanup-temp-files.sh  # Standard cleanup
./cleanup-temp-files.sh --dry-run  # Show what would be cleaned
./cleanup-temp-files.sh --aggressive --older-than 7  # Aggressive cleanup of files older than 7 days
```

**Cleanup Targets:**
```bash
# Temporary directories
/tmp/csa-docs-*
/var/tmp/mkdocs-*
~/.cache/pip/
~/.npm/_cacache/

# Build artifacts
site/
.mkdocs_cache/
**/__pycache__/
**/*.pyc
**/*.pyo

# Log files (temporary)
*.log.tmp
*.log.old

# Monitoring temp data
docs/monitoring/cache/*
docs/monitoring/temp/*
```

### `cleanup-old-logs.sh` (Priority: HIGH)

**Purpose:** Manage log files through rotation, compression, and archival

**Features:**
- Rotate log files based on size and age
- Compress old log files to save space
- Archive logs to long-term storage
- Maintain specified retention periods
- Generate log cleanup summary

**Planned Usage:**
```bash
./cleanup-old-logs.sh [--retention-days days] [--compress] [--archive-path path]

# Examples
./cleanup-old-logs.sh --retention-days 90  # Keep logs for 90 days
./cleanup-old-logs.sh --compress --archive-path /archives/logs
./cleanup-old-logs.sh --dry-run --verbose  # Show what would be done
```

**Log Management Policy:**
```bash
# Retention periods by log type
application.log:    30 days (compressed after 7 days)
error.log:         90 days (compressed after 14 days)
access.log:        60 days (compressed after 7 days)
monitoring.log:    45 days (compressed after 7 days)
maintenance.log:   180 days (compressed after 30 days)
```

### `cleanup-build-artifacts.sh` (Priority: MEDIUM)

**Purpose:** Remove old build artifacts and generated files from documentation builds

**Features:**
- Remove old documentation builds
- Clean intermediate build files
- Remove outdated static assets
- Clean deployment artifacts
- Preserve current and recent builds

**Planned Usage:**
```bash
./cleanup-build-artifacts.sh [--keep-builds count] [--older-than days]

# Examples
./cleanup-build-artifacts.sh --keep-builds 5  # Keep last 5 builds
./cleanup-build-artifacts.sh --older-than 30  # Remove builds older than 30 days
```

### `cleanup-monitoring-data.sh` (Priority: MEDIUM)

**Purpose:** Clean old monitoring cache data and temporary analytics files

**Features:**
- Remove old cache files from monitoring system
- Clean temporary analytics data files
- Archive performance metrics data
- Remove obsolete monitoring configurations
- Optimize monitoring database

**Planned Usage:**
```bash
./cleanup-monitoring-data.sh [--retention-days days] [--optimize-db]

# Examples
./cleanup-monitoring-data.sh --retention-days 30
./cleanup-monitoring-data.sh --optimize-db --verbose
```

## 🧹 Cleanup Categories

### Temporary Files and Caches

**System Temporary Files:**
- `/tmp/` - System temporary directory
- `/var/tmp/` - Persistent temporary files
- User cache directories (`~/.cache/`)

**Application Caches:**
- **Python caches** - `__pycache__/`, `*.pyc` files
- **Node.js caches** - `node_modules/.cache/`, npm cache
- **MkDocs caches** - Build cache and temporary files
- **Browser caches** - Downloaded assets and temporary files

**Build Artifacts:**
- **Documentation builds** - Generated site files
- **Intermediate files** - Processing temporary files
- **Asset compilation** - CSS/JS build artifacts

### Log Files Management

**Log File Categories:**
```bash
# Application logs
/var/log/csa-docs/application.log      # Main application logs
/var/log/csa-docs/error.log           # Error logs
/var/log/csa-docs/monitoring.log      # Monitoring system logs

# System logs (if managed)
/var/log/nginx/access.log             # Web server access logs
/var/log/nginx/error.log              # Web server error logs

# Maintenance logs  
/var/log/csa-docs/maintenance.log     # Maintenance operation logs
/var/log/csa-docs/backup.log          # Backup operation logs
```

**Log Rotation Configuration:**
```bash
# logrotate configuration for CSA docs
/var/log/csa-docs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload csa-docs-monitoring
    endscript
}
```

### Archive Management

**Archive Types:**
- **Compressed logs** - Gzipped old log files
- **Data archives** - Archived analytics and monitoring data
- **Backup archives** - Database and configuration backups
- **Documentation archives** - Historical documentation versions

## 📊 Disk Space Monitoring

### Storage Usage Tracking

**Monitored Directories:**
```bash
# Primary storage locations
/                           # Root filesystem
/var/log/                  # Log files
/tmp/                      # Temporary files
/home/user/.cache/         # User caches
docs/monitoring/data/      # Analytics database
docs/site/                 # Built documentation
backups/                   # Backup files
```

**Storage Metrics:**
- **Total disk usage** - Overall disk utilization percentage
- **Directory sizes** - Size of key directories
- **Growth rates** - Rate of storage consumption
- **Available space** - Remaining free space
- **Inode usage** - File system inode utilization

### Disk Space Alerts

**Alert Thresholds:**
```yaml
disk_usage_alerts:
  critical: 95%      # Immediate attention required
  warning: 85%       # Cleanup should be scheduled
  info: 75%         # Monitor closely
  
directory_size_alerts:
  logs:
    warning: 1GB     # Log directory size warning
    critical: 5GB    # Log directory size critical
  
  temp:
    warning: 500MB   # Temp directory size warning
    critical: 2GB    # Temp directory size critical
  
  monitoring:
    warning: 2GB     # Monitoring data size warning
    critical: 10GB   # Monitoring data size critical
```

## 🔧 Cleanup Configuration

### Cleanup Settings

**Configuration File:** `config/cleanup.yml`

```yaml
# Cleanup Configuration
cleanup:
  # Temporary files
  temp_files:
    retention_hours: 24
    aggressive_retention_hours: 6
    protected_patterns:
      - "*.lock"
      - "*.pid"
    
    directories:
      - "/tmp/csa-docs-*"
      - "/var/tmp/mkdocs-*"
      - "~/.cache/pip"
      - "**/__pycache__"
  
  # Log files
  log_files:
    default_retention_days: 30
    compress_after_days: 7
    
    retention_by_type:
      application: 30
      error: 90
      access: 60
      monitoring: 45
      maintenance: 180
  
  # Build artifacts
  build_artifacts:
    keep_recent_builds: 5
    retention_days: 30
    
    directories:
      - "site/"
      - ".mkdocs_cache/"
      - "build/"
      - "dist/"
  
  # Monitoring data
  monitoring_data:
    cache_retention_days: 14
    temp_retention_hours: 48
    archive_threshold_mb: 100
  
  # Disk space monitoring
  disk_monitoring:
    warning_threshold: 85
    critical_threshold: 95
    check_interval_minutes: 60
    
    monitored_paths:
      - "/"
      - "/var"
      - "/tmp"
      - "/home"
```

### Environment Variables

```bash
# Cleanup configuration
CLEANUP_CONFIG_PATH=/path/to/config/cleanup.yml
CLEANUP_LOG_LEVEL=INFO
CLEANUP_DRY_RUN=false

# Retention settings
TEMP_FILE_RETENTION_HOURS=24
LOG_FILE_RETENTION_DAYS=30
BUILD_ARTIFACT_RETENTION_DAYS=30

# Paths
TEMP_CLEANUP_PATHS="/tmp/csa-docs-*,/var/tmp/mkdocs-*"
LOG_CLEANUP_PATHS="/var/log/csa-docs/"
BUILD_CLEANUP_PATHS="site/,.mkdocs_cache/"

# Archive settings
ARCHIVE_PATH=/var/archives/csa-docs
COMPRESS_ARCHIVES=true
ARCHIVE_RETENTION_DAYS=365

# Monitoring
DISK_USAGE_WARNING_THRESHOLD=85
DISK_USAGE_CRITICAL_THRESHOLD=95
```

## 📈 Cleanup Reporting

### Cleanup Summary Report

**Daily Cleanup Report:**
```
CSA Documentation Cleanup Report - 2025-01-28

Disk Space Status:
- Total Usage: 42% (18.5GB / 44.1GB)
- Available Space: 25.6GB
- Status: ✅ Healthy

Cleanup Operations:
✅ Temporary Files:
   - Files removed: 1,247
   - Space reclaimed: 156.2 MB
   - Directories cleaned: 8

✅ Log Files:
   - Files rotated: 12
   - Files compressed: 5
   - Space reclaimed: 89.3 MB

✅ Build Artifacts:
   - Old builds removed: 3
   - Space reclaimed: 234.7 MB

✅ Monitoring Data:
   - Cache files cleaned: 67
   - Space reclaimed: 45.1 MB

Total Space Reclaimed: 525.3 MB
Total Files Processed: 1,331
Cleanup Duration: 2m 14s

Issues:
- None detected

Next Scheduled Cleanup: 2025-01-29 03:00:00
```

### Storage Trend Analysis

**Weekly Storage Report:**
```bash
Storage Trend Analysis (Past 7 Days):

Directory Growth:
- /var/log/: +45.2MB (normal)
- docs/monitoring/: +123.7MB (above average)  
- /tmp/: +12.3MB (normal)
- backups/: +1.2GB (new backups)

Cleanup Effectiveness:
- Space reclaimed this week: 3.2GB
- Average daily cleanup: 457MB
- Largest single cleanup: 1.1GB (log rotation)

Recommendations:
- Monitor monitoring data growth
- Consider more frequent backup cleanup
- Monitoring database may need optimization
```

## 🔍 Troubleshooting

### Common Cleanup Issues

| Issue | Symptoms | Cause | Solution |
|-------|----------|--------|----------|
| **Files not being deleted** | Cleanup reports 0 files removed | Permission issues or files in use | Check permissions and running processes |
| **Disk still full after cleanup** | High disk usage persists | Large files not covered by cleanup | Manual investigation and cleanup needed |
| **Log rotation failing** | Log files growing without rotation | Logrotate configuration issues | Check logrotate configuration and permissions |
| **Cleanup taking too long** | Cleanup scripts timeout | Too many files or slow disk I/O | Optimize cleanup scope or increase timeouts |
| **Archives consuming space** | Archive directory growing rapidly | No archive cleanup policy | Implement archive retention policy |

### Diagnostic Commands

```bash
# Check disk usage
df -h                           # Overall disk usage
du -sh /var/log/csa-docs/*     # Log directory sizes
du -sh /tmp/csa-docs-*         # Temp directory sizes
du -sh ~/.cache/*              # Cache directory sizes

# Find large files
find /var/log -type f -size +100M -ls
find /tmp -type f -size +50M -ls
find . -name "*.log" -size +10M -ls

# Check file age
find /tmp -type f -mtime +7 -ls     # Files older than 7 days
find /var/log -name "*.log" -mtime +30 -ls

# Check file permissions
ls -la /var/log/csa-docs/
ls -la /tmp/csa-docs-*/

# Check running processes using files
lsof +D /var/log/csa-docs/
lsof +D /tmp/csa-docs-*/
```

### Performance Optimization

**Cleanup Performance Tips:**
- **Parallelize operations** - Clean multiple directories concurrently
- **Use find with -delete** - More efficient than find + rm
- **Batch operations** - Process files in batches to avoid memory issues
- **Skip unnecessary checks** - Don't check files that are definitely safe to delete
- **Use rsync for archives** - More efficient for large file operations

**Optimized Find Commands:**
```bash
# Efficient temp file cleanup
find /tmp -path "/tmp/csa-docs-*" -type f -mtime +1 -delete

# Efficient cache cleanup
find ~/.cache -type f -atime +7 -delete

# Efficient log cleanup with compression
find /var/log/csa-docs -name "*.log" -mtime +7 -exec gzip {} \;
```

## 🔄 Automation and Scheduling

### Cron Configuration

**Daily Cleanup Tasks:**
```bash
# /etc/cron.d/csa-docs-cleanup

# Daily temp file cleanup at 3 AM
0 3 * * * root /path/to/scripts/maintenance/cleanup/cleanup-temp-files.sh

# Daily log rotation at 4 AM
0 4 * * * root /path/to/scripts/maintenance/cleanup/cleanup-old-logs.sh

# Daily disk space monitoring every hour
0 * * * * root /path/to/scripts/maintenance/cleanup/disk-space-monitor.sh
```

**Weekly Cleanup Tasks:**
```bash
# Weekly build artifact cleanup (Sundays at 2 AM)
0 2 * * 0 root /path/to/scripts/maintenance/cleanup/cleanup-build-artifacts.sh

# Weekly monitoring data cleanup (Sundays at 3 AM)
0 3 * * 0 root /path/to/scripts/maintenance/cleanup/cleanup-monitoring-data.sh
```

**Monthly Cleanup Tasks:**
```bash
# Monthly archive compression (1st of month at 1 AM)
0 1 1 * * root /path/to/scripts/maintenance/cleanup/compress-archives.sh

# Monthly storage optimization (1st of month at 2 AM)
0 2 1 * * root /path/to/scripts/maintenance/cleanup/storage-optimizer.sh
```

### Systemd Timers (Alternative to Cron)

```ini
# /etc/systemd/system/csa-docs-cleanup.timer
[Unit]
Description=CSA Documentation Cleanup Timer
Requires=csa-docs-cleanup.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

## 📚 Related Documentation

- [System Administration Guide](../../../docs/guides/SYSTEM_ADMIN_GUIDE.md) *(planned)*
- [Storage Management Best Practices](../../../docs/guides/STORAGE_MANAGEMENT.md) *(planned)*
- [Maintenance Scripts Overview](../README.md)
- [Database Maintenance Guide](../database/README.md)
- [Monitoring Scripts Guide](../monitoring/README.md)

## 🤝 Contributing

### Adding New Cleanup Scripts

1. **Identify cleanup target** - Determine what files/data need regular cleanup
2. **Assess impact and safety** - Ensure cleanup won't affect running systems
3. **Implement dry-run mode** - Allow testing without actual deletion
4. **Add comprehensive logging** - Log all cleanup operations and results
5. **Include size reporting** - Report how much space was reclaimed
6. **Test thoroughly** - Test with various file patterns and edge cases
7. **Update documentation** - Update this README with script details

### Script Requirements

- [ ] Supports `--dry-run` mode for testing
- [ ] Includes comprehensive error handling
- [ ] Logs all operations and results
- [ ] Reports space reclaimed and files processed
- [ ] Has configurable retention periods
- [ ] Handles locked files and permission issues gracefully
- [ ] Includes safety checks to prevent accidental deletion
- [ ] Supports parallel processing for large cleanup operations
- [ ] Is idempotent (safe to run multiple times)
- [ ] Is documented in this README file

## 📞 Support

For cleanup and storage issues:

- **GitHub Issues:** [Create Cleanup Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?labels=cleanup,maintenance)
- **Disk Space Issues:** Use diagnostic commands to identify large files
- **Permission Issues:** Check file ownership and permissions
- **Cleanup Logs:** Check cleanup logs in `/var/log/csa-docs/`
- **System Status:** Use disk monitoring tools and commands
- **Team Contact:** CSA Documentation Team

---

**Last Updated:** January 28, 2025  
**Version:** 1.0.0  
**Maintainer:** CSA Documentation Team