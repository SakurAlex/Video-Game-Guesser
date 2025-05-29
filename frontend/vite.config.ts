import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

// production or development
const isProduction = process.env.NODE_ENV === 'production';

export default defineConfig({
  plugins: [svelte()],
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: isProduction ? 'http://backend:8000' : 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path
      }
    }
  }
}); 