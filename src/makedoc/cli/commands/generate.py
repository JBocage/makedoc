import os
import pathlib

import click

from makedoc.parsers.source_directory_parser import DirectoryParser


@click.command("generate")
@click.option(
    "-v",
    "verbose",
    is_flag=True,
    help="Sets verbosity",
)
@click.option(
    "-o",
    "--output-path",
    "output_path",
    type=click.Path(),
    help="The output file path for the doc. If not provided, the default file name is "
    "chosen.",
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
        output_path = args.pop("output_path")
        if output_path is None:
            parser.save_readme()
        else:
            parser.save_readme(save_path=pathlib.Path(output_path).resolve().absolute())
