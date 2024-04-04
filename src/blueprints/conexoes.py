from flask import Blueprint, render_template, request, current_app
from dobot import Dobot  # Assumindo que você tenha uma classe separada para o Dobot
from tinydb import TinyDB
from flask import current_app
from datetime import datetime
from flask import current_app as app


conexoes = Blueprint('conexoes', __name__)

db= TinyDB('db.json', indent=4)
db_log = TinyDB('db_log.json', indent=4)

@conexoes.route('/conectarRobot', methods=['POST'])
def conexaoRobot():
    print("Conectando com o robô.")

    try:
        # app.dobot.conectar_dobot()
        current_app.config['ESTADO_CONEXAO_ROBO'] = True 
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Conexão com Robô', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': 'Conexão com o robô estabelecida.'})
        print("Conectado com sucesso.")
    except Exception as e:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Conexão com Robô', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Falha ao conectar com o robô.'})
        print("Falha ao conectar com o robô:" + str({e}))
    return ("", 204)

@conexoes.route('/desconectarRobot', methods=['POST'])
def desconectarRobot(): 
    current_app.config['ESTADO_CONEXAO_ROBO'] = False

    db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Desconexão com Robô', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': 'Desconexão com o robô estabelecida.'})
    return ("", 204)