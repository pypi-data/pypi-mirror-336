from mm_std import print_console

from mm_dev._common import Version, create_app

app = create_app()


@app.command(help="Convert hex to decimal")
def main(hex_value: str, _version: Version = None) -> None:
    print_console(int(hex_value, 16))


if __name__ == "__main__":
    app()
