# Utiliser une image Python officielle
FROM python:3.10-slim

# Créer le dossier de l’app
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt requirements.txt
COPY main.py main.py

# Installer les dépendances
RUN pip install -r requirements.txt

# Lancer l’app Flask
CMD ["python", "main.py"]
