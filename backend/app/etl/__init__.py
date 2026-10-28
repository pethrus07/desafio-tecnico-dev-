"""O ETL: evento bruto vira métrica agregada e alerta por limiar.

Um módulo só, `pipeline.py`. Fica fora dos routers de propósito: a regra de
transformação não deveria depender do transporte HTTP — a mesma função
serviria a um agendador ou a um script de linha de comando.
"""
