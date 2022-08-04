"""Implements a config command to makedoc cli"""
import click


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
    pass


# TODO: Implements a cleaner for cleaning the dirdoc from all the useless paths
