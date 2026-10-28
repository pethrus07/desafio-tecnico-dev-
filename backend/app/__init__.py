"""Pacote da aplicação Cortex: a API FastAPI, o ETL e os modelos de ML.

Todo o backend vive aqui. O pacote é importado como `app` — o uvicorn e o
Dockerfile sobem `app.main:app` —, então o diretório de trabalho é sempre
`backend/`, nunca a raiz do repositório. Rodar de outro lugar quebra o import.
"""
