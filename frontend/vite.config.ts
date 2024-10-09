import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import compression from 'vite-plugin-compression2';

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
      sourcemap: false
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
