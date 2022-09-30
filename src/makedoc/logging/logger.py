"""Defines a logger object for handling makedoc logs"""

import pathlib
from datetime import datetime
from typing import List

from makedoc.logging.messages.concept.message_abstract import MessageAbstract
from makedoc.makedoc_paths import MakedocPaths


class Logger(object):
    """Logger object"""

    def __init__(self, makedoc_paths: MakedocPaths) -> None:
        self.makedoc_paths: MakedocPaths = makedoc_paths
        self.start_date: datetime = datetime.now()
        self.log_file_name: str = self.start_date.strftime("%Y-%m-%d_%H:%M:%S.log")
        self.log_file_path: pathlib.Path = self.makedoc_paths.logs / self.log_file_name

        self.makedoc_paths.logs.mkdir(parents=True, exist_ok=True)
        self.log_file_path.touch()

        self.log_list: List[MessageAbstract] = []

    def add_log(self, msg: MessageAbstract) -> None:
        """Adds a message object to the list of logs"""
        self.log_list.append(msg)

    def save_log_file(self) -> None:
        """Saves the log file"""
        with open(self.log_file_path, "w") as f:
            for msg in self.log_list:
                f.write(msg.log_file_line)
