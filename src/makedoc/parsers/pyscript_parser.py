"""
Implements a parser class for python scripts
"""
import re
from typing import Dict, List

from makedoc.logging.messages.warnings import (
    AlreadyBeganDynamicSnippetWarning,
    EmptyPyFileDocstringWarning,
    UnclosedDynamicSnippetWarning,
    UnreferencedDynamicSnippetWarning,
)
from makedoc.parsers.concept import FileParserAbstract


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
            self.parsed_doc += "\n".join(
                self.get_dynamic_snippet_processed_file_docstrings()
            )
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

        if not (
            self.name == "__init__.py"
            and self.makedoc_paths.config_dict["parsing"]["python"][
                "ignore-init-file-level-docstrings"
            ]
        ):
            self.logger.add_log(
                EmptyPyFileDocstringWarning(
                    file_path_str=self.partial_path, makedoc_paths=self.makedoc_paths
                )
            )
        return []

    def get_dynamic_snippets(self) -> Dict[str, List[str]]:
        lines = self.content_txt_lines
        dynamic_snippets: Dict[str, List[str]] = {}
        current_snippets: List[str] = []
        for line in lines:
            end_captured = re.search("#.*end:([\w\-_]+)", line)
            if end_captured:
                for snip_name in end_captured.groups():
                    if snip_name in current_snippets:
                        current_snippets.pop(current_snippets.index(snip_name))

            for snip_name in current_snippets:
                if snip_name in dynamic_snippets.keys():
                    dynamic_snippets[snip_name].append(line.rstrip())
                else:
                    dynamic_snippets[snip_name] = [line.rstrip()]

            begin_captured = re.search("#.*begin:([\w\-_]+)", line)
            if begin_captured:
                for snip_name in begin_captured.groups():
                    if snip_name in current_snippets:
                        self.logger.add_log(
                            AlreadyBeganDynamicSnippetWarning(
                                snippet_ref=snip_name, **self._message_kwargs
                            )
                        )
                    else:
                        current_snippets.append(snip_name)

        if len(current_snippets) > 0:
            self.logger.add_log(
                UnclosedDynamicSnippetWarning(
                    snippet_ref=snip_name, **self._message_kwargs
                )
            )

        return dynamic_snippets

    def get_dynamic_snippet_processed_file_docstrings(self) -> List[str]:
        docstrings = self.get_file_beginning_comment_lines()
        dynamic_snippets = self.get_dynamic_snippets()
        processed_lines = []
        for line in docstrings:
            tokens = re.search(r"makedoc-snippet:([\w\-_]+)", line)
            if tokens:
                snip_name = tokens.groups()[0]
                if snip_name not in dynamic_snippets.keys():
                    self.logger.add_log(
                        UnreferencedDynamicSnippetWarning(
                            snippet_ref=snip_name, **self._message_kwargs
                        )
                    )
                else:
                    processed_lines.append("```python")
                    processed_lines.extend(dynamic_snippets[snip_name])
                    processed_lines.append("```")
            else:
                processed_lines.append(line + "\n")

        return processed_lines
