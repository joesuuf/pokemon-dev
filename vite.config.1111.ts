import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  root: resolve(__dirname, 'frontends/port-1111'),
  publicDir: resolve(__dirname, 'frontends/port-1111'),
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
    outDir: resolve(__dirname, 'dist/port-1111'),
    emptyOutDir: false
  }
})
