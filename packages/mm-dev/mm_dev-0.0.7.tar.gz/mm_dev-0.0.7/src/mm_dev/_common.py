import importlib.metadata
from typing import Annotated

import typer
from click.exceptions import Exit
from mm_std import print_console


def version_callback(value: bool) -> None:
    if value:
        version = importlib.metadata.version("mm-dev")
        print_console(f"v{version}")
        raise Exit


Version = Annotated[bool | None, typer.Option("--version", callback=version_callback, help="Show the version and exit.")]


def create_app(multi_command: bool = False) -> typer.Typer:
    app = typer.Typer(add_completion=False)

    if multi_command:

        @app.callback()
        def main(_version: Version = None) -> None:
            pass

    return app
