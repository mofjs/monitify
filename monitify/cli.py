import typer
from pathlib import Path
from threading import Event, Thread
from typing import Optional
from queue import SimpleQueue
from monitify import __app_name__, __version__
from monitify.config import parse_config, validate_config
from monitify.exchange import ExchangeTaskWorker
from monitify.notification import NotificationsWorker
from monitify.email import EmailTaskWorker
from monitify.owncloud import OwnCloudTaskWorker


app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command()
def main(
    config_path: Path = typer.Option(
        Path("./config.yml"),
        "--config",
        "-c",
        help="Configuration file.",
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    if not config_path.exists():
        print("No configuration file found.")
        raise typer.Exit(1)
    config = parse_config(config_path)
    if not validate_config(config):
        print("Invalid configuration.")
        raise typer.Exit(1)
    print("Configuration accepted.")
    q = SimpleQueue()
    k = Event()
    workers: list[Thread] = []

    workers.append(NotificationsWorker(
        queue=q, kill=k, configs=config["notifications"]))

    for task_config in config["tasks"]:
        task_type = task_config.pop("type")
        if task_type == "email":
            workers.append(EmailTaskWorker(queue=q, kill=k, **task_config))
        if task_type == "owncloud":
            workers.append(OwnCloudTaskWorker(queue=q, kill=k, **task_config))
        if task_type == "exchange":
            workers.append(ExchangeTaskWorker(queue=q, kill=k, **task_config))

    print("Start monitoring.")
    for worker in workers:
        worker.start()

    while not k.wait(10):
        if any(not worker.is_alive() for worker in workers):
            k.set()
            for worker in workers:
                worker.join()
