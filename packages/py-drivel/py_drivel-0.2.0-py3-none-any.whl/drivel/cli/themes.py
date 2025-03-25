import os
from pathlib import Path
from typing import Annotated, Any

from loguru import logger
import typer

from drivel.cli.config import attach_settings
from drivel.cli.constants import EXTRA_THEMES_DIR, ThemeListOutputFormat, ThemeOutputFormat
from drivel.cli.exceptions import Abort, handle_abort
from drivel.cli.extra_themes import attach_extra_themes
from drivel.cli.format import as_spaces, as_lines, as_json, as_yaml, terminal_message
from drivel.cli.utilities import ensure_storage_path
from drivel.themes import Theme


cli = typer.Typer()


@cli.callback(invoke_without_command=True)
def themes(ctx: typer.Context):
    """
    Commands to interact with themes.

    More information can be shown for each sub-command listed below by running it with the
    --help option.
    """
    if ctx.invoked_subcommand is None:
        ctx.get_help()
        terminal_message(
            "No sub-command provided. Please check [bold magenta]usage[/bold magenta]",
            subject="Need an drivel->themes sub-command",
        )
        ctx.exit()


@cli.command("list")
@attach_settings(validate=True)
@attach_extra_themes
@handle_abort
def list_all(
    ctx: typer.Context,
    output_format: Annotated[
        ThemeListOutputFormat, typer.Option("--format", help="The output format to use")
    ] = ThemeListOutputFormat.spaces,
    fancy: Annotated[bool, typer.Option(help="Enable fancy output")] = True,
    to_clipboard: Annotated[bool, typer.Option(help="Copy output to clipboard")] = True,
):
    """
    List all available themes.
    """
    extra_themes_dir: Path = ensure_storage_path(ctx.obj.cache_dir / EXTRA_THEMES_DIR, "extra-themes")
    theme_list = list(Theme.names(extra_themes_dir))
    match output_format:
        case ThemeListOutputFormat.spaces:
            as_spaces(theme_list, fancy=fancy, to_clipboard=to_clipboard)
        case ThemeListOutputFormat.lines:
            as_lines(theme_list, fancy=fancy, to_clipboard=to_clipboard)
        case ThemeListOutputFormat.json:
            as_json(theme_list, fancy=fancy, to_clipboard=to_clipboard)



@cli.command()
@attach_settings(validate=True)
@attach_extra_themes
@handle_abort
def add(
    ctx: typer.Context,
    theme_file: Annotated[Path, typer.Argument(help="The theme file to add")],
):
    """
    Fetch all available themes.
    """
    extra_themes_dir: Path = ctx.obj.extra_themes
    logger.debug(f"Adding theme from file {theme_file}")
    theme = Theme.loads(theme_file.read_text(), name=theme_file.stem)
    theme.dump(extra_themes_dir)
    logger.debug(f"Added theme {theme.name} to {extra_themes_dir}")


@cli.command()
@attach_settings(validate=True)
@attach_extra_themes
@handle_abort
def remove(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument(help="The name of the theme to remove")],
):
    """
    Fetch all available themes.
    """
    extra_themes_dir: Path = ctx.obj.extra_themes
    target: Path = extra_themes_dir / f"{name}.yaml"
    try:
        os.unlink(target)
    except Exception:
        raise Abort(
            f"""
            Could not remove theme {name}.

            It may not have been added or there was a problem removing the file.
            """,
            subject="Remove failed",
            log_message=f"Failed to remove theme file {target}",
        )
    logger.debug(f"Removed {name} from {extra_themes_dir}")


@cli.command()
@attach_settings(validate=True)
@attach_extra_themes
@handle_abort
def show(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument(help="The name of the theme to show")],
    output_format: Annotated[
        ThemeOutputFormat, typer.Option("--format", help="The output format to use")
    ] = ThemeOutputFormat.yaml,
    fancy: Annotated[bool, typer.Option(help="Enable fancy output")] = True,
    to_clipboard: Annotated[bool, typer.Option(help="Copy output to clipboard")] = True,
):
    """
    Show a theme.
    """
    extra_themes_dir: Path = ctx.obj.extra_themes
    try:
        theme = Theme.load(name, extra_themes_dir)
    except Exception:
        raise Abort(
            f"""
            Could not find theme {name}.

            It may not be available or there was a problem accessing the file.
            """,
            subject="Load failed",
            log_message=f"Failed to load theme {name}",
        )

    theme_dict = theme.model_dump()
    match output_format:
        case ThemeOutputFormat.json:
            as_json(theme_dict, fancy=fancy, to_clipboard=to_clipboard)
        case ThemeOutputFormat.yaml:
            as_yaml(theme_dict, fancy=fancy, to_clipboard=to_clipboard)


@cli.command()
@attach_settings(validate=True)
@attach_extra_themes
@handle_abort
def schema(
    ctx: typer.Context,
    fancy: Annotated[bool, typer.Option(help="Enable fancy output")] = True,
    to_clipboard: Annotated[bool, typer.Option(help="Copy output to clipboard")] = True,
):
    """
    Show a theme.
    """
    theme_schema: dict[str, Any] = Theme.model_json_schema()
    as_json(theme_schema, fancy=fancy, to_clipboard=to_clipboard)
