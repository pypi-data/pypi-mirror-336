from importlib.abc import Traversable
import re
from pathlib import Path
from random import shuffle
from typing import Annotated

import yaml
from auto_name_enum import AutoNameEnum, auto
from loguru import logger
from pydantic import BaseModel, Field, model_validator

from drivel.constants import DEFAULT_THEME
from drivel.exceptions import ThemeNotFound, ThemeReadError, DuplicateTheme, ThemeWriteError
from drivel.utilities import asset_root


Kinds = dict[str, list[str]]
kind_pattern = r"^[a-z0-9-]+$"


class Display(AutoNameEnum):
    kebab_case = auto()
    snake_case = auto()
    title_case = auto()
    upper_case = auto()


class ThemeMetadata(BaseModel):
    attribution: str | None = None
    explanation: str | None = None


class Theme(BaseModel):
    name: Annotated[str, Field(exclude=True)]
    default: str
    kinds: Kinds
    metadata: ThemeMetadata

    @model_validator(mode="after")
    def validate_theme(self) -> "Theme":
        if self.default not in self.kinds:
            raise ValueError("Default kind not found in kinds")
        for kind, items in self.kinds.items():
            if not re.match(kind_pattern, kind):
                raise ValueError(f"Kind name '{kind}' has invalid characters")
            if not items:
                raise ValueError(f"Kind '{kind}' has no items")
            for item in items:
                if not re.match(kind_pattern, item):
                    raise ValueError(f"Item '{item}' in kind '{kind}' has invalid characters")
        return self

    def give(
        self,
        max_count: int | None = None,
        kind: str | None = None,
        do_shuffle: bool = False,
    ) -> list[str]:
        logger.debug(f"Giving items from {self.name} for kind '{kind}'")
        if kind is None:
            kind = self.default
        if kind == "all":
            items = [i for k in self.kinds.values() for i in k]
        else:
            items = self.kinds[kind]
        if do_shuffle:
            shuffle(items)
        if max_count is None:
            return items
        return items[:max_count]

    @staticmethod
    def _find(name: str, *search_paths: Path | Traversable) -> Path | Traversable:
        for search_path in search_paths:
            for path in search_path.iterdir():
                if path.is_file() and path.name == f"{name}.yaml":
                    return path
        raise ThemeNotFound(f"Theme '{name}' not found in paths: {search_paths}")

    @classmethod
    def loads(cls, text: str, name: str) -> "Theme":
        data = yaml.safe_load(text)
        theme = Theme(name=name, **data)

        return theme

    @classmethod
    def load(cls, name: str = DEFAULT_THEME, *extra_paths: Path) -> "Theme":
        path = cls._find(name, asset_root, *extra_paths)

        with ThemeReadError.handle_errors(f"Couldn't read theme '{name}' from {path}"):
            text = path.read_text()
            theme = cls.loads(text, name)

        return theme

    def dump(self, target: Path) -> None:
        yaml_text = yaml.dump(self.model_dump())
        theme_path = target / f"{self.name}.yaml"
        with ThemeWriteError.handle_errors(f"Couldn't write theme '{self.name}' to {theme_path}"):
            theme_path.write_text(yaml_text)


    @classmethod
    def names(cls, *extra_paths: Path) -> set[str]:
        names: set[str] = set()
        for asset in asset_root.iterdir():
            if not asset.is_file():
                continue
            (name, ext) = asset.name.rsplit('.', 1)
            if ext != "yaml":
                continue
            names.add(name)

        for extra_path in extra_paths:
            for asset in extra_path.iterdir():
                if not asset.is_file():
                    continue
                if asset.suffix != ".yaml":
                    continue
                name = asset.stem
                DuplicateTheme.require_condition(name not in names, f"Duplicate theme name found in {extra_path}: {name}")
                names.add(name)

        return names
