import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import compression from 'vite-plugin-compression2';
import prerenderPlugin from './vite/prerenderPlugin';

const envDir = path.resolve(__dirname, '../');

export default defineConfig(({ mode }) => {
  return {
    envDir,
    plugins: [
      react(),
      compression({
        algorithm: 'brotliCompress',
        include: /\.(js|css|html|svg|json|txt|ico|xml)$/,
        deleteOriginalAssets: false,
      }),
      compression({
        algorithm: 'gzip',
        include: /\.(js|css|html|svg|json|txt|ico|xml)$/,
        deleteOriginalAssets: false,
      }),
      prerenderPlugin(),
    ],
    server: {
      host: true,
      port: 3000,
      watch: {
        usePolling: true,
      },
    },
    build: {
      outDir: './build',
      emptyOutDir: true,
      sourcemap: false,
      rollupOptions: {
        output: {
          manualChunks: {
            react: ['react', 'react-dom', 'react-router-dom'],
            mui: ['@mui/material', '@emotion/react', '@emotion/styled'],
            redux: ['@reduxjs/toolkit', 'react-redux', 'redux-persist'],
          },
        },
      },
    },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
    optimizeDeps: {
      include: ['@mui/material/Tooltip', '@emotion/styled', '@mui/material/Unstable_Grid2', '@emotion/react'],
    },
    define: {
      'process.env': {
        MODE: mode,
      },
    },
  };
});
