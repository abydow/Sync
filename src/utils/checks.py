from discord.ext import commands


def is_admin():
    """Check If User is an Admin"""

    async def check(ctx):
        return ctx.author.guild_permissions.administrator

    return commands.check(check)


def is_moderator():
    """Check If User Is Moderator"""

    async def check(ctx):
        return ctx.author.guild_permissions.manage_messages

    return commands.check(check)
