from database.conexao import conectar

def recuperar_pokemons(pag: int = 0, tipos: list = None):
    conexao,cursor = conectar()
    offset= 30 * int(pag)
    if offset > 0:
        offset= 30 * (int(pag)-1)

    base_query = """SELECT
        p.id_pokemon AS id,
        p.nome AS name,

        MAX(CASE WHEN pt.rn_tipo = 1 THEN t.tipo END) AS type1,
        MAX(CASE WHEN pt.rn_tipo = 2 THEN t.tipo END) AS type2,

        p.descricao AS description,

        MAX(CASE WHEN ap.rn_ataque = 1 THEN a.nome END) AS attack1,
        MAX(CASE WHEN ap.rn_ataque = 1 THEN a.tipo END) AS attack1_type,

        MAX(CASE WHEN ap.rn_ataque = 2 THEN a.nome END) AS attack2,
        MAX(CASE WHEN ap.rn_ataque = 2 THEN a.tipo END) AS attack2_type,

        MAX(CASE WHEN ap.rn_ataque = 3 THEN a.nome END) AS attack3,
        MAX(CASE WHEN ap.rn_ataque = 3 THEN a.tipo END) AS attack3_type,

        MAX(CASE WHEN ap.rn_ataque = 4 THEN a.nome END) AS attack4,
        MAX(CASE WHEN ap.rn_ataque = 4 THEN a.tipo END) AS attack4_type,

        p.imagem AS image,
        p.preco AS price

    FROM Pokemons p

    LEFT JOIN (
        SELECT
            pt.id_pokemon,
            pt.id_tipo,
            ROW_NUMBER() OVER (
                PARTITION BY pt.id_pokemon
                ORDER BY pt.id_tipo
            ) AS rn_tipo
        FROM Pokemons_tipos pt
    ) pt
    ON p.id_pokemon = pt.id_pokemon

    LEFT JOIN tipos t
    ON pt.id_tipo = t.id_tipo

    LEFT JOIN (
        SELECT
            ap.id_pokemon,
            ap.id_ataque,
            ROW_NUMBER() OVER (
                PARTITION BY ap.id_pokemon
                ORDER BY ap.id_ataque
            ) AS rn_ataque
        FROM ataques_pokemons ap
    ) ap
    ON p.id_pokemon = ap.id_pokemon

    LEFT JOIN Ataques a
    ON ap.id_ataque = a.id_ataque
    """

    params = []

    # Filtro opcional por tipos de pokemon (agora aceita lista)
    if tipos:
        placeholders = ','.join(['%s'] * len(tipos))
        base_query += f"""
    WHERE p.id_pokemon IN (
        SELECT pt2.id_pokemon
        FROM Pokemons_tipos pt2
        JOIN tipos t2 ON pt2.id_tipo = t2.id_tipo
        WHERE t2.tipo IN ({placeholders})
    )
        """
        params.extend(tipos)

    base_query += """
    GROUP BY
        p.id_pokemon,
        p.nome,
        p.descricao,
        p.imagem,
        p.preco

    ORDER BY
        p.id_pokemon
    LIMIT 30 OFFSET %s;
    """

    params.append(offset)

    cursor.execute(base_query, params)

    pokemons=cursor.fetchall()

    conexao.close()

    return pokemons

def recuperar_pokemon_unitario(id):
    conexao,cursor = conectar()
    cursor.execute("""SELECT
        p.id_pokemon AS id,
        p.nome AS name,

        MAX(CASE WHEN pt.rn_tipo = 1 THEN t.tipo END) AS type1,
        MAX(CASE WHEN pt.rn_tipo = 2 THEN t.tipo END) AS type2,

        p.descricao AS description,

        MAX(CASE WHEN ap.rn_ataque = 1 THEN a.nome END) AS attack1,
        MAX(CASE WHEN ap.rn_ataque = 1 THEN a.tipo END) AS attack1_type,

        MAX(CASE WHEN ap.rn_ataque = 2 THEN a.nome END) AS attack2,
        MAX(CASE WHEN ap.rn_ataque = 2 THEN a.tipo END) AS attack2_type,

        MAX(CASE WHEN ap.rn_ataque = 3 THEN a.nome END) AS attack3,
        MAX(CASE WHEN ap.rn_ataque = 3 THEN a.tipo END) AS attack3_type,

        MAX(CASE WHEN ap.rn_ataque = 4 THEN a.nome END) AS attack4,
        MAX(CASE WHEN ap.rn_ataque = 4 THEN a.tipo END) AS attack4_type,

        p.imagem AS image,
        p.preco AS price

    FROM Pokemons p

    LEFT JOIN (
        SELECT
            pt.id_pokemon,
            pt.id_tipo,
            ROW_NUMBER() OVER (
                PARTITION BY pt.id_pokemon
                ORDER BY pt.id_tipo
            ) AS rn_tipo
        FROM Pokemons_tipos pt
    ) pt
    ON p.id_pokemon = pt.id_pokemon

    LEFT JOIN tipos t
    ON pt.id_tipo = t.id_tipo

    LEFT JOIN (
        SELECT
            ap.id_pokemon,
            ap.id_ataque,
            ROW_NUMBER() OVER (
                PARTITION BY ap.id_pokemon
                ORDER BY ap.id_ataque
            ) AS rn_ataque
        FROM ataques_pokemons ap
    ) ap
    ON p.id_pokemon = ap.id_pokemon

    LEFT JOIN Ataques a
    ON ap.id_ataque = a.id_ataque

    WHERE ap.id_pokemon = %s

    GROUP BY
        p.id_pokemon,
        p.nome,
        p.descricao,
        p.imagem,
        p.preco

    ORDER BY
        p.id_pokemon;""",[id])


    pokemons=cursor.fetchone()

    conexao.close()

    return pokemons


def recuperar_pokemons_destaques():
    conexao,cursor = conectar()
    cursor.execute("""SELECT
        p.id_pokemon AS id,
        p.nome AS name,

        MAX(CASE WHEN pt.rn_tipo = 1 THEN t.tipo END) AS type1,
        MAX(CASE WHEN pt.rn_tipo = 2 THEN t.tipo END) AS type2,

        p.descricao AS description,

        MAX(CASE WHEN ap.rn_ataque = 1 THEN a.nome END) AS attack1,
        MAX(CASE WHEN ap.rn_ataque = 1 THEN a.tipo END) AS attack1_type,

        MAX(CASE WHEN ap.rn_ataque = 2 THEN a.nome END) AS attack2,
        MAX(CASE WHEN ap.rn_ataque = 2 THEN a.tipo END) AS attack2_type,

        MAX(CASE WHEN ap.rn_ataque = 3 THEN a.nome END) AS attack3,
        MAX(CASE WHEN ap.rn_ataque = 3 THEN a.tipo END) AS attack3_type,

        MAX(CASE WHEN ap.rn_ataque = 4 THEN a.nome END) AS attack4,
        MAX(CASE WHEN ap.rn_ataque = 4 THEN a.tipo END) AS attack4_type,

        p.imagem AS image,
        p.preco AS price

    FROM Pokemons p

    LEFT JOIN (
        SELECT
            pt.id_pokemon,
            pt.id_tipo,
            ROW_NUMBER() OVER (
                PARTITION BY pt.id_pokemon
                ORDER BY pt.id_tipo
            ) AS rn_tipo
        FROM Pokemons_tipos pt
    ) pt
    ON p.id_pokemon = pt.id_pokemon

    LEFT JOIN tipos t
    ON pt.id_tipo = t.id_tipo

    LEFT JOIN (
        SELECT
            ap.id_pokemon,
            ap.id_ataque,
            ROW_NUMBER() OVER (
                PARTITION BY ap.id_pokemon
                ORDER BY ap.id_ataque
            ) AS rn_ataque
        FROM ataques_pokemons ap
    ) ap
    ON p.id_pokemon = ap.id_pokemon

    LEFT JOIN Ataques a
    ON ap.id_ataque = a.id_ataque

    WHERE p.destaque = 1

    GROUP BY
        p.id_pokemon,
        p.nome,
        p.descricao,
        p.imagem,
        p.preco

    ORDER BY
        p.id_pokemon;""")


    pokemons=cursor.fetchall()

    conexao.close()

    return pokemons


def recuperar_tipos():
    conexao, cursor = conectar()
    cursor.execute("SELECT id_tipo, tipo FROM tipos ORDER BY tipo;")
    tipos = cursor.fetchall()
    conexao.close()
    return tipos

def recuperar_pokemons_preco_min(pag: int = 0, tipos: list = None):
    conexao,cursor = conectar()
    offset= 30 * int(pag)
    if offset > 0:
        offset= 30 * (int(pag)-1)

    base_query = """SELECT
        p.id_pokemon AS id,
        p.nome AS name,

        MAX(CASE WHEN pt.rn_tipo = 1 THEN t.tipo END) AS type1,
        MAX(CASE WHEN pt.rn_tipo = 2 THEN t.tipo END) AS type2,

        p.descricao AS description,

        MAX(CASE WHEN ap.rn_ataque = 1 THEN a.nome END) AS attack1,
        MAX(CASE WHEN ap.rn_ataque = 1 THEN a.tipo END) AS attack1_type,

        MAX(CASE WHEN ap.rn_ataque = 2 THEN a.nome END) AS attack2,
        MAX(CASE WHEN ap.rn_ataque = 2 THEN a.tipo END) AS attack2_type,

        MAX(CASE WHEN ap.rn_ataque = 3 THEN a.nome END) AS attack3,
        MAX(CASE WHEN ap.rn_ataque = 3 THEN a.tipo END) AS attack3_type,

        MAX(CASE WHEN ap.rn_ataque = 4 THEN a.nome END) AS attack4,
        MAX(CASE WHEN ap.rn_ataque = 4 THEN a.tipo END) AS attack4_type,

        p.imagem AS image,
        p.preco AS price

    FROM Pokemons p

    LEFT JOIN (
        SELECT
            pt.id_pokemon,
            pt.id_tipo,
            ROW_NUMBER() OVER (
                PARTITION BY pt.id_pokemon
                ORDER BY pt.id_tipo
            ) AS rn_tipo
        FROM Pokemons_tipos pt
    ) pt
    ON p.id_pokemon = pt.id_pokemon

    LEFT JOIN tipos t
    ON pt.id_tipo = t.id_tipo

    LEFT JOIN (
        SELECT
            ap.id_pokemon,
            ap.id_ataque,
            ROW_NUMBER() OVER (
                PARTITION BY ap.id_pokemon
                ORDER BY ap.id_ataque
            ) AS rn_ataque
        FROM ataques_pokemons ap
    ) ap
    ON p.id_pokemon = ap.id_pokemon

    LEFT JOIN Ataques a
    ON ap.id_ataque = a.id_ataque
    """

    params = []

    # Filtro opcional por tipos de pokemon (agora aceita lista)
    if tipos:
        placeholders = ','.join(['%s'] * len(tipos))
        base_query += f"""
    WHERE p.id_pokemon IN (
        SELECT pt2.id_pokemon
        FROM Pokemons_tipos pt2
        JOIN tipos t2 ON pt2.id_tipo = t2.id_tipo
        WHERE t2.tipo IN ({placeholders})
    )
        """
        params.extend(tipos)

    base_query += """
    GROUP BY
        p.id_pokemon,
        p.nome,
        p.descricao,
        p.imagem,
        p.preco

    ORDER BY
        p.preco
    LIMIT 30 OFFSET %s;
    """

    params.append(offset)

    cursor.execute(base_query, params)

    pokemons=cursor.fetchall()

    conexao.close()

    return pokemons


def recuperar_pokemons_preco_max(pag: int = 0, tipos: list = None):
    conexao,cursor = conectar()
    offset= 30 * int(pag)
    if offset > 0:
        offset= 30 * (int(pag)-1)

    base_query = """SELECT
        p.id_pokemon AS id,
        p.nome AS name,

        MAX(CASE WHEN pt.rn_tipo = 1 THEN t.tipo END) AS type1,
        MAX(CASE WHEN pt.rn_tipo = 2 THEN t.tipo END) AS type2,

        p.descricao AS description,

        MAX(CASE WHEN ap.rn_ataque = 1 THEN a.nome END) AS attack1,
        MAX(CASE WHEN ap.rn_ataque = 1 THEN a.tipo END) AS attack1_type,

        MAX(CASE WHEN ap.rn_ataque = 2 THEN a.nome END) AS attack2,
        MAX(CASE WHEN ap.rn_ataque = 2 THEN a.tipo END) AS attack2_type,

        MAX(CASE WHEN ap.rn_ataque = 3 THEN a.nome END) AS attack3,
        MAX(CASE WHEN ap.rn_ataque = 3 THEN a.tipo END) AS attack3_type,

        MAX(CASE WHEN ap.rn_ataque = 4 THEN a.nome END) AS attack4,
        MAX(CASE WHEN ap.rn_ataque = 4 THEN a.tipo END) AS attack4_type,

        p.imagem AS image,
        p.preco AS price

    FROM Pokemons p

    LEFT JOIN (
        SELECT
            pt.id_pokemon,
            pt.id_tipo,
            ROW_NUMBER() OVER (
                PARTITION BY pt.id_pokemon
                ORDER BY pt.id_tipo
            ) AS rn_tipo
        FROM Pokemons_tipos pt
    ) pt
    ON p.id_pokemon = pt.id_pokemon

    LEFT JOIN tipos t
    ON pt.id_tipo = t.id_tipo

    LEFT JOIN (
        SELECT
            ap.id_pokemon,
            ap.id_ataque,
            ROW_NUMBER() OVER (
                PARTITION BY ap.id_pokemon
                ORDER BY ap.id_ataque
            ) AS rn_ataque
        FROM ataques_pokemons ap
    ) ap
    ON p.id_pokemon = ap.id_pokemon

    LEFT JOIN Ataques a
    ON ap.id_ataque = a.id_ataque
    """

    params = []

    # Filtro opcional por tipos de pokemon (agora aceita lista)
    if tipos:
        placeholders = ','.join(['%s'] * len(tipos))
        base_query += f"""
    WHERE p.id_pokemon IN (
        SELECT pt2.id_pokemon
        FROM Pokemons_tipos pt2
        JOIN tipos t2 ON pt2.id_tipo = t2.id_tipo
        WHERE t2.tipo IN ({placeholders})
    )
        """
        params.extend(tipos)

    base_query += """
    GROUP BY
        p.id_pokemon,
        p.nome,
        p.descricao,
        p.imagem,
        p.preco

    ORDER BY
        p.preco
        DESC
    LIMIT 30 OFFSET %s;
    """

    params.append(offset)

    cursor.execute(base_query, params)

    pokemons=cursor.fetchall()

    conexao.close()

    return pokemons

def recuperar_pokemons_destaques_lendarios():
    conexao,cursor = conectar()
    cursor.execute("""SELECT
        p.id_pokemon AS id,
        p.nome AS name,

        MAX(CASE WHEN pt.rn_tipo = 1 THEN t.tipo END) AS type1,
        MAX(CASE WHEN pt.rn_tipo = 2 THEN t.tipo END) AS type2,

        p.descricao AS description,

        MAX(CASE WHEN ap.rn_ataque = 1 THEN a.nome END) AS attack1,
        MAX(CASE WHEN ap.rn_ataque = 1 THEN a.tipo END) AS attack1_type,

        MAX(CASE WHEN ap.rn_ataque = 2 THEN a.nome END) AS attack2,
        MAX(CASE WHEN ap.rn_ataque = 2 THEN a.tipo END) AS attack2_type,

        MAX(CASE WHEN ap.rn_ataque = 3 THEN a.nome END) AS attack3,
        MAX(CASE WHEN ap.rn_ataque = 3 THEN a.tipo END) AS attack3_type,

        MAX(CASE WHEN ap.rn_ataque = 4 THEN a.nome END) AS attack4,
        MAX(CASE WHEN ap.rn_ataque = 4 THEN a.tipo END) AS attack4_type,

        p.imagem AS image,
        p.preco AS price

    FROM Pokemons p

    LEFT JOIN (
        SELECT
            pt.id_pokemon,
            pt.id_tipo,
            ROW_NUMBER() OVER (
                PARTITION BY pt.id_pokemon
                ORDER BY pt.id_tipo
            ) AS rn_tipo
        FROM Pokemons_tipos pt
    ) pt
    ON p.id_pokemon = pt.id_pokemon

    LEFT JOIN tipos t
    ON pt.id_tipo = t.id_tipo

    LEFT JOIN (
        SELECT
            ap.id_pokemon,
            ap.id_ataque,
            ROW_NUMBER() OVER (
                PARTITION BY ap.id_pokemon
                ORDER BY ap.id_ataque
            ) AS rn_ataque
        FROM ataques_pokemons ap
    ) ap
    ON p.id_pokemon = ap.id_pokemon

    LEFT JOIN Ataques a
    ON ap.id_ataque = a.id_ataque

    WHERE p.nome IN (
    'Articuno',
    'Zapdos',
    'Moltres',
    'Mewtwo',
    'Mew',
    'Raikou',
    'Entei',
    'Suicune',
    'Lugia',
    'Ho-Oh',
    'Celebi',
    'Regirock',
    'Regice',
    'Registeel',
    'Latias',
    'Latios',
    'Kyogre',
    'Groudon',
    'Rayquaza',
    'Jirachi',
    'Deoxys',
    'Hoopa',
    'Hoopa-Despertado'
    )

    GROUP BY
        p.id_pokemon,
        p.nome,
        p.descricao,
        p.imagem,
        p.preco

    ORDER BY
        p.id_pokemon;""")


    pokemons=cursor.fetchall()

    conexao.close()

    return pokemons


def recuperar_pokemons_filtro(tipos: list = None,search:str= ""):
    conexao,cursor = conectar()


    base_query = """SELECT
        p.id_pokemon AS id,
        p.nome AS name,

        MAX(CASE WHEN pt.rn_tipo = 1 THEN t.tipo END) AS type1,
        MAX(CASE WHEN pt.rn_tipo = 2 THEN t.tipo END) AS type2,

        p.descricao AS description,

        MAX(CASE WHEN ap.rn_ataque = 1 THEN a.nome END) AS attack1,
        MAX(CASE WHEN ap.rn_ataque = 1 THEN a.tipo END) AS attack1_type,

        MAX(CASE WHEN ap.rn_ataque = 2 THEN a.nome END) AS attack2,
        MAX(CASE WHEN ap.rn_ataque = 2 THEN a.tipo END) AS attack2_type,

        MAX(CASE WHEN ap.rn_ataque = 3 THEN a.nome END) AS attack3,
        MAX(CASE WHEN ap.rn_ataque = 3 THEN a.tipo END) AS attack3_type,

        MAX(CASE WHEN ap.rn_ataque = 4 THEN a.nome END) AS attack4,
        MAX(CASE WHEN ap.rn_ataque = 4 THEN a.tipo END) AS attack4_type,

        p.imagem AS image,
        p.preco AS price

    FROM Pokemons p

    LEFT JOIN (
        SELECT
            pt.id_pokemon,
            pt.id_tipo,
            ROW_NUMBER() OVER (
                PARTITION BY pt.id_pokemon
                ORDER BY pt.id_tipo
            ) AS rn_tipo
        FROM Pokemons_tipos pt
    ) pt
    ON p.id_pokemon = pt.id_pokemon

    LEFT JOIN tipos t
    ON pt.id_tipo = t.id_tipo

    LEFT JOIN (
        SELECT
            ap.id_pokemon,
            ap.id_ataque,
            ROW_NUMBER() OVER (
                PARTITION BY ap.id_pokemon
                ORDER BY ap.id_ataque
            ) AS rn_ataque
        FROM ataques_pokemons ap
    ) ap
    ON p.id_pokemon = ap.id_pokemon

    LEFT JOIN Ataques a
    ON ap.id_ataque = a.id_ataque
    """

    params = []

    # Filtro opcional por tipos de pokemon (agora aceita lista)
    if tipos:
        placeholders = ','.join(['%s'] * len(tipos))
        base_query += f"""
    WHERE p.id_pokemon IN (
        SELECT pt2.id_pokemon
        FROM Pokemons_tipos pt2
        JOIN tipos t2 ON pt2.id_tipo = t2.id_tipo
        WHERE t2.tipo IN ({placeholders})
    )
        """
        params.extend(tipos)

    base_query += """

    WHERE p.nome 
    LIKE %s


    GROUP BY
        p.id_pokemon,
        p.nome,
        p.descricao,
        p.imagem,
        p.preco;
    """

    params.append(search)

    cursor.execute(base_query, params)

    pokemons=cursor.fetchall()

    conexao.close()

    return pokemons