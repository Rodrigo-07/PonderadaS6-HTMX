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
    def conectar_dobot(self):
        try:
            available_ports = list_ports.comports()
            print(f'available ports: {[x.device for x in available_ports]}')
            port = available_ports[2].device

            self.device = pydobot.Dobot(port=port, verbose=True)

            return True
        except Exception as e:
            print("Falha ao conectar ao robô:" + str({e}))
            return False
    
    def obter_posicao(self):
        if self.device:
            posicao = self.device.pose()
            print(f"Posição atual do dobot: {posicao}")
            return posicao
        else:
            print("Conecte ao dobot primeiro.")
    
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