import socket, sys, threading, time
from random import randint
from database import *

class Jogador:
    def __init__(self, nickname):
        self.nickname = nickname
        self.pontuacao = 0
        self.acertos = 0
        self.pular = 3
        self.vidas = 3
        self.strikes = 0
        self.rodada = 0

def interface(DADOS, id):
    mensagem = '\n================================================================================'
    mensagem = mensagem + '\nJogador: ' + DADOS.nickname
    mensagem = mensagem + '\nPontuação:\t' + str(DADOS.pontuacao) + '\t\tRodada:\t\t' + str(DADOS.rodada+1)
    mensagem = mensagem + '\nPular:\t\t' + str(DADOS.pular) + '\t\tVidas:\t\t' + str(DADOS.vidas)
    mensagem = mensagem + '\nAcertos:\t' + str(DADOS.acertos) + '\t\tStrikes:\t' + str(DADOS.strikes)
    mensagem = mensagem + '\n\n' + PERGUNTAS[id]
    mensagem = mensagem + '\n' + ALTERNATIVAS[id]
    return mensagem

def resultado(nickname, pontuacao, situacao):
    mensagem = '\n================================================================================'
    mensagem = mensagem + '\n' + situacao
    mensagem = mensagem + '\n================================================================================'
    mensagem = mensagem + '\nNick: ' + nickname + '\t\tPontuação: ' + str(pontuacao)
    mensagem = mensagem + '\n================================================================================'
    mensagem = mensagem + '\nRANKING ATUAL'
    mensagem = mensagem + '\n================================================================================'
    for i in range(len(RANKING)):
        mensagem = mensagem + '\nPosição ' + str(i+1)
        mensagem = mensagem + '\t\tNome: ' + RANKING[i][0] + '\t\tPontuacao: ' + str(RANKING[i][1])
    mensagem = mensagem + '\n================================================================================'
    return mensagem

class MultiplasExecucoes(threading.Thread):
    def __init__(self, conexao, endereco):
        self.conexao = conexao
        self.endereco = endereco
        threading.Thread.__init__(self)

    def run(self):
        mensagem = '\n================================================================================'
        mensagem = mensagem + '\nBem vindo ao Show do Milhão'
        mensagem = mensagem + '\nInsira seu nickname: '
        self.conexao.send(str.encode(mensagem))
        nickname = self.conexao.recv(1024)
        DADOS = Jogador(str(nickname, 'utf-8'))
        self.id = 0
        self.marcador = []
        while DADOS.vidas > 0 and DADOS.rodada < 15:
            if DADOS.rodada == 5 or DADOS.rodada == 10:
                DADOS.strikes = 0
            while self.id in self.marcador:
                if DADOS.rodada < 5:
                    self.id = randint(0,4)
                elif DADOS.rodada < 10 and DADOS.rodada > 4:
                    self.id = randint(5,9)
                else:
                    self.id = randint(10,14)
            self.marcador.append(self.id)
            mensagem = interface(DADOS, self.id)
            self.conexao.send(str.encode(mensagem))
            resposta = str(self.conexao.recv(1024), 'utf-8')
            DADOS.rodada += 1
            if resposta.upper() == 'PULAR':
                if DADOS.pular == 0:
                    DADOS.vidas -= 1
                    DADOS.pontuacao = 0
                    DADOS.strikes = 0
                    continue
                else:
                    DADOS.pular -= 1
                    continue
            elif resposta.upper() == RESPOSTAS[self.id]:
                if DADOS.rodada < 5:
                    DADOS.pontuacao += 1000 * (DADOS.strikes + 1)
                    DADOS.strikes += 1
                elif DADOS.rodada < 10 and DADOS.rodada > 4:
                    DADOS.pontuacao += 10000 * (DADOS.strikes + 1)
                    DADOS.strikes += 1
                else:
                    DADOS.pontuacao += 100000 * (DADOS.strikes + 1)
                    DADOS.strikes += 1
                DADOS.acertos += 1
            else:
                DADOS.vidas -= 1
                DADOS.pontuacao = int(DADOS.pontuacao/2)
                DADOS.strikes = 0

        RANKING.append((DADOS.nickname,int(DADOS.pontuacao)))
        RANKING.sort(key=lambda x: x[1],reverse=True)

        if DADOS.vidas == 0:
            situacao = 'Você foi eliminado'
        elif DADOS.vidas > 0:
            situacao = 'Parabéns ' + str(DADOS.nickname) + ', Você sobreviveu e agora irá ter seu nome lembrado no Ranking!!!!'
        mensagem = resultado(DADOS.nickname,int(DADOS.pontuacao),situacao)
        print(mensagem)
        self.conexao.send(str.encode(mensagem))
        self.conexao.close()

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
            conexao.setblocking(1)
            print("\nConexão foi estabelecida com: " + endereco[0])
            thread = MultiplasExecucoes(conexao, endereco)
            thread.start()

server = MultiServer()
server.aceita_conexoes()