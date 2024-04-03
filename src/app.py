from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS
from tinydb import TinyDB, Query
from flask import session
import os
from dobot import Dobot


# Instaciando servidor em Flask
app = Flask(__name__)

dobot = Dobot()

estado_conexao_robo = False

# Habilitando o CORS para todos os dominios
CORS(app)

db= TinyDB('db.json', indent=4)

# Configuração para recarregar os templates (Páginas HTML) automaticamente
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=['GET'])
def index():
    return render_template('Index.html')

@app.route("/teste", methods=['GET'])
def teste():
    return "Oiii"


@app.route('/conectarRobot', methods=['POST'])
def conexaoRobot():
    global estado_conexao_robo
    estado_conexao_robo = True 
    return ("", 204)

@app.route('/desconectarRobot', methods=['POST'])
def desconectarRobot():
    global estado_conexao_robo
    estado_conexao_robo = False
    return ("", 204)

@app.route('/verificarConexaoBotao', methods=['GET'])
def verificarConexao():
    global estado_conexao_robo
    if estado_conexao_robo:
        return render_template('conexao_status.html', status="Conectado")
    else:
        return render_template('conexao_status.html', status="Desconectado")
    
@app.route('/verificarConexaoNavbar', methods=['GET'])
def verificarConexaoNavbar():
    global estado_conexao_robo
    if estado_conexao_robo:
        return render_template('movimentacao_navbar.html', status="Conectado")
    else:
        return render_template('movimentacao_navbar.html', status="Desconectado")
    
@app.route('/mov_posicao_espesifica')
def mov_posicao_espesifica():
    return render_template('movi_posicao_especifica.html')

@app.route('/posicaoEspefica', methods=['POST'])
def posicaoEspecifica():
    global estado_conexao_robo
    if not estado_conexao_robo:
        return "Robô desconectado. Conecte Primeiro"
    else:
        x = float(request.form.get('x'))
        y = float(request.form.get('y'))
        z = float(request.form.get('z'))
        r = float(request.form.get('r'))

        # dobot.mover_para(x, y, z, r)

        print(f'x: {x}, y: {y}, z: {z}, r: {r}')

        return "Movido para a posição especificada."

@app.route('/salvar_posicao')
def salvar_posicao():
    return render_template('salvar_posicoes.html')

@app.route('/salvarPosicao', methods=['POST'])
def salvarPosicao():
    global estado_conexao_robo
    if not estado_conexao_robo:
        return "Robô desconectado. Conecte Primeiro"
    else:
        nome = request.form.get('nome')
        x = float(request.form.get('x'))
        y = float(request.form.get('y'))
        z = float(request.form.get('z'))
        r = float(request.form.get('r'))

        db.insert({'nome': nome, 'x': x, 'y': y, 'z': z, 'r': r})

        return "Posição salva com sucesso"


@app.route('/listar_posicoes', methods=['GET'])
def listarPosicoes():
    posicoes = db.all()
    return render_template('movi_posicao_salva.html', posicoes=posicoes)

@app.route('/movimentar_posicao_salva/<nome_posicao>', methods=['POST'])
def movimentarPosicaoSalva(nome_posicao):
    global estado_conexao_robo
    if not estado_conexao_robo:
        return "Robô desconectado. Conecte Primeiro"
    else:
        print(nome_posicao)
        nome = nome_posicao
        posicao = db.search(Query().nome == nome)[0]

        x = posicao['x']
        y = posicao['y']
        z = posicao['z']
        r = posicao['r']

        # dobot.mover_para(x, y, z, r)

        return "Movido para a posição salva"
