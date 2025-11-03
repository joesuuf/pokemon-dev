# Quick Deployment Instructions

## 🚀 Ready to Deploy!

Everything is configured and ready. Just follow these steps:

### 1. Authenticate (if not already done)
```bash
export PATH="$HOME/google-cloud-sdk/bin:$PATH"
gcloud auth login
gcloud config set project chk-poke-ocr
```

### 2. Deploy
```bash
bash deploy-to-gcp-dual.sh
```

Or skip the prompt:
```bash
AUTO_DEPLOY=1 bash deploy-to-gcp-dual.sh
```

### 3. After Deployment

You'll get URLs like:
- React: `https://storage.googleapis.com/gcp-count-la/index.html`
- Static: `https://storage.googleapis.com/gcp-count-la/v2/index.html`

### 4. Configure DNS in Cloudflare

**Simple CNAME method:**
```
Type: CNAME
Name: gcp
Target: c.storage.googleapis.com
Proxy: DNS only (gray) or Proxied (orange) - both work
```

**Or use Load Balancer** (see documentation/deployment/documentation/deployment/GCP_DEPLOYMENT_READY.md for details)

### 5. Verify

After DNS propagates (5-30 min):
- https://gcp.count.la/ → React app
- https://gcp.count.la/v2/ → Static site

---

**All configuration complete!** Just run the deployment script.
