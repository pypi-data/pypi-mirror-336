from typing import Optional

import typer
from click import Choice

app = typer.Typer(no_args_is_help=True)

from infrable import IS_PROJECT_DIR, __version__, init


@app.command()
def version():
    """Print the version."""
    print(f"infrable {__version__}")


@app.command(name="init")
def init_():
    """Bootstrap a dummy project."""
    init.init()


if IS_PROJECT_DIR:
    from infrable import infra
    from infrable.cli import files, remote, switch

    @app.command()
    def hosts(format: Optional[str] = None, repr: bool = False):
        """List all hosts in the infrastructure."""

        for name, host in infra.hosts.items():
            if format:
                print(host.format(name, format=format))
            elif repr:
                print(f"{name} = {host.__repr__()}")
            else:
                print(f"{name} = {host}")

    @app.command()
    def services(format: Optional[str] = None, repr: bool = False):
        """List all services in the infrastructure."""

        for name, service in infra.services.items():
            if format:
                print(service.format(name, format=format))
            elif repr:
                print(f"{name} = {service.__repr__()}")
            else:
                print(f"{name} = {service}")

    @app.command()
    def switches(format: Optional[str] = None, repr: bool = False):
        """List all switches in the infrastructure."""

        for name, switch in infra.switches.items():
            if format:
                print(switch.format(name, format=format))
            elif repr:
                print(f"{name} = {switch.__repr__()}")
            else:
                print(f"{name} = {switch}")

    app.add_typer(files.app, name="files", help="Manage files.")
    app.add_typer(switch.app, name="switch", help="Manage switches.")
    app.add_typer(remote.app, name="remote", help="Execute remote commands.")

    for name, ext in infra.typers.items():
        app.add_typer(ext, name=name.replace("_", "-"))

    if sw := infra.switches.get("env"):
        # Alias for 'infrable switch env'
        def env(
            value: str = typer.Argument(None, click_type=Choice(list(sw.options))),
            options: bool = False,
        ):
            """Alias for `infrable switch env`."""

            if options:
                for opt in sorted(sw.options):
                    print(opt)
                return

            if value is None:
                print(sw())
            else:
                sw.set(value)

        app.command()(env)
