import socket
from threading import Thread
import argparse

parser = argparse.ArgumentParser(description='Servidor que vai esperar os jogadores')
parser.add_argument('--numero', type=int, help='Indica o número de jogadores')
parser.add_argument('--porta', type=str, help='Indica em que porta vai escutar')
parser.add_argument('--host', type=str, help='Indica qual vai ser o host do server')
args = parser.parse_args()

users: socket.socket = []

def handle(client):
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            for user in users:
                user.send(msg.encode("utf-8"))
        except:
            users.remove(client)
            client.close()
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 9803))
server.listen()

print("SERVER STARTED")

while True:
    client, address = server.accept()
    users.append(client)
    print("[CONNECTION]: ", address)

    Thread(target = handle, args = (client,)).start()
