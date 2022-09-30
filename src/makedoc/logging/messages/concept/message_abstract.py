"""Defines what a message should look like"""
import pathlib
from datetime import datetime
from typing import Optional, Tuple, Union

from makedoc.makedoc_paths import MakedocPaths


class MessageAbstract(object):
    """Blueprint class for messages"""

    CODE: int = 0
    FMT: Tuple[str, str] = ("", "")
    CONTENT: str = ""
    SOLUTION: str = ""
    VERBOSE_TOKEN: str = "[MSG]"

    def __init__(
        self,
        file_path_str: Union[str, pathlib.Path],
        makedoc_paths: MakedocPaths,
        content: Optional[str] = None,
        code: Optional[int] = None,
        solution: Optional[str] = None,
    ) -> None:
        if code is None:
            code = self.CODE
        self.code = code
        if content is None:
            content = self.CONTENT
        self.content = content
        self.time: datetime = datetime.now()
        if isinstance(file_path_str, pathlib.Path):
            file_path_str = file_path_str.as_posix()
        self.file_path_str = file_path_str
        if solution is None:
            solution = self.SOLUTION
        self.solution = solution
        self.makedoc_paths = makedoc_paths

    @property
    def time_str(self) -> str:
        """Builds the HH:MM:SS string that gives the time of the message creation"""
        return self.time.strftime("%H:%M:%S")

    @property
    def line_description(self) -> str:
        """Builds the line description for the message"""
        return f"{self.time_str}  {self.file_path_str}: {self.content}"

    @property
    def log_file_line(self) -> str:
        """Builds the line description for the log file"""
        return self.VERBOSE_TOKEN + " " + self.line_description + "\n"

    def format(self, s: str) -> str:
        """Formats a string with the message inner color scheme"""
        return s.join(self.FMT)

    def print_in_console(self) -> None:
        """Verboses the message in the console"""
        print(self.format(self.VERBOSE_TOKEN) + " " + self.line_description)


class ErrorAbstract(MessageAbstract):
    """Error message base class"""

    FMT: Tuple[str, str] = ("\x1b[1;31;48m", "\x1b[0m")
    VERBOSE_TOKEN: str = "[ERR]"

    def __init__(
        self,
        file_path_str: Union[str, pathlib.Path],
        makedoc_paths: MakedocPaths,
        content: Optional[str] = None,
        code: Optional[int] = None,
        solution: Optional[str] = None,
    ) -> None:
        super().__init__(file_path_str, makedoc_paths, content, code, solution)
        if self.makedoc_paths.config_dict["verbosity"]["print-error"]:
            self.print_in_console()


class WarningAbstract(MessageAbstract):
    """Warning message base class"""

    FMT: Tuple[str, str] = ("\x1b[1;33;48m", "\x1b[0m")
    VERBOSE_TOKEN: str = "[WNG]"

    def __init__(
        self,
        file_path_str: Union[str, pathlib.Path],
        makedoc_paths: MakedocPaths,
        content: Optional[str] = None,
        code: Optional[int] = None,
        solution: Optional[str] = None,
    ) -> None:
        super().__init__(file_path_str, makedoc_paths, content, code, solution)
        if self.makedoc_paths.config_dict["verbosity"]["print-warning"]:
            self.print_in_console()


class InfoAbstract(MessageAbstract):
    """Info message base class"""

    FMT: Tuple[str, str] = ("\x1b[1;36;48m", "\x1b[0m")
    VERBOSE_TOKEN: str = "[NFO]"

    def __init__(
        self,
        file_path_str: Union[str, pathlib.Path],
        makedoc_paths: MakedocPaths,
        content: Optional[str] = None,
        code: Optional[int] = None,
        solution: Optional[str] = None,
    ) -> None:
        super().__init__(file_path_str, makedoc_paths, content, code, solution)
        if self.makedoc_paths.config_dict["verbosity"]["print-info"]:
            self.print_in_console()


class SuccessAbstract(MessageAbstract):
    """Success message base class"""

    FMT: Tuple[str, str] = ("\x1b[1;32;48m", "\x1b[0m")
    VERBOSE_TOKEN: str = "[SCS]"

    def __init__(
        self,
        file_path_str: Union[str, pathlib.Path],
        makedoc_paths: MakedocPaths,
        content: Optional[str] = None,
        code: Optional[int] = None,
        solution: Optional[str] = None,
    ) -> None:
        super().__init__(file_path_str, makedoc_paths, content, code, solution)
        if self.makedoc_paths.config_dict["verbosity"]["print-success"]:
            self.print_in_console()
