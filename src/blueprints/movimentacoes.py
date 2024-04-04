from flask import Blueprint, render_template, request, current_app
from dobot import Dobot  # Assumindo que você tenha uma classe separada para o Dobot
from tinydb import TinyDB, Query
from flask import current_app
from datetime import datetime
from flask import current_app as app


movimentacoes = Blueprint('movimentacoes', __name__)

db= TinyDB('db.json', indent=4)
db_log = TinyDB('db_log.json', indent=4)

@movimentacoes.route('/posicaoEspefica', methods=['POST'])
def posicaoEspecifica():
    estado_conexao_robo = current_app.config['ESTADO_CONEXAO_ROBO']
    if not estado_conexao_robo:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação para Posição Específica', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        x = float(request.form.get('x'))
        y = float(request.form.get('y'))
        z = float(request.form.get('z'))
        r = float(request.form.get('r'))

        app.dobot.mover_para(x, y, z, r)

        print(f'x: {x}, y: {y}, z: {z}, r: {r}')

        mensagem_log = f'Movido para a posição especificada. x: {x}, y: {y}, z: {z}, r: {r}'

        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação para Posição Específica', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Movido para a posição especificada."
    

@movimentacoes.route('/movimentar_posicao_salva/<nome_posicao>', methods=['POST'])
def movimentarPosicaoSalva(nome_posicao):
    estado_conexao_robo = current_app.config['ESTADO_CONEXAO_ROBO']
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

        app.dobot.mover_para(x, y, z, r)

        mensagem_log = f'Movido para a posição salva. Nome: {nome}, x: {x}, y: {y}, z: {z}, r: {r}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação para Posição Salva', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Movido para a posição salva"

@movimentacoes.route('/movimentacaoLivre/<direcao>/<taxa>', methods=['POST'])
def movimentacaoLivreDirecao(direcao, taxa):
    estado_conexao_robo = current_app.config['ESTADO_CONEXAO_ROBO']
    if not estado_conexao_robo:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação Livre', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        print(direcao, taxa)
        app.dobot.movimentacao_livre(direcao, float(taxa))

        mensagem_log = f'Movimentação livre realizada com sucesso. Direção: {direcao}, Taxa: {taxa}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação Livre', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Movimentação livre realizada com sucesso."