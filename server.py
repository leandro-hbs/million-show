import socket, sys, threading, time
from queue import Queue

threads = 2
tipo = [1, 2]
fila = Queue()
conexoes = []
enderecos = []

def cria_socket():
    try:
        global host
        global port
        global sock
        host = '0.0.0.0'
        port = 9999
        sock = socket.socket()
    except socket.error as msg:
        print ("Erro de criação de socket: " + str(msg))

def conecta_socket():
    try:
        global host
        global port
        global sock
        print ("Conectando a porta: " + str(port))
        sock.bind((host,port))
        sock.listen(5)
    except socket.error as msg:
        print ("Erro de conexão de socket: " + str(msg) + "\n" + "Reconectando...")

def aceita_conexoes():
    conexao, endereco = sock.accept()
    print("Conexão foi estabelecida\n" + "Ip: " + str(endereco[0]) + " Port: " + str(endereco[1]))
    conexao.send(str.encode('Porfavor insira seu nickname: '))

cria_socket()
conecta_socket()

#freaks me out é o q?