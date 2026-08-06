from flask import Flask, render_template, request, redirect, url_for # importação do recursos do Flask
from flask_sqlalchemy import SQLAlchemy # importação do flask_sqlalchemy


app = Flask(__name__) # instanciação da aplicação flask
app.config['SECRET_KEY'] = 'minhachaveultrasecretaqueninguemconhece' # configuração da chave secreta 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///milkshake.db'  # criação de contexto de banco de dados no sqlalchemy
db = SQLAlchemy(app)  # Instanciação do sqlalchemy no objeto de banco de dados

class Milkshake(db.Model): # db.Model Herança de métodos e atributos do objeto de banco
    uid = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80),unique=True, nullable=False)
    sabor = db.Column(db.String(80),unique=True, nullable=False)
    cobertura = db.Column(db.String(80))
    confeitos = db.Column(db.String(80))
    tamanho = db.Column(db.String(80), nullable=False)
    preco = db.Column(db.Float(precision=2))

with app.app_context():
    db.create_all()

# rota Padrão
@app.route('/')
def home():
    milkshakes = Milkshake.query.all()
    return render_template('index.html', milkshakes=milkshakes)

# rota de inserção
@app.route('/insert', methods=['GET', 'POST'])
def insert_milk():
    if request.method == 'GET':
        return render_template('insert.html')
    else:
        nome = request.form['nome']
        sabor = request.form['sabor']
        cobertura = request.form['cobertura']
        confeitos = request.form['confeitos']
        tamanho = request.form['tamanho']
        preco = float(request.form['preco'])
        milkshake = Milkshake(
            nome=nome,
            sabor=sabor,
            cobertura=cobertura,
            confeitos=confeitos,
            tamanho=tamanho,
            preco=preco
        )
        db.session.add(milkshake)
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/edit/<int:uid>', methods=['GET', 'POST'])
def edit_milk(uid):
    milkshake = Milkshake.query.get_or_404(uid)
    if request.method == 'GET':
        return render_template('edit.html', milkshake=milkshake)
    else:
        milkshake.nome = request.form['nome']
        milkshake.sabor = request.form['sabor']
        milkshake.cobertura = request.form['cobertura']
        milkshake.confeitos = request.form['confeitos']
        milkshake.tamanho = request.form['tamanho']
        milkshake.preco = float(request.form['preco'])
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/delete/<int:uid>', methods=['POST'])
def delete_leite(uid):
    milkshake = Milkshake.query.get_or_404(uid)
    db.session.delete(milkshake)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

