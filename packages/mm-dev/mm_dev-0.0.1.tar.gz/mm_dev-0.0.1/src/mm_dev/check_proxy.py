from urllib.parse import urlparse

from mm_std import hr, print_console

from mm_dev._common import Version, create_app

app = create_app()


@app.command(help="Check a proxy")
def main(proxy: str, _version: Version = None) -> None:
    res = hr("https://httpbin.org/ip", proxy=proxy)
    if res.is_error():
        return print_console(f"failed: {res.error}")

    if res.json and urlparse(proxy).hostname == res.json.get("origin"):
        print_console("ok")
    else:
        print_console("failed")


if __name__ == "__main__":
    app()
