# Front-End Refresh Guide

**Date:** November 1, 2025  
**Branch:** `critical-performance-fixes`

---

## Quick Answer

### React Apps (Ports 6666 & 8888)
**You can just refresh the page** - Vite's Hot Module Replacement (HMR) should pick up most changes automatically, but with the structural changes we made (adding hooks, memoization), a **hard refresh is recommended** to ensure you're seeing the latest code.

### Static HTML Apps (Ports 9999 & 7777)
**Refresh the page** - These are static files, so you'll need to refresh to see changes.

---

## Detailed Breakdown

### Port 6666 - React 19 (Vite Dev Server)
- **HMR Status:** ? Enabled
- **Action:** Hard refresh (Ctrl+Shift+R or Cmd+Shift+R) recommended
- **Why:** We added new React hooks (useEffect, useCallback) which sometimes require a refresh
- **Alternative:** Regular refresh should work, but hard refresh ensures clean state

### Port 8888 - React Main (Vite Dev Server)
- **HMR Status:** ? Enabled
- **Action:** Hard refresh (Ctrl+Shift+R or Cmd+Shift+R) recommended
- **Why:** Same as above - structural changes to components
- **Alternative:** Regular refresh should work

### Port 9999 - Pure HTML v2 (Static Files)
- **HMR Status:** ? Not available (static files)
- **Action:** **Refresh required** (F5 or Ctrl+R)
- **Why:** No hot reload for static HTML files
- **Note:** No changes were made to v2 files in this branch

### Port 7777 - Carousel (Static Files)
- **HMR Status:** ? Not available (static files)
- **Action:** **Refresh required** (F5 or Ctrl+R)
- **Why:** No hot reload for static HTML files
- **Note:** No changes were made to carousel files in this branch

---

## What Changed

### Files Modified (React Apps):
- `src/App.tsx` - Added useEffect, useCallback hooks
- `src/components/CardList.tsx` - Wrapped with React.memo
- `src/components/GridCardItem.tsx` - Wrapped with React.memo, added useCallback
- `src/components/CardDisplay.tsx` - Wrapped with React.memo
- `src/components/SearchForm.tsx` - Wrapped with React.memo, added useCallback
- `src/components/LoadingSpinner.tsx` - Wrapped with React.memo
- `src/components/ErrorMessage.tsx` - Wrapped with React.memo

### Files NOT Modified:
- `v2/` directory - No changes
- `carousel/` directory - No changes

---

## Recommended Refresh Steps

### For React Apps (6666, 8888):

1. **Hard Refresh (Recommended):**
   - Windows/Linux: `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`
   - This clears cache and ensures latest code

2. **Or Regular Refresh:**
   - Press `F5` or `Ctrl+R` (Windows/Linux)
   - Press `Cmd+R` (Mac)
   - HMR should handle most changes

3. **If Issues Persist:**
   - Open DevTools (F12)
   - Right-click refresh button ? "Empty Cache and Hard Reload"
   - Or close and reopen the browser tab

### For Static Apps (9999, 7777):

1. **Simple Refresh:**
   - Press `F5` or `Ctrl+R` (Windows/Linux)
   - Press `Cmd+R` (Mac)

2. **Hard Refresh (if needed):**
   - Windows/Linux: `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`

---

## How to Verify You're Seeing New Code

### Check 1: React DevTools
1. Open React DevTools (browser extension)
2. Check component tree
3. Components should show `Memo()` wrapper in DevTools

### Check 2: Browser Console
1. Open DevTools Console (F12)
2. Look for any errors
3. Should see no errors related to hooks or memoization

### Check 3: Network Tab
1. Open DevTools ? Network tab
2. Hard refresh
3. Check that JavaScript files are reloaded (not cached)

### Check 4: Timer Behavior
1. Perform a search
2. Timer should countdown from 60
3. If you navigate away or cancel search, timer should clean up (no memory leaks)

---

## Troubleshooting

### If Changes Don't Appear:

1. **Check Branch:**
   ```bash
   git branch --show-current
   ```
   Should show: `critical-performance-fixes`

2. **Check Server Status:**
   ```bash
   # Check if servers are running
   curl http://localhost:6666
   curl http://localhost:8888
   ```

3. **Restart Dev Server (if needed):**
   ```bash
   # Stop current server (Ctrl+C)
   # Restart
   npm run dev:6666  # For port 6666
   npm run dev       # For port 8888
   ```

4. **Clear Browser Cache:**
   - DevTools ? Application ? Clear Storage
   - Or use incognito/private window

---

## Expected Behavior After Refresh

### What You Should See:

1. **Same Functionality:**
   - Search still works
   - Cards still display
   - All features work as before

2. **Performance Improvements (Behind the Scenes):**
   - Components only re-render when needed
   - Timer properly cleans up
   - Better memory management

3. **No Visual Changes:**
   - UI looks identical
   - Changes are performance optimizations only

---

## Summary

**For React Apps (6666, 8888):**
- ? Just refresh the page (hard refresh recommended)
- ? Vite HMR should pick up changes
- ? If unsure, use hard refresh (Ctrl+Shift+R)

**For Static Apps (9999, 7777):**
- ? Just refresh the page
- ? No changes were made to these files anyway

**Bottom Line:** Refresh your browser tabs and you should see the updated code with all performance optimizations!

---

**Last Updated:** November 1, 2025
