import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function MetricsChart({ events }) {
  // Inverte pra ficar em ordem cronológica e mapeia pro formato do gráfico.
  const data = events
    .slice()
    .reverse()
    .map((e, i) => ({
      idx: i,
      temperatura: e.temperature,
      vibracao: e.vibration,
      pressao: e.pressure,
    }));

  return (
    <div className="bg-cortex-card rounded-xl p-5 border border-white/5 shadow-lg">
      <h2 className="text-sm font-semibold text-gray-200 mb-4">
        Telemetria dos sensores
      </h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
          <XAxis dataKey="idx" stroke="#6b7280" tick={{ fontSize: 11 }} />
          <YAxis stroke="#6b7280" tick={{ fontSize: 11 }} />
          <Tooltip contentStyle={{ background: "#141b2e", border: "1px solid #334155" }} />
          <Legend />
          <Line type="monotone" dataKey="temperatura" stroke="#3b82f6" dot={false} />
          <Line type="monotone" dataKey="vibracao" stroke="#f59e0b" dot={false} />
          <Line type="monotone" dataKey="pressao" stroke="#22c55e" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
