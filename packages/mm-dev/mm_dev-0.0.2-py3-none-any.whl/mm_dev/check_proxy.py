import asyncio
from typing import cast
from urllib.parse import urlparse

import anyio
from mm_std import ahr, print_plain

from mm_dev._common import Version, create_app

app = create_app()


@app.command(help="Check a proxy")
def main(proxy_url: str, _version: Version = None) -> None:
    anyio.run(_main, proxy_url)


if __name__ == "__main__":
    app()


async def _main(proxy_url: str) -> None:
    httpbin_res, ipify = await asyncio.gather(httpbin_check(proxy_url), ipify_check(proxy_url))

    print_plain(f"proxy:\t\t{urlparse(proxy_url).hostname}")
    print_plain(f"httpbin.org:\t{httpbin_res}")
    print_plain(f"ipify.org:\t{ipify}")


async def httpbin_check(proxy: str) -> str:
    res = await ahr("https://httpbin.org/ip", proxy=proxy, timeout=5)
    if res.error is not None:
        return res.error
    if isinstance(res.json, dict) and "origin" in res.json:
        return cast(str, res.json["origin"])
    return res.body


async def ipify_check(proxy: str) -> str:
    res = await ahr("https://api.ipify.org/?format=json", proxy=proxy, timeout=5)
    if res.error is not None:
        return res.error
    if isinstance(res.json, dict) and "ip" in res.json:
        return cast(str, res.json["ip"])
    return res.body
