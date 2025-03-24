from mm_std import hr, print_console

from mm_dev._common import Version, create_app

app = create_app()


@app.command(help="Check my ip via httpbin.org, ip-api.com")
def main(_version: Version = None) -> None:
    res = hr("https://httpbin.org/ip")
    ip = res.json["origin"]
    print_console(ip)
    res = hr(f"http://ip-api.com/json/{ip}")
    print_console(res.json)


if __name__ == "__main__":
    app()
