import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

# Função para conectar ao MySQL
def connect():
    try:
        conn = mysql.connector.connect(
            host=r56789;            user='root',     # Substitua pelo seu usuário MySQL
            password='130388'  # Substitua pela sua senha MySQL, se necessário
        )
        if conn.is_connected():
            print("Conexão estabelecida com sucesso.")
            return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Erro de autenticação: Usuário ou senha inválidos.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Erro de banco de dados: Banco de dados não existe.')
        else:
            print(err)
    return None

# Função para criar o banco de dados e tabelas
def create_database(conn):
    try:
        cursor = conn.cursor()

        # Criação do banco de dados 'meublog'
        cursor.execute("DROP DATABASE IF EXISTS `meublog`;")
        cursor.execute("CREATE DATABASE `meublog`;")
        cursor.execute("USE `meublog`;")

        # Definição das tabelas
        TABLES = {}
        TABLES['post'] = (
            "CREATE TABLE `post` ("
            "  `id` int(11) NOT NULL AUTO_INCREMENT,"
            "  `title` varchar(50) NOT NULL,"
            "  `content` text NOT NULL,"
            "  `created_at` datetime NOT NULL,"
            "  PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB"
        )

        TABLES['user'] = (
            "CREATE TABLE `user` ("
            "  `id` int(11) NOT NULL AUTO_INCREMENT,"
            "  `username` varchar(20) NOT NULL,"
            "  `password` varchar(60) NOT NULL,"  # Aumentado para acomodar hashes de senha
            "  `created_at` datetime NOT NULL,"
            "  PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB"
        )

        # Criação das tabelas
        for table_name, table_sql in TABLES.items():
            print(f'Criando tabela {table_name}: ', end='')
            cursor.execute(table_sql)
            print('OK')

        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(err)
        return False

# Função para inserir posts
def insert_posts(conn):
    try:
        cursor = conn.cursor()

        postSQL = 'INSERT INTO post (title, content, created_at) VALUES (%s, %s, %s)'
        posts = [
            ("Projetos", "Projetos relacionados ao curso", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        ]
        cursor.executemany(postSQL, posts)
        conn.commit()

        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(err)
        return False

# Função para inserir usuários
def insert_users(conn):
    try:
        cursor = conn.cursor()

        userSQL = 'INSERT INTO user (username, password, created_at) VALUES (%s, %s, %s)'
        users = [
            ('renan', '1303', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        ]
        cursor.executemany(userSQL, users)
        conn.commit()

        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(err)
        return False

# Função principal
def main():
    conn = connect()
    if conn:
        if create_database(conn):
            if insert_posts(conn):
                print("Inserção de posts realizada com sucesso.")
            if insert_users(conn):
                print("Inserção de usuários realizada com sucesso.")
        conn.close()
    else:
        print("Não foi possível estabelecer a conexão.")

if __name__ == "__main__":
    main()
