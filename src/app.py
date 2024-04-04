from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS
from tinydb import TinyDB, Query
from flask import session
import os
from dobot import Dobot
from datetime import datetime


def create_app():
    app = Flask(__name__)

    app.config['ESTADO_CONEXAO_ROBO'] = False

    dobot = Dobot()
    app.dobot = dobot

    from blueprints.rotas_paginas import rotas_blueprint
    from blueprints.verificacoes import verificacoes
    from blueprints.conexoes import conexoes
    from blueprints.movimentacoes import movimentacoes
    from blueprints.edicoes_posicoes import edicoes_posicoes
    from blueprints.atuador import atuador_blueprint

    app.register_blueprint(rotas_blueprint)
    app.register_blueprint(verificacoes)
    app.register_blueprint(conexoes)
    app.register_blueprint(movimentacoes)
    app.register_blueprint(edicoes_posicoes)
    app.register_blueprint(atuador_blueprint)
    
    CORS(app)

    # Registre seus Blueprints
    # app.register_blueprint(seu_blueprint)

    # Armazene a instância dobot no app para acesso posterior

    return app



app = create_app()

if __name__ == '__main__':
    app.run()