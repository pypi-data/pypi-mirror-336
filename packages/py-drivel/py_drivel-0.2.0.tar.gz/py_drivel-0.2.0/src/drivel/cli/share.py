from functools import wraps
from typing import Callable, Concatenate, ParamSpec, TypeAlias, TypeVar

import typer

from drivel.cli.constants import SHARE_DIR
from drivel.cli.utilities import attach_to_context, ensure_storage_path

P = ParamSpec("P")
R = TypeVar("R")
WithContext: TypeAlias = Callable[Concatenate[typer.Context, P], R]


def attach_share_to_context(ctx: typer.Context) -> None:
    attach_to_context(ctx, "share_dir", ensure_storage_path(SHARE_DIR, "share"))


def attach_share(func: WithContext[P, R]) -> WithContext[P, R]:
    @wraps(func)
    def wrapper(ctx: typer.Context, *args: P.args, **kwargs: P.kwargs) -> R:
        attach_share_to_context(ctx)
        return func(ctx, *args, **kwargs)

    return wrapper
