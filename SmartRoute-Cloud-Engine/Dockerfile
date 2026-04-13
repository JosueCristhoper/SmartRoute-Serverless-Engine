FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalamos herramientas de Linux necesarias para PostgreSQL y conexiones seguras con Azure
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 8000