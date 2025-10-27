from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date
from models import db, Usuario, Livro, Emprestimo, Avaliacao

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "chave_secreta"

db.init_app(app)


@app.route("/")
def index():
    livros = Livro.query.all()
    return render_template("index.html", livros=livros)


@app.route("/livros")
def livros():
    livros = Livro.query.all()
    return render_template("livros.html", livros=livros)


@app.route("/livros/add", methods=["GET", "POST"])
def add_livro():
    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        ano = request.form["ano"]

        if not titulo or not autor:
            flash("Título e autor são obrigatórios!")
        else:
            novo_livro = Livro(titulo=titulo, autor=autor, ano_publicacao=ano)
            db.session.add(novo_livro)
            db.session.commit()
            flash("Livro adicionado com sucesso!")
            return redirect(url_for("livros"))

    return render_template("add_livro.html")


@app.route("/livros/<int:id_livro>")
def livro_detalhes(id_livro):
    livro = Livro.query.get_or_404(id_livro)
    avaliacoes = Avaliacao.query.filter_by(livro_id_livro=id_livro).all()
    emprestimos = Emprestimo.query.filter_by(livro_id_livro=id_livro).all()
    return render_template("livro_detalhes.html", livro=livro, avaliacoes=avaliacoes, emprestimos=emprestimos)


@app.route("/livros/<int:id_livro>/avaliar", methods=["GET", "POST"])
def avaliar_livro(id_livro):
    livro = Livro.query.get_or_404(id_livro)

    if request.method == "POST":
        usuario_id = 1  # exemplo (poderia vir do login)
        nota = int(request.form["nota"])
        comentario = request.form["comentario"]

        avaliacao = Avaliacao(
            nota=nota,
            comentario=comentario,
            data_avaliacao=date.today(),
            usuarios_id_usuarios=usuario_id,
            livro_id_livro=livro.id_livro
        )

        db.session.add(avaliacao)
        db.session.commit()
        flash("Avaliação adicionada com sucesso!")
        return redirect(url_for("livro_detalhes", id_livro=id_livro))

    return render_template("avaliacao.html", livro=livro)


@app.route("/livros/<int:id_livro>/emprestimo", methods=["GET", "POST"])
def emprestar_livro(id_livro):
    livro = Livro.query.get_or_404(id_livro)

    if request.method == "POST":
        usuario_id = 1  # exemplo (poderia vir do login)
        emprestimo = Emprestimo(
            data_emprestimo=date.today(),
            status="Em andamento",
            usuarios_id_usuarios=usuario_id,
            livro_id_livro=livro.id_livro
        )

        db.session.add(emprestimo)
        db.session.commit()
        flash("Empréstimo registrado!")
        return redirect(url_for("livro_detalhes", id_livro=id_livro))

    return render_template("emprestimo.html", livro=livro)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
