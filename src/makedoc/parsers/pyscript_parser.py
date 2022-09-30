"""
Implements a parser class for python scripts
"""
from typing import List

from makedoc.logging.messages.warnings import EmptyPyFileDocstringWarning

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
            self.parsed_doc += "\n\n".join(self.get_file_beginning_comment_lines())
        return self.parsed_doc

    def get_file_beginning_comment_lines(self) -> List[str]:
        """Gets the beginning of file docstrings if applicable

        Returns
            List[str] : The line-wise list of all comments of the beginning of
                the file.
        """
        lines = self.content_txt_lines
        file_beginning_comment_lines = []
        comment_marker = None

        for line in lines:

            # If file beginning comment not started yet:
            if comment_marker is None:

                if line.lstrip()[:3] in ["'''", '"""']:  # Comment starts
                    comment_marker = "'''" if line.lstrip()[:3] == "'''" else '"""'

                    if (
                        line.lstrip()[3:].rstrip()[-3:] == comment_marker
                    ):  # One line comment
                        return [line.strip()[3:-3]]
                    elif line.rstrip()[3:]:
                        file_beginning_comment_lines.append(line.strip()[3:])

            else:
                if line.lstrip()[:3] == comment_marker:
                    return file_beginning_comment_lines
                elif line.rstrip()[-3:] == comment_marker:
                    file_beginning_comment_lines.append(line.rstrip()[:-3])
                    return file_beginning_comment_lines
                else:
                    file_beginning_comment_lines.append(line.rstrip())

        self.logger.add_log(
            EmptyPyFileDocstringWarning(
                file_path_str=self.partial_path, makedoc_paths=self.makedoc_paths
            )
        )
        return []
