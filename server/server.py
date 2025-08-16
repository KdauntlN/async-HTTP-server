import os

def handle_client(conn):
    request: str = conn.recv(1024).decode()
    print(request)

    request_line = request.splitlines()[0]

    words = request_line.split(" ")

    if words[0] != "GET":
        response = "HTTP/1.1 501 NOT IMPLEMENTED"
        conn.send(response.encode())
        return

    requested_file = words[1]
    filename, extension = os.path.splitext(requested_file)

    if extension == "":
        extension = ".html"

    if filename == "/":
        filename = "/index"

    path = f"public{filename}{extension}"

    try:
        with open(path, "r") as file:
            content = file.read()
            length = len(content)
            status_line = "HTTP/1.1 200 OK"
    except FileNotFoundError:
        with open("public/404.html") as file:
            content = file.read()
            length = len(content)
            status_line = "HTTP/1.1 404 NOT FOUND"

    response = f"{status_line}\r\nContent-Length: {length}\r\n\r\n{content}"
    print(response)

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