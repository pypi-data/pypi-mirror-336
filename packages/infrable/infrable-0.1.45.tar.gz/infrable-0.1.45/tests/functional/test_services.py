from pathlib import Path

from sh import infrable

from infrable import __version__

data = Path("tests/data")


def gen_test_data():
    infrable.services(_out=data.joinpath("services"))
    infrable.services(repr=True, _out=data.joinpath("services_repr"))
    infrable.services(
        format="{name},{host.ip},{meta}", _out=data.joinpath("services_format")
    )


def test_services():
    assert infrable.services(_tty_out=False) == data.joinpath("services").read_text()
    assert (
        "nginx = Service(host=Host(ip='127.0.0.1"
        in data.joinpath("services_repr").read_text()
    )
    assert (
        infrable.services(format="{name},{host.ip},{meta}", _tty_out=False)
        == data.joinpath("services_format").read_text()
    )
