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

# Configurar o caminho do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')

app = Flask(__name__, instance_path=instance_path)

# Configurações do aplicativo
logger.info("Configurando variáveis de ambiente...")
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui')

# Configuração do banco de dados
if os.getenv('DATABASE_URL'):
    # Estamos no Render (produção)
    logger.info("Usando PostgreSQL (ambiente de produção)")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    # Desenvolvimento local
    logger.info("Usando SQLite (ambiente de desenvolvimento)")
    db_path = os.path.join(instance_path, 'erp.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    # Garantir que o diretório instance existe
    if not os.path.exists(instance_path):
        logger.info(f"Criando diretório instance em {instance_path}...")
        os.makedirs(instance_path, exist_ok=True)
        logger.info("Diretório instance criado com sucesso!")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger.info(f"DATABASE_URL configurada como: {app.config['SQLALCHEMY_DATABASE_URI']}")

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

def init_db():
    """Inicializa o banco de dados."""
    logger.info("Tentando criar tabelas do banco de dados...")
    try:
        with app.app_context():
            db.create_all()
            logger.info("Tabelas criadas com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {e}")
        raise

# Inicializar o banco de dados durante a inicialização do app
with app.app_context():
    init_db()

if __name__ == '__main__':
    logger.info("Iniciando o servidor...")
    try:
        logger.info(f"Servidor iniciando em http://0.0.0.0:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Erro ao iniciar o servidor: {e}")
        raise 