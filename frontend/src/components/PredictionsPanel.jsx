const RISK_COLORS = {
  high_risk: "bg-cortex-crit/20 text-cortex-crit",
  medium_risk: "bg-cortex-warn/20 text-cortex-warn",
  low_risk: "bg-cortex-ok/20 text-cortex-ok",
  anomalous: "bg-cortex-crit/20 text-cortex-crit",
  normal: "bg-cortex-ok/20 text-cortex-ok",
};

function Section({ title, modelName, items }) {
  return (
    <div>
      <div className="flex justify-between items-baseline mb-2">
        <h3 className="text-xs font-semibold text-gray-300">{title}</h3>
        <span className="text-[10px] text-gray-500">{modelName}</span>
      </div>
      {items.length === 0 ? (
        <p className="text-gray-500 text-sm">Sem predições. Rode o modelo.</p>
      ) : (
        <ul className="space-y-2">
          {items.map((p) => (
            <li key={p.id} className="flex justify-between items-center bg-black/20 rounded px-3 py-2">
              <span className="text-sm text-gray-200">Ativo #{p.asset_id}</span>
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-400">{(p.score * 100).toFixed(0)}%</span>
                <span className={`text-[11px] px-2 py-0.5 rounded ${RISK_COLORS[p.label] || ""}`}>
                  {p.label}
                </span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default function PredictionsPanel({ predictions }) {
  const failures = predictions.filter((p) => p.target === "failure_risk");
  const anomalies = predictions.filter((p) => p.target === "anomaly");

  return (
    <div className="bg-cortex-card rounded-xl p-5 border border-white/5 shadow-lg space-y-5">
      <h2 className="text-sm font-semibold text-gray-200">Inteligência Preditiva</h2>
      <Section title="Risco de falha" modelName="Random Forest" items={failures} />
      <Section title="Anomalias" modelName="Isolation Forest" items={anomalies} />
    </div>
  );
}
