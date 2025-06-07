import { defineConfig } from 'vite';
import djangoVite from 'django-vite';

export default defineConfig({
  plugins: [
    djangoVite({
      input: [
        'frontend/main.js',
      ],
    })
  ],
  build: {
    outDir: 'static/dist',
    manifest: true,
    rollupOptions: {
      input: {
        main: 'frontend/main.js',
      },
    },
  },
}); 