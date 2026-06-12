from database.conexao import conectar

def recuperar_tipos():
    conexao,cursor = conectar()

    cursor.execute("""SELECT id_tipo,tipo FROM pokevault.tipos;""")

    pokemons=cursor.fetchall()

    conexao.close()

    return pokemons