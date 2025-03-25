import sys
from importlib import resources

if sys.version_info >= (3, 12):
    from importlib.resources.abc import Traversable
else:
    from importlib.abc import Traversable


asset_root = resources.files(f"{__package__}.assets")


def asset_path(file_name: str) -> Traversable:
    return asset_root / file_name
