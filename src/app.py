from flask import Flask
from flask_cors import CORS
from dobot import Dobot

# Importe dos  Blueprints
from blueprints.rotas_paginas import rotas_blueprint
from blueprints.verificacoes import verificacoes
from blueprints.conexoes import conexoes
from blueprints.movimentacoes import movimentacoes
from blueprints.edicoes_posicoes import edicoes_posicoes
from blueprints.atuador import atuador_blueprint

# Factory de criação do app
def create_app():
    # Instancia do Flask
    app = Flask(__name__)

    # Variavel global
    app.config['ESTADO_CONEXAO_ROBO'] = False

    # Instancia do Dobot
    dobot = Dobot()
    # Adiciono o Dobot ao app para poder acessar em qualquer lugar
    app.dobot = dobot

    # Registro seus Blueprints
    app.register_blueprint(rotas_blueprint)
    app.register_blueprint(verificacoes)
    app.register_blueprint(conexoes)
    app.register_blueprint(movimentacoes)
    app.register_blueprint(edicoes_posicoes)
    app.register_blueprint(atuador_blueprint)
    
    # Habilitar o CORS
    CORS(app)

    return app


# Instancia do app
app = create_app()

# Rodar o app
if __name__ == '__main__':
    app.run()