from logging import Formatter, LogRecord
from typing import Literal

from colorama import init, Fore, Style

init(autoreset=True)


class LogConsoleFormatter(Formatter):
    DEFAULT_LEVEL_COLORS = {
        "DEBUG": Fore.BLUE,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA,
    }

    def __init__(
        self,
        fmt: str = None,
        datefmt: str = None,
        style: Literal["%", "{", "$"] = "{",
        validate: bool = True,
        *,
        level_colors: dict[str, str] = None,
        name_color: str = Fore.CYAN,
        msg_color: str = Fore.RESET,
        **kwargs,
    ):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate, **kwargs)
        self.level_colors = level_colors or self.DEFAULT_LEVEL_COLORS
        self.name_color = name_color
        self.msg_color = msg_color

    def format(self, record: LogRecord) -> str:
        level_name = f"{self.level_colors.get(record.levelname, Fore.RESET)}{record.levelname:8}{Style.RESET_ALL}"
        name = f"{self.name_color}{record.name}{Style.RESET_ALL}"
        msg = f"{self.msg_color}{record.msg}{Style.RESET_ALL}"

        r = LogRecord(
            name=name,
            level=record.levelno,
            pathname=record.pathname,
            lineno=record.lineno,
            msg=msg,
            args=record.args,
            exc_info=record.exc_info,
            func=record.funcName,
            sinfo=record.stack_info,
        )
        r.asctime = self.formatTime(r, self.datefmt)
        r.levelname = level_name

        return super().format(r)
