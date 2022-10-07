"""Defines a logger object for handling makedoc logs"""

import pathlib
from datetime import datetime
from typing import List

from makedoc.logging.messages.concept.message_abstract import (
    ErrorAbstract,
    InfoAbstract,
    MessageAbstract,
    SuccessAbstract,
    WarningAbstract,
)
from makedoc.makedoc_paths import MakedocPaths


class Logger(object):
    """Logger object"""

    def __init__(self, makedoc_paths: MakedocPaths) -> None:
        self.makedoc_paths: MakedocPaths = makedoc_paths
        self.start_date: datetime = datetime.now()
        self.log_file_name: str = self.start_date.strftime("%Y-%m-%d_%H:%M:%S.log")
        self.log_file_path: pathlib.Path = self.makedoc_paths.logs / self.log_file_name

        self.makedoc_paths.logs.mkdir(parents=True, exist_ok=True)

        self.log_list: List[MessageAbstract] = []

    def add_log(self, msg: MessageAbstract) -> None:
        """Adds a message object to the list of logs"""
        self.log_list.append(msg)

    def save_log_file(self) -> None:
        """Saves the log file"""
        with open(self.log_file_path, "w+") as f:
            f.write(
                "#################################################\n"
                "#################  MAKEDOC LOG  #################\n"
                "#################################################\n\n"
            )

            nfos = [
                log_msg
                for log_msg in self.log_list
                if isinstance(log_msg, InfoAbstract)
            ]
            wngs = [
                log_msg
                for log_msg in self.log_list
                if isinstance(log_msg, WarningAbstract)
            ]
            errs = [
                log_msg
                for log_msg in self.log_list
                if isinstance(log_msg, ErrorAbstract)
            ]
            scss = [
                log_msg
                for log_msg in self.log_list
                if isinstance(log_msg, SuccessAbstract)
            ]
            f.write(
                "MESSAGE REPORT\n"
                f"    INFO    : {len(nfos)}\n"
                f"    SUCCESS : {len(scss)}\n"
                f"    WARNING : {len(wngs)}\n"
                f"    ERROR   : {len(errs)}\n\n"
            )

            if len(errs):
                f.write("ERRORS DETAILS\n")
                for err_num in list(set([log_msg.CODE for log_msg in errs])):
                    filtered_errs = [
                        log_msg for log_msg in errs if log_msg.CODE == err_num
                    ]
                    f.write(
                        f"    {len(filtered_errs)} ERROR [{err_num:03}]: {filtered_errs[0].__class__.__name__}\n"
                    )
                    for log_msg in filtered_errs:
                        if log_msg.SOLUTION:
                            f.write(f"        {log_msg.line_solution}\n")
                f.write("\n")
            if len(wngs):
                f.write("WARNINGS DETAILS\n")
                for wng_num in list(set([log_msg.CODE for log_msg in wngs])):
                    filtered_wngs = [
                        log_msg for log_msg in wngs if log_msg.CODE == wng_num
                    ]
                    f.write(
                        f"    {len(filtered_wngs)} WARNING [{wng_num:03}]: {filtered_wngs[0].__class__.__name__}\n"
                    )
                    for log_msg in filtered_wngs:
                        if log_msg.SOLUTION:
                            f.write(f"        {log_msg.line_solution}\n")
                f.write("\n")
            if len(nfos):
                f.write("INFOS DETAILS\n")
                for nfo_num in list(set([log_msg.CODE for log_msg in nfos])):
                    filtered_nfos = [
                        log_msg for log_msg in nfos if log_msg.CODE == nfo_num
                    ]
                    f.write(
                        f"    {len(filtered_nfos)} INFO [{nfo_num:03}]: {filtered_nfos[0].__class__.__name__}\n"
                    )
                    for log_msg in filtered_nfos:
                        if log_msg.SOLUTION:
                            f.write(f"        {log_msg.line_solution}\n")
                f.write("\n")
            if len(scss):
                f.write("SUCCESS DETAILS\n")
                for scs_num in list(set([log_msg.CODE for log_msg in scss])):
                    filtered_scss = [
                        log_msg for log_msg in scss if log_msg.CODE == scs_num
                    ]
                    f.write(
                        f"    {len(filtered_scss)} SUCCESS [{scs_num:03}]: {filtered_scss[0].__class__.__name__}\n"
                    )
                    for log_msg in filtered_scss:
                        if log_msg.SOLUTION:
                            f.write(f"        {log_msg.line_solution}\n")
                f.write("\n")

            f.write("LOG TIMELINE\n")

            for msg in self.log_list:
                f.write("    " + msg.log_file_line)
