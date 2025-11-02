import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 8888,
    strictPort: false,
    host: '0.0.0.0', // Allow access from Codespaces and WSL (public)
  }
})