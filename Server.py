import pickle
import socket
import argparse
import random
from typing import List

def getArgs():
    parser = argparse.ArgumentParser(description='Servidor que vai esperar os jogadores')
    parser.add_argument('--numero', type=int, help='Indica o número de jogadores')
    parser.add_argument('--porta', type=int, help='Indica em que porta vai escutar')
    parser.add_argument('--host', type=str, help='Indica qual vai ser o host do server')
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
    server.listen()
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
            "vez": vez
            }
    return dados

def enviaDadosJogo(jogo, users):
    dados = pickle.dumps(jogo)
    for user in users:
        user.send(dados)

def iniciaJogo():
    pass

def main():
    args = getArgs()
    users, server = conexaoJogadores(args.host, args.porta, args.numero)
    jogo = criaJogo(args.numero)

    enviaDadosJogo(jogo, users)


    fechaConexao(users, server)


if __name__ == "__main__":
    main()
