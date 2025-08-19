from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "chave_secreta"

# Configuração do banco (SQLite simples)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ================================
# MODELOS
# ================================
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

class Anuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Pergunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(200), nullable=False)
    anuncio_id = db.Column(db.Integer, db.ForeignKey('anuncio.id'))

class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    anuncio_id = db.Column(db.Integer, db.ForeignKey('anuncio.id'))

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    anuncio_id = db.Column(db.Integer, db.ForeignKey('anuncio.id'))

# ================================
# HOME
# ================================
@app.route('/')
def index():
    return render_template('index.html')

# ================================
# CRUD USUÁRIOS
# ================================
@app.route('/usuarios')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/lista.html', usuarios=usuarios)

@app.route('/usuarios/criar', methods=['GET','POST'])
def criar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        novo = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo)
        db.session.commit()
        flash("Usuário criado com sucesso!")
        return redirect(url_for('listar_usuarios'))
    return render_template('usuarios/form.html')

@app.route('/usuarios/editar/<int:id>', methods=['GET','POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.senha = request.form['senha']
        db.session.commit()
        flash("Usuário atualizado!")
        return redirect(url_for('listar_usuarios'))
    return render_template('usuarios/form.html', usuario=usuario)

@app.route('/usuarios/deletar/<int:id>', methods=['POST'])
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuário deletado com sucesso!")
    return redirect(url_for('listar_usuarios'))

# ================================
# CRUD ANÚNCIOS
# ================================
@app.route('/anuncios')
def listar_anuncios():
    anuncios = Anuncio.query.all()
    return render_template('anuncios/lista.html', anuncios=anuncios)

@app.route('/anuncios/criar', methods=['GET','POST'])
def criar_anuncio():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        preco = float(request.form['preco'])
        anuncio = Anuncio(titulo=titulo, descricao=descricao, preco=preco)
        db.session.add(anuncio)
        db.session.commit()
        flash("Anúncio criado!")
        return redirect(url_for('listar_anuncios'))
    return render_template('anuncios/form.html')

@app.route('/anuncios/editar/<int:id>', methods=['GET','POST'])
def editar_anuncio(id):
    anuncio = Anuncio.query.get_or_404(id)
    if request.method == 'POST':
        anuncio.titulo = request.form['titulo']
        anuncio.descricao = request.form['descricao']
        anuncio.preco = float(request.form['preco'])
        db.session.commit()
        flash("Anúncio atualizado!")
        return redirect(url_for('listar_anuncios'))
    return render_template('anuncios/form.html', anuncio=anuncio)

@app.route('/anuncios/deletar/<int:id>', methods=['POST'])
def deletar_anuncio(id):
    anuncio = Anuncio.query.get_or_404(id)
    db.session.delete(anuncio)
    db.session.commit()
    flash("Anúncio excluído!")
    return redirect(url_for('listar_anuncios'))

# ================================
# CRUD PERGUNTAS
# ================================
@app.route('/perguntas')
def listar_perguntas():
    perguntas = Pergunta.query.all()
    return render_template('perguntas/lista.html', perguntas=perguntas)

@app.route('/perguntas/criar', methods=['GET','POST'])
def criar_pergunta():
    if request.method == 'POST':
        texto = request.form['texto']
        anuncio_id = int(request.form['anuncio_id'])
        pergunta = Pergunta(texto=texto, anuncio_id=anuncio_id)
        db.session.add(pergunta)
        db.session.commit()
        flash("Pergunta criada!")
        return redirect(url_for('listar_perguntas'))
    return render_template('perguntas/form.html')

@app.route('/perguntas/editar/<int:id>', methods=['GET','POST'])
def editar_pergunta(id):
    pergunta = Pergunta.query.get_or_404(id)
    if request.method == 'POST':
        pergunta.texto = request.form['texto']
        pergunta.anuncio_id = int(request.form['anuncio_id'])
        db.session.commit()
        flash("Pergunta atualizada!")
        return redirect(url_for('listar_perguntas'))
    return render_template('perguntas/form.html', pergunta=pergunta)

@app.route('/perguntas/deletar/<int:id>', methods=['POST'])
def deletar_pergunta(id):
    pergunta = Pergunta.query.get_or_404(id)
    db.session.delete(pergunta)
    db.session.commit()
    flash("Pergunta excluída!")
    return redirect(url_for('listar_perguntas'))

# ================================
# CRUD FAVORITOS
# ================================
@app.route('/favoritos')
def listar_favoritos():
    favoritos = Favorito.query.all()
    return render_template('favoritos/lista.html', favoritos=favoritos)

@app.route('/favoritos/criar', methods=['GET','POST'])
def criar_favorito():
    if request.method == 'POST':
        usuario_id = int(request.form['usuario_id'])
        anuncio_id = int(request.form['anuncio_id'])
        favorito = Favorito(usuario_id=usuario_id, anuncio_id=anuncio_id)
        db.session.add(favorito)
        db.session.commit()
        flash("Favorito adicionado!")
        return redirect(url_for('listar_favoritos'))
    return render_template('favoritos/form.html')

@app.route('/favoritos/deletar/<int:id>', methods=['POST'])
def deletar_favorito(id):
    favorito = Favorito.query.get_or_404(id)
    db.session.delete(favorito)
    db.session.commit()
    flash("Favorito removido!")
    return redirect(url_for('listar_favoritos'))

# ================================
# CRUD COMPRAS
# ================================
@app.route('/compras')
def listar_compras():
    compras = Compra.query.all()
    return render_template('compras/lista.html', compras=compras)

@app.route('/compras/criar', methods=['GET','POST'])
def criar_compra():
    if request.method == 'POST':
        usuario_id = int(request.form['usuario_id'])
        anuncio_id = int(request.form['anuncio_id'])
        compra = Compra(usuario_id=usuario_id, anuncio_id=anuncio_id)
        db.session.add(compra)
        db.session.commit()
        flash("Compra registrada!")
        return redirect(url_for('listar_compras'))
    return render_template('compras/form.html')

@app.route('/compras/deletar/<int:id>', methods=['POST'])
def deletar_compra(id):
    compra = Compra.query.get_or_404(id)
    db.session.delete(compra)
    db.session.commit()
    flash("Compra removida!")
    return redirect(url_for('listar_compras'))

# ================================
# Inicialização
# ================================
@app.before_first_request
def criar_tabelas():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
