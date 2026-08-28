import logging
import sys
import typing
from logging.handlers import RotatingFileHandler


@typing.final
class ColoredFormatter(logging.Formatter):
    """Custom logging formatter that adds ANSI color codes based on log level."""

    def __init__(self) -> None:
        super().__init__()
        GRAY = "\x1b[38;20m"
        CYAN = "\x1b[36;20m"
        GREEN = "\x1b[32;20m"
        YELLOW = "\x1b[33;20m"
        RED = "\x1b[31;20m"
        RED_BOLD = "\x1b[31;1m"
        RESET = "\x1b[0m"
        BOLD = "\x1b[1m"

        self.DEFAULT_FMT = "{asctime} {levelname} {name}: {message}"

        self.FORMATS = {
            logging.DEBUG: BOLD
            + GRAY
            + "{asctime} "
            + RESET
            + CYAN
            + "{levelname} "
            + RESET
            + "{name}: {message}"
            + RESET,
            logging.INFO: BOLD
            + GRAY
            + "{asctime} "
            + RESET
            + GREEN
            + "{levelname} "
            + RESET
            + "{name}: {message}"
            + RESET,
            logging.WARNING: BOLD
            + GRAY
            + "{asctime} "
            + RESET
            + YELLOW
            + "{levelname} "
            + RESET
            + "{name}: {message}"
            + RESET,
            logging.ERROR: BOLD
            + GRAY
            + "{asctime} "
            + RESET
            + RED
            + "{levelname} "
            + RESET
            + "{name}: {message}"
            + RESET,
            logging.CRITICAL: BOLD
            + GRAY
            + "{asctime} "
            + RESET
            + RED_BOLD
            + "{levelname} "
            + RESET
            + "{name}: {message}"
            + RESET,
        }

    @typing.override
    def format(self, record: logging.LogRecord):
        log_fmt = self.FORMATS.get(record.levelno, self.DEFAULT_FMT)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


def setup_logging():
    formatter = ColoredFormatter()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        filename="bot.log",
        encoding="utf-8",
        maxBytes=5 * 1024 * 1024,  # 5 MiB
        backupCount=5,
    )

    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
