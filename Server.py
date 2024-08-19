import pickle
import socket
import argparse
import random
import sys
import time
from typing import List

def getArgs():
    parser = argparse.ArgumentParser(description='Servidor que vai esperar os jogadores')
    parser.add_argument('--numero', type=int, help='Indica o número de jogadores')
    parser.add_argument('--porta', type=int, help='Indica em que porta vai escutar')
    parser.add_argument('--dimensao', type=int, help='Indica a dimensão do tabuleiro')
    return parser.parse_args()

# Função para fechar a conexão
def fechaConexao(users: List[socket.socket], server: socket.socket):
    for user in users:
        user.close()
    server.close()

def conexaoJogadores(PORT, numeroJogadores):
    print("SERVER STARTED")
    users: List[socket.socket] = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("HOSTNAME:", socket.gethostname())
    server.bind((socket.gethostname(), PORT))
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

def criaJogo(numeroJogadores, dimensao):
    dados = {
            "dimensao": dimensao,
            "numeroPares": dimensao ** 2 / 2,
            "tabuleiro": novoTabuleiro(dimensao),
            "placar": novoPlacar(numeroJogadores),
            "paresEncontrados": 0,
            "vez": 0,
            "numeroJogadores": numeroJogadores
            }
    return dados

def enviaDadosIniciaisJogo(jogo, users):
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
        return True

    return False

def atualizaPlacar(jogo):
    jogo["placar"][jogo["vez"]] += 1

def atualizaVez(jogo):
    jogo["vez"] = (jogo["vez"] + 1) % jogo["numeroJogadores"]

def verificaJogada(tabuleiro, jogada):
    coordenada1, coordenada2 = jogada
    x1, y1 = coordenada1
    x2, y2 = coordenada2

    if tabuleiro[x1][y1] == tabuleiro[x2][y2]:
        print("jogada certa!")
        return True
    else:
        print("jogada errada!")
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
        tabuleiro[x1][y1] = "-"

    if tabuleiro[x2][y2] == '-':
        return False
    else:
        tabuleiro[x2][y2] = "-"

def enviaDadosParaTodosExcetoJogadorVez(users, vez, dado):
    dado_serializado = pickle.dumps(dado)
    i = 0
    print(f"Enviando dados para todos exceto: {vez}")
    for user in users:
        if i != vez:
            user.send(dado_serializado)
        i += 1
         
def verificaVencedores(placar, numeroJogadores):
    vencedores = []
    pontuacaoMaxima = max(placar)
    for i in range(0, numeroJogadores):
        if placar[i] == pontuacaoMaxima:
            vencedores.append(i)
    return vencedores

def iniciaJogo(jogo, users):
    while jogo["paresEncontrados"] < jogo["numeroPares"]:
        print("Aguardando coordenada 1...")
        coordenada1 = recebeDados(users[jogo["vez"]])
        enviaDadosParaTodosExcetoJogadorVez(users, jogo["vez"], coordenada1)
        time.sleep(0.5)

        print("Aguardando coordenada 2...")
        coordenada2 = recebeDados(users[jogo["vez"]])
        enviaDadosParaTodosExcetoJogadorVez(users, jogo["vez"], coordenada2)
        time.sleep(0.5)

        jogada = (coordenada1, coordenada2)
        validadeJogada = verificaJogada(jogo["tabuleiro"], jogada)

        enviaDadosParaTodos(users, (jogada, validadeJogada))
        if validadeJogada:
            atualizaTabuleiro(jogo["tabuleiro"], jogada)
            atualizaPlacar(jogo)
            jogo["paresEncontrados"] += 1
            time.sleep(5)
        else:
            jogo["vez"] = (jogo["vez"] + 1) % jogo["numeroJogadores"]
            time.sleep(3)

        enviaDadosParaTodos(users, jogo)

    time.sleep(0.25)
    vencedores = verificaVencedores(jogo["placar"], jogo["numeroJogadores"])
    print("Jogo encerrado...")
    enviaDadosParaTodos(users, vencedores)

def main():
    args = getArgs()
    if args.dimensao % 2 == 1 or args.dimensao > 10:
        print("Erro no argumento --dimensao")
        sys.exit(-1)
    users, server = conexaoJogadores(args.porta, args.numero)

    jogo = criaJogo(args.numero, args.dimensao)
    try:
        enviaDadosIniciaisJogo(jogo, users)

        iniciaJogo(jogo, users)

        fechaConexao(users, server)
        
    except:
        print("Saindo...")
        fechaConexao(users, server)
    finally:
        fechaConexao(users, server)


if __name__ == "__main__":
    main()
