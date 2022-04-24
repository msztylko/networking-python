from socket import *

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("", 9876))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    print(f'Got connection from {addr}')
    data = conn.recv(10000)
    print(f'Received message {data}')
    msg = f'Thanks for your {data}'
    conn.send(msg.encode())
    conn.close()
