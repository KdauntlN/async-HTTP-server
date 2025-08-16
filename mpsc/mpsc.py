import threading
import time

class Sender:
    def __init__(self, queue: list, lock: threading.Lock):
        self.queue = queue
        self.lock = lock

    def send(self, item):
        with self.lock:
            self.queue.append(item)

class Receiver:
    def __init__(self, queue: list, lock: threading.Lock):
        self.queue = queue
        self.lock = lock

    def recv(self):
        while True:
            self.lock.acquire()
            if len(self.queue) == 0:
                self.lock.release()
                time.sleep(0.001)
                continue
            else:
                message = self.queue.pop(0)
                self.lock.release()
                return message


def channel() -> tuple[Sender, Receiver]:
    queue = []
    lock = threading.Lock()
    return (Sender(queue, lock), Receiver(queue, lock))