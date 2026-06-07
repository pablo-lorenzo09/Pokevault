from flask import Flask, render_template, request, redirect, session, jsonify
# from models.itens import recuperar_produtos, recuperar_produtos_destaques,recuperar_produto
# from models.pokemon import cadastrar_usuarios
# from models.usuario import pegar_login
app = Flask(__name__)

app.secret_key = 'IsoSOsoso'

@app.route("/")
@app.route("/inicio")
def pagina_inicial():
    return render_template("index.html")

@app.route("/login")
def pagina_login():
    return render_template("login.html")

@app.route("/cadastro")
def pagina_cadastro():
    return render_template("cadastro.html")

@app.route("/catalogo")
def pagina_catalogo():
    return render_template("catalogo.html")
# @app.route("/produto/<int:codigo>")
# def segunda_pagina(codigo):
#     return render_template("produto.html", produto = produto)



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