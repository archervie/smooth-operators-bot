import logging
import os

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

        self.guild_id = int(os.environ["GUILD_ID"])

        self.staff_channel_id = int(os.environ["STAFF_CHANNEL_ID"])
        self.lobby_id = int(os.environ["LOBBY_ID"])
        self.log_channel_id = int(os.environ["LOG_CHANNEL_ID"])

        self.subscribers_role_id = int(os.environ["SUBSCRIBERS_ROLE_ID"])
        self.unverified_role_id = int(os.environ["UNVERIFIED_ROLE_ID"])

        self.welcome_gif_1 = str(os.environ["WELCOME_GIF_1"])

    @property
    def GUILD(self) -> discord.Guild | None:
        return self.bot.get_guild(self.guild_id)

    @property
    def STAFF_CHANNEL(self) -> discord.TextChannel | None:
        channel = self.bot.get_channel(self.staff_channel_id)
        if isinstance(channel, discord.TextChannel):
            return channel
        return None

    @property
    def  LOBBY(self) -> discord.TextChannel | None:
        channel = self.bot.get_channel(self.lobby_id)
        if isinstance(channel, discord.TextChannel):
            return channel
        return None

    @property
    def LOG_CHANNEL(self) -> discord.TextChannel | None:
        channel = self.bot.get_channel(self.log_channel_id)
        if isinstance(channel, discord.TextChannel):
            return channel
        return None

    @property
    def SUBSCRIBERS(self) -> discord.Object:
        return discord.Object(self.subscribers_role_id)

    @property
    def UNVERIFIED(self) -> discord.Object:
        return discord.Object(self.unverified_role_id)

    @property
    def WELCOME_GIF_URLS(self) -> list:
        welcome_gifs = [
            self.welcome_gif_1
        ]
        return welcome_gifs
