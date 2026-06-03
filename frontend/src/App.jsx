import { useEffect, useState } from "react";
import { api } from "./api";
import KPICard from "./components/KPICard";
import MetricsChart from "./components/MetricsChart";
import AlertsPanel from "./components/AlertsPanel";
import PredictionsPanel from "./components/PredictionsPanel";

export default function App() {
  const [summary, setSummary] = useState(null);
  const [events, setEvents] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function loadAll() {
    try {
      setError(null);
      const [s, e, a, p] = await Promise.all([
        api.summary(),
        api.events(),
        api.alerts(),
        api.predictions(),
      ]);
      setSummary(s);
      setEvents(e);
      setAlerts(a);
      setPredictions(p);
    } catch {
      setError("Não consegui falar com a API. O backend está rodando na :8000?");
    }
  }

  // Roda ETL + os dois modelos em sequência e recarrega a tela.
  async function runPipelines() {
    setLoading(true);
    try {
      await api.runEtl();
      await api.runAnomalies();
      await api.runFailures();
      await loadAll();
    } catch {
      setError("Erro ao rodar os pipelines.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAll();
  }, []);

  return (
    <div className="min-h-screen p-6 max-w-7xl mx-auto">
      <header className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">
            Cortex <span className="text-cortex-accent">Analytics</span>
          </h1>
          <p className="text-sm text-gray-400">
            Monitoramento operacional, ETL e análise preditiva
          </p>
        </div>
        <button
          onClick={runPipelines}
          disabled={loading}
          className="bg-cortex-accent hover:bg-blue-600 disabled:opacity-50 text-white text-sm font-semibold px-4 py-2 rounded-lg transition"
        >
          {loading ? "Processando..." : "Rodar ETL + Modelos"}
        </button>
      </header>

      {error && (
        <div className="bg-cortex-crit/20 border border-cortex-crit text-cortex-crit rounded-lg p-3 mb-6 text-sm">
          {error}
        </div>
      )}

      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
          <KPICard label="Ativos" value={summary.total_assets} />
          <KPICard label="Eventos" value={summary.total_events} />
          <KPICard label="Alertas" value={summary.open_alerts} tone="warn" />
          <KPICard label="Temp. média" value={summary.avg_temperature} suffix="°C" />
          <KPICard label="Vibração média" value={summary.avg_vibration} suffix="mm/s" />
          <KPICard
            label="Uptime"
            value={summary.uptime_pct}
            suffix="%"
            tone={summary.uptime_pct > 90 ? "ok" : "warn"}
          />
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <MetricsChart events={events} />
        </div>
        <PredictionsPanel predictions={predictions} />
        <div className="lg:col-span-3">
          <AlertsPanel alerts={alerts} />
        </div>
      </div>

      <footer className="mt-8 text-center text-xs text-gray-600">
        Cortex Analytics Platform · FastAPI · React · scikit-learn
      </footer>
    </div>
  );
}
