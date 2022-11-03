from threading import Thread
from time import sleep
from typing import Any
from queue import Queue


class BaseTaskWorker(Thread):
    def __init__(self, name: str, queue: Queue, delay: float, data: list = []) -> None:
        super().__init__()
        self.name = name
        self.queue = queue
        self.delay = delay
        self.data = data

    def getData(self) -> list:
        return []

    def getItem(self, item: Any) -> str:
        return f"{item}"

    def run(self) -> None:
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
                print(f"{len(items)} new items found in {self.name}.")
            else:
                print(f"No new items found in {self.name}.")
            sleep(self.delay)
