from app import app, db
from models import User

def create_test_users():
    users = [
        {'username': 'tecnico1', 'name': 'Técnico Teste', 'email': 'tecnico@teste.com', 'role': 'tecnico', 'password': 'tecnico123'},
        {'username': 'suporte1', 'name': 'Suporte Teste', 'email': 'suporte@teste.com', 'role': 'suporte', 'password': 'suporte123'},
        {'username': 'financeiro1', 'name': 'Financeiro Teste', 'email': 'financeiro@teste.com', 'role': 'financeiro', 'password': 'financeiro123'},
        {'username': 'estoque1', 'name': 'Estoque Teste', 'email': 'estoque@teste.com', 'role': 'estoque', 'password': 'estoque123'},
    ]
    with app.app_context():
        for u in users:
            if not User.query.filter_by(username=u['username']).first():
                user = User(
                    username=u['username'],
                    name=u['name'],
                    email=u['email'],
                    role=u['role']
                )
                user.set_password(u['password'])
                db.session.add(user)
        db.session.commit()
        print('Usuários de teste criados com sucesso!')

if __name__ == '__main__':
    create_test_users() 