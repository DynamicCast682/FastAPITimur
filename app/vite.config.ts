import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
// need to activate CORS to http://127.0.0.1:8000 
export default defineConfig({
  plugins: [react()],
  base: '/',
  publicDir: 'static',
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api': {
        target: "http://127.0.0.1:8000",
        // changeOrigin: true,
      }
    }
  },
})
