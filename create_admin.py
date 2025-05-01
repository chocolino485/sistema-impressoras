from app import app, db
from models import User

def create_admin():
    with app.app_context():
        # Verifica se já existe um admin
        if User.query.filter_by(username='admin').first():
            print('Usuário admin já existe!')
            return

        # Cria o usuário admin
        admin = User(
            username='admin',
            name='Administrador',
            email='admin@example.com',
            role='suporte'
        )
        admin.set_password('admin123')  # Senha inicial

        db.session.add(admin)
        db.session.commit()
        print('Usuário admin criado com sucesso!')

if __name__ == '__main__':
    create_admin() 