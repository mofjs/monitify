from pymsteams import connectorcard
from monitify.notif import BaseNotif


class TeamsNotif(BaseNotif):
    def __init__(self, url: str, ) -> None:
        super().__init__()
        self.url = url

    def send_message(self, name: str, items: list[str]):
        message = connectorcard(self.url)
        message.title("❗ Pemberitahuan ❗")
        message.text(
            f"{len(items)} item baru pada {name}:\n\n - " + "\n - ".join(items))
        message.send()
