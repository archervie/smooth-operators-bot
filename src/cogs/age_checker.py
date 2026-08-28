import datetime
import logging

import discord
from discord import app_commands
from discord.ext import commands

from core.base_cog import BaseCog

logger = logging.getLogger(__name__)


class JoinChecker(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)

    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:

        try:
            await member.add_roles(self.SUBSCRIBERS, reason="Joined the server.")
            logger.info(f"Granted {member.name} the subscribers role")
        except discord.errors.Forbidden:
            if isinstance(self.STAFF_CHANNEL, discord.TextChannel):
                await self.STAFF_CHANNEL.send(
                    f"Missing permissions for giving {member.name} subscriber role; please assign manually."
                )
                logger.error(
                    f"Missing permissions for giving {member.name} subscriber role; please assign manually."
                )
                
        create_time = member.created_at
        current_time = datetime.datetime.now(datetime.UTC)
        time_difference = current_time - create_time

        if time_difference.days < 122:
            timeout_date = datetime.timedelta(days=28)
            await member.timeout(
                timeout_date,
                reason=f"Account flagged, account is {time_difference.days} days old.",
            )
            logger.info(
                f"Account flagged for {member.name}: account is {time_difference.days} days old."
            )
            try:
                await member.add_roles(self.UNVERIFIED)
                logger.info(f"Granted {member.name} the unverified role")
            except discord.errors.Forbidden:
                if isinstance(self.STAFF_CHANNEL, discord.TextChannel):
                    await self.STAFF_CHANNEL.send(
                        f"Missing permissions for giving {member.name} unverified role; please assign manually."
                    )
                    logger.error(
                        f"Missing permissions for giving {member.name} unverified role; please assign manually."
                    )

            try:
                await member.send(
                    f"Welcome to **{member.guild.name}**, {member.name}! Unfortunately, due to an influx of scammers,"
                    f" your account was flagged for being only {time_difference.days} days old. If you believe"
                    " this was a mistake, please respond to this DM with the message 'jojodoss verify'. You will be untimed out afterwards."
                )
                logger.info(f"Successfully sent {member.name} verification DM")

            except discord.errors.Forbidden:
                logger.error(f"Unable to dm {member.name}, falling back to default.")
                if isinstance(self.STAFF_CHANNEL, discord.TextChannel):
                    await self.STAFF_CHANNEL.send(
                        f"Timed out **{member.name}** for having their account be {time_difference.days} days old, but was unable to DM them."
                        "Please keep this in mind, and act accordingly."
                    )

    @app_commands.allowed_contexts(guilds=False, dms=True, private_channels=False)
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.content == "jojodoss verify" and isinstance(
            self.GUILD, discord.Guild
        ):
            member = self.GUILD.get_member(message.author.id)

            if (
                isinstance(member, discord.Member)
                and member.timed_out_until is not None
                and self.UNVERIFIED not in member.roles
            ):
                await member.timeout(None)
                await member.remove_roles(self.UNVERIFIED)
                await member.send(
                    "Thank you for verifying yourself! You have been untimed out."
                )
                logger.info(f"Verified {member.name}, and removed unverified role")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(JoinChecker(bot))
