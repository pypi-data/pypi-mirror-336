from mm_std import print_console

from mm_dev._common import Version, create_app

app = create_app()


@app.command(help="Convert decimal to hex")
def main(value: int, _version: Version = None) -> None:
    print_console(hex(value))


if __name__ == "__main__":
    app()
