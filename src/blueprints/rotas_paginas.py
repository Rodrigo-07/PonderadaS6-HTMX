from flask import Blueprint, render_template, request, current_app
from dobot import Dobot  # Assumindo que você tenha uma classe separada para o Dobot
from tinydb import TinyDB, Query

rotas_blueprint = Blueprint('rotas_paginas', __name__)

db= TinyDB('db.json', indent=4)
db_log = TinyDB('db_log.json', indent=4)

@rotas_blueprint.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@rotas_blueprint.route("/home_content", methods=['GET'])
def home_content():
    return render_template('home_content.html')

@rotas_blueprint.route('/mov_posicao_espesifica')
def mov_posicao_espesifica():
    return render_template('movi_posicao_especifica.html')

@rotas_blueprint.route('/salvar_posicao')
def salvar_posicao():
    return render_template('salvar_posicoes.html')

@rotas_blueprint.route('/salvar_posicao_atual')
def salvar_posicao_atual():
    return render_template('salvar_posicao_atual.html')

@rotas_blueprint.route('/listar_posicoes', methods=['GET'])
def listarPosicoes():
    posicoes = db.all()
    return render_template('movi_posicao_salva.html', posicoes=posicoes)

@rotas_blueprint.route('/logs', methods=['GET'])
def logs():
    logs = db_log.all()

    logs.reverse()
    return render_template('log.html', logs=logs)

@rotas_blueprint.route('/caminho_para_abrir_modal')
def abrir_modal():
    return render_template('atualizar_posicao_salva.html', active=True)  # Onde 'modal.html' é o arquivo com o HTML do modal.

@rotas_blueprint.route('/atualizar_posicao_salva_modal/<nome_posicao>', methods=['GET'])
def atualizarPosicaoSalvaModal(nome_posicao):
    posicao = db.search(Query().nome == nome_posicao)[0]


    return render_template('atualizar_posicao_salva.html', active=True, nome=nome_posicao, x=posicao['x'], y=posicao['y'], z=posicao['z'], r=posicao['r'])

@rotas_blueprint.route('/movimentacao_livre')
def movimentacaoLivre():
    return render_template('movimentacao_livre.html')
