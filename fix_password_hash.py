import os
import subprocess
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_password_hash():
    try:
        # Obter a URL do banco de dados do ambiente
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL não encontrada nas variáveis de ambiente")
        
        logger.info("Iniciando processo de correção do campo password_hash...")
        
        # 1. Remover a tabela user
        logger.info("Removendo tabela user...")
        drop_table_cmd = f'psql "{database_url}" -c "DROP TABLE IF EXISTS \\"user\\" CASCADE;"'
        subprocess.run(drop_table_cmd, shell=True, check=True)
        logger.info("Tabela user removida com sucesso!")
        
        # 2. Recriar a tabela user
        logger.info("Recriando tabela user...")
        create_table_cmd = f'''psql "{database_url}" -c "
            CREATE TABLE \\"user\\" (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                password_hash TEXT,
                role VARCHAR(20) NOT NULL,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                created_at TIMESTAMP
            );"
        '''
        subprocess.run(create_table_cmd, shell=True, check=True)
        logger.info("Tabela user recriada com sucesso!")
        
        logger.info("Processo de correção concluído com sucesso!")
        logger.info("Agora você pode criar os usuários através da interface do sistema.")
        
    except Exception as e:
        logger.error(f"Erro durante o processo de correção: {e}")
        raise

if __name__ == '__main__':
    fix_password_hash() 