import os
import shutil
from pathlib import Path

import pytest
from sh import infrable

from infrable import __version__, paths

data = Path("tests/data")


def gen_test_data():
    infrable.files.gen(_out=data.joinpath("pre_files_gen"))
    infrable.files.gen("templates/nginx", _out=data.joinpath("files_gen_nginx"))
    infrable.files.gen(
        "templates/nginx/web.j2", _out=data.joinpath("files_gen_nginx_web")
    )
    infrable.files.gen(_out=data.joinpath("post_files_gen"))
    _gen_old_files(copy=False)
    infrable.files.diff(_out=data.joinpath("files_diff"))


def _gen_old_files(copy: bool):
    for new in paths.files.glob("**/*.new"):
        old = (paths.files / new.relative_to(paths.files)).with_suffix(".old")
        text = new.read_text() if copy else ""
        old.write_text(text)


def test_files_gen():
    shutil.rmtree(paths.files, ignore_errors=True)
    assert set(infrable.files.gen(_tty_out=False).splitlines()) == set(
        data.joinpath("pre_files_gen").read_text().splitlines()
    )
    assert set(
        infrable.files.gen("templates/nginx", _tty_out=False).splitlines()
    ) == set(data.joinpath("files_gen_nginx").read_text().splitlines())
    assert set(
        infrable.files.gen("templates/nginx/web.j2", _tty_out=False).splitlines()
    ) == set(data.joinpath("files_gen_nginx_web").read_text().splitlines())
    assert set(infrable.files.gen(_tty_out=False).splitlines()) == set(
        data.joinpath("post_files_gen").read_text().splitlines()
    )


def test_files_diff():
    shutil.rmtree(paths.files, ignore_errors=True)
    infrable.files.gen()
    _gen_old_files(copy=True)
    assert infrable.files.diff(_tty_out=False) == ""
    _gen_old_files(copy=False)
    assert set(infrable.files.diff(_tty_out=False).splitlines()) == set(
        data.joinpath("files_diff").read_text().splitlines()
    )


def test_files_backup():
    infrable.files.gen()
    _gen_old_files(copy=False)
    backups_count = len(list(paths.backups.glob("*")))
    out = infrable.files.backup(_tty_out=False)
    assert out.strip().startswith(f"backup: {paths.backups}/")
    assert len(list(paths.backups.glob("*"))) == backups_count + 1


def test_files_revert():
    infrable.files.gen()
    _gen_old_files(copy=False)
    infrable.files.backup()

    news1, olds1 = [f.read_text() for f in paths.files.glob("**/*.new")], [
        f.read_text() for f in paths.files.glob("**/*.old")
    ]

    out = infrable.files.revert(_tty_out=False)
    assert out.strip().startswith(f"reverting from: {paths.backups}/")

    news2, olds2 = [f.read_text() for f in paths.files.glob("**/*.new")], [
        f.read_text() for f in paths.files.glob("**/*.old")
    ]

    assert news1 == olds2
    assert olds1 == news2

    bkpdir = out.split(": ", 1)[-1].strip()
    assert infrable.files.revert(bkpdir, _tty_out=False) == out


def test_files_affect_hosts():
    infrable.files.gen()
    _gen_old_files(copy=True)
    assert infrable.files("affected-hosts", _tty_out=False) == ""
    _gen_old_files(copy=False)
    assert (
        infrable.files("affected-hosts", _tty_out=False).strip()
        == "root@dev.example.com"
    )
    assert (
        infrable.files("affected-hosts", only="dev_host", _tty_out=False).strip()
        == "root@dev.example.com"
    )
    assert (
        infrable.files("affected-hosts", only="dev.example.com", _tty_out=False).strip()
        == "root@dev.example.com"
    )
    assert (
        infrable.files("affected-hosts", only="127.0.0.1", _tty_out=False).strip()
        == "root@dev.example.com"
    )
    assert (
        infrable.files("affected-hosts", only="managed_hosts", _tty_out=False).strip()
        == "root@dev.example.com"
    )
    assert (
        infrable.files("affected-hosts", only="prod_host", _tty_out=False).strip() == ""
    )


def test_symlinks():
    os.symlink("../tests/data", paths.templates / "symlink")
    try:
        with pytest.raises(Exception) as e:
            infrable.files.gen()
    except Exception as e:
        os.remove(paths.templates / "symlink")
        raise e


def test_hidden_files():
    hiddendir = paths.templates.joinpath(".config")
    hiddendir.mkdir(parents=True, exist_ok=True)
    hiddendir.joinpath(".hiddenfile").touch(exist_ok=True)

    try:
        with pytest.raises(Exception) as e:
            infrable.files.gen()
    except Exception as e:
        shutil.rmtree(hiddendir, ignore_errors=True)
        raise e
