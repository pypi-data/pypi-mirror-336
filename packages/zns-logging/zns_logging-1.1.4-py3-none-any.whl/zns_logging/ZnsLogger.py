import inspect
import logging
from typing import Type

from zns_logging.constant.HandlerConstant import HandlerConstant
from zns_logging.constant.LoggerConstant import LoggerConstant
from zns_logging.utility.LogHandlerFactory import LogHandlerFactory

_ALLOWED_LEVELS = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]


def _check_level(level: int | str) -> int:
    if isinstance(level, str):
        level = logging.getLevelName(level.upper())
    elif isinstance(level, int):
        pass
    else:
        raise TypeError(f"Expected str or int, got {type(level).__name__}")

    if level not in _ALLOWED_LEVELS:
        raise ValueError(f"Expected one of {_ALLOWED_LEVELS}, got {level}")

    return level


class ZnsLogger(logging.Logger):
    def __init__(
        self,
        name: str,
        level: int | str = logging.INFO,
        *,
        console_format_str: str = HandlerConstant.CONSOLE_FORMAT_STR,
        console_level_colors: dict[str, str] = HandlerConstant.MISSING,
        console_color_name: str = HandlerConstant.CONSOLE_COLOR_NAME,
        console_color_message: str = HandlerConstant.CONSOLE_COLOR_MESSAGE,
        file_path: str = HandlerConstant.MISSING,
        file_mode: str = HandlerConstant.FILE_MODE,
        file_max_bytes: int = HandlerConstant.FILE_MAX_BYTES,
        file_backup_count: int = HandlerConstant.FILE_BACKUP_COUNT,
        file_encoding: str = HandlerConstant.FILE_ENCODING,
        file_delay: bool = HandlerConstant.FILE_DELAY,
        file_errors: str = HandlerConstant.FILE_ERRORS,
        file_format_str: str = HandlerConstant.FILE_FORMAT_STR,
        date_format_str: str = HandlerConstant.DATE_FORMAT_STR,
        enable_console_logging: bool = LoggerConstant.ENABLE_CONSOLE_LOGGING,
        enable_file_logging: bool = LoggerConstant.ENABLE_FILE_LOGGING,
    ):
        _check_level(level)

        super().__init__(name, level)

        if enable_console_logging:
            console_handler = LogHandlerFactory.create_console_handler(
                fmt=console_format_str,
                datefmt=date_format_str,
                level_colors=console_level_colors,
                name_color=console_color_name,
                msg_color=console_color_message,
            )
            self.addHandler(console_handler)

        if enable_file_logging and file_path:
            file_handler = LogHandlerFactory.create_file_handler(
                filename=file_path,
                mode=file_mode,
                maxBytes=file_max_bytes,
                backupCount=file_backup_count,
                encoding=file_encoding,
                delay=file_delay,
                errors=file_errors,
                fmt=file_format_str,
                datefmt=date_format_str,
            )
            self.addHandler(file_handler)

        self.propagate = False

    def log_and_raise(self, message: str, n: Type[Exception], e: Exception = None) -> None:
        if not issubclass(n, Exception):
            raise TypeError("exception_type must be a subclass of Exception")

        file = inspect.stack()[1].filename
        m = f"{message} - Module: [{file}]"

        self.error(m)
        raise n(m) from e

__all__ = ["ZnsLogger"]
