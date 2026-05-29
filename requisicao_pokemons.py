import requests
import json
from concurrent.futures import ThreadPoolExecutor

def get_move_name_and_type(move_name):
    """Busca o nome e o tipo do golpe em inglês"""
    try:
        move_data = requests.get(f"https://pokeapi.co/api/v2/move/{move_name}").json()
        
        # Busca o nome em inglês
        move_display_name = move_name.replace("-", " ").title()
        for name in move_data["names"]:
            if name["language"]["name"] == "en":
                move_display_name = name["name"]
                break
        
        # Busca o tipo do golpe
        move_type = move_data["type"]["name"].title()
        
        return move_display_name, move_type
    except:
        return move_name.replace("-", " ").title(), "Normal"

def get_pokemon_rarity(pokemon_id, species_data):
    """Determina a raridade do Pokémon"""
    
    # Lista de Pokémon lendários (IDs conhecidos até a geração 3)
    legendary_ids = {
        144, 145, 146, 150, 151, 243, 244, 245, 249, 250, 251, 
        377, 378, 379, 380, 381, 382, 383, 384, 385, 386
    }
    
    # Verifica se é lendário
    if pokemon_id in legendary_ids:
        return "legendary"
    
    # Verifica taxa de captura
    capture_rate = species_data.get("capture_rate", 127)
    if capture_rate <= 3:
        return "legendary"
    elif capture_rate <= 25:
        return "very_rare"
    elif capture_rate <= 75:
        return "rare"
    elif capture_rate <= 150:
        return "common"
    else:
        return "very_common"

def calculate_pokemon_price(pokemon_id, pokemon_data, species_data):
    """Calcula o preço do Pokémon (máximo 2000)"""
    
    rarity = get_pokemon_rarity(pokemon_id, species_data)
    
    # Preços base por raridade (ajustados para máximo 2000)
    rarity_prices = {
        "very_common": 50,
        "common": 100,
        "rare": 250,
        "very_rare": 500,
        "legendary": 1000
    }
    
    base_price = rarity_prices[rarity]
    multiplier = 1.0
    
    # Fator Base Stats
    stats_total = sum(stat["base_stat"] for stat in pokemon_data["stats"])
    if stats_total >= 600:
        multiplier *= 2.0
    elif stats_total >= 500:
        multiplier *= 1.5
    elif stats_total >= 400:
        multiplier *= 1.2
    elif stats_total >= 300:
        multiplier *= 1.0
    else:
        multiplier *= 0.8
    
    # Bônus por Tipo
    type_bonus = {
        "Dragon": 1.3,
        "Psychic": 1.2,
        "Ghost": 1.15,
        "Dark": 1.1,
        "Steel": 1.1,
        "Fairy": 1.05,
        "Fire": 1.05,
        "Electric": 1.05,
        "Ice": 1.0,
        "Fighting": 1.0,
        "Normal": 0.9,
        "Bug": 0.85,
        "Grass": 0.9,
        "Poison": 0.9,
        "Rock": 0.95
    }
    
    # Aplica bônus do tipo1
    type1 = pokemon_data["types"][0]["type"]["name"].title()
    if type1 in type_bonus:
        multiplier *= type_bonus[type1]
    
    # Aplica bônus do type2 se existir
    if len(pokemon_data["types"]) > 1:
        type2 = pokemon_data["types"][1]["type"]["name"].title()
        if type2 in type_bonus:
            multiplier *= type_bonus[type2]
    
    # Calcula preço final
    final_price = int(base_price * multiplier)
    
    # Garante que não ultrapasse 2000
    if final_price > 2000:
        final_price = 2000
    
    # Caso especial: Mewtwo (ID 150) tem preço máximo
    if pokemon_id == 150:
        final_price = 2000
    
    # Arredonda para números bonitos
    if final_price < 100:
        final_price = round(final_price / 10) * 10
    elif final_price < 500:
        final_price = round(final_price / 25) * 25
    else:
        final_price = round(final_price / 50) * 50
    
    # Garante mínimo de 10
    if final_price < 10:
        final_price = 10
    
    return final_price

def get_pokemon_data(pokemon_id):
    """Busca todos os dados de um Pokémon"""
    try:
        # Busca dados principais do Pokémon
        pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}").json()
        
        # Busca dados da espécie
        species = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}").json()
        
        # Pega a descrição em inglês
        description = ""
        for entry in species["flavor_text_entries"]:
            if entry["language"]["name"] == "en":
                description = entry["flavor_text"].replace("\n", " ").replace("\f", " ").replace("\u000c", " ")
                break
        
        # Pega os tipos
        types = [t["type"]["name"].title() for t in pokemon["types"]]
        type1 = types[0] if len(types) > 0 else None
        type2 = types[1] if len(types) > 1 else None
        
        # Calcula o preço
        price = calculate_pokemon_price(pokemon_id, pokemon, species)
        
        # Pega os 4 primeiros golpes e seus tipos
        moves = []
        move_types = []
        
        for move in pokemon["moves"][:4]:
            move_name = move["move"]["name"]
            move_display_name, move_type = get_move_name_and_type(move_name)
            moves.append(move_display_name)
            move_types.append(move_type)
        
        # Completa com vazio se tiver menos de 4 golpes
        while len(moves) < 4:
            moves.append("")
            move_types.append("")
        
        # Pega a imagem oficial
        image_url = pokemon["sprites"]["other"]["official-artwork"]["front_default"]
        if not image_url:
            image_url = pokemon["sprites"]["front_default"]
        
        # Retorna todos os campos
        return {
            "id": pokemon["id"],
            "name": pokemon["name"].title(),
            "type1": type1,
            "type2": type2,
            "description": description,
            "attack1": moves[0],
            "attack2": moves[1],
            "attack3": moves[2],
            "attack4": moves[3],
            "attack_type1": move_types[0],
            "attack_type2": move_types[1],
            "attack_type3": move_types[2],
            "attack_type4": move_types[3],
            "image": image_url,
            "price": price
        }
    
    except Exception as e:
        print(f"✖ Erro ao processar Pokémon {pokemon_id}: {e}")
        return None

def main():
    print("🚀 Iniciando coleta de dados dos Pokémons...")
    print("=" * 60)
    
    total_pokemons = 386
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_pokemon_data, i): i for i in range(1, total_pokemons + 1)}
        
        # Lista para armazenar na ordem correta
        results = [None] * (total_pokemons + 1)
        
        for future in futures:
            pokemon_id = futures[future]
            result = future.result()
            if result:
                results[pokemon_id] = result
                tipo_info = f"{result['type1']}"
                if result['type2']:
                    tipo_info += f"/{result['type2']}"
                print(f"✔ {pokemon_id:3d} - {result['name']:15s} - {tipo_info:12s} - ${result['price']:4d}")
    
    # Remove índices vazios
    all_pokemons = [p for p in results[1:] if p is not None]
    
    # Salva em arquivo JSON
    output_file = "pokemons.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_pokemons, f, ensure_ascii=False, indent=4)
    
    print("\n" + "=" * 60)
    print(f"✅ Arquivo '{output_file}' criado com sucesso!")
    print(f"📈 Total de Pokémons: {len(all_pokemons)}")
    
    # Estatísticas de preços
    precos = [p['price'] for p in all_pokemons]
    print(f"\n💰 Preço médio: ${sum(precos) // len(precos):,}")
    print(f"💰 Preço mínimo: ${min(precos):,}")
    print(f"💰 Preço máximo: ${max(precos):,}")
    
    # Mostra os mais baratos e mais caros
    print("\n🔹 5 Pokémons mais baratos:")
    for p in sorted(all_pokemons, key=lambda x: x['price'])[:5]:
        print(f"   ID: {p['id']:3d} | {p['name']:15s} | ${p['price']:4d}")
    
    print("\n🔹 5 Pokémons mais caros:")
    for p in sorted(all_pokemons, key=lambda x: x['price'], reverse=True)[:5]:
        print(f"   ID: {p['id']:3d} | {p['name']:15s} | ${p['price']:4d}")
    
    # Mostra exemplos com ataques e seus tipos
    print("\n📋 Exemplos de Pokémons (com tipos dos ataques):")
    print("-" * 80)
    for p in all_pokemons[:3]:
        print(f"ID: {p['id']} | {p['name']} | {p['type1']}{'/' + p['type2'] if p['type2'] else ''} | ${p['price']}")
        print(f"   Ataque 1: {p['attack1']:20s} (Tipo: {p['attack_type1']})")
        print(f"   Ataque 2: {p['attack2']:20s} (Tipo: {p['attack_type2']})")
        print(f"   Ataque 3: {p['attack3']:20s} (Tipo: {p['attack_type3']})")
        print(f"   Ataque 4: {p['attack4']:20s} (Tipo: {p['attack_type4']})")
        print()
    
    # Mostra o JSON de exemplo do primeiro Pokémon
    print("\n📄 Exemplo do JSON gerado (primeiro Pokémon):")
    print(json.dumps(all_pokemons[0], ensure_ascii=False, indent=2))
    
    print("\n🔥 Finalizado com sucesso!")

if __name__ == "__main__":
    main()