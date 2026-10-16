import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import config_loader
from database import init_db
from logger import setup_logging

COG_EXTS = [
    "cogs.auto_logger",
    "cogs.join_manager",
    "cogs.profile_manager",
    "cogs.leveling_manager",
]
CONFIGS = config_loader()
DOTENV_PATH = Path(__file__).parent.parent / ".env"

setup_logging()

load_dotenv(dotenv_path=DOTENV_PATH)
logger = logging.getLogger(__name__)


class SmoothOperators(commands.Bot):
    def __init__(self) -> None:
        # This bot uses app commands, so the prefix isn't used
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=commands.DefaultHelpCommand(),
        )

    async def setup_hook(self) -> None:
        logger.info("Beginning database initialization")
        await init_db()

        logger.info(
            f"Beginning extension loading, detected {len(COG_EXTS)} extensions..."
        )

        await self.load_extension("core.error_handler")
        logger.info("Loaded error handler cog...")

        for cog in COG_EXTS:
            await self.load_extension(cog)
            logger.info(f"Loaded extension: {cog}...")

        _ = await self.tree.sync()
        logger.info("Synced command tree, exiting extension setup...")
        return await super().setup_hook()

    async def on_ready(self) -> None:
        await self.change_presence(
            activity=discord.Game(name="Searching for Lava Rocks")
        )
        logger.info("Switched status, please change if needed")
        logger.info(
            f"Smooth Operators is up; running at {round(self.latency * 1000, 2)}ms"
        )


def main() -> None:
    bot = SmoothOperators()
    logger.info("Running bot...")
    bot.run(
        token=os.environ["TOKEN"],
        reconnect=True,
        log_handler=None,
        root_logger=True,
    )


if __name__ == "__main__":
    main()
