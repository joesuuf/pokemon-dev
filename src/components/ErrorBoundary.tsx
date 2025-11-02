/**
 * Error Boundary Component
 * 
 * Catches React errors and service worker errors gracefully,
 * preventing the entire application from crashing.
 */

import { Component, ErrorInfo, ReactNode } from 'react';
import { logger } from '../utils/logger';
import { isWebviewEnvironment } from '../utils/serviceWorkerHandler';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

/**
 * ErrorBoundary component that catches React errors
 * and handles service worker errors gracefully
 */
export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    // Check if this is a service worker error
    const errorMessage = error.message || String(error);
    const isServiceWorkerError =
      errorMessage.includes('service worker') ||
      errorMessage.includes('ServiceWorker') ||
      errorMessage.includes('service-worker') ||
      errorMessage.includes('AbortError') ||
      errorMessage.includes('Failed to register');

    // Don't update state for service worker errors in webview environments
    if (isServiceWorkerError && isWebviewEnvironment()) {
      logger.warn('Service worker error caught by error boundary (suppressed)');
      return { hasError: false }; // Don't trigger error state
    }

    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    const errorMessage = error.message || String(error);
    const isServiceWorkerError =
      errorMessage.includes('service worker') ||
      errorMessage.includes('ServiceWorker') ||
      errorMessage.includes('service-worker') ||
      errorMessage.includes('AbortError') ||
      errorMessage.includes('Failed to register');

    // Log error, but suppress service worker errors in webview environments
    if (isServiceWorkerError && isWebviewEnvironment()) {
      logger.warn(
        `Service worker error caught by error boundary (suppressed in webview) - ${window.location.href}`
      );
      // Reset error state to prevent error UI from showing
      this.setState({ hasError: false, error: null, errorInfo: null });
      return;
    }

    // Log other errors normally
    logger.error('Error caught by error boundary', {
      url: window.location.href,
    });
    this.setState({ error, errorInfo });

    // Log to console for debugging
    if (process.env.NODE_ENV === 'development') {
      console.error('ErrorBoundary caught an error:', error, errorInfo);
    }
  }

  render() {
    if (this.state.hasError) {
      // Use custom fallback if provided
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default error UI
      return (
        <div
          style={{
            padding: '20px',
            textAlign: 'center',
            color: '#d32f2f',
            backgroundColor: '#ffebee',
            borderRadius: '8px',
            margin: '20px',
          }}
        >
          <h2>Something went wrong</h2>
          <p>
            {this.state.error?.message ||
              'An unexpected error occurred. Please refresh the page.'}
          </p>
          {process.env.NODE_ENV === 'development' && this.state.errorInfo && (
            <details style={{ marginTop: '20px', textAlign: 'left' }}>
              <summary>Error Details (Development Only)</summary>
              <pre style={{ overflow: 'auto', fontSize: '12px' }}>
                {this.state.error?.stack}
                {this.state.errorInfo.componentStack}
              </pre>
            </details>
          )}
          <button
            onClick={() => {
              this.setState({ hasError: false, error: null, errorInfo: null });
              window.location.reload();
            }}
            style={{
              marginTop: '20px',
              padding: '10px 20px',
              backgroundColor: '#1976d2',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            Reload Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
