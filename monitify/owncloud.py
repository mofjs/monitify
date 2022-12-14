from owncloud import Client
from threading import Event
from queue import SimpleQueue
from monitify.task import BaseTaskWorker


class OwnCloudTaskWorker(BaseTaskWorker):
    def __init__(
        self,
        queue: SimpleQueue,
        kill: Event,
        name: str,
        url: str,
        user_id: str,
        password: str,
        path: str = "/",
        delay: float = 300.0,
    ) -> None:
        super().__init__(name, queue, kill, delay)
        self.url = url
        self.user_id = user_id
        self.password = password
        self.path = path
        print(f"OwnCloudTaskWorker for {name} is initialized.")

    def setup(self) -> None:
        self.client = Client(self.url)
        self.client.login(self.user_id, self.password)

    def getData(self) -> list:
        contents = self.client.list(self.path)
        return [file.name for file in contents if file.file_type == "file"]
