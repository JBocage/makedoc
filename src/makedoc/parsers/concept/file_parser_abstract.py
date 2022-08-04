"""Implements a blueprint class for file parsers"""

from typing import List

from .parser_abstract import ParserAbstract


class FileParserAbstract(ParserAbstract):
    """Blueprint class for file parsers. An file parser should inherit from
    this class.
    """

    def __init__(self, **kwargs):
        super(FileParserAbstract, self).__init__(**kwargs)

    def get_hierarchy_repr(self) -> str:
        """The hierarchy of a single file is itself."""
        return self.name

    def get_parsed_doc(self) -> str:
        """The default doc for a file is empty. The file is ignored"""
        return ""

    def readlines_as_txt(self) -> List[str]:
        """Implements a method to read the content of the file as text

        Returns:
            lines: List[str]
                The list of all lines strings

        # TODO: Make it a property
        """
        with open(self.path, "r") as f:
            lines = f.readlines()
        return lines
