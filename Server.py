import socket
import argparse
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


def main():
    args = getArgs()
    users, server = conexaoJogadores(args.host, args.porta, args.numero)
    fechaConexao(users, server)


if __name__ == "__main__":
    main()
