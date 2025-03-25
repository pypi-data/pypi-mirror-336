import json
from typing import Any
from collections.abc import Iterable

import pyperclip
import snick
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import yaml


def _to_clipboard(text: str) -> bool:
    try:
        pyperclip.copy(text)
        return True
    except Exception as exc:
        logger.debug(f"Could not copy letter to clipboard: {exc}")
        return False


def terminal_message(
    message: str,
    subject: str | None = None,
    color: str = "green",
    footer: str | None = None,
    indent: bool = True,
    markdown: bool = False,
    to_clipboard: bool = False,
):
    if to_clipboard:
        result = _to_clipboard(message)
        if result and not footer:
            footer = "Copied to clipboard!"
    panel_kwargs: dict[str, Any] = dict(padding=1)
    if subject is not None:
        panel_kwargs["title"] = f"[{color}]{subject}"
    if footer is not None:
        panel_kwargs["subtitle"] = f"[dim italic]{footer}[/dim italic]"
    text = snick.dedent(message)
    if indent:
        text = snick.indent(text, prefix="  ")
    console = Console()
    console.print()
    if markdown:
        console.print(Panel(Markdown(text), **panel_kwargs))
    else:
        console.print(Panel(text, **panel_kwargs))
    console.print()


def simple_message(
    message: str,
    indent: bool = False,
    markdown: bool = False,
    to_clipboard: bool = False,
):
    text = snick.dedent(message)
    if indent:
        text = snick.indent(text, prefix="  ")
    if to_clipboard:
        result = _to_clipboard(text)
        if result:
            logger.debug("output copied to clipboard")
    console = Console()
    console.print()
    if markdown:
        console.print(Markdown)
    else:
        console.print(text)
    console.print()


def as_spaces(stuff: Iterable[Any], fancy: bool = False, **kwargs: Any):
    output = " ".join(stuff)
    if fancy:
        return terminal_message(output, **kwargs)
    else:
        kwargs.pop("subject", None)
    return simple_message(output, **kwargs)


def as_lines(stuff: Iterable[Any], fancy: bool = False, **kwargs: Any):
    output = "\n".join(stuff)
    if fancy:
        return terminal_message(output, **kwargs)
    else:
        kwargs.pop("fancy", None)
    return simple_message(output, **kwargs)


def as_json(stuff: Any, fancy: bool = False, to_clipboard: bool = False, **kwargs: Any):
    indent: int | None = 2 if fancy else None
    if to_clipboard:
        result = _to_clipboard(json.dumps(stuff, indent=indent))
        if result:
            logger.debug("output copied to clipboard")
    console = Console()
    console.print()
    console.print_json(data=stuff, indent=indent, **kwargs)
    console.print()


def as_yaml(stuff: Any, fancy: bool = False, to_clipboard: bool = False, **kwargs: Any):
    if fancy:
        logger.warning("as_yaml doesn't support fancy output")
    text = yaml.dump(stuff, sort_keys=False)
    if to_clipboard:
        result = _to_clipboard(text)
        if result:
            logger.debug("output copied to clipboard")
    console = Console()
    console.print()
    console.print(text, **kwargs)
    console.print()
