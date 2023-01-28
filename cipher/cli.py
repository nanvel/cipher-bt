import typer
from pathlib import Path

from .models import Template
from .container import Container


app = typer.Typer()


@app.callback()
def callback():
    """Cipher - trading strategy backtester."""


@app.command()
def init(path: Path = typer.Argument(default=".", file_okay=False, resolve_path=True)):
    """Init directory / strategies repository."""
    container = Container()
    container.init_resources()
    use_case = container.init_repository()

    use_case.call(path)


@app.command()
def new(name: str, template: Template = Template.default):
    """Create a new strategy file from template."""
    container = Container()
    container.init_resources()
    use_case = container.create_strategy()

    use_case.call(name=name, template=template)
