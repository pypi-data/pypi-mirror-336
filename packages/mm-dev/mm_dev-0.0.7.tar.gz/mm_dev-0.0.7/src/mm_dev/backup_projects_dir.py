from mm_std import print_console, run_command

from mm_dev._common import Version, create_app

app = create_app()


@app.command(help="Backup a dir with projects.")
def main(src_path: str, dest_path: str, _version: Version = None) -> None:
    exclude_list = [".idea"]
    exclude_list += ["target/", "node_modules/", ".venv/", "__pycache__/", ".mypy_cache/", ".pytest_cache/", ".ruff_cache/"]
    exclude_list += ["**/dist/*.gz", "**/dist/*.whl"]
    exclude_list += [".coverage"]

    exclude = " ".join(f"--exclude={e}" for e in exclude_list)
    cmd = f"rsync -azvhP {exclude} {src_path} {dest_path}"
    run_command(cmd, capture_output=False, echo_cmd_console=True)
    print_console("done")


if __name__ == "__main__":
    app()
