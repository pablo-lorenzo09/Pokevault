from database.conexao import conectar

def enviar_comentario_unitario(comentario, id_pokemon, nome_usuario, nota):
    conexao, cursor = conectar()
    try:
        sql = """
            INSERT INTO comentario_unitario(comentario, id_pokemon, nome_usuario, nota) 
            VALUES(%s, %s, %s, %s)
        """
        cursor.execute(sql, (comentario, id_pokemon, nome_usuario, nota))
        conexao.commit()
    except Exception as e:
        print(f"Erro ao Inserir Comentário: {e}")
    finally:
        cursor.close()
        conexao.close()

def obter_comentarios_unitario(id_pokemon):
    conexao, cursor = conectar()
    sql = """
        SELECT cod_comentario, nome_usuario, comentario, nota 
        FROM comentario_unitario 
        WHERE id_pokemon = %s
        ORDER BY cod_comentario DESC
    """
    cursor.execute(sql, (id_pokemon,))
    comentarios = cursor.fetchall()
    cursor.close()
    conexao.close()
    return comentarios


def deletar_comentario_unitario(id):
    conexao, cursor = conectar()
    sql = "DELETE FROM comentario_unitario WHERE cod_comentario = %s"
    cursor.execute(sql, (id,))
    conexao.commit()
    cursor.close()
    conexao.close()