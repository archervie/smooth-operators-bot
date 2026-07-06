import asyncio
import logging
import os
from pathlib import Path
from typing import Union

import discord
from discord.ext import commands
from dotenv import load_dotenv

logger = logging.Logger(__name__)


async def main() -> None:
    """
    Run the core bot.
    """

    dotenv_path: Union[str, os.PathLike[str]] = Path(".env")
    load_dotenv(dotenv_path=dotenv_path)

    intents = discord.Intents.default()

    # This bot uses application commands, not prefix commands
    bot = commands.Bot(command_prefix="!", intents=intents)

    try:
        bot.run(token=os.environ["TOKEN"])
    except Exception as e:
        logger.error(f"An error has occurred :{e}")


if __name__ == "__main__":
    asyncio.run(main())
