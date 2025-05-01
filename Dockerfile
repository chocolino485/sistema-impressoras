FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Criar diretório para o banco de dados SQLite
RUN mkdir -p instance && chmod 777 instance

# Inicializar o banco de dados
RUN python init_db.py

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"] 