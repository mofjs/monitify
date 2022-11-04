from wa_automate_socket_client import SocketClient
from monitify.notif import BaseNotif


class WaNotif(BaseNotif):
    def __init__(self, url: str, api_key: str, chat_id: str) -> None:
        super().__init__()
        self.url = url
        self.api_key = api_key
        self.chat_id = chat_id

    def send_message(self, name: str, items: list[str]):
        client = SocketClient(self.url, self.api_key)
        client.sendText(
            self.chat_id,
            f"❗ *Pemberitahuan* ❗\n {len(items)} item baru pada {name}:\n\n🆕 " +
            "\n🆕 ".join(items)
        )
        client.disconnect()
