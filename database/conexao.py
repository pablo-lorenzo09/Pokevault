import mysql.connector

def conectar():
    conexao=mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="PokeVault"
        )

    cursor=conexao.cursor(dictionary=True)

    return conexao, cursor

