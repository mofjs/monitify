from monitify.notif import BaseNotif
from requests import post


class WebhookNotif(BaseNotif):
    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url

    def send_message(self, name: str, items: list[str]) -> None:
        message = f"❗ *Pemberitahuan* ❗\n {len(items)} item baru pada {name}:\n\n🆕 " + \
            "\n🆕 ".join(items)
        post(self.url, message.encode("utf-8"))
