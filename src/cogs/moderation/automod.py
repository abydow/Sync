import logging
from datetime import timedelta

import discord
from discord.ext import commands

from config.settings import settings
from services.antispam import AntiSpamService
from services.moderation import ModerationService
from utils.embeds import EmbedBuilder

logger = logging.getLogger(__name__)


class AutoModCog(commands.Cog):
    # Automated Moderation System

    def __init__(self, bot):
        self.bot = bot
        self.antispam = AntiSpamService()

    def _is_immune(self, member: discord.Member) -> bool:
        # If user is immune to Automod
        if member.bot:
            return True
        if (
            member.guild_permissions.administrator
            or member.guild_permission.manage_messages
        ):
            return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.guild or not isinstance(message.author, discord.Member):
            return

        #!TODO:
        """Immunity Check"""
        if self._is_immune(message.author):
            return
        """Check for Spam"""
        is_spam, reason = self.antispam.check_spam(message)

        if is_spam:
            await self._punish_spammer(message, reason)

    async def _punish_spammer(self, message: discord.Message, reason: str):
        """Punish the spammer based on the reason"""
        member = message.author
        guild = message.guild

        logger.info(f"AutoMod detected spam from {member} in {guild}: {reason}")

        # Timeout (10min)

        try:
            duration = timedelta(minutes=10)
            await member.timeout(duration, reason=f"[AutoMod] {reason}")
        except discord.Forbidden:
            logger.warning(f"Failed to timeout {member} in {guild}")
            return

        # Delete recent messages (Cleanup)
        try:
            await
