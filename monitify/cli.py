import typer
from pathlib import Path
from typing import Optional
from queue import Queue
from monitify import __app_name__, __version__
from monitify.config import parse_config, validate_config
from monitify.wa import WaNotificationWorker
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
        typer.secho("No configuration file found.")
        raise typer.Exit(1)
    config = parse_config(config_path)
    if not validate_config(config):
        typer.secho("Invalid configuration.")
        raise typer.Exit(1)
    q = Queue()
    workers = []

    for notification_config in config["notifications"]:
        notification_type = notification_config.pop("type")
        if notification_type == "wa":
            workers.append(WaNotificationWorker(
                queue=q, **notification_config))
        if notification_type == "teams":
            pass

    for task_config in config["tasks"]:
        task_type = task_config.pop("type")
        if task_type == "email":
            workers.append(EmailTaskWorker(queue=q, **task_config))
        if task_type == "owncloud":
            workers.append(OwnCloudTaskWorker(queue=q, **task_config))

    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()
