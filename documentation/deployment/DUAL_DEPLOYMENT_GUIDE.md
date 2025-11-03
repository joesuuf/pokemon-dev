## Pokemon TCG - Dual Version Deployment Guide

Complete guide for deploying both React and Static versions side-by-side.

---

## 🎯 Deployment Architecture

### git.count.la (GitHub Pages)
```
https://git.count.la/
├── /              → React TypeScript version (main)
└── /v2/           → Static HTML/CSS/JS version
```

### gcp.count.la (Google Cloud Platform)
```
https://gcp.count.la/
├── /              → React TypeScript version (main)
└── /v2/           → Static HTML/CSS/JS version
```

### Cross-Navigation
- **React version:** Footer link "Static v2 →" points to `/v2/`
- **Static version:** Footer link "← React Version" points to `/`

---

## 🚀 Quick Start

### Option 1: Deploy Both Platforms

```bash
# Deploy to GitHub Pages (git.count.la)
git push origin main  # Triggers workflow automatically

# Deploy to GCP (gcp.count.la)
bash deploy-to-gcp-dual.sh
```

### Option 2: Test Locally First

```bash
# Build dual deployment package
npm run build
mkdir -p dist/v2
cp -r static-site/* dist/v2/

# Serve locally
npx http-server dist -p 8080

# Test:
# React: http://localhost:8080/
# Static: http://localhost:8080/v2/
```

---

## 📦 What's Included

### Code Changes Made

#### 1. React App (`src/App.tsx`)
Added footer link to static version:
```tsx
<a
  href="/v2/"
  className="version-footer"
  title="Switch to Static HTML/CSS Version"
>
  Static v2 →
</a>
```

#### 2. React Styles (`src/styles/App.css`)
Added version footer styling:
```css
.version-footer {
  position: fixed;
  bottom: 15px;
  right: 15px;
  background: rgba(0, 61, 165, 0.9);
  /* ... more styles */
}
```

#### 3. GitHub Actions Workflow
**File:** `.github/workflows/deploy-dual-github.yml`
- Builds React app with API key
- Copies static site to `dist/v2/`
- Adds footer link to static version
- Deploys to GitHub Pages
- Configures `git.count.la` domain

#### 4. GCP Deployment Script
**File:** `deploy-to-gcp-dual.sh`
- Builds React app
- Adds static site to v2/
- Uploads to Cloud Storage
- Configures for `gcp.count.la`

---

## 🌐 Cloudflare DNS Configuration

### For git.count.la (GitHub Pages)

**In Cloudflare Dashboard:**
```
Type: CNAME
Name: git
Target: joesuuf.github.io
Proxy Status: DNS only (gray cloud) ← REQUIRED
TTL: Auto
```

**Important:** GitHub Pages requires gray cloud (DNS only). Orange cloud will NOT work.

---

### For gcp.count.la (Google Cloud Storage)

**Option A: Direct to Storage (Simple)**
```
Type: CNAME
Name: gcp
Target: c.storage.googleapis.com
Proxy Status: DNS only OR Proxied (both work)
TTL: Auto
```

**Option B: With Load Balancer (Recommended for production)**

1. Create HTTPS Load Balancer in GCP Console
2. Get static IP address from load balancer
3. Configure DNS:
```
Type: A
Name: gcp
IPv4 Address: [Load Balancer IP]
Proxy Status: DNS only OR Proxied (both work)
TTL: Auto
```

---

## 📋 Deployment Checklist

### GitHub Pages (git.count.la)

- [ ] Code committed to `main` branch
- [ ] `.github/workflows/deploy-dual-github.yml` exists
- [ ] GitHub Actions workflow triggered
- [ ] Check deployment status:
  - Go to: https://github.com/joesuuf/pokemon-dev/actions
  - Verify workflow succeeded
- [ ] Configure Cloudflare DNS (CNAME → joesuuf.github.io)
- [ ] Set DNS only mode (gray cloud)
- [ ] Wait for DNS propagation (5-30 min)
- [ ] Test https://git.count.la/
- [ ] Test https://git.count.la/v2/
- [ ] Verify footer links work both ways

### GCP (gcp.count.la)

- [ ] Install gcloud CLI
- [ ] Authenticate: `gcloud auth login`
- [ ] Run: `bash deploy-to-gcp-dual.sh`
- [ ] Verify deployment succeeded
- [ ] Get Cloud Storage URL or Load Balancer IP
- [ ] Configure Cloudflare DNS
- [ ] Wait for DNS propagation (5-30 min)
- [ ] Test https://gcp.count.la/
- [ ] Test https://gcp.count.la/v2/
- [ ] Verify footer links work both ways

---

## 🧪 Testing

### Local Testing

```bash
# Build
npm run build

# Add v2
mkdir -p dist/v2
cp -r static-site/* dist/v2/

# Serve
npx http-server dist -p 8080

# Test URLs:
# http://localhost:8080/      → React
# http://localhost:8080/v2/   → Static
```

### Production Testing

```bash
# GitHub Pages
curl -I https://git.count.la/
curl -I https://git.count.la/v2/

# GCP
curl -I https://gcp.count.la/
curl -I https://gcp.count.la/v2/

# Check footer links work
# Open in browser and click footer links
```

---

## 🔑 API Key Configuration

Your Pokemon TCG API key is automatically injected during build.

### GitHub Actions
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

---

## 📊 Deployment Comparison

### git.count.la (GitHub Pages)

**Pros:**
- ✅ Free ($0/month)
- ✅ Automatic deployments via GitHub Actions
- ✅ Built-in CI/CD
- ✅ Simple setup

**Cons:**
- ❌ Must use gray cloud (DNS only) in Cloudflare
- ❌ No advanced monitoring
- ❌ 1GB size limit

**Best for:** Development, testing, free hosting

---

### gcp.count.la (Google Cloud)

**Pros:**
- ✅ Works with orange cloud (proxied) in Cloudflare
- ✅ Advanced monitoring and logging
- ✅ Cloud CDN available
- ✅ Guaranteed SLA (99.95%)
- ✅ Enterprise features

**Cons:**
- ❌ Costs money (~$0.15-$1/month for storage)
- ❌ Manual deployment
- ❌ More complex setup

**Best for:** Production, enterprise, advanced features

---

## 🔄 Update Workflow

### Update React Version

1. Make changes to `src/` files
2. Commit and push to `main` branch
3. GitHub Actions automatically rebuilds and deploys
4. For GCP: Run `bash deploy-to-gcp-dual.sh`

### Update Static Version

1. Make changes to `static-site/` files
2. Commit and push to `main` branch
3. GitHub Actions automatically includes v2/ in deploy
4. For GCP: Run `bash deploy-to-gcp-dual.sh`

---

## 🎨 Customization

### Change Footer Link Style

Edit `src/styles/App.css`:
```css
.version-footer {
  /* Change colors, position, etc. */
  background: rgba(0, 61, 165, 0.9);  /* Blue for React */
  bottom: 15px;
  right: 15px;
}
```

### Change Link Text

Edit `src/App.tsx`:
```tsx
<a href="/v2/" className="version-footer">
  Your Custom Text →
</a>
```

---

## 🐛 Troubleshooting

### Issue: git.count.la not loading

**Check:**
1. GitHub Actions workflow succeeded?
   - https://github.com/joesuuf/pokemon-dev/actions
2. DNS configured correctly in Cloudflare?
   - CNAME → joesuuf.github.io
   - Gray cloud (DNS only)
3. DNS propagated?
   - Check: https://dnschecker.org
4. GitHub Pages enabled?
   - https://github.com/joesuuf/pokemon-dev/settings/pages

---

### Issue: gcp.count.la not loading

**Check:**
1. Deployment succeeded?
   - Check terminal output from deploy script
2. Bucket is public?
   - `gsutil iam ch allUsers:objectViewer gs://gcp-count-la`
3. DNS configured in Cloudflare?
4. DNS propagated?
   - Check: https://dnschecker.org

---

### Issue: Footer links not working

**Check:**
1. React footer added to `src/App.tsx`?
2. CSS added to `src/styles/App.css`?
3. Static footer added during deployment?
   - Check `dist/v2/index.html` has footer
4. Paths are relative (`/v2/` not absolute)?

---

### Issue: API key not working

**Check:**
1. GitHub Secret configured?
   - https://github.com/joesuuf/pokemon-dev/settings/secrets/actions
2. Workflow uses secret in build step?
   - Check `.github/workflows/deploy-dual-github.yml`
3. Local `.env.local` file exists?

---

## 📈 Performance Monitoring

### GitHub Pages
- **Built-in:** Deployment status in Actions
- **External:** Use UptimeRobot, Pingdom (free tiers)
- **Analytics:** Add Google Analytics to both versions

### GCP
- **Cloud Monitoring:** https://console.cloud.google.com/monitoring
- **Cloud Logging:** https://console.cloud.google.com/logs
- **Metrics:** Request count, response time, errors

---

## 💰 Cost Tracking

### GitHub Pages
```
Monthly Cost: $0 (FREE)
```

### GCP (Storage Only)
```
Monthly Cost: ~$0.15 - $1.00
- Storage (1GB): $0.02
- Network (10GB): $0.12
- Requests: Negligible

Total: ~$0.15/month
```

### GCP (With Load Balancer + CDN)
```
Monthly Cost: ~$1.00 - $5.00
- Storage: $0.02
- Load Balancer: $18/month (but prorated)
- CDN: $0.08/GB
- SSL Certificate: Free (Google-managed)

Total: ~$1-5/month depending on traffic
```

---

## 🎯 Recommended Setup

### Development/Testing
- Use **git.count.la** (GitHub Pages)
- Free, automatic deployments
- Perfect for testing

### Production
- **Option A:** Keep GitHub Pages (free, good performance)
- **Option B:** Use **gcp.count.la** if you need:
  - Advanced monitoring
  - Cloud CDN
  - Enterprise SLA
  - Integration with other GCP services

---

## 📚 Related Documentation

- **documentation/audits/collection/AUDIT_SUMMARY.md** - Performance comparison (8.8/10 static vs 8.2/10 React)
- **documentation/guides/DEV_PORTS_GUIDE.md** - Local development ports
- **documentation/api/API_KEYS_SETUP.md** - Secret management
- **documentation/guides/GCP_SETUP_GUIDE.md** - Detailed GCP instructions
- **documentation/process/GITHUB_SETUP_REVIEW.md** - GitHub configuration review

---

## ✅ Success Criteria

Deployment is successful when:

- ✅ git.count.la loads React version
- ✅ git.count.la/v2/ loads static version
- ✅ gcp.count.la loads React version
- ✅ gcp.count.la/v2/ loads static version
- ✅ Footer link on React goes to /v2/
- ✅ Footer link on Static goes back to /
- ✅ Both versions work on both domains
- ✅ Search functionality works on all pages
- ✅ No console errors
- ✅ HTTPS works on both domains

---

## 🎬 Quick Commands

```bash
# Deploy to GitHub Pages
git push origin main

# Deploy to GCP
bash deploy-to-gcp-dual.sh

# Test locally
npm run build && npx http-server dist -p 8080

# Check GitHub Actions
open https://github.com/joesuuf/pokemon-dev/actions

# Check GCP Console
open https://console.cloud.google.com/storage

# Test DNS propagation
open https://dnschecker.org
```

---

## 🤝 Need Help?

1. Check the troubleshooting section above
2. Review related documentation
3. Check GitHub Actions logs for deployment issues
4. Verify DNS configuration in Cloudflare
5. Test with curl commands to isolate issues

---

**Last Updated:** November 2, 2025
**Deployment Type:** Dual Version (React + Static v2)
**Domains:** git.count.la (GitHub), gcp.count.la (GCP)
**Status:** Ready for deployment
