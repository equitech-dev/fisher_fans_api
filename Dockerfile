FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copier et rendre le script exécutable
COPY wait-for-db.sh /app/wait-for-db.sh
RUN chmod +x /app/wait-for-db.sh

ENV PYTHONPATH=/app

# Commande unique pour exécuter le script d'attente, charger les données et démarrer l'API
CMD ["sh", "-c", "/app/wait-for-db.sh && python /app/load_data.py && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
