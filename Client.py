import socket

HOST = "127.0.0.1"
PORT = 5000
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)

tcp.connect(dest)

msg = ""

while msg != "\x18":
    msg = bytearray(input(), "utf-8")
    tcp.send(msg)


tcp.close()