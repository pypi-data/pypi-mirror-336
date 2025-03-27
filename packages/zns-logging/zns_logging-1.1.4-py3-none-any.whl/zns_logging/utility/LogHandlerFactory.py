from logging import StreamHandler, Formatter
from logging.handlers import RotatingFileHandler

from zns_logging.constant.HandlerConstant import HandlerConstant
from zns_logging.utility.LogConsoleFormatter import LogConsoleFormatter


class LogHandlerFactory:
    @staticmethod
    def create_console_handler(
        fmt: str = HandlerConstant.CONSOLE_FORMAT_STR,
        datefmt: str = HandlerConstant.DATE_FORMAT_STR,
        level_colors: dict[str, str] = HandlerConstant.MISSING,
        name_color: str = HandlerConstant.CONSOLE_COLOR_NAME,
        msg_color: str = HandlerConstant.CONSOLE_COLOR_MESSAGE,
    ) -> StreamHandler:
        handler = StreamHandler()
        formatter = LogConsoleFormatter(
            fmt=fmt,
            datefmt=datefmt,
            level_colors=level_colors,
            name_color=name_color,
            msg_color=msg_color,
        )
        handler.setFormatter(formatter)

        return handler

    @staticmethod
    def create_file_handler(
        filename: str,
        mode: str = HandlerConstant.FILE_MODE,
        maxBytes: int = HandlerConstant.FILE_MAX_BYTES,
        backupCount: int = HandlerConstant.FILE_BACKUP_COUNT,
        encoding: str = HandlerConstant.FILE_ENCODING,
        delay: bool = HandlerConstant.FILE_DELAY,
        errors: str = HandlerConstant.FILE_ERRORS,
        fmt: str = HandlerConstant.FILE_FORMAT_STR,
        datefmt: str = HandlerConstant.DATE_FORMAT_STR,
    ) -> StreamHandler:
        handler = RotatingFileHandler(
            filename=filename,
            mode=mode,
            maxBytes=maxBytes,
            backupCount=backupCount,
            encoding=encoding,
            delay=delay,
            errors=errors,
        )
        formatter = Formatter(fmt, datefmt)
        handler.setFormatter(formatter)

        return handler
