"""This file implements a command line interface for launching generators"""

import pathlib
from typing import Dict
import os

import click

from makedoc.parsers.source_directory_parser import (
    DirectoryParser,
    SourceDirectoryParser,
)

from makedoc import __VERSION__


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
    """Loads all high level kwargs into the config"""
    ctx.obj = Config()
    for key, value in kwargs.items():
        ctx.obj.set_config(key, value)
        print(key, type(value), value)


@cli.command("init")
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


@cli.command("gen")
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


@cli.command("unpack")
@click.option(
    "-v",
    "verbose",
    is_flag=True,
    help="Sets verbosity",
)
@click.option(
    "-r",
    "recurse",
    is_flag=True,
    help="Recursively apply the command to all non-ignored subdirs",
)
@click.argument("root_dir", type=click.Path(), required=False)
@click.pass_context
def unpack(ctx, *args, **kwargs):
    """Unpacks the directory doc"""

    for key, value in kwargs.items():
        ctx.obj.set_config(key, value)

    args = ctx.obj.config

    if args.pop("verbose"):
        print("Unppacking the directory doc")

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
        print(parser.dir_children)
        parser.unpack_doc(recurse=args.pop("recurse"))


@cli.command("pack")
@click.option(
    "-v",
    "verbose",
    is_flag=True,
    help="Sets verbosity",
)
@click.option(
    "-r",
    "recurse",
    is_flag=True,
    help="Recursively apply the command to all non-ignored subdirs",
)
@click.argument("root_dir", type=click.Path(), required=False)
@click.pass_context
def repack(ctx, *args, **kwargs):
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
        parser.pack_doc(recurse=args.pop("recurse"))


@cli.command("update")
@click.option(
    "-v",
    "verbose",
    is_flag=True,
    help="Sets verbosity",
)
@click.option(
    "-r",
    "recurse",
    is_flag=True,
    help="Recursively apply the command to all non-ignored subdirs",
)
@click.argument("root_dir", type=click.Path(), required=False)
@click.pass_context
def update(ctx, *args, **kwargs):
    """Updates the doc md files"""

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
        parser.update_readme(recurse=args.pop("recurse"))
