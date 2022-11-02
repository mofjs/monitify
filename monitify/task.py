import threading
import time
import typing
import queue


class BaseTask:
    def __init__(self, name: str, queue: queue.Queue, data: list = []) -> None:
        self.name = name
        self.queue = queue
        self.data = data

    def getData(self) -> list:
        return []

    def getItem(self, item: typing.Any) -> str:
        return f"{item}"

    def loop(self, secs: float) -> None:
        while True:
            new_data = self.getData()
            items = [self.getItem(item)
                     for item in new_data if item not in self.data]
            if items:
                self.queue.put({
                    "name": self.name,
                    "items": items
                })
                self.data = new_data
            time.sleep(secs)

    def run(self, secs: float) -> None:
        threading.Thread(target=self.loop, args=(secs))
