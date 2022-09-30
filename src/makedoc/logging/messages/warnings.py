"""Defines all the default warning messages that makedoc can verbose"""
from makedoc.logging.messages.concept.message_abstract import WarningAbstract


class EmptyPyFileDocstringWarning(WarningAbstract):
    """Appears when a python file misses file-level docstrings"""

    CODE: int = 101
    CONTENT: str = "Empty file-level docstring"
    SOLUTION: str = "Fill in the file docstring"


class EmptyDirdocWarning(WarningAbstract):
    """Apprears when a directory documentation is empty"""

    CODE: int = 100
    CONTENT: str = "Empty directory documentation"
    SOLUTION: str = (
        "Use makedoc unpack [DIRPATH] to create the dirdoc file and fill it in"
    )
