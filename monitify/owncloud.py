import owncloud
import queue
from monitify import task


class OwnCloudTask(task.BaseTask):
    def __init__(
        self,
        name: str,
        url: str,
        username: str,
        password: str,
        directory: str,
        queue: queue.Queue
    ) -> None:
        self.client = owncloud.Client(url)
        self.client.login(username, password)
        self.directory = directory
        data = []
        super().__init__(name, queue, data)

    def getData(self) -> list:
        contents = self.client.list(self.directory)
        return [file.name for file in contents if file.file_type == "file"]

