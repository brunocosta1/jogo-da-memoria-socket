import pickle
import socket
import argparse
import random
import time
from typing import List, Tuple

def getArgs():
    parser = argparse.ArgumentParser(description='Servidor que vai esperar os jogadores')
    parser.add_argument('--numero', type=int, help='Indica o número de jogadores')
    parser.add_argument('--porta', type=int, help='Indica em que porta vai escutar')
    parser.add_argument('--host', type=str, help='Indica qual vai ser o host do server')
    parser.add_argument('--dimensao', type=int, help='Indica a dimensão do tabuleiro')
    return parser.parse_args()


# Função para fechar a conexão
def fechaConexao(users: List[socket.socket], server: socket.socket):
    for user in users:
        user.close()
    server.close()




# Conexão dos jogadores

def conexaoJogadores(HOST, PORT, numeroJogadores):
    print("SERVER STARTED")
    users: List[socket.socket] = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(numeroJogadores)
    while len(users) < numeroJogadores:
        client, address = server.accept()
        users.append(client)
        print(f"Número de jogadores conectados: {len(users)}")
        print("[CONNECTION]: ", address)
    print("Todos os jogadores se conectaram!")
    return users, server

def novoTabuleiro(dim):

    # Cria um tabuleiro vazio.
    tabuleiro = []
    for i in range(0, dim):

        linha = []
        for j in range(0, dim):

            linha.append(0)

        tabuleiro.append(linha)

    # Cria uma lista de todas as posicoes do tabuleiro. Util para
    # sortearmos posicoes aleatoriamente para as pecas.
    posicoesDisponiveis = []
    for i in range(0, dim):

        for j in range(0, dim):

            posicoesDisponiveis.append((i, j))

    # Varre todas as pecas que serao colocadas no 
    # tabuleiro e posiciona cada par de pecas iguais
    # em posicoes aleatorias.
    for j in range(0, dim // 2):
        for i in range(1, dim + 1):

            # Sorteio da posicao da segunda peca com valor 'i'
            maximo = len(posicoesDisponiveis)
            indiceAleatorio = random.randint(0, maximo - 1)
            rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

            tabuleiro[rI][rJ] = -i

            # Sorteio da posicao da segunda peca com valor 'i'
            maximo = len(posicoesDisponiveis)
            indiceAleatorio = random.randint(0, maximo - 1)
            rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

            tabuleiro[rI][rJ] = -i

    return tabuleiro

def novoPlacar(nJogadores):

    return [0] * nJogadores

def criaJogo(numeroJogadores):
    dim = 4
    totalDePares = dim ** 2 / 2
    tabuleiro = novoTabuleiro(dim)
    placar = novoPlacar(numeroJogadores)
    paresEncontrados = 0
    vez = 0
    dados = {
            "dimensao": dim,
            "numeroPares": totalDePares,
            "tabuleiro": tabuleiro,
            "placar": placar,
            "paresEncontrados": paresEncontrados,
            "vez": vez,
            "numeroJogadores": numeroJogadores
            }
    return dados

def enviaDadosJogo(jogo, users):
    print("Enviando dados do jogo e uma identificação para cada jogador...")
    i = 0
    for user in users:
        dados = pickle.dumps((jogo, i))
        user.send(dados)
        i += 1

def enviaDados(user, dado):
    dadoSerializado = pickle.dumps(dado)
    user.send(dadoSerializado)

def recebeDados(user):
    dadoSerializado = user.recv(1024)
    dado = pickle.loads(dadoSerializado)
    return dado


def abrePeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False
    elif tabuleiro[i][j] < 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        # Envia para o servidor
        return True

    return False

def recebeJogada(user: socket.socket, jogo):
    while True:
        coordenada1 = recebeDados(user)

        if coordenada1 == False:
            continue

        i1, j1 = coordenada1

        if abrePeca(jogo["tabuleiro"], i1, j1) == False:
            continue
        break

    while True:
        coordenada2 = recebeDados(user)

        if coordenada2 == False:
            continue

        i2, j2 = coordenada2
         
        if abrePeca(jogo["tabuleiro"], i2, j2) == False:
            continue
        break

    return coordenada1, coordenada2

def enviaMensagem(users, msg):
    msg = pickle.dumps(msg)
    for user in users:
        user.send(msg)

def distribuiJogada(users: List[socket.socket], jogada):
    jogadaSerializada = pickle.dumps(jogada)
    for user in users:
        user.send(jogadaSerializada)

def atualizaPlacar(jogo):
    jogo["placar"][jogo["vez"]] += 1

def removePeca(tabuleiro, i, j):
    if tabuleiro[i][j] == '-':
        return False
    else:
        tabuleiro[i][j] = '-'
        return True

def fechaPeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False
    elif tabuleiro[i][j] > 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True

    return False


def atualizaVez(jogo):
    jogo["vez"] = (jogo["vez"] + 1) % jogo["numeroJogadores"]

def validaJogada(jogo, jogada):
    coordenada1, coordenada2 = jogada
    x1, y1 = coordenada1
    x2, y2 = coordenada2

    if jogo["tabuleiro"][x1][y1] == jogo["tabuleiro"][x2][y2]:
        atualizaPlacar(jogo)
        jogo["paresEncontrados"] += 1
        removePeca(jogo["tabuleiro"], x1, y1)
        removePeca(jogo["tabuleiro"], x2, y2)
    else:
        fechaPeca(jogo["tabuleiro"], x1, y2)
        fechaPeca(jogo["tabuleiro"], x1, y2)
        atualizaVez(jogo)

def verificaJogada(tabuleiro, jogada):
    coordenada1, coordenada2 = jogada
    x1, y1 = coordenada1
    x2, y2 = coordenada2

    if tabuleiro[x1][y1] == tabuleiro[x2][y2]:
        return True
    else:
        return False

def enviaDadosParaTodos(users: List[socket.socket], dado):
    dado_serializado = pickle.dumps(dado)
    for user in users:
        user.send(dado_serializado)

def atualizaTabuleiro(tabuleiro, jogada):
    coordenada1, coordenada2 = jogada
    x1, y1 = coordenada1
    x2, y2 = coordenada2

    if tabuleiro[x1][y1] == '-':
        return False
    else:
        tabuleiro[x1][y1] = '-'

    if tabuleiro[x2][y2] == '-':
        return False
    else:
        tabuleiro[x2][y2] = '-'


def iniciaJogo2(jogo, users):
    while jogo["paresEncontrados"] < jogo["numeroPares"]:
        print("Aguardando coordenada 1...")
        coordenada1 = recebeDados(users[jogo["vez"]])
        print("Aguardando coordenada 2...")
        coordenada2 = recebeDados(users[jogo["vez"]])

        jogada = (coordenada1, coordenada2)
        validadeJogada = verificaJogada(jogo["tabuleiro"], jogada)

        enviaDadosParaTodos(users, (jogada, validadeJogada))
        if validadeJogada:
            atualizaTabuleiro(jogo, jogada)
            atualizaPlacar(jogo)
            jogo["paresEncontrados"] += 1
            time.sleep(5)
        else:
            jogo["vez"] = (jogo["vez"] + 1) % jogo["numeroJogadores"]
            time.sleep(3)

        enviaDadosParaTodos(users, jogo)

def main():
    args = getArgs()
    users, server = conexaoJogadores(args.host, args.porta, args.numero)

    try:
        jogo = criaJogo(args.numero)
        enviaDadosJogo(jogo, users)

        iniciaJogo2(jogo, users)

        fechaConexao(users, server)
    except:
        print("Saindo...")
        fechaConexao(users, server)

if __name__ == "__main__":
    main()
