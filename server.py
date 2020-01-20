import socket, sys, threading, time
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

def resultado(nickname, pontuacao, adicional):
    RANKING.append((nickname,pontuacao))
    RANKING.sort(key=lambda x: x[1],reverse=True)
    mensagem = adicional
    mensagem += '\n================================================================================'
    mensagem += '\nNick: ' + nickname + '\t\tPontuação: ' + str(pontuacao)
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
                        mensagem = 'Jogador ' + player.nickname + ' foi cadastrado com sucesso'
                        self.conexao.send(str.encode(mensagem))
                        break
                    else:
                        mensagem = 'Infelizmente o nome escolhido já está em uso, por favor tente outro nome'
                        self.conexao.send(str.encode(mensagem))
                        continue
                else:
                    mensagem = 'Sintaxe inválida, por favor siga o modelo abaixo:'
                    mensagem += '\nnickname xxxx'
                    self.conexao.send(str.encode(mensagem))
            else:
                mensagem = 'Por favor defina seu nickname para que o jogo possa iniciar'
                mensagem += '\nSintaxe: nickname xxxx'
                self.conexao.send(str.encode(mensagem))

        while player.round < 15:
            comando = str(self.conexao.recv(1024), 'utf-8').split()

            if comando[0].upper() in COMANDOS:
                if comando[0].upper() == "QUESTION":
                    mensagem = PERGUNTAS[self.id]
                    mensagem += '\n' + ALTERNATIVAS[self.id]
                    self.conexao.send(str.encode(mensagem))

                elif comando[0].upper() == "ANSWER":
                    if len(comando) > 1:
                        if comando[1].upper() == RESPOSTAS[self.id]:
                            mensagem = 'Resposta Correta' + '\nVoce recebeu: '
                            if player.round < 5:
                                player.score += 1000 * (player.strikes + 1)
                                mensagem += str(1000 * (player.strikes + 1)) + ' pontos' + '\nVocê tem ' + str(player.score) + ' pontos'
                                player.strikes += 1
                            elif player.round < 10 and player.round > 4:
                                player.score += 10000 * (player.strikes + 1)
                                mensagem += str(10000 * (player.strikes + 1)) + ' pontos'  + '\nVocê tem ' + str(player.score) + ' pontos'
                                player.strikes += 1
                            else:
                                player.score += 100000 * (player.strikes + 1)
                                mensagem += str(100000 * (player.strikes + 1)) + ' pontos'  + '\nVocê tem ' + str(player.score) + ' pontos'
                                player.strikes += 1
                            player.hits += 1
                        else:
                            mensagem = 'Resposta Incorreta' + '\nA resposta certa era a letra: ' + RESPOSTAS[self.id]
                            player.lifes -= 1
                            if player.lifes == 0:
                                mensagem = 'Infelizmente suas vidas acabaram, mas parabéns por ter chegado até aqui' + '\nA resposta certa era a letra: ' + RESPOSTAS[self.id]
                                mensagem = resultado(player.nickname,player.score,mensagem)
                                self.conexao.send(str.encode(mensagem))
                                self.conexao.close()
                                break
                            player.strikes = 0
                    else:
                        mensagem = 'Sintaxe invalida, por favor siga o modelo abaixo:'
                        mensagem += '\nanswer xxxx'
                    self.marcador.append(self.id)
                    player.round += 1
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
                        mensagem = 'Voce pulou essa questão e agora tem ' + str(player.skip) + ' pular'
                    elif player.skip == 1:
                        player.skip -= 1
                        COMANDOS.remove("SKIP")
                        mensagem = 'Você pulou essa questão, mas cuidado, pois daqui em diante não haverá mais essa opção'
                    self.marcador.append(self.id)
                    while self.id in self.marcador and len(self.marcador) < 15:
                        if player.round < 5:
                            self.id = randint(0,4)
                        elif player.round < 10 and player.round > 4:
                            self.id = randint(5,9)
                        else:
                            self.id = randint(10,14)
                    player.round += 1
                    self.conexao.send(str.encode(mensagem))

                elif comando[0].upper() == "RANKING":
                    mensagem = 'Uma pena que tenha desistido tão cedo, tinha muita fé em você'
                    mensagem = resultado(player.nickname,player.score,mensagem)
                    self.conexao.send(str.encode(mensagem))
                    self.conexao.close()
                    break

                elif comando[0].upper() == "HELP":
                    mensagem = 'O jogo do milhão consiste em um jogo de perguntas e respostas'
                    mensagem += '\n\nNele está contido 3 niveis:'
                    mensagem += '\nO primeiro tem questões relacionadas aos protocolos de aplicação estudados'
                    mensagem += '\nO segundo tem questões relacionadas a biologia humana em geral'
                    mensagem += '\nO terceiro tem questões relacionadas ao raciocínio lógico'
                    mensagem += '\n\nO jogador tem 6 comandos, são eles:'
                    mensagem += '\nNICKNAME - usado para definir seu nick. Exemplo: nickname leandro'
                    mensagem += '\nQUESTION - usado para requesitar uma questão do sistema. Exemplo: question'
                    mensagem += '\nSKIP - usado para pular a questão atual. Exemplo: skip'
                    mensagem += '\nANSWER - usado para responder a questão atual. Exemplo: answer c'
                    mensagem += '\nRANKING - usado para encerrar o jogo e verificar sua pontuação. Exemplo: ranking'
                    mensagem += '\nLembre-se, você tem apenas 3 vidas e 3 pular'
                    mensagem += '\nBoa sorte e Bom jogo ;D'
                    self.conexao.send(str.encode(mensagem))
                
                elif comando[0].upper() == "INFORMATION":
                    mensagem = informacao(player)
                    self.conexao.send(str.encode(mensagem))


            else:
                mensagem = 'Comando não identificado, por favor verifique se a ortografia ou sintaxe está como os comandos abaixo: '
                for i in range(len(COMANDOS)):
                    mensagem += '\n' + COMANDOS[i]
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