import click
import pathlib


@click.command("config")
@click.option(
    "-v",
    "verbose",
    is_flag=True,
    help="Sets verbosity",
)
@click.pass_context
def config(ctx, *args, **kwargs):
    """Gets config utilities"""
