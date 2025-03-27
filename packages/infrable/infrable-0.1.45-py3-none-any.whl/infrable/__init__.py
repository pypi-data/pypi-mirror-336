__version__ = "0.1.45"


from pathlib import Path

INFRA_MODULE_NAME = "infra"
IS_PROJECT_DIR = Path(f"{INFRA_MODULE_NAME}.py").exists()

if IS_PROJECT_DIR:
    from infrable.host import Host
    from infrable.meta import Meta
    from infrable.readfile import readfile
    from infrable.service import Service
    from infrable.switch import Switch
    from infrable.utils import concurrent, concurrentcontext
