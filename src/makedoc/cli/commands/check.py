import os
import pathlib

import click

from makedoc.parsers.directory_parser import DirectoryParser


@click.command("check")
@click.option(
    "-v",
    "verbose",
    is_flag=True,
    help="Sets verbosity",
)
@click.option(
    "-r",
    "--recurse",
    "recurse",
    is_flag=True,
    help="Recursively apply the command to all non-ignored subdirs",
)
@click.argument("root_dir", type=click.Path(), required=False)
@click.pass_context
def check(ctx, *args, **kwargs):
    """Checks the parsing without touching files"""

    for key, value in kwargs.items():
        ctx.obj.set_config(key, value)

    args = ctx.obj.config

    if args.pop("verbose"):
        print("Updating doc")

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

        recurse = args.pop("recurse")

        parser.check_parsing(recurse=recurse)
