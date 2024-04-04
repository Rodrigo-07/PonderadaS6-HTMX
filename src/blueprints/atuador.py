from flask import Blueprint, current_app
from tinydb import TinyDB, Query
from datetime import datetime

# Blueprint para o controle do atuador
atuador_blueprint = Blueprint('atuador', __name__)

db= TinyDB('db.json', indent=4)
db_log = TinyDB('db_log.json', indent=4)

# Rota para acionar o atuador
@atuador_blueprint.route('/atuador/<acao>/<estado>', methods=['POST'])
def funcao_atuador(acao, estado):
    if not current_app.config['ESTADO_CONEXAO_ROBO']:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Atuador', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Robô desconectado. Conecte Primeiro.'})
        return "Robô desconectado. Conecte Primeiro"
    else:
        print(acao, estado)
        # Acionar o atuador
        current_app.dobot.atuador(acao, estado)

        mensagem_log = f'Atuador acionado com sucesso. Ação: {acao}, Estado: {estado}'
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Atuador', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': mensagem_log})

        return "Atuador acionado com sucesso."
