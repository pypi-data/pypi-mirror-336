from functools import wraps
from typing import Callable, Concatenate, ParamSpec, TypeAlias, TypeVar

import typer

from drivel.cli.constants import CACHE_DIR
from drivel.cli.utilities import attach_to_context, ensure_storage_path

P = ParamSpec("P")
R = TypeVar("R")
WithContext: TypeAlias = Callable[Concatenate[typer.Context, P], R]


def attach_cache_to_context(ctx: typer.Context) -> None:
    attach_to_context(ctx, "cache_dir", ensure_storage_path(CACHE_DIR, "cache"))

def attach_cache(func: WithContext[P, R]) -> WithContext[P, R]:
    @wraps(func)
    def wrapper(ctx: typer.Context, *args: P.args, **kwargs: P.kwargs) -> R:
        attach_cache_to_context(ctx)
        return func(ctx, *args, **kwargs)

    return wrapper
