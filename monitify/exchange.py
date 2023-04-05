from exchangelib import Credentials, Account, Configuration, DELEGATE
from exchangelib.properties import NewMailEvent
from threading import Thread, Event
from typer import Exit
from queue import SimpleQueue


class ExchangeTaskWorker(Thread):
    def __init__(
        self,
        queue: SimpleQueue,
        kill: Event,
        name: str,
        server: str,
        username: str,
        password: str,
        email: str,
        timeout = 5
    ) -> None:
        super().__init__()
        self.queue = queue
        self.kill = kill
        self.name = name
        credentials = Credentials(username, password)
        config = Configuration(credentials, server, max_connections=4)
        self.account = Account(email, autodiscover=False,
                               config=config, access_type=DELEGATE)
        self.timeout = timeout
        print(f"ExchangeTaskWorker for {name} is initialized.")

    def run(self) -> None:
        retry = 0
        while not self.kill.wait(retry * 5):
            try:
                with self.account.inbox.streaming_subscription() as subscription_id:
                    print(f"[{self.name}]: Subscribed with id {subscription_id}")
                    while not self.kill.wait():
                        for notification in self.account.inbox.get_streaming_events(subscription_id, connection_timeout=self.timeout):
                            items = []
                            for event in notification.events:
                                if isinstance(event, NewMailEvent):
                                    mail = self.account.inbox.get(event.item_id.id)
                                    items.append(
                                        f"{mail.sender.name}<{mail.sender.email_address}>: {mail.subject}")
                            if items:
                                self.queue.put({
                                    "name": self.name,
                                    "items": items
                                })
                retry = 0
            except Exception as e:
                print(f"[{self.name}]: Retrying subscription for {retry} time(s)")
                print(f"[{self.name}]: Last error\t {e}")
                if retry > 99:
                    raise Exit(1)
                retry += 1
