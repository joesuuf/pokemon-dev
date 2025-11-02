import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  root: resolve(__dirname, 'frontends/port-5555'),
  publicDir: resolve(__dirname, 'frontends/port-5555'),
  server: {
    port: 5555,
    strictPort: true,
    host: '0.0.0.0',
    hmr: {
      host: '0.0.0.0',
      port: 5555,
      protocol: 'ws',
    },
    watch: {
      usePolling: true,
      interval: 1000,
    },
  },
  build: {
    outDir: resolve(__dirname, 'dist/port-5555')
  }
})
