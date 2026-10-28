/**
 * O tema do dashboard. A paleta `cortex` é a fonte da verdade das cores:
 * ok/warn/crit são semânticas (estado do ativo), não decorativas, e é por elas
 * que KPICard, AlertsPanel e PredictionsPanel escolhem cor sem repetir
 * hexadecimal. `content` precisa listar todo arquivo que use classe: o que não
 * for varrido aqui tem a classe removida do CSS final e some da tela.
 */
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        cortex: {
          bg: "#0b1020",
          card: "#141b2e",
          accent: "#3b82f6",
          ok: "#22c55e",
          warn: "#f59e0b",
          crit: "#ef4444",
        },
      },
    },
  },
  plugins: [],
};
