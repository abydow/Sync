from typing import Optional

import discord
from discord.ext import commands

from utils.embeds import EmbedBuilder


class HelpCog(commands.Cog):
    """Custom Help Command"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="help",
        aliases=["h", "commands", "?", "cmds", "support"],
        help="Shows Help for Commands.",
    )
    async def help(self, ctx: commands.Context, command_name: Optional[str] = None):
        """Show Help Information"""

        if command_name:
            """Show Help for a Specific Command"""

            command = self.bot.get_command(command_name)

            if not command:
                embed = EmbedBuilder.error(
                    "Command Not Found", f"Command `{command_name}` does not exist."
                )
                await ctx.send(embed=embed)
                return

            # Build Command Help
            embed = discord.Embed(
                title=f"Help: {command.name}", color=discord.Color.blue()
            )

            if command.help:
                embed.description = command.help

            if command.aliases:
                embed.add_field(
                    name="Aliases", value=", ".join(command.aliases), inline=False
                )

            # To Show Usage
