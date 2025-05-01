from flask import Flask
from dotenv import load_dotenv
import os
from extensions import db, login_manager, migrate

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///erp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização das extensões
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate.init_app(app, db)

# Importação dos modelos e rotas
from models import *
from routes import *

if __name__ == '__main__':
    print("Iniciando o servidor...")
    try:
        with app.app_context():
            db.create_all()
            print("Banco de dados inicializado com sucesso!")
        print(f"Servidor iniciando em http://192.168.0.34:5000")
        app.run(debug=True, host='192.168.0.34', port=5000)
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}") 