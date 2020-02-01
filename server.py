import socket, threading
from random import randint
from database import *

class Jogador:
    def __init__(self, nickname):
        self.nickname = nickname
        self.score = 0
        self.hits = 0
        self.skip = 3
        self.lifes = 3
        self.strikes = 0
        self.round = 0

def informacao(player):
    mensagem = 'Jogador: ' + player.nickname
    mensagem += '\nPontuação:\t' + str(player.score) + '\t\tRodada:\t\t' + str(player.round+1)
    mensagem += '\nPular:\t\t' + str(player.skip) + '\t\tVidas:\t\t' + str(player.lifes)
    mensagem += '\nAcertos:\t' + str(player.hits) + '\t\tStrikes:\t' + str(player.strikes)
    return mensagem

def resultado(nickname, score, add):
    RANKING.append((nickname,score))
    RANKING.sort(key=lambda x: x[1],reverse=True)
    mensagem = add
    mensagem += '\n================================================================================'
    mensagem += '\nNick: ' + nickname + '\t\tPontuação: ' + str(score)
    mensagem += '\n================================================================================'
    mensagem += '\nRANKING ATUAL'
    mensagem += '\n================================================================================'
    for i in range(len(RANKING)):
        mensagem += '\nPosição ' + str(i+1)
        mensagem += '\t\tNome: ' + RANKING[i][0] + '\t\tPontuacao: ' + str(RANKING[i][1])
    return mensagem

class MultiplasExecucoes(threading.Thread):
    def __init__(self, conexao, endereco, conexoes):
        self.conexao = conexao
        self.endereco = endereco
        self.conexoes = conexoes
        self.comandos = ['QUESTION','HELP','SKIP','ANSWER','QUIT','INFORMATION']
        self.id = randint(0,4)
        self.marcador = []
        threading.Thread.__init__(self)

    def run(self):
        mensagem = 'Bem vindo ao Show do Milhão'
        self.conexao.send(str.encode(mensagem))

        while True:
            comando = str(self.conexao.recv(1024), 'utf-8').split()
            if comando[0].upper() == "NICKNAME":
                if len(comando) > 1:
                    auxiliar = 0
                    for i in range(len(RANKING)):
                        if RANKING[i][0] == comando[1]:
                            auxiliar = 1
                    if auxiliar == 0:
                        player = Jogador(comando[1])
                        mensagem = MENSAGENS[601]
                        self.conexao.send(str.encode(mensagem))
                        break
                    else:
                        mensagem = MENSAGENS[602]
                        self.conexao.send(str.encode(mensagem))
                        continue
                else:
                    mensagem = MENSAGENS[603]
                    self.conexao.send(str.encode(mensagem))
            else:
                mensagem = MENSAGENS[604]
                self.conexao.send(str.encode(mensagem))

        while True:
            comando = str(self.conexao.recv(1024), 'utf-8').split()

            if comando[0].upper() in self.comandos:
                if comando[0].upper() == "QUESTION":
                    mensagem = PERGUNTAS[self.id]
                    mensagem += '\n' + ALTERNATIVAS[self.id]
                    self.conexao.send(str.encode(mensagem))

                elif comando[0].upper() == "ANSWER":
                    if len(comando) > 1:
                        if comando[1].upper() == RESPOSTAS[self.id]:
                            mensagem = MENSAGENS[605]
                            if player.round < 5:
                                player.score += 1000 * (player.strikes + 1)
                                mensagem += '\nVocê recebeu: ' + str(1000 * (player.strikes + 1)) + ' pontos' + '\nVocê tem ' + str(player.score) + ' pontos'
                                player.strikes += 1
                            elif player.round < 10 and player.round > 4:
                                player.score += 10000 * (player.strikes + 1)
                                mensagem += '\nVocê recebeu: ' + str(10000 * (player.strikes + 1)) + ' pontos'  + '\nVocê tem ' + str(player.score) + ' pontos'
                                player.strikes += 1
                            else:
                                player.score += 100000 * (player.strikes + 1)
                                mensagem += '\nVocê recebeu: ' + str(100000 * (player.strikes + 1)) + ' pontos'  + '\nVocê tem ' + str(player.score) + ' pontos'
                                player.strikes += 1
                            if player.round == 5 or player.round == 10:
                                player.strikes = 0
                            player.hits += 1
                        else:
                            mensagem = MENSAGENS[606]
                            player.lifes -= 1
                            if player.lifes == 0:
                                mensagem = MENSAGENS[608]
                                mensagem = resultado(player.nickname,player.score,mensagem)
                                self.conexao.send(str.encode(mensagem))
                                self.conexao.close()
                                break
                            player.strikes = 0
                    else:
                        mensagem = MENSAGENS[603]
                    self.marcador.append(self.id)
                    player.round += 1
                    if player.round == 14 and player.lifes > 0:
                        mensagem = MENSAGENS[609]
                        mensagem = resultado(player.nickname,player.score,mensagem)
                        self.conexao.send(str.encode(mensagem))
                        self.conexao.close()
                        break
                    while self.id in self.marcador and len(self.marcador) < 15:
                        if player.round < 5:
                            self.id = randint(0,4)
                        elif player.round < 10 and player.round > 4:
                            self.id = randint(5,9)
                        else:
                            self.id = randint(10,14)
                    self.conexao.send(str.encode(mensagem))

                elif comando[0].upper() == "SKIP":
                    if player.skip > 1:
                        player.skip -= 1
                        mensagem = MENSAGENS[607]
                    elif player.skip == 1:
                        player.skip -= 1
                        self.comandos.remove("SKIP")
                        mensagem = MENSAGENS[607]
                    self.marcador.append(self.id)
                    player.round += 1
                    if player.round == 14 and player.lifes > 0:
                        mensagem = MENSAGENS[609]
                        mensagem = resultado(player.nickname,player.score,mensagem)
                        self.conexao.send(str.encode(mensagem))
                        self.conexao.close()
                        break
                    while self.id in self.marcador and len(self.marcador) < 15:
                        if player.round < 5:
                            self.id = randint(0,4)
                        elif player.round < 10 and player.round > 4:
                            self.id = randint(5,9)
                        else:
                            self.id = randint(10,14)
                    self.conexao.send(str.encode(mensagem))

                elif comando[0].upper() == "QUIT":
                    mensagem = MENSAGENS[608]
                    mensagem = resultado(player.nickname,player.score,mensagem)
                    self.conexao.send(str.encode(mensagem))
                    self.conexao.close()
                    break

                elif comando[0].upper() == "HELP":
                    mensagem = 'O jogo do milhão consiste em um jogo de perguntas e respostas'
                    mensagem += '\n\nNele está contido 3 níveis:'
                    mensagem += '\nO primeiro tem questões relacionadas aos protocolos de aplicação estudados'
                    mensagem += '\nO segundo tem questões relacionadas a biologia humana em geral'
                    mensagem += '\nO terceiro tem questões relacionadas ao raciocínio lógico'
                    mensagem += '\n\nO jogador tem 6 comandos, são eles:'
                    mensagem += '\nNICKNAME - usado para definir seu nick. Exemplo: nickname leandro'
                    mensagem += '\nINFORMATION - usado para mostrar as informações atuais. Exemplo: information'
                    mensagem += '\nQUESTION - usado para requesitar uma questão do sistema. Exemplo: question'
                    mensagem += '\nSKIP - usado para pular a questão atual. Exemplo: skip'
                    mensagem += '\nANSWER - usado para responder a questão atual. Exemplo: answer c'
                    mensagem += '\nQUIT - usado para encerrar o jogo e verificar sua pontuação. Exemplo: quit'
                    mensagem += '\nLembre-se, você tem apenas 3 vidas e 3 pular'
                    mensagem += '\nBoa sorte e Bom jogo'
                    self.conexao.send(str.encode(mensagem))
                
                elif comando[0].upper() == "INFORMATION":
                    mensagem = informacao(player)
                    self.conexao.send(str.encode(mensagem))

            else:
                mensagem = MENSAGENS[604] + '\nCOMANDOS:'
                for i in range(len(self.comandos)):
                    mensagem += '\n' + self.comandos[i]
                self.conexao.send(str.encode(mensagem))

class MultiServer:
    def __init__(self):
        try:
            self.host = '0.0.0.0'
            self.port = 9999
            self.conexoes = []
            self.enderecos = []
            self.sock = socket.socket()
            print ("Conectando a porta: " + str(self.port))
            self.sock.bind((self.host,self.port))
            self.sock.listen(5)
        except socket.error as msg:
            print ("Erro de criação de socket: " + str(msg))

    def aceita_conexoes(self):
        while True:
            conexao, endereco = self.sock.accept()
            self.conexoes.append(conexao)
            conexao.setblocking(1)
            print("\nConexão foi estabelecida com: " + endereco[0])
            thread = MultiplasExecucoes(conexao, endereco, self.conexoes)
            thread.start()

server = MultiServer()
server.aceita_conexoes()