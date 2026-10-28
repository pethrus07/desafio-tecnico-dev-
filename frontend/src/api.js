/**
 * A única camada que fala HTTP. Nenhum componente chama fetch direto.
 * Concentrar as sete chamadas aqui é o que permite trocar a base da API num
 * lugar só e o que garante que todo erro de rede chegue à tela com a mesma
 * cara — o `req` transforma status != 2xx em exceção, que é o que o App.jsx
 * espera para mostrar o aviso de "não consegui falar com a API".
 */
// Base da API. Em dev o Vite faz proxy de /api -> :8000, então fica vazia.
// No build a base é congelada dentro do bundle — `import.meta.env` é
// substituído em tempo de compilação, então definir VITE_API_URL depois de
// buildar não muda nada. A imagem Docker do front compila sem essa variável
// e o nginx dela não tem proxy: é o caminho em que a tela sobe e não
// encontra a API (ver seção 8 de docs/ARQUITETURA.md).
const BASE = import.meta.env.VITE_API_URL || "";

async function req(path, opts = {}) {
  const res = await fetch(`${BASE}${path}`, opts);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export const api = {
  summary: () => req("/api/dashboard/summary"),
  events: () => req("/api/events?limit=300"),
  alerts: () => req("/api/alerts"),
  predictions: () => req("/api/ml/predictions"),
  runEtl: () => req("/api/etl/run", { method: "POST" }),
  runAnomalies: () => req("/api/ml/anomalies/run", { method: "POST" }),
  runFailures: () => req("/api/ml/failures/run", { method: "POST" }),
};
