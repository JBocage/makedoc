"""This file implements a command line interface for launching generators"""

import click
from makedoc.cli.commands.pack import pack
from makedoc.cli.commands.unpack import unpack
from makedoc.cli.commands.update import update

from makedoc import __VERSION__

from .commands import generate, init, config


class Config(object):
    """An object designed to conatin and pass the config"""

    def __init__(self) -> None:
        self.config = {}

    def set_config(self, key, value):
        """Sets a key-value pair into the config"""
        self.config[key] = value


@click.group()
@click.version_option(version=__VERSION__)
@click.pass_context
def cli(ctx, *args, **kwargs):
    """
    Loads all high level kwargs into the config.
    For supporting autocompletion, please run:

    source autocomplete-makedoc
    """
    ctx.obj = Config()
    for key, value in kwargs.items():
        ctx.obj.set_config(key, value)
        print(key, type(value), value)


cli.add_command(config)
cli.add_command(generate)
cli.add_command(init)
cli.add_command(pack)
cli.add_command(unpack)
cli.add_command(update)
