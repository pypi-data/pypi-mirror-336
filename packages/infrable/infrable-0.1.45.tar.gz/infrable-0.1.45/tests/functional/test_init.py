import shutil
from pathlib import Path

from sh import infrable

from infrable import __version__

data = Path("tests/data")


def gen_test_data():
    Path("infra.py").unlink(missing_ok=True)
    shutil.rmtree("templates", ignore_errors=True)
    shutil.rmtree("modules", ignore_errors=True)
    infrable.init(_out=data.joinpath("pre_init"))
    infrable.init(_out=data.joinpath("post_init"))


def test_version():
    assert infrable.version().strip() == f"infrable {__version__}"


def test_init():
    Path("infra.py").unlink(missing_ok=True)
    shutil.rmtree("modules", ignore_errors=True)
    shutil.rmtree("templates", ignore_errors=True)
    assert infrable.init() == data.joinpath("pre_init").read_text()
    assert infrable.init() == data.joinpath("post_init").read_text()
