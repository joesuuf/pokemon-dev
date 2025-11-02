/// <reference types="vite/client" />

interface ImportMetaEnv {
  // API keys are handled server-side via the proxy API
  // No client-side environment variables needed
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}