from flask import Flask
from models import db, Usuario, Livro, Emprestimo, Avaliacao  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "chave_secreta"  

db.init_app(app)


@app.route("/")
def index():
    return "Sistema de Biblioteca rodando!"


if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
