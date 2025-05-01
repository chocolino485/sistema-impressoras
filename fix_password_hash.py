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
            
            # 1. Fazer backup dos usuários existentes
            users = User.query.all()
            user_data = []
            for user in users:
                user_data.append({
                    'username': user.username,
                    'name': user.name,
                    'email': user.email,
                    'role': user.role,
                    'password_hash': user.password_hash,
                    'created_at': user.created_at
                })
            
            logger.info(f"Backup de {len(user_data)} usuários concluído")
            
            # 2. Remover a tabela user
            logger.info("Removendo tabela user...")
            User.__table__.drop(db.engine)
            logger.info("Tabela user removida com sucesso!")
            
            # 3. Recriar a tabela user
            logger.info("Recriando tabela user...")
            User.__table__.create(db.engine)
            logger.info("Tabela user recriada com sucesso!")
            
            # 4. Restaurar os usuários
            logger.info("Restaurando usuários...")
            for user_data in user_data:
                user = User(
                    username=user_data['username'],
                    name=user_data['name'],
                    email=user_data['email'],
                    role=user_data['role'],
                    password_hash=user_data['password_hash'],
                    created_at=user_data['created_at']
                )
                db.session.add(user)
            
            db.session.commit()
            logger.info("Usuários restaurados com sucesso!")
            
            logger.info("Processo de correção concluído com sucesso!")
            
        except Exception as e:
            logger.error(f"Erro durante o processo de correção: {e}")
            raise

if __name__ == '__main__':
    fix_password_hash() 