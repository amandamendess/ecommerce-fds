from flask import Flask
from markupsafe import escape
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from flask import url_for
from flask import request
import pymysql 
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ecomerce:Margarida0#@localhost:3306/ecomerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column('usu_id', db.Integer, primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    telefone = db.Column('usu_telefone', db.Integer)
    cpf = db.Column('usu_cpf', db.Integer)
    senha = db.Column('usu_senha', db.String(256))
    email = db.Column('usu_email', db.String(256))

    def __init__(self, nome, telefone,cpf, senha, email):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.senha = senha
        self.email = email

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))

    def __init__ (self, nome):
        self.nome = nome

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

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cadastrar/usuario")
def usuario():
      return render_template('users.html', usuarios = Usuario.query.all(), titulo="Usuario")

@app.route("/usuario/criar", methods=['POST'])
def criarusuario():  
    usuario = Usuario(request.form.get('user'), request.form.get('telefone'), request.form.get('cpf'), request.form.get('senha'), request.form.get('email'))  
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>",  methods=['GET', 'POST'])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('user')
        usuario.telefone = request.form.get('telefone'), 
        usuario.cpf = request.form.get('cpf'), 
        usuario.senha = request.form.get('senha'), 
        usuario.email = request.form.get('email')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario'))
    
    return render_template('editar_usuario.html', usuario = usuario, titulo='Usuario')

@app.route("/usuario/deletar/<int:id>")
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

@app.route("/cadastrar/anuncio")
def cadastrar_anuncio():
    return render_template('anuncio.html')

@app.route('/anuncio/perguntas')
def pergunta():
    return render_template('pergunta.html')


@app.route("/relatorio/compra")
def compra():
    return ''

@app.route("/relatorio/venda")
def venda():
    return 'l'

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