from app import app, db
from models import User
from create_admin import create_admin
from create_test_users import create_test_users
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    logger.info("Iniciando processo de inicialização do banco de dados...")
    
    # Garantir que o diretório instance existe
    if not os.path.exists('instance'):
        logger.info("Criando diretório instance...")
        os.makedirs('instance')
        logger.info("Diretório instance criado com sucesso!")
    
    with app.app_context():
        try:
            logger.info("Criando tabelas do banco de dados...")
            db.create_all()
            logger.info("Tabelas criadas com sucesso!")
            
            logger.info("Criando usuário admin...")
            create_admin()
            
            logger.info("Criando usuários de teste...")
            create_test_users()
            
            logger.info("Inicialização do banco de dados concluída com sucesso!")
        except Exception as e:
            logger.error(f"Erro durante a inicialização do banco de dados: {e}")
            raise

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        logger.error(f"Falha na inicialização do banco de dados: {e}")
        raise 