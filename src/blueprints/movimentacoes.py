from flask import Blueprint, request, current_app
from tinydb import TinyDB, Query
from flask import current_app
from datetime import datetime
from flask import current_app 

# Blueprint para movimentações do robô
movimentacoes = Blueprint('movimentacoes', __name__)

db= TinyDB('db.json', indent=4)
db_log = TinyDB('db_log.json', indent=4)

# Rota para movimentar o robô para uma posição específica atraves das infos de um forms
@movimentacoes.route('/posicaoEspefica', methods=['POST'])
def posicaoEspecifica():
    estado_conexao_robo = current_app.config['ESTADO_CONEXAO_ROBO']
    if not estado_conexao_robo:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação para Posição Específica', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        # Pegar os valores do form
        x = float(request.form.get('x'))
        y = float(request.form.get('y'))
        z = float(request.form.get('z'))
        r = float(request.form.get('r'))

        # Movimentar o robô para a posição especificada
        current_app.dobot.mover_para(x, y, z, r)

        print(f'x: {x}, y: {y}, z: {z}, r: {r}')

        # Mensagem de log
        mensagem_log = f'Movido para a posição especificada. x: {x}, y: {y}, z: {z}, r: {r}'

        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação para Posição Específica', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Movido para a posição especificada."
    
# Rota para movimentar o robô para uma posição salva atraves do nome dela
@movimentacoes.route('/movimentar_posicao_salva/<nome_posicao>', methods=['POST'])
def movimentarPosicaoSalva(nome_posicao):
    estado_conexao_robo = current_app.config['ESTADO_CONEXAO_ROBO']
    if not estado_conexao_robo:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação para Posição Salva', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        print(nome_posicao)
        nome = nome_posicao

        # Buscar a posição no banco
        posicao = db.search(Query().nome == nome)[0]
        
        # Pegar os valores da posição
        x = posicao['x']
        y = posicao['y']
        z = posicao['z']
        r = posicao['r']

        # Movimentar o robô para a posição salva
        current_app.dobot.mover_para(x, y, z, r)

        # Mensagem de log
        mensagem_log = f'Movido para a posição salva. Nome: {nome}, x: {x}, y: {y}, z: {z}, r: {r}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação para Posição Salva', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Movido para a posição salva"

# Controlar o robô livremente para qualquer direção
@movimentacoes.route('/movimentacaoLivre/<direcao>/<taxa>', methods=['POST'])
def movimentacaoLivreDirecao(direcao, taxa):
    if not current_app.config['ESTADO_CONEXAO_ROBO']:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação Livre', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        print(direcao, taxa)

        # Passar uma direção e uma taxa para a movimentação na direção especificada
        current_app.dobot.movimentacao_livre(direcao, float(taxa))

        # Mensagem de log
        mensagem_log = f'Movimentação livre realizada com sucesso. Direção: {direcao}, Taxa: {taxa}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Movimentação Livre', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Movimentação livre realizada com sucesso."