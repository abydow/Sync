import discord
from discord.ext import commands


class BasicCommands(commands.Cog):
    # Basic utility commands

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="ping",
        aliases=["latency", "pong"],
        help="Check the bot's latency.",
    )
    async def ping(self, ctx: commands.Context):
        # Bot latency
        latency_ms = round(self.bot.latency * 1000)
        await ctx.send(f" 🏓 Pong! Latency: **{latency_ms}ms**")

    @commands.command(
        name="info",
        help="Get information about the bot.",
    )
    async def info(self, ctx: commands.Context):
        # Bot info
        info_text = f"""
**🤖 Bot Information**
• Name: {self.bot.user.name}
• ID: {self.bot.user.id}
• Guilds: {len(self.bot.guilds)}
• Users: {sum(g.member_count for g in self.bot.guilds)}
• Latency: {round(self.bot.latency * 1000)}ms
"""
        await ctx.send(info_text)

    @commands.command(
        name="userinfo",
        aliases=["user", "memberinfo"],
        help="Get information about a user.",
    )
    async def user_info(self, ctx: commands.Context, member: discord.Member = None):
        # show user info
        member = member or ctx.author

        info_text = f"""
**👤 User Information**
• Name: {member.name}
• Display Name: {member.display_name}
• ID: {member.id}
• Created At: {member.created_at.strftime("%Y-%m-%d %H:%M")}
• Bot: {"Yes" if member.bot else "No"}
• Avatar: [Link]({member.display_avatar.url})
"""
        if ctx.guild and isinstance(member, discord.Member):
            info_text += "\n** 🫱🏼‍🫲🏾 Guild Member info**\n"
            info_text += f"• Joined : {member.joined_at.strftime('%Y-%m-%d %H:%M')}\n"
            info_text += f"• Nickname: {member.nick or 'None'}\n"
            info_text += f"• Top Role: {member.top_role.mention}\n"

            # Show roles (highest to lowest, excluding @everyone)
            roles = member.roles[1:][::-1]
            role_mentions = [r.mention for r in roles[:10]]
            info_text += f"• Roles ({len(roles)}): {', '.join(role_mentions) or 'None'}"

            if len(roles) > 10:
                info_text += f" ... and {len(roles) - 10} more"

        await ctx.send(info_text)

    @commands.command(
        name="serverinfo",
        aliases=["guildinfo", "server", "guild"],
        help="Get information about the server.",
    )
    async def server_info(self, ctx: commands.Context):
        # Show server information
        guild = ctx.guild

        text_channels = len(
            [c for c in guild.channels if isinstance(c, discord.TextChannel)]
        )
        voice_channels = len(
            [c for c in guild.channels if isinstance(c, discord.VoiceChannel)]
        )
        roles = len(guild.roles)
        info_text = f"""
**🏰 Server Information**

• Name: {guild.name}
• ID: {guild.id}
• Owner: {guild.owner.mention if guild.owner else "Unknown"}
• Created : {guild.created_at.strftime("%Y-%m-%d %H:%M")}
• Members: {guild.member_count}
• Channels: {text_channels} text, {voice_channels} voice
• Roles: {roles}
• Verification : {guild.verification_level}
"""
        await ctx.send(info_text)


# Setup


async def setup(bot):
    await bot.add_cog(BasicCommands(bot))
