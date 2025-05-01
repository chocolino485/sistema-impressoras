# Sistema de Gerenciamento de Impressoras

Sistema web desenvolvido em Flask para gerenciamento de impressoras, clientes, chamados técnicos e vendas.

## Funcionalidades

- Gestão de Clientes
- Controle de Equipamentos
- Gerenciamento de Chamados Técnicos
- Sistema de Vendas
- Controle de Estoque
- Gestão de Usuários com diferentes níveis de acesso

## Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/sistema-impressoras.git
cd sistema-impressoras
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta
DATABASE_URL=sqlite:///database.db
```

5. Inicialize o banco de dados:
```bash
flask db upgrade
```

## Executando o Sistema

Para executar em desenvolvimento:
```bash
python app.py
```

Para produção, use o Gunicorn:
```bash
gunicorn app:app
```

## Acesso Remoto

Para acessar o sistema remotamente, você pode:

1. Hospedar em um servidor VPS (DigitalOcean, AWS, etc.)
2. Usar serviços como Heroku, PythonAnywhere
3. Configurar seu roteador para acesso externo (port forwarding)

## Segurança

- Mantenha o arquivo `.env` seguro e nunca o compartilhe
- Use HTTPS em produção
- Faça backup regular do banco de dados
- Mantenha as dependências atualizadas

## Suporte

Para suporte, entre em contato através de [seu-email@dominio.com] 