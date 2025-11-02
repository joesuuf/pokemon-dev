import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  root: resolve(__dirname, 'hub'),
  publicDir: resolve(__dirname, 'hub'),
  server: {
    port: 1111,
    strictPort: true,
    host: '0.0.0.0',
    hmr: {
      host: '0.0.0.0',
      port: 1111,
      protocol: 'ws',
    },
    watch: {
      usePolling: true,
      interval: 1000,
    },
  },
  build: {
    outDir: resolve(__dirname, 'dist/hub'),
    emptyOutDir: false
  }
})
