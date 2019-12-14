import os, socket, subprocess

sock = socket.socket()
host = '127.0.0.1'
port = 9999
sock.connect((host, port))

while True:
    dados = sock.recv(2048)
    print(str(dados, 'utf-8'))
    resposta = input()
    sock.send(str.encode(resposta))

sock.close()
