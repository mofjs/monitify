import email
import imaplib
import typing
import queue
from monitify import task


class EmailTask(task.BaseTask):
    def __init__(
        self,
        name: str,
        hostname: str,
        port: int,
        username: str,
        password: str,
        queue: queue.Queue
    ) -> None:
        self.client = imaplib.IMAP4_SSL(hostname, port)
        self.client.login(username, password)
        data = []
        super().__init__(name, queue, data)

    def getData(self) -> list:
        self.client.select("INBOX")
        (_, data) = self.client.search(None, "ALL")
        return data

    def getItem(self, item: typing.Any) -> str:
        (_, data) = self.client.fetch(item, "(BODY.PEEK[HEADER])")
        msg = email.message_from_bytes(data[0][1])
        return f"{msg['from']}: {msg['subject']}"
