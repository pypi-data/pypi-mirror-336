from mm_std import fatal, run_command

from mm_dev._common import create_app

app = create_app(multi_command=True)


@app.command(name="l", help="List servers")
def list_servers() -> None:
    run_command(
        "hcloud server list -o columns=name,ipv4,private_net,datacenter,status,type,volumes",
        capture_output=False,
        echo_cmd_console=True,
    )


@app.command(name="r", help="Rebuild a server")
def rebuild_server(server: str) -> None:
    if server != "test":
        confirm = input("Sure? Type the server name again: ")
        if server != confirm:
            fatal("Confirm failed!")

    run_command(f"hcloud server rebuild '{server}' --image=ubuntu-22.04", capture_output=False, echo_cmd_console=True)
    run_command(f"dh {server}", capture_output=False, echo_cmd_console=True)


@app.command(name="d", help="Delete a server")
def delete_server(server: str) -> None:
    confirm = input("Sure? Type the server name again: ")
    if server != confirm:
        fatal("Confirm failed!")

    run_command(f"hcloud server delete '{server}'", capture_output=False, echo_cmd_console=True)


if __name__ == "__main__":
    app()
