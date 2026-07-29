import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import config_loader
from logger import setup_logging

COG_EXTS = ["cogs.autolog", "cogs.join_checker", "cogs.welcome"]
CONFIGS = config_loader()
DOTENV_PATH = Path(__file__).parent.parent / ".env"

setup_logging()
load_dotenv(dotenv_path=DOTENV_PATH)
logger = logging.getLogger(__name__)


class SmoothOperators(commands.Bot):
    """
    Bot class for SmoothOperators
    """

    def __init__(self) -> None:
        # This bot uses app commands, so the prefix isn't used
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=commands.DefaultHelpCommand(),
        )

    async def setup_hook(self) -> None:
        logger.info(
            f"Beginning extension loading, detected {len(COG_EXTS)} extensions..."
        )

        await self.load_extension("core.error_handler")

        for cog in COG_EXTS:
            await self.load_extension(cog)
            logger.info(f"Loaded ext: {cog}...")

        await self.tree.sync()
        logger.info("Synced command tree, exiting ext setup...")
        return await super().setup_hook()

    async def on_ready(self) -> None:
        await self.change_presence(
            activity=discord.Game(name="Searching for Lava Rocks")
        )
        logger.info("Switched status, please change if needed")
        logger.info(
            f"Bot is fully running; running at {round(self.latency * 1000, 2)}ms"
        )


def main() -> None:
    """
    Run the core bot.
    """

    bot = SmoothOperators()

    # Currently using .env files for testing and development
    # purposes, replace with doppler eventually
    # Uncomment the line below for testing
    if CONFIGS["core"]["bot"] == 1:
        bot.run(
            token=os.environ["TOKEN"],
            reconnect=True,
            log_handler=None,
            root_logger=True,
        )
    else:
        bot.run(
            token=os.environ["TEST_TOKEN"],
            reconnect=True,
            log_handler=None,
            root_logger=True,
        )


if __name__ == "__main__":
    main()
