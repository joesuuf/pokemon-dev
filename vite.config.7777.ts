import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  root: resolve(__dirname, 'frontends/port-7777'),
  publicDir: resolve(__dirname, 'frontends/port-7777'),
  server: {
    port: 7777,
    strictPort: true,
    host: true
  },
  build: {
    outDir: resolve(__dirname, 'dist/port-7777')
  }
})
