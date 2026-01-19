import logging

import discord
from discord.ext import commands

from database.service import DatabaseService

logger = logging.getLogger(__name__)


class EventListeners(commands.Cog):
    """Core Event Listeners"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Handle All Messages"""

        # Ignore Bot Messages
        if message.author.bot:
            return

        # Ensure Guild Exists in Database
        if message.guild:
            async with self.bot.db_session() as session:
                db = DatabaseService(session)
                await db.get_or_create_guild(message.guild.id)

        # Process Commands (required  for command framework to work)
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Handle Member Joining Server"""

        logger.info(f"👋 {member} joined {member.guild}")

        # Get Guild Config
        async with self.bot.db_session() as session:
            db = DatabaseService(session)
            config = await db.get_guild_config(member.guild.id)

        # Send Welcome Message <if enabled>
        if config["welcome_enabled"] and config["welcome_channel_id"]:
            channel = member.guild.get_channel(config["welcome_channel_id"])

            if channel:
                welcome_message = config["welcome_message"].format(
                    member=member.mention,
                    server=member.guild.name,
                    count=member.guild.member_count,
                )

                try:
                    await channel.send(welcome_message)
                except discord.Forbidden:
                    logger.warning(f"Cannot send message to {channel}")

        # Auto-assign role if configured
        if config["auto_role_id"]:
            role = member.guild.get_role(config["auto_role_id"])
            if role:
                try:
                    await member.add_roles(role)
                    logger.info(f"Assigned role {role} to {member}")
                except discord.Forbidden:
                    logger.warning(f"Cannot assign role to {member}")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Handle Member Leaving Server"""
        logger.info(f"👋 {member} left {member.guild}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Handle Bot Joining New guild"""
        logger.info(f"✨ Bot joined {guild.name} ({guild.id})")
        logger.info(f"📈 Now serving {len(self.bot.guilds)} guilds")

        # Create Guild Config
        async with self.bot.db_session() as session:
            db = DatabaseService(session)
            await db.get_or_create_guild(guild.id)

        # Send Welcome DM to owner
        try:
            owner = guild.owner
            embed = discord.Embed(
                title="Thanks for adding me!",
                description=f"I'm now in **{guild.name}**",
                color=discord.Color.green(),
            )
            embed.add_field(
                name="Get Started", value="Use `!help` to see all commands "
            )
            await owner.send(embed=embed)
        except discord.Forbidden:
            logger.warning(f"Cannot DM owner of {guild}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        """Handle bot leaving guild"""
        logger.info(f"😢 Bot left {guild.name} ({guild.id})")
        logger.info(f"📉 Now serving {len(self.bot.guilds)} guilds")


async def setup(bot):
    await bot.add_cog(EventListeners(bot))
