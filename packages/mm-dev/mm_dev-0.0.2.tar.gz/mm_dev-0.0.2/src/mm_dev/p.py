import os
from pathlib import Path
from typing import Optional

from mm_std import fatal, run_command
from typer import Argument

from mm_dev._common import create_app

app = create_app(multi_command=True)


@app.command(name="o", help="pip list -o")
def pip_list_outdated() -> None:
    run_command("pip list -o", capture_output=False)


@app.command(name="l", help="pip list")
def pip_list() -> None:
    run_command("pip list", capture_output=False)


@app.command(name="u", help="pip install -U pip setuptools wheel")
def update_pip() -> None:
    run_command("pip install -U pip setuptools wheel", capture_output=False)


@app.command(name="i", help="install packages or project (setup.py or requirements.txt)")
def install(packages: Optional[str] = Argument(None)) -> None:  # noqa: UP007
    if not os.getenv("VIRTUAL_ENV"):
        fatal("venv is not activated")

    if packages:
        run_command(f"pip install {packages}", capture_output=False)
        return

    if Path("setup.py").is_file():
        run_command("pip install -Ue .[dev]", capture_output=False)
        return

    if Path("requirements.txt").is_file():
        run_command("pip install -Ur requirements.txt", capture_output=False)
        return

    run_command("pdm install", capture_output=False)


@app.command(name="v", help="create or activate virtualenv")
def venv() -> None:
    if os.getenv("VIRTUAL_ENV"):
        fatal("venv is activated already")

    if not Path(".venv").exists():
        run_command("python -m venv .venv", capture_output=False)
        run_command(".venv/bin/pip install -U pip setuptools", capture_output=False)


@app.command(name="d", help="uninstall all packages(+editable) from venv")
def uninstall() -> None:
    if not os.getenv("VIRTUAL_ENV"):
        fatal("venv is not activated")

    run_command("pip list --format freeze -e | xargs pip uninstall -y", capture_output=False)
    run_command("pip freeze | xargs pip uninstall -y", capture_output=False)


if __name__ == "__main__":
    app()
