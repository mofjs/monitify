from abc import ABCMeta, abstractmethod
from queue import Queue
from threading import Thread
from monitify.notif import BaseNotif
from monitify.wa import WaNotif
from monitify.teams import TeamsNotif


class NotificationsWorker(Thread):
    def __init__(self, queue: Queue, configs: list[dict]) -> None:
        super().__init__()
        self.queue = queue
        self.notifs: list[BaseNotif] = []
        for config in configs:
            type = config.pop("type")
            if type == "wa":
                self.notifs.append(WaNotif(**config))
            if type == "teams":
                self.notifs.append(TeamsNotif(**config))

    def run(self) -> None:
        while True:
            message = self.queue.get()
            for notif in self.notifs:
                notif.send_message(message["name"], message["items"])