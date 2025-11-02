#!/bin/bash
# Security Agent v2 Runner Script
# Runs the comprehensive security agent v2 with all enhancements

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}?? Security Agent v2.0${NC}"
echo "=================================="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Run the agent
python3 agents/python/security_agent_v2.py "$@"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}? Security scan completed successfully${NC}"
else
    echo ""
    echo -e "${YELLOW}??  Security scan completed with issues${NC}"
fi

exit $EXIT_CODE
