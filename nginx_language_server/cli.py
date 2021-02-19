import click

from .server import SERVER


@click.command()
@click.version_option()
def cli() -> None:
    """Nginx language server.

    Examples:

        Run from stdio : nginx-language-server
    """
    SERVER.start_io()
