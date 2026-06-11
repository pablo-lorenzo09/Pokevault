import mysql.connector
import json

conexao=mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="PokeVault"
        )

cursor=conexao.cursor(dictionary=True)


with open("pokemons_pt.json", "r", encoding="utf-8") as f:
    pokemons = json.load(f)

tipos_ids = {}
ataques_ids = {}

# Evita relacionamentos duplicados
relacoes_tipos = set()
relacoes_ataques = set()

next_tipo_id = 1
next_ataque_id = 1

for pokemon in pokemons:

    # =====================
    # POKEMON
    # =====================

    cursor.execute("""
        INSERT INTO Pokemons
        (id_pokemon, nome, descricao, imagem, preco, destaque)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        pokemon["id"],
        pokemon["name"],
        pokemon["description"],
        pokemon["image"],
        pokemon["price"],
        False
    ))

    # =====================
    # TIPOS
    # =====================

    tipos = [pokemon["type1"]]

    if pokemon.get("type2"):
        tipos.append(pokemon["type2"])

    for tipo in tipos:

        if tipo not in tipos_ids:

            tipos_ids[tipo] = next_tipo_id

            cursor.execute("""
                INSERT INTO tipos
                (id_tipo, tipo)
                VALUES (%s, %s)
            """, (
                next_tipo_id,
                tipo
            ))

            next_tipo_id += 1

        relacao_tipo = (
            tipos_ids[tipo],
            pokemon["id"]
        )

        if relacao_tipo not in relacoes_tipos:

            cursor.execute("""
                INSERT INTO Pokemons_tipos
                (id_tipo, id_pokemon)
                VALUES (%s, %s)
            """, relacao_tipo)

            relacoes_tipos.add(relacao_tipo)

    # =====================
    # ATAQUES
    # =====================

    for i in range(1, 5):

        nome_ataque = pokemon[f"attack{i}"]
        tipo_ataque = pokemon[f"attack_type{i}"]

        chave = (
            nome_ataque,
            tipo_ataque
        )

        if chave not in ataques_ids:

            ataques_ids[chave] = next_ataque_id

            cursor.execute("""
                INSERT INTO Ataques
                (id_ataque, nome, tipo)
                VALUES (%s, %s, %s)
            """, (
                next_ataque_id,
                nome_ataque,
                tipo_ataque
            ))

            next_ataque_id += 1

        relacao_ataque = (
            pokemon["id"],
            ataques_ids[chave]
        )

        if relacao_ataque not in relacoes_ataques:

            cursor.execute("""
                INSERT INTO ataques_pokemons
                (id_pokemon, id_ataque)
                VALUES (%s, %s)
            """, relacao_ataque)

            relacoes_ataques.add(relacao_ataque)

conexao.commit()

cursor.close()
conexao.close()

