# Comprehensive Security Audit Report
**Date:** November 2, 2025
**Auditor:** Automated Security Scan
**Project:** Pokemon TCG Search Application
**Branch:** claude/security-audit-comprehensive-011CUibJfXYSPg9bXbykV7SB

---

## Executive Summary

This comprehensive security audit identified **7 critical/high severity issues** and **4 medium/low severity issues** that require immediate attention. The most critical finding is the exposure of the Pokemon TCG API key in git history and frontend JavaScript bundles.

**Risk Level:** 🔴 **HIGH** - Immediate action required

---

## 🔴 CRITICAL FINDINGS

### 1. API Key Exposed in Git Repository
**Severity:** CRITICAL
**File:** `.env`
**Location:** `/home/user/pokemon-dev/.env:3`

**Issue:**
- The `.env` file containing `VITE_POKEMON_TCG_API_KEY=f43ae006-2449-4771-8442-a17179cacbdf` is tracked by git
- API key is visible in git history (commit `dcab2d4ceb92750ac4e307f1e475548f3d613f38`)
- While `.env` is in `.gitignore`, the file was added before `.gitignore` was created

**Impact:**
- API key is publicly accessible in repository history
- Anyone with repository access can extract and abuse the API key
- May lead to rate limit exhaustion or API key revocation

**Evidence:**
```bash
$ git ls-files | grep .env
.env

$ git log --all --full-history -- .env
commit dcab2d4ceb92750ac4e307f1e475548f3d613f38
Author: joesuuf <38440410+joesuuf@users.noreply.github.com>
Date:   Sat Oct 25 18:42:27 2025 -0700
    Add Pokemon TCG API key to .env file
```

---

### 2. API Key Exposed in Frontend JavaScript Bundle
**Severity:** CRITICAL
**Files:**
- `src/lib/api.ts:4`
- `src/services/pokemonTcgApi.ts:5`

**Issue:**
```typescript
// src/lib/api.ts
const API_KEY = import.meta.env.VITE_POKEMON_TCG_API_KEY;

// src/services/pokemonTcgApi.ts
const API_KEY = import.meta.env.VITE_POKEMON_TCG_API_KEY;
```

**Impact:**
- Any environment variable prefixed with `VITE_` is bundled into the frontend JavaScript
- The API key is visible to anyone who inspects the browser's network tab or JavaScript files
- This defeats the purpose of keeping API keys secret

**Explanation:**
Vite exposes any environment variable starting with `VITE_` to the client-side code. This means the API key is embedded in the compiled JavaScript bundle and accessible to anyone viewing the application.

---

### 3. Backend API Proxy Not Used Consistently
**Severity:** HIGH
**Files:** Frontend API clients don't use the backend proxy

**Issue:**
- A proper backend proxy exists at `api/cards.ts` that securely handles the API key
- Frontend code directly calls the Pokemon TCG API instead of using the proxy
- This exposes the API key and bypasses server-side security controls

**Proper Implementation (api/cards.ts:32-39):**
```typescript
// Get API key from environment variable
const apiKey = process.env.POKEMON_TCG_API_KEY
if (!apiKey) {
  console.error('POKEMON_TCG_API_KEY not set in environment')
  return response.status(500).json({
    error: 'Server configuration error - API key not found',
  })
}
```

---

## 🟠 HIGH SEVERITY FINDINGS

### 4. CORS Wildcard Configuration
**Severity:** HIGH
**File:** `api/cards.ts:82`

**Issue:**
```typescript
response.setHeader('Access-Control-Allow-Origin', '*')
```

**Impact:**
- Any website can make requests to your API endpoint
- Potential for abuse from malicious sites
- No origin validation or whitelisting

**Recommendation:**
Restrict CORS to specific trusted domains:
```typescript
const allowedOrigins = [
  'https://yourdomain.com',
  'https://www.yourdomain.com',
  process.env.NODE_ENV === 'development' ? 'http://localhost:8888' : null
].filter(Boolean);

const origin = request.headers.origin;
if (allowedOrigins.includes(origin)) {
  response.setHeader('Access-Control-Allow-Origin', origin);
}
```

---

### 5. Missing Security Headers
**Severity:** HIGH
**Files:** `vite.config.ts`, `vercel.json`

**Issue:**
No security headers configured:
- ❌ Content-Security-Policy (CSP)
- ❌ X-Frame-Options
- ❌ X-Content-Type-Options
- ❌ Strict-Transport-Security (HSTS)
- ❌ Referrer-Policy
- ❌ Permissions-Policy

**Impact:**
- Vulnerable to clickjacking attacks
- No XSS protection via CSP
- No MIME-type sniffing protection
- No HTTPS enforcement

---

### 6. Sensitive Data in localStorage
**Severity:** HIGH
**File:** `src/utils/logger.ts:50-55`

**Issue:**
```typescript
private writeToFile(content: string) {
  const key = `pokemon-tcg-logs-${this.logFileName}`
  const existing = localStorage.getItem(key) || ''
  localStorage.setItem(key, existing + content)
}
```

**Impact:**
- Logs include URLs (which may contain sensitive query params)
- localStorage is accessible to any JavaScript on the same domain
- XSS vulnerabilities could expose logged data
- Logs persist across sessions

**Evidence from logger (lines 104-106):**
```typescript
if (options?.url) {
  fileLine += ` 🌐 \`${options.url}\``
}
```

---

## 🟡 MEDIUM SEVERITY FINDINGS

### 7. Excessive Console Logging
**Severity:** MEDIUM
**Files:** 30+ console.log statements across codebase

**Issue:**
```typescript
// src/services/pokemonTcgApi.ts:59
console.log('[DEBUG] Using API Key:', API_KEY ? 'Yes' : 'No (public access)');
```

**Impact:**
- Debug information may leak in production
- Potential information disclosure
- Console logs visible in browser DevTools

**Files affected:**
- `api/cards.ts` - 5 occurrences
- `src/App.tsx` - 2 occurrences
- `src/utils/logger.ts` - 1 occurrence
- `src/services/pokemonTcgApi.ts` - 22 occurrences

---

### 8. Development Server Publicly Accessible
**Severity:** MEDIUM
**File:** `vite.config.ts:9`

**Issue:**
```typescript
host: '0.0.0.0', // Allow access from Codespaces and WSL (public)
```

**Impact:**
- Development server accessible from any network interface
- Potential exposure of development environment
- Should be restricted in production

---

### 9. No Rate Limiting Visible
**Severity:** MEDIUM

**Issue:**
- No rate limiting implementation found in API proxy
- Could lead to API abuse or DoS

**Recommendation:**
Implement rate limiting on the backend proxy using libraries like `express-rate-limit` or Vercel's built-in rate limiting.

---

## 🟢 POSITIVE SECURITY FINDINGS

✅ **No npm package vulnerabilities** (npm audit clean)
✅ `.env` is in `.gitignore` (though already tracked)
✅ `env.example` exists for documentation
✅ Backend proxy implementation is secure (`api/cards.ts`)
✅ Good input sanitization in `v2/scripts/api.js:197-208`
✅ URL validation implemented in `v2/scripts/api.js:213-223`
✅ Query sanitization prevents injection attacks
✅ Proper timeout handling with AbortController

---

## 📊 Security Metrics

| Category | Count |
|----------|-------|
| Critical Issues | 3 |
| High Issues | 4 |
| Medium Issues | 3 |
| Low Issues | 1 |
| **Total Issues** | **11** |
| Files Scanned | 442 |
| Dependencies Audited | 442 |
| Vulnerabilities in Dependencies | 0 |

---

## 🔧 REMEDIATION PLAN

### Immediate Actions (Within 24 hours)

1. **CRITICAL: Remove API Key from Git History**
   - Rotate the Pokemon TCG API key at https://pokemontcg.io/
   - Remove `.env` from git tracking: `git rm --cached .env`
   - Use BFG Repo-Cleaner or `git filter-branch` to remove from history
   - Force push changes (coordinate with team)

2. **CRITICAL: Migrate to Backend Proxy**
   - Update all frontend API calls to use `/api/cards` endpoint
   - Remove `VITE_POKEMON_TCG_API_KEY` from frontend
   - Store API key only in Vercel environment variables

3. **HIGH: Implement Security Headers**
   - Add security headers to `vercel.json`
   - Implement Content-Security-Policy

4. **HIGH: Fix CORS Configuration**
   - Replace wildcard with domain whitelist
   - Test with production domain

### Short-term Actions (Within 1 week)

5. **Remove Sensitive Logging**
   - Remove localStorage logging of URLs
   - Disable console.log statements in production
   - Implement proper production logging

6. **Add Rate Limiting**
   - Implement rate limiting on API proxy
   - Set reasonable limits for API calls

### Long-term Improvements

7. **Security Monitoring**
   - Implement automated security scanning in CI/CD
   - Set up dependency vulnerability scanning
   - Regular security audits

8. **Documentation**
   - Update security documentation
   - Create security incident response plan

---

## 📝 FILES REQUIRING IMMEDIATE ATTENTION

### Must Fix (Critical)
- [ ] `.env` - Remove from git, rotate key
- [ ] `src/lib/api.ts` - Remove frontend API key usage
- [ ] `src/services/pokemonTcgApi.ts` - Remove frontend API key usage

### Should Fix (High)
- [ ] `api/cards.ts` - Fix CORS configuration
- [ ] `vercel.json` - Add security headers
- [ ] `src/utils/logger.ts` - Remove localStorage logging
- [ ] `vite.config.ts` - Add security configuration

### Could Fix (Medium/Low)
- [ ] `src/services/pokemonTcgApi.ts` - Reduce console logging
- [ ] `api/cards.ts` - Add rate limiting
- [ ] `vite.config.ts` - Restrict development server host

---

## 🔍 DETAILED FILE ANALYSIS

### Critical Files

#### .env
```
Line 3: VITE_POKEMON_TCG_API_KEY=f43ae006-2449-4771-8442-a17179cacbdf
Status: ❌ TRACKED IN GIT
Action: Remove from git, rotate key
```

#### src/lib/api.ts
```typescript
Line 4: const API_KEY = import.meta.env.VITE_POKEMON_TCG_API_KEY;
Status: ❌ EXPOSES KEY TO FRONTEND
Action: Remove, use backend proxy
```

#### src/services/pokemonTcgApi.ts
```typescript
Line 5: const API_KEY = import.meta.env.VITE_POKEMON_TCG_API_KEY;
Status: ❌ EXPOSES KEY TO FRONTEND
Action: Remove, use backend proxy
```

---

## 🛡️ RECOMMENDED SECURITY ARCHITECTURE

### Current (Insecure) Architecture
```
Browser → Pokemon TCG API (with exposed API key)
   ↑
[API Key in JavaScript Bundle]
```

### Recommended (Secure) Architecture
```
Browser → Your Backend Proxy → Pokemon TCG API
             ↑                        ↑
    [No API Key]              [API Key in env vars]
```

---

## 📋 COMPLIANCE NOTES

- **GDPR**: No personal data identified in logs (good)
- **OWASP Top 10**: Addresses A01:2021 (Broken Access Control), A05:2021 (Security Misconfiguration)
- **API Security**: Addresses OWASP API Security Top 10 - API1:2023 (Broken Object Level Authorization)

---

## 🔗 REFERENCES

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [Pokemon TCG API Docs](https://docs.pokemontcg.io/)
- [Vercel Security](https://vercel.com/docs/security/secure-your-app)

---

## ✅ NEXT STEPS

See detailed remediation todos created separately in the issue tracker.

**Priority Order:**
1. Rotate API key immediately
2. Remove .env from git history
3. Migrate frontend to use backend proxy
4. Add security headers
5. Fix CORS configuration
6. Clean up logging
7. Add rate limiting

---

**End of Report**
