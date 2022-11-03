from owncloud import Client
from queue import Queue
from monitify.task import BaseTaskWorker


class OwnCloudTaskWorker(BaseTaskWorker):
    def __init__(
        self,
        queue: Queue,
        name: str,
        url: str,
        user_id: str,
        password: str,
        path: str = "/",
        delay: float = 300.0,
    ) -> None:
        super().__init__(name, queue, delay)
        self.client = Client(url)
        self.client.login(user_id, password)
        self.path = path
        self.data = self.getData()
        print(f"OwnCloudTaskWorker for {name} is initialized.")

    def getData(self) -> list:
        contents = self.client.list(self.path)
        return [file.name for file in contents if file.file_type == "file"]
