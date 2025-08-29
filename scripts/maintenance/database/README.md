# 🗄️ Database Maintenance Scripts

> **🏠 [Home](../../../README.md)** | **📚 [Documentation](../../../docs/README.md)** | **📜 [Scripts](../../README.md)** | **🔧 [Maintenance](../README.md)**

---

## 📋 Overview

This directory contains scripts for maintaining the analytics and monitoring databases used by the Cloud Scale Analytics (CSA) in-a-Box documentation project. These scripts handle database optimization, backup procedures, data archival, and performance monitoring to ensure reliable data storage and retrieval.

## 🎯 Purpose

The database maintenance scripts are designed to:

- **Optimize database performance** through regular maintenance operations
- **Backup and restore databases** to prevent data loss
- **Archive old data** to manage database size and performance
- **Monitor database health** and identify performance issues
- **Clean up obsolete data** and maintain data integrity
- **Generate database reports** for analysis and troubleshooting

## 📂 Current Scripts

### Available Scripts

Currently, no scripts exist in this directory. All scripts listed below are planned for implementation.

### Planned Scripts (To Be Created)

| Script | Purpose | Priority | Database Type |
|--------|---------|----------|---------------|
| `optimize-analytics-db.sh` | Optimize SQLite analytics database | **HIGH** | SQLite |
| `backup-databases.sh` | Backup all project databases | **HIGH** | All |
| `restore-database.sh` | Restore database from backup | **MEDIUM** | All |
| `archive-old-data.sh` | Archive old analytics data | **MEDIUM** | SQLite |
| `cleanup-database.sh` | Remove obsolete data and optimize | **MEDIUM** | All |
| `monitor-db-performance.sh` | Monitor database performance metrics | **LOW** | All |
| `migrate-database.sh` | Handle database schema migrations | **LOW** | All |

## 🗄️ Database Architecture

### Current Databases

The CSA documentation project uses the following databases:

**Analytics Database (`analytics.db`):**
- **Type:** SQLite
- **Location:** `docs/monitoring/data/analytics.db`
- **Purpose:** Store user analytics, page views, and performance metrics
- **Size:** Typically 10-100MB depending on usage
- **Retention:** 365 days for detailed data, indefinite for aggregated data

**Tables in Analytics Database:**
```sql
-- User events and page views
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    session_id TEXT,
    user_id TEXT,
    page_path TEXT,
    data JSON,
    context JSON
);

-- User feedback and ratings  
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    page_path TEXT,
    rating INTEGER,
    comment TEXT,
    session_id TEXT
);

-- Performance metrics
CREATE TABLE performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    page_path TEXT,
    load_time REAL,
    ttfb REAL,
    lcp REAL,
    fid REAL,
    cls REAL
);
```

## 🚀 Planned Script Details

### `optimize-analytics-db.sh` (Priority: HIGH)

**Purpose:** Optimize SQLite analytics database for best performance

**Features:**
- Run VACUUM to reclaim unused space
- Update table statistics with ANALYZE
- Rebuild indexes for optimal performance  
- Remove duplicate or corrupted records
- Generate optimization report

**Planned Usage:**
```bash
./optimize-analytics-db.sh [--database-path path] [--dry-run] [--verbose]

# Examples
./optimize-analytics-db.sh  # Use default database location
./optimize-analytics-db.sh --database-path /custom/path/analytics.db
./optimize-analytics-db.sh --dry-run --verbose  # Show what would be done
```

**Optimization Process:**
1. **Pre-optimization checks** - Verify database integrity
2. **Backup creation** - Create backup before optimization
3. **VACUUM operation** - Reclaim unused space
4. **ANALYZE operation** - Update table statistics
5. **Index rebuilding** - Optimize indexes for performance
6. **Integrity check** - Verify database after optimization
7. **Performance comparison** - Compare before/after metrics

### `backup-databases.sh` (Priority: HIGH)

**Purpose:** Create comprehensive backups of all project databases

**Features:**
- Backup all databases with consistent snapshots
- Support for full and incremental backups
- Compress backups to save storage space
- Verify backup integrity after creation
- Manage backup retention policies
- Store backups locally and optionally in cloud storage

**Planned Usage:**
```bash
./backup-databases.sh [--type type] [--output-dir path] [--compress] [--verify]

# Examples
./backup-databases.sh --type full  # Full backup of all databases
./backup-databases.sh --type incremental  # Incremental backup since last full
./backup-databases.sh --output-dir /backups/csa-docs --compress --verify
```

**Backup Types:**
- **Full backup:** Complete copy of all databases
- **Incremental backup:** Only changed data since last backup
- **Differential backup:** All changes since last full backup

### `restore-database.sh` (Priority: MEDIUM)

**Purpose:** Restore databases from backup files

**Features:**
- Restore from full or incremental backups
- Point-in-time recovery capabilities
- Verify data integrity after restore
- Support for partial restoration (specific tables)
- Rollback capability if restore fails

**Planned Usage:**
```bash
./restore-database.sh --backup-file path [--target-db path] [--verify]

# Examples
./restore-database.sh --backup-file /backups/analytics-2025-01-28.sql.gz
./restore-database.sh --backup-file /backups/full-backup.tar.gz --verify
```

### `archive-old-data.sh` (Priority: MEDIUM)

**Purpose:** Archive old analytics data to manage database size

**Features:**
- Archive data older than specified retention period
- Maintain aggregated summaries of archived data
- Export archived data to CSV/JSON for analysis
- Compress archived data for storage efficiency
- Verify archival process integrity

**Planned Usage:**
```bash
./archive-old-data.sh [--retention-days days] [--archive-format format] [--keep-summary]

# Examples
./archive-old-data.sh --retention-days 365  # Archive data older than 1 year
./archive-old-data.sh --archive-format csv --keep-summary
```

**Archival Process:**
1. **Identify old data** - Find records older than retention period
2. **Create summary data** - Generate aggregated statistics
3. **Export data** - Export to specified format (CSV, JSON, SQL)
4. **Compress archives** - Compress exported data files
5. **Remove from database** - Delete archived records from active database
6. **Update metadata** - Record archival operation details

## 📊 Database Performance Monitoring

### Key Performance Metrics

**Database Size and Growth:**
```sql
-- Database file size
SELECT 
    page_count * page_size as size_bytes,
    page_count * page_size / 1024 / 1024 as size_mb
FROM pragma_page_count(), pragma_page_size();

-- Table sizes
SELECT 
    name as table_name,
    COUNT(*) as row_count
FROM sqlite_master 
WHERE type='table' 
GROUP BY name;
```

**Query Performance:**
- **Average query execution time** - Monitor slow queries
- **Index usage statistics** - Ensure indexes are being used
- **Lock contention** - Monitor database locking issues
- **Connection pool utilization** - Track connection usage

**Data Quality Metrics:**
- **Record count trends** - Track data volume growth
- **Data freshness** - Monitor latest record timestamps
- **Duplicate detection** - Check for duplicate records
- **Referential integrity** - Verify foreign key constraints

### Performance Monitoring Dashboard

**Planned Metrics Dashboard:**
```bash
# Database performance summary
Database Size: 45.2 MB (+2.1MB this week)
Record Count: 1,247,893 records
Query Performance: 12ms avg (↓2ms from last week)
Index Usage: 98.5% (optimal)

Recent Operations:
- Last backup: 2025-01-28 02:00:00 (success)
- Last optimization: 2025-01-27 03:00:00 (success)  
- Last archival: 2025-01-21 01:00:00 (365 days)

Health Status: ✅ Healthy
Issues: None detected
```

## 🔧 Database Configuration

### SQLite Configuration

**Performance Settings:**
```sql
-- Enable WAL mode for better concurrency
PRAGMA journal_mode = WAL;

-- Optimize cache size (in pages)
PRAGMA cache_size = 10000;  

-- Set synchronous mode for performance/reliability balance
PRAGMA synchronous = NORMAL;

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Set temp store to memory for better performance
PRAGMA temp_store = MEMORY;

-- Optimize mmap size for large databases
PRAGMA mmap_size = 268435456;  -- 256MB
```

### Backup Configuration

**Backup Settings:**
```yaml
# Database backup configuration
database_backup:
  # Schedule
  full_backup_frequency: "daily"
  incremental_backup_frequency: "hourly"
  backup_time: "02:00"
  
  # Retention
  daily_retention: 30    # days
  weekly_retention: 12   # weeks  
  monthly_retention: 12  # months
  yearly_retention: 5    # years
  
  # Storage
  local_backup_path: "/var/backups/csa-docs"
  compress_backups: true
  verify_backups: true
  
  # Cloud storage (optional)
  azure_storage_account: "csadocsbackups"
  azure_container: "database-backups"
  
  # Notifications
  notify_on_success: false
  notify_on_failure: true
  notification_email: "admin@contoso.com"
```

### Archival Configuration

**Data Retention Policies:**
```yaml
# Data retention configuration  
data_retention:
  # Analytics data
  events:
    detailed_retention: 365    # days
    summary_retention: 1825    # days (5 years)
    archive_format: "csv"
  
  feedback:
    retention: 1095           # days (3 years)
    archive_format: "json"
  
  performance:
    detailed_retention: 90     # days
    summary_retention: 365     # days (1 year)
    archive_format: "csv"
  
  # Archival settings
  archive_path: "/var/archives/csa-docs"
  compress_archives: true
  verify_archives: true
  maintain_summaries: true
```

## 🔍 Database Health Monitoring

### Automated Health Checks

**Daily Health Check Items:**
- [ ] **Database accessibility** - Can connect and query successfully
- [ ] **File integrity** - Database files are not corrupted
- [ ] **Backup status** - Recent backups completed successfully
- [ ] **Disk space** - Sufficient space for growth and backups
- [ ] **Query performance** - No significant performance degradation
- [ ] **Data freshness** - Recent data is being written properly

**Weekly Health Check Items:**
- [ ] **Database size trends** - Monitor growth patterns
- [ ] **Index efficiency** - Verify indexes are being used effectively
- [ ] **Archival status** - Check if archival is needed
- [ ] **Backup verification** - Test restore from recent backups
- [ ] **Performance trends** - Analyze query performance over time

### Alert Conditions

**Critical Alerts:**
- **Database corruption detected** - Immediate attention required
- **Backup failures** - No successful backup in 48 hours
- **Disk space critical** - Less than 1GB free space
- **Query timeout errors** - Queries taking longer than 30 seconds

**Warning Alerts:**  
- **High database growth** - Size increased >50% in 7 days
- **Slow query performance** - Average query time >100ms
- **Backup warnings** - Backup took longer than usual
- **Archival needed** - Database size exceeds threshold

## 🛠️ Maintenance Procedures

### Routine Maintenance Schedule

**Daily (Automated):**
```bash
# 01:00 - Database health check
0 1 * * * /path/to/scripts/maintenance/database/monitor-db-performance.sh

# 02:00 - Incremental backup
0 2 * * * /path/to/scripts/maintenance/database/backup-databases.sh --type incremental

# 03:00 - Cleanup obsolete data
0 3 * * * /path/to/scripts/maintenance/database/cleanup-database.sh --routine
```

**Weekly (Sundays):**
```bash
# 01:00 - Full backup
0 1 * * 0 /path/to/scripts/maintenance/database/backup-databases.sh --type full

# 02:00 - Database optimization  
0 2 * * 0 /path/to/scripts/maintenance/database/optimize-analytics-db.sh

# 03:00 - Archive old data (if needed)
0 3 * * 0 /path/to/scripts/maintenance/database/archive-old-data.sh --retention-days 365
```

**Monthly (First Sunday):**
```bash
# 00:00 - Comprehensive maintenance
0 0 1-7 * 0 /path/to/scripts/maintenance/database/comprehensive-maintenance.sh
```

### Emergency Procedures

**Database Corruption Recovery:**
1. **Stop all database access** immediately
2. **Assess corruption extent** using integrity check
3. **Restore from most recent backup** if corruption is severe
4. **Recover using SQLite .recover command** if backup is not available
5. **Verify data integrity** after recovery
6. **Document incident** and review backup procedures

**Performance Issue Resolution:**
1. **Identify slow queries** using performance monitoring
2. **Check index usage** and add missing indexes if needed
3. **Optimize problematic queries** or redesign if necessary
4. **Consider archival** if database size is causing issues
5. **Monitor improvements** after optimization

## 🔍 Troubleshooting

### Common Database Issues

| Issue | Symptoms | Cause | Solution |
|-------|----------|--------|----------|
| **Database locked** | "Database is locked" errors | Concurrent access or crashed process | Kill blocking processes, check for stale locks |
| **Slow queries** | High response times | Missing indexes or large table scans | Analyze queries, add indexes, optimize schema |
| **Database growth** | Rapidly increasing file size | No archival or data retention policy | Implement archival, cleanup old data |
| **Backup failures** | Backup scripts failing | Insufficient permissions or disk space | Check permissions, free up disk space |
| **Corruption errors** | Integrity check failures | Disk issues or improper shutdown | Restore from backup or use .recover command |

### Diagnostic Commands

```bash
# Check database integrity
sqlite3 analytics.db "PRAGMA integrity_check;"

# Analyze database performance
sqlite3 analytics.db "PRAGMA optimize;"
sqlite3 analytics.db ".stats on"

# Check database file size and page info
sqlite3 analytics.db "PRAGMA page_count; PRAGMA page_size;"

# List all tables and their sizes
sqlite3 analytics.db ".tables"
sqlite3 analytics.db "SELECT name, COUNT(*) FROM sqlite_master WHERE type='table' GROUP BY name;"

# Check for locks and connections
lsof | grep analytics.db
```

### Performance Tuning

**SQLite Optimization Tips:**
- **Use WAL mode** - Better concurrency and crash recovery
- **Optimize cache size** - Increase cache_size for better performance
- **Create proper indexes** - Index frequently queried columns
- **Use prepared statements** - Avoid query compilation overhead
- **Batch transactions** - Group multiple operations in transactions
- **Regular VACUUM** - Reclaim space and optimize file structure

## 📚 Related Documentation

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Database Backup Best Practices](https://sqlite.org/backup.html)
- [SQLite Performance Tuning](https://www.sqlite.org/optoverview.html)
- [Maintenance Scripts Overview](../README.md)
- [System Administration Guide](../../../docs/guides/SYSTEM_ADMIN_GUIDE.md) *(planned)*

## 🤝 Contributing

### Adding New Database Scripts

1. **Identify database maintenance need** - Determine what database operation needs automation
2. **Follow database best practices** - Use transactions, proper error handling
3. **Include comprehensive testing** - Test with various database states and sizes
4. **Add proper logging** - Log all database operations and results
5. **Support different database types** - Consider SQLite, PostgreSQL, MySQL compatibility
6. **Include rollback procedures** - Provide way to undo operations if needed
7. **Update documentation** - Update this README with script details

### Script Requirements

- [ ] Uses database transactions for data consistency
- [ ] Includes comprehensive error handling and rollback
- [ ] Supports `--dry-run` mode for testing
- [ ] Has proper logging of all database operations
- [ ] Includes data integrity verification
- [ ] Supports multiple database types when applicable
- [ ] Has been tested with various database sizes
- [ ] Includes performance impact assessment
- [ ] Documents required database permissions
- [ ] Is documented in this README file

## 📞 Support

For database maintenance issues:

- **GitHub Issues:** [Create Database Issue](https://github.com/fgarofalo56/csa-inabox-docs/issues/new?labels=database,maintenance)
- **SQLite Help:** Check SQLite documentation and community forums
- **Database Logs:** Check database-specific logs in `/var/log/csa-docs/`
- **Performance Issues:** Use database profiling and diagnostic commands
- **Data Recovery:** Follow emergency procedures or contact team
- **Team Contact:** CSA Documentation Team

---

**Last Updated:** January 28, 2025  
**Version:** 1.0.0  
**Maintainer:** CSA Documentation Team