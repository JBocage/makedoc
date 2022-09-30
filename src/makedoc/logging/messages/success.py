"""Defines all the default success messages that makedoc can verbose"""
from makedoc.logging.messages.concept.message_abstract import SuccessAbstract


class ParsingFinishedSuccess(SuccessAbstract):
    """Appears when parsing finishes"""

    CODE: int = 999
    CONTENT: str = "Makedoc finished parsing"
    SOLUTION: str = ""
