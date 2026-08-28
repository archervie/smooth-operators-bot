import datetime
import logging
import random
from zoneinfo import ZoneInfo

import discord
from discord import app_commands
from discord.ext import commands

from core.base_cog import BaseCog

logger = logging.getLogger(__name__)

class Welcome(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)

    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
    
        join_embed = discord.Embed(
            color=member.roles[0].color,
            description="Say hello to them! Make sure to get roles in the roles channel.",
            title=f"{member.name} joined the server!",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York"))
        )
        
        welcome_gif_url = random.choice(self.WELCOME_GIF_URLS)

        join_embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        join_embed.set_footer(text=f"User ID: {member.id}")
        join_embed.set_image(url=welcome_gif_url)
        
        if isinstance(self.LOBBY, discord.TextChannel):
            await self.LOBBY.send(embed=join_embed)
            logger.info(f"Sent welcome embed for {member.name}")
        else:
            logger.error("Unable to send message to lobby due to an error with the channel type")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Welcome(bot))
