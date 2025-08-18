import os
from socket import socket

binary_extensions = {
    ".png",
    ".jpg",
    ".jpeg",
    ".ico",
    ".svg",
    ".pdf"
}

def read_text(path:str):
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

    return content, length, status_line

def read_bin(path: str):
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

    words = request_line.split(" ")

    match words[0]:
        case "GET":
            uri = words[1]
            response = get(uri)
            conn.send(response)
        case _:
            response = "HTTP/1.1 501 NOT IMPLEMENTED\r\n"
            conn.send(response.encode())

def get(uri: str) -> bytes:
    filename, extension = os.path.splitext(uri)

    if extension == "":
        extension = ".html"

    if filename == "/":
        filename = "/index"

    path = f"public{filename}{extension}"

    content, length, status_line = read_bin(path) if extension in binary_extensions else read_text(path)

    headers = f"{status_line}\r\nContent-Length: {length}\r\n\r\n".encode()
    content = content if extension in binary_extensions else content.encode()
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