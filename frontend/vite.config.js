import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  test: {
    testOptions: {
      files: ['**/*.spec.js']
    },
    environment: "happy-dom"
  },
  publicPath: process.env.NODE_ENV === 'production'
    ? '/media/'  // Ruta donde se encuentran los archivos estáticos
    : '/'
})
