from typing import Annotated
import typer

from drivel.cli.config import cli as config_cli
from drivel.cli.format import terminal_message
from drivel.cli.give import cli as give_cli
from drivel.cli.logging import init_logs
from drivel.cli.schemas import CliContext
from drivel.cli.themes import cli as themes_cli
from drivel.cli.version import show_version


cli = typer.Typer(rich_markup_mode="rich")


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: Annotated[bool, typer.Option(help="Enable verbose logging to the terminal")] = False,
    version: Annotated[bool, typer.Option(help="Print the version of this app and exit")] = False,
):
    """
    Welcome to drivel!

    More information can be shown for each command listed below by running it with the
    --help option.
    """

    if version:
        show_version()
        ctx.exit()

    if ctx.invoked_subcommand is None:
        ctx.get_help()
        terminal_message(
            "No command provided. Please check [bold magenta]usage[/bold magenta]",
            subject="Need an drivel command",
        )
        ctx.exit()

    init_logs(verbose=verbose)
    ctx.obj = CliContext()


cli.add_typer(config_cli, name="config")
cli.add_typer(give_cli, name="give")
cli.add_typer(themes_cli, name="themes")


if __name__ == "__main__":
    cli()
