from flask import Flask
from markupsafe import escape
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from flask import url_for
from flask import request
from flask_login import (current_user, LoginManager,
                             login_user, logout_user,
                             login_required)
import hashlib
import pymysql 
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ecomerce:Margarida0#@localhost:3306/ecomerce'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://amandamendes:Margarida0#@amandamendes.mysql.pythonanywhere-services.com:3306/amandamendes$ecomerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key = 'chaveecomerce'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column('usu_id', db.Integer, primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    telefone = db.Column('usu_telefone', db.Integer)
    cpf = db.Column('usu_cpf', db.Integer)
    senha = db.Column('usu_senha', db.String(256))
    email = db.Column('usu_email', db.String(256))
    login = db.Column('usu_login', db.String(256))

    def __init__(self, nome, telefone,cpf, senha, email, login):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.senha = senha
        self.email = email
        self.login = login


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))

    def __init__ (self, nome):
        self.nome = nome

class Pergunta(db.Model):
    __table_name = "pergunta"
    id = db.Column('perg_id', db.Integer, primary_key=True)
    desc = db.Column('perg_desc', db.String(256))
    anu_id = db.Column('anu_id', db.Integer, db.ForeignKey('anuncio.anu_id'))

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('anu_id', db.Integer, primary_key=True)
    nome = db.Column('anu_nome', db.String(256))
    desc = db.Column('anu_desc', db.String(256))
    qtd = db.Column('anu_qtd', db.Integer)
    preco = db.Column('anu_preco', db.Float)
    cat_id = db.Column('cat_id',db.Integer, db.ForeignKey("categoria.cat_id"))
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, nome, desc, qtd, preco, cat_id, usu_id):
        self.nome = nome
        self.desc = desc
        self.qtd = qtd
        self.preco = preco
        self.cat_id = cat_id
        self.usu_id = usu_id

@app.errorhandler(404)
def paginanaoencontrada(error):  
    return render_template('pagina_nao_encontrada.html')

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        senha = hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest()

        user = Usuario.query.filter_by(login=login, senha=senha).first()

        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')
            
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/cadastrar/usuario")
# @login_required
def usuario():
      return render_template('users.html', usuarios = Usuario.query.all(), titulo="Usuario")

@app.route("/usuario/criar", methods=['POST'])
def criarusuario():  
    hash = hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest()
    usuario = Usuario(request.form.get('user'), request.form.get('telefone'), request.form.get('cpf'),hash , request.form.get('email'))  
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>",  methods=['GET', 'POST'])
@login_required
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('user')
        usuario.telefone = request.form.get('telefone'), 
        usuario.cpf = request.form.get('cpf'), 
        usuario.senha =  hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest(),
        usuario.email = request.form.get('email')
        usuario.login = request.form.get('login')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario'))
    
    return render_template('editar_usuario.html', usuario = usuario, titulo='Usuario')

@app.route("/usuario/deletar/<int:id>")
# @login_required
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/config/categoria")
def categoria():
    return render_template('categoria.html', categorias = Categoria.query.all(), titulo='Categoria')

@app.route("/categoria/novo", methods=['POST'])
def novacategoria():
    categoria = Categoria(request.form.get('nome'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/categoria/editar/<int:id>",  methods=['GET', 'POST'])
def categoriaeditar(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        categoria.nome = request.form.get('nome')
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('categoria'))
    
    return render_template('editar_categoria.html', categoria = categoria, titulo='Categoria')


@app.route("/cadastrar/anuncio")
def anuncio():
    return render_template('anuncio.html', anuncios = Anuncio.query.all())

@app.route("/anuncio/criar", methods=['POST'])
def cadastrar_anuncio(): 
    anuncio = Anuncio(request.form.get('nome'), request.form.get('desc'), request.form.get('qnt'), request.form.get('preco'), request.form.get('cat'), request.form.get('usu'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))

# @app.route("/anuncio/editar/<int:id>",  methods=['GET', 'POST'])
# def editaranuncio(id):
#     anuncio = Anuncio.query.get(id)
#     if request.method == 'POST':
#         anuncio.nome = request.form.get('nome')
#         anuncio.desc = request.form.get('desc')
#         anuncio.qnt = request.form.get('qnt')
#         anuncio.preco = request.form.get('preco')
#         db.session.add(anuncio)
#         db.session.commit()
#         return redirect(url_for('anuncio'))
    
#     return render_template('editar_anuncio.html', anuncio=anuncio)

@app.route('/anuncio/perguntas')
def pergunta():
    return render_template('pergunta.html')


@app.route("/compra")
def compra():
    return render_template('relat_compra.html')

@app.route("/relatorio/venda")
def venda():
    return render_template('relat_venda.html')

@app.route("/login")
def entrar():
    return 'l'

@app.route('/user/<username>')
def username(username):
    return f'{username}</h4>'

with app.app_context():
    if __name__ == 'ecomerce3':
        print('ecomerce3')
    db.create_all()
    #quando testar somente na web comentar a linha de baixo
    # app.run()