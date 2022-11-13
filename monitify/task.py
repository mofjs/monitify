from threading import Thread, Event
from typer import Exit
from typing import Any
from queue import SimpleQueue


class BaseTaskWorker(Thread):
    def __init__(self, name: str, queue: SimpleQueue, kill: Event, delay: float) -> None:
        super().__init__()
        self.name = name
        self.queue = queue
        self.kill = kill
        self.delay = delay

    def setup(self) -> None:
        pass

    def getData(self) -> list:
        return []

    def getItem(self, item: Any) -> str:
        return f"{item}"

    def run(self) -> None:
        unset = True
        retry = 0
        while not self.kill.wait((retry * 5) if unset else self.delay):
            try:
                if unset:
                    self.setup()
                    self.data = self.getData()
                    unset = False
                    retry = 0
                else:
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
            except:
                if retry > 99:
                    raise Exit(1)
                unset = True
                retry += 1
