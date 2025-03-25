from pathlib import Path
from typing import Any

from loguru import logger
import typer

from drivel.cli.exceptions import Abort


def ensure_storage_path(
    storage_path: Path,
    description: str,
) -> Path:
    try:
        storage_path.mkdir(exist_ok=True, parents=True)
        info_file = storage_path / "info.txt"
        info_file.write_text(
            f"""
            This directory is used by Drivel for its {description}.
            """
        )
        return storage_path
    except Exception:
        raise Abort(
            """
            {description.capitalize()} directory {storage_path} doesn't exist, is not writable,
            or could not be created.

            Please check your home directory permissions and try again.
            """,
            subject=f"Non-writable {description} dir",
            log_message=f"Non-writable {description} cache dir",
        )


def attach_to_context(ctx: typer.Context, key: str, value: Any) -> None:
    logger.debug(f"Binding {key} to CLI context")
    if getattr(ctx.obj, key):
        logger.warning(f"Context already has attribute {key}. Skipping.")
        return
    setattr(ctx.obj, key, value)
