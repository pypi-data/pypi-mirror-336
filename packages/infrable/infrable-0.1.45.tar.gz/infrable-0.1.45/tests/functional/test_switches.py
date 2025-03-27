from pathlib import Path

from sh import infrable

from infrable import __version__

data = Path("tests/data")


def gen_test_data():
    infrable.switches(_out=data.joinpath("switches"))
    infrable.switches(repr=True, _out=data.joinpath("switches_repr"))
    infrable.switches(
        format="{name},{foo},{init}", _out=data.joinpath("switches_format")
    )


def test_switches():
    assert infrable.switches(_tty_out=False) == data.joinpath("switches").read_text()
    assert "env = Switch(options={'" in data.joinpath("switches_repr").read_text()
    assert (
        infrable.switches(format="{name},,{init}", _tty_out=False)
        == data.joinpath("switches_format").read_text()
    )
