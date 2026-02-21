import logging

import discord
from discord.ext import commands
from sqlalchemy.exc import SQLAlchemyError

from utils.embeds import EmbedBuilder

logger = logging.getLogger(__name__)


class ErrorHandler(commands.Cog):
    """Global Error Handling Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        """Handle Command Errors"""

        if hasattr(ctx.command, "on_error"):
            return

        # non-errors
        if isinstance(error, commands.CommandNotFound):
            return

        # original error if it's wrapped
        error = getattr(error, "original", error)

        if isinstance(error, commands.MissingRequiredArgument):
            embed = EmbedBuilder.warning(
                ctx,
                title="Missing Argument",
                description=f"You missed a required argument: `{error.param.name}`",
            )
            await ctx.send(embed=embed)

        elif isinstance(error, SQLAlchemyError):
            logger.error("Database Error:", exc_info=error)
            embed = EmbedBuilder.error(
                ctx,
                title="Database Error",
                description="A database error occurred. Please try again later.",
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_permissions
            ]
            embed = EmbedBuilder.error(
                ctx,
                title="Missing Permissions",
                description=f"I need the following permissions to run this command:\n**{', '.join(missing)}**",
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_permissions
            ]
            embed = EmbedBuilder.error(
                ctx,
                title="Access Denied",
                description=f"You do not have the required permissions:\n**{', '.join(missing)}**",
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                embed = EmbedBuilder.warning(
                    ctx,
                    title="No Private Messages",
                    description="This command cannot be used in private messages.",
                )
                await ctx.author.send(embed=embed)
            except discord.Forbidden:
                pass

        elif isinstance(error, commands.BadArgument):
            embed = EmbedBuilder.warning(
                ctx,
                title="Invalid Argument",
                description=f"Could not parse arguments. Please check your input.\nError: `{str(error)}`",
            )
            await ctx.send(embed=embed)

        elif isinstance(error, discord.Forbidden):
            embed = EmbedBuilder.error(
                ctx,
                title="Permission Denied",
                description="I do not have the necessary permissions to perform this action.",
            )
            try:
                await ctx.send(embed=embed)
            except discord.Forbidden:
                pass  # Cannot send message to channel

        elif isinstance(error, discord.HTTPException):
            embed = EmbedBuilder.error(
                ctx,
                title="API Error",
                description="An unexpected error occurred while communicating with Discord.",
            )
            await ctx.send(embed=embed)

        else:
            # Log unknown errors
            logger.error(
                f"Ignoring exception in command {ctx.command}:", exc_info=error
            )
            embed = EmbedBuilder.error(
                ctx,
                title="Unexpected Error",
                description=f"An error occurred while running this command.\n`{str(error)[:200]}`",
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
