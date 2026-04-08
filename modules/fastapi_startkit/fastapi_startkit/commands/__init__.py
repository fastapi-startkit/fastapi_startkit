from typer import Typer

from core.commands.database import app as migrate_command


def register_command(cli: Typer):
    cli.add_typer(migrate_command)
