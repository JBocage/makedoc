"""Defines all the default info messages that makedoc can verbose"""
from makedoc.logging.messages.concept.message_abstract import InfoAbstract


class ParsingStartsInfo(InfoAbstract):
    """Appears when a parsing starts"""

    CODE: int = 1
    CONTENT: str = "Makedoc starts to parse documentation"
    SOLUTION: str = ""
