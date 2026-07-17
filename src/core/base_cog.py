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

    async def runner(self) -> None:
        self.STAFF_CHANNEL = await self._get_staff_channel()
        self.SUBSCRIBERS_ROLE = await self._get_subscribers_role()



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
