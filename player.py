import os, socket, subprocess

sock = socket.socket()
host = '127.0.0.1'
port = 9999
sock.connect((host, port))

while True:
    try:
        dados = sock.recv(2048)
        print('\n================================================================================')
        print(str(dados, 'utf-8'),end='')
        print('\n================================================================================')
        resposta = ''
        while len(resposta) == 0:
            resposta = input("Comando: ")
        sock.send(str.encode(resposta))
    except KeyboardInterrupt:
        sock.close()
        print('Fim de jogo')
        break