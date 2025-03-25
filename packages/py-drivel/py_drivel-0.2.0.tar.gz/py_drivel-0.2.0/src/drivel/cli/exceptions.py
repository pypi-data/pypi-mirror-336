"""
Provide custom exceptions and error handling for the CLI.

Borrowed from Smart Letters CLI: https://github.com/dusktreader/smart-letters
"""

from sys import exc_info
from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar, final

import buzz
import snick
import typer
from loguru import logger
from rich.console import Console
from rich.panel import Panel


@final
class Abort(buzz.Buzz):
    def __init__(
        self,
        message: str,
        *args: Any,
        subject: str | None = None,
        log_message: str | None = None,
        warn_only: bool = False,
        **kwargs: Any,
    ):
        self.subject = subject
        self.log_message = log_message
        self.warn_only = warn_only
        self.original_error: BaseException | None = None
        (_, self.original_error, __) = exc_info()
        super().__init__(message, *args, **kwargs)


P = ParamSpec("P")
R = TypeVar("R")


def handle_abort(func: Callable[P, R]) -> Callable[P, R]:

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return func(*args, **kwargs)
        except Abort as err:
            if not err.warn_only:
                if err.log_message is not None:
                    logger.error(err.log_message)

                if err.original_error is not None:
                    logger.error(f"Original exception: {err.original_error}")

            panel_kwargs: dict[str, Any] = dict()
            if err.subject is not None:
                panel_kwargs["title"] = f"[red]{err.subject}"
            message = snick.dedent(err.message)

            console = Console()
            console.print()
            console.print(Panel(message, **panel_kwargs))
            console.print()
            raise typer.Exit(code=1)

    return wrapper
