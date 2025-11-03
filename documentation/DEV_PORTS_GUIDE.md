# Development Ports Guide

## Default Development Ports

### Primary Ports (Most Used)

#### Port 8888 - Main React Frontend ⭐ PRIMARY
**Command:** `npm run frontend:8888`
- **Frontend:** React 19.2.0 + TypeScript + Vite
- **Location:** `src/` directory
- **Index:** `index.html` (root)
- **URL:** http://localhost:8888
- **Features:**
  - Full React app with lazy loading
  - TypeScript strict mode
  - Tailwind CSS 4.1.16
  - Hot Module Replacement (HMR)
  - Service worker error handling

**Best for:** Main development work

---

#### Static Site (Port varies) ⭐ RECOMMENDED FOR PRODUCTION
**Command:**
```bash
cd static-site
python3 -m http.server 8000
```
Or:
```bash
npx http-server static-site -p 8000
```

- **Frontend:** Pure HTML/CSS/JavaScript (zero dependencies)
- **Location:** `static-site/` directory
- **Index:** `static-site/index.html`
- **URL:** http://localhost:8000 (or any port you choose)
- **Features:**
  - No build process
  - ~10KB total size
  - 30x faster than React version
  - Content Security Policy
  - Accessibility features

**Best for:** Production deployment, maximum performance

---

### Additional Development Ports

#### Port 6666 - Alternative React Dev
**Command:** `npm run dev:6666`
- Same as port 8888, just different port
- Configured for public access (0.0.0.0)

#### Port 9999 - React Variant
**Command:** `npm run frontend:9999`
- Alternative React frontend
- Uses `vite.config.9999.ts`

#### Port 7777 - Carousel Demo
**Command:** `npm run frontend:7777`
- Carousel frontend variant
- Vite configuration

#### Port 5555 - Frontend Variant
**Command:** `npm run frontend:5555`
- Another React variant
- Uses `vite.config.5555.ts`

---

## GitHub Pages Deployment

### Which Frontend to Deploy?

Based on the comprehensive audit results:

#### 🏆 Recommended: Static Site
**Why?**
- **Performance:** 15x smaller, 30x faster
- **Score:** 8.8/10 (vs React 8.2/10)
- **Maintenance:** Zero dependencies, no updates needed
- **SEO:** Better search engine optimization
- **Cost:** Works on cheapest hosting

**Deploy command:**
```bash
bash deploy-to-github-pages.sh
# Choose option 2 (Static Site)
```

#### Alternative: React Frontend
**When to use:**
- Need complex state management
- Planning to add advanced features
- Team prefers React ecosystem

**Deploy command:**
```bash
bash deploy-to-github-pages.sh
# Choose option 1 (React)
```

---

## Port Mapping Summary

| Port | Frontend | Command | Index File |
|------|----------|---------|------------|
| **8888** | **React Main** | `npm run dev` | `index.html` (root) |
| 6666 | React Alt | `npm run dev:6666` | `index.html` (root) |
| **8000** | **Static Site** | `python3 -m http.server` | `static-site/index.html` |
| 9999 | React Variant | `npm run frontend:9999` | `frontends/port-9999/index.html` |
| 7777 | Carousel | `npm run frontend:7777` | `frontends/port-7777/index.html` |
| 5555 | React Variant | `npm run frontend:5555` | `frontends/port-5555/index.html` |

---

## Cloudflare DNS Configuration (Non-Proxy)

### For Custom Domain

1. **Cloudflare Dashboard** → Your Domain → DNS

2. **Add DNS Record:**

   For subdomain (e.g., pokemon.yourdomain.com):
   ```
   Type: CNAME
   Name: pokemon
   Target: joesuuf.github.io
   Proxy: DNS only (gray cloud) ← IMPORTANT
   ```

   For apex domain (e.g., yourdomain.com):
   ```
   Type: A
   Name: @
   Content: 185.199.108.153
   Proxy: DNS only (gray cloud) ← IMPORTANT
   ```
   Repeat for: 185.199.109.153, 185.199.110.153, 185.199.111.153

3. **GitHub Pages Settings:**
   - Go to: https://github.com/joesuuf/pokemon-dev/settings/pages
   - Custom domain: your-domain.com
   - Save
   - Enable "Enforce HTTPS" (after DNS propagates)

4. **Wait for DNS propagation** (15-30 minutes)

---

## Quick Start Commands

### Local Development

```bash
# Start main React dev server (port 8888)
npm run dev

# Start static site (port 8000)
cd static-site && python3 -m http.server 8000

# Start all frontends at once
npm run frontends:all
```

### Production Deployment

```bash
# Deploy to GitHub Pages (interactive)
bash deploy-to-github-pages.sh

# Extract standalone React app
bash extract-react-app.sh

# Extract standalone static site
bash extract-static-site.sh
```

### Testing

```bash
# Run tests
npm test

# Run tests with UI
npm run test:ui

# Lint code
npm run lint
```

---

## Environment Summary

### Current Versions (Verified Nov 2, 2025)
- ✅ React: 19.2.0 (Latest Stable)
- ✅ Tailwind CSS: 4.1.16 (Latest Stable)
- ✅ TypeScript: 5.2.2
- ✅ Vite: 7.1.12
- ✅ Node.js: v22.21.0
- ✅ Python: 3.11.14

---

## Recommended Workflow

### For Development:
1. Use **port 8888** (React main) for feature development
2. Test on **static site** (port 8000) for production preview

### For Production:
1. **Deploy static site** to GitHub Pages (better performance)
2. Configure Cloudflare DNS (gray cloud - DNS only)
3. Enable HTTPS in GitHub Pages settings

---

## Troubleshooting

### Port already in use?
```bash
# Kill process on port 8888
npx kill-port 8888

# Or use different port
npm run dev:6666
```

### Site not loading on GitHub Pages?
1. Check deployment: https://github.com/joesuuf/pokemon-dev/deployments
2. Verify DNS: https://dnschecker.org
3. Check GitHub Pages settings: Settings → Pages
4. Ensure Cloudflare is in DNS only mode (gray cloud)

### Build fails?
```bash
# Clear and reinstall
rm -rf node_modules
npm install

# Clear Vite cache
rm -rf .vite

# Try build again
npm run build
```

---

## Performance Comparison

| Metric | React (8888) | Static Site | Winner |
|--------|-------------|-------------|--------|
| Bundle Size | 150KB | 10KB | 🏆 Static (15x smaller) |
| Load Time | 1.5s | 0.05s | 🏆 Static (30x faster) |
| TTI | 2s | 0.2s | 🏆 Static (10x faster) |
| Dependencies | 28 | 0 | 🏆 Static (zero) |

**Recommendation: Deploy static site for production**

---

## Quick Links

- **Audit Reports:**
  - AUDIT_SUMMARY.md
  - AUDIT_REPORT_REACT.md
  - AUDIT_REPORT_STATIC_SITE.md

- **Deployment:**
  - deploy-to-github-pages.sh

- **Extraction:**
  - extract-react-app.sh
  - extract-static-site.sh

---

**Last Updated:** November 2, 2025
