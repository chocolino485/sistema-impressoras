from app import app, db
from models import User
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_password_hash():
    with app.app_context():
        try:
            logger.info("Iniciando processo de correção do campo password_hash...")
            
            # 1. Remover a tabela user
            logger.info("Removendo tabela user...")
            User.__table__.drop(db.engine)
            logger.info("Tabela user removida com sucesso!")
            
            # 2. Recriar a tabela user
            logger.info("Recriando tabela user...")
            User.__table__.create(db.engine)
            logger.info("Tabela user recriada com sucesso!")
            
            logger.info("Processo de correção concluído com sucesso!")
            logger.info("Agora você pode criar os usuários através da interface do sistema.")
            
        except Exception as e:
            logger.error(f"Erro durante o processo de correção: {e}")
            raise

if __name__ == '__main__':
    fix_password_hash()
    # Iniciar o servidor Flask
    app.run(host='0.0.0.0', port=5000, debug=True) 