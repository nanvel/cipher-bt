import typer

from .create import create_cmd


app = typer.Typer()
app.add_typer(create_cmd, name="create")


@app.callback()
def callback():
    """Cipher - trading strategy backtester."""


@app.command()
def run():
    pass
