import logging

import discord
from discord.ext import commands

from config import config_loader

logger = logging.getLogger(__name__)


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.config = config_loader()

    @property
    def GUILD(self) -> discord.Guild | None:
        return self.bot.get_guild(self.config["core"]["guild"])

    @property
    def STAFF_CHANNEL(self) -> discord.TextChannel | None:
        channel = self.bot.get_channel(self.config["channels"]["staff"])
        if isinstance(channel, discord.TextChannel):
            return channel
        return None

    @property
    def LOBBY(self) -> discord.TextChannel | None:
        channel = self.bot.get_channel(self.config["channels"]["lobby"])
        if isinstance(channel, discord.TextChannel):
            return channel
        return None

    @property
    def LOG_CHANNEL(self) -> discord.TextChannel | None:
        channel = self.bot.get_channel(self.config["channels"]["logs"])
        if isinstance(channel, discord.TextChannel):
            return channel
        return None

    @property
    def SUBSCRIBERS(self) -> discord.Object:
        return discord.Object(self.config["roles"]["subscribers"])

    @property
    def UNVERIFIED(self) -> discord.Object:
        return discord.Object(self.config["roles"]["unverified"])

    @property
    def WELCOME_GIF_URLS(self) -> list:
        welcome_gifs = [
            self.config["welcome"]["gif_1"],
            self.config["welcome"]["gif_2"],
        ]
        return welcome_gifs
