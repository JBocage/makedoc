import os
import datetime
import json
from struct import pack

from .concept import ParserAbstract
from .concept import FileParserAbstract
from .pyscript_parser import PyscriptParser
from typing import List, Dict


class DirectoryParser(ParserAbstract):

    EXTENSION_MATCHING = {"py": PyscriptParser}

    def __init__(self, **kwargs):
        super(DirectoryParser, self).__init__(**kwargs)

        self.dir_children: List[DirectoryParser] = []
        self.file_children: List[FileParserAbstract] = []
        if not self.is_ignored():
            self._init_packed_doc()
            self._mine_for_doc()

    def _init_packed_doc(self):

        with open(self.makedoc_paths.packed_doc, "r") as f:
            packed_doc: Dict[str, str] = json.load(f)

        if not self.get_partial_path() in packed_doc.keys():
            packed_doc[self.get_partial_path()] = f"# {self.name}\n"
            with open(self.makedoc_paths.packed_doc, "w+") as f:
                json.dump(
                    packed_doc, f, indent=4, separators=(",", ": "), sort_keys=True
                )

    def _mine_for_doc(self):
        self.dir_children: List[DirectoryParser] = []
        self.file_children: List[FileParserAbstract] = []
        for fname in os.listdir(self.path):
            if (self.path / fname).is_dir():
                child = DirectoryParser(
                    path=self.path / fname, root_path=self.root_path
                )
                if not child.is_ignored():
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
                if not child.is_ignored():
                    self.file_children.append(child)
        self.dir_children.sort(key=lambda x: x.name)
        self.file_children.sort(key=lambda x: x.name)

    def get_parsed_doc(self) -> str:

        if self.makedoc_paths.unpacked_doc_file_name in os.listdir(self.path):
            with open(self.path / self.makedoc_paths.unpacked_doc_file_name, "r") as f:
                doc = "".join(f.readlines())
            return doc

        with open(self.makedoc_paths.packed_doc, "r") as f:
            packed_doc: Dict[str, str] = json.load(f)
        return packed_doc[self.get_partial_path()]

    def get_doc_file_content(self) -> str:
        content = ""

        content += self.get_parsed_doc()

        content += (
            f"\n"
            f'<hr style="border:2px solid gray"> </hr>\n'
            f"\n"
            f"# Structure\n"
            f"\n"
            f"```\n"
        )
        content += self.get_hierarchy_repr()
        content += f"\n```\n" f'<hr style="border:2px solid gray"> </hr>\n' f"\n"

        for subdir in self.dir_children:
            subdirdoc = subdir.get_parsed_doc()
            for line in subdirdoc.split("\n"):
                if line[:1] == "#":
                    content += f"#{line}\n"
                else:
                    content += f">{line}\n"
            content += "\n" "---\n" "\n"

        content += f'\n\n\n\n<sub>This doc was automatically generated with makedoc v{self.VERSION} on {datetime.datetime.now().strftime(" %D %H:%M:%S ")}'
        return content

    def get_hierarchy_repr(self) -> str:
        FCROSS = "└── "
        CROSSDIR = "├── "
        VERTLINE = "│   "
        NOTHING = "    "
        output = self.name + "/\n"
        n_childs = len(self.dir_children) + len(self.file_children)
        i = 0
        for subdir in self.dir_children:
            i += 1
            subdir_hierarchy = subdir.get_hierarchy_repr()
            marker = CROSSDIR if i != n_childs else FCROSS
            for line in subdir_hierarchy.split("\n"):
                output += marker + line + "\n"
                marker = VERTLINE if i != n_childs else NOTHING
        for subfile in self.file_children:
            i += 1
            marker = CROSSDIR if i != n_childs else FCROSS
            output += marker + subfile.get_hierarchy_repr() + "\n"
        return output[:-1]

    def save_readme(self, recurse=False):
        with open(self.path / self.makedoc_paths.autodoc_file_name, "w+") as f:
            f.write(self.get_doc_file_content())
        if recurse:
            for child_dir in self.dir_children:
                child_dir.save_readme(recurse=True)
        return

    def update_readme(self, recurse=False):
        if self.makedoc_paths.autodoc_file_name in os.listdir(self.path):
            with open(self.path / self.makedoc_paths.autodoc_file_name, "w") as f:
                f.write(self.get_doc_file_content())
        if recurse:
            for child_dir in self.dir_children:
                child_dir.update_readme(recurse=True)
        return

    def unpack_doc(self, recurse=False):
        with open(self.makedoc_paths.packed_doc, "r") as f:
            packed_doc: Dict[str, str] = json.load(f)

        if self.makedoc_paths.unpacked_doc_file_name in os.listdir(self.path):
            if not recurse:
                raise RuntimeError("The directory doc is already unpacked")
        else:
            with open(self.path / self.makedoc_paths.unpacked_doc_file_name, "w+") as f:
                f.write(packed_doc[self.get_partial_path()])

        if recurse:
            for child in self.dir_children:
                child.unpack_doc(recurse=True)

    def pack_doc(self, recurse=False):

        if self.makedoc_paths.unpacked_doc_file_name not in os.listdir(self.path):
            if not recurse:
                raise RuntimeError("The directory doc is unexisting")
        else:
            with open(self.path / self.makedoc_paths.unpacked_doc_file_name, "r") as f:
                doc = "".join(f.readlines())

            with open(self.makedoc_paths.packed_doc, "r") as f:
                packed_doc: Dict[str, str] = json.load(f)
                packed_doc[self.get_partial_path()] = doc

            with open(self.makedoc_paths.packed_doc, "w") as f:
                json.dump(
                    packed_doc, f, indent=4, separators=(",", ": "), sort_keys=True
                )

            os.remove(self.path / self.makedoc_paths.unpacked_doc_file_name)

        if recurse:
            for child in self.dir_children:
                child.pack_doc(recurse=True)

    def parse_doc(self) -> str:
        pass
