import logging
import os

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

        self.bot = bot
        self.staff_channel_id = int(os.environ["STAFF_CHANNEL_ID"])
        self.subscribers_role_id = int(os.environ["SUBSCRIBERS_ROLE_ID"])
        self.guild_id = int(os.environ["GUILD_ID"])
        self.unverified_role_id = int(os.environ["UNVERIFIED_ROLE_ID"])

    async def _get_staff_channel(self) -> discord.TextChannel | None:
        channel = self.bot.get_channel(self.staff_channel_id)
        if not channel:
            logger.warning("Failed to fetch staff channel id from cache, pinging Discord")
            channel = await self.bot.fetch_channel(self.staff_channel_id)
        if isinstance(channel, discord.TextChannel):
            return channel
        return None

    async def _get_subscribers_role(self) -> discord.Object:
        return discord.Object(self.subscribers_role_id)

    async def _get_unverified_role(self) -> discord.Object:
        return discord.Object(self.unverified_role_id)

    async def _get_guild_obj(self) -> discord.Guild:
        guild = self.bot.get_guild(self.guild_id)
        if not guild:
            logger.warning("Failed to fetch guild id from cache, pinging Discord")
            guild = await self.bot.fetch_guild(self.guild_id)
        return guild


class BaseGroupCog(commands.GroupCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

        self.bot = bot
        self.staff_channel_id = int(os.environ["STAFF_CHANNEL_ID"])
        self.subscribers_role_id = int(os.environ["SUBSCRIBERS_ROLE_ID"])

    async def _get_staff_channel(self) -> discord.TextChannel | None:
        channel = self.bot.get_channel(self.staff_channel_id)
        if not channel:
            logger.warning("Failed to fetch staff channel id from cache, pinging Discord")
            channel = await self.bot.fetch_channel(self.staff_channel_id)
        if isinstance(channel, discord.TextChannel):
            return channel
        return None

    async def _get_subscribers_role(self) -> discord.Object:
        subscribers_role = discord.Object(os.environ["SUBSCRIBERS_ROLE_ID"])
        return subscribers_role
