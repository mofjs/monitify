import json
from owncloud import Client


def check_owncloud(host: str, user_id: str, password: str, file_path: str, dir: str = "/") -> list[str]:
    last_filelist = []
    with open(file_path, "r") as f:
        last_filelist = json.load(f)
    client = Client(host)
    client.login(user_id, password)
    new_filelist = [file.name for file in client.list(
        dir) if file.file_type == "file"]
    new_files = [file for file in new_filelist if file not in last_filelist]
    if new_files:
        with open(file_path, "w+") as f:
            json.dump(new_filelist, f)
    return new_files
