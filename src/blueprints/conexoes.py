from flask import Blueprint, current_app
from tinydb import TinyDB
from flask import current_app
from datetime import datetime

# Blueprint de conexões do robô
conexoes = Blueprint('conexoes', __name__)

db= TinyDB('db.json', indent=4)
db_log = TinyDB('db_log.json', indent=4)

# Rota para conectar com o robô
@conexoes.route('/conectarRobot', methods=['POST'])
def conexaoRobot():
    print("Conectando com o robô.")

    try:
        # Conectar com o robô
        current_app.dobot.conectar_dobot()
        current_app.config['ESTADO_CONEXAO_ROBO'] = True 
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Conexão com Robô', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': 'Conexão com o robô estabelecida.'})
        print("Conectado com sucesso.")
    except Exception as e:
        db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Conexão com Robô', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Falha', 'Mensagem': 'Falha ao conectar com o robô.'})
        print("Falha ao conectar com o robô:" + str({e}))
    return ("", 204)

# Rota para desconectar com o robô
@conexoes.route('/desconectarRobot', methods=['POST'])
def desconectarRobot(): 
    current_app.config['ESTADO_CONEXAO_ROBO'] = False

    # Desconectar com o robô
    current_app.dobot.desconectar_dobot()

    db_log.insert({'Usuario':'Rodrigo', 'Ação': 'Desconexão com Robô', 'Data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Status': 'Sucesso', 'Mensagem': 'Desconexão com o robô estabelecida.'})
    return ("", 204)