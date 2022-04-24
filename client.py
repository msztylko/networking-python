from socket import *

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 9876))
sock.send(b'hey')
data = sock.recv(10000)
print(f'Got back {data}')
sock.close()


