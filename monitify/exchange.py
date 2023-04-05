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
        delay=60.0
    ) -> None:
        self.queue = queue
        self.kill = kill
        self.delay = delay
        credentials = Credentials(username, password)
        config = Configuration(credentials, server)
        self.account = Account(email, autodiscover=False,
                               config=config, access_type=DELEGATE)
        print(f"ExchangeTaskWorker for {name} is initialized.")

    def run(self) -> None:
        retry = 0
        while not self.kill.wait((retry * 5) if retry > 0 else self.delay):
            try:
                with self.account.inbox.streaming_subscription() as subscription_id:
                    for notification in self.account.inbox.get_streaming_events(subscription_id):
                        items = []
                        for event in notification.events:
                            if isinstance(event, NewMailEvent):
                                mail = self.account.inbox.get(event.item_id)
                                items.append(
                                    f"{mail.sender.name}<{mail.sender.email_address}>: {mail.subject}")
                        if items:
                            self.queue.put({
                                "name": self.name,
                                "items": items
                            })
                retry = 0
            except:
                if retry > 99:
                    raise Exit(1)
                retry += 1