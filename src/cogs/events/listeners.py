import discord
from discord.ext import commands

from config.logger import setup_logging
from config.settings import Settings
from database.service import DatabaseService

logger = setup_logging()


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

        # Ensure Guild Exists in Database (Check Cache First)
        if message.guild:
            if not self.bot.cache.has_guild(message.guild.id):
                async with self.bot.db_session() as session:
                    db = DatabaseService(session)
                    await db.get_or_create_guild(message.guild.id)
                self.bot.cache.add_guild(message.guild.id)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Handle Member Joining Server"""
        if member.bot:
            return

        logger.info(f"👋 {member} joined {member.guild}")

        # Get Guild Config
        config = self.bot.cache.get_config(member.guild.id)
        if not config:
            async with self.bot.db_session() as session:
                db = DatabaseService(session)
                config = await db.get_guild_config(member.guild.id)
            self.bot.cache.set_config(member.guild.id, config)

        # Send Welcome Message <if enabled>
        if config.welcome_enabled and config.welcome_channel_id:
            channel = member.guild.get_channel(config.welcome_channel_id)

            if channel:
                # Safe formatting
                raw_message = config.welcome_message or Settings.DEFAULT_WELCOME_MESSAGE
                welcome_message = (
                    raw_message.replace("{member}", member.mention)
                    .replace("{server}", member.guild.name)
                    .replace("{count}", str(member.guild.member_count))
                )

                try:
                    await channel.send(welcome_message)
                except discord.Forbidden:
                    logger.warning(f"Cannot send message to {channel}")

        # Auto-assign role if configured
        if config.auto_role_id:
            role = member.guild.get_role(config.auto_role_id)
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
            if owner:
                embed = discord.Embed(
                    title="Thanks for adding me!",
                    description=f"I'm now in **{guild.name}**",
                    color=discord.Color.from_rgb(80, 60, 127),
                )
                embed.add_field(
                    name="Get Started", value="Use `!help` to see all commands "
                )
                await owner.send(embed=embed)
            else:
                logger.warning(f"No owner found for {guild}")
        except discord.Forbidden:
            logger.warning(f"Cannot DM owner of {guild}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        """Handle bot leaving guild"""
        logger.info(f"😢 Bot left {guild.name} ({guild.id})")
        logger.info(f"📉 Now serving {len(self.bot.guilds)} guilds")


async def setup(bot):
    await bot.add_cog(EventListeners(bot))
