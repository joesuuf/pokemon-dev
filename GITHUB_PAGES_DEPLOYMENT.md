# GitHub Pages Deployment Guide

## Quick Deploy

1. **Automatic Deployment (via GitHub Actions)**
   - Push to `test-static` branch
   - GitHub Actions will automatically deploy to GitHub Pages
   - Check status: https://github.com/joesuuf/pokemon-dev/actions

2. **Manual Deployment Script**
   ```bash
   ./deploy-static-pages.sh
   ```

3. **Open GitHub Pages URL**
   ```bash
   ./open-github-pages.sh
   ```

## GitHub Pages URL

**Live Site**: https://joesuuf.github.io/pokemon-dev/

## Deployment Status

- ? Workflow created: `.github/workflows/deploy-static-pages.yml`
- ? Deployment script: `deploy-static-pages.sh`
- ? Static site ready: `static-site/` directory
- ? Committed and pushed to `test-static` branch

## How It Works

1. When you push to `test-static` branch, GitHub Actions workflow triggers
2. Workflow copies `static-site/*` files to `dist/` directory
3. GitHub Pages deploys from `dist/` directory
4. Site is live at: https://joesuuf.github.io/pokemon-dev/

## Troubleshooting

If GitHub Pages doesn't update:
1. Check GitHub Actions: https://github.com/joesuuf/pokemon-dev/actions
2. Verify GitHub Pages settings in repository Settings > Pages
3. Ensure GitHub Pages source is set to "GitHub Actions" (not branch)

## Files Deployed

- `static-site/index.html` - Main HTML file
- `static-site/styles/` - CSS files
- `static-site/scripts/` - JavaScript files

All files are pure HTML/CSS/JavaScript - no build step required!
