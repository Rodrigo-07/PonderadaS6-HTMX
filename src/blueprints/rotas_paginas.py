from flask import Blueprint, render_template, request, current_app
from tinydb import TinyDB, Query

# Blueprint para rotas das páginas
rotas_blueprint = Blueprint('rotas_paginas', __name__)

db= TinyDB('db.json', indent=4)
db_log = TinyDB('db_log.json', indent=4)

# Rota para a página inicial
@rotas_blueprint.route("/", methods=['GET'])
def index():
    return render_template('index.html')

# Rota o conteúdo da página inicial
@rotas_blueprint.route("/home_content", methods=['GET'])
def home_content():
    return render_template('home_content.html')

# Rota para a página de mover para uma posição específica
@rotas_blueprint.route('/mov_posicao_espesifica')
def mov_posicao_espesifica():
    return render_template('movi_posicao_especifica.html')

# Rota para a página de mover para uma posição salva
@rotas_blueprint.route('/salvar_posicao')
def salvar_posicao():
    return render_template('salvar_posicoes.html')

# Rota para a página de mover para uma posição salva baseada na posição atual do Dobot
@rotas_blueprint.route('/salvar_posicao_atual')
def salvar_posicao_atual():
    return render_template('salvar_posicao_atual.html')

# Rota para a página de listar posições salvas
@rotas_blueprint.route('/listar_posicoes', methods=['GET'])
def listarPosicoes():
    posicoes = db.all()
    return render_template('movi_posicao_salva.html', posicoes=posicoes)

# Rota para a página de logs
@rotas_blueprint.route('/logs', methods=['GET'])
def logs():
    logs = db_log.all()

    logs.reverse()
    return render_template('log.html', logs=logs)

# Rota para abrir o modal de atualizar uma posição salva
@rotas_blueprint.route('/caminho_para_abrir_modal')
def abrir_modal():
    return render_template('atualizar_posicao_salva.html', active=True)

# Rota para abrir o modal de atualizar uma posição salva
@rotas_blueprint.route('/atualizar_posicao_salva_modal/<nome_posicao>', methods=['GET'])
def atualizarPosicaoSalvaModal(nome_posicao):
    posicao = db.search(Query().nome == nome_posicao)[0]


    return render_template('atualizar_posicao_salva.html', active=True, nome=nome_posicao, x=posicao['x'], y=posicao['y'], z=posicao['z'], r=posicao['r'])

# Rota para a página de movimentação livre
@rotas_blueprint.route('/movimentacao_livre')
def movimentacaoLivre():
    return render_template('movimentacao_livre.html')
