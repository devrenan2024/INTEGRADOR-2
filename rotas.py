from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import datetime
import bcrypt

# Configuração do Flask
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Chave secreta para sessão

# Configuração do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sua_senha'
app.config['MYSQL_DB'] = 'meu_blog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Retorna resultados como dicionários

mysql = MySQL(app)

# Rota principal - Index
@app.route('/')
def index():
    return render_template('index.html')

# Rota Sobre Mim
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Rota Meus Projetos
@app.route('/projetos')
def projetos():
    return render_template('projetos.html')

# Rota Contato
@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        # Captura dos dados do formulário de contato
        nome = request.form['name']
        email = request.form['email']
        mensagem = request.form['message']
        
        # Aqui você poderia salvar esses dados no banco de dados, se necessário
        
        return redirect(url_for('contato'))  # Redireciona para evitar reenvio do formulário
    
    return render_template('contato.html')

# Rota Blog
@app.route('/blog')
def blog():
    # Aqui você poderia buscar os posts do banco de dados e passá-los para a página
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM post ORDER BY created_at DESC')
    posts = cursor.fetchall()
    cursor.close()
    
    return render_template('blog.html', posts=posts)

# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Captura dos dados do formulário de login
        username = request.form['username']
        password = request.form['password']

        # Conexão com o banco de dados para autenticação
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Login bem-sucedido, armazena o usuário na sessão
            session['username'] = user['username']
            return redirect(url_for('admin'))
        else:
            # Login falhou
            return render_template('login.html', error='Usuário ou senha inválidos')

    return render_template('login.html')

# Rota de Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Rota de Administração
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Captura dos dados do formulário de adicionar post
        title = request.form['title']
        content = request.form['content']
        created_at = datetime.now()

        # Inserção do post no banco de dados
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO post (title, content, created_at) VALUES (%s, %s, %s)',
                       (title, content, created_at))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('admin'))

    # Busca todos os posts do banco de dados
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM post ORDER BY created_at DESC')
    posts = cursor.fetchall()
    cursor.close()

    return render_template('admin.html', posts=posts)

# Execução do aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)
