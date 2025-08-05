from pathlib import Path

import typer

from cipher.container import Container
from cipher.models import Template
from cipher.settings import Settings

app = typer.Typer()


@app.callback()
def callback():
    """Cipher - trading strategy backtester."""


@app.command()
def init(path: Path = typer.Argument(default=".", file_okay=False, resolve_path=True)):
    """Init directory / strategies repository."""
    container = Container()
    container.config.from_dict(Settings().model_dump())
    container.init_resources()
    use_case = container.init_repository()

    use_case.call(path)


@app.command()
def new(name: str, template: Template = Template.default):
    """Create a new strategy file from template."""
    container = Container()
    container.config.from_dict(Settings().model_dump())
    container.init_resources()
    use_case = container.create_strategy()

    use_case.call(name=name, template=template)
