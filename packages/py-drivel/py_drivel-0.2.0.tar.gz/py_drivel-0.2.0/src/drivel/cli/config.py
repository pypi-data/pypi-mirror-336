from contextlib import contextmanager
import json
from functools import wraps
from pathlib import Path
from typing import Annotated, Any, Callable, Concatenate, ParamSpec, TypeAlias, TypeVar, cast

import snick
import typer
from inflection import dasherize
from loguru import logger
from pydantic import BaseModel, ValidationError, Field

from drivel.cli.share import attach_share, attach_share_to_context
from drivel.cli.utilities import attach_to_context
from drivel.constants import DEFAULT_THEME
from drivel.cli.constants import SETTINGS_FILE_NAME
from drivel.cli.exceptions import Abort, handle_abort
from drivel.cli.format import terminal_message


P = ParamSpec("P")
R = TypeVar("R", covariant=True)
WithContext: TypeAlias = Callable[Concatenate[typer.Context, P], R]


def file_exists(value: Path | None) -> Path | None:
    if value is None:
        return value

    value = value.expanduser()
    if not value.exists():
        raise ValueError(f"File not found at {value}")
    return value


class Settings(BaseModel):
    default_theme: str = DEFAULT_THEME

    invalid_warning: Annotated[
        str | None,
        Field(
            exclude=True,
            description="""
            An optional warning that can be included when the model is invalid.

            Used when we use the `attach_settings` decorator with `validate=False`.
        """,
        ),
    ] = None


@contextmanager
def handle_config_error():
    try:
        yield
    except ValidationError as err:
        raise Abort(
            snick.conjoin(
                "A configuration error was detected.",
                "",
                "Details:",
                "",
                f"[red]{err}[/red]",
            ),
            subject="Configuration Error",
            log_message="Configuration error",
        )


def init_settings(validate: bool = True, **settings_values: Any) -> Settings:
    with handle_config_error():
        logger.debug("Validating settings")
        try:
            return Settings(**settings_values)
        except ValidationError as err:
            if validate:
                raise
            settings = Settings.model_construct(**settings_values)
            settings.invalid_warning = str(err)
            return settings


def update_settings(settings: Settings, **settings_values: Any) -> Settings:
    with handle_config_error():
        logger.debug("Validating settings")
        settings_dict = settings.model_dump(exclude_unset=True)
        settings_dict.update(**settings_values)
        return Settings(**settings_dict)


def unset_settings(settings: Settings, *unset_keys: str) -> Settings:
    with handle_config_error():
        logger.debug("Unsetting settings")
        return Settings(**{k: v for (k, v) in settings.model_dump(exclude_unset=True).items() if k not in unset_keys})


def attach_settings(validate: bool = True) -> Callable[[WithContext[P, R]], WithContext[P, R]]:
    """
    Attach the settings to the CLI context.

    If the share directory hasn't been attached yet, attach it.

    Optionally, skip validation of the settings. This is useful in case the config
    file being loaded is not valid, but we still want to use the settings. Then, we
    can update the settings with correct values.

    I would love to figure out how to make this work with optional parameters as described in:
    https://stackoverflow.com/a/24617244/642511

    However, I couldn't figure out the typing for it.
    """

    def _decorate(func: WithContext[P, R]) -> WithContext[P, R]:

        @wraps(func)
        def wrapper(ctx: typer.Context, *args: P.args, **kwargs: P.kwargs) -> R:
            attach_share_to_context(ctx)
            settings_path = ctx.obj.share_dir / "settings.json"

            settings_values: dict[str, Any] = {}
            try:
                logger.debug(f"Loading settings from {settings_path}")
                settings_values.update(**json.loads(settings_path.read_text()))
            except FileNotFoundError:
                # If I ever port this into a cli toolkit, need a way to detect if all settings have a default and only
                # trigger this if they do not
                #
                # raise Abort(
                #     f"""
                #     No settings file found at {settings_path}!

                #     Run the bind sub-command first to establish your settings.
                #     """,
                #     subject="Settings file missing!",
                #     log_message="Settings file missing!",
                # )
                pass
            settings: Settings = init_settings(validate=validate, **settings_values)
            attach_to_context(ctx, "settings", settings)
            return func(ctx, *args, **kwargs)

        return wrapper

    return _decorate


def dump_settings(settings: Settings, settings_path: Path) -> None:
    logger.debug(f"Saving settings to {settings_path}")
    settings_values = settings.model_dump_json(indent=2)
    settings_path.write_text(settings_values)


def clear_settings(settings_path: Path) -> None:
    logger.debug(f"Removing saved settings at {settings_path}")
    settings_path.unlink(missing_ok=True)


def show_settings(settings: Settings):
    parts: list[tuple[str, str]] = []
    for field_name, field_value in settings:
        if field_name == "invalid_warning":
            continue
        parts.append((dasherize(field_name), field_value))
    max_field_len = max(len(field_name) for field_name, _ in parts)
    message = "\n".join(f"[bold]{k:<{max_field_len}}[/bold] -> {v}" for k, v in parts)
    if settings.invalid_warning:
        message += f"\n\n[red]Configuration is invalid: {settings.invalid_warning}[/red]"
    terminal_message(message, subject="Current Configuration")


cli = typer.Typer(help="Configure the app, change settings, or view how it's currently configured")


@cli.command()
@attach_share
@handle_abort
def bind(
    ctx: typer.Context,
    default_theme: Annotated[str | None, typer.Option(help="The default theme to use in the CLI")] = None,
) -> None:
    """
    Bind the configuration to the app.
    """
    filtered_locals: dict[str, Any] = {k: v for (k, v) in locals().items() if k != "ctx" and v is not None}
    logger.debug(f"Initializing settings with {filtered_locals}")
    settings = init_settings(**filtered_locals)

    settings_path: Path = cast(Path, ctx.obj.share_dir / SETTINGS_FILE_NAME)
    dump_settings(settings, settings_path)
    show_settings(settings)


@cli.command()
@attach_settings(validate=False)
@handle_abort
def update(
    ctx: typer.Context,
    default_theme: Annotated[str | None, typer.Option(help="The default theme to use in the CLI")] = None,
) -> None:
    """
    Update one or more configuration settings that are bound to the app.
    """
    filtered_locals: dict[str, Any] = {k: v for (k, v) in locals().items() if k != "ctx" and v is not None}
    logger.debug(f"Updating settings with {filtered_locals}")
    settings = update_settings(ctx.obj.settings or Settings(), **filtered_locals)

    settings_path: Path = cast(Path, ctx.obj.share_dir / SETTINGS_FILE_NAME)
    dump_settings(settings, settings_path)
    show_settings(settings)


@cli.command()
@handle_abort
@attach_settings(validate=False)
def unset(
    ctx: typer.Context,
    default_theme: Annotated[bool, typer.Option(help="The default theme to use in the CLI")] = False,
):
    """
    Remove a configuration setting that was previously bound to the app.
    """
    keys: list[str] = [k for (k, v) in locals().items() if k != "ctx" and v]
    logger.debug(f"Unsetting settings: {keys}")
    settings = unset_settings(ctx.obj.settings, *keys)

    settings_path: Path = cast(Path, ctx.obj.share_dir / SETTINGS_FILE_NAME)
    dump_settings(settings, settings_path)
    show_settings(settings)


@cli.command()
@handle_abort
@attach_settings(validate=False)
def show(ctx: typer.Context):
    """
    Show the config that is currently bound to the app.
    """
    settings: Settings = ctx.obj.settings or Settings()
    show_settings(settings)


@cli.command()
@handle_abort
@attach_settings(validate=False)
def path(ctx: typer.Context):
    """
    Show the path to the config file that is currently bound to the app.
    """
    settings_path: Path = cast(Path, ctx.obj.share_dir / SETTINGS_FILE_NAME)
    terminal_message(str(settings_path), subject="Current Configuration Path")


@cli.command()
@handle_abort
@attach_share
def clear(ctx: typer.Context):
    """
    Clear the config from the app.
    """
    doit = typer.confirm("Are you sure you want to clear the settings?")
    if doit:
        logger.debug("Clearing settings")
        settings_path: Path = cast(Path, ctx.obj.share_dir / SETTINGS_FILE_NAME)
        clear_settings(settings_path)
        terminal_message(
            "All settings have been cleared and returned to built-in defaults",
            subject="Settings Cleared"
        )
    else:
        logger.debug("Clearing settings aborted")
