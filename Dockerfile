FROM python:3.8-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Inicializar o banco de dados
RUN python init_db.py

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"] 