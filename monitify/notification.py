from queue import SimpleQueue, Empty
from threading import Thread, Event
from monitify.notif import BaseNotif
from monitify.wa import WaNotif
from monitify.teams import TeamsNotif


class NotificationsWorker(Thread):
    def __init__(self, queue: SimpleQueue, kill: Event, configs: list[dict]) -> None:
        super().__init__()
        self.queue = queue
        self.kill = kill
        self.notifs: list[BaseNotif] = []
        for config in configs:
            notif_type = config.pop("type")
            if notif_type == "wa":
                self.notifs.append(WaNotif(**config))
            if notif_type == "teams":
                self.notifs.append(TeamsNotif(**config))

    def run(self) -> None:
        while not self.kill.is_set():
            try:
                message = self.queue.get(timeout=10)
                for notif in self.notifs:
                    notif.send_message(message["name"], message["items"])
            except Empty:
                continue