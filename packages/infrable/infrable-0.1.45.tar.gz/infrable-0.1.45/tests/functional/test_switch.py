from sh import infrable

from infrable import __version__


def test_switch():
    infrable.switch.env.beta()
    assert infrable.switch.env(_tty_out=False).strip() == "beta"
    assert infrable.switches(_tty_out=False).strip() == "env = beta"

    infrable.switch.env.prod()
    assert infrable.switch.env(_tty_out=False).strip() == "prod"
    assert infrable.switches(_tty_out=False).strip() == "env = prod"

    infrable.env.dev()
    assert infrable.switch.env(_tty_out=False).strip() == "dev"
    assert infrable.switches(_tty_out=False).strip() == "env = dev"
