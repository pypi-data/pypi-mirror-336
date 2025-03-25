from pathlib import Path

from auto_name_enum import AutoNameEnum, auto


class ThemeListOutputFormat(AutoNameEnum):
    json = auto()
    spaces = auto()
    lines = auto()


class ThemeOutputFormat(AutoNameEnum):
    json = auto()
    yaml = auto()


SHARE_DIR: Path = Path.home() / ".local/share/drivel"
CONFIG_DIR: Path = Path.home() / ".config/drivel"
CACHE_DIR: Path = Path.home() / ".cache/drivel"

SETTINGS_FILE_NAME: str = "settings.json"
EXTRA_THEMES_DIR: str = "extra-themes"
