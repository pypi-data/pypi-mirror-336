import typer
from mm_std import run_command

from mm_dev._common import create_app

app = create_app(multi_command=True)


@app.command(name="d", help="git diff")
def diff() -> None:
    run_command("git diff", capture_output=False, echo_cmd_console=True)


@app.command(name="l", help="""git log --pretty=format:"%ar / %an / %s\"""")
def log() -> None:
    run_command("""git log --pretty=format:"%ar / %an / %s\"""", capture_output=False)


@app.command(name="t", help="git tag --sort=-creatordate")
def tag() -> None:
    run_command("git tag --sort=-creatordate", capture_output=False, echo_cmd_console=True)


@app.command(name="s", help="git status --untracked-files --short")
def status() -> None:
    run_command("git status --untracked-files --short", capture_output=False, echo_cmd_console=True)


@app.command(name="c", help="git clone")
def clone(repo: str) -> None:
    run_command(f"git clone {repo}", capture_output=False, echo_cmd_console=True)


@app.command(name="p", help="git add & commit & push")
def push(message: str = typer.Argument("update")) -> None:
    run_command(f"git add . && git commit -m '{message}' && git push", capture_output=False, echo_cmd_console=True)


@app.command(name="at", help="add tag local and push")
def add_tag(version: str) -> None:
    run_command(
        f"git tag -a '{version}' -m '{version}' && git push origin {version}",
        capture_output=False,
        echo_cmd_console=True,
    )


@app.command(name="dt", help="delete tag local and push")
def delete_tag(version: str) -> None:
    run_command(f"git tag -d '{version}' && git push origin :refs/tags/{version}", capture_output=False, echo_cmd_console=True)


@app.command(name="amend", help="git add . && git commit --amend --no-edit && git push --force")
def amend() -> None:
    run_command("git add . && git commit --amend --no-edit && git push --force", capture_output=False, echo_cmd_console=True)


@app.command(name="reset", help="git reset --hard HEAD")
def reset() -> None:
    run_command("git reset --hard HEAD", capture_output=False, echo_cmd_console=True)


if __name__ == "__main__":
    app()
