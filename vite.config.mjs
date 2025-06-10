import { defineConfig } from 'vite';
import { viteStaticCopy } from 'vite-plugin-static-copy';

export default defineConfig({
  base: '/static/',
  build: {
    manifest: 'manifest.json',
    outDir: 'static/dist',
    rollupOptions: {
      input: {
        main: 'frontend/main.js',
        favicon: 'frontend/favicon.ico',
      },
    },
  },
  plugins: [
    viteStaticCopy({
      targets: [
        {
          src: 'frontend/favicon.ico',
          dest: '.'
        }
      ]
    })
  ]
}); 