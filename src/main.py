import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from database import init_db

# configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# env. variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# intents

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,  # disable default help command
)


@bot.event
async def on_ready():
    "after bot is ready"
    logger.info(f" ✔ Bot connected as --> {bot.user} ")
    logger.info(f" ⑃ Currently serving {len(bot.guilds):^3} guild(s) ")

    # bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="!help for commands"
        ),
        status=discord.Status.online,
    )


@bot.event
async def on_guild_join(guild):
    # when bot joins a new server
    logger.info(f"✨Joined new guild: {guild.name} (id: {guild.id})")
    logger.info(f"📊 Now serving {len(bot.guilds)} guilds in total")


@bot.event
async def setup_hook():
    """Initialize database and load cogs"""
    # database

    await init_db()
    logger.info("✔ Database Initialized")

    # load cogs
    cog_files = []

    # Recursively find all cog files in src/cogs

    for root, dirs, files in os.walk(os.path.join("src", "cogs")):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                # Convert file path to module name
                path = os.path.relpath(os.path.join(root, file), "src")
                module = path.replace(os.sep, ".")[:-3]  # remove .py
                cog_files.append(module)

    # Now We have to load each cog

    for cog in cog_files:
        try:
            await bot.load_extension(cog)
            logger.info(f" ✔ Loaded cog: {cog} ")
        except Exception as e:
            logger.error(f" ✕ Failed to load cog {cog}: {e} ")


# Error handling
@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    # command error handler
    if isinstance(error, commands.CommandNotFound):
        return  # ignore unknown commands
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠ Missing argument: {error.param.name}")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(
            f"⚠ I do not have the required permission : {', '.join(error.missing_permissions)}"
        )
    else:
        logger.error(f"✕ Error in command : {error}")
        await ctx.send(
            f"⚠ An error :{str(error)[:100]} occurred while processing the command"
        )


# Final execution

if __name__ == "__main__":
    try:
        logger.info("⚿ Starting bot...")
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"✕ Bot crashed: {e}")
