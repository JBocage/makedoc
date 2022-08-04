"""
> author: Julien Bocage
> author-email: julien.bocage@gmail.com

Implements a parser class for the source directory of a project
"""

import json

from makedoc.parsers.concept.parser_abstract import MakedocPaths

from .directory_parser import DirectoryParser


class SourceDirectoryParser(DirectoryParser):
    """Parser class for the source directory"""

    def __init__(self, path):

        self.makedoc_paths = MakedocPaths(path)
        self._init_makedoc_file_structure()
        super(SourceDirectoryParser, self).__init__(path=path, root_path=path)

    def get_partial_path(self) -> str:
        """Returns the partial path of the parser"""
        return ""

    def is_ignored(self) -> bool:
        """Returns True if the directory has to be ignored.
        Source directory cannot be ignored.
        """
        return False

    def _init_makedoc_file_structure(self):
        """Initialises the .makedoc folder"""

        if not self.makedoc_paths.packed_doc.exists():
            self.makedoc_paths.packed_doc.parent.mkdir(exist_ok=True, parents=True)
            with open(self.makedoc_paths.packed_doc, "w+") as f:
                f.write("{\n}")
        self.makedoc_paths.config.mkdir(exist_ok=True)  # Create the config folder

        if not self.makedoc_paths.files_naming.exists():
            with open(self.makedoc_paths.files_naming, "w+") as f:
                json.dump(
                    {
                        "unpacked_doc_file_name": "dirdoc.makedoc.md",
                        "autodoc_file_name": "README.md",
                    },
                    f,
                    indent=4,
                    sort_keys=True,
                    separators=(",", ": "),
                )

        # Ignored files and directories initialisation
        if not self.makedoc_paths.ignored_path.exists():
            with open(self.makedoc_paths.ignored_path, "w+") as f:
                f.write(
                    "###################################################\n"
                    "# This file shall contain all ignored directories\n"
                    "# and files for this project.\n"
                    "# \n"
                    "# Every path that matches those relative or absolute\n"
                    "# paths are to be ignored in both structure representation\n"
                    "# and README documentation.\n"
                    "###################################################\n"
                    "\n"
                    "venv/\n"
                    "makedoc\n"
                    ".idea\n"
                    ".git\n"
                    ".makedoc\n"
                    "doc/makedoc/\n"
                    "doc/imgs/\n"
                    "\n"
                    "###################################################\n"
                    "# AUTO ADDED:\n"
                )

        if not self.makedoc_paths.ignored_every.exists():
            with open(self.makedoc_paths.ignored_every, "w+") as f:
                f.write(
                    "###################################################\n"
                    "# This file shall contain all ignored directories\n"
                    "# and files for this project.\n"
                    "# \n"
                    "# Every location or directory which name matches one\n"
                    "# that is provided here shall be ignored\n"
                    "###################################################\n"
                    "\n"
                    "README.md\n"
                    "__pycache__\n"
                    "\n"
                    "###################################################\n"
                    "# AUTO ADDED:\n"
                )

        if not self.makedoc_paths.ignored_extensions.exists():
            with open(self.makedoc_paths.ignored_extensions, "w+") as f:
                f.write(
                    "###################################################\n"
                    "# This file shall contain all ignored file \n"
                    "# extensions for this project.\n"
                    "# \n"
                    "# Every file the extension of which matches one\n"
                    "# that is provided here shall be ignored\n"
                    "###################################################\n"
                    "\n"
                    "pdf\n"
                    "txt\n"
                )
