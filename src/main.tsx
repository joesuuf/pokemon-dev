import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
import { handleServiceWorkerErrors } from './utils/serviceWorkerHandler'
import { ErrorBoundary } from './components/ErrorBoundary'

// Handle service worker errors gracefully (especially for VS Code/Cursor webviews)
handleServiceWorkerErrors()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>,
)
