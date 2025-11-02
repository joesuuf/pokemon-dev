import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // Base path for GitHub Pages - empty string means root deployment
  base: '/',
  server: {
    port: 8888,
    strictPort: false,
    host: '0.0.0.0', // Allow access from Codespaces and WSL (public)
    hmr: {
      host: '0.0.0.0',
      port: 8888,
      protocol: 'ws',
    },
    watch: {
      usePolling: true, // Enable polling for file watching (needed for WSL/remote)
      interval: 1000, // Poll interval in milliseconds
    },
  },
})