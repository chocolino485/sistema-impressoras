from flask import Flask
from dotenv import load_dotenv
import os
import logging
from extensions import db, login_manager, migrate

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações do aplicativo
logger.info("Configurando variáveis de ambiente...")
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/erp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger.info(f"DATABASE_URL configurada como: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Garantir que o diretório instance existe
if not os.path.exists('instance'):
    logger.info("Criando diretório instance...")
    os.makedirs('instance')
    logger.info("Diretório instance criado com sucesso!")

# Inicialização das extensões
logger.info("Inicializando extensões...")
try:
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    migrate.init_app(app, db)
    logger.info("Extensões inicializadas com sucesso!")
except Exception as e:
    logger.error(f"Erro ao inicializar extensões: {e}")
    raise

# Importação dos modelos e rotas
logger.info("Importando modelos e rotas...")
from models import *
from routes import *
logger.info("Modelos e rotas importados com sucesso!")

@app.before_first_request
def create_tables():
    logger.info("Tentando criar tabelas do banco de dados...")
    try:
        db.create_all()
        logger.info("Tabelas criadas com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {e}")
        raise

if __name__ == '__main__':
    logger.info("Iniciando o servidor...")
    try:
        with app.app_context():
            db.create_all()
            logger.info("Banco de dados inicializado com sucesso!")
        logger.info(f"Servidor iniciando em http://0.0.0.0:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Erro ao iniciar o servidor: {e}")
        raise 