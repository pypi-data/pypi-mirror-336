from typing import Iterable, Optional

import typer
from tqdm import tqdm

from infrable import Host, files, infra, utils

app = typer.Typer(no_args_is_help=True)


@app.command(name="-")
def from_stdin(command: str, workers: Optional[int] = None):
    """Execute a script on the list of hosts passed via stdin."""

    hosts = []
    for line in typer.get_text_stream("stdin").readlines():
        host = line.split(maxsplit=1)[0].split("@", 1)[-1].strip()
        if not host:
            continue
        for host in infra.filtered_hosts(only=[host]):
            hosts.append(host)

    _execute_batch(hosts, command=command, workers=workers)


@app.command()
def infra_hosts(
    command: str,
    only: Optional[list[str]] = None,
    workers: Optional[int] = None,
):
    """Execute a script on the hosts listed in the infra."""

    hosts = infra.hosts.values()
    if only:
        hosts = infra.filtered_hosts(only=only)

    _execute_batch(hosts, command=command, workers=workers)


@app.command()
def affected_hosts(
    command: str,
    only: Optional[list[str]] = None,
    workers: Optional[int] = None,
):
    """Execute a script on the affected hosts in the last deployment."""

    hosts = files.affected_hosts()

    if only:
        only_hosts = set(h.fqdn for h in infra.filtered_hosts(only=only))
        hosts = (h for h in hosts if h.fqdn in only_hosts)

    _execute_batch(hosts, command=command, workers=workers)


def _create_host_groups_command(group):
    def main(
        command: str, only: Optional[list[str]] = None, workers: Optional[int] = None
    ):
        hosts = group
        if only:
            only_hosts = set(h.fqdn for h in infra.filtered_hosts(only=only))
            hosts = (h for h in hosts if h.fqdn in only_hosts)

        _execute_batch(hosts, command=command, workers=workers)

    return main


for name, group in infra.host_groups.items():
    help = f"Execute a script on {name} hosts."
    cmd = _create_host_groups_command(group)
    app.command(name=name, help=help)(cmd)


def _create_host_command(host):
    def main(command: str):
        host.remote()(command, _fg=True)

    return main


for name, host in infra.hosts.items():

    help = f"Execute a script on {name}."
    cmd = _create_host_command(host)
    app.command(name=name, help=help)(cmd)


def _execute_batch(hosts: Iterable[Host], command: str, workers: int | None):
    hosts = {h.ip: h for h in hosts}.values()
    fn = lambda host: (host, host.remote()(command, _err_to_out=True))
    with utils.concurrentcontext(fn, hosts, workers=workers) as results:
        for host, result in tqdm(results, total=len(hosts)):
            typer.secho(f"╭ {host}", bold=True)
            print(result)
            print()
