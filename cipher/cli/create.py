import typer

from ..container import Container


create_cmd = typer.Typer()


@create_cmd.command()
def new():
    pass


@create_cmd.command()
def repository(name: str):
    container = Container()
    use_case = container.create_repository()

    use_case.call(name)
