import logging

import discord
from discord import app_commands
from discord.ext import commands

from core.base_cog import BaseCog

logger = logging.getLogger(__name__)


class GlobalErrorHandler(BaseCog):
    """
    Handle all specific errors.
    """

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        """
        Respond to specific errors that can occur.

        Args:
            interaction (discord.Interaction): The interaction where the error occurred.
            error (app_commands.AppCommandError): The specific error raised.
        """

        # This handles missing permissions
        if isinstance(error, app_commands.CheckFailure):
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        "Sorry, you don't have permission to do this.", ephemeral=True
                    )
            finally:
                logger.warning(f"Missing permissions causing error: {error}")

        # This handles any cooldown errors.
        elif isinstance(error, app_commands.CommandOnCooldown):
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"There seems to be a cooldown. Try again in {error.retry_after:.1f} seconds.",
                        ephemeral=True,
                    )
            finally:
                if isinstance(interaction.command, app_commands.Command):
                    logger.info(
                        f"Cooldown needed for {interaction.command.name}. Try again in {error.retry_after:.1f}"
                    )

        # For any unexpected bugs
        else:
            logger.error(
                f"Ignoring exception in command {interaction.command}: {error}"
            )

            # Only send a message if we haven't already responded
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "An unknown error seems to have occurred.",
                    ephemeral=True,
                )

            if isinstance(interaction.command, app_commands.Command):
                logger.error(
                    f"An unknown error seems to have occurred for command {interaction.command.name}."
                )


async def setup(bot: commands.Bot):
    await bot.add_cog(GlobalErrorHandler(bot))
