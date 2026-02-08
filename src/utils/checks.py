from discord.ext import commands


def is_admin():
    """Check If User is an Admin"""

    async def check(ctx):
        if not ctx.guild:
            return False
        return ctx.author.guild_permissions.administrator

    return commands.check(check)


def is_moderator():
    """Check If User Is Moderator"""

    async def check(ctx):
        if not ctx.guild:
            return False
        return ctx.author.guild_permissions.manage_messages

    return commands.check(check)


async def check_hierarchy(ctx, member):
    """
    Check if the author and bot have a higher role than the target member.
    Returns (bool, str): (passed, error_message)
    """
    if ctx.author.id == ctx.guild.owner_id:
        return True, None

    if member.top_role >= ctx.author.top_role:
        return False, "Target user has equal or higher role than you"

    if member.top_role >= ctx.guild.me.top_role:
        return False, "Target user has equal or higher role than the bot"

    return True, None
