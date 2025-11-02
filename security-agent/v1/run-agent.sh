#!/bin/bash

#
# Mobile Security & Standards Agent - Runner Script
# Automatically detects environment and runs security scans
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}🔒 Mobile Security & Standards Agent${NC}"
echo -e "${BLUE}======================================${NC}\n"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python version: $PYTHON_VERSION${NC}"

# Check if running from correct directory
if [ ! -f "$SCRIPT_DIR/agent.py" ]; then
    echo -e "${RED}❌ Error: agent.py not found${NC}"
    echo "Please run this script from the security-agent directory"
    exit 1
fi

# Parse arguments
CONFIG_FILE="$SCRIPT_DIR/config/agent-config.json"
OUTPUT_FORMAT="all"
EXIT_ON_CRITICAL=false
HELP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        --format)
            OUTPUT_FORMAT="$2"
            shift 2
            ;;
        --exit-on-critical)
            EXIT_ON_CRITICAL=true
            shift
            ;;
        --help|-h)
            HELP=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            HELP=true
            shift
            ;;
    esac
done

# Show help
if [ "$HELP" = true ]; then
    echo "Usage: ./run-agent.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --config FILE          Path to config file (default: config/agent-config.json)"
    echo "  --format FORMAT        Report format: json, html, markdown, all (default: all)"
    echo "  --exit-on-critical     Exit with error if critical issues found"
    echo "  --help, -h             Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run-agent.sh"
    echo "  ./run-agent.sh --format html"
    echo "  ./run-agent.sh --exit-on-critical  # For CI/CD"
    exit 0
fi

# Check config file
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}❌ Error: Config file not found: $CONFIG_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Configuration: $CONFIG_FILE${NC}"
echo -e "${GREEN}✓ Output format: $OUTPUT_FORMAT${NC}\n"

# Change to project root for scanning
cd "$PROJECT_ROOT"

# Run the agent
echo -e "${YELLOW}🔍 Starting security scan...${NC}\n"

if [ "$EXIT_ON_CRITICAL" = true ]; then
    python3 "$SCRIPT_DIR/agent.py" || {
        echo -e "\n${RED}❌ Security scan failed with critical issues!${NC}"
        exit 1
    }
else
    python3 "$SCRIPT_DIR/agent.py" || {
        echo -e "\n${YELLOW}⚠️  Security scan completed with warnings${NC}"
    }
fi

echo -e "\n${GREEN}✅ Security scan complete!${NC}"

# Show report locations
if [ -d "$SCRIPT_DIR/reports" ]; then
    echo -e "\n${BLUE}📊 Reports generated:${NC}"
    ls -lh "$SCRIPT_DIR/reports/" | tail -n +2 | awk '{print "  - " $9 " (" $5 ")"}'
fi

echo -e "\n${BLUE}💡 Tip: Open HTML report in browser for interactive view${NC}"
echo -e "${BLUE}   Example: open security-agent/reports/security-report-*.html${NC}\n"

exit 0
