import click

import pathlib

from makedoc.parsers.source_directory_parser import SourceDirectoryParser


@click.command("init")
@click.option(
    "-v",
    "verbose",
    is_flag=True,
    help="Sets verbosity",
)
@click.argument("root_dir", type=click.Path(), required=False)
@click.pass_context
def init(ctx, *args, **kwargs):
    """initialise the makedoc profile for the directory"""

    for key, value in kwargs.items():
        ctx.obj.set_config(key, value)

    args = ctx.obj.config

    if args.pop("verbose"):
        print("Generating a doc file")

    root_dir_str = args.pop("root_dir")
    if root_dir_str is None:
        root_dir_str = "."
    pth = pathlib.Path(root_dir_str).resolve().absolute()
    _ = SourceDirectoryParser(path=pth)
