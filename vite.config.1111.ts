import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  root: resolve(__dirname, 'hub'),
  publicDir: resolve(__dirname, 'hub'),
  server: {
    port: 1111,
    strictPort: true,
    host: '0.0.0.0'
  },
  build: {
    outDir: resolve(__dirname, 'dist/hub')
  }
})
