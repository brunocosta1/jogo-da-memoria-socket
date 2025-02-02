import pickle
import socket
import sys
import os
import argparse
import time

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

def limpaTela():
    os.system('cls' if os.name == 'nt' else 'clear')

def recebeDados(client: socket.socket):
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

        print (f"Vez do Jogador {vez + 1}.\n")

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

def abrePeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False
    elif tabuleiro[i][j] < 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        # Envia para o servidor
        return True

    return False


def iniciaJogo(ID, user: socket.socket, jogo):
    while(jogo["paresEncontrados"] < jogo["numeroPares"]):
        if jogo["vez"] == ID:
            # Lendo primeira coordenada 
            while True:
                imprimeStatus(jogo["tabuleiro"], jogo["placar"], jogo["vez"])
                primeiraCoordenada = leCoordenada(jogo["dimensao"])

                if primeiraCoordenada == False:
                    continue
                
                x1, y1 = primeiraCoordenada

                if abrePeca(jogo["tabuleiro"], x1, y1) == False:
                    print("Escolha uma peça ainda fechada!")
                    input("Pressiona <enter para continuar...")
                    continue

                break

            enviaDados(user, primeiraCoordenada)
            time.sleep(0.5)
            # Lendo segunda coordenada
            while True:
                imprimeStatus(jogo["tabuleiro"], jogo["placar"], jogo["vez"])
                segundaCoordenada = leCoordenada(jogo["dimensao"])

                if segundaCoordenada == False:
                    continue
                
                x2, y2 = segundaCoordenada

                if abrePeca(jogo["tabuleiro"], x2, y2) == False:
                    print("Escolha uma peça ainda fechada!")
                    input("Pressiona <enter para continuar...")
                    continue

                break
            enviaDados(user, segundaCoordenada)
            time.sleep(0.5)
        else:
            imprimeStatus(jogo["tabuleiro"], jogo["placar"], jogo["vez"])
            primeiraCoordenada = recebeDados(user)
            x1, y1 = primeiraCoordenada 
            abrePeca(jogo["tabuleiro"], x1, y1)
            time.sleep(0.5)

            imprimeStatus(jogo["tabuleiro"], jogo["placar"], jogo["vez"])
            segundaCoordenada = recebeDados(user)
            x2, y2 = segundaCoordenada 
            abrePeca(jogo["tabuleiro"], x2, y2)
            time.sleep(0.5)


        imprimeStatus(jogo["tabuleiro"], jogo["placar"], jogo["vez"])
        jogada, validadeJogada = recebeDados(user)

        primeiraCoordenada, segundaCoordenada = jogada
        x1, y1 = primeiraCoordenada
        x2, y2 = segundaCoordenada


        imprimeStatus(jogo["tabuleiro"], jogo["placar"], jogo["vez"])
        print(f"Peças escolhidas --> ({x1}, {y1}) e ({x2}, {y2})")
        if validadeJogada == True:
            print(f"Peças casam! Ponto para o jogador {jogo['vez'] + 1}")
            time.sleep(5)
        else:
            print("Peças não casam!")
            time.sleep(3)


        jogo = recebeDados(user)

    time.sleep(0.25)
    vencedores = recebeDados(user)

    if len(vencedores) > 1:
        sys.stdout.write("Houve empate entre os jogadores ")
        for i in vencedores:
            sys.stdout.write(str(i + 1) + ' ')
        sys.stdout.write("\n")
    else:
        print(f"Jogador {vencedores[0] + 1} foi o vencedor")

def main():
    args = getArgs()
    client = connect(args.host, args.porta)
    limpaTela()

    print("Aguardando os jogadores se conectarem para o início do jogo")

    try:
        jogo, identificador = recebeDados(client)
        time.sleep(0.5)
        iniciaJogo(identificador, client, jogo)
        client.close()
    except:
        print("Saindo...")
        client.close()
    finally:
        client.close()


if __name__ == "__main__":
    main()

