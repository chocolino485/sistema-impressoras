from app import app, db
from models import User
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_password_hash():
    with app.app_context():
        try:
            logger.info("Iniciando processo de correção do campo password_hash...")
            
            # 1. Remover a tabela user usando SQL nativo
            logger.info("Removendo tabela user...")
            db.session.execute('DROP TABLE IF EXISTS "user" CASCADE')
            db.session.commit()
            logger.info("Tabela user removida com sucesso!")
            
            # 2. Recriar a tabela user usando SQL nativo
            logger.info("Recriando tabela user...")
            create_table_sql = """
            CREATE TABLE "user" (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                password_hash TEXT,
                role VARCHAR(20) NOT NULL,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                created_at TIMESTAMP
            )
            """
            db.session.execute(create_table_sql)
            db.session.commit()
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