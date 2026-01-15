# Dockerfile
FROM python:3.10-slim


# Créer un dossier de travail
WORKDIR /app


# Copier les fichiers
COPY requirements.txt ./
COPY main.py ./


# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt


# Installer les navigateurs Playwright + dépendances
RUN apt-get update && apt-get install -y wget gnupg && \
pip install playwright && \
playwright install --with-deps


# Lancer l'application Flask
CMD ["python", "main.py"]
