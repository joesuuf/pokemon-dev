#!/bin/bash

# ========================================================================
# Deploy Dual Version to GCP (gcp.count.la)
# ========================================================================
# Deploys React + Static v2 to Google Cloud Platform
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
echo "========================================================================"
echo "   Deploy Dual Version to GCP (gcp.count.la)"
echo "========================================================================"
echo -e "${NC}"

# Check for gcloud
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI not installed${NC}"
    echo "Install: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Configuration
PROJECT_ID="pokemon-tcg-gcp"  # Change if needed
BUCKET_NAME="gcp-count-la"
REGION="us-central1"

echo -e "${CYAN}GCP Configuration:${NC}"
echo "  Project: $PROJECT_ID"
echo "  Bucket: $BUCKET_NAME"
echo "  Region: $REGION"
echo "  Domain: gcp.count.la"
echo ""

read -p "Continue with deployment? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

# Authenticate
echo -e "${BLUE}Step 1: Authentication${NC}"
ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null || echo "")
if [ -z "$ACTIVE_ACCOUNT" ]; then
    echo "  → Logging in to GCP..."
    gcloud auth login
else
    echo "  ✓ Authenticated as: $ACTIVE_ACCOUNT"
fi

# Set project
echo ""
echo -e "${BLUE}Step 2: Setting up project${NC}"
gcloud config set project "$PROJECT_ID" 2>/dev/null || {
    echo "  → Project doesn't exist. Creating..."
    gcloud projects create "$PROJECT_ID" --name="Pokemon TCG GCP"
}

# Enable APIs
echo ""
echo -e "${BLUE}Step 3: Enabling required APIs${NC}"
gcloud services enable storage-api.googleapis.com --project="$PROJECT_ID"
gcloud services enable compute.googleapis.com --project="$PROJECT_ID"

# Build deployment
echo ""
echo -e "${BLUE}Step 4: Building deployment package${NC}"

# Clean build
if [ -d "dist" ]; then
    rm -rf dist
fi

# Install and build
if [ ! -d "node_modules" ]; then
    echo "  → Installing dependencies..."
    npm install
fi

echo "  → Building React app..."
npm run build

# Add static site to v2
echo "  → Adding static site to v2/..."
mkdir -p dist/v2
cp static-site/index.html dist/v2/
cp -r static-site/scripts dist/v2/
cp -r static-site/styles dist/v2/

if [ -d "static-site/assets" ]; then
    cp -r static-site/assets dist/v2/
fi

# Add footer link to static version
cat >> dist/v2/index.html << 'FOOTER'

<style>
.version-footer {
    position: fixed;
    bottom: 15px;
    right: 15px;
    background: rgba(204, 0, 0, 0.9);
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    z-index: 9999;
    transition: all 0.3s ease;
    border: 2px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}
.version-footer:hover {
    background: rgba(204, 0, 0, 1);
    border-color: rgba(255, 255, 255, 0.6);
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
}
</style>
<a href="/" class="version-footer" title="Switch to React TypeScript Version">← React Version</a>
</body>
</html>
FOOTER

# Fix duplicate closing tags
sed -i '$ d' dist/v2/index.html
sed -i '$ d' dist/v2/index.html

echo "  ✓ Deployment package ready"

# Create or configure bucket
echo ""
echo -e "${BLUE}Step 5: Setting up Cloud Storage bucket${NC}"

# Create bucket
gsutil mb -p "$PROJECT_ID" -c STANDARD -l "$REGION" "gs://$BUCKET_NAME" 2>/dev/null || echo "  → Bucket already exists"

# Make bucket public
echo "  → Making bucket publicly readable..."
gsutil iam ch allUsers:objectViewer "gs://$BUCKET_NAME"

# Configure for static website
echo "  → Configuring for static website..."
gsutil web set -m index.html -e index.html "gs://$BUCKET_NAME"

# Upload files
echo ""
echo -e "${BLUE}Step 6: Uploading files to GCP${NC}"
gsutil -m rsync -r -d dist "gs://$BUCKET_NAME"

# Set cache control
echo "  → Setting cache headers..."
gsutil -m setmeta -h "Cache-Control:public, max-age=3600" "gs://$BUCKET_NAME/**"

# Get URLs
STORAGE_URL="https://storage.googleapis.com/$BUCKET_NAME/index.html"

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}              DEPLOYMENT COMPLETE!                               ${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${CYAN}Access URLs:${NC}"
echo "  • React Version:  $STORAGE_URL"
echo "  • Static Version: https://storage.googleapis.com/$BUCKET_NAME/v2/index.html"
echo ""
echo "  • Or via bucket URL: https://$BUCKET_NAME.storage.googleapis.com/"
echo ""

echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}          CONFIGURE CLOUDFLARE DNS FOR gcp.count.la             ${NC}"
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "For best performance, set up a Load Balancer:"
echo ""
echo "1. Create HTTPS Load Balancer:"
echo "   https://console.cloud.google.com/net-services/loadbalancing"
echo ""
echo "2. Backend configuration:"
echo "   • Type: Cloud Storage bucket"
echo "   • Bucket: $BUCKET_NAME"
echo "   • Enable Cloud CDN: Yes"
echo ""
echo "3. Frontend configuration:"
echo "   • Protocol: HTTPS"
echo "   • IP: Create new external IP"
echo "   • Certificate: Create Google-managed certificate for gcp.count.la"
echo ""
echo "4. Add DNS record in Cloudflare:"
echo "   Type: A"
echo "   Name: gcp"
echo "   IPv4: [Load Balancer IP from step 3]"
echo "   Proxy: DNS only (gray cloud) OR Proxied (orange cloud)"
echo ""
echo "Alternative (without CDN):"
echo "   Type: CNAME"
echo "   Name: gcp"
echo "   Target: c.storage.googleapis.com"
echo "   Proxy: Either works"
echo ""
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${CYAN}Testing URLs:${NC}"
echo "  curl -I $STORAGE_URL"
echo "  curl -I https://storage.googleapis.com/$BUCKET_NAME/v2/index.html"
echo ""

echo -e "${GREEN}Deployment to GCP complete!${NC}"
echo ""
