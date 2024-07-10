import mysql.connector
from mysql.connector import Error, errorcode

def conectar_mysql():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='130388',
            database='meu_blog'  # Nome do seu banco de dados
        )

        if conn.is_connected():
            print('Conexão estabelecida com sucesso.')
        else:
            print('Problemas ao conectar.')

    except Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Erro de autenticação: Usuário ou senha inválidos.')
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print('Erro de banco de dados: Banco de dados não existe.')
        else:
            print(e)

    return conn

def fechar_conexao(conn):
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print('Conexão fechada.')

# Exemplo de uso:
# conn = conectar_mysql()
# if conn:
#     # Realize suas operações com o banco de dados aqui
#     # Não se esqueça de fechar a conexão quando terminar
#     fechar_conexao(conn)
# else:
#     print('Não foi possível conectar ao MySQL.')

