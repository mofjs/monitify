from queue import Queue
from threading import Thread


class BaseNotificationWorker(Thread):
    def __init__(self, queue: Queue) -> None:
        super().__init__()
        self.queue = queue

    def send_message(self, name: str, items: list[str]):
        pass

    def run(self) -> None:
        while True:
            message = self.queue.get()
            self.send_message(message["name"], message["items"])
