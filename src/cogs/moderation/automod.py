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
        """Check for Spam"""
