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
            usage = f"{ctx.clean_prefix}{command.qualified_name}"
            if command.signature:
                usage += f" {command.signature}"

            embed.add_field(name="Usage", value=f"```{usage}```", inline=False)

            await ctx.send(embed=embed)

        else:
            """Show All Commands Grouped by Cog"""
            embed = discord.Embed(
                title="📚 Help",
                description=f"Use `{ctx.clean_prefix}help [command]` for more info",
                color=discord.Color.blue(),
            )

            cogs = {}

            for command in self.bot.commands:
                # Skip Hidden Commands
                if command.hidden:
                    continue

                # Get Cog Name
                cog_name = command.cog.qualified_name if command.cog else "Other"

                if cog_name not in cogs:
                    cogs[cog_name] = []

                cogs[cog_name].append(command)

            # Add Fields For Each Cog
            for cog_name, commands in sorted(cogs.items()):
                command_list = ", ".join(f"`{cmd.name}`" for cmd in commands)
                embed.add_field(
                    name=f"**{cog_name}**",
                    value=command_list,
                    inline=False,
                )

            embed.set_footer(text=f"Total commands: {len(self.bot.commands)}")

            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
