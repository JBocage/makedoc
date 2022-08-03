import click
from makedoc.parsers.source_directory_parser import (
    DirectoryParser,
)
import pathlib

import os


@click.command("generate")
@click.option(
    "-v",
    "verbose",
    is_flag=True,
    help="Sets verbosity",
)
@click.argument("root_dir", type=click.Path(), required=False)
@click.pass_context
def generate(ctx, *args, **kwargs):
    """Generates a doc file"""

    for key, value in kwargs.items():
        ctx.obj.set_config(key, value)

    args = ctx.obj.config

    if args.pop("verbose"):
        print("Generating a doc file")

    root_dir_str = args.pop("root_dir")
    if root_dir_str is None:
        root_dir_str = "."
    pth = pathlib.Path(root_dir_str).resolve().absolute()
    root = None
    while pth:
        if ".makedoc" in os.listdir(pth):
            root = pth
            break
        else:
            pth = pth.parent
    if root is None:
        raise ValueError(
            "The provided path is does not seem to be in a makedoc project"
        )
    else:
        parser = DirectoryParser(
            path=pathlib.Path(root_dir_str).resolve().absolute(), root_path=root
        )
        parser.save_readme()
