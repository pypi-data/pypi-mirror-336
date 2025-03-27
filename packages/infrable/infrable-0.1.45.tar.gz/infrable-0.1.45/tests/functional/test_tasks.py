from sh import infrable

from infrable import __version__


def test_tasks():
    assert "[TASK] Reload nginx" in infrable.nginx.reload("--help")
