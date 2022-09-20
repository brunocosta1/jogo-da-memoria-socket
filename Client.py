import pickle
import socket
import sys
import os
from datetime import datetime

import argparse

def getArgs():
    parser = argparse.ArgumentParser(description='Player que vai se conectar com o servidor do jogo')
    parser.add_argument('--porta', type=int, help='Indica em que porta vai se conectar')
    parser.add_argument('--host', type=str, help='Indica qual vai ser o host')
    args = parser.parse_args()
    return args



def connect(HOST: str, PORT: int):
    print("Conectando...")
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((HOST, PORT))
    print("Conectado!")
    return c 


def clear():
    os.system("cls" if os.name == "nt" else "clear")

# def receive():
#     log = ""
#     while True:
#         try:
#             msg = client.recv(1024).decode("utf-8")
#             clear()
#             log = log + f"\n{msg}"
#             print(log)
#         except:
#             client.close()
#             sys.exit(0)
#
# def send():
#     while True:
#         msg = input()
#         clear()
#         if(msg == "\quit"):
#             client.close()
#             sys.exit(0)
#         client.send("[{}] {}: {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), id, msg).encode("utf-8"))
#
# send()

def limpaTela():
    os.system('cls' if os.name == 'nt' else 'clear')

def recebeDados(client: socket.socket):
    limpaTela()
    print("Recebendo dados...")
    datajogo = client.recv(1024)
    datajogo = pickle.loads(datajogo)
    return datajogo

def enviaDados(client: socket.socket, dados):
    dado_serializado = pickle.dumps(dados)
    client.send(dado_serializado)



def imprimeTabuleiro(tabuleiro):

    # Limpa a tela
    limpaTela()

    # Imprime coordenadas horizontais
    dim = len(tabuleiro)
    sys.stdout.write("     ")
    for i in range(0, dim):
        sys.stdout.write("{0:2d} ".format(i))

    sys.stdout.write("\n")

    # Imprime separador horizontal
    sys.stdout.write("-----")
    for i in range(0, dim):
        sys.stdout.write("---")

    sys.stdout.write("\n")

    for i in range(0, dim):

        # Imprime coordenadas verticais
        sys.stdout.write("{0:2d} | ".format(i))

        # Imprime conteudo da linha 'i'
        for j in range(0, dim):

            # Peca ja foi removida?
            if tabuleiro[i][j] == '-':

                # Sim.
                sys.stdout.write(" - ")

            # Peca esta levantada?
            elif tabuleiro[i][j] >= 0:

                # Sim, imprime valor.
                sys.stdout.write("{0:2d} ".format(tabuleiro[i][j]))
            else:

                # Nao, imprime '?'
                sys.stdout.write(" ? ")

        sys.stdout.write("\n")

def imprimeStatus(tabuleiro, placar, vez):

        imprimeTabuleiro(tabuleiro)
        sys.stdout.write('\n')

        imprimePlacar(placar)
        sys.stdout.write('\n')
        sys.stdout.write('\n')

        print ("Vez do Jogador {0}.\n".format(vez + 1))

def imprimePlacar(placar):

    nJogadores = len(placar)

    print ("Placar:")
    print ("---------------------")
    for i in range(0, nJogadores):
        print ("Jogador {0}: {1:2d}".format(i + 1, placar[i]))

def leCoordenada(dim):

    inp = input("Especifique uma peca: ")

    try:
        i = int(inp.split(' ')[0])
        j = int(inp.split(' ')[1])
    except ValueError:
        print ("Coordenadas invalidas! Use o formato \"i j\" (sem aspas),")
        print ("onde i e j sao inteiros maiores ou iguais a 0 e menores que {0}".format(dim))
        input("Pressione <enter> para continuar...")
        return False

    if i < 0 or i >= dim:

        print ("Coordenada i deve ser maior ou igual a zero e menor que {0}".format(dim))
        input("Pressione <enter> para continuar...")
        return False

    if j < 0 or j >= dim:

        print ("Coordenada j deve ser maior ou igual a zero e menor que {0}".format(dim))
        input("Pressione <enter> para continuar...")
        return False

    return (i, j)

def recebeID(client: socket.socket):
    print("Pegando ID...")
    identificacao = client.recv(1024)
    identificacao = pickle.loads(identificacao)
    return int(identificacao)

def iniciaJogo(ID, user: socket.socket, jogo):
    while(jogo["paresEncontrados"] < jogo["numeroPares"]):
        imprimeStatus(jogo["tabuleiro"], jogo["placar"], jogo["vez"])
        if jogo["vez"] == ID:
            jogada = leCoordenada(jogo["dimensao"])
            enviaDados(user, jogada)

        

def main():
    args = getArgs()
    client = connect(args.host, args.porta)

    limpaTela()
    print("Aguardando os jogadores se conectarem para o início do jogo")
    # jogador recebe dados do jogo do servidor
    jogo, identificador = recebeDados(client)
    print(jogo)
    print(identificador)
    # jogador recebe uma identificação
    iniciaJogo(identificador, client, jogo)
    client.close()






if __name__ == "__main__":
    main()

