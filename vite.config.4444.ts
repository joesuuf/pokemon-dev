import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 4444,
    host: '0.0.0.0',
    strictPort: true,
    hmr: {
      host: '0.0.0.0',
      port: 4444,
      protocol: 'ws',
    },
    watch: {
      usePolling: true,
      interval: 1000,
    },
  },
  build: {
    outDir: resolve(__dirname, 'dist/port-4444'),
  },
  // Point Vite root to the OCR frontend folder
  root: resolve(__dirname, 'frontends/port-4444'),
  publicDir: resolve(__dirname, 'frontends/port-4444'),
});





