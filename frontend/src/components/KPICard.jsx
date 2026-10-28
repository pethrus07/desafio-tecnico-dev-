/**
 * O quadrado de número do topo do dashboard. Puro: rótulo, valor, sufixo, tom.
 * O `tone` existe para a cor mudar sem o componente saber o que o número
 * significa — quem decide se um uptime é bom é o App.jsx, e é lá que a regra
 * fica visível em vez de escondida na peça de tela.
 */
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
