"""Os dois modelos de scikit-learn que rodam sobre os eventos.

`anomaly.py` (Isolation Forest, sem rótulo nenhum) e `failure_prediction.py`
(Random Forest, com rótulo tirado do próprio campo `status`). Nenhum dos dois
persiste modelo em disco: treinam a cada chamada, sobre o banco inteiro.
"""
