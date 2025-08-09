from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home and navigation
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/perfil')
def perfil():
    # placeholder: in real app pass user data
    return render_template('perfil.html')

# Announcements (Anúncios)
@app.route('/anuncios')
def anuncios():
    return render_template('anuncios.html')

@app.route('/anuncio/<int:id_anuncio>')
def anuncio_detalhe(id_anuncio):
    # placeholder: fetch anuncio by id
    return render_template('anuncio_detalhe.html', id_anuncio=id_anuncio)

@app.route('/anuncio/criar', methods=['GET','POST'])
def anuncio_criar():
    if request.method == 'POST':
        # process creation logic
        return redirect(url_for('anuncios'))
    return render_template('anuncio_form.html')

# Perguntas e respostas
@app.route('/anuncio/<int:id_anuncio>/pergunta', methods=['POST'])
def preguntar(id_anuncio):
    # process question submission
    pergunta = request.form.get('pergunta')
    return redirect(url_for('anuncio_detalhe', id_anuncio=id_anuncio))

# Favoritos
@app.route('/favoritos')
def favoritos():
    return render_template('favoritos.html')

# Compras
@app.route('/comprar/<int:id_anuncio>', methods=['POST'])
def comprar(id_anuncio):
    # process purchase (no cart)
    return redirect(url_for('perfil'))

if __name__ == '__main__':
    app.run(debug=True)
