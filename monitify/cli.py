import typer
from pathlib import Path
from typing import Optional
from monitify import __app_name__, __version__


app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command()
def main(
    config: Path = typer.Option(
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
    if not config.exists():
        typer.echo("No configuration file found.")
    return
