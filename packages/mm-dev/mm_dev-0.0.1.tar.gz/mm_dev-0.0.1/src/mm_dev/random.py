import secrets
import string

from mm_std import print_console
from typer import Option

from mm_dev._common import Version, create_app

app = create_app()


@app.command(help="Generate a random password")
def main(
    length: int = Option(16, "--length", "-l"), punctuation: bool = Option(False, "--punctuation", "-p"), _version: Version = None
) -> None:
    alphabet = string.ascii_letters + string.digits
    if punctuation:
        alphabet += string.punctuation
    password = "".join(secrets.choice(alphabet) for _ in range(length))
    print_console(password)


if __name__ == "__main__":
    app()
