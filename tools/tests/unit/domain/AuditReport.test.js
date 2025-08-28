/**
 * Unit tests for AuditReport domain model
 */
import { AuditReport } from '../../../src/domain/models/AuditReport.js';
import { SAMPLE_AUDIT_ISSUES } from '../../fixtures/sample-files.js';

describe('AuditReport', () => {
  let report;

  beforeEach(() => {
    report = new AuditReport();
  });

  describe('constructor', () => {
    test('should initialize with default values', () => {
      expect(report.timestamp).toBeInstanceOf(Date);
      expect(report.totalFiles).toBe(0);
      expect(report.issues).toBeDefined();
      expect(report.summary.totalIssues).toBe(0);
      expect(report.recommendations).toEqual([]);
    });

    test('should initialize all issue types', () => {
      const expectedTypes = [
        'emptyFiles',
        'brokenLinks', 
        'orphanedFiles',
        'duplicateIndexReadme',
        'missingContent',
        'inaccessibleFiles',
        'diagramIssues',
        'customIssues'
      ];

      expectedTypes.forEach(type => {
        expect(report.issues[type]).toEqual([]);
      });
    });
  });

  describe('issue management', () => {
    test('should add single issue', () => {
      report.addIssue('emptyFiles', { file: 'test.md' }, 'critical');

      expect(report.issues.emptyFiles.length).toBe(1);
      expect(report.summary.totalIssues).toBe(1);
      expect(report.summary.criticalIssues).toBe(1);
    });

    test('should add multiple issues', () => {
      const issues = [
        { file: 'empty1.md', reason: 'Empty' },
        { file: 'empty2.md', reason: 'Empty' }
      ];
      
      report.addIssues('emptyFiles', issues, 'warning');

      expect(report.issues.emptyFiles.length).toBe(2);
      expect(report.summary.totalIssues).toBe(2);
      expect(report.summary.warningIssues).toBe(2);
    });

    test('should handle custom issue types', () => {
      report.addIssue('customType', { data: 'test' }, 'info');

      expect(report.issues.customIssues.length).toBe(1);
      expect(report.issues.customIssues[0].type).toBe('customType');
    });

    test('should get issues by type', () => {
      report.addIssue('emptyFiles', { file: 'test1.md' });
      report.addIssue('brokenLinks', { file: 'test2.md' });
      report.addIssue('emptyFiles', { file: 'test3.md' });

      const emptyFiles = report.getIssuesByType('emptyFiles');
      const brokenLinks = report.getIssuesByType('brokenLinks');

      expect(emptyFiles.length).toBe(2);
      expect(brokenLinks.length).toBe(1);
    });

    test('should get issues by severity', () => {
      report.addIssue('emptyFiles', { file: 'test1.md' }, 'critical');
      report.addIssue('brokenLinks', { file: 'test2.md' }, 'warning');
      report.addIssue('orphanedFiles', { file: 'test3.md' }, 'critical');

      const criticalIssues = report.getIssuesBySeverity('critical');
      const warningIssues = report.getIssuesBySeverity('warning');

      expect(criticalIssues.length).toBe(2);
      expect(warningIssues.length).toBe(1);
    });
  });

  describe('recommendations', () => {
    test('should add recommendation', () => {
      report.addRecommendation('Fix broken links', 1);

      expect(report.recommendations.length).toBe(1);
      expect(report.recommendations[0]).toMatchObject({
        recommendation: 'Fix broken links',
        priority: 1,
        type: 'general'
      });
    });

    test('should sort recommendations by priority', () => {
      report.addRecommendation('Low priority', 5);
      report.addRecommendation('High priority', 1);
      report.addRecommendation('Medium priority', 3);

      const sorted = report.getSortedRecommendations();

      expect(sorted[0].priority).toBe(1);
      expect(sorted[1].priority).toBe(3);
      expect(sorted[2].priority).toBe(5);
    });
  });

  describe('health score calculation', () => {
    test('should return 100 for no files', () => {
      const score = report.calculateHealthScore();
      expect(score).toBe(100);
    });

    test('should return 100 for no issues', () => {
      report.setTotalFiles(10);
      const score = report.calculateHealthScore();
      expect(score).toBe(100);
    });

    test('should calculate score with issues', () => {
      report.setTotalFiles(10);
      report.addIssue('emptyFiles', { file: 'test.md' }, 'critical'); // weight 3
      report.addIssue('brokenLinks', { file: 'test.md' }, 'warning'); // weight 1

      const score = report.calculateHealthScore();
      
      // Expected: 100 - ((1*3 + 1*1) / (10*3)) * 100 = 100 - (4/30)*100 = 86.67 ≈ 87
      expect(score).toBeLessThan(100);
      expect(score).toBeGreaterThan(80);
    });

    test('should not go below 0', () => {
      report.setTotalFiles(1);
      
      // Add many critical issues
      for (let i = 0; i < 10; i++) {
        report.addIssue('emptyFiles', { file: `test${i}.md` }, 'critical');
      }

      const score = report.calculateHealthScore();
      expect(score).toBe(0);
    });
  });

  describe('executive summary', () => {
    test('should generate executive summary', () => {
      report.setTotalFiles(5);
      report.addIssue('emptyFiles', { file: 'test1.md' }, 'critical');
      report.addIssue('brokenLinks', { file: 'test2.md' }, 'warning');

      const summary = report.getExecutiveSummary();

      expect(summary).toMatchObject({
        totalFiles: 5,
        totalIssues: 2,
        totalIssueTypes: 2,
        criticalIssues: 1,
        warningIssues: 1,
        infoIssues: 0
      });
      expect(summary.healthScore).toBeGreaterThan(0);
      expect(summary.timestamp).toBeDefined();
    });
  });

  describe('text report generation', () => {
    test('should generate comprehensive text report', () => {
      report.setTotalFiles(5);
      report.addIssue('emptyFiles', { file: 'empty.md', reason: 'Empty file' }, 'critical');
      report.addIssue('brokenLinks', {
        sourceFile: 'test.md',
        linkText: 'Missing',
        linkUrl: './missing.md',
        line: 5
      }, 'warning');
      report.addRecommendation('Fix empty files', 1);

      const textReport = report.generateTextReport();

      expect(textReport).toContain('DOCUMENTATION AUDIT REPORT');
      expect(textReport).toContain('EXECUTIVE SUMMARY');
      expect(textReport).toContain('Total files analyzed: 5');
      expect(textReport).toContain('EMPTY FILES (1)');
      expect(textReport).toContain('BROKEN LINKS (1)');
      expect(textReport).toContain('RECOMMENDATIONS');
      expect(textReport).toContain('Fix empty files');
    });

    test('should format different issue types correctly', () => {
      // Test broken link formatting
      const brokenLinkIssue = {
        sourceFile: '/test/file.md',
        linkText: 'Missing Link',
        linkUrl: './missing.md',
        line: 10
      };

      const formatted = report.formatIssue(brokenLinkIssue, 'brokenLinks');
      expect(formatted).toContain('/test/file.md:10');
      expect(formatted).toContain('[Missing Link](./missing.md)');

      // Test empty file formatting
      const emptyFileIssue = {
        file: '/test/empty.md',
        reason: 'Completely empty'
      };

      const formattedEmpty = report.formatIssue(emptyFileIssue, 'emptyFiles');
      expect(formattedEmpty).toContain('/test/empty.md');
      expect(formattedEmpty).toContain('Completely empty');
    });
  });

  describe('JSON serialization', () => {
    test('should serialize to complete JSON', () => {
      report.setTotalFiles(3);
      report.addIssue('emptyFiles', { file: 'empty.md' }, 'critical');
      report.addRecommendation('Fix issues', 1);

      const json = report.toJSON();

      expect(json).toHaveProperty('timestamp');
      expect(json).toHaveProperty('totalFiles', 3);
      expect(json).toHaveProperty('issues');
      expect(json).toHaveProperty('summary');
      expect(json).toHaveProperty('recommendations');
      expect(json).toHaveProperty('executiveSummary');

      expect(json.issues.emptyFiles.length).toBe(1);
      expect(json.summary.totalIssues).toBe(1);
      expect(json.recommendations.length).toBe(1);
    });

    test('should have valid JSON structure', () => {
      report.setTotalFiles(1);
      report.addIssue('emptyFiles', { file: 'test.md' });

      const json = report.toJSON();
      const serialized = JSON.stringify(json);
      const parsed = JSON.parse(serialized);

      expect(parsed).toEqual(json);
    });
  });

  describe('integration with sample data', () => {
    test('should handle sample audit issues', () => {
      report.setTotalFiles(10);

      // Add sample issues
      report.addIssues('emptyFiles', SAMPLE_AUDIT_ISSUES.emptyFiles, 'critical');
      report.addIssues('brokenLinks', SAMPLE_AUDIT_ISSUES.brokenLinks, 'warning');
      report.addIssues('orphanedFiles', SAMPLE_AUDIT_ISSUES.orphanedFiles, 'info');
      report.addIssues('duplicateIndexReadme', SAMPLE_AUDIT_ISSUES.duplicateIndexReadme, 'warning');

      expect(report.summary.totalIssues).toBe(4);
      expect(report.summary.criticalIssues).toBe(1);
      expect(report.summary.warningIssues).toBe(2);
      expect(report.summary.infoIssues).toBe(1);

      const healthScore = report.calculateHealthScore();
      expect(healthScore).toBeLessThan(100);
      expect(healthScore).toBeGreaterThan(50);
    });
  });
});