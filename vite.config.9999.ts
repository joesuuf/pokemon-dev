import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  root: resolve(__dirname, 'frontends/port-9999'),
  publicDir: resolve(__dirname, 'frontends/port-9999'),
  server: {
    port: 9999,
    strictPort: true,
    host: true
  },
  build: {
    outDir: resolve(__dirname, 'dist/port-9999')
  }
})
