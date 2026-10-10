import datetime
import logging
from zoneinfo import ZoneInfo

import discord
from discord import app_commands
from discord.ext import commands

from core.base_group_cog import BaseGroupCog

logger = logging.getLogger(__name__)


@app_commands.allowed_installs(guilds=True, users=False)
@app_commands.allowed_contexts(dms=False, guilds=True, private_channels=False)
class ProfileManager(BaseGroupCog, name="profile"):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)

    @app_commands.command(description="Initialize your profile", name="init")
    async def profile_init(self, interaction: discord.Interaction) -> None:
        id = interaction.user.id
        user_added = await self.add_user_to_db(id)
        if user_added:
            await interaction.response.send_message(
                "Your profile has been successfully initialized! Use /profile view to view your profile.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "Your profile has already been initialized.", ephemeral=True
            )

    @app_commands.command(description="View a user's profile", name="view")
    async def profile_view(
        self, interaction: discord.Interaction, user: discord.User = None
    ) -> None:
        if not user:
            user = interaction.user

        id = user.id
        user_profile = await self.get_user_from_db(id)

        if not user_profile:
            await interaction.response.send_message(
                "Profile does not exist.", ephemeral=True
            )

        embed = discord.Embed(
            color=discord.Color.blue(),
            title=f"{user}'s Profile",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )

        embed.set_author(
            name=interaction.user.name, icon_url=interaction.user.display_avatar.url
        )
        embed.set_thumbnail(url=user.display_avatar.url)

        total_xp_needed = self.get_xp_needed(user_profile["level"])

        embed.add_field(name="ID", value=user_profile["id"], inline=False)
        embed.add_field(name="Level", value=user_profile["level"], inline=False)
        embed.add_field(name="Title", value=user_profile["title"], inline=False)
        embed.add_field(name="XP Gained", value=user_profile["xp_gained"], inline=False)
        embed.add_field(name="Total XP Needed", value=total_xp_needed)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ProfileManager(bot))
