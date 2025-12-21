import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_user_table():
    connection = sqlite3.connect(f'{BASE_DIR}/user_warnings.db')
    cursor = connection.cursor()
    cursor.execute('''
          CREATE TABLE IF NOT EXISTS "users_per_guild" (
          "user_id" INTEGER,
          "warning_count" INTEGER,
          "guild_id" INTEGER,
          PRIMARY KEY ("user_id", "guild_id")
          )
    ''')
    connection.commit()
    connection.close()

create_user_table()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print('╭────────────────────────────────╮')
    print('│ SYNC has connected to Discord! │')
    print('╰────────────────────────────────╯')

@bot.event
async def on_message(msg):
    if msg.author.id != bot.user.id :
        await msg.channel.send(f'Interesting! {msg.author.mention}')

@bot.tree.command(name="greet", description="Sends a greeting to the user.")
async def greet(interaction: discord.Interaction):
    username = interaction.user.mention
    await interaction.response.send_message(f'Hello there, {username}')

bot.run(TOKEN)
