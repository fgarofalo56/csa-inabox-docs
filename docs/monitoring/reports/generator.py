"""
Automated Reporting System
Generates comprehensive reports and insights for Cloud Scale Analytics documentation
"""

import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import statistics
from collections import defaultdict, Counter
import re
from jinja2 import Template
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportType(Enum):
    """Types of reports that can be generated"""
    DAILY_HEALTH = "daily_health"
    WEEKLY_SUMMARY = "weekly_summary"
    MONTHLY_ANALYSIS = "monthly_analysis"
    PERFORMANCE_AUDIT = "performance_audit"
    USER_BEHAVIOR = "user_behavior"
    CONTENT_EFFECTIVENESS = "content_effectiveness"
    SEARCH_INSIGHTS = "search_insights"
    ISSUE_TRACKER = "issue_tracker"
    CUSTOM = "custom"


class InsightPriority(Enum):
    """Priority levels for insights"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class Insight:
    """Represents an actionable insight"""
    title: str
    description: str
    priority: InsightPriority
    category: str
    metric_value: Any
    threshold: Any
    recommendation: str
    impact: str
    effort: str
    data_source: str
    timestamp: datetime


@dataclass
class ReportSection:
    """Represents a section of a report"""
    title: str
    content: Dict[str, Any]
    charts: List[Dict[str, Any]]
    insights: List[Insight]
    summary: str


class ReportGenerator:
    """Generates automated reports with insights"""
    
    def __init__(self, config_path: str = "config/reports.yml"):
        self.config = self._load_config(config_path)
        self.templates = self._load_templates()
        self.data_sources = {}
        self.insights_engine = InsightsEngine()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load report configuration"""
        config_file = Path(config_path)
        if config_file.exists():
            import yaml
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default report configuration"""
        return {
            "reports": {
                "daily_health": {
                    "enabled": True,
                    "schedule": "0 9 * * *",  # 9 AM daily
                    "recipients": ["docs-team@microsoft.com"],
                    "format": ["html", "pdf"]
                },
                "weekly_summary": {
                    "enabled": True,
                    "schedule": "0 9 * * MON",  # 9 AM Monday
                    "recipients": ["docs-team@microsoft.com", "stakeholders@microsoft.com"],
                    "format": ["html", "pdf", "csv"]
                },
                "monthly_analysis": {
                    "enabled": True,
                    "schedule": "0 9 1 * *",  # 9 AM first of month
                    "recipients": ["management@microsoft.com"],
                    "format": ["html", "pdf", "pptx"]
                }
            },
            "thresholds": {
                "quality_score_min": 85,
                "page_load_max": 3000,
                "broken_links_max": 5,
                "error_rate_max": 0.01,
                "bounce_rate_max": 0.40
            },
            "insights": {
                "enabled": True,
                "min_confidence": 0.7,
                "max_insights_per_report": 10
            }
        }
    
    def _load_templates(self) -> Dict[str, Template]:
        """Load report templates"""
        templates = {}
        template_dir = Path("templates")
        
        if template_dir.exists():
            for template_file in template_dir.glob("*.html"):
                with open(template_file, 'r') as f:
                    templates[template_file.stem] = Template(f.read())
        else:
            # Use default templates
            templates = {
                "daily_health": Template(self._default_daily_template()),
                "weekly_summary": Template(self._default_weekly_template()),
                "monthly_analysis": Template(self._default_monthly_template())
            }
        
        return templates
    
    def _default_daily_template(self) -> str:
        """Default daily health report template"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Daily Health Report - {{ date }}</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
                .header { background: #0066cc; color: white; padding: 20px; }
                .metric { display: inline-block; margin: 10px; padding: 15px; background: #f5f5f5; }
                .alert { padding: 10px; margin: 10px 0; border-left: 4px solid; }
                .alert.critical { border-color: #d83b01; background: #fef2f1; }
                .alert.warning { border-color: #ffb700; background: #fff9e6; }
                .alert.info { border-color: #0066cc; background: #e6f2ff; }
                table { width: 100%; border-collapse: collapse; }
                th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Documentation Health Report</h1>
                <p>{{ date }} | Overall Status: {{ overall_status }}</p>
            </div>
            
            <h2>Key Metrics</h2>
            <div class="metrics">
                {% for metric in key_metrics %}
                <div class="metric">
                    <h3>{{ metric.name }}</h3>
                    <p class="value">{{ metric.value }}</p>
                    <p class="change">{{ metric.change }}</p>
                </div>
                {% endfor %}
            </div>
            
            <h2>Critical Issues</h2>
            {% for issue in critical_issues %}
            <div class="alert critical">
                <strong>{{ issue.title }}</strong>
                <p>{{ issue.description }}</p>
                <p>Action: {{ issue.action }}</p>
            </div>
            {% endfor %}
            
            <h2>Insights & Recommendations</h2>
            {% for insight in insights %}
            <div class="alert {{ insight.priority }}">
                <strong>{{ insight.title }}</strong>
                <p>{{ insight.description }}</p>
                <p>Recommendation: {{ insight.recommendation }}</p>
            </div>
            {% endfor %}
            
            <h2>Detailed Metrics</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Current</th>
                    <th>Previous</th>
                    <th>Change</th>
                    <th>Status</th>
                </tr>
                {% for row in detailed_metrics %}
                <tr>
                    <td>{{ row.metric }}</td>
                    <td>{{ row.current }}</td>
                    <td>{{ row.previous }}</td>
                    <td>{{ row.change }}</td>
                    <td>{{ row.status }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
        """
    
    def _default_weekly_template(self) -> str:
        """Default weekly summary template"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Weekly Summary - Week {{ week_number }}</title>
            <style>
                /* Similar styles as daily template */
            </style>
        </head>
        <body>
            <h1>Weekly Documentation Summary</h1>
            <!-- Weekly content here -->
        </body>
        </html>
        """
    
    def _default_monthly_template(self) -> str:
        """Default monthly analysis template"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Monthly Analysis - {{ month }} {{ year }}</title>
            <style>
                /* Similar styles as daily template */
            </style>
        </head>
        <body>
            <h1>Monthly Documentation Analysis</h1>
            <!-- Monthly content here -->
        </body>
        </html>
        """
    
    async def generate_report(self, report_type: ReportType, 
                             start_date: datetime = None, 
                             end_date: datetime = None) -> Dict:
        """Generate a specific type of report"""
        
        if not start_date:
            start_date = self._get_default_start_date(report_type)
        if not end_date:
            end_date = datetime.now()
        
        # Collect data from various sources
        data = await self._collect_data(start_date, end_date)
        
        # Generate insights
        insights = self.insights_engine.analyze(data, report_type)
        
        # Build report sections
        sections = self._build_report_sections(report_type, data, insights)
        
        # Generate report
        report = {
            "type": report_type.value,
            "generated_at": datetime.now().isoformat(),
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "sections": sections,
            "insights": [asdict(i) for i in insights],
            "summary": self._generate_executive_summary(sections, insights)
        }
        
        # Render report in requested formats
        rendered = await self._render_report(report, report_type)
        
        return rendered
    
    def _get_default_start_date(self, report_type: ReportType) -> datetime:
        """Get default start date based on report type"""
        now = datetime.now()
        
        if report_type == ReportType.DAILY_HEALTH:
            return now - timedelta(days=1)
        elif report_type == ReportType.WEEKLY_SUMMARY:
            return now - timedelta(weeks=1)
        elif report_type == ReportType.MONTHLY_ANALYSIS:
            return now - timedelta(days=30)
        else:
            return now - timedelta(days=7)
    
    async def _collect_data(self, start_date: datetime, end_date: datetime) -> Dict:
        """Collect data from various sources"""
        tasks = [
            self._fetch_analytics_data(start_date, end_date),
            self._fetch_performance_data(start_date, end_date),
            self._fetch_health_data(start_date, end_date),
            self._fetch_feedback_data(start_date, end_date),
            self._fetch_error_data(start_date, end_date)
        ]
        
        results = await asyncio.gather(*tasks)
        
        return {
            "analytics": results[0],
            "performance": results[1],
            "health": results[2],
            "feedback": results[3],
            "errors": results[4]
        }
    
    async def _fetch_analytics_data(self, start_date: datetime, end_date: datetime) -> Dict:
        """Fetch analytics data"""
        # This would connect to the analytics database
        return {
            "page_views": 45678,
            "unique_users": 12345,
            "avg_session_duration": 245,  # seconds
            "bounce_rate": 0.32,
            "top_pages": [
                {"path": "/getting-started", "views": 5432},
                {"path": "/api-reference", "views": 3211},
                {"path": "/tutorials", "views": 2987}
            ]
        }
    
    async def _fetch_performance_data(self, start_date: datetime, end_date: datetime) -> Dict:
        """Fetch performance data"""
        return {
            "avg_load_time": 1.8,  # seconds
            "p95_load_time": 3.2,
            "core_web_vitals": {
                "lcp": {"value": 2.1, "rating": "good"},
                "fid": {"value": 85, "rating": "good"},
                "cls": {"value": 0.08, "rating": "good"}
            }
        }
    
    async def _fetch_health_data(self, start_date: datetime, end_date: datetime) -> Dict:
        """Fetch health data"""
        return {
            "quality_score": 92,
            "broken_links": 3,
            "missing_images": 1,
            "outdated_content": 5,
            "build_success_rate": 0.985
        }
    
    async def _fetch_feedback_data(self, start_date: datetime, end_date: datetime) -> Dict:
        """Fetch feedback data"""
        return {
            "total_feedback": 234,
            "avg_rating": 4.2,
            "sentiment": {
                "positive": 0.72,
                "neutral": 0.20,
                "negative": 0.08
            }
        }
    
    async def _fetch_error_data(self, start_date: datetime, end_date: datetime) -> Dict:
        """Fetch error data"""
        return {
            "total_errors": 45,
            "error_rate": 0.0098,
            "top_errors": [
                {"type": "404", "count": 23},
                {"type": "JavaScript", "count": 12}
            ]
        }
    
    def _build_report_sections(self, report_type: ReportType, 
                              data: Dict, insights: List[Insight]) -> List[ReportSection]:
        """Build report sections based on type and data"""
        sections = []
        
        if report_type == ReportType.DAILY_HEALTH:
            sections.extend([
                self._build_overview_section(data),
                self._build_health_section(data),
                self._build_issues_section(data),
                self._build_performance_section(data)
            ])
        elif report_type == ReportType.WEEKLY_SUMMARY:
            sections.extend([
                self._build_overview_section(data),
                self._build_trends_section(data),
                self._build_user_behavior_section(data),
                self._build_content_section(data)
            ])
        elif report_type == ReportType.MONTHLY_ANALYSIS:
            sections.extend([
                self._build_executive_section(data),
                self._build_comprehensive_analysis_section(data),
                self._build_recommendations_section(insights)
            ])
        
        return sections
    
    def _build_overview_section(self, data: Dict) -> ReportSection:
        """Build overview section"""
        return ReportSection(
            title="Overview",
            content={
                "total_page_views": data["analytics"]["page_views"],
                "unique_users": data["analytics"]["unique_users"],
                "quality_score": data["health"]["quality_score"],
                "performance_score": self._calculate_performance_score(data["performance"])
            },
            charts=[
                {
                    "type": "line",
                    "title": "Daily Page Views",
                    "data": []  # Would contain actual chart data
                }
            ],
            insights=[],
            summary="Documentation health and usage metrics for the reporting period"
        )
    
    def _build_health_section(self, data: Dict) -> ReportSection:
        """Build health metrics section"""
        return ReportSection(
            title="Health Metrics",
            content=data["health"],
            charts=[],
            insights=[],
            summary="Current health status of documentation"
        )
    
    def _build_issues_section(self, data: Dict) -> ReportSection:
        """Build issues section"""
        return ReportSection(
            title="Active Issues",
            content={
                "broken_links": data["health"]["broken_links"],
                "errors": data["errors"]["total_errors"],
                "outdated_content": data["health"]["outdated_content"]
            },
            charts=[],
            insights=[],
            summary="Current issues requiring attention"
        )
    
    def _build_performance_section(self, data: Dict) -> ReportSection:
        """Build performance section"""
        return ReportSection(
            title="Performance",
            content=data["performance"],
            charts=[
                {
                    "type": "gauge",
                    "title": "Core Web Vitals",
                    "data": data["performance"]["core_web_vitals"]
                }
            ],
            insights=[],
            summary="Performance metrics and Core Web Vitals"
        )
    
    def _build_trends_section(self, data: Dict) -> ReportSection:
        """Build trends section"""
        # Calculate trends from historical data
        return ReportSection(
            title="Weekly Trends",
            content={},
            charts=[],
            insights=[],
            summary="Week-over-week trends"
        )
    
    def _build_user_behavior_section(self, data: Dict) -> ReportSection:
        """Build user behavior section"""
        return ReportSection(
            title="User Behavior",
            content={
                "avg_session_duration": data["analytics"]["avg_session_duration"],
                "bounce_rate": data["analytics"]["bounce_rate"],
                "top_pages": data["analytics"]["top_pages"]
            },
            charts=[],
            insights=[],
            summary="User interaction patterns"
        )
    
    def _build_content_section(self, data: Dict) -> ReportSection:
        """Build content effectiveness section"""
        return ReportSection(
            title="Content Effectiveness",
            content={
                "feedback_score": data["feedback"]["avg_rating"],
                "sentiment": data["feedback"]["sentiment"]
            },
            charts=[],
            insights=[],
            summary="Content performance and user satisfaction"
        )
    
    def _build_executive_section(self, data: Dict) -> ReportSection:
        """Build executive summary section"""
        return ReportSection(
            title="Executive Summary",
            content={},
            charts=[],
            insights=[],
            summary="High-level overview for leadership"
        )
    
    def _build_comprehensive_analysis_section(self, data: Dict) -> ReportSection:
        """Build comprehensive analysis section"""
        return ReportSection(
            title="Comprehensive Analysis",
            content={},
            charts=[],
            insights=[],
            summary="Deep dive into all metrics"
        )
    
    def _build_recommendations_section(self, insights: List[Insight]) -> ReportSection:
        """Build recommendations section"""
        return ReportSection(
            title="Recommendations",
            content={
                "critical": [i for i in insights if i.priority == InsightPriority.CRITICAL],
                "high": [i for i in insights if i.priority == InsightPriority.HIGH]
            },
            charts=[],
            insights=insights,
            summary="Actionable recommendations based on data analysis"
        )
    
    def _calculate_performance_score(self, performance_data: Dict) -> int:
        """Calculate overall performance score"""
        scores = []
        
        # LCP score
        lcp = performance_data["core_web_vitals"]["lcp"]["value"]
        if lcp <= 2.5:
            scores.append(100)
        elif lcp <= 4.0:
            scores.append(50)
        else:
            scores.append(0)
        
        # FID score
        fid = performance_data["core_web_vitals"]["fid"]["value"]
        if fid <= 100:
            scores.append(100)
        elif fid <= 300:
            scores.append(50)
        else:
            scores.append(0)
        
        # CLS score
        cls = performance_data["core_web_vitals"]["cls"]["value"]
        if cls <= 0.1:
            scores.append(100)
        elif cls <= 0.25:
            scores.append(50)
        else:
            scores.append(0)
        
        return int(statistics.mean(scores))
    
    def _generate_executive_summary(self, sections: List[ReportSection], 
                                  insights: List[Insight]) -> str:
        """Generate executive summary"""
        critical_insights = [i for i in insights if i.priority == InsightPriority.CRITICAL]
        high_insights = [i for i in insights if i.priority == InsightPriority.HIGH]
        
        summary = f"Report generated with {len(sections)} sections and {len(insights)} insights. "
        
        if critical_insights:
            summary += f"{len(critical_insights)} critical issues require immediate attention. "
        
        if high_insights:
            summary += f"{len(high_insights)} high-priority recommendations identified."
        
        return summary
    
    async def _render_report(self, report: Dict, report_type: ReportType) -> Dict:
        """Render report in various formats"""
        rendered = {}
        
        # Render HTML
        if report_type.value in self.templates:
            template = self.templates[report_type.value]
            rendered["html"] = template.render(**report)
        
        # Generate PDF (would use library like weasyprint)
        rendered["pdf"] = None  # Placeholder
        
        # Generate CSV data export
        rendered["csv"] = self._generate_csv_export(report)
        
        return rendered
    
    def _generate_csv_export(self, report: Dict) -> str:
        """Generate CSV export of report data"""
        # Flatten report data for CSV export
        rows = []
        
        for section in report["sections"]:
            for key, value in section.content.items():
                rows.append({
                    "section": section.title,
                    "metric": key,
                    "value": value
                })
        
        df = pd.DataFrame(rows)
        return df.to_csv(index=False)


class InsightsEngine:
    """Generates actionable insights from data"""
    
    def analyze(self, data: Dict, report_type: ReportType) -> List[Insight]:
        """Analyze data and generate insights"""
        insights = []
        
        # Analyze performance
        insights.extend(self._analyze_performance(data.get("performance", {})))
        
        # Analyze health
        insights.extend(self._analyze_health(data.get("health", {})))
        
        # Analyze user behavior
        insights.extend(self._analyze_user_behavior(data.get("analytics", {})))
        
        # Analyze errors
        insights.extend(self._analyze_errors(data.get("errors", {})))
        
        # Analyze feedback
        insights.extend(self._analyze_feedback(data.get("feedback", {})))
        
        # Sort by priority and limit
        insights.sort(key=lambda x: self._priority_value(x.priority), reverse=True)
        
        return insights[:10]  # Return top 10 insights
    
    def _analyze_performance(self, performance_data: Dict) -> List[Insight]:
        """Analyze performance data for insights"""
        insights = []
        
        if performance_data.get("avg_load_time", 0) > 3:
            insights.append(Insight(
                title="Slow Page Load Times",
                description=f"Average page load time is {performance_data['avg_load_time']}s, exceeding the 3s threshold",
                priority=InsightPriority.HIGH,
                category="performance",
                metric_value=performance_data["avg_load_time"],
                threshold=3,
                recommendation="Optimize images, enable compression, and review resource loading",
                impact="High - Affects user experience and SEO",
                effort="Medium - Requires technical optimization",
                data_source="performance_metrics",
                timestamp=datetime.now()
            ))
        
        # Check Core Web Vitals
        cwv = performance_data.get("core_web_vitals", {})
        if cwv.get("lcp", {}).get("rating") == "poor":
            insights.append(Insight(
                title="Poor Largest Contentful Paint",
                description="LCP is in the poor range, affecting perceived load speed",
                priority=InsightPriority.HIGH,
                category="performance",
                metric_value=cwv["lcp"]["value"],
                threshold=2.5,
                recommendation="Optimize largest content element, use lazy loading",
                impact="High - Key metric for user experience",
                effort="Medium",
                data_source="core_web_vitals",
                timestamp=datetime.now()
            ))
        
        return insights
    
    def _analyze_health(self, health_data: Dict) -> List[Insight]:
        """Analyze health data for insights"""
        insights = []
        
        if health_data.get("broken_links", 0) > 5:
            insights.append(Insight(
                title="Multiple Broken Links Detected",
                description=f"{health_data['broken_links']} broken links found in documentation",
                priority=InsightPriority.CRITICAL,
                category="health",
                metric_value=health_data["broken_links"],
                threshold=5,
                recommendation="Run link checker and fix broken references immediately",
                impact="Critical - Degrades user experience and trust",
                effort="Low - Quick fixes required",
                data_source="health_monitor",
                timestamp=datetime.now()
            ))
        
        if health_data.get("quality_score", 100) < 85:
            insights.append(Insight(
                title="Documentation Quality Below Threshold",
                description=f"Quality score is {health_data['quality_score']}%, below the 85% threshold",
                priority=InsightPriority.HIGH,
                category="health",
                metric_value=health_data["quality_score"],
                threshold=85,
                recommendation="Review and update outdated content, add missing documentation",
                impact="High - Affects documentation effectiveness",
                effort="High - Requires content review",
                data_source="quality_analyzer",
                timestamp=datetime.now()
            ))
        
        return insights
    
    def _analyze_user_behavior(self, analytics_data: Dict) -> List[Insight]:
        """Analyze user behavior for insights"""
        insights = []
        
        bounce_rate = analytics_data.get("bounce_rate", 0)
        if bounce_rate > 0.4:
            insights.append(Insight(
                title="High Bounce Rate",
                description=f"Bounce rate is {bounce_rate*100:.1f}%, indicating users leave quickly",
                priority=InsightPriority.MEDIUM,
                category="user_behavior",
                metric_value=bounce_rate,
                threshold=0.4,
                recommendation="Improve landing pages, enhance navigation, add related content",
                impact="Medium - Affects engagement",
                effort="Medium - Content and UX improvements",
                data_source="analytics",
                timestamp=datetime.now()
            ))
        
        # Analyze top pages for opportunities
        top_pages = analytics_data.get("top_pages", [])
        if top_pages:
            insights.append(Insight(
                title="Popular Content Identified",
                description=f"Top page '{top_pages[0]['path']}' receives {top_pages[0]['views']} views",
                priority=InsightPriority.INFO,
                category="content",
                metric_value=top_pages[0]["views"],
                threshold=None,
                recommendation="Ensure top pages are optimized and link to related content",
                impact="Low - Optimization opportunity",
                effort="Low",
                data_source="analytics",
                timestamp=datetime.now()
            ))
        
        return insights
    
    def _analyze_errors(self, error_data: Dict) -> List[Insight]:
        """Analyze error data for insights"""
        insights = []
        
        error_rate = error_data.get("error_rate", 0)
        if error_rate > 0.01:
            insights.append(Insight(
                title="Elevated Error Rate",
                description=f"Error rate is {error_rate*100:.2f}%, above 1% threshold",
                priority=InsightPriority.HIGH,
                category="errors",
                metric_value=error_rate,
                threshold=0.01,
                recommendation="Investigate and fix top error types",
                impact="High - Affects reliability",
                effort="Medium - Debugging required",
                data_source="error_tracking",
                timestamp=datetime.now()
            ))
        
        return insights
    
    def _analyze_feedback(self, feedback_data: Dict) -> List[Insight]:
        """Analyze feedback data for insights"""
        insights = []
        
        sentiment = feedback_data.get("sentiment", {})
        if sentiment.get("negative", 0) > 0.15:
            insights.append(Insight(
                title="Negative Feedback Trend",
                description=f"{sentiment['negative']*100:.1f}% of feedback is negative",
                priority=InsightPriority.MEDIUM,
                category="feedback",
                metric_value=sentiment["negative"],
                threshold=0.15,
                recommendation="Review negative feedback and address common complaints",
                impact="Medium - Affects user satisfaction",
                effort="Medium - Content improvements needed",
                data_source="feedback_system",
                timestamp=datetime.now()
            ))
        
        avg_rating = feedback_data.get("avg_rating", 5)
        if avg_rating < 4:
            insights.append(Insight(
                title="Below-Target User Satisfaction",
                description=f"Average rating is {avg_rating:.1f}/5, below target of 4.0",
                priority=InsightPriority.MEDIUM,
                category="feedback",
                metric_value=avg_rating,
                threshold=4.0,
                recommendation="Analyze low-rated pages and improve content quality",
                impact="Medium - User satisfaction indicator",
                effort="Medium",
                data_source="feedback_system",
                timestamp=datetime.now()
            ))
        
        return insights
    
    def _priority_value(self, priority: InsightPriority) -> int:
        """Convert priority to numeric value for sorting"""
        priority_map = {
            InsightPriority.CRITICAL: 5,
            InsightPriority.HIGH: 4,
            InsightPriority.MEDIUM: 3,
            InsightPriority.LOW: 2,
            InsightPriority.INFO: 1
        }
        return priority_map.get(priority, 0)


class ReportScheduler:
    """Schedules and manages automated report generation"""
    
    def __init__(self, generator: ReportGenerator):
        self.generator = generator
        self.scheduled_jobs = {}
        
    async def start(self):
        """Start the report scheduler"""
        # Schedule configured reports
        config = self.generator.config.get("reports", {})
        
        for report_type, settings in config.items():
            if settings.get("enabled"):
                await self.schedule_report(
                    ReportType[report_type.upper()],
                    settings.get("schedule"),
                    settings.get("recipients", [])
                )
    
    async def schedule_report(self, report_type: ReportType, 
                            schedule: str, recipients: List[str]):
        """Schedule a report for automated generation"""
        # Would use a scheduling library like APScheduler
        logger.info(f"Scheduled {report_type.value} report: {schedule}")
    
    async def generate_and_send(self, report_type: ReportType, recipients: List[str]):
        """Generate and send a report"""
        report = await self.generator.generate_report(report_type)
        await self.send_report(report, recipients)
    
    async def send_report(self, report: Dict, recipients: List[str]):
        """Send report to recipients"""
        # Would implement email sending
        logger.info(f"Sending report to {len(recipients)} recipients")


# Initialize report system
async def initialize_reporting():
    """Initialize the reporting system"""
    generator = ReportGenerator()
    scheduler = ReportScheduler(generator)
    await scheduler.start()
    return generator, scheduler