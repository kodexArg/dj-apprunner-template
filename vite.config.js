import { defineConfig } from 'vite';

export default defineConfig({
  base: '/static/',
  build: {
    manifest: 'manifest.json',
    outDir: 'static/dist',
    rollupOptions: {
      input: {
        main: 'frontend/main.js',
      },
    },
  },
}); 