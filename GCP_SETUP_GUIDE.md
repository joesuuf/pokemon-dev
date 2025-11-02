# Google Cloud Platform (GCP) Setup Guide

Complete guide to deploying Pokemon TCG Search on Google Cloud Platform and comparing with GitHub Pages.

---

## 📋 Prerequisites Checklist

Use the todo list to track your progress:

### ✅ Todo List Created
Run this to see your progress:
```bash
# The script will guide you through each step
bash deploy-to-gcp.sh
```

### Required Steps:
- [ ] Install Google Cloud SDK (gcloud CLI)
- [ ] Create/select GCP project
- [ ] Enable required APIs
- [ ] Set up billing
- [ ] Choose deployment method
- [ ] Deploy application
- [ ] Configure custom domain (optional)
- [ ] Set up SSL/TLS
- [ ] Enable monitoring
- [ ] Compare with GitHub Pages

---

## 🛠️ Step 1: Install Google Cloud SDK

### Linux/Mac:
```bash
# Download and install
curl https://sdk.cloud.google.com | bash

# Restart shell
exec -l $SHELL

# Initialize
gcloud init
```

### Windows:
Download from: https://cloud.google.com/sdk/docs/install

### Verify Installation:
```bash
gcloud --version
gcloud auth login
```

---

## 🚀 Step 2: Quick Start Deployment

### Run the Interactive Script:
```bash
bash deploy-to-gcp.sh
```

The script will guide you through:
1. **Authentication** - Login to GCP
2. **Project selection** - Choose or create project
3. **Frontend selection** - React or Static site
4. **Deployment method** - Storage, Cloud Run, or App Engine
5. **Deployment** - Automatic build and deploy
6. **Custom domain** - Optional setup
7. **Cost estimation** - Monthly cost breakdown

---

## 📊 Deployment Methods Comparison

### 1. Cloud Storage + Cloud CDN ⭐ RECOMMENDED

**Best for:** Static sites, maximum performance, lowest cost

**Pros:**
- ✅ Lowest cost (~$0.15-$1.00/month)
- ✅ Global CDN included
- ✅ 99.95% SLA
- ✅ Instant scaling
- ✅ Simple setup

**Cons:**
- ❌ Static files only
- ❌ No server-side rendering

**Perfect for:** Static site version (recommended)

---

### 2. Cloud Run

**Best for:** Containerized apps, serverless

**Pros:**
- ✅ Auto-scaling (0 to 1000+ instances)
- ✅ Pay only for requests
- ✅ Container support
- ✅ Easy updates

**Cons:**
- ❌ Higher cost (~$5-$20/month)
- ❌ Cold starts (minimal)

**Perfect for:** React version with backend needs

---

### 3. App Engine

**Best for:** Fully managed applications

**Pros:**
- ✅ Zero infrastructure management
- ✅ Auto-scaling
- ✅ Integrated services

**Cons:**
- ❌ Highest cost (~$10-$50/month)
- ❌ More complex

**Perfect for:** Production apps with traffic

---

## 💰 Cost Comparison

### GCP Cloud Storage (Recommended)
| Item | Monthly Cost |
|------|-------------|
| Storage (1GB) | $0.02 |
| Network (10GB) | $0.12 |
| Cloud CDN (optional) | $0.80 |
| **Total** | **$0.15 - $1.00** |

### Cloud Run
| Item | Monthly Cost |
|------|-------------|
| Requests (100K) | $0.10 |
| Memory | $0.08 |
| Network | $0.12 |
| **Total** | **$5 - $20** |

### App Engine
| Item | Monthly Cost |
|------|-------------|
| Instance hours | $36 |
| Network | $1.20 |
| **Total** | **$10 - $50** |

### GitHub Pages
| Item | Monthly Cost |
|------|-------------|
| Everything | **$0 (FREE)** |

---

## 🌍 GitHub Pages vs GCP Comparison

| Feature | GitHub Pages | GCP Cloud Storage | GCP Cloud Run |
|---------|-------------|-------------------|---------------|
| **Cost** | ✅ FREE | ~$0.15-$1/mo | ~$5-$20/mo |
| **Setup** | ✅ Very Easy | Medium | Medium |
| **Performance** | Good | ✅ Excellent (CDN) | Very Good |
| **Scalability** | ✅ Unlimited | ✅ Unlimited | ✅ Auto-scale |
| **Custom Domain** | ✅ Free SSL | ✅ Free SSL | ✅ Free SSL |
| **Monitoring** | Basic | ✅ Advanced | ✅ Advanced |
| **Build Time** | 1-2 min | Instant | 2-3 min |
| **Global CDN** | Yes (Fastly) | ✅ Yes (Google) | Optional |
| **Logs** | No | ✅ Yes | ✅ Yes |
| **Metrics** | No | ✅ Yes | ✅ Yes |

### When to Use GitHub Pages:
- ✅ Free tier needed
- ✅ Simple static site
- ✅ No advanced monitoring
- ✅ Open source project

### When to Use GCP:
- ✅ Advanced monitoring/logging needed
- ✅ Enterprise requirements
- ✅ Need guaranteed SLA
- ✅ Custom infrastructure control
- ✅ Integration with other GCP services

---

## 🔐 Environment Variables & API Keys

### Pokemon TCG API Key

You mentioned having a GitHub repo secret for the Pokemon API. Here's how to handle it in GCP:

### For Cloud Storage (Static Site):
API key is handled client-side in JavaScript:
```javascript
// static-site/scripts/api.js
const API_KEY = 'your-api-key-here'; // Or fetch from config
const API_URL = 'https://api.pokemontcg.io/v2/cards';
```

### For Cloud Run:
Use Secret Manager:
```bash
# Create secret
echo -n "your-api-key" | gcloud secrets create pokemon-api-key --data-file=-

# Grant access to Cloud Run
gcloud secrets add-iam-policy-binding pokemon-api-key \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Deploy with secret
gcloud run deploy SERVICE_NAME \
  --set-secrets="POKEMON_API_KEY=pokemon-api-key:latest"
```

### For App Engine:
Use environment variables in `app.yaml`:
```yaml
env_variables:
  POKEMON_API_KEY: "your-api-key-here"
```

**Note:** The Pokemon TCG API is currently free and doesn't require an API key for basic usage. The secret may be for future premium features.

---

## 🔧 Custom Domain Setup

### Option 1: Cloudflare DNS (Recommended)

#### For Cloud Storage + Load Balancer:
1. **Create Load Balancer in GCP:**
   - Go to: https://console.cloud.google.com/net-services/loadbalancing
   - Create HTTP(S) Load Balancer
   - Backend: Cloud Storage bucket
   - Frontend: Reserve static IP

2. **Get Load Balancer IP:**
   ```bash
   gcloud compute addresses list
   ```

3. **Add to Cloudflare:**
   ```
   Type: A
   Name: @ or subdomain
   IPv4: [Load Balancer IP]
   Proxy: Orange cloud (proxied) OR gray cloud (DNS only)
   ```

4. **Both work with Cloud Storage!** (Unlike GitHub Pages)

#### For Cloud Run:
1. **Map domain:**
   ```bash
   gcloud run domain-mappings create \
     --service=pokemon-tcg-search \
     --domain=yourdomain.com \
     --region=us-central1
   ```

2. **Get DNS records:**
   ```bash
   gcloud run domain-mappings describe \
     --domain=yourdomain.com \
     --region=us-central1
   ```

3. **Add to Cloudflare** as instructed

---

### Option 2: Cloud DNS

1. **Create Cloud DNS zone:**
   ```bash
   gcloud dns managed-zones create pokemon-tcg \
     --dns-name="yourdomain.com." \
     --description="Pokemon TCG Search"
   ```

2. **Add records:**
   ```bash
   gcloud dns record-sets transaction start --zone=pokemon-tcg
   gcloud dns record-sets transaction add [IP] \
     --name="yourdomain.com." \
     --ttl=300 \
     --type=A \
     --zone=pokemon-tcg
   gcloud dns record-sets transaction execute --zone=pokemon-tcg
   ```

3. **Update domain registrar** to use Cloud DNS nameservers

---

## 📈 Monitoring & Logging

### Enable Monitoring:
```bash
# Enable APIs
gcloud services enable monitoring.googleapis.com
gcloud services enable logging.googleapis.com
```

### Access Dashboards:
- **Monitoring:** https://console.cloud.google.com/monitoring
- **Logging:** https://console.cloud.google.com/logs
- **Metrics:** https://console.cloud.google.com/monitoring/metrics-explorer

### Key Metrics to Track:
- Request count
- Response time
- Error rate
- Traffic (bandwidth)
- Cost

### Set Up Alerts:
```bash
# Create alert policy
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High error rate" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=0.05
```

---

## 🧪 Testing Your Deployment

### 1. Load Testing

Use Apache Bench:
```bash
# Test GitHub Pages
ab -n 1000 -c 10 https://yourusername.github.io/pokemon-dev/

# Test GCP
ab -n 1000 -c 10 https://your-gcp-url/
```

### 2. Performance Testing

Use Lighthouse:
```bash
npm install -g lighthouse

# Test GitHub Pages
lighthouse https://yourusername.github.io/pokemon-dev/

# Test GCP
lighthouse https://your-gcp-url/
```

### 3. Global Performance

Test from multiple locations:
- https://tools.pingdom.com
- https://www.webpagetest.org
- https://gtmetrix.com

---

## 📊 Performance Comparison Template

| Metric | GitHub Pages | GCP Storage | GCP Run | Winner |
|--------|-------------|-------------|---------|--------|
| Load Time (US) | ? | ? | ? | ? |
| Load Time (EU) | ? | ? | ? | ? |
| Load Time (Asia) | ? | ? | ? | ? |
| TTFB | ? | ? | ? | ? |
| Lighthouse Score | ? | ? | ? | ? |
| Cost/month | $0 | ~$0.50 | ~$10 | ? |

Fill in after testing both platforms.

---

## 🔄 Update/Redeploy

### Cloud Storage:
```bash
# Update files
npm run build  # For React
gsutil -m rsync -r -d dist gs://BUCKET_NAME
```

### Cloud Run:
```bash
# Redeploy
gcloud run deploy SERVICE_NAME --source . --region=REGION
```

### App Engine:
```bash
# Deploy new version
gcloud app deploy
```

---

## 🗑️ Cleanup / Delete Resources

### Delete Cloud Storage:
```bash
gsutil rm -r gs://BUCKET_NAME
```

### Delete Cloud Run:
```bash
gcloud run services delete SERVICE_NAME --region=REGION
```

### Delete App Engine:
```bash
# Can't delete app, but can stop serving:
gcloud app versions delete VERSION
```

### Delete Project (everything):
```bash
gcloud projects delete PROJECT_ID
```

---

## 🐛 Troubleshooting

### Issue: "gcloud: command not found"
**Solution:** Install Google Cloud SDK (see Step 1)

### Issue: "Permission denied" or "403 Forbidden"
**Solution:**
```bash
gcloud auth login
gcloud config set project PROJECT_ID
```

### Issue: "Billing must be enabled"
**Solution:** Enable billing at:
https://console.cloud.google.com/billing

### Issue: API not enabled
**Solution:**
```bash
gcloud services enable SERVICE_NAME.googleapis.com
```

### Issue: Site not loading
**Solution:**
1. Check deployment status in console
2. Verify bucket/service is public
3. Check DNS propagation (dnschecker.org)
4. Review Cloud Logs

---

## 📚 Additional Resources

### Official Documentation:
- **Cloud Storage:** https://cloud.google.com/storage/docs
- **Cloud Run:** https://cloud.google.com/run/docs
- **App Engine:** https://cloud.google.com/appengine/docs
- **Cloud CDN:** https://cloud.google.com/cdn/docs

### Pricing Calculators:
- **GCP Calculator:** https://cloud.google.com/products/calculator
- **Free Tier:** https://cloud.google.com/free

### Support:
- **Stack Overflow:** https://stackoverflow.com/questions/tagged/google-cloud-platform
- **GCP Community:** https://www.googlecloudcommunity.com

---

## ✅ Quick Commands Reference

```bash
# Login
gcloud auth login

# Set project
gcloud config set project PROJECT_ID

# Deploy to Cloud Storage
gsutil -m rsync -r -d dist gs://BUCKET_NAME

# Deploy to Cloud Run
gcloud run deploy SERVICE_NAME --source . --region=REGION --allow-unauthenticated

# Deploy to App Engine
gcloud app deploy

# View logs
gcloud logging read --limit 50

# List all resources
gcloud compute instances list
gcloud storage buckets list
gcloud run services list

# Delete everything
gcloud projects delete PROJECT_ID
```

---

## 🎯 Recommended Deployment Path

### For Testing/Comparison:
1. **Start with Cloud Storage** (cheapest, fastest to set up)
2. Deploy static site version (best performance)
3. Enable Cloud CDN for global performance
4. Compare with GitHub Pages
5. Monitor costs for 1 month

### For Production:
- **Low traffic (<10K visits/month):** GitHub Pages (free)
- **Medium traffic + monitoring needed:** GCP Cloud Storage + CDN
- **High traffic or enterprise:** GCP Cloud Run or App Engine

---

## 🏁 Next Steps

1. ✅ Complete the todo list (track with the deployment script)
2. 🚀 Deploy to GCP using `deploy-to-gcp.sh`
3. 📊 Run performance tests (both platforms)
4. 💰 Monitor costs for 1 week
5. 📈 Compare metrics (speed, reliability, cost)
6. 🎯 Choose final deployment platform

---

**Last Updated:** November 2, 2025
**Script:** `deploy-to-gcp.sh`
**Todo List:** Tracked automatically during deployment
