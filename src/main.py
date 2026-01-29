import os

import discord
from discord.ext import commands

from config.logger import setup_logging
from config.settings import Settings
from database import AsyncSessionLocal, init_db

# Configure Logging
logger = setup_logging()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


# Bot class
class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=Settings.PREFIX,
            intents=intents,
            help_command=None,
            owner_ids=set(Settings.OWNER_IDS) if Settings.OWNER_IDS else set(),
        )
        self.db_session = AsyncSessionLocal

    async def setup_hook(self):
        """Initialize database and load cogs"""
        # Database
        await init_db()
        logger.info("✔ Database Initialized")

        # Load Cogs
        await self.load_cogs()

    async def load_cogs(self):
        """Recursively load cogs from src/cogs"""
        cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")

        count = 0
        for root, _, files in os.walk(cogs_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    # Calculate module path relative to src
                    # e.g. src/cogs/admin/help.py -> cogs.admin.help

                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(
                        full_path, os.path.dirname(__file__)
                    )
                    module_name = relative_path.replace(os.sep, ".")[:-3]

                    try:
                        await self.load_extension(module_name)
                        logger.info(f"✔ Loaded cog: {module_name}")
                        count += 1
                    except Exception as e:
                        logger.error(f"✕ Failed to load cog {module_name}: {e}")

        logger.info(f"Loaded {count} cogs")

    async def on_ready(self):
        """Bot Startup Event"""
        logger.info(f"✔ Bot connected as --> {self.user}")
        logger.info(f"⑃ Currently serving {len(self.guilds)} guild(s)")

        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"{Settings.PREFIX}help"
            ),
            status=discord.Status.online,
        )


# Instance
bot = DiscordBot()

if __name__ == "__main__":
    try:
        # Validate critical settings
        Settings.validate()
        logger.info("⚿ Starting bot...")
        bot.run(Settings.DISCORD_TOKEN)
    except ValueError as e:
        logger.critical(f"Configuration Error: {e}")
    except Exception as e:
        logger.critical(f"Bot crashed: {e}", exc_info=True)
