import logging
import os
import sys
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

COG_EXTS = ["cogs.join_checker"]
DOTENV_PATH = Path(__file__).parent.parent / ".env"

load_dotenv(dotenv_path=DOTENV_PATH)

class ColoredFormatter(logging.Formatter):
    """Custom logging formatter that adds ANSI color codes based on log level."""

    GRAY = "\x1b[38;20m"
    CYAN = "\x1b[36;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    RED_BOLD = "\x1b[31;1m"
    RESET = "\x1b[0m"
    BOLD = "\x1b[1m"

    DEFAULT_FMT = "[{asctime}] [{levelname:<8}] {name}: {message}"

    FORMATS = {
        logging.DEBUG: BOLD + "[{asctime}] " + GRAY + "[{levelname}] " + RESET + "{name}: {message}" + RESET,
        logging.INFO: BOLD + "[{asctime}] " + GREEN + "[{levelname}] " + RESET + "{name}: {message}" + RESET,
        logging.WARNING: BOLD + "[{asctime}] " + YELLOW + "[{levelname}] " + RESET + "{name}: {message}" + RESET,
        logging.ERROR: BOLD + "[{asctime}] " + RED + "[{levelname}] " + RESET + "{name}: {message}" + RESET,
        logging.CRITICAL: BOLD + "[{asctime}] " + RED_BOLD + "[{levelname}] " + RESET + "{name}: {message}" + RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.DEFAULT_FMT)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


def setup_logging():
    formatter = ColoredFormatter()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


setup_logging()
logger = logging.getLogger(__name__)


class SmoothOperators(commands.Bot):
    def __init__(self) -> None:
        # This bot uses app commands, so the prefix isn't used
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        logger.info(f"Beginning ext loading, detected {len(COG_EXTS)} exts")
        for cog in COG_EXTS:
            await self.load_extension(cog)
            logger.info(f"Loaded ext: {cog}")
        await self.tree.sync()
        logger.info("Synced command tree, exiting ext setup")
        return await super().setup_hook()

    async def on_ready(self) -> None:
        await self.change_presence(
            activity=discord.Game(name="Searching for Lava Rocks")
        )
        logger.info("Switched status, please change if needed")
        logger.info(f"Bot is fully running, running at {self.latency}ms")


def main() -> None:
    """
    Run the core bot.
    """

    # We need to separate the bot logs and discord.py logs
    logging.getLogger("discord").setLevel(256)

    bot = SmoothOperators()

    try:
        # Currently using .env files for testing and development
        # purposes, replace with doppler eventually
        # Uncomment the line below for testing
        bot.run(token=os.environ["TEST_TOKEN"], log_handler=None)
        # bot.run(token=os.environ["TOKEN"], log_handler=None)

    except Exception as e:
        logger.error(f"An error has occurred\n\n{e}")


if __name__ == "__main__":
    main()
