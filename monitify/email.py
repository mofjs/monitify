from email import message_from_bytes
from imaplib import IMAP4_SSL
from threading import Event
from typing import Any
from queue import Queue
from monitify.task import BaseTaskWorker


class EmailTaskWorker(BaseTaskWorker):
    def __init__(
        self,
        queue: Queue,
        kill: Event,
        name: str,
        host: str,
        user: str,
        password: str,
        port: int = 993,
        delay: float = 60.0,
    ) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        super().__init__(name, queue, kill, delay)
        print(f"EmailTaskWorker for {name} is initialized.")

    def setup(self) -> None:
        self.client = IMAP4_SSL(self.host, self.port)
        self.client.login(self.user, self.password)

    def getData(self) -> list:
        self.client.select("INBOX")
        (_, data) = self.client.search(None, "ALL")
        return str(data[0], "utf-8").split()

    def getItem(self, item: Any) -> str:
        (_, data) = self.client.fetch(item, "(BODY.PEEK[HEADER])")
        msg = message_from_bytes(data[0][1])
        return f"{msg['from']}: {msg['subject']}"
