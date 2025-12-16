# 📊 Multimedia Analytics

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **📊 Analytics**

![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)
![Type: Analytics](https://img.shields.io/badge/Type-Analytics-blue)
![Integration: Azure](https://img.shields.io/badge/Integration-Azure-0078D4)

## 📋 Overview

Comprehensive analytics and monitoring for multimedia content in the Cloud Scale Analytics documentation. Track engagement, performance, and usage patterns using Azure Application Insights and custom metrics.

## 🎯 Analytics Features

### Video Analytics

Track video engagement and completion rates:

```javascript
// Video tracking implementation
const videoPlayer = document.getElementById('tutorial-video');

// Track video start
videoPlayer.addEventListener('play', () => {
  trackEvent('video_play', {
    video_id: 'tutorial-01',
    video_title: 'Azure Synapse Setup',
    timestamp: new Date().toISOString()
  });
});

// Track video progress
videoPlayer.addEventListener('timeupdate', () => {
  const progress = (videoPlayer.currentTime / videoPlayer.duration) * 100;

  // Track 25%, 50%, 75%, 100% milestones
  const milestones = [25, 50, 75, 100];
  milestones.forEach(milestone => {
    if (progress >= milestone && !trackedMilestones[milestone]) {
      trackEvent('video_progress', {
        video_id: 'tutorial-01',
        milestone: milestone,
        time_elapsed: videoPlayer.currentTime
      });
      trackedMilestones[milestone] = true;
    }
  });
});

// Track video completion
videoPlayer.addEventListener('ended', () => {
  trackEvent('video_complete', {
    video_id: 'tutorial-01',
    duration_watched: videoPlayer.currentTime,
    completion_rate: 100
  });
});
```

### Image Analytics

Monitor image load performance and errors:

```javascript
// Image performance tracking
const images = document.querySelectorAll('img[data-track]');

images.forEach(img => {
  // Track successful load
  img.addEventListener('load', () => {
    trackEvent('image_loaded', {
      image_src: img.src,
      image_alt: img.alt,
      load_time: performance.now(),
      viewport_visible: isInViewport(img)
    });
  });

  // Track load errors
  img.addEventListener('error', () => {
    trackEvent('image_error', {
      image_src: img.src,
      image_alt: img.alt,
      error_type: 'load_failed'
    });
  });

  // Track lazy loading
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        trackEvent('image_viewed', {
          image_src: img.src,
          scroll_depth: window.scrollY
        });
      }
    });
  });
  observer.observe(img);
});
```

### Interactive Demo Analytics

Track demo usage and interactions:

```javascript
// Demo interaction tracking
class DemoAnalytics {
  constructor(demoId) {
    this.demoId = demoId;
    this.startTime = Date.now();
    this.interactions = 0;
  }

  trackInteraction(actionType, details) {
    this.interactions++;

    trackEvent('demo_interaction', {
      demo_id: this.demoId,
      action_type: actionType,
      interaction_count: this.interactions,
      time_since_start: Date.now() - this.startTime,
      ...details
    });
  }

  trackCompletion(success) {
    const duration = Date.now() - this.startTime;

    trackEvent('demo_completion', {
      demo_id: this.demoId,
      success: success,
      duration_seconds: duration / 1000,
      total_interactions: this.interactions
    });
  }
}

// Usage
const demoAnalytics = new DemoAnalytics('spark-notebook-demo');

document.getElementById('run-code').addEventListener('click', () => {
  demoAnalytics.trackInteraction('code_execution', {
    code_length: editor.getValue().length
  });
});
```

## 📈 Azure Application Insights Integration

### Setup

```bash
# Install Application Insights SDK
npm install @microsoft/applicationinsights-web

# Install Azure SDK
npm install @azure/monitor-query
```

### Configuration

```javascript
// appInsights.js
import { ApplicationInsights } from '@microsoft/applicationinsights-web';

const appInsights = new ApplicationInsights({
  config: {
    connectionString: process.env.APPINSIGHTS_CONNECTION_STRING,
    enableAutoRouteTracking: true,
    enableCorsCorrelation: true,
    enableRequestHeaderTracking: true,
    enableResponseHeaderTracking: true,
    disableFetchTracking: false,
    disableAjaxTracking: false
  }
});

appInsights.loadAppInsights();

// Track page views
appInsights.trackPageView({
  name: document.title,
  properties: {
    page_type: 'multimedia',
    content_type: 'tutorial'
  }
});

// Custom event tracking
export function trackEvent(eventName, properties) {
  appInsights.trackEvent({
    name: eventName,
    properties: {
      timestamp: new Date().toISOString(),
      user_id: getUserId(),
      session_id: getSessionId(),
      ...properties
    }
  });
}

// Track metrics
export function trackMetric(name, value, properties) {
  appInsights.trackMetric({
    name: name,
    average: value,
    properties: properties
  });
}

// Track exceptions
export function trackException(error, properties) {
  appInsights.trackException({
    exception: error,
    properties: properties
  });
}

export default appInsights;
```

### Usage Example

```javascript
import { trackEvent, trackMetric } from './appInsights';

// Track video performance
function trackVideoPerformance(videoElement) {
  const loadTime = performance.getEntriesByName(videoElement.src)[0];

  trackMetric('video_load_time', loadTime.duration, {
    video_id: videoElement.dataset.id,
    video_format: getVideoFormat(videoElement.src),
    file_size: videoElement.dataset.size
  });

  trackEvent('video_loaded', {
    video_id: videoElement.dataset.id,
    load_time_ms: loadTime.duration,
    auto_play: videoElement.autoplay
  });
}

// Track user engagement
function trackEngagement() {
  const timeOnPage = Date.now() - pageLoadTime;
  const scrollDepth = (window.scrollY / document.body.scrollHeight) * 100;

  trackMetric('time_on_page', timeOnPage / 1000);
  trackMetric('scroll_depth', scrollDepth);

  trackEvent('engagement_snapshot', {
    time_on_page_seconds: timeOnPage / 1000,
    scroll_depth_percent: scrollDepth,
    interactions: totalInteractions
  });
}
```

## 📊 Custom Dashboards

### Azure Dashboard Configuration

```json
{
  "dashboard": {
    "name": "CSA Multimedia Analytics",
    "tiles": [
      {
        "title": "Video Views",
        "query": "customEvents | where name == 'video_play' | summarize count() by bin(timestamp, 1h)",
        "visualization": "timechart"
      },
      {
        "title": "Video Completion Rate",
        "query": "let starts = customEvents | where name == 'video_play' | summarize starts=count() by video_id; let completes = customEvents | where name == 'video_complete' | summarize completes=count() by video_id; starts | join completes on video_id | extend completion_rate = (completes * 100.0) / starts",
        "visualization": "barchart"
      },
      {
        "title": "Interactive Demo Usage",
        "query": "customEvents | where name == 'demo_interaction' | summarize interactions=count() by demo_id, action_type",
        "visualization": "piechart"
      },
      {
        "title": "Image Load Performance",
        "query": "customMetrics | where name == 'image_load_time' | summarize avg(value) by bin(timestamp, 1h)",
        "visualization": "timechart"
      },
      {
        "title": "Error Rate",
        "query": "exceptions | union (customEvents | where name endswith '_error') | summarize count() by bin(timestamp, 1h)",
        "visualization": "timechart"
      }
    ]
  }
}
```

### Power BI Integration

```python
# Export analytics data to Power BI
from azure.monitor.query import LogsQueryClient
from azure.identity import DefaultAzureCredential
import pandas as pd

credential = DefaultAzureCredential()
client = LogsQueryClient(credential)

# Query Application Insights
query = """
customEvents
| where timestamp > ago(30d)
| where name in ('video_play', 'video_complete', 'demo_interaction')
| project timestamp, name, video_id=tostring(customDimensions.video_id),
          demo_id=tostring(customDimensions.demo_id),
          user_id=tostring(customDimensions.user_id)
"""

response = client.query_workspace(
    workspace_id="your-workspace-id",
    query=query,
    timespan="P30D"
)

# Convert to DataFrame
df = pd.DataFrame(response.tables[0].rows, columns=[col.name for col in response.tables[0].columns])

# Export to CSV for Power BI
df.to_csv('multimedia_analytics.csv', index=False)
```

## 📈 Key Metrics

### Video Metrics

```kusto
// Average video completion rate by video
customEvents
| where name in ('video_play', 'video_complete')
| extend video_id = tostring(customDimensions.video_id)
| summarize plays = countif(name == 'video_play'),
            completions = countif(name == 'video_complete')
  by video_id
| extend completion_rate = (completions * 100.0) / plays
| order by completion_rate desc
```

### Image Performance

```kusto
// Average image load time by format
customMetrics
| where name == 'image_load_time'
| extend format = tostring(customDimensions.image_format)
| summarize avg_load_time = avg(value) by format
| order by avg_load_time asc
```

### Demo Engagement

```kusto
// Demo interaction funnel
customEvents
| where name in ('demo_started', 'demo_interaction', 'demo_completion')
| extend demo_id = tostring(customDimensions.demo_id)
| summarize started = countif(name == 'demo_started'),
            interactions = countif(name == 'demo_interaction'),
            completed = countif(name == 'demo_completion')
  by demo_id
| extend interaction_rate = (interactions * 1.0) / started,
         completion_rate = (completed * 100.0) / started
```

### User Engagement

```kusto
// Average time on page by content type
pageViews
| extend content_type = tostring(customDimensions.content_type)
| summarize avg_duration = avg(duration) / 1000 by content_type
| order by avg_duration desc
```

## 🔍 Query Examples

### Most Popular Videos

```kusto
customEvents
| where name == 'video_play'
| extend video_title = tostring(customDimensions.video_title)
| summarize views = count() by video_title
| top 10 by views desc
```

### Video Drop-off Points

```kusto
customEvents
| where name == 'video_progress'
| extend video_id = tostring(customDimensions.video_id),
         milestone = toint(customDimensions.milestone)
| summarize viewers = dcount(user_Id) by video_id, milestone
| order by video_id, milestone asc
```

### Interactive Demo Success Rate

```kusto
customEvents
| where name == 'demo_completion'
| extend demo_id = tostring(customDimensions.demo_id),
         success = tobool(customDimensions.success)
| summarize total = count(),
            successful = countif(success == true)
  by demo_id
| extend success_rate = (successful * 100.0) / total
```

## 📊 Reporting

### Automated Reports

```javascript
// Generate weekly analytics report
const { LogsQueryClient } = require('@azure/monitor-query');
const { DefaultAzureCredential } = require('@azure/identity');

async function generateWeeklyReport() {
  const credential = new DefaultAzureCredential();
  const client = new LogsQueryClient(credential);

  const queries = {
    video_views: `customEvents | where name == 'video_play' | where timestamp > ago(7d) | summarize count()`,
    demo_completions: `customEvents | where name == 'demo_completion' | where timestamp > ago(7d) | summarize count()`,
    avg_engagement: `pageViews | where timestamp > ago(7d) | summarize avg(duration) / 1000`
  };

  const results = {};
  for (const [key, query] of Object.entries(queries)) {
    const response = await client.queryWorkspace(workspaceId, query, { duration: 'P7D' });
    results[key] = response.tables[0].rows[0][0];
  }

  // Send report via email or Teams
  await sendReport(results);
}
```

## 📚 Related Resources

- [Multimedia Overview](../README.md)
- [Production Guide](../production-guide/README.md)
- [Tools](../tools/README.md)
- [Azure Application Insights](https://azure.microsoft.com/services/monitor/)

---

*Last Updated: January 2025 | Version: 1.0.0*
