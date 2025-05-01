from app import app, db
from models import User
from create_admin import create_admin
from create_test_users import create_test_users

def init_database():
    with app.app_context():
        print("Criando tabelas do banco de dados...")
        db.create_all()
        print("Tabelas criadas com sucesso!")
        
        print("Criando usuário admin...")
        create_admin()
        
        print("Criando usuários de teste...")
        create_test_users()
        
        print("Inicialização do banco de dados concluída!")

if __name__ == '__main__':
    init_database() 