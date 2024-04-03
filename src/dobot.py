import pydobot
from serial.tools import list_ports
import time
from tinydb import TinyDB, Query

# Classe do Dobot
class Dobot:
    def __init__(self) -> None:
        pass

    def listar_portas(self):

        portas_disponiveis = list_ports.comports()

        portas = [x.device for x in portas_disponiveis]

        return portas

    # Função para conectar ao dobot
    def conectar_dobot(self, porta):
        try:
            available_ports = list_ports.comports()
            print(f'available ports: {[x.device for x in available_ports]}')
            port = available_ports[0].device

            self.device = pydobot.Dobot(port=port, verbose=False)

            return True
        except Exception as e:
            print("Falha ao conectar ao robô:" + str({e}))
            return False
    
    # Função de conexão com banco de dados TinyDB
    def conectar_DB(self):
        db = TinyDB('dbDobot.json', indent=4)
        return db

    # Função para desconectar do banco de dados
    def desconectar_DB(self, db):
        db.close()

    # Função para salvar a posição atual do dobot
    def salvar_posicao(self, nomePosicao):
        # Instanciar o banco de dados
        db = self.conectar_DB()
        if self.device:
            try:
                # Pegar a posição atual do dobot e inserir no banco de dados
                posicao = self.device.pose()

                db.insert({'nomePosicao': nomePosicao, 'x': posicao[0], 'y': posicao[1], 'z': posicao[2], 'r': posicao[3]})
                print("Posição salva com sucesso.")
            except Exception as e:
                print("Erro ao salvar posição:" + str({e}))
        else:
            print('Conecte ao dobot primeiro.')
    
    # Função para desconectar do dobot
    def desconectar_robot(self):
        if self.device:
            try:
                self.device.close()
                print("Disconectado do dobot com sucesso.")
            except Exception as e:
                print("Erro ao desconectar:" + str({e}))
        else:
            print("Não há conexão com o dobot.")

    # Função para mover o dobot para uma posição salva
    def mover_para_ponto(self, nomePosicao):
        if self.device:
            try:
                # Conectar ao banco de dados
                db = self.conectar_DB()
                # Instanciar a Query
                Posicao = Query()
                nome_da_posicao = nomePosicao['Pontos'] if isinstance(nomePosicao, dict) else nomePosicao
                posicao = db.search(Posicao.nomePosicao == nome_da_posicao)  # Busca no banco de dados o nome itens com o nome da posição
                if posicao:
                    x = posicao[0]['x']
                    y = posicao[0]['y']
                    z = posicao[0]['z']
                    r = posicao[0]['r']
                    # Mover o dobot para a posição
                    self.device.move_to(x, y, z, r, wait=True)
                else:
                    print("Posição não encontrada.")
                self.desconectar_DB(db)
            except Exception as e:
                print("Erro ao mover para a posição:" + str(e))  # Melhor formatação da mensagem de erro
        else:
            print("Conecte ao dobot primeiro.")

    # Função para executar uma sequencia de movimentos
    def sequencia_de_movimentos(self, comandos):
        print(comandos)
        if self.device:
            try:
                # Exemplo de comados
                # comandos = [
                #     {'tipo': 'ponto', 'nome': 'ponto1'},
                #     {'tipo': 'atuador', 'estado': 'on'}
                #     ]
                
                # Interar nos comandos escolhidos
                for comando in comandos:
                    # Executar cada tipo de comando
                    if comando['tipo'] == 'ponto':
                        print(comando['nome'])
                        self.mover_para_ponto(comando['nome'])
                    elif comando['tipo'] == 'atuador':
                        if comando['estado'] == 'On':
                            self.device.suck(True)
                        else:
                            self.device.suck(False)
            except Exception as e:
                print("Erro ao mover para a posição:" + str({e}))
        else:
            print("Conecte ao dobot primeiro.")

    # Função para mover o dobot para uma posição especifica
    def mover_para(self, x, y, z, r):
        if self.device:
            try:
                self.device.move_to(x, y, z, r, wait=True)

                print(f"Braço robotico movido para: ({x}, {y}, {z}, {r})")

                return True
            except Exception as e:
                print("Erro ao mover o braço" + str({e}))

                return False
        else:
            print("Conecte ao dobot primeiro.")

    # Controle de movimentação livre
    def movimentacao_livre(self, direcao, taxa):
        if self.device:
            # POssibilidade de mover o dobot em qualquer eixo
            posicaoAtual = self.device.pose()
            
            try:
                # Mover o dobot no eixo escolhido e a taxa de movimentação
                if direcao == "X":
                    self.device.move_to(posicaoAtual[0]+taxa, posicaoAtual[1], posicaoAtual[2], posicaoAtual[3], wait=True)
                elif direcao == "Y":
                    self.device.move_to(posicaoAtual[0], posicaoAtual[1]+taxa, posicaoAtual[2], posicaoAtual[3], wait=True)
                elif direcao == "Z":
                    self.device.move_to(posicaoAtual[0], posicaoAtual[1], posicaoAtual[2]+taxa, posicaoAtual[3], wait=True)
                elif direcao == "R":
                    self.device.move_to(posicaoAtual[0], posicaoAtual[1], posicaoAtual[2], posicaoAtual[3]+taxa, wait=True)
                elif direcao == 'Sair':
                    print("Saindo da movimentação livre.")
            except Exception as e:
                print("Erro ao mover o dobot:" + str({e}))
        else:
            print("Conecte ao dobot primeiro.")

    # Função para controlar o atuador
    def atuador(self, acao, estado):
        # Ligar ou desligar o suck ou grip
        if self.device:
            try:
                if acao == "suck":
                    if estado == "On":
                        self.device.suck(True)
                    else:
                        self.device.suck(False)
                elif acao == "grip":
                    if estado == "On":
                        self.device.grab(True)
                    else:
                        self.device.grab(False)
            except Exception as e:
                print("Erro na ação:" + str({e}))


# # Inicializar uma instacncia da classe dobot
# meuRobo = Dobot()
# meuRobo.CLI()