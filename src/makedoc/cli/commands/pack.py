import click
import pathlib

import os

from makedoc.parsers.directory_parser import DirectoryParser


@click.command("pack")
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
@click.option("-u", "--update", "update", is_flag=True, help="Updates the doc md file")
@click.option(
    "-ru",
    "--recurse-update",
    "recurse_update",
    is_flag=True,
    help="Combines -r and -u in one single flag",
)
@click.argument("root_dir", type=click.Path(), required=False)
@click.pass_context
def pack(ctx, *args, **kwargs):
    """Repacks the directory doc"""

    for key, value in kwargs.items():
        ctx.obj.set_config(key, value)

    args = ctx.obj.config

    if args.pop("verbose"):
        print("Repacking the directory doc")

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
        update = args.pop("update")
        recurse_update = args.pop("recurse_update")

        recurse = recurse or recurse_update
        update = update or recurse_update

        parser.pack_doc(recurse=recurse)
        if update:
            parser.update_readme(recurse=recurse)
