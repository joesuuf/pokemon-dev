# Dual Deployment Setup - Complete Summary

**Created:** November 2, 2025
**For:** Pokemon TCG Search - React + Static Versions
**Domains:** git.count.la & gcp.count.la

---

## ✅ COMPLETE - Ready to Deploy!

All code, workflows, and scripts have been created and committed to your branch:
`claude/run-site-through-011CUjUQ4obsFRz7K1pzihx8`

---

## 🎯 What You Requested

1. ✅ **Two frontends**: React TypeScript + Static HTML/CSS
2. ✅ **Two domains**: git.count.la & gcp.count.la
3. ✅ **React as index**: Main page on both domains
4. ✅ **Static in /v2/ folder**: Accessible via `/v2/` on both
5. ✅ **Cross-navigation**: Footer links between versions
6. ✅ **Public & persistent**: Both deployments are permanent
7. ✅ **Appropriate workflows**: GitHub Actions + GCP script

---

## 🌐 Deployment URLs

### git.count.la (GitHub Pages)
- **React Version:** https://git.count.la/
- **Static Version:** https://git.count.la/v2/
- **Platform:** GitHub Pages (Free)
- **Deployment:** Automatic via GitHub Actions

### gcp.count.la (Google Cloud Platform)
- **React Version:** https://gcp.count.la/
- **Static Version:** https://gcp.count.la/v2/
- **Platform:** GCP Cloud Storage (~$0.15-1/month)
- **Deployment:** Manual via script

---

## 🔗 Cross-Navigation

Both versions have footer links for easy switching:

### React Version (Blue footer, bottom-right):
```
"Static v2 →"
```
Clicks take you to `/v2/` (static version)

### Static Version (Red footer, bottom-right):
```
"← React Version"
```
Clicks take you back to `/` (React version)

---

## 🖥️ Local Testing Ports

### React Development Server
```bash
npm run dev
```
- **Port:** 8888
- **URL:** http://localhost:8888
- **Index:** `index.html` (root directory)

### Static Site Development Server
```bash
cd static-site && python3 -m http.server 8000
```
- **Port:** 8000
- **URL:** http://localhost:8000
- **Index:** `static-site/index.html`

---

## 🚀 Deployment Instructions

### Deploy to GitHub Pages (git.count.la)

**Option 1: Automatic (Recommended)**
```bash
# Merge your branch to main
git checkout main
git merge claude/run-site-through-011CUjUQ4obsFRz7K1pzihx8
git push origin main

# GitHub Actions workflow automatically:
# 1. Builds React app with your API key
# 2. Copies static site to dist/v2/
# 3. Deploys to GitHub Pages
```

**Option 2: Manual Trigger**
1. Go to: https://github.com/joesuuf/pokemon-dev/actions
2. Select "Deploy Dual Version to GitHub Pages"
3. Click "Run workflow"

**Monitor Deployment:**
- https://github.com/joesuuf/pokemon-dev/actions

---

### Deploy to GCP (gcp.count.la)

**Prerequisites:**
```bash
# Install gcloud CLI (one-time)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

**Deploy:**
```bash
# Run the deployment script
bash deploy-to-gcp-dual.sh

# Script will:
# 1. Authenticate with GCP
# 2. Build React app
# 3. Add static site to v2/
# 4. Upload to Cloud Storage
# 5. Configure public access
```

---

## 🌐 Cloudflare DNS Setup

### For git.count.la (GitHub Pages)

**In Cloudflare Dashboard:**
1. Go to your domain's DNS settings
2. Add a CNAME record:
   ```
   Type: CNAME
   Name: git
   Target: joesuuf.github.io
   Proxy Status: DNS only (gray cloud ☁️) ← CRITICAL!
   TTL: Auto
   ```

**Important:** GitHub Pages requires gray cloud (DNS only). Orange cloud will NOT work.

---

### For gcp.count.la (Google Cloud)

**Option A: Direct to Storage (Simpler)**
```
Type: CNAME
Name: gcp
Target: c.storage.googleapis.com
Proxy Status: DNS only OR Proxied (both work ✅)
TTL: Auto
```

**Option B: With Load Balancer (Better performance)**
1. Create HTTPS Load Balancer in GCP Console
2. Point backend to Cloud Storage bucket
3. Enable Cloud CDN
4. Get Load Balancer IP
5. Configure DNS:
   ```
   Type: A
   Name: gcp
   IPv4 Address: [Load Balancer IP]
   Proxy Status: DNS only OR Proxied (both work ✅)
   TTL: Auto
   ```

---

## 📋 Step-by-Step Deployment Checklist

### Phase 1: Merge to Main Branch

- [ ] Review all changes in your branch
- [ ] Checkout main: `git checkout main`
- [ ] Merge: `git merge claude/run-site-through-011CUjUQ4obsFRz7K1pzihx8`
- [ ] Push: `git push origin main`

### Phase 2: GitHub Pages (git.count.la)

- [ ] GitHub Actions workflow triggers automatically
- [ ] Monitor workflow: https://github.com/joesuuf/pokemon-dev/actions
- [ ] Wait for "Deploy Dual Version to GitHub Pages" to complete (2-3 min)
- [ ] Check deployment succeeded (green checkmark)
- [ ] Configure Cloudflare DNS (CNAME → joesuuf.github.io, gray cloud)
- [ ] Wait for DNS propagation (5-30 minutes)
- [ ] Test: https://git.count.la/
- [ ] Test: https://git.count.la/v2/
- [ ] Verify footer links work

### Phase 3: GCP (gcp.count.la)

- [ ] Install gcloud CLI (if not already installed)
- [ ] Run: `bash deploy-to-gcp-dual.sh`
- [ ] Follow script prompts
- [ ] Verify deployment succeeded
- [ ] Note the Cloud Storage URL
- [ ] Configure Cloudflare DNS (CNAME or A record)
- [ ] Wait for DNS propagation (5-30 minutes)
- [ ] Test: https://gcp.count.la/
- [ ] Test: https://gcp.count.la/v2/
- [ ] Verify footer links work

---

## 🧪 Testing Your Deployments

### Quick Tests

```bash
# GitHub Pages
curl -I https://git.count.la/
curl -I https://git.count.la/v2/

# GCP
curl -I https://gcp.count.la/
curl -I https://gcp.count.la/v2/
```

### Browser Tests

1. **Open React Version:**
   - git.count.la → Should load React app
   - gcp.count.la → Should load React app

2. **Check Footer Link:**
   - Click "Static v2 →" in bottom-right corner
   - Should navigate to `/v2/`

3. **Open Static Version:**
   - git.count.la/v2/ → Should load static site
   - gcp.count.la/v2/ → Should load static site

4. **Check Footer Link:**
   - Click "← React Version" in bottom-right corner
   - Should navigate back to `/`

5. **Test Functionality:**
   - Search for a Pokemon card on both versions
   - Verify results display correctly
   - Check that footer links always work

---

## 📊 What Was Changed

### Code Changes

1. **src/App.tsx**
   - Added footer link to static version

2. **src/styles/App.css**
   - Added `.version-footer` styling

### New Files Created

1. **.github/workflows/deploy-dual-github.yml**
   - GitHub Actions workflow for automatic deployment
   - Builds React + copies static to v2/
   - Deploys to GitHub Pages with git.count.la domain

2. **deploy-to-gcp-dual.sh**
   - GCP deployment script
   - Builds React + adds static to v2/
   - Uploads to Cloud Storage

3. **documentation/guides/documentation/guides/DUAL_DEPLOYMENT_GUIDE.md**
   - Complete deployment documentation
   - Step-by-step instructions
   - Troubleshooting guide

4. **documentation/deployment/documentation/deployment/DEPLOYMENT_SUMMARY.md**
   - This file - quick reference

---

## 🔑 API Key Handling

Your Pokemon TCG API key (stored in GitHub Secrets) is automatically injected during builds.

### GitHub Actions
The workflow includes:
```yaml
env:
  VITE_POKEMON_API_KEY: ${{ secrets.POKEMON_API_KEY }}
run: npm run build
```

### Local Development
Create `.env.local`:
```
VITE_POKEMON_API_KEY=your-api-key-here
```
(This file is in .gitignore and won't be committed)

---

## 💰 Cost Comparison

### git.count.la (GitHub Pages)
```
Monthly Cost: $0 (FREE)
```

### gcp.count.la (Cloud Storage)
```
Monthly Cost: ~$0.15 - $1.00
- Storage: $0.02/month
- Network: $0.12/month
- Requests: Negligible
```

---

## 🐛 Troubleshooting

### DNS Not Resolving

**Check DNS propagation:**
- Visit: https://dnschecker.org
- Enter: git.count.la (or gcp.count.la)
- Wait 5-30 minutes if still propagating

### GitHub Pages Deployment Failed

**Check workflow:**
1. Go to: https://github.com/joesuuf/pokemon-dev/actions
2. Click failed workflow
3. Review error logs
4. Common issues:
   - Build failed: Check package.json, dependencies
   - API key missing: Verify GitHub Secret exists
   - Permissions: Ensure workflow has pages:write permission

### Footer Links Not Working

**Verify:**
1. React footer added to `src/App.tsx`
2. CSS added to `src/styles/App.css`
3. Static footer injected during deployment
4. Links use relative paths (`/v2/` not absolute)

### GCP Deployment Failed

**Check:**
1. gcloud CLI installed: `gcloud --version`
2. Authenticated: `gcloud auth list`
3. Billing enabled for project
4. APIs enabled (Storage, Compute)
5. Bucket name available

---

## 📚 Documentation Files

All documentation has been created:

1. **documentation/deployment/documentation/deployment/DEPLOYMENT_SUMMARY.md** (this file) - Quick start guide
2. **documentation/guides/documentation/guides/DUAL_DEPLOYMENT_GUIDE.md** - Complete guide with all details
3. **documentation/guides/documentation/guides/DEV_PORTS_GUIDE.md** - Local development ports
4. **documentation/audits/collection/documentation/audits/collection/AUDIT_SUMMARY.md** - Performance audit results
5. **documentation/guides/documentation/guides/GCP_SETUP_GUIDE.md** - Detailed GCP instructions
6. **documentation/api/documentation/api/API_KEYS_SETUP.md** - Secret management
7. **documentation/process/documentation/process/GITHUB_SETUP_REVIEW.md** - GitHub configuration review

---

## ✅ Success Indicators

Your deployment is successful when:

- ✅ git.count.la shows React version
- ✅ git.count.la/v2/ shows static version
- ✅ gcp.count.la shows React version
- ✅ gcp.count.la/v2/ shows static version
- ✅ Footer link on React navigates to /v2/
- ✅ Footer link on Static navigates back to /
- ✅ Search works on all 4 pages
- ✅ No console errors
- ✅ HTTPS works (SSL certificates)
- ✅ Both deployments are publicly accessible

---

## 🎉 You're Ready!

Everything is set up and ready to deploy:

1. **Merge to main** → GitHub Pages deploys automatically
2. **Run GCP script** → Manual GCP deployment
3. **Configure DNS** → Point domains to deployments
4. **Test** → Verify everything works

**All code is committed to:** `claude/run-site-through-011CUjUQ4obsFRz7K1pzihx8`

---

## 🆘 Need Help?

1. Check **documentation/guides/documentation/guides/DUAL_DEPLOYMENT_GUIDE.md** for detailed instructions
2. Review workflow logs in GitHub Actions
3. Test locally first: `npm run build && npx http-server dist -p 8080`
4. Verify DNS with dnschecker.org
5. Check GCP Console for deployment status

---

**Status:** ✅ READY FOR DEPLOYMENT
**Branch:** claude/run-site-through-011CUjUQ4obsFRz7K1pzihx8
**Next Step:** Merge to main and configure DNS
