
from pymsteams import connectorcard
from queue import Queue
from monitify.notification import BaseNotificationWorker


class TeamsNotificationWorker(BaseNotificationWorker):
    def __init__(self, url: str, queue: Queue) -> None:
        super().__init__(queue)
        self.url = url

    def send_message(self, name: str, items: list[str]):
        message = connectorcard(self.url)
        message.title("❗ Pemberitahuan ❗")
        message.text(
            f"{len(items)} item baru pada {name}:\n\n - " + "\n - ".join(items))
