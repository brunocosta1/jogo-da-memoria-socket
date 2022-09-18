import pickle
import socket
import sys
import os
from random import randint
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
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("Conectado!")
    return client

id = randint(0, 10)

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

def recebeDadosJogo(client):
    datajogo = client.recv(1024)
    datajogo = pickle.loads(datajogo)
    return datajogo

def main():
    args = getArgs()
    client = connect(args.host, args.porta)

    limpaTela()
    print("Aguardando os jogadores se conectarem para o início do jogo")
    jogo = recebeDadosJogo(client)


    print(jogo)


    client.close()

if __name__ == "__main__":
    main()

