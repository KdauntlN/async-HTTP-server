import threading
import mpsc

class ShutDownThread(Exception):
    pass

class Worker:
    def __init__(self, id, receiver):
        self.id = id
        self.thread = threading.Thread(target=self.job, args=(receiver,), name=f"worker-{id}")
        self.thread.start()
        

    def job(self, receiver):
        while True:
            try:
                task, *args = receiver.recv()

                print(f"thread {self.id} got a job, starting...")
                task(*args)
                print(f"thread {self.id} finished the job")
            except ShutDownThread:
                return


class ThreadPool:
    def __init__(self, size):
        self.size = size
        self.workers: list[Worker] = []
        (self.sender, receiver) = mpsc.channel()

        for id in range(size):
            self.workers.append(Worker(id, receiver))

    def execute(self, f, *args):
        self.sender.send((f, *args))

    def end_thread(self):
        raise ShutDownThread
    
    def shutdown(self):
        for worker in self.workers:
            self.sender.send(self.end_thread)
        for worker in self.workers:
            worker.thread.join()

