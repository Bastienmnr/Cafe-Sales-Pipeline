# Dockerfile pour le pipeline de nettoyage café
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le code source et les données
COPY src/ src/
COPY requirements.txt ./
COPY data/ data/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Définir le volume pour les données
VOLUME ["/app/data"]

# Commande par défaut : exécuter le pipeline
CMD ["python", "src/main.py"]
