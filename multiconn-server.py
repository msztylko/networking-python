import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f'Listening on {(host, port)}')

# configure non-blocking mode
lsock.setblocking(False)
# sel.register() registers the socket to be monitored with sel.select() 
# For the listening socket, you want read events: selectors.EVENT_READ. 
sel.register(lsock, selectors.EVENT_READ, data=None)


def accept_wrapper(sock):
    conn, addr = sock.accept() # should be ready to read
    print(f'Accepted connection from {addr}')
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    # True if socket ready for reading
    if mask &selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print(f'Closing connection to {data.addr}')
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f'Echoing {data.outb!r} to {data.addr}')
            sent = sock.send(data.outb)
            # discard sent data from the buffer
            data.outb = data.outb[sent:]

try:
    while True:
        # blocks until sockets are ready for I/O
        # sel.select() returns a list of tuples, one for each socket.
        events = sel.select(timeout=None)
        # key - SelectorKey namedtuple; key.fileobj is the socket object
        # mask - event mask of the operations that are ready
        for key, mask in events:
            # if None then from listening socket
            if key.data is None:
                accept_wrapper(key.fileobj)
            # client socket that's already been accepted; you want to service it
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print('Caught keyboard interrupt, exiting')
finally:
    sel.close()