import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

# configure logging
logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# env. variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# intents

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    help_command=None # disable default help command
)

@bot.event
async def on_ready():
  "after bot is ready"
  logger.info(f' ✔ Bot connected as --> {bot.user} ')
  logger.info(f' ⑃ Currently serving {len(bot.guilds):^3} guild(s) ')

  # bot status
  await bot.change_presence(
      activity=discord.Activity(
          type=discord.ActivityType.watching,
          name='!help for commands'
      ),
      status=discord.Status.online
  )

@bot.event
async def on_guild_join(guild):
  # when bot joins a new server
  logger.info(f'✨Joined new guild: {guild.name} (id: {guild.id})')
  logger.info(f'📊 Now serving {len(bot.guilds)} guilds in total')

# Final execution

if __name__ == '__main__':
    try:
        logger.info('⚿ Starting bot...')
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f'✕ Bot crashed: {e}')

