import socket
import sys
import os
from threading import Thread
from random import randint
from datetime import datetime

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("", 9803))

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

Thread(target = receive).start()
Thread(target = send).start()
