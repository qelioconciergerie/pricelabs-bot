# Base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    chromium \
    chromium-driver \
    && apt-get clean

# Set display port
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the web server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
