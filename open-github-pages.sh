#!/bin/bash

# Open GitHub Pages URL
# This script opens the GitHub Pages URL for the static site

PAGES_URL="https://joesuuf.github.io/pokemon-dev"
REPO_URL="https://github.com/joesuuf/pokemon-dev"

echo "?? GitHub Pages URL: $PAGES_URL"
echo "?? Repository: $REPO_URL"
echo ""
echo "? Note: GitHub Pages may take 1-2 minutes to deploy after GitHub Actions completes."
echo "   Check deployment status at: $REPO_URL/actions"
echo ""

# Try to open the URL
if command -v open > /dev/null; then
    echo "Opening GitHub Pages URL..."
    open "$PAGES_URL"
elif command -v xdg-open > /dev/null; then
    echo "Opening GitHub Pages URL..."
    xdg-open "$PAGES_URL"
else
    echo "Please open this URL manually: $PAGES_URL"
fi
