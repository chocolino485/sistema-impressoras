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
            
            # 3. Criar usuário de suporte
            logger.info("Criando usuário de suporte...")
            admin = User(
                username='suporte',
                name='Usuário Suporte',
                email='suporte@sistema.com',
                role='suporte'
            )
            admin.set_password('suporte123')  # Senha inicial
            db.session.add(admin)
            db.session.commit()
            logger.info("Usuário de suporte criado com sucesso!")
            
            logger.info("Processo de correção concluído com sucesso!")
            
        except Exception as e:
            logger.error(f"Erro durante o processo de correção: {e}")
            raise

if __name__ == '__main__':
    fix_password_hash() 