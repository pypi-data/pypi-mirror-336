from sh import infrable

from infrable import __version__


def test_remote():
    out = infrable.remote("--help")
    assert "-" in out
    assert "affected-hosts" in out
    assert "infra-hosts" in out
    assert "dev_host" in out
    assert "beta_host" in out
    assert "prod_host" in out
    assert "managed_hosts" in out
