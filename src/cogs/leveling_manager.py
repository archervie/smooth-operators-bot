import datetime
import logging
import random
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands

from core.base_group_cog import BaseGroupCog

logger = logging.getLogger(__name__)


class LevelingManager(BaseGroupCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        user_profile = await self.get_user_from_db(message.author.id)
        if not user_profile:
            return

        xp_amount = random.randrange(15, 25)
        await self.add_xp(message.author.id, xp_amount)
        leveled_up = await self.check_and_apply_level_up(message.author.id)
        if leveled_up:
            embed = discord.Embed(
                color=discord.Color.green(),
                description=f"{message.author.name} leveled up to {leveled_up['new_level']}!",
                title="Level Up!",
                timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
            )
            logger.info(f"{message.author.name} leveled up to {leveled_up['new_level']}")

            embed.set_thumbnail(url=message.author.display_avatar.url)
            await message.channel.send(embed=embed)

            if leveled_up["old_title"] != leveled_up["new_title"]:
                if message.guild:
                    member = await message.guild.fetch_member(message.author.id)
                else:
                    logger.error(f"Unable to fetch guild of message of ID {message.id}")
                    return

                if isinstance(member, discord.Member):
                    match leveled_up["new_title"]:
                        case "Hamon User":
                            await member.add_roles(self.TIER_1)
                        case "Stand User":
                            await member.add_roles(self.TIER_2)
                        case "Joestar":
                            await member.add_roles(self.TIER_3)

                logger.info(f"Provided {message.author} with {leveled_up['new_title']} role")



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(LevelingManager(bot))
