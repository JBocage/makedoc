import json
import pathlib
from typing import Optional

from makedoc.utils.config_dict_struc import CfgDict


class MakedocPaths:
    """Contains all the paths used by the package.

    Attributes:
        logs (pathlib.Path)
            The path to .makedoc/logs/
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
        self.config_json = config / "config.json"

        self._unpacked_doc_file_name: Optional[str] = None
        self._autodoc_file_name: Optional[str] = None
        self._config_dict: Optional[CfgDict] = None

    def _read_files_naming(self):
        """Reads the files naming configuration"""
        with open(self.files_naming, "r") as f:
            files_naming = json.load(f)
            self._unpacked_doc_file_name = files_naming["unpacked_doc_file_name"]
            self._autodoc_file_name = files_naming["autodoc_file_name"]

    @property
    def config_dict(self) -> CfgDict:
        """Reads the config.json file"""
        if self._config_dict is None:
            with open(self.config_json, "r") as f:
                self._config_dict = json.load(f)
        return self._config_dict

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
