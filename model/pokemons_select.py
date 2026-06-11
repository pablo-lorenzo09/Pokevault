from database.conexao import conectar

def recuperar_pokemons(pag:int=0):
    conexao,cursor = conectar()
    offset= 30 * int(pag)
    if offset > 0:
        offset= 30 * (int(pag)-1)
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

    GROUP BY
        p.id_pokemon,
        p.nome,
        p.descricao,
        p.imagem,
        p.preco

    ORDER BY
        p.id_pokemon
        LIMIT 30 OFFSET %s;""", [offset])


    pokemons=cursor.fetchall()

    conexao.close()

    return pokemons
