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
