import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import sys

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
  logger.info('╭──────────────────────────────────╮')
  logger.info(f'│ ✔ Bot connected as --> {bot.user} │')
  logger.info(f'│ ⑃ Currently serving {len(bot.guilds):^3} guild(s) │')
  logger.info('╰──────────────────────────────────╯')

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



# Totally made for CLI fun not related to bot functionality
'''
colors = [
'\033[38;2;99;0;191m', '\033[38;2;112;0;197m', '\033[38;2;125;0;203m', '\033[38;2;138;0;209m',
    '\033[38;2;151;0;215m', '\033[38;2;164;0;221m', '\033[38;2;177;0;227m', '\033[38;2;190;0;233m',
    '\033[38;2;203;0;239m', '\033[38;2;216;0;245m', '\033[38;2;229;0;251m', '\033[38;2;242;0;255m',
    '\033[38;2;200;50;255m', '\033[38;2;160;100;255m', '\033[38;2;120;150;255m', '\033[38;2;80;200;255m',
    '\033[38;2;40;240;255m', '\033[38;2;0;255;255m', '\033[38;2;0;255;220m', '\033[38;2;0;255;180m',
    '\033[38;2;0;255;140m', '\033[38;2;0;255;100m', '\033[38;2;0;255;60m', '\033[38;2;0;255;20m'
]
reset = '\033[0m'


ascii_art ="""
                 ░                                       ░
                ░█                                       █░
              ░░██                                       ██░░
           ░░████   ███████╗██╗   ██╗███╗   ██╗ ██████╗   ████░░
         ░██████    ██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝    █████░
        ░███████    ███████╗ ╚████╔╝ ██╔██╗ ██║██║         ███████░
       ░████████    ╚════██║  ╚██╔╝  ██║╚██╗██║██║         ████████░
       ░██████████  ███████║   ██║   ██║ ╚████║╚██████╗  ██████████░
       ░██████████░ ╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝ ░██████████░
        ░███████████░             🅶🅴🆃🆃🅸🅽🅶             ░███████████░
         ░█████████████░░          🆁🅴🅰🅳🆈          ░░█████████████░
           ░░██████████████████████████████████████████████████░░
            ░░░░████████████████████████████████████████████░░░░
               ░░░░░████████████████████████████████████░░░░░




"""
def print_colored():
    # Split by line so we can apply color based on vertical position for a smooth blend
    lines = ascii_art.splitlines()
    for i, line in enumerate(lines):
        # Pick a color based on which line we are on
        color = colors[i % len(colors)]
        for char in line:
            if char not in [' ', '░']:
                sys.stdout.write(f"{color}{char}{reset}")
            else:
                # Keep decorative borders slightly dimmer or just standard
                sys.stdout.write(f"{char}")
        sys.stdout.write('\n')
        sys.stdout.flush()
'''


# Final execution

if __name__ == '__main__':
    try:
        #print_colored()
        logger.info('⚿ Starting bot...')
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f'✕ Bot crashed: {e}')

