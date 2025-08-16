def handle_client(conn):
    message = conn.recv(1024).decode()
    response = "HTTP/1.1 200 OK"
    conn.send(response.encode())

class IterConn:
    def __init__(self, server):
        self.server = server

    def __iter__(self):
        return self
    
    def __next__(self):
        return self.server.accept()

def incoming(server):
    return IterConn(server)