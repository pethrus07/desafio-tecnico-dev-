"""Os routers da API, um por assunto.

`events` (ativos e leituras), `metrics` (ETL e KPIs), `alerts` e `predictions`
(ML). Cada um traz o próprio `prefix`, então nenhum caminho é montado aqui —
para saber a URL de uma rota, olhe o `APIRouter(...)` do arquivo dela.
"""
