import json
import time
from deep_translator import GoogleTranslator

# Tradutor
translator = GoogleTranslator(source="en", target="pt")

# Traduções fixas dos tipos
TIPOS = {
    "Normal": "Normal",
    "Fire": "Fogo",
    "Water": "Água",
    "Electric": "Elétrico",
    "Grass": "Planta",
    "Ice": "Gelo",
    "Fighting": "Lutador",
    "Poison": "Veneno",
    "Ground": "Terra",
    "Flying": "Voador",
    "Psychic": "Psíquico",
    "Bug": "Inseto",
    "Rock": "Pedra",
    "Ghost": "Fantasma",
    "Dragon": "Dragão",
    "Dark": "Sombrio",
    "Steel": "Aço",
    "Fairy": "Fada"
}


def traduzir(texto):
    if not texto:
        return texto

    try:
        return translator.translate(texto)
    except Exception as e:
        print(f"Erro ao traduzir: {texto}")
        print(e)
        return texto


# Carrega JSON original
with open("pokemons.json", "r", encoding="utf-8") as f:
    pokemons = json.load(f)

total = len(pokemons)

for i, pokemon in enumerate(pokemons, start=1):

    print(f"[{i}/{total}] Traduzindo {pokemon['name']}...")

    # Tipos do Pokémon
    pokemon["type1"] = TIPOS.get(
        pokemon["type1"],
        pokemon["type1"]
    )

    if pokemon.get("type2"):
        pokemon["type2"] = TIPOS.get(
            pokemon["type2"],
            pokemon["type2"]
        )

    # Descrição
    pokemon["description"] = traduzir(
        pokemon["description"]
    )

    # Ataques
    for n in range(1, 5):

        pokemon[f"attack{n}"] = traduzir(
            pokemon[f"attack{n}"]
        )

        pokemon[f"attack_type{n}"] = TIPOS.get(
            pokemon[f"attack_type{n}"],
            pokemon[f"attack_type{n}"]
        )


# Salva em OUTRO arquivo
with open(
    "pokemons_pt.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        pokemons,
        f,
        ensure_ascii=False,
        indent=4
    )

print("✅ Arquivo pokemons_pt.json criado com sucesso!")