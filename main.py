from threadpool import ThreadPool
from server import incoming, handle_client

import time
import socket

def main():
    threadpool = ThreadPool(5)

    host, port = "127.0.0.1", 7878
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)

    for conn, _addr in incoming(server):
        threadpool.execute(handle_client, conn)

if __name__ == "__main__":
    main()