"""Implements a parser class for python scripts"""
from .concept import FileParserAbstract


class PyscriptParser(FileParserAbstract):
    """Parser class for pathyon scripts"""

    def __init__(self, **kwargs):
        super(PyscriptParser, self).__init__(**kwargs)

    def get_parsed_doc(self) -> str:
        """Gets the doc for the script

        The doc corresponds to the name of the file as a header
        """
        if self.parsed_doc == "":
            self.parsed_doc = f"# {self.name}\n"
        return self.parsed_doc
