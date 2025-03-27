import random
import shutil
import subprocess as sp
import time
from datetime import datetime
from difflib import unified_diff
from pathlib import Path
from shlex import quote as q
from typing import IO, Any, Iterable, Iterator

import typer
from click import Choice
from tqdm import tqdm

from infrable import errors, infra, paths, utils
from infrable.host import Host
from infrable.template import Metadata, render


def _iter_files(root: Path, pattern: str) -> Iterator[Path]:
    # NOTE: Path.glob doesn't traverse symlinks
    # See: https://bugs.python.org/issue33428
    for path in root.glob(pattern):
        path = Path(path)
        if path.is_file():
            yield path
        elif path.is_symlink():
            yield from _iter_files(path, pattern)


def affected_hosts(only: Iterable[str] | None = None) -> list[Host]:
    """List the affected hosts as per the files diff."""

    _only = list(infra.filtered_hosts(only=only))
    only_hosts = set(h.ip for h in _only) | set(h.fqdn for h in _only if h.fqdn)

    hosts = {}
    for new in _iter_files(paths.files, "**/*.new"):
        old = _old_path(new)
        if not _diff(new=new, old=old):
            continue
        remote, _ = str(new.relative_to(paths.files)).removesuffix(".new").split("/", 1)
        host = remote.split("@", 1)[-1]
        if only and host not in only_hosts:
            continue
        if host not in hosts:
            hosts[host] = infra.get_host(host)
    return list(hosts.values())


def gen(path: Path | str | None = None, only: Iterable[str] | None = None):
    """Generate files by rendering the templates with context from infra."""

    if paths.files.exists():
        shutil.rmtree(str(paths.files))

    path = Path(path or paths.templates)

    if path.is_dir():
        templates = [p for p in _iter_files(path, "**/*")]
    else:
        templates = [path]

    _only = list(infra.filtered_hosts(only=only))
    only_hosts = set(h.ip for h in _only) | set(h.fqdn for h in _only if h.fqdn)
    for src in templates:
        # Render the template metadata
        typer.secho(f"╭ {src}", bold=True)

        meta = Metadata.parse(src, infra.items)

        if meta.skip:
            print("╰ skip: true")
            print()
            continue

        for i, dest in enumerate(meta.dest):
            if i + 1 == len(meta.dest):
                print("╰─ ", end="")
            else:
                print("├─ ", end="")

            # Render the template for each destination

            remote, loc = dest.loc.split(":", 1)
            host = remote.split("@", 1)[-1]
            if not host or host == "None" or (only and host not in only_hosts):
                print(f"skipping {dest.loc}")
                continue
            outpath = paths.files / remote / (loc.removeprefix("/") + ".new")
            outpath.parent.mkdir(exist_ok=True, parents=True)
            rendered = render(src, dest.loc, infra.items, **dest.ctx)
            outpath.write_text(rendered)
            print(outpath)
        print()


def pull(workers: int | None = None):
    """For each generated file pull the current version from the server."""

    if not paths.files.exists():
        return

    for old in _iter_files(paths.files, "**/*.old"):
        old.unlink()

    new_files = list(_iter_files(paths.files, "**/*.new"))
    with utils.concurrentcontext(_pull, new_files, workers=workers) as results:
        for new, dest in tqdm(results, total=len(new_files)):
            typer.secho(f"╭ {new}", bold=True)
            print(f"╰ {dest}")
            print()


def backup():
    """Backup the files locally."""

    if not paths.files.exists():
        return

    dirname = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    backupdir = paths.backups / dirname
    while backupdir.exists():
        time.sleep(1)
        dirname = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        backupdir = paths.backups / dirname
    shutil.copytree(str(paths.files), str(backupdir))
    print(f"backup: {backupdir}")


def diff():
    """Diff the generated files with the pulled versions."""

    for new in _iter_files(paths.files, "**/*.new"):
        old = _old_path(new)
        if d := _diff(new=new, old=old):
            _print_diff(d)
            print()


def push(yes: bool = False, workers: int | None = None):
    """Diff and push the generated files to the remote server."""

    to_push = []
    for new in _iter_files(paths.files, "**/*.new"):
        remote, loc = (
            str(new.relative_to(paths.files)).removesuffix(".new").split("/", 1)
        )

        old = _old_path(new)
        remote_dest = f"{remote}:/{loc}"

        if d := _diff(new=new, old=old):
            _print_diff(d)
            if not yes:
                ans = typer.prompt(
                    f"Push?", type=Choice(["y", "n", "all"]), default="y"
                )
                match ans.lower():
                    case "n":
                        new.unlink()
                        old.unlink()
                        continue
                    case "all":
                        yes = True
            to_push.append({"new": new, "remote_dest": remote_dest})
        else:
            print(f"skipping {remote_dest}")
            new.unlink()
            old.unlink()
        print()
    with utils.concurrentcontext(
        lambda d: _push(**d), to_push, workers=workers
    ) as results:
        for new, remote_dest in tqdm(results, total=len(to_push)):
            typer.secho(f"╭ {new}", bold=True)
            print(f"╰ {remote_dest}")
            print()


def revert(path: Path | str | None = None):
    """Revert files from backup."""

    if path is None:
        path = max(paths.backups.glob("*"))

    print(f"reverting from: {path}")

    for bkold in _iter_files(Path(path), "**/*.old"):
        bknew = Path(str(bkold).removesuffix(".old") + ".new")

        old = paths.files / bkold.relative_to(path)
        new = paths.files / bknew.relative_to(path)

        typer.secho(f"╭ {new}", bold=True)
        shutil.copy(str(bkold), str(new))

        print(f"╰ {old}")
        shutil.copy(str(bknew), str(old))


def deploy(
    path: Path | str | None = None,
    only: Iterable[str] | None = None,
    yes: bool = False,
    workers: int | None = None,
):
    """[WORKFLOW] generate, pull, backup, compare and push the generated files to the remote server."""

    if path or yes or typer.confirm("Generate fresh files?", default=True, err=True):
        gen(path, only=only)
        print()
        pull(workers=workers)
        print()
        backup()
    elif typer.confirm("Pull files from remote?", default=True, err=True):
        pull(workers=workers)
        print()
        backup()
    elif typer.confirm("Backup files locally?", default=True, err=True):
        backup()

    print()
    push(yes=yes, workers=workers)


def recover(
    path: Path | str | None = None, yes: bool = False, workers: int | None = None
):
    """[WORKFLOW] revert and push files from backup."""

    revert(path)
    print()
    push(yes=yes, workers=workers)


def _pull(new: Path) -> tuple[Path, str]:
    dest = str(new).removesuffix(".new") + ".old"
    remote, loc = str(new.relative_to(paths.files)).removesuffix(".new").split("/", 1)
    src = f"/{loc}"
    name = remote.split("@", 1)[-1]
    host = infra.get_host(name)
    if not host:
        raise errors.InvalidDestinationError(dest=dest)
    addr = f"{host.admin}@{host.ip}"
    _sudo_pull_file(addr, src, dest, admin_ssh_key=host.admin_ssh_key)
    return new, dest


def _push(new: Path, remote_dest: str) -> tuple[Path, str]:
    meta = Metadata.parse(new)
    dest = next(d for d in meta.dest if d.loc == remote_dest)
    chown = dest.chown or meta.chown
    chmod = dest.chmod or meta.chmod

    remote, loc = remote_dest.split(":", 1)
    dest = f"/{loc}"
    name = remote.split("@", 1)[-1]
    host = infra.get_host(name)
    if not host:
        raise errors.InvalidDestinationError(dest)
    addr = f"{host.admin}@{host.ip}"
    _sudo_push_file(
        addr,
        new,
        dest,
        chown=chown,
        chmod=chmod,
        admin_ssh_key=host.admin_ssh_key,
        execute=meta.execute,
    )
    return new, remote_dest


def _old_path(new: Path) -> Path:
    return Path(str(new).removesuffix(".new") + ".old")


def _diff(new: Path, old: Path) -> list[str]:
    new_lines = new.read_text().splitlines()
    old_lines = Path(old).read_text().splitlines()
    return list(unified_diff(old_lines, new_lines, fromfile=str(old), tofile=str(new)))


def _print_diff(diff: list[str]):
    for line in diff:
        if line.startswith("---"):
            typer.secho(line, fg=typer.colors.RED, bold=True)
        elif line.startswith("+++"):
            typer.secho(line, fg=typer.colors.GREEN, bold=True)
        elif line.startswith("-"):
            typer.secho(line, fg=typer.colors.RED)
        elif line.startswith("+"):
            typer.secho(line, fg=typer.colors.GREEN)

        elif line.startswith("@"):
            typer.secho(line, dim=True)
        else:
            print(line)


def _sudo_exec(
    address: str,
    command: list[str] | str,
    options: list[str] | None = None,
    shell: str | None = None,
    stdout: int | IO[Any] = sp.PIPE,
    stderr: int | IO[Any] = sp.PIPE,
    stdin: int | IO[Any] = sp.PIPE,
) -> sp.CompletedProcess[bytes]:
    if isinstance(command, list):
        command = sp.list2cmdline(command)
    if shell:
        command = sp.list2cmdline([shell, "-c", q(command)])
    options = options or []
    return sp.run(
        [
            "ssh",
            "-o",
            "StrictHostKeyChecking=no",
            *options,
            address,
            command,
        ],
        stdout=stdout,
        stderr=stderr,
        stdin=stdin,
    )


def _sudo_pull_file(
    address: str, remote_src: str, local_dest: str, admin_ssh_key: str | None = None
):
    options = None
    if admin_ssh_key:
        options = ["-i", admin_ssh_key]
    with Path(local_dest).open("w") as f:
        _sudo_exec(
            address,
            f"sudo test -f {q(remote_src)} && sudo cat -- {q(remote_src)} || true",
            options=options,
            stdout=f,
            stderr=sp.PIPE,
            stdin=sp.PIPE,
        ).check_returncode()


def _sudo_push_file(
    address: str,
    local_src,
    remote_dest,
    chmod: str | None = None,
    chown: str | None = None,
    admin_ssh_key: str | None = None,
    execute: bool = False,
):
    ts = time.time()
    rand = random.randint(0, 9999)
    tmpname = f"/tmp/infrable-push-{ts}.{rand}"
    parent = str(Path(remote_dest).parent)
    cmd = f"sudo tee -- {q(tmpname)}"  # as root for security

    # Change permissions and ownership before moving to final destination.
    # Else, you might end up getting locked from the server.
    if chmod:
        cmd = f"{cmd} && sudo chmod -- {q(chmod)} {q(tmpname)}"

    if chown:
        cmd = f"{cmd} && sudo chown -- {q(chown)} {q(tmpname)}"

    cmd += f" && sudo mkdir -p -- {q(parent)}"
    cmd += f" && sudo mv -f -- {q(tmpname)} {q(remote_dest)}"

    if execute:
        if not chmod:
            cmd += f" && sudo chmod u+rx -- {q(remote_dest)}"
        cmd += f" && sudo -- {q(remote_dest)}"

    options = None
    if admin_ssh_key:
        options = ["-i", admin_ssh_key]

    with Path(local_src).open("r") as f:
        _sudo_exec(address, cmd, options=options, stdin=f).check_returncode()
