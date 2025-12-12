/**
 * User Feedback Collection System
 * Collects and manages user feedback for Cloud Scale Analytics documentation
 */

(function() {
    'use strict';

    // Configuration
    const config = {
        endpoint: '/api/feedback',
        widgetPosition: 'bottom-right',
        enablePageRating: true,
        enableComments: true,
        enableIssueReporting: true,
        enableSuggestions: true,
        requireAuth: false,
        cooldownPeriod: 60000, // 1 minute between submissions
        maxCommentLength: 1000
    };

    // Feedback Widget Class
    class FeedbackWidget {
        constructor() {
            this.isOpen = false;
            this.currentPage = window.location.pathname;
            this.sessionId = this.getSessionId();
            this.feedbackHistory = this.loadFeedbackHistory();
            this.init();
        }

        init() {
            this.createWidget();
            this.attachEventListeners();
            this.checkPageFeedback();
        }

        getSessionId() {
            let sessionId = sessionStorage.getItem('feedback-session');
            if (!sessionId) {
                sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
                sessionStorage.setItem('feedback-session', sessionId);
            }
            return sessionId;
        }

        loadFeedbackHistory() {
            const history = localStorage.getItem('feedback-history');
            return history ? JSON.parse(history) : [];
        }

        saveFeedbackHistory(feedback) {
            this.feedbackHistory.push({
                ...feedback,
                timestamp: new Date().toISOString()
            });
            // Keep only last 50 feedback items
            if (this.feedbackHistory.length > 50) {
                this.feedbackHistory = this.feedbackHistory.slice(-50);
            }
            localStorage.setItem('feedback-history', JSON.stringify(this.feedbackHistory));
        }

        createWidget() {
            // Create main container
            const widget = document.createElement('div');
            widget.id = 'feedback-widget';
            widget.className = 'feedback-widget';
            widget.innerHTML = `
                <style>
                    .feedback-widget {
                        position: fixed;
                        bottom: 20px;
                        right: 20px;
                        z-index: 10000;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    }

                    .feedback-trigger {
                        background: #0066cc;
                        color: white;
                        border: none;
                        border-radius: 50%;
                        width: 56px;
                        height: 56px;
                        font-size: 24px;
                        cursor: pointer;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                        transition: transform 0.2s, box-shadow 0.2s;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }

                    .feedback-trigger:hover {
                        transform: scale(1.1);
                        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
                    }

                    .feedback-panel {
                        position: absolute;
                        bottom: 70px;
                        right: 0;
                        width: 400px;
                        max-width: 90vw;
                        background: white;
                        border-radius: 12px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                        display: none;
                        opacity: 0;
                        transform: translateY(20px);
                        transition: opacity 0.3s, transform 0.3s;
                    }

                    .feedback-panel.open {
                        display: block;
                        opacity: 1;
                        transform: translateY(0);
                    }

                    .feedback-header {
                        padding: 20px;
                        border-bottom: 1px solid #e1e1e1;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }

                    .feedback-title {
                        font-size: 18px;
                        font-weight: 600;
                        margin: 0;
                    }

                    .feedback-close {
                        background: none;
                        border: none;
                        font-size: 24px;
                        cursor: pointer;
                        color: #666;
                        padding: 0;
                        width: 30px;
                        height: 30px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }

                    .feedback-close:hover {
                        color: #333;
                    }

                    .feedback-tabs {
                        display: flex;
                        border-bottom: 1px solid #e1e1e1;
                        background: #f5f5f5;
                    }

                    .feedback-tab {
                        flex: 1;
                        padding: 12px;
                        background: none;
                        border: none;
                        cursor: pointer;
                        font-size: 14px;
                        color: #666;
                        transition: background 0.2s, color 0.2s;
                    }

                    .feedback-tab:hover {
                        background: #ebebeb;
                    }

                    .feedback-tab.active {
                        background: white;
                        color: #0066cc;
                        font-weight: 500;
                    }

                    .feedback-content {
                        padding: 20px;
                        max-height: 400px;
                        overflow-y: auto;
                    }

                    .feedback-section {
                        display: none;
                    }

                    .feedback-section.active {
                        display: block;
                        animation: fadeIn 0.3s;
                    }

                    @keyframes fadeIn {
                        from { opacity: 0; }
                        to { opacity: 1; }
                    }

                    .rating-container {
                        text-align: center;
                        padding: 20px 0;
                    }

                    .rating-question {
                        font-size: 16px;
                        margin-bottom: 20px;
                        color: #333;
                    }

                    .rating-stars {
                        display: flex;
                        justify-content: center;
                        gap: 10px;
                        margin-bottom: 20px;
                    }

                    .rating-star {
                        font-size: 32px;
                        cursor: pointer;
                        color: #ddd;
                        transition: color 0.2s, transform 0.2s;
                    }

                    .rating-star:hover {
                        transform: scale(1.2);
                    }

                    .rating-star.filled {
                        color: #ffb700;
                    }

                    .rating-emoji {
                        display: flex;
                        justify-content: center;
                        gap: 15px;
                        margin-bottom: 20px;
                    }

                    .emoji-btn {
                        background: none;
                        border: 2px solid transparent;
                        border-radius: 8px;
                        padding: 10px;
                        font-size: 32px;
                        cursor: pointer;
                        transition: all 0.2s;
                    }

                    .emoji-btn:hover {
                        transform: scale(1.1);
                        border-color: #0066cc;
                    }

                    .emoji-btn.selected {
                        background: #e6f2ff;
                        border-color: #0066cc;
                    }

                    .feedback-form {
                        display: flex;
                        flex-direction: column;
                        gap: 15px;
                    }

                    .form-group {
                        display: flex;
                        flex-direction: column;
                        gap: 5px;
                    }

                    .form-label {
                        font-size: 14px;
                        font-weight: 500;
                        color: #333;
                    }

                    .form-input,
                    .form-textarea,
                    .form-select {
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 6px;
                        font-size: 14px;
                        transition: border-color 0.2s;
                    }

                    .form-input:focus,
                    .form-textarea:focus,
                    .form-select:focus {
                        outline: none;
                        border-color: #0066cc;
                    }

                    .form-textarea {
                        resize: vertical;
                        min-height: 100px;
                    }

                    .char-count {
                        font-size: 12px;
                        color: #666;
                        text-align: right;
                    }

                    .form-checkbox {
                        display: flex;
                        align-items: center;
                        gap: 8px;
                    }

                    .form-checkbox input {
                        width: 18px;
                        height: 18px;
                    }

                    .submit-btn {
                        background: #0066cc;
                        color: white;
                        border: none;
                        padding: 12px 24px;
                        border-radius: 6px;
                        font-size: 14px;
                        font-weight: 500;
                        cursor: pointer;
                        transition: background 0.2s;
                    }

                    .submit-btn:hover {
                        background: #005299;
                    }

                    .submit-btn:disabled {
                        background: #ccc;
                        cursor: not-allowed;
                    }

                    .feedback-success {
                        text-align: center;
                        padding: 40px 20px;
                    }

                    .success-icon {
                        font-size: 48px;
                        color: #00a651;
                        margin-bottom: 20px;
                    }

                    .success-message {
                        font-size: 16px;
                        color: #333;
                        margin-bottom: 10px;
                    }

                    .success-submessage {
                        font-size: 14px;
                        color: #666;
                    }

                    .quick-actions {
                        display: grid;
                        grid-template-columns: repeat(2, 1fr);
                        gap: 10px;
                        margin-top: 20px;
                    }

                    .quick-action {
                        padding: 12px;
                        background: #f5f5f5;
                        border: 1px solid #ddd;
                        border-radius: 6px;
                        cursor: pointer;
                        transition: all 0.2s;
                        text-align: center;
                    }

                    .quick-action:hover {
                        background: #e6f2ff;
                        border-color: #0066cc;
                    }

                    .quick-action-icon {
                        font-size: 24px;
                        margin-bottom: 5px;
                    }

                    .quick-action-label {
                        font-size: 12px;
                        color: #666;
                    }

                    @media (max-width: 480px) {
                        .feedback-panel {
                            width: calc(100vw - 40px);
                            right: 20px;
                        }

                        .feedback-tabs {
                            flex-direction: column;
                        }

                        .quick-actions {
                            grid-template-columns: 1fr;
                        }
                    }
                </style>

                <button class="feedback-trigger" id="feedback-trigger" aria-label="Open feedback">
                    💬
                </button>

                <div class="feedback-panel" id="feedback-panel">
                    <div class="feedback-header">
                        <h3 class="feedback-title">Help Us Improve</h3>
                        <button class="feedback-close" id="feedback-close" aria-label="Close feedback">×</button>
                    </div>

                    <div class="feedback-tabs">
                        <button class="feedback-tab active" data-tab="rating">Rate Page</button>
                        <button class="feedback-tab" data-tab="issue">Report Issue</button>
                        <button class="feedback-tab" data-tab="suggestion">Suggest</button>
                        <button class="feedback-tab" data-tab="contribute">Contribute</button>
                    </div>

                    <div class="feedback-content">
                        <!-- Page Rating Section -->
                        <div class="feedback-section active" data-section="rating">
                            <div class="rating-container">
                                <div class="rating-question">Was this page helpful?</div>
                                <div class="rating-emoji">
                                    <button class="emoji-btn" data-rating="5" title="Very Helpful">😍</button>
                                    <button class="emoji-btn" data-rating="4" title="Helpful">😊</button>
                                    <button class="emoji-btn" data-rating="3" title="Neutral">😐</button>
                                    <button class="emoji-btn" data-rating="2" title="Not Helpful">😕</button>
                                    <button class="emoji-btn" data-rating="1" title="Very Unhelpful">😞</button>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Additional comments (optional)</label>
                                    <textarea class="form-textarea" id="rating-comment" placeholder="Tell us more about your experience..."></textarea>
                                    <div class="char-count">0 / 500</div>
                                </div>
                                <button class="submit-btn" id="submit-rating">Submit Feedback</button>
                            </div>
                        </div>

                        <!-- Issue Reporting Section -->
                        <div class="feedback-section" data-section="issue">
                            <form class="feedback-form" id="issue-form">
                                <div class="form-group">
                                    <label class="form-label">Issue Type</label>
                                    <select class="form-select" id="issue-type" required>
                                        <option value="">Select an issue type...</option>
                                        <option value="broken-link">Broken Link</option>
                                        <option value="incorrect-info">Incorrect Information</option>
                                        <option value="missing-content">Missing Content</option>
                                        <option value="code-error">Code Error</option>
                                        <option value="formatting">Formatting Issue</option>
                                        <option value="performance">Performance Problem</option>
                                        <option value="other">Other</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Description</label>
                                    <textarea class="form-textarea" id="issue-description" required placeholder="Describe the issue in detail..."></textarea>
                                    <div class="char-count">0 / 1000</div>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Steps to Reproduce (if applicable)</label>
                                    <textarea class="form-textarea" id="issue-steps" placeholder="1. Go to...\n2. Click on...\n3. See error..."></textarea>
                                </div>
                                <div class="form-checkbox">
                                    <input type="checkbox" id="issue-screenshot">
                                    <label for="issue-screenshot">Include page screenshot</label>
                                </div>
                                <button type="submit" class="submit-btn">Report Issue</button>
                            </form>
                        </div>

                        <!-- Suggestion Section -->
                        <div class="feedback-section" data-section="suggestion">
                            <form class="feedback-form" id="suggestion-form">
                                <div class="form-group">
                                    <label class="form-label">Suggestion Type</label>
                                    <select class="form-select" id="suggestion-type" required>
                                        <option value="">Select a type...</option>
                                        <option value="new-content">New Content</option>
                                        <option value="improvement">Content Improvement</option>
                                        <option value="feature">New Feature</option>
                                        <option value="navigation">Navigation Enhancement</option>
                                        <option value="design">Design Improvement</option>
                                        <option value="other">Other</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Your Suggestion</label>
                                    <textarea class="form-textarea" id="suggestion-text" required placeholder="Share your idea to improve the documentation..."></textarea>
                                    <div class="char-count">0 / 1000</div>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Expected Benefit</label>
                                    <textarea class="form-textarea" id="suggestion-benefit" placeholder="How will this help users?"></textarea>
                                </div>
                                <button type="submit" class="submit-btn">Submit Suggestion</button>
                            </form>
                        </div>

                        <!-- Contribution Section -->
                        <div class="feedback-section" data-section="contribute">
                            <div style="text-align: center; padding: 20px;">
                                <h4 style="margin-bottom: 20px;">Contribute to Documentation</h4>
                                <p style="color: #666; margin-bottom: 30px;">Help us improve by contributing directly to the documentation.</p>
                                <div class="quick-actions">
                                    <div class="quick-action" onclick="window.open('https://github.com/microsoft/csa-inabox-docs/edit/main${this.currentPage}')">
                                        <div class="quick-action-icon">✏️</div>
                                        <div class="quick-action-label">Edit This Page</div>
                                    </div>
                                    <div class="quick-action" onclick="window.open('https://github.com/microsoft/csa-inabox-docs/issues/new')">
                                        <div class="quick-action-icon">🐛</div>
                                        <div class="quick-action-label">File an Issue</div>
                                    </div>
                                    <div class="quick-action" onclick="window.open('https://github.com/microsoft/csa-inabox-docs/discussions')">
                                        <div class="quick-action-icon">💭</div>
                                        <div class="quick-action-label">Start Discussion</div>
                                    </div>
                                    <div class="quick-action" onclick="window.open('https://github.com/microsoft/csa-inabox-docs')">
                                        <div class="quick-action-icon">⭐</div>
                                        <div class="quick-action-label">Star on GitHub</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Success Message -->
                        <div class="feedback-success" id="feedback-success" style="display: none;">
                            <div class="success-icon">✅</div>
                            <div class="success-message">Thank you for your feedback!</div>
                            <div class="success-submessage">Your input helps us improve the documentation.</div>
                        </div>
                    </div>
                </div>
            `;

            document.body.appendChild(widget);

            // Store references
            this.trigger = document.getElementById('feedback-trigger');
            this.panel = document.getElementById('feedback-panel');
            this.closeBtn = document.getElementById('feedback-close');
            this.tabs = document.querySelectorAll('.feedback-tab');
            this.sections = document.querySelectorAll('.feedback-section');
        }

        attachEventListeners() {
            // Toggle panel
            this.trigger.addEventListener('click', () => this.togglePanel());
            this.closeBtn.addEventListener('click', () => this.closePanel());

            // Tab switching
            this.tabs.forEach(tab => {
                tab.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
            });

            // Rating emojis
            document.querySelectorAll('.emoji-btn').forEach(btn => {
                btn.addEventListener('click', (e) => this.selectRating(e.target));
            });

            // Character counting
            document.querySelectorAll('.form-textarea').forEach(textarea => {
                textarea.addEventListener('input', (e) => this.updateCharCount(e.target));
            });

            // Form submissions
            document.getElementById('submit-rating').addEventListener('click', () => this.submitRating());
            document.getElementById('issue-form').addEventListener('submit', (e) => this.submitIssue(e));
            document.getElementById('suggestion-form').addEventListener('submit', (e) => this.submitSuggestion(e));

            // Close on escape
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && this.isOpen) {
                    this.closePanel();
                }
            });

            // Close on click outside
            document.addEventListener('click', (e) => {
                if (this.isOpen && !this.panel.contains(e.target) && !this.trigger.contains(e.target)) {
                    this.closePanel();
                }
            });
        }

        togglePanel() {
            this.isOpen ? this.closePanel() : this.openPanel();
        }

        openPanel() {
            this.panel.classList.add('open');
            this.isOpen = true;
            this.trigger.innerHTML = '✕';
            
            // Track panel open event
            if (window.docAnalytics) {
                window.docAnalytics.track('feedback_panel_opened', {
                    page: this.currentPage
                });
            }
        }

        closePanel() {
            this.panel.classList.remove('open');
            this.isOpen = false;
            this.trigger.innerHTML = '💬';
        }

        switchTab(tabName) {
            // Update tab states
            this.tabs.forEach(tab => {
                tab.classList.toggle('active', tab.dataset.tab === tabName);
            });

            // Update section visibility
            this.sections.forEach(section => {
                section.classList.toggle('active', section.dataset.section === tabName);
            });

            // Track tab switch
            if (window.docAnalytics) {
                window.docAnalytics.track('feedback_tab_switched', {
                    tab: tabName,
                    page: this.currentPage
                });
            }
        }

        selectRating(button) {
            // Clear previous selection
            document.querySelectorAll('.emoji-btn').forEach(btn => {
                btn.classList.remove('selected');
            });

            // Mark as selected
            button.classList.add('selected');
            this.selectedRating = parseInt(button.dataset.rating);
        }

        updateCharCount(textarea) {
            const maxLength = textarea.id.includes('rating') ? 500 : 1000;
            const currentLength = textarea.value.length;
            const charCountElement = textarea.parentElement.querySelector('.char-count');
            
            if (charCountElement) {
                charCountElement.textContent = `${currentLength} / ${maxLength}`;
                charCountElement.style.color = currentLength > maxLength ? '#d83b01' : '#666';
            }
        }

        checkPageFeedback() {
            // Check if user has already provided feedback for this page
            const pageFeedback = this.feedbackHistory.find(f => f.page === this.currentPage);
            if (pageFeedback && this.wasRecentlySubmitted(pageFeedback.timestamp)) {
                // User has recently provided feedback for this page
                this.showPreviousFeedback(pageFeedback);
            }
        }

        wasRecentlySubmitted(timestamp) {
            const submittedAt = new Date(timestamp);
            const now = new Date();
            const diff = now - submittedAt;
            return diff < config.cooldownPeriod;
        }

        showPreviousFeedback(feedback) {
            // Show that feedback was already submitted
            const ratingSection = document.querySelector('[data-section="rating"]');
            if (ratingSection && feedback.type === 'rating') {
                const message = document.createElement('div');
                message.className = 'previous-feedback';
                message.innerHTML = `
                    <p style="color: #666; text-align: center; padding: 20px;">
                        You've already rated this page. Thank you for your feedback!
                    </p>
                `;
                ratingSection.prepend(message);
            }
        }

        async submitRating() {
            if (!this.selectedRating) {
                alert('Please select a rating');
                return;
            }

            const comment = document.getElementById('rating-comment').value;
            const feedback = {
                type: 'rating',
                page: this.currentPage,
                rating: this.selectedRating,
                comment: comment,
                sessionId: this.sessionId
            };

            await this.sendFeedback(feedback);
            this.showSuccess();
        }

        async submitIssue(e) {
            e.preventDefault();
            
            const feedback = {
                type: 'issue',
                page: this.currentPage,
                issueType: document.getElementById('issue-type').value,
                description: document.getElementById('issue-description').value,
                steps: document.getElementById('issue-steps').value,
                includeScreenshot: document.getElementById('issue-screenshot').checked,
                sessionId: this.sessionId
            };

            await this.sendFeedback(feedback);
            this.showSuccess();
            e.target.reset();
        }

        async submitSuggestion(e) {
            e.preventDefault();
            
            const feedback = {
                type: 'suggestion',
                page: this.currentPage,
                suggestionType: document.getElementById('suggestion-type').value,
                suggestion: document.getElementById('suggestion-text').value,
                benefit: document.getElementById('suggestion-benefit').value,
                sessionId: this.sessionId
            };

            await this.sendFeedback(feedback);
            this.showSuccess();
            e.target.reset();
        }

        async sendFeedback(feedback) {
            try {
                const response = await fetch(config.endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        ...feedback,
                        timestamp: new Date().toISOString(),
                        userAgent: navigator.userAgent,
                        viewport: {
                            width: window.innerWidth,
                            height: window.innerHeight
                        }
                    })
                });

                if (response.ok) {
                    this.saveFeedbackHistory(feedback);
                    
                    // Track with analytics
                    if (window.docAnalytics) {
                        window.docAnalytics.trackFeedback(feedback.type, feedback.rating || feedback.issueType || feedback.suggestionType, feedback.comment || feedback.description || feedback.suggestion);
                    }
                }
            } catch (error) {
                console.error('Failed to submit feedback:', error);
                // Still save locally even if API fails
                this.saveFeedbackHistory(feedback);
            }
        }

        showSuccess() {
            const successElement = document.getElementById('feedback-success');
            const contentElements = document.querySelectorAll('.feedback-section');
            
            // Hide all sections
            contentElements.forEach(el => el.style.display = 'none');
            
            // Show success message
            successElement.style.display = 'block';
            
            // Reset after 3 seconds
            setTimeout(() => {
                successElement.style.display = 'none';
                contentElements.forEach(el => el.style.display = '');
                this.closePanel();
                this.resetForms();
            }, 3000);
        }

        resetForms() {
            // Reset all forms
            document.querySelectorAll('.feedback-form').forEach(form => form.reset());
            document.querySelectorAll('.emoji-btn').forEach(btn => btn.classList.remove('selected'));
            document.getElementById('rating-comment').value = '';
            this.selectedRating = null;
        }
    }

    // Page-level feedback prompt
    class PageFeedbackPrompt {
        constructor() {
            this.promptShown = false;
            this.init();
        }

        init() {
            // Show prompt after user has spent some time on the page
            setTimeout(() => this.checkShowPrompt(), 30000); // 30 seconds

            // Show prompt when user scrolls to bottom
            window.addEventListener('scroll', () => {
                if (this.isNearBottom() && !this.promptShown) {
                    this.showPrompt();
                }
            });
        }

        isNearBottom() {
            const scrollPercent = (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight;
            return scrollPercent > 0.8;
        }

        checkShowPrompt() {
            // Check if we should show the prompt
            const lastPrompt = localStorage.getItem('last-feedback-prompt');
            const daysSinceLastPrompt = lastPrompt ? (Date.now() - parseInt(lastPrompt)) / (1000 * 60 * 60 * 24) : Infinity;
            
            if (daysSinceLastPrompt > 7 && !this.promptShown) {
                this.showPrompt();
            }
        }

        showPrompt() {
            if (this.promptShown) return;
            
            this.promptShown = true;
            localStorage.setItem('last-feedback-prompt', Date.now());

            const prompt = document.createElement('div');
            prompt.className = 'page-feedback-prompt';
            prompt.innerHTML = `
                <style>
                    .page-feedback-prompt {
                        position: fixed;
                        bottom: 100px;
                        right: 20px;
                        background: white;
                        border-radius: 8px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                        padding: 16px;
                        max-width: 300px;
                        z-index: 9999;
                        animation: slideIn 0.3s ease;
                    }

                    @keyframes slideIn {
                        from {
                            transform: translateX(100%);
                            opacity: 0;
                        }
                        to {
                            transform: translateX(0);
                            opacity: 1;
                        }
                    }

                    .prompt-content {
                        margin-bottom: 12px;
                    }

                    .prompt-title {
                        font-weight: 600;
                        margin-bottom: 4px;
                    }

                    .prompt-text {
                        font-size: 14px;
                        color: #666;
                    }

                    .prompt-actions {
                        display: flex;
                        gap: 8px;
                    }

                    .prompt-btn {
                        padding: 8px 16px;
                        border: none;
                        border-radius: 4px;
                        font-size: 14px;
                        cursor: pointer;
                        transition: background 0.2s;
                    }

                    .prompt-btn-primary {
                        background: #0066cc;
                        color: white;
                    }

                    .prompt-btn-primary:hover {
                        background: #005299;
                    }

                    .prompt-btn-secondary {
                        background: #f5f5f5;
                        color: #333;
                    }

                    .prompt-btn-secondary:hover {
                        background: #e1e1e1;
                    }
                </style>
                <div class="prompt-content">
                    <div class="prompt-title">Was this helpful?</div>
                    <div class="prompt-text">Let us know how we can improve this page.</div>
                </div>
                <div class="prompt-actions">
                    <button class="prompt-btn prompt-btn-primary" onclick="window.feedbackWidget.openPanel(); this.parentElement.parentElement.remove();">
                        Give Feedback
                    </button>
                    <button class="prompt-btn prompt-btn-secondary" onclick="this.parentElement.parentElement.remove();">
                        Not Now
                    </button>
                </div>
            `;

            document.body.appendChild(prompt);

            // Auto-remove after 10 seconds
            setTimeout(() => {
                if (prompt.parentElement) {
                    prompt.remove();
                }
            }, 10000);
        }
    }

    // Initialize feedback system
    window.feedbackWidget = new FeedbackWidget();
    window.pageFeedbackPrompt = new PageFeedbackPrompt();

    // Public API
    window.FeedbackAPI = {
        open: () => window.feedbackWidget.openPanel(),
        close: () => window.feedbackWidget.closePanel(),
        setPage: (path) => window.feedbackWidget.currentPage = path,
        submitCustom: (feedback) => window.feedbackWidget.sendFeedback(feedback)
    };
})();