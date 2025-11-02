#!/bin/bash

# ========================================================================
# Prepare GCP Deployment - Non-Interactive Setup
# ========================================================================
# Prepares build and checks configuration before deployment
# Run this before deploy-to-gcp-dual.sh
# ========================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}"
echo "========================================================================="
echo "   Prepare GCP Deployment Package"
echo "========================================================================="
echo -e "${NC}"

# Add gcloud to PATH if installed
if [ -d "$HOME/google-cloud-sdk/bin" ]; then
    export PATH="$HOME/google-cloud-sdk/bin:$PATH"
fi

# Configuration
PROJECT_ID="chk-poke-ocr"
BUCKET_NAME="gcp-count-la"
REGION="us-central1"

echo -e "${CYAN}Configuration:${NC}"
echo "  Project: $PROJECT_ID"
echo "  Bucket: $BUCKET_NAME"
echo "  Region: $REGION"
echo "  Domain: gcp.count.la"
echo ""

# Check gcloud
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI not found${NC}"
    echo "Install with: curl https://sdk.cloud.google.com | bash"
    exit 1
fi

echo -e "${GREEN}✓ gcloud CLI found${NC}"

# Check authentication
ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null || echo "")
if [ -z "$ACTIVE_ACCOUNT" ]; then
    echo -e "${YELLOW}⚠️  Not authenticated with GCP${NC}"
    echo ""
    echo "Run: gcloud auth login"
    echo "Then run this script again"
    exit 1
fi

echo -e "${GREEN}✓ Authenticated as: $ACTIVE_ACCOUNT${NC}"

# Set project
gcloud config set project "$PROJECT_ID" 2>/dev/null || {
    echo -e "${RED}Error: Project $PROJECT_ID not found or not accessible${NC}"
    exit 1
}

echo -e "${GREEN}✓ Project set to: $PROJECT_ID${NC}"

# Build React app
echo ""
echo -e "${BLUE}Building React app...${NC}"
if [ -d "dist" ]; then
    rm -rf dist
fi

if [ ! -d "node_modules" ]; then
    echo "  → Installing dependencies..."
    npm install
fi

npm run build
echo -e "${GREEN}✓ React app built${NC}"

# Add static site to v2
echo ""
echo -e "${BLUE}Adding static site to v2/...${NC}"
mkdir -p dist/v2
cp static-site/index.html dist/v2/
cp -r static-site/scripts dist/v2/
cp -r static-site/styles dist/v2/

if [ -d "static-site/assets" ]; then
    cp -r static-site/assets dist/v2/
fi

# Add footer link to static version (before closing body tag)
if ! grep -q "version-footer" dist/v2/index.html; then
    # Find the closing body tag and insert footer before it
    sed -i '/<\/body>/i\
<style>\
.version-footer {\
    position: fixed;\
    bottom: 15px;\
    right: 15px;\
    background: rgba(204, 0, 0, 0.9);\
    color: white;\
    padding: 10px 20px;\
    border-radius: 4px;\
    text-decoration: none;\
    font-size: 14px;\
    font-weight: 600;\
    z-index: 9999;\
    transition: all 0.3s ease;\
    border: 2px solid rgba(255, 255, 255, 0.3);\
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);\
}\
.version-footer:hover {\
    background: rgba(204, 0, 0, 1);\
    border-color: rgba(255, 255, 255, 0.6);\
    transform: translateY(-2px);\
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);\
}\
</style>\
<a href="/" class="version-footer" title="Switch to React TypeScript Version">← React Version</a>\
' dist/v2/index.html
    echo -e "${GREEN}✓ Footer link added to static site${NC}"
else
    echo -e "${YELLOW}⚠️  Footer link already exists${NC}"
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}              PREPARATION COMPLETE!                             ${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}Next steps:${NC}"
echo "1. Run: bash deploy-to-gcp-dual.sh"
echo "2. Or deploy manually with gsutil commands"
echo ""
echo -e "${CYAN}Deployment package ready in:${NC}"
echo "  • React: dist/index.html"
echo "  • Static: dist/v2/index.html"
echo ""
