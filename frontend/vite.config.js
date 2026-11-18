import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
  server: { port: 5173, strictPort: true },
  preview: { port: 4173 },
  test: {
    environment: 'jsdom',
    include: ['tests/**/*.{test,spec}.js', 'src/**/*.{test,spec}.js'],
  },
})
