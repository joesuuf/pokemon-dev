# Security Audit - Action Items & To-Do List

**Date:** November 1, 2025  
**Audit Version:** 2.0  
**Overall Score:** 85/100 ?

---

## ?? Critical Priority (Fix Immediately)

### Issue #1: Timer Cleanup Memory Leak
**Severity:** ?? Critical  
**File:** `src/App.tsx:64-72`  
**Impact:** Potential memory leak if component unmounts during search  
**Estimated Effort:** 1 hour

#### To-Do List:
- [ ] **Task 1.1:** Identify current timer implementation location
  - [ ] Open `src/App.tsx`
  - [ ] Locate `handleSearch` function (around line 36)
  - [ ] Find `setInterval` call (around line 64)
  - [ ] Document current implementation

- [ ] **Task 1.2:** Create useEffect hook for timer management
  - [ ] Add new `useEffect` hook after state declarations
  - [ ] Move timer logic into useEffect
  - [ ] Add `loading` as dependency
  - [ ] Implement cleanup function with `clearInterval`

- [ ] **Task 1.3:** Remove timer from handleSearch function
  - [ ] Remove `setInterval` from `handleSearch`
  - [ ] Remove `clearInterval` calls from handleSearch
  - [ ] Keep timer state updates in useEffect

- [ ] **Task 1.4:** Test timer cleanup
  - [ ] Test search functionality
  - [ ] Test component unmount during search
  - [ ] Verify no memory leaks in React DevTools
  - [ ] Test timer stops when loading completes

- [ ] **Task 1.5:** Commit changes
  - [ ] Stage `src/App.tsx`
  - [ ] Commit with message: "fix: move timer to useEffect to prevent memory leaks"

**Code Reference:**
```typescript
// BEFORE (current - problematic)
const handleSearch = async (params: SearchParams) => {
  const timerInterval = setInterval(() => {
    setTimeRemaining(prev => prev - 1);
  }, 1000);
  // Timer may not cleanup if component unmounts
};

// AFTER (recommended)
useEffect(() => {
  let timerInterval: NodeJS.Timeout | null = null;
  
  if (loading) {
    timerInterval = setInterval(() => {
      setTimeRemaining(prev => {
        if (prev <= 1) return 0;
        return prev - 1;
      });
    }, 1000);
  }
  
  return () => {
    if (timerInterval) {
      clearInterval(timerInterval);
    }
  };
}, [loading]);
```

---

## ?? High Priority (Fix Within 24-48 Hours)

### Issue #2: Console Logging in Production Code
**Severity:** ?? High  
**Files:** `src/App.tsx`, `src/services/pokemonTcgApi.ts`, `api/cards.ts`  
**Impact:** Performance overhead, information leakage, security risk  
**Estimated Effort:** 2-3 hours

#### To-Do List:

- [ ] **Task 2.1:** Audit all console statements
  - [ ] Search for `console.log` in `src/`
  - [ ] Search for `console.warn` in `src/`
  - [ ] Search for `console.error` in `src/`
  - [ ] Document all instances with file and line numbers
  - [ ] Categorize: keep (console.error), remove (console.log), migrate (to logger)

- [ ] **Task 2.2:** Review centralized logger utility
  - [ ] Open `src/utils/logger.ts`
  - [ ] Review logger implementation
  - [ ] Check if it supports log levels
  - [ ] Verify environment-based logging

- [ ] **Task 2.3:** Migrate console.log to logger utility
  - [ ] Update `src/App.tsx` (2 instances)
    - [ ] Line 61: Replace `console.log` with logger.info
    - [ ] Keep `console.error` at line 84 (or migrate to logger.error)
  - [ ] Update `src/services/pokemonTcgApi.ts` (12+ instances)
    - [ ] Replace `console.log` with logger.debug/info
    - [ ] Replace `console.warn` with logger.warn
    - [ ] Migrate `console.error` to logger.error
  - [ ] Update `api/cards.ts` (5+ instances)
    - [ ] Replace `console.log` with logger.info
    - [ ] Migrate `console.error` to logger.error

- [ ] **Task 2.4:** Configure production build to strip console statements
  - [ ] Open `vite.config.ts`
  - [ ] Add rollup plugin for console stripping
  - [ ] Configure to keep `console.error` (critical errors)
  - [ ] Strip `console.log`, `console.warn`, `console.debug`, `console.info`

- [ ] **Task 2.5:** Test logging in development and production
  - [ ] Run `npm run dev` - verify logs appear
  - [ ] Run `npm run build`
  - [ ] Run `npm run preview` - verify logs stripped
  - [ ] Verify console.error still works in production

- [ ] **Task 2.6:** Commit changes
  - [ ] Stage all modified files
  - [ ] Commit with message: "refactor: migrate console logging to centralized logger and strip in production"

**Code Reference:**
```typescript
// vite.config.ts - Add console stripping
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      plugins: [
        {
          name: 'strip-console',
          transform(code, id) {
            if (id.includes('node_modules')) return null;
            // Keep console.error for critical errors
            return code.replace(/console\.(log|warn|debug|info)\([^)]*\);?/g, '');
          }
        }
      ]
    }
  }
});
```

---

## ?? Medium Priority (Fix Within Sprint)

### Issue #3: Missing Content Security Policy (CSP)
**Severity:** ?? Medium  
**Files:** `index.html`, `v2/index.html`  
**Impact:** XSS protection, security headers  
**Estimated Effort:** 1 hour

#### To-Do List:

- [ ] **Task 3.1:** Review current CSP implementation
  - [ ] Check `v2/index.html` - CSP already exists
  - [ ] Check `index.html` (React app) - CSP missing
  - [ ] Review v2 CSP policy

- [ ] **Task 3.2:** Add CSP meta tag to React app
  - [ ] Open `index.html`
  - [ ] Add CSP meta tag in `<head>` section
  - [ ] Configure policy:
    - `default-src 'self'`
    - `script-src 'self' 'unsafe-inline' 'unsafe-eval'` (for Vite)
    - `style-src 'self' 'unsafe-inline'`
    - `img-src 'self' data: https://*.pokemontcg.io https://via.placeholder.com`
    - `connect-src 'self' https://api.pokemontcg.io`
    - `font-src 'self' data:`
    - `frame-ancestors 'none'`

- [ ] **Task 3.3:** Test CSP in development
  - [ ] Run `npm run dev`
  - [ ] Check browser console for CSP violations
  - [ ] Verify images load correctly
  - [ ] Verify API calls work

- [ ] **Task 3.4:** Configure CSP via Vercel (alternative/optional)
  - [ ] Open `vercel.json`
  - [ ] Add headers section for CSP
  - [ ] Apply to all routes

- [ ] **Task 3.5:** Commit changes
  - [ ] Stage `index.html` (and `vercel.json` if modified)
  - [ ] Commit with message: "security: add Content Security Policy headers"

---

### Issue #4: Missing X-Frame-Options Header
**Severity:** ?? Medium  
**Files:** `index.html`, `vercel.json`  
**Impact:** Clickjacking protection  
**Estimated Effort:** 30 minutes

#### To-Do List:

- [ ] **Task 4.1:** Add X-Frame-Options meta tag
  - [ ] Open `index.html`
  - [ ] Add meta tag in `<head>`: `<meta http-equiv="X-Frame-Options" content="DENY">`
  - [ ] Open `v2/index.html`
  - [ ] Add same meta tag

- [ ] **Task 4.2:** Configure via Vercel (preferred)
  - [ ] Open `vercel.json`
  - [ ] Add headers section if not exists
  - [ ] Add X-Frame-Options header for all routes
  - [ ] Set value to "DENY"

- [ ] **Task 4.3:** Test header configuration
  - [ ] Deploy to preview/staging
  - [ ] Check response headers using browser DevTools
  - [ ] Verify X-Frame-Options: DENY header present

- [ ] **Task 4.4:** Commit changes
  - [ ] Stage `index.html`, `v2/index.html`, `vercel.json`
  - [ ] Commit with message: "security: add X-Frame-Options header to prevent clickjacking"

**Code Reference:**
```json
// vercel.json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ]
}
```

---

## ?? Low Priority (Backlog)

### Issue #5: External Link Security (Future)
**Severity:** ?? Low  
**Status:** ? No issues currently (no external links)  
**Action:** When adding external links in future

#### To-Do List (When Needed):

- [ ] **Task 5.1:** Review external links
  - [ ] Search for `<a href="http` or `<a href="https`
  - [ ] Identify external links

- [ ] **Task 5.2:** Add rel="noopener noreferrer"
  - [ ] For each external link with `target="_blank"`
  - [ ] Add `rel="noopener noreferrer"`
  - [ ] Verify links work correctly

- [ ] **Task 5.3:** Commit changes
  - [ ] Commit with message: "security: add noopener noreferrer to external links"

---

## Summary Checklist

### Critical (Fix Immediately)
- [ ] Issue #1: Timer Cleanup Memory Leak

### High Priority (24-48 Hours)
- [ ] Issue #2: Console Logging Cleanup

### Medium Priority (Within Sprint)
- [ ] Issue #3: Content Security Policy
- [ ] Issue #4: X-Frame-Options Header

### Low Priority (Backlog)
- [ ] Issue #5: External Link Security (when needed)

---

## Testing Checklist

After completing each issue, verify:
- [ ] No console errors in browser
- [ ] Application functionality works correctly
- [ ] Security headers present (check DevTools Network tab)
- [ ] No memory leaks (React DevTools Profiler)
- [ ] Build succeeds: `npm run build`
- [ ] Tests pass: `npm test`

---

**Last Updated:** November 1, 2025  
**Next Review:** After each issue completion
