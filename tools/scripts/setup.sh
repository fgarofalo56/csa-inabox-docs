#!/bin/bash

# CSA Documentation Tools Setup Script
# Sets up the unified documentation tooling environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$TOOLS_DIR")"

log_info "Starting CSA Documentation Tools setup..."
log_info "Tools directory: $TOOLS_DIR"
log_info "Project root: $PROJECT_ROOT"

# Check prerequisites
log_info "Checking prerequisites..."

if ! command_exists node; then
    log_error "Node.js not found. Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    log_error "Node.js version $NODE_VERSION is too old. Please install Node.js 18 or newer."
    exit 1
fi
log_success "Node.js $(node --version) found"

if ! command_exists npm; then
    log_error "npm not found. Please install npm."
    exit 1
fi

NPM_VERSION=$(npm --version | cut -d'.' -f1)
if [ "$NPM_VERSION" -lt 8 ]; then
    log_warning "npm version $(npm --version) is older than recommended (8+). Consider upgrading."
else
    log_success "npm $(npm --version) found"
fi

# Check if Python is available (for integration)
if command_exists python3; then
    log_success "Python 3 found: $(python3 --version)"
elif command_exists python; then
    log_success "Python found: $(python --version)"
else
    log_warning "Python not found. Integration scripts will not work."
fi

# Change to tools directory
cd "$TOOLS_DIR"

# Install Node.js dependencies
log_info "Installing Node.js dependencies..."
if [ -f package.json ]; then
    npm install
    log_success "Node.js dependencies installed"
else
    log_error "package.json not found in tools directory"
    exit 1
fi

# Install Mermaid CLI globally
log_info "Checking Mermaid CLI..."
if ! command_exists mmdc; then
    log_info "Installing Mermaid CLI globally..."
    npm install -g @mermaid-js/mermaid-cli || {
        log_warning "Failed to install Mermaid CLI globally. You may need to run with sudo or configure npm global permissions."
        log_info "Alternative: npx @mermaid-js/mermaid-cli will be used"
    }
else
    log_success "Mermaid CLI already installed: $(mmdc --version)"
fi

# Make CLI executable
log_info "Making CLI executable..."
if [ -f "src/bin/csa-docs.js" ]; then
    chmod +x src/bin/csa-docs.js
    log_success "CLI made executable"
else
    log_error "CLI file not found: src/bin/csa-docs.js"
    exit 1
fi

# Create npm link (optional)
log_info "Creating npm link for global access..."
npm link 2>/dev/null || {
    log_warning "Failed to create npm link. You may need to run with sudo."
    log_info "You can still use: node src/bin/csa-docs.js"
}

# Run initial tests
log_info "Running initial validation..."

# Test CLI
if node src/bin/csa-docs.js info >/dev/null 2>&1; then
    log_success "CLI working correctly"
else
    log_warning "CLI test failed - check dependencies"
fi

# Test integration (if Python available)
if command_exists python3 && [ -f "$PROJECT_ROOT/project_tracking/tools/csa-docs-integration.py" ]; then
    cd "$PROJECT_ROOT/project_tracking/tools"
    if python3 csa-docs-integration.py info >/dev/null 2>&1; then
        log_success "Python integration working"
    else
        log_warning "Python integration test failed"
    fi
    cd "$TOOLS_DIR"
fi

# Run tests if available
if [ -f package.json ] && grep -q '"test"' package.json; then
    log_info "Running unit tests..."
    if npm test >/dev/null 2>&1; then
        log_success "All tests passed"
    else
        log_warning "Some tests failed - check npm test output"
    fi
fi

# Create sample config files
log_info "Creating sample configuration files..."

# Mermaid config
if [ ! -f mermaid.config.json ]; then
    cat > mermaid.config.json << 'EOF'
{
  "theme": "default",
  "themeVariables": {
    "primaryColor": "#ff6b6b",
    "primaryTextColor": "#2c3e50",
    "primaryBorderColor": "#ff6b6b",
    "lineColor": "#333333"
  },
  "flowchart": {
    "htmlLabels": false,
    "curve": "basis"
  },
  "sequence": {
    "diagramMarginX": 50,
    "diagramMarginY": 10
  }
}
EOF
    log_success "Created sample mermaid.config.json"
fi

# Environment template
if [ ! -f .env.template ]; then
    cat > .env.template << 'EOF'
# CSA Documentation Tools Configuration

# Logging
LOG_LEVEL=info
LOG_FILE=./logs/csa-docs.log

# Mermaid Configuration
MERMAID_CLI_PATH=mmdc
MERMAID_CONFIG_PATH=./mermaid.config.json

# Tool Behavior
CSA_DOCS_DIR=../docs
CSA_AUTO_FIX=true
CSA_HEALTH_THRESHOLD=80

# Diagram Generation
DIAGRAM_THEME=default
DIAGRAM_BACKGROUND=transparent
DIAGRAM_WIDTH=1920
DIAGRAM_HEIGHT=1080
EOF
    log_success "Created .env.template"
fi

# Create logs directory
mkdir -p logs
log_success "Created logs directory"

# Display setup completion
echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Test the CLI: node src/bin/csa-docs.js info"
echo "2. Run documentation audit: node src/bin/csa-docs.js audit"
echo "3. Check the README.md for detailed usage instructions"
echo "4. Configure .env file based on .env.template if needed"
echo ""

# Show available commands
echo "🚀 Available Commands:"
echo "  csa-docs info                 - Show tool information"
echo "  csa-docs audit               - Run documentation audit" 
echo "  csa-docs generate-diagrams   - Generate PNG diagrams"
echo "  csa-docs replace-mermaid     - Replace Mermaid blocks"
echo "  csa-docs fix-issues          - Fix common issues"
echo "  csa-docs build              - Run complete pipeline"
echo "  csa-docs status             - Show health status"
echo ""

# Show integration info if Python available
if command_exists python3; then
    echo "🔗 Python Integration Available:"
    echo "  cd project_tracking/tools"
    echo "  python3 csa-docs-integration.py health"
    echo "  python3 enhanced_link_checker.py --quick-health"
    echo "  python3 integrated_docs_workflow.py"
    echo ""
fi

log_success "Setup complete! 🎉"