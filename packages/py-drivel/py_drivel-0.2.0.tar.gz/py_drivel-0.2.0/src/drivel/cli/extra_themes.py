from functools import wraps
from typing import Callable, Concatenate, ParamSpec, TypeAlias, TypeVar

import typer

from drivel.cli.cache import attach_cache_to_context
from drivel.cli.constants import EXTRA_THEMES_DIR
from drivel.cli.utilities import attach_to_context, ensure_storage_path

P = ParamSpec("P")
R = TypeVar("R")
WithContext: TypeAlias = Callable[Concatenate[typer.Context, P], R]


def attach_extra_themes_to_context(ctx: typer.Context) -> None:
    extra_themes_dir = ctx.obj.cache_dir / EXTRA_THEMES_DIR
    attach_to_context(ctx, "extra_themes", ensure_storage_path(extra_themes_dir, "extra-themes"))

def attach_extra_themes(func: WithContext[P, R]) -> WithContext[P, R]:
    @wraps(func)
    def wrapper(ctx: typer.Context, *args: P.args, **kwargs: P.kwargs) -> R:
        attach_cache_to_context(ctx)
        attach_extra_themes_to_context(ctx)
        return func(ctx, *args, **kwargs)

    return wrapper
