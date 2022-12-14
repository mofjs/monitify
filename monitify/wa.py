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
            f"ā *Pemberitahuan* ā\n {len(items)} item baru pada {name}:\n\nš " +
            "\nš ".join(items)
        )
        client.disconnect()
