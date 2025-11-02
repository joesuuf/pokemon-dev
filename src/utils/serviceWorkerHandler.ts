/**
 * Service Worker Error Handler
 * 
 * Handles service worker registration errors gracefully, especially
 * for VS Code/Cursor webview environments where service worker registration
 * may fail due to security restrictions or network issues.
 */

import { logger } from './logger';

/**
 * Checks if we're running in a VS Code/Cursor webview environment
 */
export function isWebviewEnvironment(): boolean {
  return (
    typeof window !== 'undefined' &&
    (
      window.location.hostname.includes('github.dev') ||
      window.location.hostname.includes('githubusercontent.com') ||
      window.location.hostname.includes('vscode-cdn.net') ||
      document.referrer.includes('vscode-webview') ||
      // Check for VS Code webview user agent patterns
      navigator.userAgent.includes('vscode-webview') ||
      navigator.userAgent.includes('Code/')
    )
  );
}

/**
 * Handles service worker registration errors gracefully
 * 
 * This function intercepts unhandled service worker errors and prevents
 * them from crashing the application, especially in webview environments
 * where service worker registration may fail.
 */
export function handleServiceWorkerErrors(): void {
  if (typeof window === 'undefined' || typeof navigator === 'undefined') {
    return;
  }

  const isWebview = isWebviewEnvironment();

  // Override console.error to catch service worker errors
  const originalConsoleError = console.error;
  console.error = (...args: unknown[]) => {
    const errorMessage = args.join(' ');
    
    // Check if this is a service worker registration error
    if (
      typeof errorMessage === 'string' &&
      (
        errorMessage.includes('service worker') ||
        errorMessage.includes('ServiceWorker') ||
        errorMessage.includes('service-worker') ||
        errorMessage.includes('AbortError') ||
        errorMessage.includes('Failed to register')
      )
    ) {
      // Log the error for debugging but don't crash the app
      if (isWebview) {
        logger.warn(
          'Service worker registration failed in webview environment (this is expected and harmless)',
          { url: window.location.href }
        );
      } else {
        logger.warn(
          'Service worker registration failed (non-critical)',
          { url: window.location.href }
        );
      }
      
      // Suppress the error in webview environments
      if (isWebview) {
        return; // Don't log to console in webview
      }
    }
    
    // Call original console.error for other errors
    originalConsoleError.apply(console, args);
  };

  // Handle unhandled promise rejections related to service workers
  window.addEventListener('unhandledrejection', (event) => {
    const reason = event.reason;
    const errorMessage = reason?.message || reason?.toString() || String(reason);
    
    if (
      typeof errorMessage === 'string' &&
      (
        errorMessage.includes('service worker') ||
        errorMessage.includes('ServiceWorker') ||
        errorMessage.includes('service-worker') ||
        errorMessage.includes('AbortError') ||
        errorMessage.includes('Failed to register')
      )
    ) {
      // Prevent the error from bubbling up
      event.preventDefault();
      
      if (isWebview) {
        logger.warn(
          'Suppressed service worker registration error in webview',
          { url: window.location.href }
        );
      } else {
        logger.warn(
          'Suppressed service worker registration error',
          { url: window.location.href }
        );
      }
      
      // Return early to prevent default error handling
      return;
    }
  });

  // Handle error events related to service workers
  window.addEventListener('error', (event) => {
    const errorMessage = event.message || String(event.error);
    
    if (
      typeof errorMessage === 'string' &&
      (
        errorMessage.includes('service worker') ||
        errorMessage.includes('ServiceWorker') ||
        errorMessage.includes('service-worker') ||
        errorMessage.includes('AbortError') ||
        errorMessage.includes('Failed to register')
      )
    ) {
      // Prevent the error from bubbling up
      event.preventDefault();
      
      if (isWebview) {
        logger.warn(
          'Suppressed service worker error event in webview',
          { url: window.location.href }
        );
      } else {
        logger.warn(
          'Suppressed service worker error event',
          { url: window.location.href }
        );
      }
      
      return;
    }
  });

  // Log initialization
  if (isWebview) {
    logger.info('Service worker error handler initialized (webview environment detected)');
  } else {
    logger.info('Service worker error handler initialized');
  }
}

/**
 * Safely register a service worker if needed
 * 
 * This function should be used if you want to register your own
 * service worker. It handles errors gracefully.
 */
export async function safeRegisterServiceWorker(
  swPath: string,
  options?: RegistrationOptions
): Promise<ServiceWorkerRegistration | null> {
  if (typeof navigator === 'undefined' || !('serviceWorker' in navigator)) {
    logger.warn('Service workers are not supported in this environment');
    return null;
  }

  try {
    const registration = await navigator.serviceWorker.register(swPath, options);
    logger.info(`Service worker registered successfully: ${swPath}`);
    return registration;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    
    // Don't log errors in webview environments as they're expected
    if (!isWebviewEnvironment()) {
      logger.warn(`Service worker registration failed: ${errorMessage}`, {
        url: swPath
      });
    }
    
    return null;
  }
}
