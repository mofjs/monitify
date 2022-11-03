from email import message_from_bytes
from imaplib import IMAP4_SSL
from typing import Any
from queue import Queue
from monitify.task import BaseTaskWorker


class EmailTaskWorker(BaseTaskWorker):
    def __init__(
        self,
        queue: Queue,
        name: str,
        host: str,
        user: str,
        password: str,
        port: int = 993,
        delay: float = 60.0,
    ) -> None:
        super().__init__(name, queue, delay)
        self.client = IMAP4_SSL(host, port)
        self.client.login(user, password)
        self.data = self.getData()
        print(f"EmailTaskWorker for {name} is initialized.")

    def getData(self) -> list:
        self.client.select("INBOX")
        (_, data) = self.client.search(None, "ALL")
        return data

    def getItem(self, item: Any) -> str:
        (_, data) = self.client.fetch(item, "(BODY.PEEK[HEADER])")
        msg = message_from_bytes(data[0][1])
        return f"{msg['from']}: {msg['subject']}"
