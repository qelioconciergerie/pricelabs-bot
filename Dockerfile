# Utilise une image Python
FROM python:3.10-slim

# Crée un dossier de travail
WORKDIR /app

# Copie les fichiers nécessaires
COPY requirements.txt requirements.txt
COPY main.py main.py

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Lance l'application
CMD ["python", "main.py"]
