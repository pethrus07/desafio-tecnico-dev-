/**
 * Configuração do Vite. O que importa aqui é o proxy: é ele que permite o
 * front chamar "/api/..." sem base e sem esbarrar em CORS durante o
 * desenvolvimento. Esse proxy é coisa do servidor de dev e NÃO existe no
 * build — quem serve o `dist` precisa resolver /api por conta própria
 * (ver seção 8 de docs/ARQUITETURA.md).
 */
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Encaminha chamadas /api para o backend FastAPI em dev.
      "/api": "http://localhost:8000",
    },
  },
});
