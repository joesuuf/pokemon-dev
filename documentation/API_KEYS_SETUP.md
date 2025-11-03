# API Keys & Secrets Management Guide

Complete guide for managing the Pokemon TCG API key across GitHub Pages and GCP deployments.

---

## 🔐 Current Setup: GitHub Repo Secret

You mentioned having a GitHub repository secret for the Pokemon API. Here's how to use it and migrate to GCP.

---

## 📋 Pokemon TCG API Information

### Current API Status:
- **Base URL:** https://api.pokemontcg.io/v2
- **Authentication:** Optional (API key not required for basic usage)
- **Rate Limits:** ~1000 requests/hour without key, ~unlimited with key
- **Free Tier:** Available

### When API Key is Needed:
- ✅ Higher rate limits
- ✅ Premium features
- ✅ Commercial usage
- ✅ Guaranteed SLA

---

## 🔧 GitHub Pages Setup (Current)

### Option 1: Using GitHub Secrets with Actions

If you're using GitHub Actions to build and deploy:

#### 1. Add Secret to Repository:
Already done! (You mentioned you have this)
- Go to: Settings → Secrets and variables → Actions
- Secret name: `POKEMON_API_KEY`
- Value: Your API key

#### 2. Use in Build Process:

**For React (Vite):**

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '22'

      - name: Install dependencies
        run: npm ci

      - name: Build
        env:
          VITE_POKEMON_API_KEY: ${{ secrets.POKEMON_API_KEY }}
        run: npm run build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

#### 3. Access in React Code:

**`src/services/pokemonTcgApi.ts`:**
```typescript
const API_KEY = import.meta.env.VITE_POKEMON_API_KEY || '';
const API_BASE_URL = 'https://api.pokemontcg.io/v2';

export async function searchCards(params: SearchParams) {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };

  // Add API key if available
  if (API_KEY) {
    headers['X-Api-Key'] = API_KEY;
  }

  const response = await fetch(`${API_BASE_URL}/cards`, {
    headers,
    // ... other options
  });

  return response.json();
}
```

#### 4. Local Development:

Create `.env.local` (NOT committed to git):
```bash
VITE_POKEMON_API_KEY=your-api-key-here
```

Add to `.gitignore` (if not already there):
```
.env.local
.env*.local
```

---

### Option 2: Client-Side Only (Static Site)

**For static site (no build process):**

#### 1. Configuration File Approach:

**`static-site/config.js`** (NOT committed):
```javascript
// config.js (add to .gitignore)
window.POKEMON_CONFIG = {
  apiKey: 'your-api-key-here',
  apiUrl: 'https://api.pokemontcg.io/v2'
};
```

**`static-site/index.html`:**
```html
<script src="config.js"></script>
<script src="scripts/api.js"></script>
```

**`static-site/scripts/api.js`:**
```javascript
const API_KEY = window.POKEMON_CONFIG?.apiKey || '';
const API_URL = window.POKEMON_CONFIG?.apiUrl || 'https://api.pokemontcg.io/v2';

function getHeaders() {
  const headers = {
    'Content-Type': 'application/json'
  };

  if (API_KEY) {
    headers['X-Api-Key'] = API_KEY;
  }

  return headers;
}

async function searchCards(query) {
  const response = await fetch(`${API_URL}/cards?q=name:${query}`, {
    headers: getHeaders()
  });
  return response.json();
}
```

#### 2. For GitHub Pages Deployment:

Create a GitHub Action that injects the key during build:

**`.github/workflows/deploy-static.yml`:**
```yaml
name: Deploy Static Site

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Create config file
        run: |
          cat > static-site/config.js << EOF
          window.POKEMON_CONFIG = {
            apiKey: '${{ secrets.POKEMON_API_KEY }}',
            apiUrl: 'https://api.pokemontcg.io/v2'
          };
          EOF

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./static-site
```

**⚠️ Security Note:** Client-side API keys are visible to users. Use backend proxy for sensitive operations.

---

## ☁️ GCP Setup

### Method 1: Cloud Storage (Static Site)

**Same as GitHub Pages** - API key is client-side.

#### Deployment with Key:

**Update `deploy-to-gcp.sh`** to inject config:
```bash
# Add before uploading to bucket:
cat > "$DEPLOY_DIR/config.js" << EOF
window.POKEMON_CONFIG = {
  apiKey: '$POKEMON_API_KEY',
  apiUrl: 'https://api.pokemontcg.io/v2'
};
EOF
```

#### Set environment variable locally:
```bash
export POKEMON_API_KEY="your-api-key"
bash deploy-to-gcp.sh
```

---

### Method 2: Cloud Run (Best for API Keys)

Cloud Run supports **Secret Manager** for secure key storage.

#### 1. Store API Key in Secret Manager:

```bash
# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com

# Create secret
echo -n "your-api-key" | gcloud secrets create pokemon-api-key \
  --data-file=- \
  --replication-policy="automatic"

# Verify
gcloud secrets versions access latest --secret="pokemon-api-key"
```

#### 2. Create Backend Proxy (Recommended):

**`proxy-server/server.js`:**
```javascript
const express = require('express');
const axios = require('axios');
const app = express();

const API_KEY = process.env.POKEMON_API_KEY;
const API_URL = 'https://api.pokemontcg.io/v2';

app.use(express.json());
app.use(express.static('public'));

// Proxy endpoint
app.get('/api/cards', async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/cards`, {
      headers: {
        'X-Api-Key': API_KEY
      },
      params: req.query
    });
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch cards' });
  }
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

**`Dockerfile`:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 8080

CMD ["node", "server.js"]
```

#### 3. Deploy with Secret:

```bash
# Grant Cloud Run access to secret
PROJECT_NUMBER=$(gcloud projects describe PROJECT_ID --format="value(projectNumber)")

gcloud secrets add-iam-policy-binding pokemon-api-key \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Deploy with secret
gcloud run deploy pokemon-tcg-search \
  --source . \
  --region us-central1 \
  --set-secrets="POKEMON_API_KEY=pokemon-api-key:latest" \
  --allow-unauthenticated
```

#### 4. Update Frontend to Use Proxy:

**`src/services/pokemonTcgApi.ts`:**
```typescript
// Use your Cloud Run URL instead of direct API
const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://your-cloud-run-url/api'  // Your proxy
  : 'https://api.pokemontcg.io/v2';    // Direct for dev

// No API key needed - handled by backend
export async function searchCards(params: SearchParams) {
  const response = await fetch(`${API_BASE_URL}/cards`, {
    headers: {
      'Content-Type': 'application/json',
    },
    // API key is handled by backend proxy
  });

  return response.json();
}
```

**✅ Benefits:**
- API key never exposed to client
- Better security
- Can add rate limiting, caching, logging
- Can transform/filter responses

---

### Method 3: App Engine

Similar to Cloud Run, use environment variables:

**`app.yaml`:**
```yaml
runtime: nodejs18

env_variables:
  POKEMON_API_KEY: "your-api-key"  # Not recommended - use Secret Manager

# Better: Use Secret Manager
includes:
  - secrets.yaml
```

**`secrets.yaml`:**
```yaml
secrets:
  POKEMON_API_KEY:
    secretName: pokemon-api-key
    version: latest
```

---

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Use Secret Manager for production
- ✅ Use backend proxy for API calls
- ✅ Add API key to `.gitignore`
- ✅ Rotate keys regularly
- ✅ Use environment variables
- ✅ Implement rate limiting
- ✅ Monitor API usage

### ❌ DON'T:
- ❌ Commit API keys to git
- ❌ Hardcode keys in source code
- ❌ Expose keys in client-side JavaScript (if sensitive)
- ❌ Share keys in public channels
- ❌ Use production keys in development

---

## 🔄 Migration Path: GitHub Pages → GCP

### Current: GitHub Pages with Secret
```
GitHub Repo Secret → GitHub Actions → Build → Deploy
```

### Option A: GCP Cloud Storage (No Backend)
```
Manual config → Build locally → Upload to GCS
```

### Option B: GCP Cloud Run (With Backend Proxy) ⭐ RECOMMENDED
```
Secret Manager → Cloud Run → Backend Proxy → Frontend
```

---

## 📝 Setup Scripts

### For GitHub Actions:

**`.github/workflows/deploy-react.yml`:**
```yaml
name: Deploy React to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: '22'

      - name: Install dependencies
        run: npm ci

      - name: Build with API key
        env:
          VITE_POKEMON_API_KEY: ${{ secrets.POKEMON_API_KEY }}
        run: npm run build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
          cname: your-domain.com  # Optional
```

### For GCP Cloud Run:

**Create `deploy-with-secrets.sh`:**
```bash
#!/bin/bash

# Check for API key in environment
if [ -z "$POKEMON_API_KEY" ]; then
    echo "Error: POKEMON_API_KEY not set"
    echo "Export it first: export POKEMON_API_KEY='your-key'"
    exit 1
fi

# Store in Secret Manager (one-time)
echo -n "$POKEMON_API_KEY" | gcloud secrets create pokemon-api-key \
  --data-file=- \
  --replication-policy="automatic" \
  2>/dev/null || echo "Secret already exists"

# Deploy to Cloud Run with secret
gcloud run deploy pokemon-tcg-search \
  --source . \
  --region us-central1 \
  --set-secrets="POKEMON_API_KEY=pokemon-api-key:latest" \
  --allow-unauthenticated

echo "Deployed with API key from Secret Manager"
```

---

## 🧪 Testing API Key Setup

### Test without API key:
```bash
curl https://api.pokemontcg.io/v2/cards?q=name:charizard
```

### Test with API key:
```bash
curl -H "X-Api-Key: your-api-key" \
  https://api.pokemontcg.io/v2/cards?q=name:charizard
```

### Test your deployed site:
```javascript
// In browser console
fetch('/api/cards?q=name:charizard')
  .then(r => r.json())
  .then(console.log)
```

---

## 📊 API Usage Monitoring

### GitHub Pages:
- No built-in monitoring
- Use Pokemon API dashboard: https://dev.pokemontcg.io

### GCP Cloud Run:
```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50

# View metrics
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/request_count"'
```

### Set Up Alerts:
```bash
# Alert on high API usage
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High API usage" \
  --condition-threshold-value=1000 \
  --condition-threshold-duration=3600s
```

---

## 🎯 Recommended Setup

### For Development:
```bash
# .env.local (not committed)
VITE_POKEMON_API_KEY=your-dev-api-key
```

### For GitHub Pages:
- Use GitHub Secrets
- Build with GitHub Actions
- API key injected during build
- **Client-side exposure** (acceptable for public API)

### For GCP Production:
- Use Secret Manager
- Deploy backend proxy on Cloud Run
- API key never exposed to client
- **Server-side only** (most secure)

---

## 🔑 Quick Commands

```bash
# Create secret in GCP
echo -n "your-key" | gcloud secrets create pokemon-api-key --data-file=-

# Update secret
echo -n "new-key" | gcloud secrets versions add pokemon-api-key --data-file=-

# View secret
gcloud secrets versions access latest --secret="pokemon-api-key"

# Delete secret
gcloud secrets delete pokemon-api-key

# Deploy Cloud Run with secret
gcloud run deploy SERVICE_NAME \
  --set-secrets="POKEMON_API_KEY=pokemon-api-key:latest"

# Test API with key
curl -H "X-Api-Key: KEY" https://api.pokemontcg.io/v2/cards
```

---

## ✅ Checklist

- [ ] API key stored in GitHub Secrets (already done)
- [ ] `.env.local` created for local development
- [ ] `.env.local` added to `.gitignore`
- [ ] GitHub Actions workflow configured (if using)
- [ ] GCP Secret Manager set up (if using GCP)
- [ ] Backend proxy created (if using GCP + sensitive data)
- [ ] API usage monitoring configured
- [ ] Test deployment with and without key

---

**Last Updated:** November 2, 2025
**Related Files:** `deploy-to-gcp.sh`, `deploy-to-github-pages.sh`
