# Utiliser l'image officielle Python slim
FROM python:3.11-slim

# Créer un utilisateur non-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires pour MySQL
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt et changer le propriétaire
COPY --chown=appuser:appuser requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source et changer le propriétaire
COPY --chown=appuser:appuser . .

# Changer le propriétaire du répertoire de travail
RUN chown -R appuser:appuser /app

# Passer à l'utilisateur non-root
USER appuser

# Exposer le port 8000
EXPOSE 8000

# Commande par défaut pour démarrer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 