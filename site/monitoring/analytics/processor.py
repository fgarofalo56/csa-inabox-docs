"""
Documentation Analytics Processor
Server-side processing for documentation analytics data
"""

import json
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
from enum import Enum
import asyncio
import aiohttp
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventType(Enum):
    """Analytics event types"""
    PAGE_VIEW = "page_view"
    SCROLL_DEPTH = "scroll_depth"
    SEARCH = "search"
    SEARCH_RESULT_CLICK = "search_result_click"
    LINK_CLICK = "link_click"
    PAGE_TIME = "page_time"
    JAVASCRIPT_ERROR = "javascript_error"
    BROKEN_LINK = "broken_link"
    PERFORMANCE = "performance"
    WEB_VITALS = "web_vitals"
    FEEDBACK = "feedback"
    CUSTOM = "custom"


@dataclass
class AnalyticsEvent:
    """Analytics event data structure"""
    event_id: str
    event_type: EventType
    timestamp: datetime
    session_id: str
    user_id: str
    page_path: str
    data: Dict[str, Any]
    context: Dict[str, Any]
    processed: bool = False


class AnalyticsProcessor:
    """Process and analyze documentation analytics data"""
    
    def __init__(self, config_path: str = "config/analytics.yml"):
        self.config = self._load_config(config_path)
        self.events_queue = asyncio.Queue()
        self.metrics = defaultdict(lambda: defaultdict(int))
        self.user_journeys = defaultdict(list)
        self.search_analytics = defaultdict(lambda: {"queries": [], "clicks": []})
        self.performance_data = []
        self.feedback_data = []
        self.error_logs = []
        
    def _load_config(self, config_path: str) -> Dict:
        """Load analytics configuration"""
        config_file = Path(config_path)
        if config_file.exists():
            import yaml
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default analytics configuration"""
        return {
            "privacy": {
                "anonymize_ip": True,
                "hash_user_ids": True,
                "retention_days": 90,
                "gdpr_compliant": True
            },
            "processing": {
                "batch_size": 100,
                "flush_interval": 60,
                "max_queue_size": 10000
            },
            "storage": {
                "type": "sqlite",
                "path": "data/analytics.db"
            },
            "features": {
                "real_time": True,
                "journey_mapping": True,
                "search_analytics": True,
                "performance_monitoring": True
            }
        }
    
    async def process_event(self, raw_event: Dict) -> Optional[AnalyticsEvent]:
        """Process incoming analytics event"""
        try:
            # Validate and sanitize event
            if not self._validate_event(raw_event):
                return None
            
            # Apply privacy rules
            event = self._apply_privacy_rules(raw_event)
            
            # Create structured event
            analytics_event = AnalyticsEvent(
                event_id=self._generate_event_id(event),
                event_type=EventType(event.get('event')),
                timestamp=datetime.fromisoformat(event.get('timestamp')),
                session_id=event.get('context', {}).get('sessionId'),
                user_id=self._hash_user_id(event.get('context', {}).get('userId')),
                page_path=event.get('page', ''),
                data=event,
                context=event.get('context', {})
            )
            
            # Add to processing queue
            await self.events_queue.put(analytics_event)
            
            # Process specific event types
            await self._process_by_type(analytics_event)
            
            return analytics_event
            
        except Exception as e:
            logger.error(f"Error processing event: {e}")
            return None
    
    def _validate_event(self, event: Dict) -> bool:
        """Validate event structure and required fields"""
        required_fields = ['event', 'timestamp']
        return all(field in event for field in required_fields)
    
    def _apply_privacy_rules(self, event: Dict) -> Dict:
        """Apply privacy rules to event data"""
        if self.config['privacy']['anonymize_ip']:
            # Remove IP address if present
            if 'ip' in event.get('context', {}):
                del event['context']['ip']
        
        # Sanitize user data
        if 'context' in event:
            context = event['context']
            # Anonymize user agent
            if 'userAgent' in context:
                context['userAgent'] = self._anonymize_user_agent(context['userAgent'])
        
        return event
    
    def _hash_user_id(self, user_id: str) -> str:
        """Hash user ID for privacy"""
        if not user_id or not self.config['privacy']['hash_user_ids']:
            return user_id
        return hashlib.sha256(user_id.encode()).hexdigest()[:16]
    
    def _generate_event_id(self, event: Dict) -> str:
        """Generate unique event ID"""
        content = json.dumps(event, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()
    
    def _anonymize_user_agent(self, user_agent: str) -> str:
        """Anonymize user agent string"""
        # Already anonymized on client side, but double-check
        import re
        # Remove specific version numbers
        patterns = [
            (r'Chrome/[\d.]+', 'Chrome'),
            (r'Firefox/[\d.]+', 'Firefox'),
            (r'Safari/[\d.]+', 'Safari'),
            (r'Edge/[\d.]+', 'Edge'),
        ]
        for pattern, replacement in patterns:
            user_agent = re.sub(pattern, replacement, user_agent)
        return user_agent
    
    async def _process_by_type(self, event: AnalyticsEvent):
        """Process event based on its type"""
        if event.event_type == EventType.PAGE_VIEW:
            await self._process_page_view(event)
        elif event.event_type == EventType.SEARCH:
            await self._process_search(event)
        elif event.event_type == EventType.LINK_CLICK:
            await self._process_link_click(event)
        elif event.event_type == EventType.PERFORMANCE:
            await self._process_performance(event)
        elif event.event_type == EventType.FEEDBACK:
            await self._process_feedback(event)
        elif event.event_type == EventType.JAVASCRIPT_ERROR:
            await self._process_error(event)
    
    async def _process_page_view(self, event: AnalyticsEvent):
        """Process page view event"""
        page_path = event.page_path
        section = event.data.get('page', {}).get('section', 'unknown')
        
        # Update metrics
        self.metrics['pages'][page_path] += 1
        self.metrics['sections'][section] += 1
        self.metrics['daily'][datetime.now().date().isoformat()] += 1
        
        # Track unique sessions
        self.metrics['unique_sessions'].add(event.session_id)
        
        # Update user journey
        if self.config['features']['journey_mapping']:
            self.user_journeys[event.session_id].append({
                'path': page_path,
                'timestamp': event.timestamp,
                'referrer': event.data.get('page', {}).get('referrer')
            })
    
    async def _process_search(self, event: AnalyticsEvent):
        """Process search event"""
        if not self.config['features']['search_analytics']:
            return
        
        query = event.data.get('query', '')
        results_count = event.data.get('resultsCount', 0)
        
        self.search_analytics[event.session_id]['queries'].append({
            'query': query,
            'results_count': results_count,
            'timestamp': event.timestamp,
            'page': event.page_path
        })
        
        # Track zero-result searches
        if results_count == 0:
            self.metrics['zero_result_searches'][query] += 1
    
    async def _process_link_click(self, event: AnalyticsEvent):
        """Process link click event"""
        link_data = event.data.get('link', {})
        
        if link_data.get('isExternal'):
            self.metrics['external_links'][link_data.get('href')] += 1
        else:
            # Update journey if internal link
            if self.config['features']['journey_mapping']:
                self.user_journeys[event.session_id].append({
                    'from': event.page_path,
                    'to': link_data.get('href'),
                    'timestamp': event.timestamp
                })
    
    async def _process_performance(self, event: AnalyticsEvent):
        """Process performance event"""
        if not self.config['features']['performance_monitoring']:
            return
        
        metrics = event.data.get('metrics', {})
        self.performance_data.append({
            'page': event.page_path,
            'timestamp': event.timestamp,
            'metrics': metrics,
            'session_id': event.session_id
        })
        
        # Track slow pages
        load_time = metrics.get('loadComplete', 0)
        if load_time > 3000:  # More than 3 seconds
            self.metrics['slow_pages'][event.page_path] += 1
    
    async def _process_feedback(self, event: AnalyticsEvent):
        """Process feedback event"""
        feedback = event.data.get('feedback', {})
        self.feedback_data.append({
            'page': event.page_path,
            'timestamp': event.timestamp,
            'type': feedback.get('type'),
            'value': feedback.get('value'),
            'comment': feedback.get('comment'),
            'session_id': event.session_id
        })
    
    async def _process_error(self, event: AnalyticsEvent):
        """Process error event"""
        error = event.data.get('error', {})
        self.error_logs.append({
            'page': event.page_path,
            'timestamp': event.timestamp,
            'error': error,
            'session_id': event.session_id
        })
    
    def get_analytics_summary(self) -> Dict:
        """Generate analytics summary"""
        return {
            'overview': {
                'total_page_views': sum(self.metrics['pages'].values()),
                'unique_sessions': len(self.metrics['unique_sessions']),
                'top_pages': self._get_top_items(self.metrics['pages'], 10),
                'top_sections': self._get_top_items(self.metrics['sections'], 5)
            },
            'search': {
                'total_searches': sum(len(s['queries']) for s in self.search_analytics.values()),
                'zero_result_queries': dict(self.metrics['zero_result_searches']),
                'popular_queries': self._get_popular_searches()
            },
            'performance': {
                'slow_pages': dict(self.metrics['slow_pages']),
                'average_load_time': self._calculate_average_load_time(),
                'core_web_vitals': self._get_core_web_vitals()
            },
            'user_behavior': {
                'average_session_duration': self._calculate_session_duration(),
                'pages_per_session': self._calculate_pages_per_session(),
                'bounce_rate': self._calculate_bounce_rate(),
                'user_flows': self._analyze_user_flows()
            },
            'feedback': {
                'total_feedback': len(self.feedback_data),
                'satisfaction_score': self._calculate_satisfaction_score(),
                'recent_feedback': self.feedback_data[-10:]
            },
            'errors': {
                'total_errors': len(self.error_logs),
                'recent_errors': self.error_logs[-10:],
                'error_pages': self._get_error_pages()
            }
        }
    
    def _get_top_items(self, items: Dict, limit: int) -> List:
        """Get top items by count"""
        sorted_items = sorted(items.items(), key=lambda x: x[1], reverse=True)
        return [{'name': k, 'count': v} for k, v in sorted_items[:limit]]
    
    def _get_popular_searches(self) -> List:
        """Get most popular search queries"""
        all_queries = []
        for session in self.search_analytics.values():
            all_queries.extend([q['query'] for q in session['queries']])
        
        query_counts = defaultdict(int)
        for query in all_queries:
            query_counts[query] += 1
        
        return self._get_top_items(query_counts, 10)
    
    def _calculate_average_load_time(self) -> float:
        """Calculate average page load time"""
        if not self.performance_data:
            return 0
        
        load_times = [p['metrics'].get('loadComplete', 0) for p in self.performance_data]
        return sum(load_times) / len(load_times) if load_times else 0
    
    def _get_core_web_vitals(self) -> Dict:
        """Get Core Web Vitals metrics"""
        # This would aggregate LCP, FID, CLS data
        return {
            'lcp': {'good': 0, 'needs_improvement': 0, 'poor': 0},
            'fid': {'good': 0, 'needs_improvement': 0, 'poor': 0},
            'cls': {'good': 0, 'needs_improvement': 0, 'poor': 0}
        }
    
    def _calculate_session_duration(self) -> float:
        """Calculate average session duration"""
        durations = []
        for journey in self.user_journeys.values():
            if len(journey) > 1:
                duration = (journey[-1]['timestamp'] - journey[0]['timestamp']).total_seconds()
                durations.append(duration)
        
        return sum(durations) / len(durations) if durations else 0
    
    def _calculate_pages_per_session(self) -> float:
        """Calculate average pages per session"""
        page_counts = [len(journey) for journey in self.user_journeys.values()]
        return sum(page_counts) / len(page_counts) if page_counts else 0
    
    def _calculate_bounce_rate(self) -> float:
        """Calculate bounce rate (single page sessions)"""
        if not self.user_journeys:
            return 0
        
        single_page = sum(1 for journey in self.user_journeys.values() if len(journey) == 1)
        return (single_page / len(self.user_journeys)) * 100
    
    def _analyze_user_flows(self) -> List:
        """Analyze common user navigation flows"""
        flows = defaultdict(int)
        
        for journey in self.user_journeys.values():
            for i in range(len(journey) - 1):
                flow = f"{journey[i]['path']} -> {journey[i+1].get('to', journey[i+1]['path'])}"
                flows[flow] += 1
        
        return self._get_top_items(flows, 10)
    
    def _calculate_satisfaction_score(self) -> float:
        """Calculate average satisfaction score from feedback"""
        if not self.feedback_data:
            return 0
        
        scores = [f['value'] for f in self.feedback_data if isinstance(f.get('value'), (int, float))]
        return sum(scores) / len(scores) if scores else 0
    
    def _get_error_pages(self) -> Dict:
        """Get pages with most errors"""
        error_pages = defaultdict(int)
        for error in self.error_logs:
            error_pages[error['page']] += 1
        return dict(error_pages)
    
    async def cleanup_old_data(self):
        """Remove data older than retention period"""
        retention_days = self.config['privacy']['retention_days']
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        # Clean up old events
        # This would be implemented based on storage backend
        logger.info(f"Cleaning up data older than {cutoff_date}")
    
    async def export_data(self, format: str = "json") -> str:
        """Export analytics data for analysis"""
        summary = self.get_analytics_summary()
        
        if format == "json":
            return json.dumps(summary, indent=2, default=str)
        elif format == "csv":
            # Convert to CSV format
            import csv
            import io
            output = io.StringIO()
            writer = csv.writer(output)
            # Write CSV data
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported export format: {format}")


class AnalyticsAPI:
    """REST API for analytics data"""
    
    def __init__(self, processor: AnalyticsProcessor):
        self.processor = processor
    
    async def handle_event(self, request_data: Dict) -> Dict:
        """Handle incoming analytics event"""
        event = await self.processor.process_event(request_data)
        if event:
            return {"status": "success", "event_id": event.event_id}
        return {"status": "error", "message": "Invalid event data"}
    
    async def get_summary(self, params: Dict = None) -> Dict:
        """Get analytics summary"""
        return self.processor.get_analytics_summary()
    
    async def get_realtime(self) -> Dict:
        """Get real-time analytics data"""
        # Return last 5 minutes of data
        return {
            "active_users": len(self.processor.metrics['unique_sessions']),
            "current_page_views": sum(self.processor.metrics['pages'].values()),
            "recent_searches": self.processor._get_popular_searches()[:5],
            "current_errors": len(self.processor.error_logs)
        }
    
    async def export(self, format: str = "json") -> str:
        """Export analytics data"""
        return await self.processor.export_data(format)