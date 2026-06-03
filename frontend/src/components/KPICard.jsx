export default function KPICard({ label, value, suffix = "", tone = "accent" }) {
  const tones = {
    accent: "text-cortex-accent",
    ok: "text-cortex-ok",
    warn: "text-cortex-warn",
    crit: "text-cortex-crit",
  };

  return (
    <div className="bg-cortex-card rounded-xl p-5 border border-white/5 shadow-lg">
      <p className="text-xs uppercase tracking-wider text-gray-400">{label}</p>
      <p className={`mt-2 text-3xl font-bold ${tones[tone]}`}>
        {value}
        <span className="text-base font-normal text-gray-400 ml-1">{suffix}</span>
      </p>
    </div>
  );
}
