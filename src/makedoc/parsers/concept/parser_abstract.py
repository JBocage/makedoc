"""Implements a blueprint class for all parsers"""

import json
import pathlib
from abc import ABC, abstractmethod, abstractproperty
from typing import Optional

from makedoc import __VERSION__


class MakedocPaths:
    """Contains all the paths used by the package.

    Attributes:
        logs (pathlib.Path)
            The path to .makedoc/logs/  # TODO: Implement logging
        config (pathlib.Path)
            The path to .makedoc/config/
        packed_doc (pathlib.Path)
            The path to the packed doc file.
            .makedoc/packed_doc.json
        ignored_path (pathlib.Path)
            The path to the ignored paths file.
            .makedoc/config/makedoc.ignored_paths
        ignore_every (pathlib.Path)
            The path to the ignore_every file.
            .makedoc/config/makedoc.ignore_every
        ignored_extensions (pathlib.Path)
            The path to the ignored_extensions file.
            .makedoc/config/makedoc.ignored_extensions
        files_naming (pathlib.Path)
            The path to the files naming file.
            .makedoc/config/makedoc.files_naming.json

    Properties:
        unpacked_doc_file_name (str)
            The file name of the directory unpacked doc
        autodoc_file_name (str)
            The file name of the doc md files (default: README.md)
    """

    def __init__(self, source_path: pathlib.Path) -> None:

        makedoc = source_path / ".makedoc"
        config = makedoc / "config"

        self.logs = makedoc / "logs"
        self.config = makedoc / "config"

        self.packed_doc = makedoc / "packed_doc.json"

        self.ignored_path = config / "makedoc.ignored_paths"
        self.ignored_every = config / "makedoc.ignore_every"
        self.ignored_extensions = config / "makedoc.ignored_extensions"
        self.files_naming = config / "makedoc.files_naming.json"

        self._unpacked_doc_file_name: Optional[str] = None
        self._autodoc_file_name: Optional[str] = None

    def _read_files_naming(self):
        """Reads the files naming configuration"""
        with open(self.files_naming, "r") as f:
            files_naming = json.load(f)
            self._unpacked_doc_file_name = files_naming["unpacked_doc_file_name"]
            self._autodoc_file_name = files_naming["autodoc_file_name"]

    @property
    def unpacked_doc_file_name(self) -> str:
        """Gets the directory unpacked doc file name"""
        if self._unpacked_doc_file_name is None:
            self._read_files_naming()
        return self._unpacked_doc_file_name

    @property
    def autodoc_file_name(self) -> str:
        """Gets the auto doc file name"""
        if self._autodoc_file_name is None:
            self._read_files_naming()
        return self._autodoc_file_name


class ParserAbstract(ABC):
    """Abstract class for parsers to define the mandatory methods"""

    VERSION = __VERSION__

    def __init__(self, path: pathlib.Path, root_path: pathlib.Path):
        self.path = path
        self.root_path = root_path
        self.name = str(self.path).split("/")[-1]
        self.parsed_doc: str = ""
        self.makedoc_paths = MakedocPaths(root_path)

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
