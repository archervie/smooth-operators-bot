import logging

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
        user_added = await self.add_user(id)
        if user_added:
            await interaction.response.send_message(
                "Your profile has been successfully initialized! Use /profile view to view your profile.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "Your profile has already been initialized.", ephemeral=True
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ProfileManager(bot))
