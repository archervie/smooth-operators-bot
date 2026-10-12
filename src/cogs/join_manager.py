import datetime
import logging
import random
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands

from core.base_cog import BaseCog

logger = logging.getLogger(__name__)


class JoinManager(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:

        logger.info(f"{member.name} has joined the server")
        if isinstance(self.GUILD, discord.Guild):
            member_num = self.GUILD.member_count
        else:
            return

        embed = discord.Embed(
            color=discord.Color.green(),
            description=f"{member.mention} has joined the server. They are member {member_num}.",
            title="Member Joined",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(
                f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
            )

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

        join_embed = discord.Embed(
            color=member.roles[0].color,
            description="Hello! Make sure to get roles in the roles channel. Please initialize your profile with /profile init!",
            title=f"Member {member_num}: {member.name} has joined the server!",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )

        welcome_gifs = [
            "https://i.imgur.com/NDBNYKh.gif",
            "https://i.imgur.com/vNsTQS1.gif",
        ]

        welcome_gif_url = random.choice(welcome_gifs)

        join_embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        join_embed.set_footer(text=f"User ID: {member.id}")
        join_embed.set_image(url=welcome_gif_url)

        if isinstance(self.LOBBY, discord.TextChannel):
            await self.LOBBY.send(embed=join_embed)
            logger.info(f"Sent welcome embed for {member.name}")
        else:
            logger.error(
                "Unable to send message to lobby due to an error with the channel type"
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

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.content == "jojodoss verify" and isinstance(
            message.channel, discord.DMChannel) and isinstance(self.GUILD, discord.Guild):
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
    await bot.add_cog(JoinManager(bot))
