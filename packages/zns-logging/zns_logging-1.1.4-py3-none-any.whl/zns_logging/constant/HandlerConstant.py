from colorama import Fore


class HandlerConstant:
    MISSING = None

    DATE_FORMAT_STR = "%Y-%m-%d %H:%M:%S"

    CONSOLE_FORMAT_STR = "[{asctime}] [{levelname}] [{name}]: {message}"
    CONSOLE_COLOR_NAME = Fore.CYAN
    CONSOLE_COLOR_MESSAGE = Fore.RESET

    FILE_FORMAT_STR = "[%(asctime)s] [%(levelname)-8s] [%(name)s]: %(message)s"
    FILE_MODE = "a"
    FILE_MAX_BYTES = 1024 * 1024
    FILE_BACKUP_COUNT = 4
    FILE_ENCODING = "utf-8"
    FILE_DELAY = False
    FILE_ERRORS = None
