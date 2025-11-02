# GCP vs GitHub Pages - Complete Comparison

Quick reference for deploying and comparing both platforms.

---

## 📊 Quick Comparison

| Feature | GitHub Pages | GCP Cloud Storage | GCP Cloud Run |
|---------|-------------|------------------|---------------|
| **Cost** | ✅ FREE | ~$0.15-$1/mo | ~$5-$20/mo |
| **Setup Time** | 5 min | 10 min | 15 min |
| **Build Required** | Yes (Actions) | Optional | Yes |
| **CDN** | ✅ Included (Fastly) | ✅ Available | Optional |
| **Custom Domain** | ✅ Free SSL | ✅ Free SSL | ✅ Free SSL |
| **Monitoring** | Basic | ✅ Advanced | ✅ Advanced |
| **Logs** | No | ✅ Yes | ✅ Yes |
| **SLA** | No guarantee | ✅ 99.95% | ✅ 99.95% |
| **API Proxy** | ❌ No | ❌ No | ✅ Yes |
| **Backend Support** | ❌ No | ❌ No | ✅ Yes |
| **Secrets** | GitHub Secrets | Secret Manager | Secret Manager |

---

## 🎯 Default Dev Port Mappings

### When you run `npm run dev`:
- **Port 8888**: React Main Frontend
  - Index: `index.html` (root directory)
  - Best for: Main development work

### When you run static site:
- **Port 8000**: Static Site (recommended)
  - Index: `static-site/index.html`
  - Best for: Production preview

---

## 🚀 Quick Start Guide

### Step 1: Deploy to GitHub Pages First
```bash
bash deploy-to-github-pages.sh
# Choose option 2 (Static Site - recommended)
# Enter custom domain or skip
```

**Result:** Your site is live at:
- Default: https://joesuuf.github.io/pokemon-dev/
- Custom: https://your-domain.com

---

### Step 2: Deploy to GCP for Comparison
```bash
# Install gcloud CLI first (one-time)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Deploy to GCP
bash deploy-to-gcp.sh
# Follow prompts:
# 1. Login to GCP
# 2. Select/create project
# 3. Choose frontend (Static recommended)
# 4. Choose method (Cloud Storage recommended)
# 5. Enter custom domain (optional)
```

**Result:** Your site is live on GCP:
- Storage: https://storage.googleapis.com/BUCKET/index.html
- Custom: https://your-gcp-domain.com

---

### Step 3: Compare Performance
```bash
bash compare-deployments.sh
# Enter both URLs when prompted
# Review results in comparison-results-* folder
```

---

## 📝 Todo List Tracker

Your GCP setup todo list tracks these steps:

1. ✅ **Install gcloud CLI** - Download and configure
2. ⏳ **Create GCP project** - Script will guide you
3. ⏳ **Enable APIs** - Automatic during deployment
4. ⏳ **Set up billing** - Required for GCP
5. ⏳ **Choose deployment method** - Script offers options
6. ⏳ **Deploy** - Automated by script
7. ⏳ **Custom domain** - Optional configuration
8. ⏳ **SSL/TLS** - Automatic
9. ⏳ **Cloud CDN** - Optional enhancement
10. ⏳ **Test & Compare** - Use comparison script
11. ⏳ **Monitoring** - Set up in GCP Console
12. ⏳ **Cost tracking** - Monitor for 1 week

**Track progress with:** The `deploy-to-gcp.sh` script guides you through each step.

---

## 💰 Cost Breakdown

### GitHub Pages (Current)
```
Monthly Cost: $0 (FREE)
- Bandwidth: Unlimited
- Build minutes: 2,000/month free
- Storage: 1GB
- Custom domain: Free SSL

Total: $0/month
```

### GCP Cloud Storage + CDN (Recommended)
```
Monthly Cost: ~$0.15 - $1.00
- Storage (1GB): $0.02
- Network egress (10GB): $0.12
- Cloud CDN cache: $0.01-0.80
- Requests (100K): Negligible

Total: $0.15 - $1.00/month
```

### GCP Cloud Run
```
Monthly Cost: ~$5 - $20
- CPU time: $0.10/100K requests
- Memory: $0.08/100K requests
- Network egress: $0.12/GB
- Always-on: Optional ($5-10)

Total: $5 - $20/month
```

---

## 🔑 API Key Handling

### Your Current Setup: GitHub Repo Secret

You mentioned having a GitHub repository secret. Here's how it works:

#### On GitHub Pages:
```yaml
# .github/workflows/deploy.yml (example)
env:
  VITE_POKEMON_API_KEY: ${{ secrets.POKEMON_API_KEY }}
```

#### On GCP Cloud Storage:
```bash
# API key is client-side (same as GitHub Pages)
# Injected during build or loaded from config
```

#### On GCP Cloud Run (Most Secure):
```bash
# Store in Secret Manager
echo -n "your-key" | gcloud secrets create pokemon-api-key --data-file=-

# Deploy with secret
gcloud run deploy SERVICE \
  --set-secrets="POKEMON_API_KEY=pokemon-api-key:latest"
```

**See:** `API_KEYS_SETUP.md` for complete guide

---

## 📈 Performance Testing Results Template

Fill this in after running `compare-deployments.sh`:

| Metric | GitHub Pages | GCP Storage | Winner |
|--------|-------------|-------------|--------|
| Avg Response Time | ___ ms | ___ ms | ? |
| Lighthouse Performance | ___ | ___ | ? |
| Lighthouse Accessibility | ___ | ___ | ? |
| Load Test (req/sec) | ___ | ___ | ? |
| Failed Requests | ___ | ___ | ? |
| Global CDN | ✅ Yes | ✅ Yes | Tie |
| Monitoring | ❌ No | ✅ Yes | GCP |
| Cost | ✅ $0 | ~$0.50 | GitHub |

---

## 🎯 Decision Matrix

### Choose GitHub Pages If:
- ✅ Cost is primary concern (free)
- ✅ Simple static site
- ✅ Open source project
- ✅ No monitoring needed
- ✅ GitHub Actions already used
- ✅ Traffic < 100K visits/month

### Choose GCP If:
- ✅ Need advanced monitoring/logging
- ✅ Require guaranteed SLA (99.95%)
- ✅ Enterprise requirements
- ✅ Custom infrastructure control
- ✅ Integration with other GCP services
- ✅ Need backend API proxy
- ✅ Budget allows $1-20/month

### Recommendation:
**For Pokemon TCG Search:** Start with **GitHub Pages** (free), add GCP later if monitoring/SLA needed.

---

## 🔄 Deployment Workflows

### GitHub Pages Workflow:
```
Code Change → Git Push → GitHub Actions → Build → Deploy → Live
Time: 2-3 minutes
Cost: $0
```

### GCP Cloud Storage Workflow:
```
Code Change → Local Build → Upload to Bucket → Live
Time: 1-2 minutes
Cost: ~$0.50/month
```

### GCP Cloud Run Workflow:
```
Code Change → Build Container → Deploy → Live
Time: 3-5 minutes
Cost: ~$10/month
```

---

## 📋 Commands Cheat Sheet

### Local Development:
```bash
# Start React (port 8888)
npm run dev

# Start static site (port 8000)
cd static-site && python3 -m http.server 8000

# Interactive dev server selector
bash start-local-dev.sh
```

### Deployment:
```bash
# Deploy to GitHub Pages
bash deploy-to-github-pages.sh

# Deploy to GCP
bash deploy-to-gcp.sh

# Compare both
bash compare-deployments.sh
```

### GCP Management:
```bash
# View deployments
gcloud storage buckets list          # Storage
gcloud run services list              # Cloud Run

# View logs
gcloud logging read --limit 50

# View costs
gcloud billing accounts list
```

### GitHub Pages:
```bash
# Check deployment status
# Visit: https://github.com/joesuuf/pokemon-dev/deployments

# View via gh CLI (if installed)
gh run list
gh run view [run-id]
```

---

## 🌍 Custom Domain Setup

### Cloudflare DNS (Works for Both)

#### For GitHub Pages:
```
Type: CNAME
Name: subdomain (or @)
Target: joesuuf.github.io
Proxy: DNS only (gray cloud) ← REQUIRED
```

#### For GCP Cloud Storage:
```
Type: CNAME
Name: subdomain
Target: c.storage.googleapis.com
Proxy: DNS only OR Proxied (both work!)
```

**Key Difference:** GCP allows orange cloud (proxied), GitHub Pages requires gray cloud (DNS only).

---

## 🧪 Testing Checklist

After deploying to both platforms:

- [ ] Test site loads on both URLs
- [ ] Check custom domain (if configured)
- [ ] Verify SSL certificate works
- [ ] Test from multiple locations (pingdom, webpagetest)
- [ ] Run Lighthouse audits
- [ ] Check Pokemon API calls work
- [ ] Test on mobile devices
- [ ] Compare load times
- [ ] Review monitoring dashboards (GCP only)
- [ ] Track costs for 1 week
- [ ] Make final platform decision

---

## 📊 1-Week Cost Monitoring

Track actual costs:

| Day | GitHub Pages | GCP | Notes |
|-----|-------------|-----|-------|
| Day 1 | $0 | $? | Check GCP billing |
| Day 2 | $0 | $? | |
| Day 3 | $0 | $? | |
| Day 4 | $0 | $? | |
| Day 5 | $0 | $? | |
| Day 6 | $0 | $? | |
| Day 7 | $0 | $? | |
| **Total** | **$0** | **$?** | |

**Check GCP costs:** https://console.cloud.google.com/billing

---

## 🎓 Key Learnings

### GitHub Pages Pros:
- ✅ Completely free
- ✅ Simple setup
- ✅ Works great for static sites
- ✅ Automatic builds with Actions
- ✅ Good performance (Fastly CDN)

### GitHub Pages Cons:
- ❌ No monitoring/logs
- ❌ No SLA guarantee
- ❌ Limited to static content
- ❌ 1GB size limit
- ❌ DNS-only mode required for custom domains

### GCP Pros:
- ✅ Advanced monitoring/logging
- ✅ Guaranteed SLA (99.95%)
- ✅ Secret Manager integration
- ✅ Backend support (Cloud Run)
- ✅ Enterprise features
- ✅ Full control

### GCP Cons:
- ❌ Costs money (~$0.15-$50/month)
- ❌ More complex setup
- ❌ Requires billing account
- ❌ Steeper learning curve
- ❌ Over-engineered for simple sites

---

## 🏁 Final Recommendations

### For This Project (Pokemon TCG Search):

**Phase 1 - Start Simple:**
1. Deploy to **GitHub Pages** (free)
2. Use static site version (8.8/10 score, 15x smaller)
3. Add Cloudflare DNS for custom domain
4. Monitor with free tools (UptimeRobot, Google Analytics)

**Phase 2 - If Needed:**
1. Deploy to **GCP Cloud Storage** for comparison
2. Test performance for 1 week
3. Compare costs (should be ~$0.50/month)
4. Decide based on actual needs

**Phase 3 - Scale Up (Optional):**
1. Move to **GCP Cloud Run** if backend needed
2. Enable advanced monitoring
3. Set up alerting
4. Budget $10-20/month

### Best Practice:
**Start free (GitHub Pages), upgrade only if needed (GCP)**

For most static sites: GitHub Pages is sufficient ✅

---

## 📚 All Documentation

Quick access to all guides:

1. **AUDIT_SUMMARY.md** - Complete audit results
2. **AUDIT_REPORT_REACT.md** - React audit (50+ pages)
3. **AUDIT_REPORT_STATIC_SITE.md** - Static audit (45+ pages)
4. **DEV_PORTS_GUIDE.md** - Port mappings and local dev
5. **GCP_SETUP_GUIDE.md** - Complete GCP guide (130+ pages)
6. **API_KEYS_SETUP.md** - Secret management guide
7. **GCP_VS_GITHUB_PAGES.md** - This file

### Scripts:
- `deploy-to-github-pages.sh` - GitHub Pages deployment
- `deploy-to-gcp.sh` - GCP deployment
- `compare-deployments.sh` - Performance comparison
- `start-local-dev.sh` - Local dev server
- `extract-react-app.sh` - Extract React app
- `extract-static-site.sh` - Extract static site

---

## ✅ Next Steps

1. **Now:** Deploy to GitHub Pages (free, quick test)
   ```bash
   bash deploy-to-github-pages.sh
   ```

2. **Today:** Test your GitHub Pages deployment
   - Verify site works
   - Test custom domain (if configured)
   - Run Lighthouse audit

3. **This Week:** Set up GCP for comparison
   ```bash
   bash deploy-to-gcp.sh
   ```

4. **Next Week:** Run performance comparison
   ```bash
   bash compare-deployments.sh
   ```

5. **After 1 Week:** Review costs and make decision
   - Check GCP billing dashboard
   - Compare performance metrics
   - Choose final platform

---

**Last Updated:** November 2, 2025
**Status:** Ready for testing both platforms
**Recommendation:** Start with GitHub Pages (free) ✅
