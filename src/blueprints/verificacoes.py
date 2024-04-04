from flask import Blueprint, render_template, request, current_app
from tinydb import TinyDB
from flask import current_app

# Blueprint para verificação de conexão
verificacoes = Blueprint('verificacoes', __name__)

db= TinyDB('db.json', indent=4)
db_log = TinyDB('db_log.json', indent=4)

# Rota para verificar a conexão do robô em relação ao botão de conexão
@verificacoes.route('/verificarConexaoBotao', methods=['GET'])
def verificarConexao():
    estado_conexao_robo = current_app.config['ESTADO_CONEXAO_ROBO']
    if estado_conexao_robo:
        return render_template('conexao_status.html', status="Conectado")
    else:
        return render_template('conexao_status.html', status="Desconectado")

# Rota para verificar a conexão do robô em relação a ações que dependem de conexão com o robô
@verificacoes.route('/verificarConexaoNavbar', methods=['GET'])
def verificarConexaoNavbar():
    estado_conexao_robo = current_app.config['ESTADO_CONEXAO_ROBO']
    if estado_conexao_robo:
        return render_template('movimentacao_navbar.html', status="Conectado")
    else:
        return render_template('movimentacao_navbar.html', status="Desconectado")
    
