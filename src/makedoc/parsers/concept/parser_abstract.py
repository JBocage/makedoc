"""Implements a blueprint class for all parsers"""

import pathlib
from abc import ABC, abstractmethod, abstractproperty
from typing import Optional, Tuple

from makedoc import __VERSION__
from makedoc.logging.logger import Logger
from makedoc.makedoc_paths import MakedocPaths


class ParserAbstract(ABC):
    """Abstract class for parsers to define the mandatory methods"""

    VERSION = __VERSION__

    def __init__(
        self,
        path: pathlib.Path,
        root_path: pathlib.Path,
        logger: Optional[Logger] = None,
        makedoc_path: Optional[MakedocPaths] = None,
    ):
        self.path = path
        self.root_path = root_path
        self.name = str(self.path).split("/")[-1]

        self.parsed_doc: str = ""
        if makedoc_path is None:
            self.makedoc_paths = MakedocPaths(root_path)
        else:
            self.makedoc_paths = makedoc_path
        self.source_parser: bool = False
        if logger is None:
            logger = Logger(self.makedoc_paths)
            self.source_parser = True
        self.logger = logger

    @abstractmethod
    def get_parsed_doc(self) -> str:
        """Should get the parsed documentation for the path"""
        if self.parsed_doc == "":
            self.parsed_doc = ""
        return self.parsed_doc

    @abstractproperty
    def file_arborescence_repr(self) -> str:
        """Should get the file arborescence representation of the path."""
        return ""

    @property
    def is_ignored(self) -> bool:
        """Checks if the parser should be ignored"""
        if self.name == self.makedoc_paths.unpacked_doc_file_name:
            return True
        with open(self.makedoc_paths.ignored_path, "r") as f:
            lines = f.readlines()
        for line in lines:
            if self.partial_path:
                if (
                    line[0] != "#"
                    and line.strip() == str(self.path)
                    or line.strip() == self.partial_path
                    or (
                        line.strip()
                        == "/".join(self.partial_path.split("/")[:-1]) + "/"
                        and line.strip() != ""
                    )
                ):
                    return True
            else:
                if line[0] != "#" and line.strip() == str(self.path):
                    return True
        with open(self.makedoc_paths.ignored_every, "r") as f:
            lines = f.readlines()
        for line in lines:
            if line[0] != "#" and line.strip() == self.name:
                return True
        if self.path.is_file():
            with open(self.makedoc_paths.ignored_extensions, "r") as f:
                lines = f.readlines()
            for line in lines:
                if line[0] != "#" and line.strip() == ".".join(
                    self.name.split(".")[1:]
                ):
                    return True
        return False

    @property
    def partial_path(self) -> str:
        """Gets the partial path of the parser"""
        fullpath = str(self.path.absolute())
        root_path = str(self.root_path.absolute())
        return fullpath[len(root_path) + 1 :]

    def __repr__(self):
        """Gets the representation of the parser"""
        return str(self.path)

    @property
    def _message_args(self) -> Tuple[str, MakedocPaths]:
        """Builds the arguments to provide to the messages upon creation"""
        return (self.partial_path, self.makedoc_paths)
