import typer
from click import Choice

from infrable import infra

app = typer.Typer(no_args_is_help=True)


def _create_switch_command(switch):
    def main(
        value: str = typer.Argument(None, click_type=Choice(list(switch.options))),
        options: bool = False,
    ):
        if options:
            for opt in sorted(switch.options):
                print(opt)
            return

        if value is None:
            print(switch())
        else:
            switch.set(value)

    return main


for name, switch in infra.switches.items():
    help = f"Get or set the value of the {name} switch."
    cmd = _create_switch_command(switch)
    app.command(name=name, help=help)(cmd)
