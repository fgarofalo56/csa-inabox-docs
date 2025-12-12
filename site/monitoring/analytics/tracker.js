/**
 * Documentation Analytics Tracker
 * Privacy-compliant analytics for Cloud Scale Analytics documentation
 */

(function() {
    'use strict';

    // Configuration
    const config = {
        endpoint: '/api/analytics',
        sessionTimeout: 30 * 60 * 1000, // 30 minutes
        scrollDepthThresholds: [25, 50, 75, 100],
        privacyMode: 'strict', // 'strict', 'balanced', 'full'
        enabledFeatures: {
            pageViews: true,
            userJourney: true,
            searchTracking: true,
            scrollDepth: true,
            timeOnPage: true,
            feedback: true
        }
    };

    // Analytics Tracker Class
    class DocumentationAnalytics {
        constructor() {
            this.sessionId = this.getOrCreateSession();
            this.userId = this.getAnonymousUserId();
            this.pageStartTime = Date.now();
            this.scrollDepthReached = 0;
            this.searchQueries = [];
            this.journey = [];
            this.events = [];
            
            this.init();
        }

        init() {
            if (!this.checkConsent()) {
                console.log('Analytics disabled - no user consent');
                return;
            }

            this.trackPageView();
            this.setupScrollTracking();
            this.setupSearchTracking();
            this.setupLinkTracking();
            this.setupVisibilityTracking();
            this.setupErrorTracking();
            this.setupPerformanceTracking();
        }

        // Privacy & Consent Management
        checkConsent() {
            const consent = localStorage.getItem('analytics-consent');
            return consent === 'granted' || (config.privacyMode === 'balanced' && consent !== 'denied');
        }

        requestConsent() {
            const banner = document.createElement('div');
            banner.className = 'consent-banner';
            banner.innerHTML = `
                <div class="consent-content">
                    <p>We use privacy-compliant analytics to improve documentation. No personal data is collected.</p>
                    <div class="consent-actions">
                        <button onclick="docAnalytics.acceptConsent()">Accept</button>
                        <button onclick="docAnalytics.declineConsent()">Decline</button>
                        <a href="/privacy-policy">Learn More</a>
                    </div>
                </div>
            `;
            document.body.appendChild(banner);
        }

        acceptConsent() {
            localStorage.setItem('analytics-consent', 'granted');
            document.querySelector('.consent-banner').remove();
            this.init();
        }

        declineConsent() {
            localStorage.setItem('analytics-consent', 'denied');
            document.querySelector('.consent-banner').remove();
        }

        // Session Management
        getOrCreateSession() {
            let session = sessionStorage.getItem('analytics-session');
            if (!session) {
                session = this.generateId();
                sessionStorage.setItem('analytics-session', session);
                sessionStorage.setItem('session-start', Date.now());
            }
            return session;
        }

        getAnonymousUserId() {
            let userId = localStorage.getItem('anonymous-user-id');
            if (!userId) {
                userId = this.generateId();
                localStorage.setItem('anonymous-user-id', userId);
            }
            return userId;
        }

        generateId() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                const r = Math.random() * 16 | 0;
                const v = c === 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
        }

        // Page View Tracking
        trackPageView() {
            if (!config.enabledFeatures.pageViews) return;

            const pageData = {
                event: 'page_view',
                page: {
                    path: window.location.pathname,
                    title: document.title,
                    section: this.getPageSection(),
                    referrer: document.referrer ? new URL(document.referrer).pathname : 'direct',
                    queryParams: this.sanitizeQueryParams()
                },
                session: {
                    id: this.sessionId,
                    isNew: !sessionStorage.getItem('returning-user')
                },
                timestamp: new Date().toISOString()
            };

            this.journey.push({
                path: pageData.page.path,
                timestamp: pageData.timestamp
            });

            this.sendEvent(pageData);
            sessionStorage.setItem('returning-user', 'true');
        }

        getPageSection() {
            const path = window.location.pathname;
            const sections = path.split('/').filter(Boolean);
            return sections[0] || 'home';
        }

        sanitizeQueryParams() {
            const params = new URLSearchParams(window.location.search);
            const sanitized = {};
            const allowedParams = ['q', 'section', 'version', 'lang'];
            
            for (const [key, value] of params) {
                if (allowedParams.includes(key)) {
                    sanitized[key] = value;
                }
            }
            return sanitized;
        }

        // Scroll Depth Tracking
        setupScrollTracking() {
            if (!config.enabledFeatures.scrollDepth) return;

            let ticking = false;
            const trackScroll = () => {
                const scrollPercent = this.getScrollPercent();
                
                config.scrollDepthThresholds.forEach(threshold => {
                    if (scrollPercent >= threshold && this.scrollDepthReached < threshold) {
                        this.scrollDepthReached = threshold;
                        this.sendEvent({
                            event: 'scroll_depth',
                            depth: threshold,
                            page: window.location.pathname,
                            timestamp: new Date().toISOString()
                        });
                    }
                });
            };

            window.addEventListener('scroll', () => {
                if (!ticking) {
                    window.requestAnimationFrame(() => {
                        trackScroll();
                        ticking = false;
                    });
                    ticking = true;
                }
            });
        }

        getScrollPercent() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const scrollHeight = document.documentElement.scrollHeight;
            const clientHeight = document.documentElement.clientHeight;
            return Math.round((scrollTop / (scrollHeight - clientHeight)) * 100);
        }

        // Search Tracking
        setupSearchTracking() {
            if (!config.enabledFeatures.searchTracking) return;

            // Track search input
            const searchInput = document.querySelector('input[type="search"], .search-input');
            if (searchInput) {
                let searchTimeout;
                searchInput.addEventListener('input', (e) => {
                    clearTimeout(searchTimeout);
                    searchTimeout = setTimeout(() => {
                        if (e.target.value.length > 2) {
                            this.trackSearch(e.target.value);
                        }
                    }, 1000);
                });
            }

            // Track search result clicks
            document.addEventListener('click', (e) => {
                if (e.target.closest('.search-result')) {
                    const result = e.target.closest('.search-result');
                    this.trackSearchResultClick(result);
                }
            });
        }

        trackSearch(query) {
            const searchData = {
                event: 'search',
                query: this.anonymizeQuery(query),
                resultsCount: document.querySelectorAll('.search-result').length,
                page: window.location.pathname,
                timestamp: new Date().toISOString()
            };
            
            this.searchQueries.push(searchData);
            this.sendEvent(searchData);
        }

        anonymizeQuery(query) {
            // Remove potential PII from search queries
            return query
                .replace(/\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/gi, '[email]')
                .replace(/\b\d{4,}\b/g, '[number]')
                .toLowerCase()
                .trim();
        }

        trackSearchResultClick(result) {
            this.sendEvent({
                event: 'search_result_click',
                resultTitle: result.querySelector('.result-title')?.textContent,
                resultPosition: Array.from(document.querySelectorAll('.search-result')).indexOf(result) + 1,
                query: this.searchQueries[this.searchQueries.length - 1]?.query,
                timestamp: new Date().toISOString()
            });
        }

        // Link & Navigation Tracking
        setupLinkTracking() {
            if (!config.enabledFeatures.userJourney) return;

            document.addEventListener('click', (e) => {
                const link = e.target.closest('a');
                if (link && link.href) {
                    this.trackLinkClick(link);
                }
            });
        }

        trackLinkClick(link) {
            const linkData = {
                event: 'link_click',
                link: {
                    text: link.textContent.substring(0, 100),
                    href: link.href,
                    isExternal: link.hostname !== window.location.hostname,
                    section: link.closest('[data-section]')?.dataset.section
                },
                page: window.location.pathname,
                timestamp: new Date().toISOString()
            };

            if (!linkData.link.isExternal) {
                this.journey.push({
                    from: window.location.pathname,
                    to: new URL(link.href).pathname,
                    timestamp: linkData.timestamp
                });
            }

            this.sendEvent(linkData);
        }

        // Page Visibility & Time Tracking
        setupVisibilityTracking() {
            if (!config.enabledFeatures.timeOnPage) return;

            let hiddenTime = 0;
            let lastHiddenTime = null;

            document.addEventListener('visibilitychange', () => {
                if (document.hidden) {
                    lastHiddenTime = Date.now();
                } else if (lastHiddenTime) {
                    hiddenTime += Date.now() - lastHiddenTime;
                    lastHiddenTime = null;
                }
            });

            // Track time on page when leaving
            window.addEventListener('beforeunload', () => {
                const totalTime = Date.now() - this.pageStartTime;
                const activeTime = totalTime - hiddenTime;
                
                this.sendEvent({
                    event: 'page_time',
                    time: {
                        total: Math.round(totalTime / 1000),
                        active: Math.round(activeTime / 1000),
                        hidden: Math.round(hiddenTime / 1000)
                    },
                    page: window.location.pathname,
                    scrollDepth: this.scrollDepthReached,
                    timestamp: new Date().toISOString()
                }, true); // Use sendBeacon for unload events
            });
        }

        // Error Tracking
        setupErrorTracking() {
            window.addEventListener('error', (e) => {
                if (e.filename && e.filename.includes('/docs/')) {
                    this.sendEvent({
                        event: 'javascript_error',
                        error: {
                            message: e.message,
                            filename: e.filename,
                            line: e.lineno,
                            column: e.colno
                        },
                        page: window.location.pathname,
                        timestamp: new Date().toISOString()
                    });
                }
            });

            // Track 404s and broken links
            this.checkBrokenLinks();
        }

        checkBrokenLinks() {
            const links = document.querySelectorAll('a[href^="/"], a[href^="./"], a[href^="../"]');
            links.forEach(link => {
                fetch(link.href, { method: 'HEAD' })
                    .then(response => {
                        if (!response.ok && response.status === 404) {
                            this.sendEvent({
                                event: 'broken_link',
                                link: link.href,
                                page: window.location.pathname,
                                timestamp: new Date().toISOString()
                            });
                        }
                    })
                    .catch(() => {}); // Silently fail for CORS or network errors
            });
        }

        // Performance Tracking
        setupPerformanceTracking() {
            if (!window.performance || !window.performance.timing) return;

            window.addEventListener('load', () => {
                setTimeout(() => {
                    const perfData = this.getPerformanceMetrics();
                    this.sendEvent({
                        event: 'performance',
                        metrics: perfData,
                        page: window.location.pathname,
                        timestamp: new Date().toISOString()
                    });
                }, 0);
            });

            // Track Core Web Vitals
            this.trackCoreWebVitals();
        }

        getPerformanceMetrics() {
            const timing = window.performance.timing;
            const navigation = window.performance.navigation;

            return {
                dns: timing.domainLookupEnd - timing.domainLookupStart,
                tcp: timing.connectEnd - timing.connectStart,
                ttfb: timing.responseStart - timing.navigationStart,
                download: timing.responseEnd - timing.responseStart,
                domInteractive: timing.domInteractive - timing.navigationStart,
                domComplete: timing.domComplete - timing.navigationStart,
                loadComplete: timing.loadEventEnd - timing.navigationStart,
                navigationType: navigation.type
            };
        }

        trackCoreWebVitals() {
            // Largest Contentful Paint (LCP)
            new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                this.sendEvent({
                    event: 'web_vitals',
                    metric: 'LCP',
                    value: lastEntry.renderTime || lastEntry.loadTime,
                    page: window.location.pathname,
                    timestamp: new Date().toISOString()
                });
            }).observe({ entryTypes: ['largest-contentful-paint'] });

            // First Input Delay (FID)
            new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    this.sendEvent({
                        event: 'web_vitals',
                        metric: 'FID',
                        value: entry.processingStart - entry.startTime,
                        page: window.location.pathname,
                        timestamp: new Date().toISOString()
                    });
                });
            }).observe({ entryTypes: ['first-input'] });

            // Cumulative Layout Shift (CLS)
            let clsValue = 0;
            new PerformanceObserver((list) => {
                list.getEntries().forEach(entry => {
                    if (!entry.hadRecentInput) {
                        clsValue += entry.value;
                    }
                });
            }).observe({ entryTypes: ['layout-shift'] });

            window.addEventListener('beforeunload', () => {
                this.sendEvent({
                    event: 'web_vitals',
                    metric: 'CLS',
                    value: clsValue,
                    page: window.location.pathname,
                    timestamp: new Date().toISOString()
                }, true);
            });
        }

        // Data Transmission
        sendEvent(data, useBeacon = false) {
            const payload = {
                ...data,
                context: {
                    sessionId: this.sessionId,
                    userId: this.userId,
                    userAgent: this.getAnonymizedUserAgent(),
                    viewport: {
                        width: window.innerWidth,
                        height: window.innerHeight
                    },
                    screen: {
                        width: window.screen.width,
                        height: window.screen.height
                    },
                    language: navigator.language,
                    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
                }
            };

            if (useBeacon && navigator.sendBeacon) {
                navigator.sendBeacon(config.endpoint, JSON.stringify(payload));
            } else {
                fetch(config.endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload),
                    keepalive: true
                }).catch(error => {
                    console.error('Analytics error:', error);
                });
            }
        }

        getAnonymizedUserAgent() {
            const ua = navigator.userAgent;
            // Remove specific version numbers for privacy
            return ua
                .replace(/Chrome\/[\d.]+/g, 'Chrome')
                .replace(/Firefox\/[\d.]+/g, 'Firefox')
                .replace(/Safari\/[\d.]+/g, 'Safari')
                .replace(/Edge\/[\d.]+/g, 'Edge');
        }

        // Public API for custom events
        track(eventName, data = {}) {
            this.sendEvent({
                event: 'custom',
                name: eventName,
                data: data,
                page: window.location.pathname,
                timestamp: new Date().toISOString()
            });
        }

        // User feedback tracking
        trackFeedback(type, value, comment = null) {
            this.sendEvent({
                event: 'feedback',
                feedback: {
                    type: type,
                    value: value,
                    comment: comment ? this.anonymizeQuery(comment) : null
                },
                page: window.location.pathname,
                timestamp: new Date().toISOString()
            });
        }
    }

    // Initialize analytics
    window.docAnalytics = new DocumentationAnalytics();

    // Check for consent on page load
    if (!localStorage.getItem('analytics-consent')) {
        setTimeout(() => {
            window.docAnalytics.requestConsent();
        }, 2000);
    }
})();