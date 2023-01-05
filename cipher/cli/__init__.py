import typer

from .new import new_cmd


app = typer.Typer()
app.add_typer(new_cmd, name="new")


@app.callback()
def callback():
    """Cipher - trading strategy backtester."""


@app.command()
def run():
    pass
