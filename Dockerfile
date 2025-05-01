FROM python:3.8-slim

# Criar usuário não-root
RUN useradd -m myuser

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
    chown -R myuser:myuser /app && \
    chmod -R 755 /app && \
    chmod 777 instance

# Mudar para o usuário não-root
USER myuser

# Inicializar o banco de dados
RUN python init_db.py

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"] 