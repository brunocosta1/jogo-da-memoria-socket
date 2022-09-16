import socket
import sys
import os
from random import randint
from datetime import datetime

import argparse

parser = argparse.ArgumentParser(description='Player que vai se conectar com o servidor do jogo')
parser.add_argument('--porta', type=int, help='Indica em que porta vai se conectar')
parser.add_argument('--host', type=str, help='Indica qual vai ser o host')
args = parser.parse_args()
PORT = args.porta
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("", 8000))

id = randint(0, 10)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def receive():
    log = ""
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            clear()
            log = log + f"\n{msg}"
            print(log)
        except:
            client.close()
            sys.exit(0)

def send():
    while True:
        msg = input()
        clear()
        if(msg == "\quit"):
            client.close()
            sys.exit(0)
        client.send("[{}] {}: {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), id, msg).encode("utf-8"))

clear()

