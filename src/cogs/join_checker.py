import datetime
import logging
import os

import discord
from discord.ext import commands

from core.base_cog import BaseCog

logger = logging.getLogger(__name__)

class JoinChecker(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        await self.runner()
        logger.info(f"{member.name} has joined the server")

        subscribers_role = discord.Object(os.environ["SUBSCRIBERS_ROLE_ID"])
        try:
            await member.add_roles(subscribers_role, reason="Joined the server.")
        except discord.errors.Forbidden:
            if isinstance(self.STAFF_CHANNEL, discord.TextChannel):
                await self.STAFF_CHANNEL.send(
                    f"Missing permissions for giving {member.name} role; please assign manually."
                )

        create_time = member.created_at
        current_time = datetime.datetime.now(datetime.timezone.utc)
        time_difference = current_time - create_time

        if time_difference.days < 122:
            timeout_date = datetime.timedelta(days=28)
            await member.timeout(
                timeout_date,
                reason=f"Account flagged, account is {time_difference.days} days old.",
            )

            try:
                await member.send(
                    f"Welcome to **{member.guild.name}**, {member.name}! Unfortunately, due to an influx of scammers,"
                    f" your account was flagged for being only {time_difference.days} days old. If you believe"
                    " this was a mistake, please respond to this DM with the message 'jojodoss verify'. You will be untimed out afterwards."
                )

            except discord.errors.Forbidden:
                logger.error(f"Unable to dm {member.name}, falling back to default.")

                if isinstance(self.STAFF_CHANNEL, discord.TextChannel):
                    await self.STAFF_CHANNEL.send(
                        f"Timed out **{member.name}** for having their account be {time_difference.days} days old, but was unable to DM them."
                        "Please keep this in mind, and act accordingly."
                    )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(JoinChecker(bot))
