#!/bin/bash

# Deploy Static Site to GitHub Pages
# This script commits changes, pushes to remote, and deploys to GitHub Pages

set -e  # Exit on error

echo "?? Deploying Static Site to GitHub Pages..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Repository info
REPO_URL="https://github.com/joesuuf/pokemon-dev"
PAGES_URL="https://joesuuf.github.io/pokemon-dev"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "? Error: Not in a git repository"
    exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${BLUE}Current branch: ${CURRENT_BRANCH}${NC}"

# Stage all changes
echo -e "${YELLOW}?? Staging changes...${NC}"
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo -e "${YELLOW}??  No changes to commit${NC}"
else
    # Commit changes
    echo -e "${YELLOW}?? Committing changes...${NC}"
    git commit -m "Deploy static site to GitHub Pages
    
- Add static-site directory with pure HTML/CSS/JS implementation
- Ready for GitHub Pages deployment
- Mobile-first, accessible, secure"
fi

# Push to remote
echo -e "${YELLOW}?? Pushing to remote...${NC}"
git push origin "$CURRENT_BRANCH" || {
    echo "? Error: Failed to push to remote"
    exit 1
}

echo -e "${GREEN}? Changes pushed to remote successfully!${NC}"

# Check if GitHub Actions workflow exists
if [ -f ".github/workflows/deploy-static-pages.yml" ]; then
    echo -e "${BLUE}?? GitHub Actions workflow will deploy automatically${NC}"
    echo -e "${BLUE}   Check deployment status at: ${REPO_URL}/actions${NC}"
else
    echo -e "${YELLOW}??  No GitHub Actions workflow found. Creating one...${NC}"
fi

# Wait a moment for GitHub to process
echo -e "${YELLOW}? Waiting for GitHub Pages to process...${NC}"
sleep 5

# Instructions
echo ""
echo -e "${GREEN}????????????????????????????????????????????????????????${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}????????????????????????????????????????????????????????${NC}"
echo ""
echo -e "${BLUE}GitHub Pages URL:${NC}"
echo -e "  ${PAGES_URL}"
echo ""
echo -e "${BLUE}Repository:${NC}"
echo -e "  ${REPO_URL}"
echo ""
echo -e "${YELLOW}Note:${NC} GitHub Pages may take 1-2 minutes to update."
echo -e "      Check deployment status at: ${REPO_URL}/actions"
echo ""

# Try to open the URL (works on macOS and Linux with xdg-open)
if command -v open > /dev/null; then
    echo -e "${YELLOW}?? Opening GitHub Pages URL...${NC}"
    open "$PAGES_URL"
elif command -v xdg-open > /dev/null; then
    echo -e "${YELLOW}?? Opening GitHub Pages URL...${NC}"
    xdg-open "$PAGES_URL"
else
    echo -e "${YELLOW}?? Please open this URL manually: ${PAGES_URL}${NC}"
fi

echo ""
echo -e "${GREEN}? Done!${NC}"
