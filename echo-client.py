import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) # connect to server
    s.sendall(b"Hello world") # send message
    data = s.recv(1024) # read the server's reply
    
print(f"Received {data!r}")