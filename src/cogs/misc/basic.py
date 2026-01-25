import discord
from discord.ext import commands

from utils.embeds import EmbedBuilder


class BasicCommands(commands.Cog):
    # Basic utility commands

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        # Bot latency
        latency_ms = round(self.bot.latency * 1000)
        embed = EmbedBuilder.info("Latency", f"🏓 Pong!**{latency_ms}ms**")
        await ctx.send(embed=embed)

    @commands.command(name="info")
    async def info(self, ctx: commands.Context):
        # Bot info
        embed = discord.Embed(title="🤖 Bot Information", color=discord.Color.blue())
        embed.add_field(name="Name", value=self.bot.user.name, inline=False)
        embed.add_field(name="ID", value=self.bot.user.id, inline=False)
        embed.add_field(name="Guilds", value=len(self.bot.guilds), inline=False)
        embed.add_field(
            name="Users",
            value=sum(g.member_count for g in self.bot.guilds),
            inline=False,
        )
        embed.add_field(
            name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="userinfo")
    async def user_info(self, ctx: commands.Context, member: discord.Member = None):
        # show user info
        member = member or ctx.author

        embed1 = discord.Embed(
            title="👤 User Information", color=discord.Color.blurple()
        )
        embed1.add_field(name="Name", value=member.name, inline=False)
        embed1.add_field(name="Display Name", value=member.display_name, inline=False)
        embed1.add_field(name="ID", value=member.id, inline=False)
        embed1.add_field(
            name="Created At",
            value=member.created_at.strftime("%Y-%m-%d %H:%M"),
            inline=False,
        )
        embed1.add_field(name="Bot", value="Yes" if member.bot else "No", inline=False)
        embed1.set_image(url=member.display_avatar.url)

        if ctx.guild and isinstance(member, discord.Member):
            embed2 = discord.Embed(
                title="🫱🏼‍🫲🏾 Guild Member info", color=discord.Color.magenta()
            )
            embed2.add_field(
                name="Joined",
                value=member.joined_at.strftime("%Y-%m-%d %H:%M"),
                inline=False,
            )
            embed2.add_field(name="Nickname", value=member.nick or "None", inline=False)
            embed2.add_field(
                name="Top Role", value=member.top_role.mention, inline=False
            )

            # Show roles (highest to lowest, excluding @everyone)
            roles = member.roles[1:][::-1]
            role_mentions = [r.mention for r in roles[:10]]
            embed2.add_field(
                name="Roles",
                value=f"{(len(member.roles) - 1)}: {', '.join(role_mentions) or 'None'}",
            )

            if len(roles) > 10:
                embed2.add_field(name=f" ... and {len(roles) - 10} more")

        await ctx.send(embeds=[embed1, embed2] if "embed2" in locals() else [embed1])

    @commands.command(name="serverinfo")
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
        embed = discord.Embed(
            title="🏰 Server Information", color=discord.Color.green()
        )
        embed.add_field(name="Name", value=guild.name, inline=False)
        embed.add_field(name="ID", value=guild.id, inline=False)
        embed.add_field(
            name="Owner",
            value=guild.owner.mention if guild.owner else "Unknown",
            inline=False,
        )
        embed.add_field(
            name="Created",
            value=guild.created_at.strftime("%Y-%m-%d %H:%M"),
            inline=False,
        )
        embed.add_field(name="Members", value=guild.member_count, inline=False)
        embed.add_field(
            name="Channels",
            value=f"{text_channels} text channels, {voice_channels} voice channels",
            inline=False,
        )
        embed.add_field(name="Roles", value=roles, inline=False)
        embed.add_field(
            name="Verification Level", value=guild.verification_level, inline=False
        )
        await ctx.send(embed=embed)


# Setup


async def setup(bot):
    await bot.add_cog(BasicCommands(bot))
