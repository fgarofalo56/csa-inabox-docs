/**
 * Domain model for documentation audit reports
 * Aggregates issues and provides analysis capabilities
 */
export class AuditReport {
  constructor() {
    this.timestamp = new Date();
    this.totalFiles = 0;
    this.issues = {
      emptyFiles: [],
      brokenLinks: [],
      orphanedFiles: [],
      duplicateIndexReadme: [],
      missingContent: [],
      inaccessibleFiles: [],
      diagramIssues: [],
      customIssues: []
    };
    this.summary = {
      totalIssues: 0,
      criticalIssues: 0,
      warningIssues: 0,
      infoIssues: 0
    };
    this.recommendations = [];
  }

  /**
   * Add an issue to the report
   * @param {string} type - Issue type
   * @param {object} issue - Issue details
   * @param {string} severity - Issue severity (critical, warning, info)
   */
  addIssue(type, issue, severity = 'warning') {
    if (!this.issues[type]) {
      this.issues.customIssues.push({ type, issue, severity });
    } else {
      this.issues[type].push({ ...issue, severity });
    }

    this.summary.totalIssues++;
    
    switch (severity) {
      case 'critical':
        this.summary.criticalIssues++;
        break;
      case 'warning':
        this.summary.warningIssues++;
        break;
      case 'info':
        this.summary.infoIssues++;
        break;
    }
  }

  /**
   * Add multiple issues of the same type
   * @param {string} type - Issue type
   * @param {object[]} issues - Array of issues
   * @param {string} severity - Issue severity
   */
  addIssues(type, issues, severity = 'warning') {
    issues.forEach(issue => this.addIssue(type, issue, severity));
  }

  /**
   * Add a recommendation
   * @param {string} recommendation - Recommendation text
   * @param {number} priority - Priority level (1-5, 1 being highest)
   */
  addRecommendation(recommendation, priority = 3) {
    this.recommendations.push({ recommendation, priority, type: 'general' });
  }

  /**
   * Get issues by type
   * @param {string} type - Issue type
   * @returns {object[]} - Array of issues
   */
  getIssuesByType(type) {
    return this.issues[type] || [];
  }

  /**
   * Get issues by severity
   * @param {string} severity - Issue severity
   * @returns {object[]} - Array of issues
   */
  getIssuesBySeverity(severity) {
    const allIssues = [];
    Object.values(this.issues).forEach(issueArray => {
      if (Array.isArray(issueArray)) {
        allIssues.push(...issueArray.filter(issue => issue.severity === severity));
      }
    });
    return allIssues;
  }

  /**
   * Get sorted recommendations by priority
   * @returns {object[]} - Sorted recommendations
   */
  getSortedRecommendations() {
    return this.recommendations.sort((a, b) => a.priority - b.priority);
  }

  /**
   * Generate executive summary
   * @returns {object} - Executive summary
   */
  getExecutiveSummary() {
    const totalIssueTypes = Object.keys(this.issues).filter(key => this.issues[key].length > 0).length;
    
    return {
      totalFiles: this.totalFiles,
      totalIssues: this.summary.totalIssues,
      totalIssueTypes,
      criticalIssues: this.summary.criticalIssues,
      warningIssues: this.summary.warningIssues,
      infoIssues: this.summary.infoIssues,
      healthScore: this.calculateHealthScore(),
      timestamp: this.timestamp.toISOString()
    };
  }

  /**
   * Calculate documentation health score (0-100)
   * @returns {number} - Health score
   */
  calculateHealthScore() {
    if (this.totalFiles === 0) return 100;

    const criticalWeight = 3;
    const warningWeight = 1;
    const infoWeight = 0.2;

    const weightedIssues = 
      (this.summary.criticalIssues * criticalWeight) +
      (this.summary.warningIssues * warningWeight) +
      (this.summary.infoIssues * infoWeight);

    const maxPossibleScore = this.totalFiles * criticalWeight;
    const score = Math.max(0, 100 - ((weightedIssues / maxPossibleScore) * 100));

    return Math.round(score);
  }

  /**
   * Generate text report
   * @returns {string} - Formatted text report
   */
  generateTextReport() {
    const lines = [];
    lines.push('📊 DOCUMENTATION AUDIT REPORT');
    lines.push('=' .repeat(60));
    lines.push('');

    // Executive Summary
    const summary = this.getExecutiveSummary();
    lines.push('📈 EXECUTIVE SUMMARY:');
    lines.push(`Total files analyzed: ${summary.totalFiles}`);
    lines.push(`Total issues found: ${summary.totalIssues}`);
    lines.push(`Documentation health score: ${summary.healthScore}/100`);
    lines.push(`Critical issues: ${summary.criticalIssues}`);
    lines.push(`Warning issues: ${summary.warningIssues}`);
    lines.push(`Info issues: ${summary.infoIssues}`);
    lines.push('');

    // Issue Details
    Object.entries(this.issues).forEach(([type, issues]) => {
      if (issues.length > 0) {
        lines.push(`🔍 ${type.toUpperCase().replace(/([A-Z])/g, ' $1').trim()} (${issues.length}):`);
        issues.forEach(issue => {
          const severity = issue.severity || 'warning';
          const icon = severity === 'critical' ? '🚨' : severity === 'warning' ? '⚠️' : 'ℹ️';
          lines.push(`   ${icon} ${this.formatIssue(issue, type)}`);
        });
        lines.push('');
      }
    });

    // Recommendations
    if (this.recommendations.length > 0) {
      lines.push('💡 RECOMMENDATIONS:');
      this.getSortedRecommendations().forEach((rec, index) => {
        const priority = rec.priority <= 2 ? '🔥 HIGH' : rec.priority <= 3 ? '📋 MEDIUM' : '📝 LOW';
        lines.push(`${index + 1}. [${priority}] ${rec.recommendation}`);
      });
      lines.push('');
    }

    lines.push(`Generated at: ${this.timestamp.toISOString()}`);
    lines.push('✨ AUDIT COMPLETE!');

    return lines.join('\n');
  }

  /**
   * Format individual issue for display
   * @param {object} issue - Issue object
   * @param {string} type - Issue type
   * @returns {string} - Formatted issue string
   */
  formatIssue(issue, type) {
    switch (type) {
      case 'brokenLinks':
        return `${issue.sourceFile}:${issue.line} - [${issue.linkText}](${issue.linkUrl})`;
      case 'emptyFiles':
      case 'missingContent':
      case 'orphanedFiles':
      case 'inaccessibleFiles':
        return `${issue.file || issue.relativePath}: ${issue.reason || issue.description}`;
      case 'duplicateIndexReadme':
        return `${issue.directory}: Both index.md and README.md exist`;
      default:
        return JSON.stringify(issue);
    }
  }

  /**
   * Export report as JSON
   * @returns {object} - Complete report as JSON
   */
  toJSON() {
    return {
      timestamp: this.timestamp.toISOString(),
      totalFiles: this.totalFiles,
      issues: this.issues,
      summary: this.summary,
      recommendations: this.recommendations,
      executiveSummary: this.getExecutiveSummary()
    };
  }

  /**
   * Set total files count
   * @param {number} count - Total files count
   */
  setTotalFiles(count) {
    this.totalFiles = count;
  }
}