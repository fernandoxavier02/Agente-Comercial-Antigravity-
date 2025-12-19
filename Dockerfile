# Usar imagem leve do Python
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY backend ./backend
COPY worker ./worker
COPY prompts ./prompts

# Configurar Python Path
ENV PYTHONPATH=/app

# Cloud Run fornece a porta via variável PORT
ENV PORT=8080

# Criar script de inicialização
RUN echo '#!/bin/sh\n\
    cd /app/backend\n\
    exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}\n\
    ' > /start.sh && chmod +x /start.sh

# Comando para iniciar o servidor
CMD ["/start.sh"]
