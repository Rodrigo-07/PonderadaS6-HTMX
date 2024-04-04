from flask import Blueprint, request, current_app
from tinydb import TinyDB, Query
from flask import current_app
from datetime import datetime
from flask import current_app as app

# Blueprint para edição de posições (UPDATE, ADD, SELECT, DELETE)
edicoes_posicoes = Blueprint('edicoes_posicoes', __name__)

db= TinyDB('db.json', indent=4)
db_log = TinyDB('db_log.json', indent=4)

# Rota para salvar uma posição
@edicoes_posicoes.route('/salvarPosicao', methods=['POST'])
def salvarPosicao():
    if not current_app.config['ESTADO_CONEXAO_ROBO']:
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
    
# Rota para salvar uma nova com os valores da posição atual do Dobot
@edicoes_posicoes.route('/salvarPosicao_atualDobot', methods=['POST'])
def salvarPosicaoAtualDobot():
    if not current_app.config['ESTADO_CONEXAO_ROBO']:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Salvar Posição Atual', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        nome = request.form.get('nome')
        posicao = app.dobot.obter_posicao()

        # Arredondar os valores para 2 casas decimais e salvar no banco
        x, y, z, r = round(posicao[0], 2), round(posicao[1], 2), round(posicao[2], 2), round(posicao[3],2)

        db.insert({'nome': nome, 'x': x, 'y': y, 'z': z, 'r': r})

        mensagem_log = f'Posição salva com sucesso. Nome: {nome}, x: {x}, y: {y}, z: {z}, r: {r}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Salvar Posição Atual', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Posição salva com sucesso"

# Rota para deletar uma posição salva atraves do nome dela
@edicoes_posicoes.route('/deletar_posicao_salva/<nome_posicao>', methods=['POST'])
def deletarPosicaoSalva(nome_posicao):
    if not current_app.config['ESTADO_CONEXAO_ROBO']:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Deletar Posição Salva', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro. Posicao: {nome_posicao} '})
        return "Robô desconectado. Conecte Primeiro"
    else:
        print(nome_posicao)
        nome = nome_posicao

        # Deletar a posição salva
        db.remove(Query().nome == nome)

        mensagem_log = f'Posição deletada com sucesso. Nome: {nome}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Deletar Posição Salva', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Posição deletada com sucesso"


@edicoes_posicoes.route('/atualizar_posicao_salva/<nome_posicao>', methods=['POST'])
def atualizarPosicaoSalva(nome_posicao):

    if not current_app.config['ESTADO_CONEXAO_ROBO']:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Atualizar Posição Salva', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        print(nome_posicao)
        nome = nome_posicao
        posicao = Query()

        # Atualizar todas as informações posição salva
        db.update({'nome': request.form.get('nome'),'x': float(request.form.get('x')),'y': float(request.form.get('y')), 'z': float(request.form.get('z')), 'r': float(request.form.get('r')) }, posicao.nome == nome)

        mensagem_log = f'Posição atualizada com sucesso. Nome: {nome}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Atualizar Posição Salva', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})
        
        return ("", 204)