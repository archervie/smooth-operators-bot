import asyncio
import logging
import os
from pathlib import Path
from typing import Union

import discord
from discord.ext import commands
from dotenv import load_dotenv

COG_EXTS = []
COG_PATH = Path("./cogs")

logger = logging.getLogger(__name__)


class SmoothOperators(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        for cog in COG_EXTS:
            await self.load_extension(f"{COG_PATH}.{cog}")
            logger.debug(f"Loaded extension: {cog}")
        await self.tree.sync()
        logger.info("Synced command tree")
        return await super().setup_hook()

    async def on_ready(self) -> None:
        await self.change_presence(
            activity=discord.Game(name="Searching for Lava Rocks")
        )
        logger.info("Switched status")
        logger.info("Bot is fully running")


def main() -> None:
    """
    Run the core bot.
    """

    dotenv_path: Union[str, os.PathLike[str]] = Path(".env")
    load_dotenv(dotenv_path=dotenv_path)

    discord.utils.setup_logging(level=logging.INFO)
    logger.setLevel(logging.DEBUG)
    logging.getLogger("discord").setLevel(logging.INFO)

    bot = SmoothOperators()

    try:
        bot.run(token=os.environ["TOKEN"], log_handler=None)
    except Exception as e:
        logger.error(f"An error has occurred\n\n{e}")


if __name__ == "__main__":
    main()
