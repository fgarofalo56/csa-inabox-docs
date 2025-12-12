/**
 * Performance Monitoring System
 * Tracks and analyzes performance metrics for Cloud Scale Analytics documentation
 */

(function() {
    'use strict';

    // Configuration
    const config = {
        endpoint: '/api/performance',
        sampleRate: 1.0, // Sample 100% of users
        enableResourceTiming: true,
        enableUserTiming: true,
        enableLongTasks: true,
        enableLayoutShift: true,
        enableFirstInput: true,
        slowThreshold: 3000, // 3 seconds
        verySlowThreshold: 10000, // 10 seconds
        reportingInterval: 30000, // 30 seconds
        maxBatchSize: 50
    };

    // Core Web Vitals thresholds
    const webVitalsThresholds = {
        LCP: { good: 2500, poor: 4000 },
        FID: { good: 100, poor: 300 },
        CLS: { good: 0.1, poor: 0.25 },
        FCP: { good: 1800, poor: 3000 },
        TTFB: { good: 800, poor: 1800 },
        INP: { good: 200, poor: 500 }
    };

    // Performance Monitor Class
    class PerformanceMonitor {
        constructor() {
            this.metrics = {
                navigation: {},
                resources: [],
                userTimings: [],
                webVitals: {},
                customMetrics: {},
                errors: []
            };
            this.observers = {};
            this.sessionId = this.getSessionId();
            this.pageLoadId = this.generateId();
            this.batchQueue = [];
            this.init();
        }

        init() {
            if (!this.checkBrowserSupport()) {
                console.warn('Performance monitoring not fully supported in this browser');
                return;
            }

            // Wait for page load to collect initial metrics
            if (document.readyState === 'complete') {
                this.collectInitialMetrics();
            } else {
                window.addEventListener('load', () => this.collectInitialMetrics());
            }

            // Set up continuous monitoring
            this.setupObservers();
            this.setupEventListeners();
            this.startReportingCycle();
        }

        checkBrowserSupport() {
            return 'performance' in window && 
                   'PerformanceObserver' in window &&
                   'navigation' in performance;
        }

        getSessionId() {
            let sessionId = sessionStorage.getItem('perf-session-id');
            if (!sessionId) {
                sessionId = this.generateId();
                sessionStorage.setItem('perf-session-id', sessionId);
            }
            return sessionId;
        }

        generateId() {
            return Date.now().toString(36) + Math.random().toString(36).substr(2);
        }

        // Initial Metrics Collection
        collectInitialMetrics() {
            this.collectNavigationTiming();
            this.collectResourceTiming();
            this.collectPaintTiming();
            this.collectConnectionInfo();
            this.collectMemoryUsage();
            this.calculateMetrics();
        }

        collectNavigationTiming() {
            if (!performance.timing) return;

            const timing = performance.timing;
            const navigation = performance.navigation;

            this.metrics.navigation = {
                // Network timings
                dns: timing.domainLookupEnd - timing.domainLookupStart,
                tcp: timing.connectEnd - timing.connectStart,
                ssl: timing.connectEnd > timing.secureConnectionStart ? 
                     timing.connectEnd - timing.secureConnectionStart : 0,
                ttfb: timing.responseStart - timing.fetchStart,
                download: timing.responseEnd - timing.responseStart,
                
                // Document processing
                domParsing: timing.domInteractive - timing.domLoading,
                domContentLoaded: timing.domContentLoadedEventEnd - timing.domContentLoadedEventStart,
                domComplete: timing.domComplete - timing.domLoading,
                
                // Full page load
                loadComplete: timing.loadEventEnd - timing.fetchStart,
                
                // Navigation info
                type: ['navigate', 'reload', 'back_forward'][navigation.type] || 'unknown',
                redirectCount: navigation.redirectCount || 0,
                
                // Key milestones
                fetchStart: timing.fetchStart,
                domInteractive: timing.domInteractive - timing.fetchStart,
                firstByte: timing.responseStart - timing.fetchStart,
                lastByte: timing.responseEnd - timing.fetchStart,
                domReady: timing.domContentLoadedEventEnd - timing.fetchStart,
                windowLoad: timing.loadEventEnd - timing.fetchStart
            };
        }

        collectResourceTiming() {
            if (!config.enableResourceTiming || !performance.getEntriesByType) return;

            const resources = performance.getEntriesByType('resource');
            const resourceMetrics = resources.map(resource => {
                const isSlowResource = resource.duration > 1000;
                
                return {
                    name: resource.name.split('?')[0], // Remove query params
                    type: this.getResourceType(resource),
                    size: resource.transferSize || 0,
                    duration: Math.round(resource.duration),
                    startTime: Math.round(resource.startTime),
                    
                    // Detailed timings for slow resources
                    ...(isSlowResource && {
                        dns: Math.round(resource.domainLookupEnd - resource.domainLookupStart),
                        tcp: Math.round(resource.connectEnd - resource.connectStart),
                        ttfb: Math.round(resource.responseStart - resource.fetchStart),
                        download: Math.round(resource.responseEnd - resource.responseStart)
                    }),
                    
                    // Cache info
                    cached: resource.transferSize === 0 && resource.decodedBodySize > 0,
                    protocol: resource.nextHopProtocol,
                    
                    // Performance flags
                    isSlow: isSlowResource,
                    isLarge: resource.transferSize > 500000, // > 500KB
                    isCritical: this.isResourceCritical(resource)
                };
            });

            // Group resources by type
            this.metrics.resources = {
                all: resourceMetrics,
                byType: this.groupResourcesByType(resourceMetrics),
                summary: this.summarizeResources(resourceMetrics)
            };
        }

        getResourceType(resource) {
            const url = resource.name;
            const mimeType = resource.initiatorType;
            
            if (mimeType === 'script' || url.endsWith('.js')) return 'javascript';
            if (mimeType === 'css' || url.endsWith('.css')) return 'stylesheet';
            if (mimeType === 'img' || /\.(jpg|jpeg|png|gif|svg|webp|ico)$/i.test(url)) return 'image';
            if (mimeType === 'xmlhttprequest' || mimeType === 'fetch') return 'api';
            if (/\.(woff2?|ttf|otf|eot)$/i.test(url)) return 'font';
            if (/\.(mp4|webm|ogg|mp3|wav)$/i.test(url)) return 'media';
            
            return mimeType || 'other';
        }

        isResourceCritical(resource) {
            // Check if resource is render-blocking
            const isCriticalType = ['script', 'css', 'font'].includes(resource.initiatorType);
            const isEarlyResource = resource.startTime < 1000;
            return isCriticalType && isEarlyResource;
        }

        groupResourcesByType(resources) {
            return resources.reduce((acc, resource) => {
                const type = resource.type;
                if (!acc[type]) acc[type] = [];
                acc[type].push(resource);
                return acc;
            }, {});
        }

        summarizeResources(resources) {
            const summary = {
                total: resources.length,
                totalSize: resources.reduce((sum, r) => sum + r.size, 0),
                totalDuration: resources.reduce((sum, r) => sum + r.duration, 0),
                cached: resources.filter(r => r.cached).length,
                slow: resources.filter(r => r.isSlow).length,
                large: resources.filter(r => r.isLarge).length,
                critical: resources.filter(r => r.isCritical).length
            };

            // Calculate percentages
            summary.cacheRate = summary.total > 0 ? (summary.cached / summary.total * 100).toFixed(1) : 0;
            summary.avgDuration = summary.total > 0 ? Math.round(summary.totalDuration / summary.total) : 0;
            summary.avgSize = summary.total > 0 ? Math.round(summary.totalSize / summary.total) : 0;

            return summary;
        }

        collectPaintTiming() {
            if (!performance.getEntriesByType) return;

            const paintEntries = performance.getEntriesByType('paint');
            const paintMetrics = {};

            paintEntries.forEach(entry => {
                if (entry.name === 'first-paint') {
                    paintMetrics.fp = Math.round(entry.startTime);
                } else if (entry.name === 'first-contentful-paint') {
                    paintMetrics.fcp = Math.round(entry.startTime);
                }
            });

            this.metrics.paint = paintMetrics;
        }

        collectConnectionInfo() {
            const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
            
            if (connection) {
                this.metrics.connection = {
                    effectiveType: connection.effectiveType,
                    downlink: connection.downlink,
                    rtt: connection.rtt,
                    saveData: connection.saveData || false
                };
            }
        }

        collectMemoryUsage() {
            if (performance.memory) {
                this.metrics.memory = {
                    usedJSHeapSize: Math.round(performance.memory.usedJSHeapSize / 1048576), // Convert to MB
                    totalJSHeapSize: Math.round(performance.memory.totalJSHeapSize / 1048576),
                    jsHeapSizeLimit: Math.round(performance.memory.jsHeapSizeLimit / 1048576)
                };
            }
        }

        // Observer Setup
        setupObservers() {
            this.observeLCP();
            this.observeFID();
            this.observeCLS();
            this.observeLongTasks();
            this.observeLayoutShift();
            this.observeINP();
        }

        observeLCP() {
            if (!config.enabledFeatures?.webVitals) return;

            try {
                this.observers.lcp = new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    const lastEntry = entries[entries.length - 1];
                    
                    this.metrics.webVitals.lcp = {
                        value: Math.round(lastEntry.renderTime || lastEntry.loadTime),
                        rating: this.getRating('LCP', lastEntry.renderTime || lastEntry.loadTime),
                        element: lastEntry.element?.tagName,
                        url: lastEntry.url,
                        size: lastEntry.size
                    };
                });
                
                this.observers.lcp.observe({ entryTypes: ['largest-contentful-paint'] });
            } catch (e) {
                console.warn('LCP observation not supported');
            }
        }

        observeFID() {
            if (!config.enabledFeatures?.webVitals) return;

            try {
                this.observers.fid = new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    const firstEntry = entries[0];
                    
                    if (firstEntry && !this.metrics.webVitals.fid) {
                        this.metrics.webVitals.fid = {
                            value: Math.round(firstEntry.processingStart - firstEntry.startTime),
                            rating: this.getRating('FID', firstEntry.processingStart - firstEntry.startTime),
                            eventType: firstEntry.name,
                            target: firstEntry.target?.tagName
                        };
                    }
                });
                
                this.observers.fid.observe({ entryTypes: ['first-input'] });
            } catch (e) {
                console.warn('FID observation not supported');
            }
        }

        observeCLS() {
            if (!config.enabledFeatures?.webVitals) return;

            let clsValue = 0;
            let clsEntries = [];

            try {
                this.observers.cls = new PerformanceObserver((list) => {
                    list.getEntries().forEach(entry => {
                        if (!entry.hadRecentInput) {
                            clsValue += entry.value;
                            clsEntries.push({
                                value: entry.value,
                                sources: entry.sources?.map(source => ({
                                    node: source.node?.tagName,
                                    previousRect: source.previousRect,
                                    currentRect: source.currentRect
                                }))
                            });
                        }
                    });
                    
                    this.metrics.webVitals.cls = {
                        value: Math.round(clsValue * 1000) / 1000,
                        rating: this.getRating('CLS', clsValue),
                        entries: clsEntries.slice(-5) // Keep last 5 shifts
                    };
                });
                
                this.observers.cls.observe({ entryTypes: ['layout-shift'] });
            } catch (e) {
                console.warn('CLS observation not supported');
            }
        }

        observeLongTasks() {
            if (!config.enableLongTasks) return;

            try {
                this.observers.longTasks = new PerformanceObserver((list) => {
                    list.getEntries().forEach(entry => {
                        if (entry.duration > 50) {
                            if (!this.metrics.longTasks) this.metrics.longTasks = [];
                            
                            this.metrics.longTasks.push({
                                duration: Math.round(entry.duration),
                                startTime: Math.round(entry.startTime),
                                attribution: entry.attribution?.map(attr => ({
                                    name: attr.name,
                                    container: attr.containerType,
                                    src: attr.containerSrc
                                }))
                            });
                        }
                    });
                });
                
                this.observers.longTasks.observe({ entryTypes: ['longtask'] });
            } catch (e) {
                console.warn('Long task observation not supported');
            }
        }

        observeLayoutShift() {
            if (!config.enableLayoutShift) return;

            try {
                this.observers.layoutShift = new PerformanceObserver((list) => {
                    list.getEntries().forEach(entry => {
                        if (entry.value > 0.01 && !entry.hadRecentInput) {
                            if (!this.metrics.layoutShifts) this.metrics.layoutShifts = [];
                            
                            this.metrics.layoutShifts.push({
                                value: entry.value,
                                startTime: Math.round(entry.startTime),
                                sources: entry.sources?.map(source => source.node?.tagName).filter(Boolean)
                            });
                        }
                    });
                });
                
                this.observers.layoutShift.observe({ entryTypes: ['layout-shift'] });
            } catch (e) {
                console.warn('Layout shift observation not supported');
            }
        }

        observeINP() {
            // Interaction to Next Paint (INP) - newer metric
            if (!config.enabledFeatures?.webVitals) return;

            const interactions = [];

            try {
                this.observers.inp = new PerformanceObserver((list) => {
                    list.getEntries().forEach(entry => {
                        if (entry.entryType === 'event' && entry.duration > 0) {
                            interactions.push({
                                duration: entry.duration,
                                processingTime: entry.processingEnd - entry.processingStart,
                                presentationDelay: entry.startTime + entry.duration - entry.processingEnd
                            });
                            
                            // Calculate P98 of interactions
                            const sorted = [...interactions].sort((a, b) => b.duration - a.duration);
                            const p98Index = Math.floor(sorted.length * 0.02);
                            const inp = sorted[p98Index]?.duration || 0;
                            
                            this.metrics.webVitals.inp = {
                                value: Math.round(inp),
                                rating: this.getRating('INP', inp),
                                count: interactions.length
                            };
                        }
                    });
                });
                
                this.observers.inp.observe({ entryTypes: ['event'], buffered: true, durationThreshold: 40 });
            } catch (e) {
                console.warn('INP observation not supported');
            }
        }

        // Event Listeners
        setupEventListeners() {
            // Track visibility changes
            document.addEventListener('visibilitychange', () => {
                if (document.hidden) {
                    this.reportMetrics(true); // Force report when page is hidden
                }
            });

            // Track page unload
            window.addEventListener('beforeunload', () => {
                this.finalReport();
            });

            // Track errors
            window.addEventListener('error', (event) => {
                this.trackError(event);
            });

            // Track unhandled promise rejections
            window.addEventListener('unhandledrejection', (event) => {
                this.trackError({
                    message: event.reason?.message || event.reason,
                    type: 'unhandledrejection'
                });
            });
        }

        trackError(error) {
            this.metrics.errors.push({
                message: error.message || error.reason,
                filename: error.filename,
                line: error.lineno,
                column: error.colno,
                stack: error.error?.stack,
                timestamp: Date.now(),
                type: error.type || 'error'
            });
        }

        // Metrics Calculation
        calculateMetrics() {
            this.calculateSpeedIndex();
            this.calculateTimeToInteractive();
            this.calculateFirstMeaningfulPaint();
            this.assessPerformance();
        }

        calculateSpeedIndex() {
            // Simplified Speed Index calculation
            // In production, use more sophisticated algorithm
            const fcp = this.metrics.paint?.fcp || 0;
            const lcp = this.metrics.webVitals?.lcp?.value || 0;
            
            if (fcp && lcp) {
                this.metrics.customMetrics.speedIndex = Math.round((fcp + lcp) / 2);
            }
        }

        calculateTimeToInteractive() {
            // TTI approximation
            const domInteractive = this.metrics.navigation?.domInteractive || 0;
            const longTasksBeforeInteractive = (this.metrics.longTasks || [])
                .filter(task => task.startTime < domInteractive)
                .reduce((sum, task) => sum + task.duration, 0);
            
            this.metrics.customMetrics.tti = domInteractive + longTasksBeforeInteractive;
        }

        calculateFirstMeaningfulPaint() {
            // FMP approximation (between FCP and LCP)
            const fcp = this.metrics.paint?.fcp || 0;
            const lcp = this.metrics.webVitals?.lcp?.value || 0;
            
            if (fcp && lcp) {
                this.metrics.customMetrics.fmp = Math.round(fcp + (lcp - fcp) * 0.3);
            }
        }

        assessPerformance() {
            const assessment = {
                score: 100,
                issues: [],
                recommendations: []
            };

            // Check TTFB
            if (this.metrics.navigation?.ttfb > webVitalsThresholds.TTFB.poor) {
                assessment.score -= 10;
                assessment.issues.push('Slow server response time');
                assessment.recommendations.push('Optimize server response time');
            }

            // Check LCP
            const lcpValue = this.metrics.webVitals?.lcp?.value;
            if (lcpValue > webVitalsThresholds.LCP.poor) {
                assessment.score -= 15;
                assessment.issues.push('Poor Largest Contentful Paint');
                assessment.recommendations.push('Optimize largest content element loading');
            }

            // Check FID
            const fidValue = this.metrics.webVitals?.fid?.value;
            if (fidValue > webVitalsThresholds.FID.poor) {
                assessment.score -= 15;
                assessment.issues.push('Poor First Input Delay');
                assessment.recommendations.push('Reduce JavaScript execution time');
            }

            // Check CLS
            const clsValue = this.metrics.webVitals?.cls?.value;
            if (clsValue > webVitalsThresholds.CLS.poor) {
                assessment.score -= 10;
                assessment.issues.push('High Cumulative Layout Shift');
                assessment.recommendations.push('Reserve space for dynamic content');
            }

            // Check resource loading
            const slowResources = this.metrics.resources?.summary?.slow || 0;
            if (slowResources > 5) {
                assessment.score -= 10;
                assessment.issues.push(`${slowResources} slow loading resources`);
                assessment.recommendations.push('Optimize resource loading');
            }

            // Check total page weight
            const totalSize = this.metrics.resources?.summary?.totalSize || 0;
            if (totalSize > 3000000) { // 3MB
                assessment.score -= 10;
                assessment.issues.push('Large page size');
                assessment.recommendations.push('Reduce page weight');
            }

            assessment.score = Math.max(0, assessment.score);
            assessment.rating = this.getPerformanceRating(assessment.score);
            
            this.metrics.assessment = assessment;
        }

        getRating(metric, value) {
            const thresholds = webVitalsThresholds[metric];
            if (!thresholds) return 'unknown';
            
            if (value <= thresholds.good) return 'good';
            if (value <= thresholds.poor) return 'needs-improvement';
            return 'poor';
        }

        getPerformanceRating(score) {
            if (score >= 90) return 'excellent';
            if (score >= 70) return 'good';
            if (score >= 50) return 'needs-improvement';
            return 'poor';
        }

        // Reporting
        startReportingCycle() {
            setInterval(() => {
                this.reportMetrics();
            }, config.reportingInterval);
        }

        reportMetrics(immediate = false) {
            const report = this.prepareReport();
            
            if (immediate) {
                this.sendReport(report);
            } else {
                this.batchQueue.push(report);
                
                if (this.batchQueue.length >= config.maxBatchSize) {
                    this.flushBatch();
                }
            }
        }

        prepareReport() {
            return {
                sessionId: this.sessionId,
                pageLoadId: this.pageLoadId,
                timestamp: new Date().toISOString(),
                url: window.location.href,
                metrics: {
                    navigation: this.metrics.navigation,
                    paint: this.metrics.paint,
                    webVitals: this.metrics.webVitals,
                    resources: this.metrics.resources?.summary,
                    custom: this.metrics.customMetrics,
                    assessment: this.metrics.assessment
                },
                errors: this.metrics.errors.slice(-10), // Last 10 errors
                connection: this.metrics.connection,
                memory: this.metrics.memory,
                viewport: {
                    width: window.innerWidth,
                    height: window.innerHeight
                },
                screen: {
                    width: window.screen.width,
                    height: window.screen.height
                }
            };
        }

        flushBatch() {
            if (this.batchQueue.length === 0) return;
            
            const batch = this.batchQueue.splice(0, config.maxBatchSize);
            this.sendReport({ batch });
        }

        sendReport(data) {
            // Use sendBeacon for reliability
            if (navigator.sendBeacon) {
                navigator.sendBeacon(config.endpoint, JSON.stringify(data));
            } else {
                // Fallback to fetch
                fetch(config.endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                    keepalive: true
                }).catch(error => {
                    console.error('Failed to send performance data:', error);
                });
            }
        }

        finalReport() {
            // Send final metrics when page unloads
            this.reportMetrics(true);
            
            // Clean up observers
            Object.values(this.observers).forEach(observer => {
                try {
                    observer.disconnect();
                } catch (e) {}
            });
        }

        // Public API
        mark(name) {
            if (performance.mark) {
                performance.mark(name);
                if (!this.metrics.userTimings) this.metrics.userTimings = [];
                this.metrics.userTimings.push({ type: 'mark', name, time: performance.now() });
            }
        }

        measure(name, startMark, endMark) {
            if (performance.measure) {
                try {
                    performance.measure(name, startMark, endMark);
                    const measure = performance.getEntriesByName(name, 'measure')[0];
                    if (measure) {
                        if (!this.metrics.userTimings) this.metrics.userTimings = [];
                        this.metrics.userTimings.push({
                            type: 'measure',
                            name,
                            duration: measure.duration,
                            startTime: measure.startTime
                        });
                    }
                } catch (e) {
                    console.warn(`Failed to measure ${name}:`, e);
                }
            }
        }

        addCustomMetric(name, value) {
            this.metrics.customMetrics[name] = value;
        }
    }

    // Initialize performance monitoring
    window.performanceMonitor = new PerformanceMonitor();

    // Public API
    window.PerformanceAPI = {
        mark: (name) => window.performanceMonitor.mark(name),
        measure: (name, start, end) => window.performanceMonitor.measure(name, start, end),
        addMetric: (name, value) => window.performanceMonitor.addCustomMetric(name, value),
        getMetrics: () => window.performanceMonitor.metrics,
        report: () => window.performanceMonitor.reportMetrics(true)
    };
})();