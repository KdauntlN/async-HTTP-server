import os
from socket import socket

def find_mime(ext) -> str:
    match ext:
        case ".html" | ".htm":
            return "text/html"
        case ".css":
            return "text/css"
        case ".js":
            return "application/javascript"
        case ".png":
            return "image/png"
        case ".jpg":
            return "image/jpg"
        case ".jpeg":
            return "image/jpeg"
        case ".gif":
            return "image/gif"
        case ".ico":
            return "image/x-icon"
        case ".svg":
            return "image/svg+xml"
        case ".webp":
            return "image/webp"
        case ".json":
            return "application/json"
        case ".pdf":
            return "application/pdf"
        case ".txt":
            return "text/plain"
        case ".xml":
            return "application/xml"

def fetch_file(path: str):
    try:
        with open(path, "rb") as file:
            content = file.read()
            length = len(content)
            status_line = "HTTP/1.1 200 OK"
    except FileNotFoundError:
        with open("public/404.html") as file:
            content = file.read()
            length = len(content)
            status_line = "HTTP/1.1 404 NOT FOUND"
    
    return content, length, status_line

def handle_client(conn: socket):
    request: str = conn.recv(1024).decode()

    try:
        request_line = request.splitlines()[0]
    except IndexError:
        print(f" Error with request: {request}\n")
        return

    method, uri, _protocol = request_line.split(" ")

    match method[0]:
        case "GET":
            response = get(uri)
            conn.send(response)
        case _:
            response = "HTTP/1.1 501 NOT IMPLEMENTED\r\n"
            conn.send(response.encode())

    conn.close()

def get(uri: str) -> bytes:
    filename, extension = os.path.splitext(uri)

    if extension == "":
        extension = ".html"

    if filename == "/":
        filename = "/index"

    path = f"public{filename}{extension}"

    content, length, status_line = fetch_file(path)

    mime_type = find_mime(extension)

    headers = (f"{status_line}\r\n"
               f"Content-Length: {length}\r\n"
               f"Content-Type: {mime_type}\r\n"
               f"Connection: close\r\n"
               "\r\n"
               ).encode()
    
    response = headers + content

    return response

class IterConn:
    def __init__(self, server: socket) -> None:
        self.server = server

    def __iter__(self) -> "IterConn":
        return self
    
    def __next__(self) -> tuple[socket, str]:
        return self.server.accept()

def incoming(server: socket) -> IterConn:
    return IterConn(server)