// Base da API. Em dev o Vite faz proxy de /api -> :8000, então fica vazia.
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
