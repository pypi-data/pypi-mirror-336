from sh import infrable

from infrable import __version__


def test_custom_module():
    assert "[WORKFLOW] Provision Ubuntu host" in infrable.cloud(
        "provision-ubuntu-host", "--help"
    )
