import logging
from typing import Literal

from colorama import init, Fore, Style

init(autoreset=True)

class LogConsoleFormatter(logging.Formatter):
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
        color_name: str = Fore.CYAN,
        color_message: str = Fore.RESET,
        level_colors: dict[str, str] = None,
        **kwargs,
    ):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate, **kwargs)
        self.color_name = color_name
        self.color_message = color_message
        self.level_colors = level_colors or self.DEFAULT_LEVEL_COLORS

    def format(self, record: logging.LogRecord) -> str:
        level_name = f"{self.level_colors.get(record.levelname, Fore.RESET)}{record.levelname:8}{Style.RESET_ALL}"
        name = f"{self.color_name}{record.name}{Style.RESET_ALL}"
        msg = f"{self.color_message}{record.msg}{Style.RESET_ALL}"

        r = logging.LogRecord(
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
