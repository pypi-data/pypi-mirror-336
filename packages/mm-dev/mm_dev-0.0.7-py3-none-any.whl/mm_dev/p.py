import os
from pathlib import Path
from typing import Optional

from mm_std import fatal, run_command
from typer import Argument

from mm_dev._common import create_app

app = create_app(multi_command=True)


@app.command(name="o", help="uv pip list --outdated")
def pip_list_outdated() -> None:
    run_command("uv pip list --outdated", capture_output=False)


@app.command(name="l", help="uv pip list")
def pip_list() -> None:
    run_command("uv pip list", capture_output=False)


@app.command(name="i", help="install packages or requirements.txt")
def install(packages: Optional[str] = Argument(None)) -> None:  # noqa: UP007
    if not os.getenv("VIRTUAL_ENV"):
        fatal("venv is not activated")
    if packages:
        run_command(f"uv pip install {packages}", capture_output=False)
        return
    run_command("uv pip install -Ur requirements.txt", capture_output=False)


@app.command(name="v", help="create .venv")
def venv() -> None:
    if os.getenv("VIRTUAL_ENV"):
        fatal("venv is activated already")

    if Path(".venv").exists():
        fatal(".venv exists")
    run_command("uv venv", capture_output=False)


@app.command(name="d", help="uninstall all packages(+editable) from venv")
def uninstall() -> None:
    if not os.getenv("VIRTUAL_ENV"):
        fatal("venv is not activated")

    run_command("uv pip list --format freeze -e | xargs uv pip uninstall -y", capture_output=False)
    run_command("uv pip freeze | xargs pip uninstall", capture_output=False)


@app.command(name="c", help="uv cache clean {package}")
def clean_cache(package: str) -> None:
    run_command(f"uv cache clean {package}", capture_output=False)


if __name__ == "__main__":
    app()
