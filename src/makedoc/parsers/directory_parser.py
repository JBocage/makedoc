"""Implements a parser class for directories"""

import datetime
import json
import os
import pathlib
from typing import Dict, List, Optional, Type

from .concept import FileParserAbstract, ParserAbstract
from .pyscript_parser import PyscriptParser


class DirectoryParser(ParserAbstract):
    """Parser class for directories"""

    # File extensions supported and their parsers
    EXTENSION_MATCHING: Dict[str, Type[FileParserAbstract]] = {"py": PyscriptParser}

    def __init__(self, **kwargs):
        super(DirectoryParser, self).__init__(**kwargs)

        self.dir_children: List[DirectoryParser] = []
        self.file_children: List[FileParserAbstract] = []
        if not self.is_ignored:
            self._init_packed_doc()
            self._mine_for_doc()

    def _init_packed_doc(self) -> None:
        """Initialised packed doc entry if not registered"""

        with open(self.makedoc_paths.packed_doc, "r") as f:
            packed_doc: Dict[str, str] = json.load(f)

        if self.partial_path not in packed_doc.keys():
            packed_doc[self.partial_path] = f"# {self.name}\n"
            with open(self.makedoc_paths.packed_doc, "w+") as f:
                json.dump(
                    packed_doc, f, indent=4, separators=(",", ": "), sort_keys=True
                )

    def _mine_for_doc(self) -> None:
        """Digs inside the file arborescence for documenting parsers.

        When a directory is found, inits a DirectoryParser
        When a file is found, checks if its extension is supported, or initialise a
        default FileParser
        """
        self.dir_children: List[DirectoryParser] = []
        self.file_children: List[FileParserAbstract] = []
        for fname in os.listdir(self.path):
            if (self.path / fname).is_dir():
                child = DirectoryParser(
                    path=self.path / fname, root_path=self.root_path
                )
                if not child.is_ignored:
                    self.dir_children.append(child)
            else:
                if fname.split(".")[-1] in self.EXTENSION_MATCHING.keys():
                    child = self.EXTENSION_MATCHING[fname.split(".")[-1]](
                        path=self.path / fname, root_path=self.root_path
                    )
                else:
                    child = FileParserAbstract(
                        path=self.path / fname, root_path=self.root_path
                    )
                if not child.is_ignored:
                    self.file_children.append(child)
        self.dir_children.sort(key=lambda x: x.name)
        self.file_children.sort(key=lambda x: x.name)

    def get_parsed_doc(self) -> str:
        """Returns the doc for the parser.
        Directory doc is stored in .makedoc/packed_doc.json
        """

        if self.makedoc_paths.unpacked_doc_file_name in os.listdir(self.path):
            with open(self.path / self.makedoc_paths.unpacked_doc_file_name, "r") as f:
                doc = "".join(f.readlines())
            return doc

        with open(self.makedoc_paths.packed_doc, "r") as f:
            packed_doc: Dict[str, str] = json.load(f)
        return packed_doc[self.partial_path]

    def get_doc_file_content(self) -> str:
        """Builds the README doc file content automatically"""
        content = ""

        content += self.get_parsed_doc()

        content += (
            "\n"
            '<hr style="border:2px solid gray"> </hr>\n'
            "\n"
            "# Structure\n"
            "\n"
            "```\n"
        )
        content += self.file_arborescence_repr
        content += "\n```\n" '<hr style="border:2px solid gray"> </hr>\n' "\n"

        for subdir in self.dir_children:
            subdirdoc = subdir.get_parsed_doc()
            for line in subdirdoc.split("\n"):
                if line[:1] == "#":
                    content += f"#{line}\n"
                else:
                    content += f">{line}\n"
            content += "\n" "---\n" "\n"

        for file in self.file_children:
            filedoc = file.get_parsed_doc()
            if filedoc:
                for line in filedoc.split("\n"):
                    if line[:1] == "#":
                        content += f"#{line}\n"
                    else:
                        content += f">{line}\n"
                content += "\n" "---\n" "\n"

        content += f'\n\n\n\n<sub>This doc was automatically generated with makedoc v{self.VERSION} on {datetime.datetime.now().strftime(" %D %H:%M:%S ")}'
        return content

    @property
    def file_arborescence_repr(self) -> str:
        """Builds the internal hierarchy of the directory.

        The return string looks like the following
        makedoc/
            ├── cli/
            │   ├── commands/
            │   │   ├── bash_scripts/
            │   │   ├── __init__.py
            │   │   ├── config.py
            │   │   ├── generate.py
            │   ├── __init__.py
            │   └── main.py
            ├── parsers/
            │   ├── concept/
            │   │   ├── __init__.py
            │   │   ├── file_parser_abstract.py
            │   │   └── parser_abstract.py
            │   ├── __init__.py
            │   ├── directory_parser.py
            │   ├── pyscript_parser.py
            │   └── source_directory_parser.py
            └── __init__.py
        """
        FCROSS = "└── "
        CROSSDIR = "├── "
        VERTLINE = "│   "
        NOTHING = "    "
        output = self.name + "/\n"
        n_childs = len(self.dir_children) + len(self.file_children)
        i = 0
        for subdir in self.dir_children:
            i += 1
            subdir_hierarchy = subdir.file_arborescence_repr
            marker = CROSSDIR if i != n_childs else FCROSS
            for line in subdir_hierarchy.split("\n"):
                output += marker + line + "\n"
                marker = VERTLINE if i != n_childs else NOTHING
        for subfile in self.file_children:
            i += 1
            marker = CROSSDIR if i != n_childs else FCROSS
            output += marker + subfile.file_arborescence_repr + "\n"
        return output[:-1]

    def save_readme(
        self, recurse=False, save_path: Optional[pathlib.Path] = None
    ) -> None:
        """Saves the doc content into a readme file.

        The name of the file is defined in .makedoc/makedoc.files_nameing.json
        """
        if save_path is None:
            save_path = self.path / self.makedoc_paths.autodoc_file_name
        with open(save_path, "w+") as f:
            f.write(self.get_doc_file_content())
        if recurse:
            for child_dir in self.dir_children:
                child_dir.save_readme(recurse=True, save_path=save_path)
        return

    def update_doc(self, recurse=False) -> None:
        """Updates the readme file of the directory if it exists.

        Passes otherwise
        """
        if self.makedoc_paths.autodoc_file_name in os.listdir(self.path):
            with open(self.path / self.makedoc_paths.autodoc_file_name, "w") as f:
                f.write(self.get_doc_file_content())
        if recurse:
            for child_dir in self.dir_children:
                child_dir.update_doc(recurse=True)
        return

    def unpack_doc(self, recurse=False) -> None:
        """Creates a file inside the directory that contains the directory doc

        The user can then update the directory doc by updating the file.
        The content of this file is synced with the content of .makedoc/packed_doc.json
        """

        with open(self.makedoc_paths.packed_doc, "r") as f:
            packed_doc: Dict[str, str] = json.load(f)

        if self.makedoc_paths.unpacked_doc_file_name in os.listdir(self.path):
            if not recurse:
                raise RuntimeError("The directory doc is already unpacked")
        else:
            with open(self.path / self.makedoc_paths.unpacked_doc_file_name, "w+") as f:
                f.write(packed_doc[self.partial_path])

        if recurse:
            for child in self.dir_children:
                child.unpack_doc(recurse=True)

    def pack_doc(self, recurse=False) -> None:
        """Updates .makedoc/packed_doc.json according to what is contained

        In the file created by the unpack_doc method.
        """

        if self.makedoc_paths.unpacked_doc_file_name not in os.listdir(self.path):
            if not recurse:
                raise RuntimeError("The directory doc is unexisting")
        else:
            with open(self.path / self.makedoc_paths.unpacked_doc_file_name, "r") as f:
                doc = "".join(f.readlines())

            with open(self.makedoc_paths.packed_doc, "r") as f:
                packed_doc: Dict[str, str] = json.load(f)
                packed_doc[self.partial_path] = doc

            with open(self.makedoc_paths.packed_doc, "w") as f:
                json.dump(
                    packed_doc, f, indent=4, separators=(",", ": "), sort_keys=True
                )

            os.remove(self.path / self.makedoc_paths.unpacked_doc_file_name)

        if recurse:
            for child in self.dir_children:
                child.pack_doc(recurse=True)
