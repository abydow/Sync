import logging
from datetime import timedelta

import discord
from discord.ext import commands

from database.service import DatabaseService
from utils.checks import is_moderator
from utils.embeds import EmbedBuilder

logger = logging.getlogger(__name__)


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
            db = DatabaseService(session)

            pass

    async def _send_mod_log(self, guild: discord.Guild, embed: discord.Embed):
        """Send Moderation Log To Mod Channel"""
        async with self.bot.db_session() as session:
            db = DatabaseService(session)
            config = await db.get_guild_config(guild.id)

        if not config["modlog_channel_id"]:
            return

        mod_channel = guild.get_channel(config["modlog_channel_id"])
        if mod_channel:
            try:
                await mod_channel.send(embed=embed)
            except discord.Forbidden:
                logger.warning(f"Cannot send to mod log in {guild}")

    @commands.hybrid_command(name="ban", help="Ban a user from the server")
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

        # Ban User
