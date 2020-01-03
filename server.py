import socket, sys, threading, time
from random import randint

global RANKING, PERGUNTAS, RESPOSTAS, ALTERNATIVAS

RANKING = [('Leandro',1605000),('Noronha',1000000)]
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
'Na Internet, para evitar que o tráfego de dados entre os usuários e seus servidores seja visualizado por terceiros, alguns sites, como os de bancos e de comércio eletrônico, utilizam em suas conexões o protocolo',
'Qual estrutura no globo ocular responsável por transformar a luz em impulso elétrico para o cérebro?',
'Qual estrutura do ouvido interno é responsável por transformar impulsos de pressão em impulsos elétricos para o cérebro?',
'A paixão (um estado "hipermotivacional" de demência temporária com duração entre 12-24 meses) do ponto de vista cerebral tem como uma caracteristica marcante: ',
'O que ocorre no cérebro ao ingerirmos alcool?',
'É um efeito e um causa da febre, EXCETO.',
'"A vida deve estar em harmonia com o cosmos e maximizando suas virtudes e talentos", "Ame o mundo como ele é e dispense ideais","Todos temos uma potência, uma energia vital que oscila, felicidade é o ganho de potência", esses conceitos para felicidade são de, respectivamente.',
'"Aja de forma que qualquer pessoa no seu lugar possa fazer exatamente o que você está fazendo", esta frase define:',
'Em qual ordem desenvolvemos os 5 sentidos durante a fecundação?',
'Como o cérebro armazena informações?',
'A afirmação "1 = 0.99999.." é:'
]
RESPOSTAS = ['B','B','A','C','C','C','B','A','B','C','A','B','B','C','B','A','B','A','C','B']
ALTERNATIVAS = [
'A) Utiliza somente UDP para resolução dos nomes\nB) Um resolver gerencia as buscas do cliente em um servidor DNS\nC) Um nome de domínio tem somente uma parte, chamada também de label\n',
'A) HTTP\nB) SMTP\nC) FTP\n',
'A) TLS\nB) ICMP\nC) NAT\n',
'A) Padrão da internet para o gerenciamento de dispositivos em redes IP\nB) Para operação de serviços de rede de forma segura que utiliza criptografia\nC) Que permite a atribuição manual e a atribuição automática de endereços IP\n',
'A) IP, TELNET, NFS\nB) ICMP, IP e DNS\nC) DHCP, DNS e SNMP\n',
'A) Tradução dos nomes dos hospedeiros para endereços IP\nB) Apelidos de hospedeiros\nC) Resolução ARP (Protocolo de Resolução de Endereços)\n',
'A) A máscara de sub-rede\nB) O endereço dos servidores Web\nC) O endereço dos servidores DNS\n',
'A) 80 e 443\nB) 8080 e 443\nC) 80 e 81\n',
'A) IMAP\nB) HTTPS\nC) SNMP\n',
'A) FTP\nB) SMTP\nC) HTTPS\n',
'A) Bastonetes\nB) Retina\nC) Cristalino\n',
'A) Timpano\nB) Coclea\nC) Estribo\n',
'A) Diminuição da Dopamina (neurotransmissor que regula motivação e prazer)\nB) Diminuição da Serotonina (neurotransmissor que regula o sono e apetite)\nC) Diminuição do cortisol (hormonio que regula o estresse)\n',
'A) O alcool libera tóxinas responsáveis por um estímulo do sistema límbico\nB) O alcool estimula a parte emotiva mais primitiva do cérebro (libido)\nC) Os gases liberados na ingestão da bebida inibem o cortex frontal do cérebro\n',
'A) Vasoconstrição e protozoários\nB) Diminuição da temperatura corporal e vírus\nC) Tremores e bactérias\n',
'A) Aristoteles, Nietzche e Spinoza\nB) Nietzche, Aristoteles e Spinoza\nC) Spinoza, Nietzche e Aristoteles\n',
'A) O Amor Fati de Nietzche\nB) O Imperativo Categórico de Kant\nC) A Virtù de Maquiavél\n',
'A) Tato, Audição, Paladar, Olfato, Visão\nB) Audição, Tato, Olfato, Paladar e Visão\nC) Tato, Olfato, Audição, Paladar e Visão\n',
'A) Os neurônios guardam os impulsos nervosos e replicam quando necessário\nB) Os neurônios levam os impulsos pro subconsciente e quando necessário tornam consciente\nC) Os neurônios formam ligações entre si que será interpretada pelo cérebro quando necessário\n',
'A) Falsa, pois claramente são strings diferentes\nB) Verdadeira, pois a fração geratriz de 0.9999.. resulta em 1\nC) Falsa, pois 1 é igual a 1 e 0.999... é igual a 0.999...\n'
]

def interface(nickname, pontuacao, id, pular, chances, cont, acumulador, acertos):
    mensagem = '\n================================================================================'
    mensagem = mensagem + '\nJogador: ' + nickname
    mensagem = mensagem + '\nPontuação: ' + str(pontuacao) + '\t\tRodada: ' + str(cont)
    mensagem = mensagem + '\nPular: ' + str(pular) + '\t\t\tVidas: ' + str(chances)
    mensagem = mensagem + '\nAcertos: ' + str(acertos) + '\t\t\tStrikes: ' + str(acumulador)
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
    return mensagem

class MultiplasExecucoes(threading.Thread):
    def __init__(self, conexao, endereco):
        self.conexao = conexao
        self.endereco = endereco
        threading.Thread.__init__(self)

    def run(self):
        mensagem = '\n================================================================================'
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
        acumulador = 0
        marcador = []
        acertos = 0
        while chances > 0 and cont < 20:
                while self.id in marcador:
                    if cont < 10:
                        self.id = randint(0,9)
                    else:
                        self.id = randint(10,19)
                marcador.append(self.id)
                mensagem = interface(self.nickname, self.pontuacao, self.id, self.pular, chances, cont, acumulador, acertos)
                self.conexao.send(str.encode(mensagem))
                resposta = str(self.conexao.recv(1024), 'utf-8')
                if resposta.upper() == 'PULAR':
                    cont += 1
                    if self.pular == 0:
                        chances -= 1
                        acumulador = 0
                        continue
                    else:
                        self.pular -= 1
                        acumulador = 0
                        continue
                elif resposta.upper() == RESPOSTAS[self.id]:
                    if cont < 10:
                        self.pontuacao += 1000 * (acumulador + 1)
                        acumulador += 1
                    else:
                        self.pontuacao += 10000 * (acumulador + 1)
                        acumulador += 1
                    acertos += 1
                else:
                    chances -= 1
                    acumulador = 0
                cont += 1


        RANKING.append((self.nickname,self.pontuacao))
        RANKING.sort(key=lambda x: x[1],reverse=True)
        print(RANKING)

        if chances == 0:
            situacao = 'Você foi eliminado'
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