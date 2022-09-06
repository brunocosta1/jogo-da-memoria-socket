import socket

HOST = ""
PORT = 5000
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    print("Conectado por", cliente)
    while True:
        msg = con.recv(1024)
        if not msg: break
        print(cliente, msg)
    print("Finalizando conexao do cliente", cliente)
    con.close()