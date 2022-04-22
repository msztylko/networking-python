import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()
messages = [b"Message 1 from client.", b"Message 2 from client."]

def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(num_conns):
        connid = i + 1
        print(f'Starting connection {connid} to {server_addr}')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        # connect() would raise BlockingIOError
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=messages.copy(),
            outb=b"",
        )
        sel.register(sock, events, data=data)
        
def service_connection(key, mask):
    sock = keyfileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = osck.recv(1024)
        if recv_data:
            print(f'Received {recv_data!r} from connection {data.connid}')
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print(f'Closing connection {data.connid}')
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print(f'Sending {data.outb!r} to connection {data.connid}')
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]