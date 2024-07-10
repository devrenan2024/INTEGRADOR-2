from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

posts = []
projetos = []

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para adicionar um novo post
@app.route('/adicionar_post', methods=['POST'])
def adicionar_post():
    title = request.form['title']
    content = request.form['content']
    image_url = request.form.get('image_url')
    video_url = request.form.get('video_url')

    novo_post = {
        'id': len(posts) + 1,
        'title': title,
        'content': content,
        'image_url': image_url,
        'video_url': video_url,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    posts.append(novo_post)

    return redirect(url_for('admin'))  # Redireciona para a página de administração após adicionar post

# Rota para adicionar um novo projeto
@app.route('/adicionar_projeto', methods=['POST'])
def adicionar_projeto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    imagem_url = request.form.get('imagem_url')
    video_url = request.form.get('video_url')

    novo_projeto = {
        'nome': nome,
        'descricao': descricao,
        'imagem_url': imagem_url,
        'video_url': video_url,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    projetos.append(novo_projeto)

    return redirect(url_for('admin'))  # Redireciona para a página de administração após adicionar projeto

# Rota para a página 'Sobre'
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Rota para a página 'Projetos'
@app.route('/projetos')
def projetos_page():
    return render_template('projetos.html', projetos=projetos)

# Rota para a página 'Blog'
@app.route('/blog')
def blog():
    return render_template('blog.html', posts=posts)

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', message="Credenciais inválidas. Tente novamente.")

    return render_template('login.html')

# Rota para a página de administração
@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('admin.html', posts=posts, projetos=projetos)

# Rota para editar um post específico
@app.route('/edit/<int:post_id>')
def edit(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return "Post não encontrado", 404

    return render_template('edit.html', post=post)

# Rota para excluir um post específico
@app.route('/delete/<int:post_id>')
def delete(post_id):
    global posts
    posts = [p for p in posts if p['id'] != post_id]
    return redirect(url_for('admin'))  # Redireciona para a página de administração após excluir o post

# Rota para a página de contato
@app.route('/contato')
def contato():
    return render_template('contato.html')

# Rota para o envio de contato
@app.route('/enviar_contato', methods=['POST'])
def enviar_contato():
    nome = request.form['name']
    email = request.form['email']
    mensagem = request.form['message']
    
    print(f"Nome: {nome}, Email: {email}, Mensagem: {mensagem}")

    return "Formulário enviado com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)
