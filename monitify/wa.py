from queue import Queue
from wa_automate_socket_client import SocketClient
from monitify.notification import BaseNotificationWorker


class WaNotificationWorker(BaseNotificationWorker):
    def __init__(self, url: str, api_key: str, chat_id: str, queue: Queue) -> None:
        super().__init__(queue=queue)
        self.client = SocketClient(url, api_key)
        self.chat_id = chat_id
        print("WaNotificationWorker initialized.")

    def send_message(self, name: str, items: list[str]):
        self.client.sendText(
            self.chat_id, f"❗ *Pemberitahuan* ❗\n {len(items)} item baru pada {name}:\n\n🆕 " + "\n🆕 ".join(items))
