# GCP Deployment Configuration Summary

## ✅ Configuration Complete

### Project Details
- **Project ID**: `chk-poke-ocr`
- **Project Number**: `834937477737`
- **Bucket Name**: `gcp-count-la`
- **Region**: `us-central1`
- **Domain**: `gcp.count.la`

### Deployment Structure
- **React App**: `/` (index.html) - Default landing page
- **Static Site**: `/v2/` (index.html) - Alternative version

### Scripts Updated
- ✅ `deploy-to-gcp-dual.sh` - Updated with your project ID
- ✅ `prepare-gcp-deploy.sh` - Created for build preparation
- ✅ Both scripts handle PATH for gcloud automatically

---

## 🚀 Deployment Steps

### Step 1: Authenticate with GCP

```bash
# Add gcloud to PATH (if not already in .bashrc)
export PATH="$HOME/google-cloud-sdk/bin:$PATH"

# Authenticate
gcloud auth login

# Verify authentication
gcloud auth list

# Set project
gcloud config set project chk-poke-ocr
```

### Step 2: Enable Required APIs

```bash
gcloud services enable storage-api.googleapis.com --project=chk-poke-ocr
gcloud services enable compute.googleapis.com --project=chk-poke-ocr
```

### Step 3: Deploy

**Option A: Full automated deployment**
```bash
bash deploy-to-gcp-dual.sh
```

**Option B: Prepare first, then deploy**
```bash
# Prepare build
bash prepare-gcp-deploy.sh

# Then deploy (skip prompt with AUTO_DEPLOY)
AUTO_DEPLOY=1 bash deploy-to-gcp-dual.sh
```

### Step 4: Verify Deployment

After deployment, you'll get URLs like:
- React: `https://storage.googleapis.com/gcp-count-la/index.html`
- Static: `https://storage.googleapis.com/gcp-count-la/v2/index.html`

Test with:
```bash
curl -I https://storage.googleapis.com/gcp-count-la/index.html
curl -I https://storage.googleapis.com/gcp-count-la/v2/index.html
```

---

## 🌐 DNS Configuration for gcp.count.la

After deployment, configure DNS in Cloudflare:

### Option 1: Direct CNAME (Simplest)

```
Type: CNAME
Name: gcp
Target: c.storage.googleapis.com
Proxy: DNS only (gray cloud) OR Proxied (orange cloud) - both work
TTL: Auto
```

### Option 2: Load Balancer with CDN (Recommended for Production)

1. **Create HTTPS Load Balancer**:
   - Go to: https://console.cloud.google.com/net-services/loadbalancing
   - Create new HTTP(S) Load Balancer

2. **Backend Configuration**:
   - Backend type: Cloud Storage bucket
   - Bucket: `gcp-count-la`
   - Enable Cloud CDN: Yes

3. **Frontend Configuration**:
   - Protocol: HTTPS
   - IP: Create new external IP address
   - Certificate: Create Google-managed certificate for `gcp.count.la`

4. **DNS Record in Cloudflare**:
   ```
   Type: A
   Name: gcp
   IPv4: [Load Balancer IP from step 3]
   Proxy: DNS only (gray cloud) OR Proxied (orange cloud)
   TTL: Auto
   ```

---

## 📋 Pre-Deployment Checklist

- [x] Project ID configured: `chk-poke-ocr`
- [x] Billing enabled (confirmed)
- [x] Build scripts updated
- [x] Footer links configured
- [ ] gcloud CLI authenticated
- [ ] APIs enabled
- [ ] Deployment executed
- [ ] DNS configured

---

## 🔍 Troubleshooting

### Issue: gcloud command not found
```bash
export PATH="$HOME/google-cloud-sdk/bin:$PATH"
# Or add to ~/.bashrc:
echo 'export PATH="$HOME/google-cloud-sdk/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Issue: Authentication required
```bash
gcloud auth login
gcloud config set project chk-poke-ocr
```

### Issue: Bucket already exists
The script will handle this automatically. If you need to recreate:
```bash
gsutil rm -r gs://gcp-count-la
gsutil mb -p chk-poke-ocr -c STANDARD -l us-central1 gs://gcp-count-la
```

### Issue: Permission denied
```bash
# Make bucket public
gsutil iam ch allUsers:objectViewer gs://gcp-count-la
```

---

## 📊 Expected URLs After Deployment

- **React Version**: `https://storage.googleapis.com/gcp-count-la/index.html`
- **Static Version**: `https://storage.googleapis.com/gcp-count-la/v2/index.html`

After DNS is configured:
- **React Version**: `https://gcp.count.la/`
- **Static Version**: `https://gcp.count.la/v2/`

---

## ✅ Success Criteria

Deployment is successful when:
- ✅ Bucket is publicly accessible
- ✅ React app loads at `/`
- ✅ Static site loads at `/v2/`
- ✅ Footer links work both ways
- ✅ Search functionality works on both versions
- ✅ No console errors

---

**Last Updated**: November 2, 2025
**Status**: Ready for deployment (pending authentication)
