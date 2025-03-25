from dataclasses import dataclass
from pathlib import Path

from drivel.cli.config import Settings


@dataclass
class CliContext:
    settings: Settings | None = None
    cache_dir: Path | None = None
    share_dir: Path | None = None
    extra_themes: Path | None = None
