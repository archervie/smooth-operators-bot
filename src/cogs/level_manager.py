import logging

import discord
from discord import app_commands
from discord.ext import commands

from core.base_group_cog import BaseGroupCog

logger = logging.getLogger(__name__)


class LevelManager(BaseGroupCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)
