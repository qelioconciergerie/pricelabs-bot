# Étape 1 : Utiliser une image officielle Python
FROM python:3.9-slim

# Étape 2 : Installer les dépendances système (pour Chrome + Selenium)
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    libgbm1 \
    libu2f-udev \
    libxshmfence-dev \
    && rm -rf /var/lib/apt/lists/*

# Étape 3 : Installer Google Chrome (Headless)
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Étape 4 : Installer ChromeDriver (compatibilité avec Chrome v121)
RUN CHROMEDRIVER_VERSION=`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Étape 5 : Définir le dossier de travail
WORKDIR /app

# Étape 6 : Copier les fichiers dans l'image Docker
COPY . /app

# Étape 7 : Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Étape 8 : Exposer le port Flask
EXPOSE 5000

# Étape 9 : Lancer le serveur Flask
CMD ["python", "main.py"]
