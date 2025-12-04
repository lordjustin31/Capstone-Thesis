import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react({
      jsxImportSource: 'react',
    }),
  ],
  server: {
    port: 3000,
    fs: {
      strict: false,
    },
    proxy: {
      '/api': {
        target: 'https://capstone-thesis-w018.onrender.com',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    target: 'esnext',
    minify: 'terser',
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
    extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json'],
  },
})


// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react'
// import path from 'path'

// // https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [
//     react({
//       jsxImportSource: 'react',
//     }),
//   ],  
//   server: {
//     port: 3000,
//     proxy: {
//       '/api': {
//         target: 'https://caps-em1t.onrender.com',
//         changeOrigin: true,
//         rewrite: (path) => path.replace(/^\/api/, '/api'),
//       },
//     },
//   },
//   build: {
//     outDir: 'dist',
//     sourcemap: true,
//     target: 'esnext',
//     minify: 'terser',
//   },
//   resolve: {
//     alias: {
//       '@': path.resolve(__dirname, './src'),
//     },
//     extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json'],
//   },
// })
