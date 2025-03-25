from pathlib import Path
from typing import Annotated, Any

import typer

from drivel.exceptions import DrivelError
from drivel.cli.config import Settings, attach_settings
from drivel.cli.constants import ThemeListOutputFormat
from drivel.cli.exceptions import Abort, handle_abort
from drivel.cli.extra_themes import attach_extra_themes
from drivel.cli.format import as_spaces, as_lines, as_json
from drivel.themes import Theme


cli = typer.Typer()


@cli.callback(invoke_without_command=True)
@attach_settings(validate=True)
@attach_extra_themes
@handle_abort
def give(
    ctx: typer.Context,
    max_count: Annotated[int | None, typer.Argument(help="The maximum number of metasyntactic names to give")] = None,
    do_shuffle: Annotated[bool, typer.Option("--shuffle", help="Mix the names")] = False,
    theme_name: Annotated[
        str | None, typer.Option("--theme", help="The theme to use (If not provided, will use current default")
    ] = None,
    kind: Annotated[str | None, typer.Option(help="The kind of names to give. Use 'all' to pull from all kinds")] = None,
    output_format: Annotated[
        ThemeListOutputFormat, typer.Option("--format", help="The output format to use")
    ] = ThemeListOutputFormat.spaces,
    fancy: Annotated[bool, typer.Option(help="Enable fancy output")] = True,
    to_clipboard: Annotated[bool, typer.Option(help="Copy output to clipboard")] = True,
):
    """
    Give N fun metasyntactic variable names.
    """
    settings: Settings = ctx.obj.settings
    extra_themes_dir: Path = ctx.obj.extra_themes
    if theme_name is None:
        theme_name = settings.default_theme

    try:
        theme = Theme.load(theme_name, extra_themes_dir)
        items = theme.give(max_count=max_count, kind=kind, do_shuffle=do_shuffle)
    except DrivelError:
        raise Abort(
            "There was an error fetching names!",
            subject="Error giving names",
        )
    kwargs: dict[str, Any] = dict(
        fancy=fancy,
        to_clipboard=to_clipboard,
    )
    match output_format:
        case ThemeListOutputFormat.spaces | ThemeListOutputFormat.lines:
            if fancy:
                kwargs["subject"] = f"Fun names from {theme_name}"
            match output_format:
                case ThemeListOutputFormat.spaces:
                    as_spaces(items, **kwargs)
                case ThemeListOutputFormat.lines:
                    as_lines(items, **kwargs)
        case ThemeListOutputFormat.json:
            as_json(items, **kwargs)
