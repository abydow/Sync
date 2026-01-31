import logging
from datetime import timedelta

import discord
from discord.ext import commands

from database.service import DatabaseService
from utils.checks import is_moderator
from utils.embeds import EmbedBuilder

loggger = logging.getlogger(__name__)

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
        duration: int = None
    ):
