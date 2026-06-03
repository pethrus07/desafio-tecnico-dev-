export default function AlertsPanel({ alerts }) {
  const colors = {
    critical: "border-cortex-crit text-cortex-crit",
    warning: "border-cortex-warn text-cortex-warn",
    info: "border-cortex-accent text-cortex-accent",
  };

  return (
    <div className="bg-cortex-card rounded-xl p-5 border border-white/5 shadow-lg">
      <h2 className="text-sm font-semibold text-gray-200 mb-4">Alertas</h2>
      {alerts.length === 0 ? (
        <p className="text-gray-500 text-sm">Nenhum alerta. Rode o ETL e os modelos.</p>
      ) : (
        <ul className="space-y-2 max-h-72 overflow-auto">
          {alerts.map((a) => (
            <li
              key={a.id}
              className={`border-l-4 pl-3 py-2 bg-black/20 rounded ${colors[a.severity] || colors.info}`}
            >
              <div className="flex justify-between">
                <span className="text-xs uppercase font-semibold">{a.severity}</span>
                <span className="text-[10px] text-gray-500">{a.source}</span>
              </div>
              <p className="text-sm text-gray-200">{a.message}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
