from pathlib import Path
from typing import Optional

import typer

from infrable import files

app = typer.Typer(no_args_is_help=True)


@app.command(help=files.affected_hosts.__doc__)
def affected_hosts(only: Optional[list[str]] = None):
    for host in files.affected_hosts(only=only):
        print(host)


@app.command(help=files.deploy.__doc__)
def deploy(
    path: Optional[Path] = typer.Argument(None),
    only: Optional[list[str]] = None,
    yes: bool = False,
    workers: Optional[int] = None,
):
    files.deploy(path, only=only, yes=yes, workers=workers)


@app.command(help=files.recover.__doc__)
def recover(
    path: Optional[Path] = typer.Argument(None),
    yes: bool = False,
    workers: Optional[int] = None,
):
    files.recover(path, yes=yes, workers=workers)


@app.command(help=files.gen.__doc__)
def gen(
    path: Optional[Path] = typer.Argument(None),
    only: Optional[list[str]] = None,
):
    files.gen(path, only=only)


@app.command(help=files.backup.__doc__)
def backup():
    files.backup()


@app.command(help=files.pull.__doc__)
def pull(workers: Optional[int] = None):
    files.pull(workers=workers)


@app.command(help=files.diff.__doc__)
def diff():
    files.diff()


@app.command(help=files.push.__doc__)
def push(yes: bool = False, workers: Optional[int] = None):
    files.push(yes=yes, workers=workers)


@app.command(help=files.revert.__doc__)
def revert(path: Path = typer.Argument(None)):
    files.revert(path)
