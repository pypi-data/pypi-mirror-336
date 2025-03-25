import socket

from mm_std import run_command

from mm_dev._common import Version, create_app

app = create_app()


@app.command(help="Delete records from .ssh/known_hosts")
def main(hosts: list[str], _version: Version = None) -> None:
    for host in hosts:
        process_host(host)


def process_host(host: str) -> None:
    run_command(f"ssh-keygen -R {host}", capture_output=False, echo_cmd_console=True)
    try:
        ip = socket.gethostbyname(host)
        run_command(f"ssh-keygen -R {ip}", capture_output=False, echo_cmd_console=True)
    except socket.gaierror:
        pass


if __name__ == "__main__":
    app()
