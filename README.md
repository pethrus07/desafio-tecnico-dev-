# Cortex Analytics Platform

![status](https://img.shields.io/badge/status-em%20desenvolvimento-blue)
![backend](https://img.shields.io/badge/backend-FastAPI-009688)
![frontend](https://img.shields.io/badge/frontend-React-61DAFB)
![ml](https://img.shields.io/badge/ML-scikit--learn-F7931E)
![license](https://img.shields.io/badge/license-MIT-green)

> Plataforma analítica full-stack para **monitoramento operacional**, **pipeline ETL**, **dashboards interativos** e **inteligência preditiva** (detecção de anomalias e predição de falhas).

---

## 1. Visão Geral e a Dor

Operações industriais e de infraestrutura geram um volume contínuo de telemetria — temperatura, vibração, pressão, tempo de operação — mas esses dados costumam ficar **espalhados, sem monitoramento centralizado e sem capacidade preditiva**. O resultado é o pior cenário possível: a falha só é percebida quando o equipamento já parou.

**O que está sendo resolvido?**
A falta de uma camada única que ingere telemetria bruta, calcula métricas operacionais e antecipa falhas antes que elas aconteçam — saindo da manutenção reativa para a **manutenção preditiva**.

**Quem sofre com esse problema?**
Times de operação, manutenção e confiabilidade que dependem de planilhas isoladas e inspeção manual, sem visão consolidada de saúde dos ativos nem alertas automáticos.

**Por que isso importa para produto/negócio?**
Downtime não planejado é caro. Cada hora de parada de um ativo crítico significa perda de produção e custo de emergência. Antecipar a falha com horas/dias de antecedência transforma uma parada catastrófica em uma manutenção programada.

---

## 2. Arquitetura e Decisões Técnicas

| Camada | Escolha | Por que escolhi isso? | Alternativa considerada | Nota de impacto |
|---|---|---|---|---|
| **Front-end** | React + Vite + TailwindCSS + Recharts | Ecossistema maduro, build instantâneo com Vite e Recharts nativo para séries temporais sem reinventar gráficos | Vue / Streamlit | Time-to-market e UX de dashboard |
| **Back-end** | FastAPI (Python) | Mantém front e ML na mesma linguagem do pipeline de dados; tipagem com Pydantic e docs OpenAPI automáticas | Flask, Node.js | Integração direta com Pandas/sklearn |
| **Banco de dados** | PostgreSQL (prod) / SQLite (dev) | Postgres para transações e queries analíticas; SQLite como fallback para o avaliador rodar em segundos sem Docker | MongoDB, DynamoDB | Consistência + zero-friction no dev |
| **ETL / Dados** | Pandas | Padrão de fato para transformação tabular; agregações expressivas em poucas linhas | Spark, Polars | Simplicidade no volume atual |
| **API / Integração** | REST (OpenAPI) | Contrato claro, fácil de consumir pelo front e documentação interativa via `/docs` | GraphQL, gRPC | Curva de adoção baixa |
| **IA / Dados** | scikit-learn (Isolation Forest + Random Forest) | Isolation Forest não exige rótulos (anomalia é rara); Random Forest é robusto e entrega *feature importance* explicável ao negócio | TensorFlow/LSTM | Custo, explicabilidade, baixo overfitting |
| **Infra** | Docker + docker-compose | Sobe banco, API e front com um comando; reproduzível | Setup manual | Onboarding e deploy |

**Fluxo de dados:**

```
Raw Events  ──►  ETL (Pandas)  ──►  Database  ──►  Analytics / ML  ──►  Dashboard
 (sensores)      transform+load     metrics/alerts   predictions         KPIs/gráficos
```

---

## 3. Demonstração

O fluxo principal cabe em 15 segundos: subir o backend com dados de seed, abrir o dashboard, clicar em **"Rodar ETL + Modelos ML"** e ver os KPIs, a telemetria e o painel de risco/anomalia preenchidos.

- **Demo / Deploy:** _[adicionar link do Vercel (front) + Render (API) após o deploy]_
- **Docs interativas da API:** `http://localhost:8000/docs`

---

## 4. Destaque de Engenharia / "The Hard Part"

O ponto mais interessante é o **pipeline ETL com Pandas que é idempotente e alimenta diretamente a camada de ML**. Ele extrai os eventos brutos, agrega por ativo, persiste métricas derivadas e gera alertas por limiar — tudo recomputável sem duplicar dados:

```python
# backend/app/etl/pipeline.py  (trecho)
def run_etl(db: Session) -> dict:
    df = _events_to_dataframe(db)          # EXTRACT: eventos -> DataFrame
    if df.empty:
        return {"processed_events": 0, "metrics": 0, "alerts": 0}

    # TRANSFORM: agregações por ativo em uma única passagem
    agg = (
        df.groupby("asset_id")
        .agg(
            avg_temperature=("temperature", "mean"),
            max_temperature=("temperature", "max"),
            avg_vibration=("vibration", "mean"),
            avg_pressure=("pressure", "mean"),
            total_runtime=("runtime_hours", "max"),
        )
        .reset_index()
    )

    # Idempotência: limpa o derivado antes de recomputar (sem duplicar histórico)
    db.query(models.Metric).delete()
    db.query(models.Alert).delete()

    for _, row in agg.iterrows():
        # LOAD: grava métricas + dispara alertas por limiar operacional
        if row["max_temperature"] > THRESHOLDS["temperature"]:
            db.add(models.Alert(asset_id=int(row["asset_id"]),
                                severity="critical", source="threshold",
                                message=f"Temperatura {row['max_temperature']:.1f}°C acima do limite."))
    db.commit()
```

**Por que importa:** o ETL é determinístico e reprocessável (rodar duas vezes não corrompe nada), e as mesmas features agregadas servem de entrada para o Random Forest. Na prática, o modelo identificou a **temperatura como a variável de maior peso (≈0.57 de importância)** para o risco de falha — um insight acionável que sai direto do pipeline para o negócio.

---

## 5. Insights e Valor de Negócio

- **Para produto:** dashboard único com KPIs (uptime, alertas, temperatura média) substitui inspeção manual e planilhas; o botão de pipeline torna a análise sob demanda.
- **Para negócio:** antecipar falha = trocar parada não planejada (cara) por manutenção programada (barata). Cada alerta `high_risk` é uma ordem de serviço preventiva.
- **Para dados / IA:** a *feature importance* responde "o que mais leva esse ativo a falhar?". Hipóteses testáveis: limiar ideal de temperatura por tipo de ativo, correlação vibração × runtime, janela ótima de antecedência da predição.

---

## 6. Instruções de Instalação e Uso

### Opção A — Rápida (sem Docker, usa SQLite)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/cortex-analytics-platform.git
cd cortex-analytics-platform

# 2. Backend
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py                  # popula dados sintéticos de demonstração
uvicorn app.main:app --reload   # API em http://localhost:8000  (docs em /docs)

# 3. Frontend (em outro terminal)
cd ../frontend
npm install
npm run dev                     # dashboard em http://localhost:5173
```

### Opção B — Docker (PostgreSQL completo)

```bash
cp .env.example .env
docker compose up --build
# frontend: http://localhost:5173  |  backend: http://localhost:8000
# (rode o seed dentro do container do backend: docker compose exec backend python seed.py)
```

### Uso

1. Abra o dashboard em `http://localhost:5173`.
2. Clique em **"Rodar ETL + Modelos ML"** — isso executa o pipeline ETL, treina o Isolation Forest (anomalias) e o Random Forest (risco de falha).
3. Veja os KPIs, a telemetria dos sensores e o painel de predições preenchidos. Alertas aparecem no rodapé.

---

## 7. Roadmap / Próximos Passos

- **V1 — Base** ✅ — estrutura, API REST, ETL, dashboard com KPIs e gráficos.
- **V2 — Machine Learning** ✅ — Isolation Forest (anomalias) + Random Forest (predição de falha) com alertas automáticos.
- **V3 — Tempo real** — ingestão e atualização via WebSocket, alertas em streaming.
- **V4 — Observabilidade** — métricas Prometheus + dashboards Grafana.
- **V5 — Escala** — ingestão via Kafka, deploy cloud, persistência de modelos versionados.
- **Engenharia** — migrations com Alembic, testes (pytest + Vitest), CI/CD, code-splitting do bundle front.

---

## Estrutura do Projeto

```
cortex-analytics-platform/
├── backend/
│   ├── app/
│   │   ├── main.py            # app FastAPI + CORS + routers
│   │   ├── database.py        # engine (Postgres/SQLite) + sessão
│   │   ├── models.py          # Asset, Event, Metric, Alert, Prediction
│   │   ├── schemas.py         # Pydantic
│   │   ├── routers/           # events, metrics/etl, alerts, predictions(ML)
│   │   ├── etl/pipeline.py    # ETL com Pandas
│   │   └── ml/                # anomaly.py (IsolationForest) + failure_prediction.py (RandomForest)
│   ├── seed.py                # dados sintéticos de demonstração
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # dashboard
│   │   ├── api.js             # camada de acesso à API
│   │   └── components/        # KPICard, MetricsChart, AlertsPanel, PredictionsPanel
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Licença

MIT — sinta-se livre para usar como base de estudo ou portfólio.
