import threading
import mpsc

class ShutDownThread(Exception):
    pass

class Worker:
    def __init__(self, id, receiver, lock):
        self.id = id
        self.thread = threading.Thread(target=self.job, args=(receiver, lock))
        self.thread.start()
        

    def job(self, receiver, lock):
        try:
            with lock:
                task, *args = receiver.recv()

            task(*args)
        except ShutDownThread:
            return


class ThreadPool:
    def __init__(self, size):
        self.size = size
        self.workers = []
        worker_lock = threading.Lock()
        (self.sender, receiver) = mpsc.channel()

        for id in range(size):
            self.workers.append(Worker(id, receiver, worker_lock))

    def execute(self, f, *args):
        self.sender.send((f, *args))

    def end_thread():
        raise ShutDownThread
    
    def shutdown(self):
        for worker in self.workers:
            self.sender.send(self.end_thread)

