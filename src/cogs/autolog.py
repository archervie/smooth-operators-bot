import datetime
import logging
from zoneinfo import ZoneInfo

import discord
from discord import app_commands
from discord.ext import commands

from core.base_cog import BaseCog

logger = logging.getLogger(__name__)

class AutoLogger(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)


    @app_commands.allowed_contexts(guilds=False, dms=True, private_channels=False)
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:

        if message.author.bot:
            return

        logger.info(f"Message deleted by {message.author} in {message.channel}: {message.content}")

        embed = discord.Embed(
            color=discord.Color.red(),
            description=message.content,
            title=f"Message Deleted in {message.channel.jump_url}",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )

        embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}")

    @app_commands.allowed_contexts(guilds=False, dms=True, private_channels=False)
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:

        if before.author.bot:
            return

        logger.info(f"Message edited by {before.author} in {before.channel}: {before.content} to {after.content}")

        embed = discord.Embed(
            color=discord.Color.blue(),
            description=
            f"**Before:**\n{before.content}\n\n**After**:\n{after.content}",
            title=f"Message Edited in {before.jump_url}",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York"))
        )

        embed.set_author(name=before.author.name, icon_url=before.author.display_avatar.url)

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}")

    @app_commands.allowed_contexts(guilds=False, dms=True, private_channels=False)
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        logger.info(f"{member.name} has joined the server")

        embed = discord.Embed(
            color=discord.Color.green(),
            description=f"{member.mention} has joined the server",
            title="Member Joined",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York"))
        )

        embed.set_author(name=member.name, icon_url=member.display_avatar.url)

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}")

    @app_commands.allowed_contexts(guilds=False, dms=True, private_channels=False)
    @commands.Cog.listener()
    async def on_member_leave(self, member: discord.Member) -> None:
        logger.info(f"{member.name} has left the server")

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"{member.mention} has left the server",
            title="Member Left",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York"))
        )

        embed.set_author(name=member.name, icon_url=member.display_avatar.url)

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoLogger(bot))
