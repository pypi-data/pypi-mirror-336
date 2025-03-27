from infrable import Host, Service, infra


def test_items():
    assert len(infra.items) == 27
    assert infra.items["dev"] == "dev"


def test_item_types():
    assert len(infra.item_types) == 11
    assert infra.item_types[Host]["dev_host"].fqdn == "dev.example.com"
    assert infra.item_types[Service]["nginx"].host.fqdn == "dev.example.com"


def test_hosts():
    assert len(infra.hosts) == 3
    assert infra.hosts["dev_host"].fqdn == "dev.example.com"


def test_services():
    assert len(infra.services) == 2
    assert infra.services["nginx"].host.fqdn == "dev.example.com"


def test_host_groups():
    assert len(infra.host_groups) == 1
    assert infra.host_groups["managed_hosts"][0].fqdn == "dev.example.com"


def test_typers():
    assert len(infra.typers) == 3
    assert infra.typers["nginx"].registered_commands[0].name == "reload"


def test_metas():
    assert len(infra.metas) == 0


def test_by_fqdn():
    assert infra.by_fqdn["dev.example.com"].fqdn == "dev.example.com"


def test_by_ip():
    assert infra.by_ip["127.0.0.1"].fqdn == "dev.example.com"


def test_get_host():
    assert infra.get_host("dev_host").fqdn == "dev.example.com"
    assert infra.get_host("dev.example.com").fqdn == "dev.example.com"
    assert infra.get_host("127.0.0.1").fqdn == "dev.example.com"
    assert infra.get_host("foo") == None
