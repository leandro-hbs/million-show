import socket, sys, threading, time
from random import randint

global RANKING, PERGUNTAS, RESPOSTAS, ALTERNATIVAS

RANKING = [('Leandro',1000000),('Norronha',5000)]
PERGUNTAS = [
'Sobre o protocolo DNS no modelo TCP/IP, é correto afirmar que: ',
'O protocolo de transmissão que permite trocas de arquivos grandes e permite também acessar remotamente sistemas de arquivos, diretamente entre computadores sem passar pela web, é chamado: ',
'O protocolo https é uma implementação do protocolo http sobre uma camada adicional de segurança que utiliza o protocolo:',
'O DHCP (Dynamic Host Configuration Protocol) é um protocolo: ',
'Dentre os protocolos que compreendem a camada de Aplicação do Modelo TCP/IP, encontram-se:',
'O Sistema de Nomes de Domínio (DNS) – Domain Name System – é uma parte fundamental da Internet. Este sistema é responsável pelos seguintes serviços, EXCETO:',
'A configuração automática de endereços IP e outras informações da rede nas estações de trabalho é provida por um servidor DHCP (Dynamic Host Configuration Protocol). Assinale a alternativa que NÃO corresponde a uma informação fornecida por este servidor',
'Seu gerente verificou uma irregularidade no tráfego HTTP e HTTPS em sua rede corporativa e solicita que estes serviços sejam bloqueados imediatamente através do sistema de firewall, sendo assim, as seguintes portas deverão ter o acesso bloqueado:',
'Qual é o protocolo de internet para transferência segura, com uso de certificado digital, utilizado em sites de compras eletrônicas?',
'Na Internet, para evitar que o tráfego de dados entre os usuários e seus servidores seja visualizado por terceiros, alguns sites, como os de bancos e de comércio eletrônico, utilizam em suas conexões o protocolo'
]
RESPOSTAS = ['B','B','A','C', 'C', 'C', 'B', 'A', 'B', 'C']
ALTERNATIVAS = [
'A) Utiliza somente UDP para resolução dos nomes\nB) Um resolver gerencia as buscas do cliente em um servidor DNS\nC) Um nome de domínio tem somente uma parte, chamada também de label\n',
'A) HTTP\nB) SMTP\nC) FTP\n',
'A) TLS\nB) ICMP\nC) NAT\n',
'A) Padrão da internet para o gerenciamento de dispositivos em redes IP\nB) Para operação de serviços de rede de forma segura que utiliza criptografia\nC) Que permite a atribuição manual e a atribuição automática de endereços IP\n',
'A) IP, TELNET, NFS\nB) ICMP, IP e DNS\nC) DHCP, DNS e SNMP\n',
'A) Tradução dos nomes dos hospedeiros para endereços IP\nB) Apelidos de hospedeiros\nC) Resolução ARP (Protocolo de Resolução de Endereços)',
'A) A máscara de sub-rede\nB) O endereço dos servidores Web\nC) O endereço dos servidores DNS',
'A) 80 e 443\nB) 8080 e 443\nC) 80 e 81',
'A) IMAP\nB) HTTPS\nC) SNMP',
'A) FTP\nB) SMTP\nC) HTTPS'
]

def interface(nickname, pontuacao, id, pular, chances):
    mensagem = '======================================================='
    mensagem = mensagem + '\n' + 'Jogador: ' + nickname + '\t\tPontuação: ' + str(pontuacao)
    mensagem = mensagem + '\t\tPular: ' + str(pular) + '\t\tVidas: ' + str(chances)
    mensagem = mensagem + '\n' + PERGUNTAS[id]
    mensagem = mensagem + '\n' + ALTERNATIVAS[id]
    return mensagem

def resultado(nickname, pontuacao, situacao):
    mensagem = '======================================================='
    mensagem = mensagem + '\n' + situacao 
    mensagem = mensagem + '\n\n' + 'Nick: ' + nickname + '\t\tPontuação: ' + str(pontuacao)
    mensagem = mensagem + '\n' + '======================================================='
    mensagem = mensagem + '\n' + 'RANKING ATUAL'
    mensagem = mensagem + '\n' + '======================================================='
    for i in range(len(RANKING)):
        mensagem = mensagem + '\n' + 'Posição ' + str(i)
        mensagem = mensagem + '\t\tNome: ' + RANKING[i][0] + '\t\tPontuacao: ' + str(RANKING[i][1])
    return mensagem

class MultiplasExecucoes(threading.Thread):
    def __init__(self, conexao, endereco):
        self.conexao = conexao
        self.endereco = endereco
        threading.Thread.__init__(self)

    def run(self):
        mensagem = '======================================================='
        mensagem = mensagem + '\n' + 'Bem vindo ao Show do Milhão'
        mensagem = mensagem + '\n' + 'Insira seu nickname: '
        self.conexao.send(str.encode(mensagem))
        nickname = self.conexao.recv(1024)
        self.nickname = str(nickname, 'utf-8')
        self.pontuacao = 0
        self.pular = 3
        self.id = 0
        chances = 3
        cont = 0
        acumulador = 1
        marcador = []
        while chances > 0 and cont < 10:
            while self.id in marcador:
                self.id = randint(0,9)
            marcador.append(self.id)
            mensagem = interface(self.nickname, self.pontuacao, self.id, self.pular, chances)
            self.conexao.send(str.encode(mensagem))
            resposta = str(self.conexao.recv(1024), 'utf-8')
            if resposta.upper() == 'PULAR':
                cont += 1
                if self.pular == 0:
                    chances -= 1
                    continue
                else:
                    self.pular -= 1
                    continue
            elif resposta.upper() == RESPOSTAS[self.id]:
                self.pontuacao += 1000 * acumulador
                acumulador += 1
            else:
                chances -= 1
                acumulador = 1
            cont += 1

        RANKING.append((self.nickname,self.pontuacao))

        if chances == 0:
            self.pontuacao = 0
            situacao = 'Você foi eliminado... mt noob'
        elif chances > 0:
            situacao = 'Você ganhou!!!!'
        mensagem = resultado(self.nickname,self.pontuacao,situacao)
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