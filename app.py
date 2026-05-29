from flask import Flask, jsonify, render_template,request,redirect,session,flash
import mysql
import mysql.connector
import json

import json

# Abrir arquivo JSON
with open("dados.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

# Transformar em lista
lista = list(dados)


app = Flask(__name__)

app.secret_key='chave-secreta-demais'

@app.route("/")
def pag_teste():
    return render_template("home.html")

