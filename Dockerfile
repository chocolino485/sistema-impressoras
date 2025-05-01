FROM python:3.8-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Criar diretório para o banco de dados SQLite e configurar permissões
RUN mkdir -p instance && \
    chmod 777 instance && \
    touch instance/erp.db && \
    chmod 666 instance/erp.db

# Inicializar o banco de dados
RUN python init_db.py

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"] 