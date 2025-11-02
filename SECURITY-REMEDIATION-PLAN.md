# Security Remediation Plan & Action Items

**Related:** SECURITY-AUDIT-COMPREHENSIVE.md
**Status:** 🔴 URGENT - Immediate action required
**Last Updated:** November 2, 2025

---

## 🚨 CRITICAL PRIORITY (Fix Immediately)

### TODO-1: Rotate Exposed API Key
**Severity:** CRITICAL
**Estimated Time:** 15 minutes
**Dependencies:** None

**Steps:**
1. [ ] Go to https://pokemontcg.io/ and log in
2. [ ] Navigate to API key management
3. [ ] Revoke the current API key: `f43ae006-2449-4771-8442-a17179cacbdf`
4. [ ] Generate a new API key
5. [ ] Update the new key in Vercel environment variables only (NOT in .env)
6. [ ] Test the application with new key
7. [ ] Document the rotation in your security log

**Why Critical:**
The current API key is publicly visible in git history and can be abused by anyone.

**Testing:**
```bash
# Verify new key works
curl -H "X-Api-Key: NEW_KEY_HERE" https://api.pokemontcg.io/v2/cards?page=1&pageSize=1
```

---

### TODO-2: Remove .env from Git Tracking
**Severity:** CRITICAL
**Estimated Time:** 30 minutes
**Dependencies:** TODO-1 (rotate key first)

**Steps:**
1. [ ] Ensure API key has been rotated (TODO-1)
2. [ ] Remove .env from git tracking:
   ```bash
   git rm --cached .env
   git commit -m "Remove .env from version control (security fix)"
   ```
3. [ ] Verify .env is in .gitignore (already done, but confirm):
   ```bash
   grep "^\.env$" .gitignore
   ```
4. [ ] Add to commit and push:
   ```bash
   git push origin claude/security-audit-comprehensive-011CUibJfXYSPg9bXbykV7SB
   ```

**Warning:**
This only prevents future tracking. The file still exists in git history!

---

### TODO-3: Remove API Key from Git History
**Severity:** CRITICAL
**Estimated Time:** 45-60 minutes
**Dependencies:** TODO-1, TODO-2
**Requires:** Team coordination (forces push)

**Option A: Using BFG Repo-Cleaner (Recommended)**
```bash
# Install BFG
# macOS: brew install bfg
# Linux: download from https://rtyley.github.io/bfg-repo-cleaner/

# Clone a fresh copy
git clone --mirror https://github.com/joesuuf/pokemon-dev.git

# Remove .env from history
bfg --delete-files .env pokemon-dev.git

# Clean up
cd pokemon-dev.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (COORDINATE WITH TEAM!)
git push --force
```

**Option B: Using git filter-repo (Alternative)**
```bash
# Install git-filter-repo
pip install git-filter-repo

# Clone fresh copy
git clone https://github.com/joesuuf/pokemon-dev.git
cd pokemon-dev

# Remove .env from all history
git filter-repo --path .env --invert-paths

# Force push (COORDINATE WITH TEAM!)
git push --force --all
git push --force --tags
```

**Steps:**
1. [ ] Coordinate with team about force push
2. [ ] Ensure all team members have pushed their work
3. [ ] Follow Option A or B above
4. [ ] Force push changes
5. [ ] Notify team to re-clone repository
6. [ ] Verify .env is gone from history:
   ```bash
   git log --all --full-history -- .env
   # Should return no results
   ```

**Warning:**
This requires a force push and will rewrite git history. All team members must re-clone!

---

### TODO-4: Migrate Frontend to Use Backend Proxy
**Severity:** CRITICAL
**Estimated Time:** 2-3 hours
**Dependencies:** None (can be done in parallel)

**Current (Insecure):**
```typescript
// src/lib/api.ts - CURRENT
const API_KEY = import.meta.env.VITE_POKEMON_TCG_API_KEY;
const response = await fetch(`${API_BASE_URL}/cards?${params}`, { headers });
```

**Target (Secure):**
```typescript
// src/lib/api.ts - SECURE
// No API key needed on frontend!
const response = await fetch(`/api/cards?${params}`);
```

**Files to Modify:**

1. [ ] **src/lib/api.ts**
   ```typescript
   // OLD (remove these lines):
   const API_KEY = import.meta.env.VITE_POKEMON_TCG_API_KEY;
   const headers: HeadersInit = {
     'X-Api-Key': API_KEY || '',
   };

   // NEW (replace with):
   const API_BASE_URL = '/api'; // Use our backend proxy
   // Remove headers completely - backend handles auth

   export async function searchPokemon(
     query: string,
     page: number = 1,
     pageSize: number = 20
   ): Promise<PokemonListResponse> {
     const searchQuery = query.trim()
       ? `name:"${query}*" OR name:"*${query}*"`
       : '';

     const params = new URLSearchParams({
       q: searchQuery,
       pageSize: pageSize.toString(),
     });

     const response = await fetch(`${API_BASE_URL}/cards?${params}`);

     if (!response.ok) {
       throw new Error('Failed to fetch Pokemon cards');
     }

     return response.json();
   }
   ```

2. [ ] **src/services/pokemonTcgApi.ts**
   ```typescript
   // OLD (remove these lines):
   const API_KEY = import.meta.env.VITE_POKEMON_TCG_API_KEY;
   const BASE_URL = 'https://api.pokemontcg.io/v2';

   const axiosInstance = axios.create({
     baseURL: BASE_URL,
     headers: {
       'Content-Type': 'application/json',
       ...(API_KEY && { 'X-Api-Key': API_KEY })
     },
     timeout: 60000
   });

   // NEW (replace with):
   const BASE_URL = '/api'; // Use our backend proxy

   const axiosInstance = axios.create({
     baseURL: BASE_URL,
     headers: {
       'Content-Type': 'application/json',
     },
     timeout: 60000
   });
   ```

3. [ ] **Remove from .env**
   ```bash
   # Delete this line from .env:
   VITE_POKEMON_TCG_API_KEY=f43ae006-2449-4771-8442-a17179cacbdf
   ```

4. [ ] **Update env.example**
   ```bash
   # Remove from env.example:
   # VITE_POKEMON_TCG_API_KEY=INSERT_KEY_HERE

   # Add comment:
   # API key is stored server-side in Vercel environment variables
   # No frontend environment variables needed
   ```

5. [ ] **Update Vercel Environment Variables**
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Ensure `POKEMON_TCG_API_KEY` is set (not `VITE_POKEMON_TCG_API_KEY`)
   - Value: [your new rotated API key from TODO-1]

6. [ ] **Test the changes**
   ```bash
   npm run build
   npm run preview
   # Test search functionality
   # Verify API calls go to /api/cards endpoint
   ```

---

## 🔴 HIGH PRIORITY (Fix within 24-48 hours)

### TODO-5: Add Security Headers
**Severity:** HIGH
**Estimated Time:** 1 hour
**Dependencies:** None

**Steps:**

1. [ ] **Update vercel.json** with security headers:
   ```json
   {
     "$schema": "https://openapi.vercel.sh/vercel.json",
     "buildCommand": "npm run build",
     "devCommand": "npm run dev",
     "installCommand": "npm ci",
     "framework": "vite",
     "functions": {
       "api/**/*.ts": {
         "runtime": "nodejs20.x",
         "maxDuration": 30
       }
     },
     "env": {
       "POKEMON_TCG_API_KEY": {
         "description": "API key for Pokemon TCG API from pokemontcg.io"
       },
       "NODE_ENV": {
         "description": "Node environment",
         "default": "production"
       }
     },
     "redirects": [],
     "rewrites": [
       {
         "source": "/api/(.*)",
         "destination": "/api/cards"
       }
     ],
     "headers": [
       {
         "source": "/(.*)",
         "headers": [
           {
             "key": "X-Frame-Options",
             "value": "DENY"
           },
           {
             "key": "X-Content-Type-Options",
             "value": "nosniff"
           },
           {
             "key": "Referrer-Policy",
             "value": "strict-origin-when-cross-origin"
           },
           {
             "key": "Permissions-Policy",
             "value": "camera=(), microphone=(), geolocation=()"
           },
           {
             "key": "X-XSS-Protection",
             "value": "1; mode=block"
           },
           {
             "key": "Strict-Transport-Security",
             "value": "max-age=31536000; includeSubDomains"
           },
           {
             "key": "Content-Security-Policy",
             "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' https://images.pokemontcg.io data:; connect-src 'self' https://api.pokemontcg.io; font-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none';"
           }
         ]
       },
       {
         "source": "/api/(.*)",
         "headers": [
           {
             "key": "Cache-Control",
             "value": "public, max-age=300, s-maxage=300"
           }
         ]
       }
     ]
   }
   ```

2. [ ] Test headers in deployment:
   ```bash
   curl -I https://your-app.vercel.app
   # Verify all security headers are present
   ```

3. [ ] Test CSP doesn't break functionality
4. [ ] Adjust CSP if needed for your specific use case

---

### TODO-6: Fix CORS Wildcard
**Severity:** HIGH
**Estimated Time:** 30 minutes
**Dependencies:** None

**Steps:**

1. [ ] **Update api/cards.ts** (lines 82-90):
   ```typescript
   // OLD (INSECURE):
   response.setHeader('Access-Control-Allow-Origin', '*')
   response.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS, HEAD')
   response.setHeader('Access-Control-Allow-Headers', 'Content-Type')

   // NEW (SECURE):
   const allowedOrigins = [
     'https://your-production-domain.com',
     'https://www.your-production-domain.com',
     'https://your-app.vercel.app',
     ...(process.env.NODE_ENV === 'development'
       ? ['http://localhost:8888', 'http://localhost:5173']
       : [])
   ];

   const origin = request.headers.origin;
   if (origin && allowedOrigins.includes(origin)) {
     response.setHeader('Access-Control-Allow-Origin', origin);
     response.setHeader('Access-Control-Allow-Credentials', 'true');
   }

   response.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS, HEAD')
   response.setHeader('Access-Control-Allow-Headers', 'Content-Type')
   ```

2. [ ] Update `allowedOrigins` array with your actual domains
3. [ ] Test CORS from allowed origins
4. [ ] Verify CORS blocks unauthorized origins

---

### TODO-7: Secure Logger Implementation
**Severity:** HIGH
**Estimated Time:** 1 hour
**Dependencies:** None

**Steps:**

1. [ ] **Update src/utils/logger.ts** to remove localStorage logging:
   ```typescript
   // REMOVE this method completely:
   private writeToFile(content: string) {
     const key = `pokemon-tcg-logs-${this.logFileName}`
     const existing = localStorage.getItem(key) || ''
     localStorage.setItem(key, existing + content)
   }

   // UPDATE log method to NOT store URLs:
   log(level: LogEntry['level'], message: string, options?: {
     duration?: number;
     size?: number;
     // REMOVE url parameter
     statusCode?: number
   }) {
     const now = new Date()
     const timestamp = now.toISOString()
     const elapsed = this.getElapsedTime()

     const entry: LogEntry = {
       timestamp,
       level,
       message,
       duration: options?.duration,
       size: options?.size,
       // REMOVE url from entry
       statusCode: options?.statusCode,
     }

     this.logs.push(entry)

     // Only log to console in development mode
     if (import.meta.env.DEV) {
       let logLine = `[${timestamp}] [${level.toUpperCase()}] ${message}`
       console.log(logLine)
     }

     // REMOVE writeToFile call
   }
   ```

2. [ ] Remove URL logging from all logger calls
3. [ ] Add rate limiting to prevent log flooding
4. [ ] Consider sending logs to secure backend service instead

---

## 🟡 MEDIUM PRIORITY (Fix within 1 week)

### TODO-8: Remove Excessive Console Logging
**Severity:** MEDIUM
**Estimated Time:** 1-2 hours

**Steps:**

1. [ ] **src/services/pokemonTcgApi.ts** - Remove or wrap debug logs:
   ```typescript
   // Wrap all console.log in development check:
   if (import.meta.env.DEV) {
     console.log('[INFO] Starting search for:', JSON.stringify(params));
   }

   // OR better, remove completely and use proper logger:
   import { logger } from '../utils/logger';
   logger.debug('Starting search for:', { params });
   ```

2. [ ] **api/cards.ts** - Keep error logs, remove debug logs:
   ```typescript
   // KEEP error logs (they go to Vercel logs, not browser):
   console.error(`[Pokemon TCG Proxy] API error: ${apiResponse.status}`)

   // REMOVE or wrap debug logs:
   // console.log(`[Pokemon TCG Proxy] Fetching: ${apiUrl.toString()}`)
   ```

3. [ ] Create a production-ready logging strategy:
   - Development: Full logging
   - Production: Errors only
   - Consider using a proper logging service (Sentry, LogRocket, etc.)

4. [ ] Run audit to verify:
   ```bash
   # Find remaining console statements:
   grep -r "console\." src/ --include="*.ts" --include="*.tsx"
   ```

---

### TODO-9: Add API Rate Limiting
**Severity:** MEDIUM
**Estimated Time:** 2 hours

**Steps:**

1. [ ] Install rate limiting package:
   ```bash
   npm install --save @vercel/edge
   ```

2. [ ] **Update api/cards.ts** with rate limiting:
   ```typescript
   import { ratelimit } from '@vercel/edge';

   // At the top of the file
   const limiter = ratelimit({
     interval: '60s',
     limit: 100, // 100 requests per 60 seconds
     tokens: 1
   });

   export default async function handler(
     request: VercelRequest,
     response: VercelResponse
   ): Promise<void> {
     // Check rate limit
     const identifier = request.headers['x-forwarded-for'] || 'anonymous';
     const { success, remaining } = await limiter.check(identifier);

     if (!success) {
       return response.status(429).json({
         error: 'Too many requests',
         message: 'Please wait before making another request'
       });
     }

     // Add rate limit headers
     response.setHeader('X-RateLimit-Remaining', remaining.toString());

     // ... rest of handler
   }
   ```

3. [ ] Test rate limiting:
   ```bash
   # Make rapid requests to test
   for i in {1..110}; do
     curl http://localhost:8888/api/cards?q=pikachu
   done
   # Should get 429 after 100 requests
   ```

4. [ ] Document rate limits in API documentation

---

### TODO-10: Restrict Development Server Access
**Severity:** MEDIUM
**Estimated Time:** 15 minutes

**Steps:**

1. [ ] **Update vite.config.ts**:
   ```typescript
   import { defineConfig } from 'vite'
   import react from '@vitejs/plugin-react'

   export default defineConfig(({ mode }) => ({
     plugins: [react()],
     server: {
       port: 8888,
       strictPort: false,
       // Only allow 0.0.0.0 in development for Codespaces/WSL
       // In production, this doesn't matter (Vite is only for dev)
       host: mode === 'development' ? '0.0.0.0' : 'localhost',
     }
   }))
   ```

2. [ ] Add environment-specific configuration
3. [ ] Document the security consideration

---

## 🟢 LOW PRIORITY (Fix when convenient)

### TODO-11: Clean Up Documentation
**Severity:** LOW
**Estimated Time:** 30 minutes

**Steps:**

1. [ ] Review all `.md` files for example API keys
2. [ ] Replace any real-looking keys with `INSERT_KEY_HERE` or `xxx-xxx-xxx`
3. [ ] Add security warnings to documentation:
   ```markdown
   ⚠️ **Security Note:** Never commit real API keys to git.
   Always use environment variables and keep .env files out of version control.
   ```

4. [ ] Update README.md with security best practices

---

### TODO-12: Set Up Automated Security Scanning
**Severity:** LOW
**Estimated Time:** 2-3 hours

**Steps:**

1. [ ] Add GitHub Actions workflow for security:
   ```yaml
   # .github/workflows/security.yml
   name: Security Scan

   on:
     push:
       branches: [ main, develop ]
     pull_request:
       branches: [ main, develop ]

   jobs:
     security:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3

         - name: Run npm audit
           run: npm audit --audit-level=moderate

         - name: Run Snyk security scan
           uses: snyk/actions/node@master
           env:
             SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

         - name: Check for secrets
           uses: trufflesecurity/trufflehog@main
           with:
             path: ./
             base: ${{ github.event.repository.default_branch }}
             head: HEAD
   ```

2. [ ] Sign up for Snyk (free tier available)
3. [ ] Add Snyk token to GitHub secrets
4. [ ] Enable Dependabot alerts in GitHub settings
5. [ ] Configure automated security updates

---

## 📊 Progress Tracking

**Total Tasks:** 12
**Critical:** 4
**High:** 3
**Medium:** 3
**Low:** 2

### Completion Checklist

- [ ] TODO-1: Rotate Exposed API Key (CRITICAL)
- [ ] TODO-2: Remove .env from Git Tracking (CRITICAL)
- [ ] TODO-3: Remove API Key from Git History (CRITICAL)
- [ ] TODO-4: Migrate Frontend to Use Backend Proxy (CRITICAL)
- [ ] TODO-5: Add Security Headers (HIGH)
- [ ] TODO-6: Fix CORS Wildcard (HIGH)
- [ ] TODO-7: Secure Logger Implementation (HIGH)
- [ ] TODO-8: Remove Excessive Console Logging (MEDIUM)
- [ ] TODO-9: Add API Rate Limiting (MEDIUM)
- [ ] TODO-10: Restrict Development Server Access (MEDIUM)
- [ ] TODO-11: Clean Up Documentation (LOW)
- [ ] TODO-12: Set Up Automated Security Scanning (LOW)

---

## 🔄 Verification Steps (After All Fixes)

Once all critical and high priority tasks are complete:

1. [ ] **Verify API key is not in git:**
   ```bash
   git log --all --full-history --source --all -- .env
   git grep -i "f43ae006-2449-4771-8442-a17179cacbdf"
   # Both should return no results
   ```

2. [ ] **Verify frontend doesn't expose secrets:**
   ```bash
   npm run build
   grep -r "VITE_POKEMON" dist/
   # Should return no results
   ```

3. [ ] **Verify backend proxy works:**
   ```bash
   curl http://localhost:8888/api/cards?q=pikachu | jq
   # Should return Pokemon data
   ```

4. [ ] **Verify security headers:**
   ```bash
   curl -I https://your-app.vercel.app | grep -E "(X-Frame|CSP|HSTS|X-Content)"
   # Should show all security headers
   ```

5. [ ] **Verify CORS restrictions:**
   ```bash
   curl -H "Origin: https://malicious-site.com" http://localhost:8888/api/cards?q=test
   # Should NOT include Access-Control-Allow-Origin header
   ```

6. [ ] **Manual testing:**
   - [ ] Search for Pokemon cards
   - [ ] View card details
   - [ ] Check browser console for errors
   - [ ] Verify no API keys in Network tab
   - [ ] Test from production domain

---

## 📞 Support & Questions

If you need help with any of these tasks:

1. Check the main audit report: `SECURITY-AUDIT-COMPREHENSIVE.md`
2. Review Vercel security documentation
3. Consult OWASP guidelines
4. Test in staging environment first

---

## 📅 Timeline

**Week 1 (Immediate):**
- Day 1: TODO-1, TODO-2 (API key rotation & removal)
- Day 2-3: TODO-3 (Git history cleanup - coordinate with team)
- Day 4-5: TODO-4 (Frontend migration)

**Week 2 (High Priority):**
- Day 1: TODO-5, TODO-6 (Security headers & CORS)
- Day 2: TODO-7 (Logger security)

**Week 3 (Medium/Low Priority):**
- TODO-8, TODO-9, TODO-10 (Cleanup tasks)
- TODO-11, TODO-12 (Documentation & automation)

---

**Remember:** Security is an ongoing process, not a one-time fix!

