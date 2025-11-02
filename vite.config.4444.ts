import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 4444,
    host: '0.0.0.0',
    strictPort: true,
  },
  build: {
    outDir: 'dist-4444',
  },
  root: '.',
  publicDir: 'public',
});





