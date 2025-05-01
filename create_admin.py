from app import app, db
from models import User

def create_admin():
    with app.app_context():
        # Remove o usuário admin existente se houver
        existing_admin = User.query.filter_by(username='admin').first()
        if existing_admin:
            db.session.delete(existing_admin)
            db.session.commit()
            print('Usuário admin existente removido!')

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