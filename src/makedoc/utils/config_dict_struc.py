"""Define a Typedict object for the config dictionnaire.
This enables the IDE to help with autocompletion
"""

from typing import TypedDict

CfgVerbosityDict = TypedDict(
    "CfgVerbosityDict",
    {
        "print-warning": bool,
        "print-error": bool,
        "print-info": bool,
        "print-success": bool,
    },
)

CfgDict = TypedDict("ConfigDict", {"verbosity": CfgVerbosityDict})
