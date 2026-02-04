import logging
from datetime import timedelta

import discord
from discord.ext import commands

from database.service import DatabaseService
from services.moderation import ModerationService
from utils.checks import check_hierarchy
from utils.embeds import EmbedBuilder

logger = logging.getLogger(__name__)


class ModerationCog(commands.Cog):
    """Moderation Commands"""

    def __init__(self, bot):
        self.bot = bot

    async def _log_moderation(
        self,
        guild_id: int,
        user_id: int,
        moderator_id: int,
        action: str,
        reason: str,
        duration: int = None,
    ):
        """Log Moderation Action To Database"""
        async with self.bot.db_session() as session:
            service = ModerationService(session)
            await service.log_case(
                guild_id=guild_id,
                user_id=user_id,
                moderator_id=moderator_id,
                action=action,
                reason=reason,
                duration=duration,
            )

    async def _send_mod_log(self, guild: discord.Guild, embed: discord.Embed):
        """Send Moderation Log To Mod Channel"""
        # Try cache first? The service doesn't have access to cache directly here easily unless we pass bot.
        # But for mod logs, we can use the bot's cache.
        config = self.bot.cache.get_config(guild.id)
        if not config:
            async with self.bot.db_session() as session:
                db = DatabaseService(session, self.bot.cache)
                config = await db.get_guild_config(guild.id)

        if not config or not config.modlog_channel_id:
            return

        mod_channel = guild.get_channel(config.modlog_channel_id)
        if mod_channel:
            try:
                await mod_channel.send(embed=embed)
            except discord.Forbidden:
                logger.warning(f"Cannot send to mod log in {guild}")

    @commands.hybrid_command(name="ban", help="Ban a user from the server")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        user: discord.User,
        *,
        reason: str = "No reason provided",
    ):
        """Ban A User"""

        # Prevent Banning Yourself/bot
        if user.id == ctx.author.id:
            embed = EmbedBuilder.error("Cannot ban yourself")
            await ctx.send(embed=embed)
            return

        if user.id == self.bot.user.id:
            embed = EmbedBuilder.error("Cannot ban the bot")
            await ctx.send(embed=embed)
            return

        member = ctx.guild.get_member(user.id)
        if member:
            passed, error = await check_hierarchy(ctx, member)
            if not passed:
                embed = EmbedBuilder.error("Cannot ban", error)
                await ctx.send(embed=embed)
                return

        # Ban User
        try:
            await ctx.guild.ban(user, reason=f"{ctx.author} - {reason}")

            # Log To Database
            await self._log_moderation(
                ctx.guild.id, user.id, ctx.author.id, "ban", reason
            )

            # Success message
            embed = EmbedBuilder.success(
                "User Banned",
                f"{user.mention} has been banned",
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention)
            await ctx.send(embed=embed)

            await self._send_mod_log(ctx.guild, embed)

            # DM
            try:
                dm_embed = EmbedBuilder.warning(
                    "Banned from server",
                    f"You have been banned from **{ctx.guild.name}**",
                )
                dm_embed.add_field(name="Reason", value=reason)
                await user.send(embed=dm_embed)
            except discord.Forbidden:
                pass

        except discord.Forbidden:
            embed = EmbedBuilder.error("Permission Denied", "Cannot ban this user")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="kick", help="Kick a user from the server")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str = "No reason provided",
    ):
        """Kick User"""

        if member.id == ctx.author.id:
            embed = EmbedBuilder.error("Cannot kick yourself")
            await ctx.send(embed=embed)
            return

        passed, error = await check_hierarchy(ctx, member)
        if not passed:
            embed = EmbedBuilder.error("Cannot kick", error)
            await ctx.send(embed=embed)
            return

        try:
            await member.kick(reason=f"{ctx.author} - {reason}")

            await self._log_moderation(
                ctx.guild.id, member.id, ctx.author.id, "kick", reason
            )

            embed = EmbedBuilder.success(
                "User Kicked",
                f"{member.mention} has been kicked",
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            await ctx.send(embed=embed)

            await self._send_mod_log(ctx.guild, embed)

            try:
                await member.send(
                    f"You have been kicked from **{ctx.guild.name}**\nReason: {reason}"
                )

            except discord.Forbidden:
                pass

        except discord.Forbidden:
            embed = EmbedBuilder.error("Permission Denied", "Cannot kick this user")
            await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="timeout", aliases=["mute"], help="Timeout a user (prevent speaking)"
    )
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def timeout(
        self,
        ctx: commands.Context,
        member: discord.Member,
        duration: str,
        *,
        reason: str = "No reason provided",
    ):
        """Timeout"""

        if member.id == ctx.author.id:
            embed = EmbedBuilder.error("Cannot timeout yourself")
            await ctx.send(embed=embed)
            return

        passed, error = await check_hierarchy(ctx, member)
        if not passed:
            embed = EmbedBuilder.error("Cannot timeout", error)
            await ctx.send(embed=embed)
            return

        duration_mapping = {
            "s": 1,
            "m": 60,
            "h": 3600,
            "d": 86400,
            "w": 604800,
        }

        try:
            unit = duration[-1]
            amount = int(duration[:-1])
            seconds = amount * duration_mapping[unit]

        except (ValueError, KeyError):
            embed = EmbedBuilder.error(
                "Invalid Duration", "Use format: `10m`, `1h`, `1d`, `1w`"
            )
            await ctx.send(embed=embed)
            return

        try:
            await member.timeout(
                timedelta(seconds=seconds), reason=f"{ctx.author} - {reason}"
            )

            await self._log_moderation(
                ctx.guild.id, member.id, ctx.author.id, "timeout", reason, seconds
            )

            embed = EmbedBuilder.success(
                "User Timed Out", f"{member.mention} has been timed out"
            )
            embed.add_field(name="Duration", value=f"{amount}{unit}")
            embed.add_field(name="Reason", value=reason, inline=False)
            await ctx.send(embed=embed)

            await self._send_mod_log(ctx.guild, embed)

        except discord.Forbidden:
            embed = EmbedBuilder.error("Permission Denied")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="unban", help="Unban a user")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(
        self,
        ctx: commands.Context,
        user: discord.User,
        *,
        reason: str = "No reason provided",
    ):
        """Unban a user"""

        try:
            await ctx.guild.unban(user, reason=f"{ctx.author} - {reason}")

            embed = EmbedBuilder.success(
                "User Unbanned", f"{user.mention} has been unbanned"
            )
            await ctx.send(embed=embed)

            await self._send_mod_log(ctx.guild, embed)

        except discord.NotFound:
            embed = EmbedBuilder.error("User Not Banned")
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = EmbedBuilder.error("Permission Denied")
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
