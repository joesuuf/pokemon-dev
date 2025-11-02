#!/bin/bash

# ========================================================================
# Deployment Comparison Script
# ========================================================================
# Compare performance between GitHub Pages and GCP deployments
# ========================================================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}"
echo "========================================================================"
echo "   GitHub Pages vs GCP - Performance Comparison"
echo "========================================================================"
echo -e "${NC}"
echo ""

# Check for required tools
MISSING_TOOLS=()

if ! command -v curl &> /dev/null; then
    MISSING_TOOLS+=("curl")
fi

if ! command -v ab &> /dev/null; then
    echo -e "${YELLOW}Note: 'ab' (Apache Bench) not found. Install for load testing:${NC}"
    echo "  Ubuntu/Debian: sudo apt-get install apache2-utils"
    echo "  Mac: brew install httpd"
    echo ""
fi

if ! command -v lighthouse &> /dev/null; then
    echo -e "${YELLOW}Note: 'lighthouse' not found. Install for performance testing:${NC}"
    echo "  npm install -g lighthouse"
    echo ""
fi

# Get URLs
echo -e "${CYAN}Enter your deployment URLs:${NC}"
echo ""
read -p "GitHub Pages URL (e.g., https://username.github.io/repo/): " GITHUB_URL
read -p "GCP URL (leave empty to skip): " GCP_URL

if [ -z "$GITHUB_URL" ]; then
    echo -e "${RED}Error: GitHub Pages URL is required${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}Starting comparison tests...${NC}"
echo ""

# Create results directory
RESULTS_DIR="comparison-results-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$RESULTS_DIR"

# Function to test URL
test_url() {
    local URL=$1
    local NAME=$2
    local OUTPUT_FILE="$RESULTS_DIR/${NAME}-results.txt"

    echo -e "${CYAN}Testing: $NAME${NC}"
    echo "URL: $URL"
    echo ""

    {
        echo "========================================================================"
        echo "  $NAME - Performance Test Results"
        echo "========================================================================"
        echo "URL: $URL"
        echo "Date: $(date)"
        echo ""

        # Basic connectivity test
        echo "--- Basic Connectivity Test ---"
        if curl -s -o /dev/null -w "HTTP Status: %{http_code}\nTotal Time: %{time_total}s\nDNS Lookup: %{time_namelookup}s\nConnect Time: %{time_connect}s\nTTFB: %{time_starttransfer}s\nDownload Speed: %{speed_download} bytes/sec\nSize: %{size_download} bytes\n" "$URL"; then
            echo "✓ Connection successful"
        else
            echo "✗ Connection failed"
        fi
        echo ""

        # Multiple request test (average)
        echo "--- Average Response Time (10 requests) ---"
        TOTAL_TIME=0
        for i in {1..10}; do
            TIME=$(curl -s -o /dev/null -w "%{time_total}" "$URL")
            TOTAL_TIME=$(echo "$TOTAL_TIME + $TIME" | bc)
            echo "Request $i: ${TIME}s"
        done
        AVG_TIME=$(echo "scale=4; $TOTAL_TIME / 10" | bc)
        echo "Average: ${AVG_TIME}s"
        echo ""

    } > "$OUTPUT_FILE"

    cat "$OUTPUT_FILE"

    # Load test (if ab is available)
    if command -v ab &> /dev/null; then
        echo "--- Load Test (100 requests, 10 concurrent) ---"
        ab -n 100 -c 10 "$URL" > "$RESULTS_DIR/${NAME}-loadtest.txt" 2>&1

        # Extract key metrics
        REQUESTS_PER_SEC=$(grep "Requests per second" "$RESULTS_DIR/${NAME}-loadtest.txt" | awk '{print $4}')
        TIME_PER_REQUEST=$(grep "Time per request:" "$RESULTS_DIR/${NAME}-loadtest.txt" | head -1 | awk '{print $4}')
        FAILED_REQUESTS=$(grep "Failed requests:" "$RESULTS_DIR/${NAME}-loadtest.txt" | awk '{print $3}')

        echo "Requests per second: $REQUESTS_PER_SEC"
        echo "Time per request: $TIME_PER_REQUEST ms"
        echo "Failed requests: $FAILED_REQUESTS"
        echo ""
    fi

    # Lighthouse test (if available)
    if command -v lighthouse &> /dev/null; then
        echo "Running Lighthouse audit (this may take a minute)..."
        lighthouse "$URL" \
            --output=json \
            --output=html \
            --output-path="$RESULTS_DIR/${NAME}-lighthouse" \
            --chrome-flags="--headless" \
            --quiet 2>/dev/null

        if [ -f "$RESULTS_DIR/${NAME}-lighthouse.report.json" ]; then
            # Extract scores from JSON
            PERFORMANCE=$(jq '.categories.performance.score * 100' "$RESULTS_DIR/${NAME}-lighthouse.report.json" 2>/dev/null)
            ACCESSIBILITY=$(jq '.categories.accessibility.score * 100' "$RESULTS_DIR/${NAME}-lighthouse.report.json" 2>/dev/null)
            BEST_PRACTICES=$(jq '.categories["best-practices"].score * 100' "$RESULTS_DIR/${NAME}-lighthouse.report.json" 2>/dev/null)
            SEO=$(jq '.categories.seo.score * 100' "$RESULTS_DIR/${NAME}-lighthouse.report.json" 2>/dev/null)

            echo "--- Lighthouse Scores ---"
            echo "Performance: ${PERFORMANCE:-N/A}"
            echo "Accessibility: ${ACCESSIBILITY:-N/A}"
            echo "Best Practices: ${BEST_PRACTICES:-N/A}"
            echo "SEO: ${SEO:-N/A}"
            echo ""
            echo "Full report: $RESULTS_DIR/${NAME}-lighthouse.report.html"
        fi
    fi

    echo "Results saved to: $OUTPUT_FILE"
    echo ""
}

# Test GitHub Pages
test_url "$GITHUB_URL" "github-pages"

# Test GCP (if provided)
if [ ! -z "$GCP_URL" ]; then
    test_url "$GCP_URL" "gcp"
fi

# Create comparison summary
SUMMARY_FILE="$RESULTS_DIR/COMPARISON_SUMMARY.md"

{
    echo "# Deployment Comparison Summary"
    echo ""
    echo "**Test Date:** $(date)"
    echo ""
    echo "## URLs Tested"
    echo ""
    echo "- **GitHub Pages:** $GITHUB_URL"
    if [ ! -z "$GCP_URL" ]; then
        echo "- **GCP:** $GCP_URL"
    fi
    echo ""
    echo "## Results"
    echo ""
    echo "See individual result files in this directory:"
    echo ""
    ls -1 "$RESULTS_DIR" | grep -v "COMPARISON_SUMMARY" | sed 's/^/- /'
    echo ""
    echo "## Cost Comparison"
    echo ""
    echo "| Platform | Monthly Cost | Notes |"
    echo "|----------|-------------|-------|"
    echo "| GitHub Pages | \$0 | Free tier |"
    if [ ! -z "$GCP_URL" ]; then
        echo "| GCP | ~\$0.15 - \$50 | Depends on service |"
    fi
    echo ""
    echo "## Performance Summary"
    echo ""
    echo "Fill in after reviewing detailed results:"
    echo ""
    echo "| Metric | GitHub Pages | GCP | Winner |"
    echo "|--------|-------------|-----|--------|"
    echo "| Avg Response Time | ? | ? | ? |"
    echo "| Requests/sec | ? | ? | ? |"
    echo "| Lighthouse Performance | ? | ? | ? |"
    echo "| Failed Requests | ? | ? | ? |"
    echo ""
    echo "## Recommendations"
    echo ""
    echo "Based on your specific needs:"
    echo ""
    echo "- **Choose GitHub Pages if:**"
    echo "  - Cost is primary concern (free)"
    echo "  - Simple static site"
    echo "  - No advanced monitoring needed"
    echo ""
    echo "- **Choose GCP if:**"
    echo "  - Need advanced monitoring/logging"
    echo "  - Require guaranteed SLA"
    echo "  - Enterprise requirements"
    echo "  - Integration with other GCP services"
    echo ""
} > "$SUMMARY_FILE"

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}              COMPARISON COMPLETE!                               ${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}Results Directory:${NC} $RESULTS_DIR"
echo ""
echo -e "${CYAN}Files Created:${NC}"
ls -1 "$RESULTS_DIR"
echo ""
echo -e "${CYAN}View Summary:${NC}"
echo "  cat $SUMMARY_FILE"
echo ""

if command -v lighthouse &> /dev/null; then
    echo -e "${CYAN}View Lighthouse Reports:${NC}"
    echo "  GitHub Pages: open $RESULTS_DIR/github-pages-lighthouse.report.html"
    if [ ! -z "$GCP_URL" ]; then
        echo "  GCP: open $RESULTS_DIR/gcp-lighthouse.report.html"
    fi
    echo ""
fi

echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Review detailed results in $RESULTS_DIR"
echo "2. Compare performance metrics"
echo "3. Monitor costs for 1 week"
echo "4. Make final deployment decision"
echo ""
echo -e "${GREEN}Comparison complete!${NC}"
echo ""
