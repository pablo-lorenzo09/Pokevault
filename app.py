from flask import Flask, render_template, request, redirect, session, jsonify
from model.pokemons_select import recuperar_pokemons
from model.pokemons_select import recuperar_pokemon_unitario
from model.pokemons_select import recuperar_pokemons_destaques
from model.pokemons_select import recuperar_pokemons_destaques_lendarios
from model.pokemons_select import recuperar_tipos
from model.pokemons_select import recuperar_pokemons_preco_min
from model.pokemons_select import recuperar_pokemons_preco_max
from model.tipos import recuperar_tipos
from model.usuario import cadastrar
from model.usuario import logar
from model.comentarios import enviar_comentario_unitario
from model.comentarios import obter_comentarios_unitario
from model.comentarios import deletar_comentario_unitario
from model.carrinho import recuperar_carrinho
from model.carrinho import adicionar_pokemon_carrinho
from model.carrinho import remover_pokemon_carrinho
# from models.itens import recuperar_produtos, recuperar_produtos_destaques,recuperar_produto
# from models.pokemon import cadastrar_usuarios
# from models.usuario import pegar_login
import json

# Abrir arquivo JSON
with open("pokemons.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

# Transformar em lista
lista = list(dados)

app = Flask(__name__)

app.secret_key = 'IsoSOsoso'

@app.route("/")
@app.route("/inicio")
def pagina_inicial():
    poke_destaque = recuperar_pokemons_destaques()
    poke_len_destaque=recuperar_pokemons_destaques_lendarios()
    return render_template("index.html",destaques=poke_destaque, destaques_len = poke_len_destaque)

@app.route("/login")
def pagina_login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario_logado", None) 
    return redirect("/")  

@app.route("/login/post", methods=["POST"])
def logar_usuario_post():
    email = request.form.get("email")
    senha = request.form.get("senha")

    resultado = logar(email, senha)

    if resultado:
        session["usuario_logado"] = resultado
        print("RESULTADO LOGIN:", resultado["id_usuario"])
    return redirect("/")

@app.route("/cadastro")
def pagina_cadastro():
    return render_template("cadastro.html")

@app.route("/cadastro/post", methods=["POST"])
def tela_cadastro_post():
    email = request.form.get("email")
    senha = request.form.get("senha")
    nome = request.form.get("nome_completo")
    telefone = request.form.get("telefone")
    endereco = request.form.get("endereco")
    
    cadastrar(email, nome, telefone, endereco, senha)

    return redirect("/login")

@app.route("/catalogo/<pag>")
def pagina_catalogo(pag=0):
    tipos_filtro = request.args.getlist("tipo")
    ordem = request.args.get("ordem")

    if ordem == "asc":
        pokemons = recuperar_pokemons_preco_min(pag=pag, tipos=tipos_filtro)
    elif ordem == "desc":
        pokemons = recuperar_pokemons_preco_max(pag=pag, tipos=tipos_filtro)
    else:
        pokemons = recuperar_pokemons(pag=pag, tipos=tipos_filtro)

    tipos = recuperar_tipos()
    return render_template(
        "catalogo.html",
        pokemons=pokemons,
        tipos=tipos,
        tipos_selecionados=tipos_filtro,
        ordem_selecionada=ordem,
        pag=pag
    )
@app.route("/unitario/<id>")
def pagina_unitario(id):
    pokemon = recuperar_pokemon_unitario(id)
    return render_template("unitario.html",pokemon = pokemon)

@app.route("/unitario/<id>/comentarios/get", methods=['GET'])
def unitario_get_comentarios(id):
    comentarios = obter_comentarios_unitario(int(id))
    return jsonify(comentarios), 200

@app.route("/unitario/<id>/comentarios/post", methods=['POST'])
def unitario_post_comentario(id):
    if "usuario_logado" not in session:
        return jsonify({'message': 'Não autorizado'}), 401

    dados = request.get_json()
    usuario = session["usuario_logado"]

    enviar_comentario_unitario(
        comentario=dados.get('comentario'),
        id_pokemon=int(id),
        nome_usuario=usuario['nome'],  # 
        nota=dados.get('nota')
    )
    return jsonify({'message': 'Comentário enviado com sucesso'}), 200

@app.route("/unitario/<id>/comentarios/delete", methods=['DELETE'])
def unitario_delete_comentario(id):
    dados = request.get_json()
    deletar_comentario_unitario(int(dados.get('codigo')))
    return jsonify({'message': 'Comentário deletado'}), 200

@app.route("/carrinho")
def pag_carrinho():
    if 'usuario_logado' in session:
        return jsonify(recuperar_carrinho(session['usuario_logado']["id_usuario"])),200
    else :
        return jsonify({"message":"Usuario não logado"}),401

@app.route("/carrinho/post/<int:id>")
def pag_carrinho_post(id):
    adicionar_pokemon_carrinho(id,session['usuario_logado']["id_usuario"])
    return redirect("/inicio")

@app.route("/carrinho/delete/<int:id>")
def pag_carrinho_delete(id):
    remover_pokemon_carrinho(id,session['usuario_logado']["id_usuario"])
    return redirect("/inicio")


# @app.route("/api/get/carrinho", methods = ["GET"])
# def api_get_carrinho():
#     if "usuario_logado" in session:
#         usuario = session["usuario_logado"]["codigo_usuario"]
#         carrinho = recuperar_carrinho(usuario)
#         return jsonify(carrinho), 200
#     else:
#         return jsonify({"message":"Usuario não logado"}), 401


# @app.route("/api/inserir/carrinho", methods = ["POST"])
# def inserir_no_carrinho():
#     if "usuario_logado" in session:
#         usuario = session["usuario_logado"]["codigo_usuario"]
#         dados_json = request.get_json()
#         codigo_produto = dados_json.get("codigo_produto")
#         quantidade = dados_json.get("quantidade")

#         inserir_item(usuario, codigo_produto, quantidade)

#         return jsonify({"message": "Funcionou"}), 200
#     else:
#         return redirect ("/login")

    

# @app.route("/cadastro")
# def terceira_pagina():
#     return render_template("cadastro.html")


# @app.route('/cadastro/post', methods = ['POST'])
# def salvar_cadastro():
#     usuario = request.form.get('cadastrar_usuario')
#     senha = request.form.get('cadastrar_senha_usuario')
#     nick = request.form.get('cadastrar_nick_usuario')
#     if cadastrar_usuarios(usuario,senha,nick):
#         return redirect('/inicio')
#     else:
#         return 'Algum campo principal em branco.'
    

# @app.route("/login")
# def quarta_pagina():
#     return render_template("login.html")


# @app.route('/login/post', methods = ['POST'])
# def rota_login():
#     login_usuario = request.form.get('logar_usuario')
#     senha_usuario = request.form.get('logar_senha_usuario')
#     nick_usuario =  request.form.get('logar_nick_usuario')

#     resultado = pegar_login(login_usuario,senha_usuario,nick_usuario)
#     if resultado:
#         session['usuario_logado'] = resultado

#         return redirect('/inicio')
#     else:
#         return redirect('/login')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)