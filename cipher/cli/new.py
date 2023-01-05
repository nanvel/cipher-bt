from pathlib import Path

import typer


new_cmd = typer.Typer()


@new_cmd.command()
def new():
    pass


@new_cmd.command()
def repository(name: str):
    print("New repo ...")
    print(path.resolve())
