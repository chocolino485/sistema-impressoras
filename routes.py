from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from extensions import db
from models import User, Cliente, Equipamento, Chamado, Produto, Venda, MovimentacaoEstoque
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta

# Configuração do upload de arquivos
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rotas de Autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Usuário ou senha inválidos')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rotas de Dashboard
@app.route('/')
@login_required
def dashboard():
    if current_user.role == 'estoque':
        # Exemplo de dados fictícios para o dashboard de estoque
        # Substitua por consultas reais ao banco conforme necessário
        total_entradas = 10
        total_saidas = 7
        saldo_atual = 50
        produtos_baixo = 2
        movimentacoes = []  # Preencha com as movimentações reais
        return render_template('dashboard_estoque.html',
            total_entradas=total_entradas,
            total_saidas=total_saidas,
            saldo_atual=saldo_atual,
            produtos_baixo=produtos_baixo,
            movimentacoes=movimentacoes
        )
    # Chamados do mês atual
    hoje = datetime.now()
    inicio_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    inicio_mes_passado = (inicio_mes - timedelta(days=1)).replace(day=1)
    fim_mes_passado = inicio_mes - timedelta(seconds=1)

    # Total de chamados mês atual e mês passado
    total_chamados = Chamado.query.filter(Chamado.created_at >= inicio_mes).count()
    total_chamados_passado = Chamado.query.filter(Chamado.created_at >= inicio_mes_passado, Chamado.created_at <= fim_mes_passado).count()
    chamados_percent = 0
    if total_chamados_passado > 0:
        chamados_percent = int(((total_chamados - total_chamados_passado) / total_chamados_passado) * 100)

    # Chamados concluídos mês atual e mês passado
    chamados_concluidos = Chamado.query.filter(Chamado.status == 'finalizado', Chamado.created_at >= inicio_mes).count()
    chamados_concluidos_passado = Chamado.query.filter(Chamado.status == 'finalizado', Chamado.created_at >= inicio_mes_passado, Chamado.created_at <= fim_mes_passado).count()
    concluidos_percent = 0
    if chamados_concluidos_passado > 0:
        concluidos_percent = int(((chamados_concluidos - chamados_concluidos_passado) / chamados_concluidos_passado) * 100)

    # Tempo médio de resolução (em dias)
    chamados_finalizados = Chamado.query.filter(Chamado.status == 'finalizado', Chamado.created_at >= inicio_mes).all()
    if chamados_finalizados:
        tempo_medio = sum([(c.updated_at - c.created_at).days for c in chamados_finalizados]) / len(chamados_finalizados)
        tempo_medio = round(tempo_medio, 1)
    else:
        tempo_medio = 0
    # Tempo médio mês passado
    chamados_finalizados_passado = Chamado.query.filter(Chamado.status == 'finalizado', Chamado.created_at >= inicio_mes_passado, Chamado.created_at <= fim_mes_passado).all()
    if chamados_finalizados_passado:
        tempo_medio_passado = sum([(c.updated_at - c.created_at).days for c in chamados_finalizados_passado]) / len(chamados_finalizados_passado)
        tempo_medio_passado = round(tempo_medio_passado, 1)
    else:
        tempo_medio_passado = 0
    tempo_medio_percent = 0
    if tempo_medio_passado > 0:
        tempo_medio_percent = int(((tempo_medio - tempo_medio_passado) / tempo_medio_passado) * 100)

    # Vendas do mês atual e mês passado
    vendas_mes = db.session.query(db.func.sum(Venda.valor_total)).filter(Venda.created_at >= inicio_mes).scalar() or 0
    vendas_mes_passado = db.session.query(db.func.sum(Venda.valor_total)).filter(Venda.created_at >= inicio_mes_passado, Venda.created_at <= fim_mes_passado).scalar() or 0
    vendas_percent = 0
    if vendas_mes_passado > 0:
        vendas_percent = int(((vendas_mes - vendas_mes_passado) / vendas_mes_passado) * 100)

    # Chamados recentes (últimos 5)
    chamados = Chamado.query.order_by(Chamado.created_at.desc()).limit(5).all()

    return render_template('dashboard.html',
        total_chamados=total_chamados,
        chamados_percent=chamados_percent,
        chamados_concluidos=chamados_concluidos,
        concluidos_percent=concluidos_percent,
        tempo_medio=tempo_medio,
        tempo_medio_percent=tempo_medio_percent,
        vendas_mes=vendas_mes,
        vendas_percent=vendas_percent,
        chamados=chamados
    )

# Rotas de Chamados
@app.route('/chamados', methods=['GET', 'POST'])
@login_required
def chamados():
    if request.method == 'POST':
        chamado = Chamado(
            titulo=request.form['titulo'],
            descricao=request.form['descricao'],
            cliente_id=request.form['cliente_id'],
            equipamento_id=request.form['equipamento_id'],
            tecnico_id=current_user.id if current_user.role == 'tecnico' else None
        )
        db.session.add(chamado)
        db.session.commit()
        return redirect(url_for('chamado', id=chamado.id))
    
    clientes = Cliente.query.all()
    equipamentos = Equipamento.query.all()
    return render_template('chamados.html', clientes=clientes, equipamentos=equipamentos)

@app.route('/chamado/<int:id>', methods=['GET', 'POST'])
@login_required
def chamado(id):
    chamado = Chamado.query.get_or_404(id)
    if request.method == 'POST':
        if 'foto' in request.files:
            file = request.files['foto']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # Adicionar foto ao chamado
        return redirect(url_for('chamado', id=id))
    return render_template('chamado.html', chamado=chamado)

# Rotas de Vendas
@app.route('/vendas', methods=['GET', 'POST'])
@login_required
def vendas():
    if current_user.role not in ['tecnico', 'suporte']:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Processamento do cliente
        cliente_id = None
        if request.form.get('cliente_cadastrado') == 'on':
            cliente_id = request.form['cliente_id']
        else:
            # Cliente novo
            nome = request.form['novo_cliente_nome']
            telefone = request.form['novo_cliente_telefone']
            
            if request.form.get('salvar_cliente') == 'on':
                # Salvar o novo cliente no banco
                novo_cliente = Cliente(
                    nome=nome,
                    telefone=telefone
                )
                db.session.add(novo_cliente)
                db.session.commit()
                cliente_id = novo_cliente.id
            else:
                # Criar um cliente temporário apenas para esta venda
                novo_cliente = Cliente(
                    nome=nome,
                    telefone=telefone,
                    temporario=True  # Você precisará adicionar este campo ao modelo Cliente
                )
                db.session.add(novo_cliente)
                db.session.commit()
                cliente_id = novo_cliente.id

        # Processamento da venda
        if 'foto_recibo' in request.files:
            file = request.files['foto_recibo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                foto_recibo = filename
            else:
                foto_recibo = None
        else:
            foto_recibo = None

        venda = Venda(
            cliente_id=cliente_id,
            tecnico_id=current_user.id,
            valor_total=request.form['valor_total'],
            forma_pagamento=request.form['forma_pagamento'],
            foto_recibo=foto_recibo
        )
        
        # Processar produtos da venda
        produtos_ids = request.form.getlist('produto_id[]')
        quantidades = request.form.getlist('quantidade[]')
        
        for produto_id, quantidade in zip(produtos_ids, quantidades):
            if produto_id and quantidade:
                # Aqui você deve implementar a lógica para adicionar os produtos à venda
                # e atualizar o estoque
                pass

        db.session.add(venda)
        db.session.commit()
        flash('Venda realizada com sucesso!')
        return redirect(url_for('vendas'))
    
    clientes = Cliente.query.filter_by(temporario=False).all()  # Não mostrar clientes temporários
    produtos = Produto.query.all()
    vendas = Venda.query.order_by(Venda.created_at.desc()).all()
    return render_template('vendas.html', clientes=clientes, produtos=produtos, vendas=vendas)

# Rotas de Clientes
@app.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    if request.method == 'POST':
        cliente = Cliente(
            nome=request.form['nome'],
            email=request.form['email'],
            telefone=request.form['telefone'],
            endereco=request.form['endereco']
        )
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('clientes'))
    
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

# Rotas de Equipamentos
@app.route('/equipamentos', methods=['GET', 'POST'])
@login_required
def equipamentos():
    if current_user.role not in ['tecnico', 'suporte', 'estoque']:
        return redirect(url_for('dashboard'))
    mensagem = None
    ultimo_equip = Equipamento.query.order_by(Equipamento.id.desc()).first()
    proximo_codigo = f'OS {ultimo_equip.id + 1:02d}' if ultimo_equip else 'OS 01'
    if request.method == 'POST':
        data_recebimento = request.form['data_recebimento']
        municipio = request.form['municipio']
        tipo_cliente = request.form['tipo_cliente']
        if tipo_cliente == 'existente':
            cliente_id = request.form['cliente_id']
        else:
            novo_nome = request.form['novo_cliente_nome']
            novo_telefone = request.form['novo_cliente_telefone']
            novo_email = request.form['novo_cliente_email']
            novo_endereco = request.form['novo_cliente_endereco']
            novo_cliente = Cliente(nome=novo_nome, email=novo_email, telefone=novo_telefone, endereco=novo_endereco)
            db.session.add(novo_cliente)
            db.session.commit()
            cliente_id = novo_cliente.id
        marca = request.form['marca']
        modelo = request.form['modelo']
        numero_serie = request.form['numero_serie']
        codigo_equipamento = request.form['codigo_equipamento']
        equipamento = Equipamento(
            marca=marca,
            modelo=modelo,
            numero_serie=numero_serie,
            cliente_id=cliente_id,
            created_at=data_recebimento,
            municipio=municipio,
            codigo=codigo_equipamento
        )
        db.session.add(equipamento)
        db.session.commit()
        mensagem = 'Equipamento cadastrado com sucesso!'
    # Lógica de busca
    q = request.args.get('q', '').strip()
    if q:
        equipamentos = Equipamento.query.filter((Equipamento.codigo.ilike(f'%{q}%')) | (Equipamento.numero_serie.ilike(f'%{q}%'))).all()
    else:
        equipamentos = Equipamento.query.all()
    clientes = Cliente.query.all()
    return render_template('equipamentos.html', equipamentos=equipamentos, clientes=clientes, proximo_codigo=proximo_codigo, mensagem=mensagem)

# Rotas de Produtos
@app.route('/produtos', methods=['GET', 'POST'])
@login_required
def produtos():
    if current_user.role not in ['estoque', 'suporte', 'tecnico']:
        return redirect(url_for('dashboard'))
    mensagem = None
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        tipo_movimentacao = request.form['tipo_movimentacao']
        quantidade_movimentacao = int(request.form['quantidade_movimentacao'])
        responsavel = current_user.name
        # Verifica se o produto já existe
        produto = Produto.query.filter_by(nome=nome).first()
        if not produto:
            produto = Produto(nome=nome, descricao=descricao, preco=preco, quantidade_estoque=0)
            db.session.add(produto)
            db.session.commit()
        # Atualiza o estoque
        if tipo_movimentacao == 'entrada':
            produto.quantidade_estoque += quantidade_movimentacao
        elif tipo_movimentacao == 'saida':
            if produto.quantidade_estoque >= quantidade_movimentacao:
                produto.quantidade_estoque -= quantidade_movimentacao
            else:
                mensagem = 'Estoque insuficiente para saída.'
                produtos = Produto.query.all()
                return render_template('produtos.html', produtos=produtos, mensagem=mensagem)
        db.session.commit()
        # Registra a movimentação
        movimentacao = MovimentacaoEstoque(
            produto_id=produto.id,
            tipo=tipo_movimentacao,
            quantidade=quantidade_movimentacao,
            responsavel=responsavel
        )
        db.session.add(movimentacao)
        db.session.commit()
        mensagem = 'Movimentação registrada com sucesso!'
    # Lógica de busca
    q = request.args.get('q', '').strip()
    if q:
        produtos = Produto.query.filter(Produto.nome.ilike(f'%{q}%')).all()
    else:
        produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos, mensagem=mensagem)

# Cadastro de Usuários
@app.route('/usuarios/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_usuario():
    if current_user.role != 'suporte':
        flash('Acesso não autorizado')
        return redirect(url_for('dashboard'))
    
    mensagem = None
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        role = request.form['role']
        
        if User.query.filter_by(username=username).first():
            mensagem = 'Usuário já existe!'
        else:
            user = User(username=username, name=name, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Usuário cadastrado com sucesso!')
            return redirect(url_for('usuarios'))
    
    return render_template('cadastrar_usuario.html', mensagem=mensagem)

@app.route('/usuarios', methods=['GET'])
@login_required
def usuarios():
    if current_user.role != 'suporte':
        flash('Acesso não autorizado')
        return redirect(url_for('dashboard'))
    
    usuarios = User.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    if current_user.role != 'suporte':
        flash('Acesso não autorizado')
        return redirect(url_for('dashboard'))
    
    usuario = User.query.get_or_404(id)
    if request.method == 'POST':
        usuario.username = request.form['username']
        usuario.name = request.form['name']
        usuario.role = request.form['role']
        if request.form['password']:
            usuario.set_password(request.form['password'])
        db.session.commit()
        flash('Usuário atualizado com sucesso!')
        return redirect(url_for('usuarios'))
    
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/usuarios/remover/<int:id>', methods=['POST'])
@login_required
def remover_usuario(id):
    if current_user.role != 'suporte':
        flash('Acesso não autorizado')
        return redirect(url_for('dashboard'))
    
    if current_user.id == id:
        flash('Você não pode remover seu próprio usuário')
        return redirect(url_for('usuarios'))
    
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário removido com sucesso!')
    return redirect(url_for('usuarios')) 