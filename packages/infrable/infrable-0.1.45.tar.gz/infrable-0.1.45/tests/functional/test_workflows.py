from sh import infrable

from infrable import __version__


def test_workflows():
    assert "[WORKFLOW] Deploy nginx files" in infrable.deploy.nginx("--help")
