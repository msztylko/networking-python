import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 65433))
sock.listen()

while True:
    conn, addr = sock.accept()
    data = conn.recv(1024)
    if not data:
        break
    else:
        print(f'Got {data} from {addr}')