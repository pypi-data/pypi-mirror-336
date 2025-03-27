import shutil
from pathlib import Path

from sh import infrable


def pytest_configure(config):
    Path("infra.py").unlink(missing_ok=True)
    shutil.rmtree("templates", ignore_errors=True)
    shutil.rmtree("modules", ignore_errors=True)
    infrable.init()
    infrable.env.dev()
