#!/bin/bash

# ========================================================================
# Dual Version Deployment Script
# ========================================================================
# Deploys React as main index + Static site in v2/ subfolder
# For git.count.la (GitHub Pages) and gcp.count.la (GCP)
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
echo "   Dual Version Deployment - React + Static v2"
echo "========================================================================"
echo -e "${NC}"
echo ""

# Configuration
DEPLOY_DIR="dual-deploy-temp"

echo -e "${CYAN}This script creates a deployment with:${NC}"
echo "  • React TypeScript app as main index"
echo "  • Static HTML/CSS version in v2/ subfolder"
echo "  • Footer links connecting both versions"
echo ""
echo -e "${CYAN}Target domains:${NC}"
echo "  • git.count.la (GitHub Pages)"
echo "  • gcp.count.la (GCP)"
echo ""

read -p "Continue? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

# Clean up old deployment
if [ -d "$DEPLOY_DIR" ]; then
    rm -rf "$DEPLOY_DIR"
fi

mkdir -p "$DEPLOY_DIR"

echo ""
echo -e "${BLUE}Step 1: Building React application...${NC}"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "  → Running npm install..."
    npm install
fi

# Build React app
echo "  → Building with Vite..."
npm run build

if [ ! -d "dist" ]; then
    echo -e "${RED}Error: Build failed${NC}"
    exit 1
fi

# Copy React build to deployment directory
echo "  → Copying React build to deployment directory..."
cp -r dist/* "$DEPLOY_DIR/"

echo -e "${GREEN}  ✓ React build complete${NC}"

echo ""
echo -e "${BLUE}Step 2: Adding static site to v2/ subfolder...${NC}"

# Create v2 directory in deployment
mkdir -p "$DEPLOY_DIR/v2"

# Copy static site files
echo "  → Copying static site files..."
cp static-site/index.html "$DEPLOY_DIR/v2/"
cp -r static-site/scripts "$DEPLOY_DIR/v2/"
cp -r static-site/styles "$DEPLOY_DIR/v2/"

if [ -d "static-site/assets" ]; then
    cp -r static-site/assets "$DEPLOY_DIR/v2/"
fi

echo -e "${GREEN}  ✓ Static site copied to v2/${NC}"

echo ""
echo -e "${BLUE}Step 3: Creating cross-links between versions...${NC}"

# Add footer link to static site (v2) pointing back to React
cat >> "$DEPLOY_DIR/v2/index.html" << 'EOF'

<style>
.version-footer {
    position: fixed;
    bottom: 10px;
    right: 10px;
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 12px;
    z-index: 9999;
    text-decoration: none;
    font-family: 'Courier New', monospace;
}
.version-footer:hover {
    background: rgba(0, 0, 0, 0.95);
}
</style>
<a href="/" class="version-footer">← React Version</a>
EOF

echo -e "${GREEN}  ✓ Added footer link to static version${NC}"

# Note: React version footer will be added when we update the source

echo ""
echo -e "${BLUE}Step 4: Creating deployment configs...${NC}"

# Create CNAME files for both domains
echo "git.count.la" > "$DEPLOY_DIR/CNAME"
echo "gcp.count.la" > "$DEPLOY_DIR/CNAME.gcp"

# Create .nojekyll to disable Jekyll processing
touch "$DEPLOY_DIR/.nojekyll"

# Create README for deployment
cat > "$DEPLOY_DIR/README.md" << 'EOF'
# Pokemon TCG Search - Dual Version Deployment

This deployment contains both versions:

- **Main (/):** React + TypeScript frontend
- **v2/ subfolder:** Static HTML/CSS/JS frontend

## Deployment Targets

- **git.count.la** - GitHub Pages
- **gcp.count.la** - Google Cloud Platform

## Structure

```
/
├── index.html          # React app entry
├── assets/            # React build assets
├── v2/                # Static site
│   ├── index.html
│   ├── scripts/
│   └── styles/
└── CNAME              # Custom domain
```

## Navigation

- React → Static: Footer link "Static v2 →"
- Static → React: Footer link "← React Version"

## Deployed

- Date: [DEPLOY_DATE]
- React Version: 2.0.0
- Static Version: 1.0.0
EOF

echo -e "${GREEN}  ✓ Deployment configs created${NC}"

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}         DEPLOYMENT PACKAGE READY!                               ${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${CYAN}Package Location:${NC} $DEPLOY_DIR"
echo ""
echo -e "${CYAN}Structure:${NC}"
tree -L 2 "$DEPLOY_DIR" 2>/dev/null || find "$DEPLOY_DIR" -maxdepth 2 -type f | head -20
echo ""

echo -e "${CYAN}Next Steps:${NC}"
echo ""
echo "1. Deploy to GitHub Pages (git.count.la):"
echo "   ${BLUE}bash deploy-to-github-dual.sh${NC}"
echo ""
echo "2. Deploy to GCP (gcp.count.la):"
echo "   ${BLUE}bash deploy-to-gcp-dual.sh${NC}"
echo ""
echo "3. Configure DNS in Cloudflare:"
echo "   • git.count.la → CNAME → joesuuf.github.io"
echo "   • gcp.count.la → CNAME → [GCP-URL]"
echo ""

echo -e "${YELLOW}⚠️  Important: Update React source to add footer link${NC}"
echo "   Run: ${BLUE}bash add-footer-links.sh${NC}"
echo ""
