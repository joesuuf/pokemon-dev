# Service Worker Error Handling Fix

## Problem
VS Code/Cursor webview environments were throwing errors when trying to register service workers:
```
Error: Could not register service worker: AbortError: Failed to register a ServiceWorker
```

This error was occurring in GitHub Codespaces webview environments and was causing the application to fail to load.

## Solution

### 1. Service Worker Error Handler (`src/utils/serviceWorkerHandler.ts`)
Created a comprehensive error handler that:
- Detects webview environments (VS Code/Cursor, GitHub Codespaces)
- Intercepts service worker registration errors
- Suppresses harmless service worker errors in webview environments
- Provides safe service worker registration utility functions
- Logs errors appropriately without crashing the application

### 2. Error Boundary Component (`src/components/ErrorBoundary.tsx`)
Created a React Error Boundary that:
- Catches React errors gracefully
- Specifically handles service worker errors
- Suppresses service worker errors in webview environments
- Provides user-friendly error UI for other errors
- Includes development-mode error details

### 3. Integration (`src/main.tsx`)
Updated the main entry point to:
- Initialize service worker error handling on app startup
- Wrap the application in an ErrorBoundary component
- Ensure errors are caught before they crash the app

## Key Features

### Webview Detection
The handler detects webview environments by checking:
- Hostname patterns (`github.dev`, `githubusercontent.com`, `vscode-cdn.net`)
- User agent strings
- Document referrer patterns

### Error Suppression
- Service worker errors in webview environments are logged but suppressed
- Other errors are handled normally
- Application continues to function even if service worker registration fails

### Logging
- Errors are logged using the existing logger utility
- Warnings are logged for suppressed service worker errors
- Debug information is available in development mode

## Usage

The error handling is automatically active when the application loads. No additional configuration is needed.

If you need to register your own service worker in the future, use the `safeRegisterServiceWorker` utility:

```typescript
import { safeRegisterServiceWorker } from './utils/serviceWorkerHandler';

// Safely register a service worker
const registration = await safeRegisterServiceWorker('/sw.js');
if (registration) {
  console.log('Service worker registered successfully');
} else {
  console.log('Service worker registration failed (non-critical)');
}
```

## Testing

To test the fix:
1. Open the application in a VS Code/Cursor webview (GitHub Codespaces)
2. Check the browser console - service worker errors should be suppressed
3. Verify the application loads and functions normally
4. Check logs for service worker error warnings (expected and harmless)

## Files Changed

- `src/utils/serviceWorkerHandler.ts` (new)
- `src/components/ErrorBoundary.tsx` (new)
- `src/main.tsx` (updated)

## Branch Information

This fix is on branch: `cursor/handle-webview-service-worker-abort-error-8716`

## Notes

- Service worker errors in webview environments are expected and harmless
- The application does not use service workers itself - this fix handles IDE/webview infrastructure errors
- All error handling is non-intrusive and doesn't affect normal application functionality
