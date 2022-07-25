from abc import ABC, abstractmethod
from distutils.command.config import config
import json
from typing import Union, List
import pathlib
from makedoc import __VERSION__


class MakedocPaths:
    def __init__(self, source_path: pathlib.Path) -> None:

        makedoc = source_path / ".makedoc"
        config = makedoc / "config"

        self.logs = makedoc / "logs"
        self.config = makedoc / "config"

        self.packed_doc = makedoc / "packed_doc.json"

        self.ignored_path = config / "makedoc.ignored_paths"
        self.ignored_every = config / "makedoc.ignore_every"
        self.ignored_extensions = config / "makedoc.ignored_extensions"

        with open(config / "makedoc.files_naming.json", "r") as f:
            files_naming = json.load(f)
            self.unpacked_doc_file_name = files_naming["unpacked_doc_file_name"]
            self.autodoc_file_name = files_naming["autodoc_file_name"]


class ParserAbstract(ABC):

    VERSION = __VERSION__

    def __init__(self, path: pathlib.Path, root_path: pathlib.Path):
        self.path = path
        self.root_path = root_path
        self.name = str(self.path).split("/")[-1]
        self.parsed_doc: str = ""
        self.makedoc_paths = MakedocPaths(root_path)

    @abstractmethod
    def get_parsed_doc(self) -> str:
        if self.parsed_doc == "":
            self.parsed_doc = ""
        return self.parsed_doc

    @abstractmethod
    def get_hierarchy_repr(self) -> str:
        return ""

    def is_ignored(self) -> bool:
        with open(self.makedoc_paths.ignored_path, "r") as f:
            lines = f.readlines()
        for l in lines:
            if self.get_partial_path():
                if (
                    l[0] != "#"
                    and l.strip() == str(self.path)
                    or l.strip() == self.get_partial_path()
                    or (
                        l.strip()
                        == "/".join(self.get_partial_path().split("/")[:-1]) + "/"
                        and l.strip() != ""
                    )
                ):
                    return True
            else:
                if l[0] != "#" and l.strip() == str(self.path):
                    return True
        with open(self.makedoc_paths.ignored_every, "r") as f:
            lines = f.readlines()
        for l in lines:
            if l[0] != "#" and l.strip() == self.name:
                return True
        if self.path.is_file():
            with open(self.makedoc_paths.ignored_extensions, "r") as f:
                lines = f.readlines()
            for l in lines:
                if l[0] != "#" and l.strip() == ".".join(self.name.split(".")[1:]):
                    return True
        return False

    def get_partial_path(self):
        fullpath = str(self.path.absolute())
        root_path = str(self.root_path.absolute())
        return fullpath[len(root_path) + 1 :]

    def __repr__(self):
        return str(self.path)
