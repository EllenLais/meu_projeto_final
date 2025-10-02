from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id_usuarios = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo_usuario = db.Column(db.String(50))

    emprestimos = db.relationship("Emprestimo", backref="usuario", lazy=True)
    avaliacoes = db.relationship("Avaliacao", backref="usuario", lazy=True)


class Livro(db.Model):
    __tablename__ = "livro"

    id_livro = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    ano_publicacao = db.Column(db.Integer)

    emprestimos = db.relationship("Emprestimo", backref="livro", lazy=True)
    avaliacoes = db.relationship("Avaliacao", backref="livro", lazy=True)


class Emprestimo(db.Model):
    __tablename__ = "emprestimo"

    id_emprestimo = db.Column(db.Integer, primary_key=True)
    data_emprestimo = db.Column(db.Date, nullable=False)
    data_devolucao = db.Column(db.Date)
    status = db.Column(db.String(100))

    usuarios_id_usuarios = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuarios"), nullable=False)
    livro_id_livro = db.Column(db.Integer, db.ForeignKey("livro.id_livro"), nullable=False)


class Avaliacao(db.Model):
    __tablename__ = "avaliacao"

    id_avaliacao = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    data_avaliacao = db.Column(db.Date)

    usuarios_id_usuarios = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuarios"), nullable=False)
    livro_id_livro = db.Column(db.Integer, db.ForeignKey("livro.id_livro"), nullable=False)



with app.app_context():
    db.create_all()
    print("Banco de dados criado com sucesso!")
