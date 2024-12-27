import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import fs from 'fs'; // Import biblioteki do obsługi plików

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    https: {
      key: fs.readFileSync('key.pem'), // Podaj ścieżkę do klucza
      cert: fs.readFileSync('cert.pem'), // Podaj ścieżkę do certyfikatu
    },
    port: 5173, // Port dla lokalnego serwera frontendu
  },
});
