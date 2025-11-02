#!/bin/bash

# ========================================================================
# GitHub Pages Deployment Script with Cloudflare DNS
# ========================================================================
# This script deploys your chosen frontend to GitHub Pages
# Supports: React build or Static site
# DNS: Cloudflare (not proxy mode)
# ========================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "========================================================================"
echo "   GitHub Pages Deployment with Cloudflare DNS"
echo "========================================================================"
echo -e "${NC}"

# Configuration
REPO_URL="https://github.com/joesuuf/pokemon-dev"
BRANCH_NAME="gh-pages"
BUILD_DIR="dist"
STATIC_SITE_DIR="static-site"

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${CYAN}Current branch: $CURRENT_BRANCH${NC}"
echo ""

# Show default ports information
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}                    DEFAULT DEV PORTS                            ${NC}"
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}Default Development Ports:${NC}"
echo "  • Port 8888: Main React Frontend (npm run dev)"
echo "  • Port 6666: Alternative React (npm run dev:6666)"
echo "  • Port 9999: Vite variant (npm run frontend:9999)"
echo ""
echo -e "${CYAN}Static Site:${NC}"
echo "  • Uses python3 -m http.server 8000 (in static-site folder)"
echo "  • Or: npx http-server static-site -p 8000"
echo ""
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Choose frontend version
echo -e "${GREEN}Which frontend do you want to deploy to GitHub Pages?${NC}"
echo ""
echo "  1) React Frontend (port 8888 - main React app)"
echo "     • Modern React 19.2.0 + TypeScript + Vite"
echo "     • ~150KB bundle (gzipped: ~50KB)"
echo "     • Requires npm build"
echo ""
echo "  2) Static Site (recommended - 15x smaller, 30x faster)"
echo "     • Pure HTML/CSS/JavaScript"
echo "     • ~10KB total (all files)"
echo "     • No build process needed"
echo "     • Better SEO and performance"
echo ""
echo "  3) Cancel"
echo ""

read -p "Enter your choice (1, 2, or 3): " CHOICE

case $CHOICE in
    1)
        FRONTEND_TYPE="react"
        echo -e "${BLUE}→ Selected: React Frontend${NC}"
        ;;
    2)
        FRONTEND_TYPE="static"
        echo -e "${BLUE}→ Selected: Static Site (Recommended)${NC}"
        ;;
    3)
        echo -e "${YELLOW}Deployment cancelled.${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"

# Prepare deployment directory
DEPLOY_DIR="github-pages-deploy"

echo ""
echo -e "${BLUE}Preparing deployment...${NC}"

# Clean up old deployment directory if it exists
if [ -d "$DEPLOY_DIR" ]; then
    echo "  → Removing old deployment directory..."
    rm -rf "$DEPLOY_DIR"
fi

mkdir -p "$DEPLOY_DIR"

# Build or copy files based on selection
if [ "$FRONTEND_TYPE" == "react" ]; then
    echo ""
    echo -e "${BLUE}Building React application...${NC}"

    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}→ node_modules not found. Running npm install...${NC}"
        npm install
    fi

    # Build React app
    echo "  → Running TypeScript compiler and Vite build..."
    npm run build

    if [ ! -d "$BUILD_DIR" ]; then
        echo -e "${RED}Error: Build failed. $BUILD_DIR directory not found.${NC}"
        exit 1
    fi

    # Copy built files
    echo "  → Copying built files from $BUILD_DIR/..."
    cp -r "$BUILD_DIR"/* "$DEPLOY_DIR/"

    # Create CNAME file if custom domain is specified
    read -p $'\n'"Enter custom domain (e.g., pokemon-tcg.yourdomain.com) or press Enter to skip: " CUSTOM_DOMAIN

    if [ ! -z "$CUSTOM_DOMAIN" ]; then
        echo "$CUSTOM_DOMAIN" > "$DEPLOY_DIR/CNAME"
        echo -e "${GREEN}  ✓ CNAME file created for: $CUSTOM_DOMAIN${NC}"
    fi

else  # static site
    echo ""
    echo -e "${BLUE}Preparing static site...${NC}"

    if [ ! -d "$STATIC_SITE_DIR" ]; then
        echo -e "${RED}Error: Static site directory not found at $STATIC_SITE_DIR${NC}"
        exit 1
    fi

    # Copy static site files
    echo "  → Copying static site files..."
    cp "$STATIC_SITE_DIR/index.html" "$DEPLOY_DIR/"
    cp -r "$STATIC_SITE_DIR/scripts" "$DEPLOY_DIR/"
    cp -r "$STATIC_SITE_DIR/styles" "$DEPLOY_DIR/"

    # Create assets directory if it exists
    if [ -d "$STATIC_SITE_DIR/assets" ]; then
        cp -r "$STATIC_SITE_DIR/assets" "$DEPLOY_DIR/"
    fi

    # Create CNAME file if custom domain is specified
    read -p $'\n'"Enter custom domain (e.g., pokemon-tcg.yourdomain.com) or press Enter to skip: " CUSTOM_DOMAIN

    if [ ! -z "$CUSTOM_DOMAIN" ]; then
        echo "$CUSTOM_DOMAIN" > "$DEPLOY_DIR/CNAME"
        echo -e "${GREEN}  ✓ CNAME file created for: $CUSTOM_DOMAIN${NC}"
    fi
fi

# Create .nojekyll file to disable Jekyll processing
echo "  → Creating .nojekyll file (disables Jekyll)..."
touch "$DEPLOY_DIR/.nojekyll"

# Create README for gh-pages branch
cat > "$DEPLOY_DIR/README.md" << EOF
# Pokemon TCG Search - GitHub Pages Deployment

This is the deployed version of the Pokemon TCG Search application.

**Deployment Type:** $FRONTEND_TYPE
**Deployed:** $(date)
**Branch:** $BRANCH_NAME

## View Site

EOF

if [ ! -z "$CUSTOM_DOMAIN" ]; then
    echo "**URL:** https://$CUSTOM_DOMAIN" >> "$DEPLOY_DIR/README.md"
else
    echo "**URL:** https://joesuuf.github.io/pokemon-dev/" >> "$DEPLOY_DIR/README.md"
fi

cat >> "$DEPLOY_DIR/README.md" << EOF

## Deployment Details

- **Source Branch:** $CURRENT_BRANCH
- **Frontend:** $FRONTEND_TYPE
- **DNS:** Cloudflare (not proxy mode)

## Redeploy

To redeploy, run from the main repository:
\`\`\`bash
bash deploy-to-github-pages.sh
\`\`\`

EOF

echo -e "${GREEN}  ✓ Deployment files prepared${NC}"

# Deploy to gh-pages branch
echo ""
echo -e "${BLUE}Deploying to GitHub Pages...${NC}"

cd "$DEPLOY_DIR"

# Initialize git in deployment directory
git init
git add .
git commit -m "Deploy $FRONTEND_TYPE frontend to GitHub Pages - $(date)"

# Push to gh-pages branch
echo "  → Pushing to $BRANCH_NAME branch..."

# Force push to gh-pages branch
git push -f "$REPO_URL" HEAD:$BRANCH_NAME

cd ..

# Clean up
echo "  → Cleaning up deployment directory..."
rm -rf "$DEPLOY_DIR"

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}                    DEPLOYMENT COMPLETE!                          ${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Display deployment information
if [ ! -z "$CUSTOM_DOMAIN" ]; then
    SITE_URL="https://$CUSTOM_DOMAIN"
else
    SITE_URL="https://joesuuf.github.io/pokemon-dev/"
fi

echo -e "${CYAN}Deployment Information:${NC}"
echo "  • Frontend Type: $FRONTEND_TYPE"
echo "  • Branch: $BRANCH_NAME"
echo "  • Site URL: $SITE_URL"
echo ""

# GitHub Pages setup instructions
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}           GITHUB PAGES SETUP (If not already done)              ${NC}"
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "1. Go to your repository on GitHub:"
echo "   $REPO_URL"
echo ""
echo "2. Click 'Settings' → 'Pages'"
echo ""
echo "3. Under 'Source':"
echo "   • Branch: $BRANCH_NAME"
echo "   • Folder: / (root)"
echo ""
echo "4. Click 'Save'"
echo ""
echo "5. Wait 1-2 minutes for deployment to complete"
echo ""

# Cloudflare DNS setup instructions
if [ ! -z "$CUSTOM_DOMAIN" ]; then
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}              CLOUDFLARE DNS SETUP (Non-Proxy Mode)              ${NC}"
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}Step 1: Add DNS Records in Cloudflare${NC}"
    echo ""
    echo "1. Log into Cloudflare Dashboard"
    echo "2. Select your domain"
    echo "3. Go to 'DNS' section"
    echo "4. Add the following DNS records:"
    echo ""

    # Extract subdomain if present
    if [[ "$CUSTOM_DOMAIN" == *"."*"."* ]]; then
        # Has subdomain (e.g., pokemon-tcg.yourdomain.com)
        SUBDOMAIN=$(echo $CUSTOM_DOMAIN | cut -d'.' -f1)
        echo -e "${GREEN}   For subdomain: $CUSTOM_DOMAIN${NC}"
        echo ""
        echo "   Record Type: CNAME"
        echo "   Name: $SUBDOMAIN"
        echo "   Target: joesuuf.github.io"
        echo "   TTL: Auto"
        echo "   Proxy status: DNS only (click the cloud to disable proxy)"
        echo "                 ↑ IMPORTANT: Must be gray cloud (DNS only)"
    else
        # Apex domain (e.g., yourdomain.com)
        echo -e "${GREEN}   For apex domain: $CUSTOM_DOMAIN${NC}"
        echo ""
        echo "   Add FOUR A records pointing to GitHub's IPs:"
        echo ""
        echo "   Record 1:"
        echo "   • Type: A"
        echo "   • Name: @"
        echo "   • IPv4: 185.199.108.153"
        echo "   • Proxy: DNS only (gray cloud)"
        echo ""
        echo "   Record 2:"
        echo "   • Type: A"
        echo "   • Name: @"
        echo "   • IPv4: 185.199.109.153"
        echo "   • Proxy: DNS only (gray cloud)"
        echo ""
        echo "   Record 3:"
        echo "   • Type: A"
        echo "   • Name: @"
        echo "   • IPv4: 185.199.110.153"
        echo "   • Proxy: DNS only (gray cloud)"
        echo ""
        echo "   Record 4:"
        echo "   • Type: A"
        echo "   • Name: @"
        echo "   • IPv4: 185.199.111.153"
        echo "   • Proxy: DNS only (gray cloud)"
        echo ""
        echo "   Optional www subdomain:"
        echo "   • Type: CNAME"
        echo "   • Name: www"
        echo "   • Target: joesuuf.github.io"
        echo "   • Proxy: DNS only (gray cloud)"
    fi

    echo ""
    echo -e "${CYAN}Step 2: Configure GitHub Pages Custom Domain${NC}"
    echo ""
    echo "1. Go to: $REPO_URL/settings/pages"
    echo "2. Under 'Custom domain', enter: $CUSTOM_DOMAIN"
    echo "3. Click 'Save'"
    echo "4. Check 'Enforce HTTPS' (after DNS propagates)"
    echo ""

    echo -e "${CYAN}Step 3: Wait for DNS Propagation${NC}"
    echo ""
    echo "• DNS propagation can take 5 minutes to 48 hours"
    echo "• Usually completes within 15-30 minutes"
    echo "• Check status at: https://dnschecker.org"
    echo ""

    echo -e "${CYAN}Step 4: Verify Deployment${NC}"
    echo ""
    echo "Once DNS has propagated, visit:"
    echo "  → $SITE_URL"
    echo ""

    echo -e "${YELLOW}⚠️  IMPORTANT: DNS ONLY MODE (NOT PROXY)${NC}"
    echo ""
    echo "Make sure the cloud icon in Cloudflare is GRAY (DNS only)."
    echo "Orange cloud (proxied) will not work with GitHub Pages custom domain."
    echo ""
    echo "Gray cloud = DNS only = ✓ Correct"
    echo "Orange cloud = Proxied = ✗ Will not work"
    echo ""

fi

echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}                    TROUBLESHOOTING                               ${NC}"
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Site not loading?"
echo ""
echo "1. Check GitHub Pages deployment:"
echo "   • Go to: $REPO_URL/deployments"
echo "   • Verify gh-pages deployment is successful"
echo ""
echo "2. Check DNS propagation:"
echo "   • Visit: https://dnschecker.org"
if [ ! -z "$CUSTOM_DOMAIN" ]; then
    echo "   • Enter: $CUSTOM_DOMAIN"
else
    echo "   • Check your domain"
fi
echo "   • Should show GitHub's IPs or joesuuf.github.io"
echo ""
echo "3. Verify Cloudflare settings:"
echo "   • DNS records are correct"
echo "   • Proxy status is 'DNS only' (gray cloud)"
echo "   • SSL/TLS mode is 'Full' or 'Full (strict)'"
echo ""
echo "4. Check GitHub Pages settings:"
echo "   • $REPO_URL/settings/pages"
echo "   • Source branch is correct ($BRANCH_NAME)"
if [ ! -z "$CUSTOM_DOMAIN" ]; then
    echo "   • Custom domain is set to: $CUSTOM_DOMAIN"
fi
echo "   • 'Enforce HTTPS' is checked"
echo ""
echo "5. Clear browser cache:"
echo "   • Hard refresh: Ctrl+Shift+R (Windows/Linux)"
echo "   • Hard refresh: Cmd+Shift+R (Mac)"
echo ""

echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}                    DEPLOYMENT SUMMARY                            ${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "✓ Files deployed to $BRANCH_NAME branch"
echo "✓ Frontend type: $FRONTEND_TYPE"
if [ ! -z "$CUSTOM_DOMAIN" ]; then
    echo "✓ Custom domain configured: $CUSTOM_DOMAIN"
    echo "✓ CNAME file created"
fi
echo "✓ .nojekyll file created (Jekyll disabled)"
echo ""
echo -e "${CYAN}Next steps:${NC}"
echo "1. Enable GitHub Pages in repository settings (if not done)"
if [ ! -z "$CUSTOM_DOMAIN" ]; then
    echo "2. Configure Cloudflare DNS (gray cloud - DNS only mode)"
    echo "3. Add custom domain in GitHub Pages settings"
    echo "4. Wait for DNS propagation (15-30 minutes)"
    echo "5. Visit: $SITE_URL"
else
    echo "2. Wait 1-2 minutes for GitHub Pages deployment"
    echo "3. Visit: $SITE_URL"
fi
echo ""
echo -e "${GREEN}Deployment complete!${NC}"
echo ""
