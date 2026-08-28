import asyncio
import datetime
import logging
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands

from core.base_cog import BaseCog

logger = logging.getLogger(__name__)


class AutoLogger(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        logger.info(
            f"Message deleted by {message.author} in {message.channel}: {message.content}"
        )

        embed = discord.Embed(
            color=discord.Color.red(),
            description=message.content or "*[No text content / attachment only]*",
            title=f"Message Deleted in {message.jump_url}",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )
        embed.set_author(
            name=message.author.name, icon_url=message.author.display_avatar.url
        )

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(
                f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
            )

    @commands.Cog.listener()
    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ) -> None:
        if before.author.bot or before.content == after.content:
            return

        logger.info(
            f"Message edited by {before.author} in {before.channel}: {before.content} to {after.content}"
        )

        embed = discord.Embed(
            color=discord.Color.blue(),
            description=f"**Before:**\n{before.content}\n\n**After:**\n{after.content}",
            title=f"Message Edited in {before.jump_url}",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )
        embed.set_author(
            name=before.author.name, icon_url=before.author.display_avatar.url
        )

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(
                f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
            )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        logger.info(f"{member.name} has joined the server")

        embed = discord.Embed(
            color=discord.Color.green(),
            description=f"{member.mention} has joined the server",
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

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        await asyncio.sleep(0.5)

        is_kick = False
        kicker = None
        reason = None

        if member.guild.me.guild_permissions.view_audit_log:
            async for entry in member.guild.audit_logs(
                limit=3, action=discord.AuditLogAction.kick
            ):
                if (
                    entry.target.id == member.id
                    and (
                        datetime.datetime.now(datetime.UTC) - entry.created_at
                    ).total_seconds()
                    < 10
                ):
                    is_kick = True
                    kicker = entry.user
                    reason = entry.reason
                    break

        if is_kick:
            logger.info(f"{member.name} was kicked by {kicker}")
            embed = discord.Embed(
                color=discord.Color.red(),
                description=f"{member.mention} ({member.name}) was kicked by {kicker.mention if kicker else 'Unknown'}\n**Reason:** {reason or 'No reason provided'}",
                title="Member Kicked",
                timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
            )
        else:
            logger.info(f"{member.name} has left the server")
            embed = discord.Embed(
                color=discord.Color.orange(),
                description=f"{member.mention} has left the server",
                title="Member Left",
                timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
            )

        embed.set_author(name=member.name, icon_url=member.display_avatar.url)

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(
                f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
            )

    @commands.Cog.listener()
    async def on_member_ban(
        self, guild: discord.Guild, user: discord.User | discord.Member
    ) -> None:
        logger.info(f"{user.name} was banned from {guild.name}")

        reason = None
        banned_by = None
        if guild.me.guild_permissions.view_audit_log:
            async for entry in guild.audit_logs(
                limit=3, action=discord.AuditLogAction.ban
            ):
                if (
                    entry.target.id == user.id
                    and (
                        datetime.datetime.now(datetime.UTC) - entry.created_at
                    ).total_seconds()
                    < 10
                ):
                    banned_by = entry.user
                    reason = entry.reason
                    break

        embed = discord.Embed(
            color=discord.Color.dark_red(),
            description=f"{user.mention} ({user.name}) was banned by {banned_by.mention if banned_by else 'Unknown'}\n**Reason:** {reason or 'No reason provided'}",
            title="Member Banned",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )
        embed.set_author(name=user.name, icon_url=user.display_avatar.url)

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(
                f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
            )

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User) -> None:
        logger.info(f"{user.name} was unbanned from {guild.name}")

        unbanned_by = None
        if guild.me.guild_permissions.view_audit_log:
            async for entry in guild.audit_logs(
                limit=3, action=discord.AuditLogAction.unban
            ):
                if (
                    entry.target.id == user.id
                    and (
                        datetime.datetime.now(datetime.UTC) - entry.created_at
                    ).total_seconds()
                    < 10
                ):
                    unbanned_by = entry.user
                    break

        embed = discord.Embed(
            color=discord.Color.gold(),
            description=f"{user.mention} ({user.name}) was unbanned by {unbanned_by.mention if unbanned_by else 'Unknown'}",
            title="Member Unbanned",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )
        embed.set_author(name=user.name, icon_url=user.display_avatar.url)

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(
                f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
            )

    @commands.Cog.listener()
    async def on_member_update(
        self, before: discord.Member, after: discord.Member
    ) -> None:
        if before.display_avatar != after.display_avatar:
            logger.info(f"{after.name} changed their avatar")

            embed = discord.Embed(
                color=discord.Color.teal(),
                description=f"{after.mention} updated their avatar.\n[New Avatar URL]({after.display_avatar.url})",
                title=f"Avatar Changed: {after.name}",
                timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
            )
            embed.set_thumbnail(url=after.display_avatar.url)
            embed.set_author(name=after.name, icon_url=after.display_avatar.url)

            if isinstance(self.LOG_CHANNEL, discord.TextChannel):
                await self.LOG_CHANNEL.send(embed=embed)
            else:
                logger.error(
                    f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
                )

        if before.nick != after.nick:
            logger.info(
                f"{after.name} changed nickname from {before.nick} to {after.nick}"
            )

            embed = discord.Embed(
                color=discord.Color.gold(),
                description=f"**Before:** {before.nick or '*None*'}\n**After:** {after.nick or '*None*'}",
                title=f"Nickname Changed: {after.name}",
                timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
            )
            embed.set_author(name=after.name, icon_url=after.display_avatar.url)

            if isinstance(self.LOG_CHANNEL, discord.TextChannel):
                await self.LOG_CHANNEL.send(embed=embed)
            else:
                logger.error(
                    f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
                )

        if before.roles != after.roles:
            added = [r.mention for r in after.roles if r not in before.roles]
            removed = [r.mention for r in before.roles if r not in after.roles]
            desc = ""
            if added:
                desc += f"**Added Roles:** {', '.join(added)}\n"
            if removed:
                desc += f"**Removed Roles:** {', '.join(removed)}"

            logger.info(f"{after.name} had roles updated")

            embed = discord.Embed(
                color=discord.Color.purple(),
                description=desc,
                title=f"Roles Updated: {after.name}",
                timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
            )
            embed.set_author(name=after.name, icon_url=after.display_avatar.url)

            if isinstance(self.LOG_CHANNEL, discord.TextChannel):
                await self.LOG_CHANNEL.send(embed=embed)
            else:
                logger.error(
                    f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
                )

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        if before.channel == after.channel:
            return

        desc = ""
        title = ""
        if before.channel is None and after.channel is not None:
            title = "Voice Channel Joined"
            desc = f"{member.mention} joined **{after.channel.name}**"
        elif before.channel is not None and after.channel is None:
            title = "Voice Channel Left"
            desc = f"{member.mention} left **{before.channel.name}**"
        elif before.channel is not None and after.channel is not None:
            title = "Voice Channel Switched"
            desc = f"{member.mention} moved from **{before.channel.name}** to **{after.channel.name}**"

        logger.info(f"Voice update for {member.name}: {title}")

        embed = discord.Embed(
            color=discord.Color.teal(),
            description=desc,
            title=title,
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(
                f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
            )

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role) -> None:
        logger.info(f"Role created: {role.name}")

        embed = discord.Embed(
            color=discord.Color.green(),
            description=f"Role {role.mention} (`{role.name}`) has been created.",
            title="Role Created",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(
                f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
            )

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role) -> None:
        logger.info(f"Role deleted: {role.name}")

        embed = discord.Embed(
            color=discord.Color.red(),
            description=f"Role `{role.name}` has been deleted.",
            title="Role Deleted",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(
                f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
            )

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel) -> None:
        logger.info(f"Channel created: {channel.name}")

        embed = discord.Embed(
            color=discord.Color.green(),
            description=f"Channel {channel.mention} has been created.",
            title="Channel Created",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(
                f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
            )

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel) -> None:
        logger.info(f"Channel deleted: {channel.name}")

        embed = discord.Embed(
            color=discord.Color.red(),
            description=f"Channel `#{channel.name}` has been deleted.",
            title="Channel Deleted",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(
                f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
            )

    @commands.Cog.listener()
    async def on_guild_channel_update(
        self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel
    ) -> None:
        changes = []

        if before.name != after.name:
            changes.append(f"**Name:** `#{before.name}` ➔ `#{after.name}`")

        if getattr(before, "topic", None) != getattr(after, "topic", None):
            changes.append(
                f"**Topic:**\nBefore: {getattr(before, 'topic', None) or '*None*'}\nAfter: {getattr(after, 'topic', None) or '*None*'}"
            )

        if getattr(before, "slowmode_delay", None) != getattr(
            after, "slowmode_delay", None
        ):
            changes.append(
                f"**Slowmode:** `{getattr(before, 'slowmode_delay', 0)}s` ➔ `{getattr(after, 'slowmode_delay', 0)}s`"
            )

        if before.overwrites != after.overwrites:
            before_targets = set(before.overwrites.keys())
            after_targets = set(after.overwrites.keys())

            for target in after_targets - before_targets:
                target_name = (
                    target.mention if hasattr(target, "mention") else f"`{target.name}`"
                )
                changes.append(f"**Permission Overwrite Added:** for {target_name}")

            for target in before_targets - after_targets:
                target_name = (
                    target.mention if hasattr(target, "mention") else f"`{target.name}`"
                )
                changes.append(f"**Permission Overwrite Removed:** for {target_name}")

            for target in before_targets & after_targets:
                if before.overwrites[target] != after.overwrites[target]:
                    target_name = (
                        target.mention
                        if hasattr(target, "mention")
                        else f"`{target.name}`"
                    )
                    changes.append(f"**Permissions Modified:** for {target_name}")

        if not changes:
            return

        logger.info(f"Channel updated: {after.name}")

        embed = discord.Embed(
            color=discord.Color.blue(),
            description=f"Changes made to {after.mention}:\n\n" + "\n\n".join(changes),
            title="Channel Updated",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(
                f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
            )

    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite) -> None:
        logger.info(f"Invite created: {invite.code}")

        inviter = invite.inviter.mention if invite.inviter else "Unknown"
        max_uses = "Unlimited" if invite.max_uses == 0 else str(invite.max_uses)
        duration = f"{invite.max_age}s" if invite.max_age != 0 else "Never"

        embed = discord.Embed(
            color=discord.Color.green(),
            description=(
                f"**Code:** `{invite.code}`\n"
                f"**Channel:** {invite.channel.mention if invite.channel else 'Unknown'}\n"
                f"**Creator:** {inviter}\n"
                f"**Max Uses:** {max_uses}\n"
                f"**Expires In:** {duration}"
            ),
            title="Invite Created",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(
                f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
            )

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite) -> None:
        logger.info(f"Invite deleted: {invite.code}")

        embed = discord.Embed(
            color=discord.Color.red(),
            description=(
                f"**Code:** `{invite.code}`\n"
                f"**Channel:** {invite.channel.mention if invite.channel else 'Unknown'}"
            ),
            title="Invite Deleted",
            timestamp=datetime.datetime.now(tz=ZoneInfo("America/New_York")),
        )

        if isinstance(self.LOG_CHANNEL, discord.TextChannel):
            await self.LOG_CHANNEL.send(embed=embed)
        else:
            logger.error(
                f"Log channel is not TextChannel, please fix: {self.LOG_CHANNEL}"
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoLogger(bot))
