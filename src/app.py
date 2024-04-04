from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS
from tinydb import TinyDB, Query
from flask import session
import os
from dobot import Dobot
from datetime import datetime

# Instaciando servidor em Flask
app = Flask(__name__)

dobot = Dobot()

estado_conexao_robo = False

# Habilitando o CORS para todos os dominios
CORS(app)

db= TinyDB('db.json', indent=4)
db_log = TinyDB('db_log.json', indent=4)

# Configuração para recarregar os templates (Páginas HTML) automaticamente
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/home_content", methods=['GET'])
def home_content():
    return render_template('home_content.html')

@app.route('/conectarRobot', methods=['POST'])
def conexaoRobot():
    global estado_conexao_robo
    print("Conectando com o robô.")

    try:
        dobot.conectar_dobot()
        estado_conexao_robo = True 
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Conexão com Robô', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': 'Conexão com o robô estabelecida.'})
        print("Conectado com sucesso.")
    except Exception as e:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Conexão com Robô', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Falha ao conectar com o robô.'})
        print("Falha ao conectar com o robô:" + str({e}))
    return ("", 204)

@app.route('/desconectarRobot', methods=['POST'])
def desconectarRobot():
    global estado_conexao_robo
    estado_conexao_robo = False
    db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Desconexão com Robô', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': 'Desconexão com o robô estabelecida.'})
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
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação para Posição Específica', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        x = float(request.form.get('x'))
        y = float(request.form.get('y'))
        z = float(request.form.get('z'))
        r = float(request.form.get('r'))

        dobot.mover_para(x, y, z, r)

        print(f'x: {x}, y: {y}, z: {z}, r: {r}')

        mensagem_log = f'Movido para a posição especificada. x: {x}, y: {y}, z: {z}, r: {r}'

        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação para Posição Específica', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Movido para a posição especificada."

@app.route('/salvar_posicao')
def salvar_posicao():
    return render_template('salvar_posicoes.html')

@app.route('/salvar_posicao_atual')
def salvar_posicao_atual():
    return render_template('salvar_posicao_atual.html')

@app.route('/salvarPosicao', methods=['POST'])
def salvarPosicao():
    global estado_conexao_robo
    if not estado_conexao_robo:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Salvar Posição', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        nome = request.form.get('nome')
        x = float(request.form.get('x'))
        y = float(request.form.get('y'))
        z = float(request.form.get('z'))
        r = float(request.form.get('r'))

        db.insert({'nome': nome, 'x': x, 'y': y, 'z': z, 'r': r})

        mensagem_log = f'Posição salva com sucesso. Nome: {nome}, x: {x}, y: {y}, z: {z}, r: {r}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Salvar Posição', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Posição salva com sucesso"

@app.route('/salvarPosicao_atualDobot', methods=['POST'])
def salvarPosicaoAtualDobot():
    global estado_conexao_robo
    if not estado_conexao_robo:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Salvar Posição Atual', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        nome = request.form.get('nome')
        posicao = dobot.obter_posicao()

        x, y, z, r = round(posicao[0], 2), round(posicao[1], 2), round(posicao[2], 2), round(posicao[3],2)

        db.insert({'nome': nome, 'x': x, 'y': y, 'z': z, 'r': r})

        mensagem_log = f'Posição salva com sucesso. Nome: {nome}, x: {x}, y: {y}, z: {z}, r: {r}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Salvar Posição Atual', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Posição salva com sucesso"

@app.route('/listar_posicoes', methods=['GET'])
def listarPosicoes():
    posicoes = db.all()
    return render_template('movi_posicao_salva.html', posicoes=posicoes)

@app.route('/movimentar_posicao_salva/<nome_posicao>', methods=['POST'])
def movimentarPosicaoSalva(nome_posicao):
    global estado_conexao_robo
    if not estado_conexao_robo:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação para Posição Salva', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        print(nome_posicao)
        nome = nome_posicao
        posicao = db.search(Query().nome == nome)[0]

        x = posicao['x']
        y = posicao['y']
        z = posicao['z']
        r = posicao['r']

        dobot.mover_para(x, y, z, r)

        mensagem_log = f'Movido para a posição salva. Nome: {nome}, x: {x}, y: {y}, z: {z}, r: {r}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação para Posição Salva', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Movido para a posição salva"

@app.route('/deletar_posicao_salva/<nome_posicao>', methods=['POST'])
def deletarPosicaoSalva(nome_posicao):
    global estado_conexao_robo
    if not estado_conexao_robo:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Deletar Posição Salva', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro. Posicao: {nome_posicao} '})
        return "Robô desconectado. Conecte Primeiro"
    else:
        print(nome_posicao)
        nome = nome_posicao
        db.remove(Query().nome == nome)

        mensagem_log = f'Posição deletada com sucesso. Nome: {nome}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Deletar Posição Salva', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Posição deletada com sucesso"
    
@app.route('/atualizar_posicao_salva_modal/<nome_posicao>', methods=['GET'])
def atualizarPosicaoSalvaModal(nome_posicao):
    posicao = db.search(Query().nome == nome_posicao)[0]


    return render_template('atualizar_posicao_salva.html', active=True, nome=nome_posicao, x=posicao['x'], y=posicao['y'], z=posicao['z'], r=posicao['r'])
    
@app.route('/atualizar_posicao_salva/<nome_posicao>', methods=['POST'])
def atualizarPosicaoSalva(nome_posicao):
    global estado_conexao_robo

    if not estado_conexao_robo:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Atualizar Posição Salva', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        print(nome_posicao)
        nome = nome_posicao
        posicao = Query()

        db.update({'nome': request.form.get('nome'),'x': float(request.form.get('x')),'y': float(request.form.get('y')), 'z': float(request.form.get('z')), 'r': float(request.form.get('r')) }, posicao.nome == nome)

        mensagem_log = f'Posição atualizada com sucesso. Nome: {nome}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Atualizar Posição Salva', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})
        
        return ("", 204)
    
@app.route('/caminho_para_abrir_modal')
def abrir_modal():
    return render_template('atualizar_posicao_salva.html', active=True)  # Onde 'modal.html' é o arquivo com o HTML do modal.

@app.route('/logs', methods=['GET'])
def logs():
    logs = db_log.all()

    logs.reverse()
    return render_template('log.html', logs=logs)

@app.route('/movimentacao_livre')
def movimentacaoLivre():
    return render_template('movimentacao_livre.html')

@app.route('/movimentacaoLivre/<direcao>/<taxa>', methods=['POST'])
def movimentacaoLivreDirecao(direcao, taxa):
    global estado_conexao_robo
    if not estado_conexao_robo:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação Livre', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        print(direcao, taxa)
        dobot.movimentacao_livre(direcao, float(taxa))

        mensagem_log = f'Movimentação livre realizada com sucesso. Direção: {direcao}, Taxa: {taxa}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação Livre', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Movimentação livre realizada com sucesso."
    
@app.route('/atuador/<acao>/<estado>', methods=['POST'])
def atuador(acao, estado):
    global estado_conexao_robo
    if not estado_conexao_robo:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Atuador', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        print(acao, estado)
        dobot.atuador(acao, estado)

        mensagem_log = f'Atuador acionado com sucesso. Ação: {acao}, Estado: {estado}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Atuador', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Atuador acionado com sucesso."