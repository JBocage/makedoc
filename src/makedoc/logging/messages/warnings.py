"""Defines all the default warning messages that makedoc can verbose"""
from makedoc.logging.messages.concept.message_abstract import WarningAbstract


class EmptyPyFileDocstringWarning(WarningAbstract):
    """Appears when a python file misses file-level docstrings"""

    CODE: int = 101
    CONTENT: str = "Empty file-level docstring"
    SOLUTION: str = "Fill in the file docstring"


class AlreadyBeganDynamicSnippetWarning(WarningAbstract):
    """Appears when a dynamic snippet starts again inside its own zone"""

    CODE: 102

    def __init__(self, snippet_ref: str, **kwargs):
        self.CONTENT = f"Dynamic snippet '{snippet_ref}' strats more than once"
        self.SOLUTION = f"Remove 'begin:{snippet_ref}' tokens until there is only one"
        super().__init__(**kwargs)


class UnclosedDynamicSnippetWarning(WarningAbstract):
    """Appears when a dynamic snippet never ends"""

    CODE: 103

    def __init__(self, snippet_ref: str, **kwargs):
        self.CONTENT = f"Dynamic snippet '{snippet_ref}' is never closed"
        self.SOLUTION = f"Add 'end:{snippet_ref}' where the snippet ends"
        super().__init__(**kwargs)


class UnreferencedDynamicSnippetWarning(WarningAbstract):
    """Appears when a dynamic snippet never ends"""

    CODE: 104

    def __init__(self, snippet_ref: str, **kwargs):
        self.CONTENT = f"Dynamic snippet '{snippet_ref}' is not referenced"
        self.SOLUTION = "Check for all dynamic snippets definitions in the file"
        super().__init__(**kwargs)


class EmptyDirdocWarning(WarningAbstract):
    """Apprears when a directory documentation is empty"""

    CODE: int = 100
    CONTENT: str = "Empty directory documentation"
    SOLUTION: str = (
        "Use makedoc unpack [DIRPATH] to create the dirdoc file and fill it in"
    )
