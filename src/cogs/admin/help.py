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
                    ctx,
                    "Command Not Found",
                    f"Command `{command_name}` does not exist.",  # working properly
                )
                await ctx.send(embed=embed)
                return

            # Build Command Help
            embed = discord.Embed(
                title=f"📖 {command.name.capitalize()}",
                description=f">>> {command.help or 'No description available'}",
                color=discord.Color.from_rgb(88, 101, 242),
            )

            if command.aliases:
                aliases = " • ".join(f"`{alias}`" for alias in command.aliases)
                embed.add_field(name="🔗 Aliases", value=aliases, inline=False)

            # To Show Usage
            usage = f"{ctx.clean_prefix}{command.qualified_name}"
            if command.signature:
                usage += f" {command.signature}"

            embed.add_field(
                name="📝 Usage", value=f"```fix\n{usage}\n```", inline=False
            )

            embed.set_footer(
                text=f"💬 Requested by {ctx.author.name} • Use {ctx.clean_prefix}help for all commands",
                icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
            )

            embed.timestamp = discord.utils.utcnow()

            if self.bot.user.avatar:
                embed.set_thumbnail(url=self.bot.user.avatar.url)

            await ctx.send(embed=embed)

        else:
            """Show All Commands Grouped by Cog"""
            embed = discord.Embed(
                title="📚 Command Directory",
                description=(
                    f"**Need help?** Use `{ctx.clean_prefix}help [command]` for detailed information\n"
                ),
                color=discord.Color.from_rgb(88, 101, 242),
                timestamp=discord.utils.utcnow(),
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
                command_list = " • ".join(f"`{cmd.name}`" for cmd in commands)

                embed.add_field(
                    name=f"**{cog_name}** ({len(commands)})",
                    value=command_list or "No commands available.",
                    inline=False,
                )

            embed.set_footer(
                text=f"🤖 Total Commands: {len(self.bot.commands)} | Requested by {ctx.author}",
                icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
            )

            if self.bot.user.avatar:
                embed.set_thumbnail(url=self.bot.user.avatar.url)

            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
